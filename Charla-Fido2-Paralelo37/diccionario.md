# Diccionario del taller FIDO2

Todos los términos que van a aparecer, con una definición corta para la diapositiva y una explicación
larga para cuando alguien pregunte. Ordenado alfabéticamente dentro de cada bloque.

---

## 1 · Los nombres del estándar

### FIDO2

**En una línea:** el estándar abierto de autenticación sin contraseñas.

**Largo:** *Fast Identity Online 2.0*, de la FIDO Alliance. No es una tecnología concreta sino un
paraguas que agrupa dos piezas: **WebAuthn** (la API que usa la página web) y **CTAP2** (el protocolo
con el que el navegador habla con el aparato que guarda las claves). Cuando alguien dice «implementar
FIDO2» en una web, en la práctica está diciendo «implementar WebAuthn».

**La ecuación:** `FIDO2 = WebAuthn + CTAP2`

### WebAuthn

**En una línea:** la API del navegador que tu JavaScript llama.

**Largo:** *Web Authentication API*, estándar del W3C. Son dos métodos: `navigator.credentials.create()`
para registrar y `navigator.credentials.get()` para autenticar. Tu código nunca toca criptografía: le
pide al navegador que hable con el autenticador y recibe un objeto con una firma dentro.

### CTAP2

**En una línea:** cómo el navegador habla con la llave.

**Largo:** *Client To Authenticator Protocol* versión 2. Define los mensajes que viajan por USB, NFC o
Bluetooth entre el navegador y un autenticador externo. Es la capa que tú **nunca** programas: la
implementa el sistema operativo. Su versión anterior, CTAP1, es lo que se conocía como **U2F**.

### U2F

**En una línea:** el abuelo de FIDO2, el segundo factor de las llaves antiguas.

**Largo:** *Universal 2nd Factor*. Funcionaba solo como **segundo** factor: primero contraseña, luego
llave. FIDO2 lo absorbe por compatibilidad (CTAP1), pero ya permite prescindir de la contraseña.

### FIDO Alliance

**En una línea:** el consorcio que publica el estándar y certifica los autenticadores.

**Largo:** Google, Apple, Microsoft, Yubico y un largo etcétera. Además del estándar mantienen el
**MDS** (*Metadata Service*), el catálogo contra el que un servidor puede comprobar de qué modelo es
un autenticador a partir de su AAGUID.

---

## 2 · Los tres actores

### Relying Party (RP)

**En una línea:** tu servidor. El que confía en la firma.

**Largo:** literalmente «la parte que confía». En el taller es el Express. Se identifica con dos
valores que tienes que tener clarísimos: el `rpID` y el `rpName`.

### Client

**En una línea:** el navegador y el sistema operativo.

**Largo:** el intermediario obligatorio. Traduce entre WebAuthn (lo que pide tu página) y CTAP2 (lo
que entiende la llave), y **comprueba el dominio** antes de dejar que nada se firme. Tu servidor nunca
habla directamente con el autenticador, y eso es una característica de seguridad.

### Authenticator

**En una línea:** el aparato donde vive la clave privada.

**Largo:** puede estar integrado en el dispositivo (Touch ID, Windows Hello) o ser externo (una
YubiKey, una Pico FIDO). Genera los pares de claves, los guarda y firma retos. La clave privada no
sale de ahí nunca, por diseño físico.

---

## 3 · Criptografía

### Clave pública / clave privada

**En una línea:** un par matemáticamente ligado donde lo que firma una, la otra lo verifica.

**Largo:** la analogía que funciona en una charla: la **pública** es un candado abierto que repartes a
todo el mundo; la **privada** es la única llave que lo cierra. En FIDO2 el servidor guarda candados
abiertos. Si le roban la base de datos, el atacante se lleva una colección de candados que no abren
nada.

### Criptografía asimétrica

**En una línea:** cifrar/firmar con una clave y verificar con otra distinta.

**Largo:** lo contrario de la simétrica, donde ambas partes comparten el mismo secreto (que es
exactamente el problema de las contraseñas). Aquí no hay secreto compartido: no hay nada que filtrar.

