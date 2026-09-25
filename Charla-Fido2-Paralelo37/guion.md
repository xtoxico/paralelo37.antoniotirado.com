# Guion — Taller «Adiós a las contraseñas»

**Evento:** Paralelo 37 (XauenDevs) · **Duración:** 2 horas · **Formato:** taller práctico
**Ponente:** Antonio Tirado Peña

> Regla de oro: **la teoría no pasa de 45 minutos**. El resto es teclado. Si un bloque se alarga,
> se recorta del bloque siguiente, nunca de los labs.

---

## Antes de empezar (T-15 min)

- [ ] Backend y frontend arrancados en mi portátil, con el navegador ya abierto en `localhost:4200`
- [ ] Segunda ventana con `usuarios.json` abierta, lista para proyectar
- [ ] DevTools con el autenticador virtual ya configurado (por si falla la biometría)
- [ ] YubiKey en el bolsillo, **dos** Pico 2 flasheadas en la mesa
- [ ] Vídeo de respaldo de la demo de la Pico, por si el USB del proyector hace de las suyas
- [ ] Repo publicado y el enlace corto escrito en la pizarra o en la primera slide

---

## 0:00 – 0:08 · Apertura y arranque del entorno

**Diapositivas 1-4.**

Empieza con el enlace del repo en pantalla y una sola instrucción:

> «Antes de que yo diga nada: clonad esto y lanzad `npm install` en las dos carpetas. Tarda un par
> de minutos y quiero que corra mientras hablo.»

Preséntate en **30 segundos**. Nadie ha venido a oír tu currículum. Luego enseña la lista de lo que
vais a hacer y remata con la frase que fija expectativas:

> «En dos horas vais a salir de aquí con un login sin contraseñas funcionando en vuestro portátil, y
> con una llave de seguridad hecha con una placa de cinco euros.»

**Comprobación:** pregunta quién ha tenido algún error en el `npm install`. Apunta las caras, no te
pares ahora; los rescatas en la pausa.

---

## 0:08 – 0:20 · Por qué las contraseñas están rotas

**Diapositivas 5-10.**

Este bloque es puro relato. No hay código y no debe haberlo.

1. **Alberto.** Preséntalo con cariño, no con desprecio: «Alberto no es tonto, Alberto somos todos
   nosotros hace diez años». La gracia está en el `P4$$w0rd` y en la frase de la criptografía
   cuántica. Espera a que se rían.
2. **Have I Been Pwned.** Demo en vivo. Pide un correo voluntario al público o usa el tuyo. Casi
   siempre sale algo, y ese momento vale por veinte diapositivas.
3. **Los siete pecados.** No los leas uno a uno: señala la tabla y comenta tres. El resto se lee solo.
4. **El remate.** Baja el ritmo y suelta la frase bisagra:

   > «La contraseña no falla por falta de rigor. Falla por diseño: obliga a que un secreto compartido
   > viaje y se almacene.»

   Pausa de dos segundos. Ahí es donde la sala entiende que hay un problema estructural.

---

## 0:20 – 0:32 · Qué son FIDO2, WebAuthn y CTAP2

**Diapositivas 11-15.**

Arranca con la broma de «FIDO2 no es un Pokémon» para bajar la tensión del bloque anterior.

Lo importante de este bloque son **dos tablas**:

- **Los tres nombres.** Insiste en la ecuación: `FIDO2 = WebAuthn + CTAP2`. WebAuthn es lo que llama
  tu página; CTAP2 es lo que el navegador le dice al aparato.
- **Los tres actores.** Si hay pizarra, dibuja el triángulo. La idea que se tienen que llevar es:

  > «Tu servidor nunca habla con el autenticador. Siempre hay un navegador en medio, y eso es una
  > característica de seguridad, no una limitación.»

Cierra con las cuatro ventajas y con «puede que no conozcas FIDO2, pero FIDO2 te conoce a ti desde
tu primer Touch ID».

---

## 0:32 – 0:45 · Criptografía sin dolor y los dos flujos

**Diapositivas 16-21.**

El bloque más denso. Ve despacio.

1. **El par de claves.** Usa la animación de líneas del bloque de código. La analogía que funciona:

   > «La clave pública es un candado abierto que reparto a todo el mundo. La privada es la única
   > llave que lo cierra. Si me roban la base de datos, se llevan una colección de candados abiertos.»

