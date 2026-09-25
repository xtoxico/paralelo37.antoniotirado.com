# Diapositivas

Presentación en [reveal.js](https://revealjs.com) 6. **Funciona sin conexión**: la librería está
incluida en `vendor/`, no se descarga nada de internet.

## Abrirla

Doble clic en `index.html`, o:

```bash
xdg-open index.html     # Linux
open index.html         # macOS
start index.html        # Windows
```

## Atajos durante la charla

| Tecla | Acción |
|---|---|
| `→` / `espacio` | Siguiente |
| `←` | Anterior |
| **`S`** | **Vista de ponente**: notas, reloj y siguiente diapositiva |
| `Esc` | Vista general de todas las diapositivas |
| `F` | Pantalla completa |
| `B` o `.` | Pantalla en negro — úsalo cuando quieras que te miren a ti |
| `Alt + clic` | Zoom sobre un punto concreto (útil en los bloques de código) |

> La vista de ponente abre una ventana nueva. Si el navegador la bloquea, permite las ventanas
> emergentes para este fichero.

## Notas del ponente

Cada diapositiva con demo o con una frase clave lleva sus notas dentro de un
`<aside class="notes">`. Se ven con `S`. El desarrollo completo, con tiempos y plan B, está en
[`../guion.md`](../guion.md).

## Exportar a PDF

```
index.html?print-pdf
```

Abre esa URL en Chrome y usa *Imprimir → Guardar como PDF*, con márgenes en «ninguno» y gráficos de
fondo activados.

## Editarla

Es HTML plano. Cada `<section>` es una diapositiva. Clases disponibles:

| Clase | Para qué |
|---|---|
| `.grande` | Frase destacada a pantalla completa |
| `.acento` | Verde menta — lo importante |
| `.aviso` | Rojo suave — peligros y errores |
| `.dos` | Rejilla de dos columnas |
| `.caja` | Bloque con fondo sutil, para usar dentro de `.dos` |
| `.pie` | Texto pequeño y atenuado |

Para resaltar líneas de código progresivamente, usa `data-line-numbers="1-2|4-5"` en el `<code>`.