### Challenge (reto)

**En una línea:** un valor aleatorio que el servidor manda y el autenticador firma.

**Largo:** se genera **nuevo en cada intento**. La firma solo vale para ese reto concreto, así que
capturar el tráfico de ayer no sirve para entrar hoy. Es la protección contra ataques de *replay*.

### Assertion

**En una línea:** el paquete que devuelve el autenticador al hacer login.

**Largo:** contiene la firma del reto, los `authenticatorData` y el `clientDataJSON`. Es lo que tu
backend le pasa a `verifyAuthenticationResponse()`.

### Attestation

**En una línea:** la «partida de nacimiento» de la credencial: quién fabricó el autenticador.

**Largo:** durante el registro, el autenticador puede adjuntar un certificado que demuestra su modelo
y fabricante. Modos habituales:

- `'none'` — no pedimos nada. Es lo normal y es lo que usa el taller.
- `'direct'` — pedimos el certificado. Sirve para restringir por fabricante (bancos, corporativo).
- `'enterprise'` — attestation con identificador único, solo para despliegues internos.

**Por qué importa en el taller:** Pico FIDO hace *self-attestation*. Con `'none'` funciona; con
`'direct'` y validación del AAGUID contra el MDS, un banco la rechazaría.

### AAGUID

**En una línea:** el identificador de **modelo** del autenticador.

**Largo:** *Authenticator Attestation GUID*. 16 bytes que dicen «soy una YubiKey 5 NFC» o «soy Windows
Hello». No identifica al usuario ni a la unidad concreta, solo al modelo. Es lo que se consulta contra
el MDS de la FIDO Alliance.

### signCount / counter

**En una línea:** un contador que el autenticador incrementa cada vez que firma.

**Largo:** el servidor lo guarda y comprueba que siempre sube. Si un día llega un valor **menor o
igual** al guardado, es señal de que hay dos copias de la misma credencial en circulación: una llave
clonada. Muchos autenticadores modernos (incluidas las passkeys sincronizadas) lo dejan siempre a 0,
así que trátalo como una señal, no como un dogma.

### Credential ID

**En una línea:** el identificador público de una credencial concreta.

**Largo:** lo genera el autenticador y lo guarda el servidor. Sirve para que, en el login, el servidor
le diga al navegador «de todas tus credenciales, estas son las que valen aquí».

---

## 4 · Tipos de credenciales y autenticadores

### Passkey

**En una línea:** el nombre comercial de una credencial FIDO2 descubrible.

**Largo:** el término que la industria eligió para que la gente normal entendiera esto. Técnicamente
es una *discoverable credential*. Hay dos sabores, y confundirlos es el error más común del
ecosistema:

- **Sincronizada:** vive en tu cuenta de Google, iCloud o tu gestor de contraseñas. Cambias de móvil
  y sigue ahí. Cómoda, y con el riesgo trasladado a la seguridad de esa cuenta.
- **Atada al dispositivo (*device-bound*):** nace y muere en ese aparato. No se copia jamás. Más
  segura, pero si pierdes el aparato pierdes la credencial.

El backend distingue ambas por los flags `credentialDeviceType` (`singleDevice` / `multiDevice`) y
`credentialBackedUp`.

### Discoverable credential / Resident key

**En una línea:** la credencial se guarda **dentro** del autenticador, así que permite entrar sin
escribir el usuario.

**Largo:** el autenticador almacena la clave junto con el nombre de usuario. Al hacer login, el
navegador puede ofrecer una lista de cuentas sin que el servidor le diga nada. Es lo que permite el
flujo *usernameless*. Ocupa espacio en la llave, así que el número es limitado. Se pide con
`residentKey: 'required' | 'preferred' | 'discouraged'`.

### Non-discoverable credential (server-side)

**En una línea:** la clave privada va cifrada dentro del propio `credentialId`.

**Largo:** el autenticador no guarda nada: envuelve la clave privada usando un secreto maestro y la
mete en el identificador que entrega al servidor. Cuando el servidor se lo devuelve, el autenticador
la desenvuelve. Resultado: **credenciales ilimitadas**, a costa de tener que escribir el usuario para
que el servidor sepa qué identificadores enviar.

