# Changelog: Evolución a FIDO2 Auto-Discoverable (code_v2)

Este documento detalla **exclusivamente los cambios críticos de lógica** introducidos en la versión 2 para soportar un registro con más datos y un login sin nombre de usuario (Passkeys / Resident Keys). Se han omitido los cambios cosméticos (Tailwind) y de enrutado de Angular.

---

## 1. Backend (`servidor.ts`)

### A. Ampliación del modelo de datos
Para soportar el registro completo, se ha modificado la interfaz del usuario en la base de datos para aceptar nombre y apellidos. El email pasa a ser el identificador principal (clave del diccionario).

```typescript
// Antes
type Usuario = { reto: string; credenciales: Credencial[] };

// Ahora
type Usuario = { 
  reto: string; 
  nombre?: string; 
  apellidos?: string; 
  credenciales: Credencial[] 
};
```

### B. Registro: Obligar a crear "Resident Keys"
Para que el usuario pueda hacer login en el futuro sin tener que escribir quién es, la llave/dispositivo tiene que almacenar obligatoriamente la credencial de forma interna. Esto se logra cambiando la propiedad `residentKey` de FIDO2.

```typescript
// En /auth/register/begin
const opciones = await generateRegistrationOptions({
  rpName,
  rpID,
  userName: email, // El email es ahora el identificador FIDO
  // ...
  authenticatorSelection: {
    residentKey: 'required', // ANTES: 'preferred'. Ahora OBLIGAMOS a que sea Discoverable.
    userVerification: 'preferred',
  },
});
```

### C. Login (Paso 1): Eliminar `allowCredentials`
Este es el cambio más importante para el login automático. Si no le pasamos al navegador una lista de credenciales permitidas (`allowCredentials`), el navegador entiende que debe preguntar al usuario con qué Passkey quiere iniciar sesión.

```typescript
// En /auth/login/begin
app.post('/auth/login/begin', async (_peticion, respuesta) => {
  const opciones = await generateAuthenticationOptions({
    rpID,
    // ¡CRÍTICO! Al omitir el array 'allowCredentials', forzamos el modo Discoverable.
    // El SO abrirá el diálogo preguntando: "¿Con qué cuenta quieres entrar?"
    userVerification: 'preferred',
  });

  // Como no sabemos quién está intentando entrar, guardamos el reto de forma global
  // (En producción, esto iría ligado a una cookie de sesión temporal).
  retoGlobalLogin = opciones.challenge;
  
  respuesta.json(opciones);
});
```

### D. Login (Paso 2): Resolución de Identidad en el Backend
Como en el paso 1 no pedimos el email, cuando el frontend nos devuelve la firma de FIDO2 (`/auth/login/complete`), el servidor tiene que averiguar a quién pertenece.

```typescript
// En /auth/login/complete
const firma: AuthenticationResponseJSON = peticion.body.credencial;
const bd = leerBD();

let usuarioEncontrado = '';
let credencialEncontrada = null;

// Buscamos iterando toda la base de datos quién tiene el ID de credencial que acaba de firmar
for (const [email, datos] of Object.entries(bd)) {
  const c = datos.credenciales.find((cred) => cred.id === firma.id);
  if (c) {
    usuarioEncontrado = email;
    credencialEncontrada = c;
    break;
  }
}

// Si lo encontramos, procedemos a verificar la firma con la clave pública de ese usuario.
// ...
```

---

## 2. Frontend (`auth.ts`)

### A. Registro extendido
El método que dispara el registro ahora envía toda la información recopilada del formulario.

```typescript
// Antes
async registrar(usuario: string): Promise<void> { ... }

// Ahora
async registrar(email: string, nombre: string, apellidos: string): Promise<void> {
  const opciones = await this.post<PublicKeyCredentialCreationOptionsJSON>('register/begin', {
    email,
    nombre,
    apellidos
  });
  // ... (startRegistration) ...
  await this.post('register/complete', { email, credencial });
  this.usuario.set(email);
}
```

### B. Login "Zero-Input"
El frontend ya no necesita recoger el nombre de usuario de ningún campo de texto. Llama al inicio de login vacío y confía en el diálogo del sistema operativo.

```typescript
// Antes
async entrar(usuario: string): Promise<void> { ... }

// Ahora
async entrar(): Promise<void> {
  // Ya no pasamos ningún identificador al backend
  const opciones = await this.post<PublicKeyCredentialRequestOptionsJSON>('login/begin', {});
  
  // startAuthentication levanta la UI del SO para que el usuario elija su cuenta
  const credencial = await startAuthentication({ optionsJSON: opciones });
  
  // El backend verifica y nos devuelve el nombre del usuario resuelto
  const result = await this.post<{verificado: boolean, usuario: string}>('login/complete', { credencial });
  this.usuario.set(result.usuario);
}
```
