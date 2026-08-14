"""
Genera el mapa estático de la ruta de evaluación en campo (Bogotá -> Cali),
a partir de las coordenadas resueltas del enlace de Google Maps
https://maps.app.goo.gl/jvosbfadpWZmckoD6 (extraídas del parámetro
!1d{lon}!2d{lat} de la URL de direcciones resuelta, en el mismo orden
en que aparecen los puntos en la ruta).
"""
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import LineString, Point

DEPARTAMENTOS = "/Users/mauricio/Documents/Data-science-local/MR-Web/datascience/mapas/data/col_departamentos.geojson"
OUT_PNG = "/Users/mauricio/Documents/Data-science-local/A-SCR/Libros-SCR/viviendas-afectadas/media/02-ruta-evaluacion/ruta_evaluacion.png"

# (nombre, lon, lat), en el orden de la ruta
PUNTOS = [
    ("Bogotá", -74.072092, 4.7109886),
    ("Manizales", -75.5176778, 5.0677303),
    ("El Águila", -76.0417277, 4.9083995),
    ("Ansermanuevo", -75.9948121, 4.7945134),
    ("El Cairo", -76.2216962, 4.7607704),
    ("Argelia", -76.121514, 4.727773),
    ("La Unión", -76.1033371, 4.5332092),
    ("Sevilla", -75.931004, 4.2743779),
    ("Vijes", -76.4426126, 3.6998526),
    ("Cali", -76.5319854, 3.4516467),
]

gdf_puntos = gpd.GeoDataFrame(
    {"nombre": [p[0] for p in PUNTOS], "orden": range(1, len(PUNTOS) + 1)},
    geometry=[Point(p[1], p[2]) for p in PUNTOS],
    crs="EPSG:4326",
)
ruta = LineString([(p[1], p[2]) for p in PUNTOS])
gdf_ruta = gpd.GeoDataFrame({"nombre": ["Ruta"]}, geometry=[ruta], crs="EPSG:4326")

deptos = gpd.read_file(DEPARTAMENTOS)

fig, ax = plt.subplots(figsize=(7, 9), dpi=300)

deptos.plot(ax=ax, color="#eef0f2", edgecolor="#9aa5b1", linewidth=0.4, zorder=0)

gdf_ruta.plot(ax=ax, color="#223764", linewidth=1.8, linestyle="--", zorder=1)
gdf_puntos.plot(ax=ax, color="#c0392b", markersize=45, zorder=2, edgecolor="white", linewidth=0.8)

# Desplazamientos manuales de etiqueta (en puntos) para evitar solapes en el
# clúster de municipios cercanos entre sí (El Águila / Ansermanuevo / El Cairo / Argelia)
OFFSETS = {
    "El Águila": (8, 10),
    "Ansermanuevo": (10, -2),
    "El Cairo": (-70, 6),
    "Argelia": (10, -14),
    "La Unión": (8, 6),
}

for _, row in gdf_puntos.iterrows():
    dx, dy = OFFSETS.get(row.nombre, (6, 4))
    ax.annotate(
        f"{row.orden}. {row.nombre}",
        xy=(row.geometry.x, row.geometry.y),
        xytext=(dx, dy),
        textcoords="offset points",
        fontsize=7,
        fontweight="bold",
        color="#1a1a1a",
    )

# Encuadre: bbox de la ruta con margen
minx, miny, maxx, maxy = gdf_puntos.total_bounds
mx, my = (maxx - minx) * 0.18, (maxy - miny) * 0.10
ax.set_xlim(minx - mx, maxx + mx)
ax.set_ylim(miny - my, maxy + my)
ax.set_aspect("equal")
ax.set_axis_off()

ax.set_title("Ruta de evaluación en campo: Bogotá – Cali", fontsize=11, color="#223764", pad=10)

fig.tight_layout()
fig.savefig(OUT_PNG, dpi=300, bbox_inches="tight", facecolor="white")
print(f"Guardado: {OUT_PNG}")