### Autenticador de plataforma

**En una línea:** el que viene dentro del aparato.

**Largo:** Windows Hello, Touch ID, Face ID, biometría de Android. Se pide con
`authenticatorAttachment: 'platform'`. Cómodo porque no hay que llevar nada encima; atado a ese
dispositivo concreto salvo que la passkey se sincronice.

### Autenticador cross-platform / roaming

**En una línea:** el que se enchufa o se acerca.

**Largo:** llaves USB/NFC/Bluetooth, o tu propio móvil haciendo de llave para el PC. Se pide con
`authenticatorAttachment: 'cross-platform'`. Portátil entre equipos, hay que llevarlo encima.

### User Presence (UP)

**En una línea:** la prueba de que hay un humano delante.

**Largo:** normalmente, tocar el botón de la llave. No identifica a nadie: solo confirma que alguien
físicamente presente ha aprobado la operación. Es lo que impide que un malware remoto firme en
silencio.

### User Verification (UV)

**En una línea:** la prueba de que el humano es **el** humano.

**Largo:** huella, cara o PIN. Se configura con `userVerification: 'required' | 'preferred' |
'discouraged'`. En el taller lo dejamos en `'preferred'` para no excluir llaves simples sin PIN.

---

## 5 · Parámetros que vas a escribir

### rpID

**En una línea:** el dominio al que queda atada la credencial.

**Largo:** sin protocolo y sin puerto: `midominio.es`, o `localhost` en desarrollo. Puede ser el
dominio o un sufijo suyo (una credencial creada con `rpID: 'midominio.es'` funciona en
`app.midominio.es`, pero no al revés). **Es la pieza anti-phishing**: si el dominio no coincide, el
autenticador ni se despierta.

### origin

**En una línea:** la URL completa desde la que aceptas peticiones.

**Largo:** con protocolo y puerto: `http://localhost:4200`. El navegador lo incluye firmado en el
`clientDataJSON` y tu servidor comprueba que coincide. **Si `rpID` y `origin` no encajan, no funciona
nada y el error no te va a ayudar.** Es el fallo número uno en cualquier taller de WebAuthn.

### excludeCredentials

**En una línea:** «este usuario ya tiene estas credenciales, no crees una duplicada».

**Largo:** se envía en el registro. Si el autenticador reconoce alguna de la lista, se niega a crear
otra y el navegador devuelve `InvalidStateError`. Es una funcionalidad, no un error.

### allowCredentials

**En una línea:** «de todas tus credenciales, estas son las que valen aquí».

**Largo:** se envía en el login. Si lo dejas vacío y el autenticador tiene una *discoverable
credential*, el navegador ofrece la lista de cuentas por su cuenta: eso es el login sin usuario.

### Conditional UI / autofill

**En una línea:** la passkey se ofrece en el desplegable del campo de usuario.

**Largo:** se activa con `useBrowserAutofill: true` y un `<input autocomplete="username webauthn">`.
Es lo que la gente ve hoy en Google o GitHub: escribes en el campo y el navegador te sugiere entrar
con la huella. No entra en el taller por tiempo, pero es el siguiente paso natural.

---

## 6 · Hardware

### YubiKey

**En una línea:** la llave de seguridad comercial de referencia.

**Largo:** de Yubico. USB-A, USB-C, NFC, Lightning. Usa un **elemento seguro certificado** con
resistencia física a ataques y tiene una cadena de attestation reconocida por el MDS. No permite
exportar las claves, por diseño: la estrategia de respaldo es registrar dos llaves por cuenta.

### Pico FIDO

**En una línea:** firmware libre que convierte una Raspberry Pi Pico o un ESP32-S3 en una llave FIDO2.

