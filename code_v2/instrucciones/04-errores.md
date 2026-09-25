# 04 · Los errores que van a salir

Ordenados por probabilidad real en un taller.

---

## 1. `The Angular CLI requires a minimum Node.js version of v22.22.3`

**El error número uno.** Tienes Node 22, pero no lo suficientemente nuevo.

```bash
node -v          # si dice v22.22.2 o menos, es esto
nvm install 22   # y a correr
nvm use 22
```

---

## 2. `NotAllowedError: The operation either timed out or was not allowed`

El más críptico de WebAuthn, porque tiene tres causas muy distintas:

1. **La persona canceló el diálogo.** Lo normal. No es un fallo.
2. **Expiró el `timeout`** (60 s por defecto).
3. **El `rpID` no encaja con el dominio real.** Esta es la que duele: el navegador no te dirá
   *"rpID incorrecto"*, te dirá exactamente lo mismo que si hubieras pulsado *Cancelar*.

**Cómo diagnosticarlo:** comprueba que la URL de la barra del navegador es `localhost` y no
`127.0.0.1`. Para WebAuthn **son dominios distintos**, y una credencial creada en uno no funciona en
el otro.

---

## 3. `InvalidStateError`

El autenticador ya tiene una credencial de las que van en `excludeCredentials`, así que se niega a
crear una duplicada.

**No es un fallo: es la funcionalidad haciendo su trabajo.** En una aplicación real se captura y se
muestra un mensaje del tipo *"ya tienes esta llave registrada"*.

Para probar de nuevo en el taller, borra el usuario:

```bash
rm code/backend/usuarios.json
```

---

## 4. `SecurityError` o «WebAuthn is not supported on this origin»

Estás sirviendo por **HTTP** en un dominio que no es `localhost`. WebAuthn exige HTTPS, y la única
excepción del estándar es `localhost`.

Si estás probando desde otro equipo de la red contra tu IP (`http://192.168.1.40:4200`), no va a
funcionar. Opciones: un túnel con HTTPS, o que cada uno lo ejecute en su propia máquina.

---

## 5. El frontend no llega al backend (errores de CORS)

Síntoma: en la consola del navegador, *"has been blocked by CORS policy"*.

Comprueba en `src/servidor.ts` que el `origin` es **exactamente** la URL donde sirve Angular:

```typescript
const origin = 'http://localhost:4200';   // con protocolo, con puerto, sin barra final
```

Si arrancaste Angular en otro puerto (porque el 4200 estaba ocupado), cámbialo aquí también.

---

## 6. «Firma no válida» o «No se ha podido verificar el registro»

Nuestro propio backend rechazando la respuesta. Por orden de probabilidad:

| Causa | Comprobación |
|---|---|
| `origin` mal configurado | ¿Coincide con la barra de direcciones? |
| `rpID` mal configurado | ¿Es el dominio a secas, sin `http://` ni puerto? |
| El reto guardado no es el que se firmó | ¿Hiciste dos `begin` seguidos sin completar el primero? |
| `usuarios.json` corrupto de una prueba anterior | Bórralo y vuelve a empezar |

---

## 7. `ERR_UNKNOWN_FILE_EXTENSION: Unknown file extension ".ts"`

Node está intentando ejecutar TypeScript sin el flag. Revisa el script en `package.json`:

```json
"start": "node --experimental-strip-types --watch src/servidor.ts"
```

Y que el `package.json` tenga `"type": "module"`.

---

## 8. `TypeError: Unknown file extension` o errores de sintaxis al arrancar el backend

Has usado sintaxis de TypeScript que **no se puede borrar**: un `enum`, un `namespace` o un
parámetro-propiedad en un constructor (`constructor(private x: string)`).

El borrado de tipos de Node solo elimina anotaciones; no genera código. Por eso el `tsconfig.json`
lleva `"erasableSyntaxOnly": true`: para que el editor te avise antes que Node.

---

## 9. Tutoriales antiguos de SimpleWebAuthn que no compilan

La API cambió. Si copias código de un artículo de 2023 o 2024, te vas a encontrar con esto:

| Antes (v9 y anteriores) | Ahora (v14) |
|---|---|
| `registrationInfo.credentialID` | `registrationInfo.credential.id` |
| `registrationInfo.credentialPublicKey` | `registrationInfo.credential.publicKey` |
| `registrationInfo.counter` | `registrationInfo.credential.counter` |
| `verifyAuthenticationResponse({ authenticator })` | `verifyAuthenticationResponse({ credential })` |
| `startRegistration(options)` | `startRegistration({ optionsJSON: options })` |

---

## 10. La Pico no aparece como llave

- ¿La conectaste con **BOOTSEL** pulsado y copiaste el `.uf2`? Si sigue apareciendo como unidad de
  almacenamiento, el firmware no llegó a grabarse.
- Prueba otro cable: muchos cables USB son solo de carga y no llevan líneas de datos.
- En Linux puede hacer falta una regla de udev para que el navegador acceda al dispositivo HID.

---

## Herramientas de diagnóstico

| Herramienta | Para qué |
|---|---|
| **DevTools → WebAuthn** | Ver las credenciales creadas, el RP ID y el sign count |
| **<https://webauthn.io>** | Probar tu autenticador contra un Relying Party que sabes que funciona. Si ahí va y en tu app no, el problema es tu código |
| `cat usuarios.json` | Ver qué guardó realmente el servidor |
| Pestaña Network | Inspeccionar el `challenge` que viaja en cada `begin` |

> **Regla de oro para depurar WebAuthn:** el 90 % de los problemas son `rpID` u `origin`. Empieza
> siempre por ahí antes de sospechar de la criptografía.
