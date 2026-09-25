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
  
  /** Vista actual (enrutador simplificado) */
  protected readonly vista = signal<'login' | 'registro'>('login');

  protected cambiarVista(nuevaVista: 'login' | 'registro') {
    this.error.set('');
    this.vista.set(nuevaVista);
  }

  protected async registrar(email: string, nombre: string, apellidos: string): Promise<void> {
    if (!email.trim() || !nombre.trim() || !apellidos.trim()) {
      return this.error.set('Todos los campos son obligatorios');
    }
    this.error.set('');
    this.cargando.set(true);
    try {
      await this.auth.registrar(email.trim(), nombre.trim(), apellidos.trim());
    } catch (fallo) {
      this.error.set((fallo as Error).message);
    } finally {
      this.cargando.set(false);
    }
  }

  protected async entrar(): Promise<void> {
    this.error.set('');
    this.cargando.set(true);
    try {
      await this.auth.entrar();
    } catch (fallo) {
      this.error.set((fallo as Error).message);
    } finally {
      this.cargando.set(false);
    }
  }
}