2. **Por qué muere el phishing.** El punto clave: el navegador comprueba el dominio **antes** de
   pedir la firma. No es que el usuario no se equivoque, es que no puede equivocarse.

3. **El reto.** Aleatorio y nuevo cada vez. Capturar el tráfico de ayer no sirve hoy.

4. **Los dos flujos.** Preséntalos como el mismo baile: dos viajes al servidor con una llamada al
   autenticador en medio. Lo único que cambia es que en el registro **crea** claves y en el login
   **firma**.

> Si vas justo de tiempo, aquí es donde se recorta. Los flujos se vuelven a ver en el lab.

---

## 0:45 – 0:50 · Pausa

No es una pausa de cortesía: es el rescate de entornos. Ve a las mesas donde hubo errores de
`npm install`. Ten a mano el problema típico: **Node por debajo de 22.22.3**, que es el mínimo que
exige Angular 22.

---

## 0:50 – 1:15 · LAB 1 · Backend con Express y TypeScript

**Diapositivas 22-28.** Material de apoyo: `code/instrucciones/01-backend.md`.

Ritmo: tú tecleas en pantalla, ellos copian. Cada endpoint es un **punto de control**.

| Paso | Qué haces | Punto de control |
|---|---|---|
| 1 | `npm init` y dependencias | `npm start` arranca sin error |
| 2 | Las tres constantes de configuración | — |
| 3 | `POST /auth/register/begin` | `curl` devuelve un JSON con `challenge` |
| 4 | `POST /auth/register/complete` | — |
| 5 | Los dos de login | — |
| 6 | `GET /auth/users` | Devuelve `[]` |

**Insiste en `rpID` y `origin`.** Es, con diferencia, el error número uno. Di literalmente:

> «Si estos dos no encajan con la URL real, no funciona nada y el mensaje de error no os va a ayudar.»

**Momento estrella del bloque:** al terminar, proyecta `usuarios.json` y di:

> «Mirad bien lo que hay guardado aquí: un identificador, una clave pública y un número. Si mañana
> me roban esta base de datos entera, no pueden entrar en ninguna cuenta. Ni en esta ni en ninguna otra.»

---

## 1:15 – 1:35 · LAB 2 · Frontend con Angular 22

**Diapositivas 29-34.** Material de apoyo: `code/instrucciones/02-frontend.md`.

Vas con menos tiempo que en el backend, así que aquí **el código ya está escrito en el repo** y tú
lo vas explicando mientras ellos lo copian o hacen checkout de la rama.

1. `ng new` + `npm i @simplewebauthn/browser` + `ng generate service auth`. Menciona de paso las dos
   novedades de Angular 22 que van a ver: `@Service()` en lugar de `@Injectable()` y que arranca
   **zoneless** por defecto.
2. El servicio: los dos métodos son **idénticos en forma**. Tres líneas cada uno.
3. La plantilla. Y entonces, la pregunta:

   > «Buscad el campo contraseña.»

   Pausa. No está. Esa es toda la charla en una diapositiva.

4. **Prueba en vivo.** Que todo el mundo registre un usuario. Quien no tenga biometría, al
   autenticador virtual de las DevTools (diapositiva 34). Nadie se queda fuera.

**Punto de control final:** `GET /auth/users` desde el navegador muestra su usuario con una
credencial. Si alguien no llega, que haga checkout de la rama final y siga.

---

## 1:35 – 1:47 · El zoo de autenticadores

**Diapositivas 35-38.**

Cambio de ritmo: se acabó el teclado, ahora se mira.

- **De plataforma** (Windows Hello, Touch ID, Face ID, Android) frente a **cross-platform** (llaves
  USB/NFC, tu propio móvil haciendo de llave para el PC).
- **La YubiKey.** Sácala, enséñala, pásala por las filas mientras sigues hablando.
- **Passkeys sincronizadas vs atadas al dispositivo.** Es la parte peor explicada de todo el
  ecosistema, así que dedícale tiempo: la sincronizada vive en tu cuenta de Google o iCloud y
  sobrevive al cambio de móvil; la atada al dispositivo no se copia jamás. El backend recibe ambos
  flags en el registro (`credentialDeviceType` y `credentialBackedUp`) y conviene guardarlos.

---

## 1:47 – 1:57 · Fabrica tu propia llave: RP2350 + Pico FIDO

