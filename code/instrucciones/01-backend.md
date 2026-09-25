# 01 · Backend con Express y TypeScript

> Tiempo en el taller: **25 minutos**. Cinco endpoints y ni una sola contraseña.

## Paso 1 · Crear el proyecto

```bash
mkdir -p backend/src && cd backend
npm init -y
```

## Paso 2 · Instalar dependencias

```bash
npm i express @simplewebauthn/server
npm i -D @types/express @types/node typescript
```

Solo dos dependencias de verdad:

- **express** — el servidor HTTP
- **@simplewebauthn/server** — hace toda la criptografía por nosotros

## Paso 3 · `package.json`

Sustituye el generado por este. Lo importante son dos cosas: `"type": "module"` (usamos `import`, no
`require`) y el script `start`, que ejecuta TypeScript **sin compilarlo**.

```json
{
  "name": "taller-fido2-backend",
  "version": "1.0.0",
  "description": "Backend del taller FIDO2/WebAuthn de Paralelo 37",
  "type": "module",
  "private": true,
  "scripts": {
    "start": "node --experimental-strip-types --watch src/servidor.ts"
  },
  "dependencies": {
    "@simplewebauthn/server": "^14.0.2",
    "express": "^5.2.1"
  },
  "devDependencies": {
    "@types/express": "^5.0.0",
    "@types/node": "^22.0.0",
    "typescript": "^5.9.3"
  }
}
```

> `--experimental-strip-types` le dice a Node que borre los tipos al vuelo y ejecute el resultado.
> Desde Node 22.18 está activado por defecto, pero lo dejamos explícito para que funcione en
> cualquier Node 22. `--watch` reinicia el servidor solo al guardar.

## Paso 4 · `tsconfig.json`

Este fichero **no compila nada**: existe para que el editor sepa qué esperar.

```json
{
  // Node 22 ejecuta TypeScript directamente borrando los tipos, así que este fichero
  // NO se usa para compilar: solo sirve para que el editor sepa qué esperar.
  "compilerOptions": {
    "target": "ES2023",
    "module": "nodenext",
    "moduleResolution": "nodenext",
    "strict": true,
    "noEmit": true,
    // Obligatorio cuando Node borra los tipos en caliente: prohíbe sintaxis no borrable.
    "erasableSyntaxOnly": true,
    "verbatimModuleSyntax": true,
    "allowImportingTsExtensions": true,
    "skipLibCheck": true
  },
  "include": ["src"]
}
```

La opción clave es `erasableSyntaxOnly`: prohíbe la sintaxis de TypeScript que no se puede borrar sin
generar código (`enum`, `namespace`, parámetros-propiedad en constructores). Si la usas, Node fallará.

## Paso 5 · `src/servidor.ts`

Este es el backend **completo**. Léelo de arriba abajo: cada bloque está comentado.

