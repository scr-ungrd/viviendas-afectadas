# CLAUDE.md

Guía para Claude Code al trabajar en este repositorio.

## Qué es esto

Libro digital Quarto (`project: type: book`) en español: **"Viviendas Afectadas"**, producido por la Subdirección de Conocimiento del Riesgo (SCR) de la UNGRD. Estructura y estilos calcados de `../exposicion/exposicion-edificaciones` (mismo `CLAUDE.md` de referencia para las convenciones institucionales: clases `.ungrd-*` en `custom.css`, paleta institucional, `caption-bold.html`).

Repo: `github.com/scr-ungrd/viviendas-afectadas`, publicado en `https://scr-ungrd.github.io/viviendas-afectadas/` vía `.github/workflows/publish.yml` (igual que el resto de libros SCR).

## Origen: capítulo movido desde otro libro

El capítulo 1 (`01-viviendas-afectadas.qmd`, tabla + mapa D3/OJS coroplético del Valle del Cauca + gráfico de barras del `% de viviendas afectadas`) se movió tal cual desde el capítulo 3 de `scr-ungrd/exposicion-edificaciones`, junto con `data/procesar_viviendas_afectadas.py` y `data/viviendas_afectadas_valle.csv`. `data/colombia_moderate.topojson` se copió (no se movió) porque el libro de origen lo sigue usando en su propio mapa.

El mapa D3/OJS de este capítulo hereda la misma regla de esa migración: **cada celda `{ojs}` debe tener una sola declaración top-level**, o el mapa se queda cargando indefinidamente en proyectos `type: book` (bug de Quarto documentado en detalle en el `CLAUDE.md` de `exposicion-edificaciones`, sección "Bug de Quarto: celdas `{ojs}`..."). Ese mismo `CLAUDE.md` documentaba además una discrepancia local/producción no resuelta en el libro de origen: el mapa funcionaba en local (`npx serve`) pero, al último chequeo de ese libro, no cargaba los datos en GitHub Pages. **En este libro (`viviendas-afectadas`) esa discrepancia no se reprodujo**: verificado en 2026-08-14 en el sitio publicado (`https://scr-ungrd.github.io/viviendas-afectadas/`) que tanto el mapa D3/OJS como el gráfico de barras del capítulo 1 cargan los datos correctamente en producción.

## Capítulo 2: ruta de evaluación

`02-ruta-evaluacion.qmd` — mapa estático (no D3/OJS, por la discrepancia local/producción mencionada arriba) de la ruta de evaluación en campo Bogotá–Cali, seguido del cronograma día a día. Generado **fuera del render** con `data/graficar_ruta.py` (matplotlib + geopandas, ejecutado manualmente: `python3 data/graficar_ruta.py`) a partir de coordenadas resueltas manualmente del enlace corto de Google Maps (`curl -sIL <link>`, extrayendo los pares `!1d{lon}!2d{lat}` de la URL de direcciones resuelta) → `media/02-ruta-evaluacion/ruta_evaluacion.png`, versionado en git. El `.qmd` lo referencia como una imagen markdown normal (`![...](media/...png)`), **no** como celda `{python}` — el runner de GitHub Actions de este libro no tiene Jupyter/`nbformat` instalado (el `publish.yml`, copiado de un libro que solo usa OJS, no incluye un paso de setup de Python), así que una celda ejecutable de Python rompe el CI aunque funcione en local. Si se necesita regenerar el mapa (nueva ruta, nuevos municipios), hay que volver a correr el script a mano y confirmar el PNG actualizado en el commit.

Si se repite este proceso con otra ruta: usar `curl -sIL <enlace-corto-de-maps>` y leer la cabecera `location` de la redirección; ahí aparece la URL completa `/maps/dir/.../@lat,lng,zoom/data=...!1d{lon}!2d{lat}!...` con las coordenadas exactas de cada parada, en orden.

## Comandos

```bash
quarto preview          # servidor local con recarga en vivo al editar .qmd/.css
quarto render           # compila el sitio HTML estático a _book/
quarto render --to pdf  # compila la versión PDF (requiere motor LaTeX, p.ej. TinyTeX)
```

## Pendientes conocidos

- Portada propia (actualmente usa el logo genérico UNGRD).
- DOI y metadatos definitivos en `Pagina-legal.qmd` (placeholders `PENDIENTE`).
- Fuente/fecha del evento de origen de `VIVIENDAS AFECTADAS ANALISIS.xlsx` sin documentar en el Excel original.

## Estructura y orden de capítulos

```
index.qmd → Pagina-legal.qmd → 01-viviendas-afectadas.qmd → 02-ruta-evaluacion.qmd
```
