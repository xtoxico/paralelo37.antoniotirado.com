# Instrucciones paso a paso

Todo lo necesario para construir el proyecto **desde cero**, partiendo de un equipo con Node 22
instalado. Cada fichero es un bloque del taller y contiene **todo el código**, no fragmentos.

| Fichero | Contenido | Tiempo en el taller |
|---|---|---|
| [`00-requisitos.md`](00-requisitos.md) | Qué hay que tener instalado y cómo comprobarlo | 0:00 – 0:08 |
| [`01-backend.md`](01-backend.md) | Express + TypeScript: los 5 endpoints, línea a línea | 0:50 – 1:15 |
| [`02-frontend.md`](02-frontend.md) | Angular 22: el servicio y el componente | 1:15 – 1:35 |
| [`03-probar.md`](03-probar.md) | Probarlo con biometría, con autenticador virtual y con una Pico | 1:35 – 1:57 |
| [`04-errores.md`](04-errores.md) | Los fallos que van a salir y cómo se arreglan | — |

## Atajo

Si alguien se queda atrás durante el taller, el proyecto terminado está en `code/backend` y
`code/frontend`. Basta con:

```bash
cd code/backend  && npm install && npm start
cd code/frontend && npm install && npm start
```

Y abrir <http://localhost:4200>.
