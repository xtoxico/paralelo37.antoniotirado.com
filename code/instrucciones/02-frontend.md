# 02 · Frontend con Angular 22

> Tiempo en el taller: **20 minutos**. Un servicio y un componente. Y sobra código.

## Paso 1 · Crear el proyecto

```bash
ng new frontend --style=css --ssr=false --skip-tests --package-manager=npm
cd frontend
```

Si no tienes el CLI instalado globalmente, usa `npx @angular/cli@22 new ...`.

> **Dos novedades de Angular 22** que vas a ver en este código:
> - El CLI genera servicios con `@Service()` en lugar de `@Injectable({ providedIn: 'root' })`.
> - La aplicación arranca **zoneless** por defecto: no hay Zone.js y el estado va con *signals*.

## Paso 2 · Instalar SimpleWebAuthn

```bash
npm i @simplewebauthn/browser
```

Una sola dependencia. Nos ahorra todas las conversiones entre `ArrayBuffer` y base64url, que es
exactamente la parte tediosa de WebAuthn a pelo.

## Paso 3 · Generar el servicio

```bash
ng generate service auth
```

Esto crea `src/app/auth.ts` con la clase vacía.

## Paso 4 · Limpiar lo que no usamos

Para dejar el proyecto en lo mínimo:

```bash
rm src/app/app.routes.ts
```

No hay router (una sola pantalla) ni `HttpClient` (usamos `fetch` nativo). `src/app/app.config.ts`
queda así:

```typescript
import { ApplicationConfig, provideBrowserGlobalErrorListeners } from '@angular/core';

// Configuración mínima: sin router y sin HttpClient, porque usamos fetch directamente.
// Angular 22 arranca sin Zone.js por defecto, así que tampoco hay nada que configurar ahí.
export const appConfig: ApplicationConfig = {
  providers: [provideBrowserGlobalErrorListeners()],
};
```

## Paso 5 · `src/app/auth.ts` — el servicio

Aquí vive **todo** el WebAuthn del frontend. Fíjate en que los dos métodos públicos tienen
exactamente la misma forma: pedir opciones, llamar al autenticador, enviar el resultado.

```typescript
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
  async registrar(usuario: string): Promise<void> {
    // 1) Pedimos el reto y las opciones al backend.
    const opciones = await this.post<PublicKeyCredentialCreationOptionsJSON>('register/begin', {
      usuario,
    });
    // 2) El navegador abre el diálogo nativo: huella, Face ID, PIN o llave USB.
    //    Aquí es donde nace el par de claves. La privada NO sale del dispositivo.
    const credencial = await startRegistration({ optionsJSON: opciones });
    // 3) Mandamos al servidor únicamente la clave pública firmada.
    await this.post('register/complete', { usuario, credencial });
    this.usuario.set(usuario);
  }

  /** LOGIN: mismo baile, pero ahora el autenticador FIRMA en vez de crear claves. */
  async entrar(usuario: string): Promise<void> {
    const opciones = await this.post<PublicKeyCredentialRequestOptionsJSON>('login/begin', {
      usuario,
    });
    const credencial = await startAuthentication({ optionsJSON: opciones });
    await this.post('login/complete', { usuario, credencial });
    this.usuario.set(usuario);
  }

  /** Cerrar sesión es, literalmente, olvidar el nombre. No hay ningún secreto que borrar. */
  salir(): void {
    this.usuario.set(null);
  }
}
```

## Paso 6 · `src/app/app.ts` — el componente

```typescript
// Component define el componente; inject() obtiene el servicio sin constructor.
import { Component, inject, signal } from '@angular/core';
// Nuestro servicio de autenticación: todo el WebAuthn vive ahí.
import { Auth } from './auth';

@Component({
  selector: 'app-root',
  templateUrl: './app.html',
  styleUrl: './app.css',
})
export class App {
  /** El servicio es público para poder leerlo directamente desde la plantilla. */
  protected readonly auth = inject(Auth);
  /** Mensaje de error visible; cadena vacía significa "todo bien". */
  protected readonly error = signal('');
  /** Mientras el autenticador piensa, bloqueamos los botones. */
  protected readonly cargando = signal(false);

  /**
   * Un único método para los dos botones: 'registrar' y 'entrar' son métodos del
   * servicio con la misma firma, así que los invocamos por nombre.
   */
  protected async accion(tipo: 'registrar' | 'entrar', usuario: string): Promise<void> {
    // Sin nombre de usuario no hay nada que hacer.
    if (!usuario.trim()) return this.error.set('Escribe un nombre de usuario');
    this.error.set('');
    this.cargando.set(true);
    try {
      await this.auth[tipo](usuario.trim());
    } catch (fallo) {
      // Aquí caen tanto los errores del backend como los del navegador
      // (por ejemplo, NotAllowedError cuando la persona cancela el diálogo).
      this.error.set((fallo as Error).message);
    } finally {
      this.cargando.set(false);
    }
  }
}
```