```typescript
/**
 * Taller FIDO2 / WebAuthn — Paralelo 37 (XauenDevs)
 * ---------------------------------------------------------------------------
 * Backend completo en un solo fichero: 5 endpoints y ni una sola contraseña.
 * Arranca con:  npm start
 * ---------------------------------------------------------------------------
 */

// Express es nuestro servidor HTTP: enruta peticiones y nos da helpers como express.json().
import express from 'express';
// Módulos nativos de Node (no hay que instalar nada) para leer y escribir nuestro fichero JSON.
import { existsSync, readFileSync, writeFileSync } from 'node:fs';
// Las cuatro funciones de SimpleWebAuthn que hacen TODO el trabajo criptográfico por nosotros.
import {
  generateRegistrationOptions, // Paso 1 del registro: crea el reto y las opciones.
  verifyRegistrationResponse, // Paso 2 del registro: valida la respuesta del autenticador.
  generateAuthenticationOptions, // Paso 1 del login: crea un reto nuevo.
  verifyAuthenticationResponse, // Paso 2 del login: verifica la firma con la clave pública.
} from '@simplewebauthn/server';
// Tipos que nos dan autocompletado sobre lo que el navegador nos envía en el body.
import type {
  RegistrationResponseJSON,
  AuthenticationResponseJSON,
} from '@simplewebauthn/server';

// ───────────────────────── Configuración del Relying Party ─────────────────────────
// "Relying Party" es el nombre que el estándar da a nuestro servicio: quien confía en la firma.

// Nombre bonito que el navegador enseñará en el diálogo nativo ("¿Guardar passkey para…?").
const rpName = 'Taller FIDO2 — Paralelo 37';
// Dominio al que quedan ATADAS las credenciales. Esto es lo que hace el phishing imposible:
// una credencial creada para "localhost" jamás funcionará en "l0calhost.com".
const rpID = 'localhost';
// Origen exacto desde el que aceptamos peticiones: la URL donde sirve Angular.
const origin = 'http://localhost:4200';
// Nuestra "base de datos": un fichero JSON que podemos abrir en clase para ver qué se guarda.
const FICHERO = 'usuarios.json';

// ───────────────────────── Tipos y persistencia en JSON ─────────────────────────

/** Lo ÚNICO que guardamos de cada credencial. Fíjate: aquí no hay ningún secreto. */
type Credencial = {
  id: string; // Identificador público de la credencial (base64url).
  publicKey: string; // La clave PÚBLICA. Inútil para un atacante.
  counter: number; // Contador anti-replay que el autenticador incrementa en cada uso.
  transports?: string[]; // Pistas para el navegador: 'usb', 'internal', 'nfc'…
};

/** Ficha de un usuario: el reto que le hemos mandado y las credenciales que ha registrado. */
type Usuario = { reto: string; credenciales: Credencial[] };

/** Lee el fichero completo; si todavía no existe, arrancamos con un objeto vacío. */
const leerBD = (): Record<string, Usuario> =>
  existsSync(FICHERO) ? JSON.parse(readFileSync(FICHERO, 'utf8')) : {};

/** Vuelca todo a disco con sangrado, para que sea legible al proyectarlo. */
const guardarBD = (bd: Record<string, Usuario>) =>
  writeFileSync(FICHERO, JSON.stringify(bd, null, 2));

/** Devuelve la ficha del usuario y, si es nuevo, la crea vacía sobre la marcha. */
const ficha = (bd: Record<string, Usuario>, usuario: string): Usuario =>
  (bd[usuario] ??= { reto: '', credenciales: [] });

// ───────────────────────── Servidor ─────────────────────────

const app = express();

// Convierte automáticamente el cuerpo JSON de cada POST en un objeto JavaScript.
app.use(express.json());

// CORS mínimo: el frontend vive en el puerto 4200 y el backend en el 3000, así que
// hay que darle permiso explícito al navegador para que deje pasar las respuestas.
app.use((_peticion, respuesta, siguiente) => {
  respuesta.set({
    'Access-Control-Allow-Origin': origin,
    'Access-Control-Allow-Headers': 'Content-Type',
  });
  siguiente();
});

// El navegador manda un OPTIONS "de cortesía" antes de cada POST: le decimos que adelante.
app.options(/.*/, (_peticion, respuesta) => {
  respuesta.sendStatus(204);
});

// ───────── 1/5 · REGISTRO, PASO 1: el servidor propone un reto ─────────
app.post('/auth/register/begin', async (peticion, respuesta) => {
  // Lo único que pedimos a la persona: un nombre de usuario. Nunca una contraseña.
  const usuario: string = peticion.body.usuario;
  const bd = leerBD();
  const registro = ficha(bd, usuario);

  // SimpleWebAuthn genera un reto aleatorio y arma el objeto que espera el navegador.
  const opciones = await generateRegistrationOptions({
    rpName,
    rpID,
    userName: usuario,
    // 'none' = no exigimos certificado del fabricante del autenticador.
    // Cámbialo a 'direct' y una llave casera (Pico FIDO) empezará a ser rechazable.
    attestationType: 'none',
    // Le decimos qué credenciales ya tiene para que el autenticador no cree una duplicada.
    excludeCredentials: registro.credenciales.map((c) => ({ id: c.id, transports: c.transports })),
    authenticatorSelection: {
      residentKey: 'preferred', // 'preferred' = si puede, que la guarde dentro (passkey).
      userVerification: 'preferred', // 'preferred' = pide huella/PIN si el aparato sabe.
    },
  });

  // Guardamos el reto: dentro de un momento tendremos que comprobar que firmó ESTE y no otro.
  registro.reto = opciones.challenge;
  guardarBD(bd);

  // El frontend le pasará esto tal cual a navigator.credentials.create().
  respuesta.json(opciones);
});

// ───────── 2/5 · REGISTRO, PASO 2: verificamos y guardamos la clave pública ─────────
app.post('/auth/register/complete', async (peticion, respuesta) => {
  const usuario: string = peticion.body.usuario;
  // Lo que el autenticador ha devuelto al navegador (attestation).
  const credencialNueva: RegistrationResponseJSON = peticion.body.credencial;
  const bd = leerBD();
  const registro = ficha(bd, usuario);

  // Aquí ocurre toda la magia: SimpleWebAuthn comprueba la firma, el reto y el origen.
  const { verified, registrationInfo } = await verifyRegistrationResponse({
    response: credencialNueva,
    expectedChallenge: registro.reto, // ¿Firmó exactamente el reto que le mandamos?
    expectedOrigin: origin, // ¿Vino de NUESTRA web y no de una copia falsa?
    expectedRPID: rpID, // ¿La credencial es para nuestro dominio?
    requireUserVerification: false, // Aceptamos llaves sin PIN ni biometría.
  });

  // Si algo no cuadra, cortamos aquí. No hay segundo intento ni mensajes ambiguos.
  if (!verified || !registrationInfo) {
    return respuesta.status(400).json({ error: 'No se ha podido verificar el registro' });
  }

  // Guardamos SOLO la clave pública. La privada nunca ha salido del dispositivo del usuario.
  const { credential } = registrationInfo;
  registro.credenciales.push({
    id: credential.id,
    // La clave viene como bytes; la pasamos a texto base64url para poder meterla en el JSON.
    publicKey: Buffer.from(credential.publicKey).toString('base64url'),
    counter: credential.counter,
    transports: credential.transports,
  });
  guardarBD(bd);

  respuesta.json({ verificado: true });
});

// ───────── 3/5 · LOGIN, PASO 1: un reto nuevo, distinto del anterior ─────────
app.post('/auth/login/begin', async (peticion, respuesta) => {
  const usuario: string = peticion.body.usuario;
  const bd = leerBD();
  const registro = bd[usuario];

  // Si no lo conocemos o nunca registró una credencial, no hay nada que firmar.
  if (!registro?.credenciales.length) {
    return respuesta.status(404).json({ error: 'Ese usuario no tiene credenciales' });
  }

  // El reto es SIEMPRE nuevo: por eso una firma capturada ayer no sirve para entrar hoy.
  const opciones = await generateAuthenticationOptions({
    rpID,
    // Le indicamos al navegador cuáles de sus credenciales sirven para este usuario.
    allowCredentials: registro.credenciales.map((c) => ({ id: c.id, transports: c.transports })),
    userVerification: 'preferred',
  });

  registro.reto = opciones.challenge;
  guardarBD(bd);

  respuesta.json(opciones);
});

// ───────── 4/5 · LOGIN, PASO 2: verificamos la firma con la clave pública ─────────
app.post('/auth/login/complete', async (peticion, respuesta) => {
  const usuario: string = peticion.body.usuario;
  const firma: AuthenticationResponseJSON = peticion.body.credencial;
  const bd = leerBD();
  const registro = ficha(bd, usuario);

  // Buscamos, entre las credenciales del usuario, la que realmente ha firmado.
  const credencial = registro.credenciales.find((c) => c.id === firma.id);
  if (!credencial) {
    return respuesta.status(404).json({ error: 'Credencial desconocida' });
  }

  const { verified, authenticationInfo } = await verifyAuthenticationResponse({
    response: firma,
    expectedChallenge: registro.reto,
    expectedOrigin: origin,
    expectedRPID: rpID,
    // Le pasamos la clave pública guardada, devolviéndola de texto a bytes.
    credential: {
      id: credencial.id,
      publicKey: Uint8Array.from(Buffer.from(credencial.publicKey, 'base64url')),
      counter: credencial.counter,
      transports: credencial.transports,
    },
    requireUserVerification: false,
  });

  if (!verified) {
    return respuesta.status(401).json({ error: 'Firma no válida' });
  }

  // Anti-replay: el autenticador lleva su propio contador y debe ir siempre hacia arriba.
  // Si alguien clonase una llave, los contadores se desincronizarían y lo detectaríamos.
  credencial.counter = authenticationInfo.newCounter;
  guardarBD(bd);

  // Aquí es donde, en una aplicación real, emitirías la cookie de sesión o el JWT.
  respuesta.json({ verificado: true, usuario });
});

// ───────── 5/5 · Endpoint de clase: ver qué hay guardado de verdad ─────────
app.get('/auth/users', (_peticion, respuesta) => {
  const bd = leerBD();
  // Devolvemos el contenido tal cual para poder proyectarlo y comprobar que NO hay secretos.
  respuesta.json(
    Object.entries(bd).map(([usuario, datos]) => ({
      usuario,
      credenciales: datos.credenciales.length,
      detalle: datos.credenciales,
    })),
  );
});

// Arrancamos. A partir de aquí, cero contraseñas en toda la aplicación.
app.listen(3000, () => console.log('Backend FIDO2 escuchando en http://localhost:3000'));
```