**Diapositivas 39-45.** Material de apoyo: `diccionario.md` (entradas *Pico FIDO*, *attestation*, *AAGUID*).

Este es el cierre que diferencia el taller. Secuencia:

1. **Qué es.** Un firmware libre que convierte una Raspberry Pi Pico 2 en una llave FIDO2.
2. **Cómo se graba.** Tres pasos: descargar el `.uf2`, conectar con BOOTSEL pulsado, arrastrar.
   *No lo hagas en vivo* — lleva las placas ya flasheadas.
3. **LA DEMO.** Registra un usuario en **vuestra propia demo** con la Pico. Sin cambiar una línea.
   Luego abre `/auth/users` y enseña el `credentialId` y el `transports: ["usb"]`.

   > «Esto demuestra que WebAuthn es un estándar de verdad y no una integración con un fabricante.»

4. **RP2350 y no RP2040.** Secure Boot, Secure Lock y clave maestra en memoria OTP. En el RP2040 la
   flash se puede volcar y con ella las claves privadas.
5. **Entonces, ¿para qué pagar una YubiKey?**

   > «La matemática es idéntica. Lo que compras es que nadie pueda abrir la caja.»

6. **El gancho hacia el código.** Cambia `attestationType` de `'none'` a `'direct'` en el backend y
   explica que un banco que valide el AAGUID contra los metadatos de la FIDO Alliance rechazaría la
   llave casera. Ese parámetro que llevan media hora copiando sin pensar: para esto sirve.
7. **Bonus.** La semilla de 24 palabras: Pico FIDO deja respaldar y restaurar; las llaves
   comerciales no, por diseño.

---

## 1:57 – 2:00 · Producción, lo que no arregla, y cierre

**Diapositivas 46-49.**

Rápido, es la lista de «lo que os vais a encontrar»:

- **Recuperación de cuenta:** registrad siempre más de una credencial. Es el agujero práctico real.
- **`rpID` vs `origin`**, HTTPS obligatorio (salvo `localhost`) y cuidado con los subdominios.
- **`signCount`:** guardadlo y comparadlo, detecta llaves clonadas.
- **Persistencia:** nuestro JSON es didáctico; en serio, una base de datos.
- **Sesión:** FIDO2 autentica; la cookie o el JWT los pones tú.

Y lo que **no** arregla: malware ya instalado, secuestro de sesión después del login, un backend mal
programado.

Cierra con la frase final y tus datos de contacto. Deja la diapositiva de recursos en pantalla
mientras respondes preguntas.

---

## Plan B (por si algo falla)

| Si falla… | Haz esto |
|---|---|
| El wifi de la sala | Todo el código está en el repo y `npm install` ya corrió en la apertura |
| La biometría de un asistente | Autenticador virtual de las DevTools, diapositiva 34 |
| El `npm install` de alguien | Que haga checkout de la rama final y siga el hilo |
| El proyector con la Pico | Vídeo de respaldo grabado |
| Vas 10 minutos tarde | Recorta el bloque de criptografía y el zoo de autenticadores |
| Vas 10 minutos sobrado | Conditional UI (autofill de passkeys) y login sin usuario |

---

## Preguntas que van a salir sí o sí

**«¿Y si pierdo el móvil?»**
Por eso se registran varias credenciales. Y por eso existen las passkeys sincronizadas: la credencial
vive en tu cuenta de Google o iCloud, no en el aparato.

**«¿Y si me roban la llave física?»**
No sirve de nada sin tu huella o tu PIN, si configuraste verificación de usuario. Y la revocas desde
el servicio como revocarías una tarjeta.

**«¿Esto no es lo mismo que el 2FA de siempre?»**
No. El segundo factor clásico se **añade** a la contraseña y sigue siendo phishable (el código SMS se
lo puedes dictar a un atacante). Aquí la contraseña **desaparece** y la credencial está atada al
dominio.

**«¿Lo puedo usar ya en producción?»**
Sí. Google, GitHub, Microsoft, AWS y Apple ya lo usan. Lo que hay que diseñar bien es la recuperación.

**«¿Funciona en Safari / en Firefox / en móvil?»**
Sí en los tres, con matices en las passkeys sincronizadas. Usa `browserSupportsWebAuthn()` para
detectarlo y degradar con elegancia.

**«¿Qué pasa si el servidor se compromete?»**
Que el atacante se lleva claves públicas. Inútiles. Ese es exactamente el punto de todo el estándar.
