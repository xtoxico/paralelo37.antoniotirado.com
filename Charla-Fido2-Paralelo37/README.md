# Charla FIDO2 · Paralelo 37

Material completo del taller **«Adiós a las contraseñas: FIDO2 y WebAuthn, del concepto al código
(y a tu propia llave de seguridad)»**, presentado en Paralelo 37 (XauenDevs).

Taller práctico de **2 horas**. Los asistentes salen con un login sin contraseñas funcionando en su
equipo y, si quieren, con una llave de seguridad hecha con una Raspberry Pi Pico 2.

---

## Qué hay aquí

| Carpeta / fichero | Contenido |
|---|---|
| [`slides/`](slides/) | La presentación en reveal.js. Se abre con doble clic, sin internet |
| [`guion.md`](guion.md) | El guion minuto a minuto, con las frases clave, las demos y el plan B |
| [`diccionario.md`](diccionario.md) | Todos los términos del taller explicados, para responder cualquier pregunta |
| [`code/backend/`](code/backend/) | El backend terminado: Node 22 + TypeScript + Express |
| [`code/frontend/`](code/frontend/) | El frontend terminado: Angular 22 |
| [`code/instrucciones/`](code/instrucciones/) | **Todos los pasos y todo el código** para construirlo desde cero |

---

## Arranque rápido

Requisitos: **Node 22.22.3 o superior** y Chrome o Edge actualizado.

```bash
# Terminal 1 — backend (puerto 3000)
cd code/backend
npm install
npm start

# Terminal 2 — frontend (puerto 4200)
cd code/frontend
npm install
npm start
```

Abre <http://localhost:4200>, escribe un nombre de usuario y pulsa **Registrarme**.

¿Sin lector de huella ni Windows Hello? Usa el autenticador virtual de Chrome: DevTools → ⋮ →
*More tools* → **WebAuthn**. Los pasos exactos están en
[`code/instrucciones/03-probar.md`](code/instrucciones/03-probar.md).

---

## Las diapositivas

```bash
# Doble clic en slides/index.html, o:
xdg-open slides/index.html
```

reveal.js va incluido en `slides/vendor/`, así que **funciona sin conexión**. Atajos útiles durante
la charla:

| Tecla | Acción |
|---|---|
| `S` | Vista de ponente con las notas del guion |
| `Esc` | Vista general de todas las diapositivas |
| `F` | Pantalla completa |
| `B` | Pantalla en negro (para que te miren a ti) |

---

## Estructura del taller

| Tiempo | Bloque |
|---|---|
| 00:00 – 00:08 | Presentación y arranque del entorno |
| 00:08 – 00:20 | Por qué las contraseñas están rotas |
| 00:20 – 00:32 | FIDO2, WebAuthn y CTAP2: quién es quién |
| 00:32 – 00:45 | Criptografía sin dolor y los dos flujos |
| 00:45 – 00:50 | Pausa y rescate de entornos |
| 00:50 – 01:15 | **Lab 1** — Backend con Express y TypeScript |
| 01:15 – 01:35 | **Lab 2** — Frontend con Angular 22 |
| 01:35 – 01:47 | El zoo de autenticadores y una YubiKey en directo |
| 01:47 – 01:57 | Fabrica tu llave: RP2350 + Pico FIDO |
| 01:57 – 02:00 | Producción, recuperación y preguntas |

---

## Versiones usadas

| | |
|---|---|
| Node.js | 22.22.3+ |
| Express | 5.2 |
| @simplewebauthn/server | 14.0 |
| @simplewebauthn/browser | 14.0 |
| Angular | 22.1 |
| reveal.js | 6.0 |

> ⚠️ La API de SimpleWebAuthn cambió en v10/v11. Si sigues tutoriales antiguos verás
> `registrationInfo.authenticator`; en v14 es `registrationInfo.credential`. La tabla completa de
> equivalencias está en [`code/instrucciones/04-errores.md`](code/instrucciones/04-errores.md).

---

## Enlaces

- [Especificación WebAuthn (W3C)](https://www.w3.org/TR/webauthn-3/)
- [FIDO Alliance](https://fidoalliance.org/)
- [SimpleWebAuthn](https://simplewebauthn.dev/)
- [webauthn.io — banco de pruebas](https://webauthn.io/)
- [passkeys.dev](https://passkeys.dev/)
- [Pico FIDO](https://www.picokeys.com/pico-fido/) · [código fuente](https://github.com/polhenarejos/pico-fido)

---

## Autor

**Antonio Tirado Peña** — Director de TI en el Instituto de Innovación, Ciencia y Empresa.

📧 yosoy@antoniotirado.com · 💼 [LinkedIn](https://linkedin.com/in/antoniotiradopena) ·
🐙 [github.com/xtoxico](https://github.com/xtoxico) · 🌐 [normapro.es](https://normapro.es)
