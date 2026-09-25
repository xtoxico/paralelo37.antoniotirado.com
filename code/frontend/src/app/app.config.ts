import { ApplicationConfig, provideBrowserGlobalErrorListeners } from '@angular/core';

// Configuración mínima: sin router y sin HttpClient, porque usamos fetch directamente.
// Angular 22 arranca sin Zone.js por defecto, así que tampoco hay nada que configurar ahí.
export const appConfig: ApplicationConfig = {
  providers: [provideBrowserGlobalErrorListeners()],
};
