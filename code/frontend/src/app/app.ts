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
