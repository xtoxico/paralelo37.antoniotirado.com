# 00 · Requisitos

## Qué hace falta

| Herramienta | Versión | Por qué |
|---|---|---|
| **Node.js** | **22.22.3 o superior** | Angular 22 no arranca por debajo. Node 22 además ejecuta TypeScript directamente, así que el backend no necesita compilarse |
| **npm** | 10 o superior | Viene con Node |
| **Chrome o Edge** | Actualizado | Usaremos su autenticador virtual como red de seguridad |
| **Git** | Cualquiera | Para clonar el repo |
| Un editor | El que quieras | — |

**Opcional pero recomendable:** un dispositivo con biometría (huella, Windows Hello, Touch ID) o una
llave FIDO2. Si no tienes ninguno, no pasa nada: en [`03-probar.md`](03-probar.md) está el
autenticador virtual.

## Comprobación rápida

```bash
node -v    # debe decir v22.22.3 o superior
npm -v     # 10.x o superior
git --version
```

> ⚠️ **El error número uno del taller es tener Node 22.22.2 o inferior.** El mensaje que da Angular
> es claro, pero pilla por sorpresa. Si tu `node -v` se queda corto, actualiza antes de seguir:
>
> ```bash
> # con nvm
> nvm install 22 && nvm use 22
> ```

## Estructura que vamos a construir

```
code/
├── backend/                  Node 22 + TypeScript + Express
│   ├── package.json
│   ├── tsconfig.json
│   └── src/
│       └── servidor.ts       Los 5 endpoints. Un solo fichero
└── frontend/                 Angular 22
    └── src/app/
        ├── auth.ts           El servicio: todo el WebAuthn
        ├── app.ts            El componente
        ├── app.html          La plantilla (3 líneas de formulario)
        └── app.css
```

Dos puertos:

- **3000** — el backend (Express)
- **4200** — el frontend (Angular)

Esa separación importa: el `origin` que configuramos en el backend tiene que ser exactamente la URL
donde sirve Angular.

## Arranca las instalaciones ya

Son un par de minutos cada una. Lánzalas y sigue leyendo:

```bash
cd code/backend  && npm install
cd ../frontend   && npm install
```

Siguiente: [`01-backend.md`](01-backend.md)
