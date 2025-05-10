# soil_config/config.py
# soil_config/config.py

CAMINHO_SHAPES = "dados/solos_sab250"

CORES_SOLOS = {
    "AR": "#a0522d", "CXa": "#ff00ff", "CXbd": "#c0d904", "CXbe": "#6f7fc7", "CXk": "#c0d904",
    "CXve": "#b50057", "CYbe": "#6f7fc7", "Dn": "#7df2a0", "EKo": "#9b30ff", "FFc": "#bfa329",
    "FFlf": "#67c233", "FTd": "#c2ff29", "FTe": "#49e4cf", "FXd": "#c2ff29", "GJo": "#a167f2",
    "GMa": "#67c233", "GMbe": "#b89df9", "GMve": "#67df1f", "GXbd": "#e92bce", "GXbe": "#cc8854",
    "GXvd": "#e92bce", "GXve": "#00cb91", "GZn": "#2d84e6", "LAa": "#eb4d1c", "LAd": "#e31239",
    "LAdf": "#0000ff", "LAdx": "#8ce8c3", "LAe": "#c28ee8", "LAw": "#0fd3f3", "LVAa": "#0000ff",
    "LVAd": "#f44336", "LVAe": "#de8782", "LVd": "#5e71cf", "LVdf": "#0e00ff", "LVe": "#09f745",
    "LVw": "#99dc3c", "MDo": "#bfa329", "MTo": "#f18bb1", "MXo": "#c96b30", "NVe": "#98e789",
    "OXfi": "#3be1d2", "PACd": "#3a00a6", "PAd": "#3f92bf", "PAdx": "#ff00ff", "PAe": "#07d928",
    "PVa": "#6aff5d", "PVAd": "#d673d8", "PVAe": "#4dff98", "PVd": "#87c3ea", "PVe": "#66c8cf",
    "RLd": "#7de3cd", "RLe": "#d8a542", "RLk": "#c0d904", "RQg": "#b50057", "RQo": "#e92bce",
    "RRd": "#dada48", "RRe": "#a167f2", "RYbd": "#20b76a", "RYbe": "#42b1e0", "RYve": "#c2132d",
    "SNo": "#e98a17", "SNz": "#c7101e", "SXd": "#5695db", "SXe": "#00cb91", "TCk": "#00ef32",
    "TCo": "#dada48", "TCp": "#cc8a73", "TXp": "#e6cd69", "VEk": "#d1345b", "VEo": "#5f81cc",
    "VXk": "#c459df", "VXO": "#3be1d2"
}

CAMADAS_DISPONIVEIS = {
    "Limites do Semiárido": "limites_semiarido.shp",
    "Estados do Semiárido": "Estados_Semiarido.shp",
    "Caatinga": "caatinga/caatinga.shp",
    "Matopiba": "sab_matopiba/sab_matopiba.shp"
}

CAMADAS_GEOMORFOLOGIA = {
    "Planalto Aluvial": "geomorfologia_caatinga/aluvial_plains.shp",
    "Planalto Borborema": "geomorfologia_caatinga/Borborema_highlands.shp",
    "Chapada Diamantina e Espinhaço": "geomorfologia_caatinga/Chapada_diamantina_and_espinhaço_highlands.shp",
    "Planícies Costeiras": "geomorfologia_caatinga/coastal_plains.shp",
    "Tabuleiros Costeiros": "geomorfologia_caatinga/costal_tablelands.shp",
    "Maciços Cristalinos": "geomorfologia_caatinga/crystalline_massifs.shp",
    "Dunas e Paleodunas": "geomorfologia_caatinga/dunes_and_paleodunes.shp",
    "Superfícies Sedimentares Baixas": "geomorfologia_caatinga/low_sedimentary_surfaces.shp",
    "Planalto Sedimentar Alto": "geomorfologia_caatinga/sedimentary_plateau_high.shp",
    "Superfície Sertaneja Norte": "geomorfologia_caatinga/sertaneja_surface_north.shp",
    "Superfície Sertaneja Sul": "geomorfologia_caatinga/sertaneja_surface_south.shp",
    "Superfície Sertaneja Pré-Costal": "geomorfologia_caatinga/sertaneja_surface_pre_costal.shp",
}

CORES_GEOMORFOLOGIA = {
    "Planalto Aluvial": "#8dd3c7",
    "Planalto Borborema": "#ffffb3",
    "Chapada Diamantina e Espinhaço": "#bebada",
    "Planícies Costeiras": "#fb8072",
    "Tabuleiros Costeiros": "#80b1d3",
    "Maciços Cristalinos": "#fdb462",
    "Dunas e Paleodunas": "#b3de69",
    "Superfícies Sedimentares Baixas": "#fccde5",
    "Planalto Sedimentar Alto": "#d9d9d9",
    "Superfície Sertaneja Norte": "#bc80bd",
    "Superfície Sertaneja Pré-Costal": "#ccebc5",
    "Superfície Sertaneja Sul": "#ffed6f",
}