## Paso 7 · `src/app/app.html` — la plantilla

```html
<main>
  <h1>Entra sin contraseña</h1>

  <!-- Caso 1: navegador antiguo. Avisamos en vez de fallar sin explicación. -->
  @if (!auth.soportado) {
    <p class="error">Este navegador no soporta WebAuthn. Prueba con Chrome, Edge o Safari.</p>
  }
  <!-- Caso 2: ya hay sesión. El "as" nos da el nombre sin volver a leer la señal. -->
  @else if (auth.usuario(); as usuario) {
    <p class="ok">Hola, <strong>{{ usuario }}</strong>. Has entrado sin escribir ni una contraseña.</p>
    <button (click)="auth.salir()">Salir</button>
  }
  <!-- Caso 3: pantalla inicial. Un campo y dos botones: eso es todo el formulario. -->
  @else {
    <input #nombre placeholder="Nombre de usuario" (keyup.enter)="accion('entrar', nombre.value)" />
    <button [disabled]="cargando()" (click)="accion('registrar', nombre.value)">Registrarme</button>
    <button [disabled]="cargando()" (click)="accion('entrar', nombre.value)">Entrar</button>
  }

  <!-- El error solo aparece cuando hay algo que contar. -->
  @if (error()) {
    <p class="error">{{ error() }}</p>
  }
</main>
```

> **Busca el campo «contraseña».** No está. Esa es toda la charla en una plantilla de quince líneas.

## Paso 8 · `src/app/app.css` — estilos mínimos

```css
/* Estilos mínimos: lo importante del taller es el flujo, no el CSS. */
main {
  max-width: 28rem;
  margin: 4rem auto;
  padding: 0 1rem;
  font-family: system-ui, sans-serif;
  text-align: center;
}
input,
button {
  font-size: 1rem;
  padding: 0.6rem 1rem;
  margin: 0.25rem;
  border-radius: 0.5rem;
  border: 1px solid #ccc;
}
button {
  cursor: pointer;
  background: #1a73e8;
  color: #fff;
  border: 0;
}
button:disabled {
  opacity: 0.5;
  cursor: wait;
}
.error {
  color: #c5221f;
}
.ok {
  color: #137333;
}
```

## Paso 9 · Arrancar

Con el backend ya corriendo en otra terminal:

```bash
npm start
```

Abre <http://localhost:4200>, escribe un nombre de usuario y pulsa **Registrarme**. El navegador
abrirá el diálogo nativo del sistema: huella, cara, PIN o llave USB.

## Punto de control

Después de registrarte, abre <http://localhost:3000/auth/users>. Deberías ver algo así:

```json
[
  {
    "usuario": "antonio",
    "credenciales": 1,
    "detalle": [
      {
        "id": "YAcDOXlOhfnCFQCy73olwSXM1W_27kMOaeRJZJaulGQ",
        "publicKey": "pAEBAycgBiFYIC2Q1AM5OrfEzLWSbYNAVW4fTCgk4Yz_SriRDmregjda",
        "counter": 0,
        "transports": ["internal"]
      }
    ]
  }
]
```

Pulsa **Salir** y luego **Entrar** con el mismo nombre. Si vuelves a entrar sin escribir ninguna
contraseña, el taller está completo.

## Qué ha pasado realmente

1. `startRegistration()` ha llamado por debajo a `navigator.credentials.create()`.
2. El sistema operativo ha pedido tu huella (o tu PIN) y ha generado un **par de claves nuevo**, único
   para `localhost`.
3. La clave privada se ha quedado en el chip seguro de tu equipo. **No ha salido de ahí y no saldrá.**
4. La pública ha viajado hasta tu Express y está ahora mismo en `usuarios.json`.
5. Al entrar, `startAuthentication()` ha llamado a `navigator.credentials.get()`, el autenticador ha
   firmado el reto y el servidor ha verificado la firma con la clave pública.

En ningún momento ha viajado un secreto por la red.

Siguiente: [`03-probar.md`](03-probar.md)
