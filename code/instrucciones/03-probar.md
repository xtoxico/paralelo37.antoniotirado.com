# 03 · Probarlo de tres maneras

Mismo código, tres autenticadores distintos. Eso es exactamente lo que demuestra que WebAuthn es un
estándar y no una integración con un fabricante.

---

## A · Con la biometría de tu equipo

Es el camino corto. Si tu portátil tiene **Windows Hello**, **Touch ID** o un lector de huella
soportado, no hay nada que configurar: al pulsar *Registrarme* el sistema pedirá tu huella o tu cara.

En `usuarios.json` verás `"transports": ["internal"]`: el autenticador está dentro del aparato.

---

## B · Con el autenticador virtual de Chrome

**Esta es la red de seguridad del taller.** Funciona en cualquier equipo, sin hardware de ningún tipo.

1. Abre las **DevTools** (F12) en la pestaña de la aplicación.
2. Menú de los tres puntos (⋮) → **More tools** → **WebAuthn**.
3. Marca **Enable virtual authenticator environment**.
4. Pulsa **Add** con estos valores:

   | Campo | Valor |
   |---|---|
   | Protocol | `ctap2` |
   | Transport | `internal` |
   | Supports resident keys | ✔ |
   | Supports user verification | ✔ |
   | Is user verified | ✔ |

5. Registra un usuario en la aplicación con normalidad.

El panel WebAuthn irá mostrando las credenciales creadas, con su **Credential ID**, su **RP ID** y su
**Sign Count**. Es una ventana privilegiada a lo que normalmente ocurre dentro de un chip.

> **Truco para el taller:** desmarca *Is user verified* y vuelve a intentar el login. Verás en
> directo qué significa `userVerification` y por qué nuestro backend lleva
> `requireUserVerification: false`.

---

## C · Con una llave física

### Una YubiKey (o cualquier llave FIDO2 comercial)

Enchúfala, pulsa *Registrarme*, y toca el botón de la llave cuando parpadee. En `usuarios.json`
aparecerá `"transports": ["usb"]` o `["nfc"]`.

Ese toque es el **user presence**: la prueba de que hay un humano delante. Es lo que impide que un
malware remoto firme en silencio.

### Una Raspberry Pi Pico 2 (RP2350) con Pico FIDO

La misma demo, con una placa de cinco euros.

**Grabar el firmware** (hazlo antes del taller, no en directo):

1. Descarga el `.uf2` para tu placa desde <https://www.picokeys.com/pico-fido/>.
2. Conecta la Pico al USB **manteniendo pulsado el botón BOOTSEL**.
3. Aparecerá como una unidad USB. Copia el `.uf2` dentro.
4. La placa se reinicia sola y el sistema la reconoce como llave de seguridad. Sin drivers.

**Registrarla contra nuestra demo:** exactamente igual que la YubiKey. Sin cambiar una línea de
código.

### El experimento que hay que hacer

Este es el momento didáctico del bloque. En `src/servidor.ts`, cambia:

```typescript
attestationType: 'none',    // ← como está ahora
```

por:

```typescript
attestationType: 'direct',  // ← pedimos certificado de fabricante
```

Reinicia y vuelve a registrar. Ahora el autenticador adjunta su *attestation*. Con `'none'` nuestra
llave casera funciona sin problema; con `'direct'`, un Relying Party que además valide el **AAGUID**
contra los metadatos de la FIDO Alliance —lo que hacen los bancos y los despliegues corporativos—
la rechazaría.

> Pico FIDO hace *self-attestation*: no tiene una cadena de certificados de fabricante reconocida.
> Criptográficamente es idéntica a una YubiKey; lo que no tiene es un certificado que lo diga.

### Por qué RP2350 y no RP2040

| | RP2350 / ESP32-S3 | RP2040 |
|---|---|---|
| Secure Boot y Secure Lock | ✔ | ✘ |
| Clave maestra en memoria OTP | ✔ | ✘ |
| ¿Se puede volcar la flash? | No | **Sí** |

En el RP2040, quien te robe la placa puede extraer las claves privadas. Por eso el taller usa Pico 2.

---

## Lo que hay que enseñar en pantalla al terminar

```bash
cat code/backend/usuarios.json
```

Tres autenticadores distintos, tres credenciales en el mismo fichero, y en ninguna de ellas hay un
secreto. Ese es el resumen de las dos horas.

Siguiente: [`04-errores.md`](04-errores.md)