## Paso 6 · Arrancar y comprobar

```bash
npm start
```

Deberías ver:

```
Backend FIDO2 escuchando en http://localhost:3000
```

Y ahora los dos puntos de control:

```bash
# 1) La lista de usuarios debe estar vacía
curl http://localhost:3000/auth/users
# → []

# 2) Pedir un reto de registro debe devolver un JSON con "challenge"
curl -X POST http://localhost:3000/auth/register/begin \
  -H 'Content-Type: application/json' \
  -d '{"usuario":"antonio"}'
```

Si el segundo devuelve algo parecido a esto, el backend está terminado:

```json
{
  "challenge": "dadP1DH7q_lPPCBZQMmyxdILEfBdPUVw5VtxdKZKP8Y",
  "rp": { "name": "Taller FIDO2 — Paralelo 37", "id": "localhost" },
  "user": { "id": "e9dlkQ...", "name": "antonio", "displayName": "" },
  "pubKeyCredParams": [{ "alg": -8 }, { "alg": -7 }, { "alg": -257 }],
  "timeout": 60000,
  "attestation": "none",
  "authenticatorSelection": {
    "residentKey": "preferred",
    "userVerification": "preferred"
  }
}
```

## Las tres cosas que hay que entender de este fichero

**1. El servidor nunca ve un secreto.** Lo único que guardamos de cada persona es un identificador,
una clave pública y un número. Ábrelo cuando tengas usuarios registrados:

```bash
cat usuarios.json
```

Si mañana te roban ese fichero entero, el atacante no puede entrar en ninguna cuenta.

**2. `rpID` y `origin` son el 90% de los errores.** `rpID` es el dominio a secas (`localhost`);
`origin` es la URL completa con protocolo y puerto (`http://localhost:4200`). Si no encajan con la
realidad, no funciona nada y el mensaje de error no te ayudará.

**3. El reto se guarda entre los dos pasos.** `register/begin` genera un valor aleatorio y lo
almacena; `register/complete` comprueba que la firma que llega corresponde a **ese** valor. Por eso
una respuesta capturada ayer no sirve hoy.

Siguiente: [`02-frontend.md`](02-frontend.md)
