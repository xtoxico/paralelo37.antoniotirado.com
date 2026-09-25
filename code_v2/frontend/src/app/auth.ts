// Angular 22: @Service reemplaza al clásico @Injectable({ providedIn: 'root' }).
// signal() es la forma moderna de guardar estado reactivo sin RxJS ni Zone.js.
import { Service, signal } from '@angular/core';
// SimpleWebAuthn nos ahorra toda la conversión de ArrayBuffers a base64url y viceversa.
import {
  startRegistration, // Envuelve a navigator.credentials.create()
  startAuthentication, // Envuelve a navigator.credentials.get()
  browserSupportsWebAuthn, // Comprueba si el navegador conoce la API
} from '@simplewebauthn/browser';
// Tipos de las opciones que fabrica el backend, para tener autocompletado.
import type {
  PublicKeyCredentialCreationOptionsJSON,
  PublicKeyCredentialRequestOptionsJSON,
} from '@simplewebauthn/browser';

// Dirección de nuestro backend Express.
const API = 'http://localhost:3000/auth';

@Service()
export class Auth {
  /** Usuario con la sesión iniciada; null significa "nadie ha entrado todavía". */
  readonly usuario = signal<string | null>(null);

  /** false en navegadores antiguos: nos permite avisar en lugar de fallar en silencio. */
  readonly soportado = browserSupportsWebAuthn();

  /** Único helper de red: un POST con JSON que convierte los errores del backend en excepciones. */
  private async post<T>(ruta: string, cuerpo: unknown): Promise<T> {
    const respuesta = await fetch(`${API}/${ruta}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(cuerpo),
    });
    // Si el servidor ha respondido con un 4xx, levantamos su mensaje tal cual.
    if (!respuesta.ok) throw new Error((await respuesta.json()).error ?? 'Error del servidor');
    return respuesta.json();
  }

  /** REGISTRO: dos viajes al servidor y una llamada al autenticador entre medias. */
  async registrar(email: string, nombre: string, apellidos: string): Promise<void> {
    // 1) Pedimos el reto y las opciones al backend.
    const opciones = await this.post<PublicKeyCredentialCreationOptionsJSON>('register/begin', {
      email,
      nombre,
      apellidos
    });
    // 2) El navegador abre el diálogo nativo: huella, Face ID, PIN o llave USB.
    //    Aquí es donde nace el par de claves. La privada NO sale del dispositivo.
    const credencial = await startRegistration({ optionsJSON: opciones });
    // 3) Mandamos al servidor únicamente la clave pública firmada.
    await this.post('register/complete', { email, credencial });
    this.usuario.set(email);
  }

  /** LOGIN: Auto-discoverable. No pasamos usuario al begin. */
  async entrar(): Promise<void> {
    const opciones = await this.post<PublicKeyCredentialRequestOptionsJSON>('login/begin', {});
    const credencial = await startAuthentication({ optionsJSON: opciones });
    const result = await this.post<{verificado: boolean, usuario: string}>('login/complete', { credencial });
    this.usuario.set(result.usuario);
  }

  /** Cerrar sesión es, literalmente, olvidar el nombre. No hay ningún secreto que borrar. */
  salir(): void {
    this.usuario.set(null);
  }
}