**Largo:** de Pol Henarejos (`github.com/polhenarejos/pico-fido`). Soporta CTAP2, CTAP1/U2F, las
extensiones `hmac-secret`, `credProtect` y `largeBlobKey`, y además OATH TOTP/HOTP. Se instala
arrastrando un `.uf2` a la placa arrancada con BOOTSEL pulsado, y el sistema la reconoce como llave
USB sin drivers. Doble licencia: AGPLv3 para uso personal, comercial para producción.

### RP2350 vs RP2040

**En una línea:** el 2350 protege las claves; el 2040 no.

**Largo:** el **RP2350** (y el ESP32-S3) soportan Secure Boot y Secure Lock, con una clave maestra en
memoria **OTP** que cifra las credenciales guardadas, y la flash no se puede volcar. En el **RP2040**
no existe esa protección: quien te robe la placa puede extraer las claves privadas. Por eso el taller
usa Pico 2.

### Secure Element / TPM / Secure Enclave / TEE

**En una línea:** el chip aislado donde viven las claves.

**Largo:** nombres distintos para la misma idea según el fabricante — **TPM** en PC (Windows Hello),
**Secure Enclave** en Apple, **StrongBox/TEE** en Android, *secure element* en una YubiKey. Es
hardware separado del procesador principal: aunque el sistema operativo esté comprometido, no puede
leer lo que hay dentro.

### OTP (One-Time Programmable)

**En una línea:** memoria que se escribe una vez y ya no se puede cambiar.

**Largo:** ahí es donde el RP2350 guarda la clave maestra de Pico FIDO. Como no se puede reescribir ni
leer desde fuera, sirve de ancla de confianza para cifrar todo lo demás.

### UF2

**En una línea:** el formato de fichero que se arrastra a la placa para grabarla.

**Largo:** *USB Flashing Format*, de Microsoft. La placa, arrancada con BOOTSEL pulsado, se presenta
como una unidad USB; copias el `.uf2` encima y se reinicia ya programada. Sin toolchain, sin drivers.

---

## 7 · Herramientas

### SimpleWebAuthn

**En una línea:** la librería que nos ahorra toda la criptografía y las conversiones de buffers.

**Largo:** dos paquetes, `@simplewebauthn/server` y `@simplewebauthn/browser`. En el taller usamos la
**v14**; ojo si sigues tutoriales antiguos, porque la API cambió: lo que antes era
`registrationInfo.authenticator` ahora es `registrationInfo.credential`.

### Virtual Authenticator (DevTools)

**En una línea:** un autenticador por software dentro de Chrome.

**Largo:** DevTools → ⋮ → *More tools* → **WebAuthn** → *Enable virtual authenticator environment*.
Permite crear autenticadores con las características que quieras (ctap2, resident keys, user
verification) y ver las credenciales que se van creando. **Es lo que garantiza que nadie se quede
fuera del taller** por no tener biometría.

### webauthn.io

**En una línea:** un banco de pruebas público para probar tu autenticador contra un RP que funciona.

**Largo:** útil para aislar problemas: si tu llave funciona ahí pero no en tu app, el problema está en
tu código (casi siempre, en `rpID` u `origin`).

### Have I Been Pwned

**En una línea:** buscador de correos aparecidos en filtraciones.

**Largo:** `haveibeenpwned.com`, de Troy Hunt. Se usa en la apertura para el golpe de efecto: casi
cualquier correo con algunos años sale en alguna brecha.

---

## 8 · Errores que vais a ver

| Error | Qué significa de verdad |
|---|---|
| `NotAllowedError` | La persona canceló el diálogo, o expiró el `timeout`. También sale cuando el `rpID` no encaja con el dominio real |
| `InvalidStateError` | El autenticador ya tiene una credencial de las que van en `excludeCredentials`. Funciona como debe |
| `SecurityError` | Estás sirviendo por HTTP en un dominio que no es `localhost`. WebAuthn exige HTTPS |
| `NotSupportedError` | Ningún algoritmo de `pubKeyCredParams` es compatible con ese autenticador |
| `AbortError` | Se llamó a `AbortController` o se lanzó otra operación WebAuthn encima |
| «Firma no válida» (nuestro backend) | Casi siempre: `origin` o `rpID` mal, o el reto guardado no es el que se firmó |
