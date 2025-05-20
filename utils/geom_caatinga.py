from pathlib import Path

# ======= Caminhos principais =======
BASE_DIR = Path("dados").resolve()

CAMADAS_GEOMORFOLOGIA = {
    "Planalto Aluvial": BASE_DIR / "geomorfologia_caatinga" / "aluvial_plains.shp",
    "Planalto Borborema": BASE_DIR / "geomorfologia_caatinga" / "Borborema_highlands.shp",
    "Chapada Diamantina e Espinhaço": BASE_DIR / "geomorfologia_caatinga" / "Chapada_diamantina_and_espinhaço_highlands.shp",
    "Planícies Costeiras": BASE_DIR / "geomorfologia_caatinga" / "coastal_plains.shp",
    "Tabuleiros Costeiros": BASE_DIR / "geomorfologia_caatinga" / "costal_tablelands.shp",
    "Maciços Cristalinos": BASE_DIR / "geomorfologia_caatinga" / "crystalline_massifs.shp",
    "Dunas e Paleodunas": BASE_DIR / "geomorfologia_caatinga" / "dunes_and_paleodunes.shp",
    "Superfícies Sedimentares Baixas": BASE_DIR / "geomorfologia_caatinga" / "low_sedimentary_surfaces.shp",
    "Planalto Sedimentar Alto": BASE_DIR / "geomorfologia_caatinga" / "sedimentary_plateau_high.shp",
    "Superfície Sertaneja Norte": BASE_DIR / "geomorfologia_caatinga" / "sertaneja_surface_north.shp",
    "Superfície Sertaneja Sul": BASE_DIR / "geomorfologia_caatinga" / "sertaneja_surface_south.shp",
    "Superfície Sertaneja Pré-Costal": BASE_DIR / "geomorfologia_caatinga" / "sertaneja_surface_pre_costal.shp",
}