import os

# Configuración básica del juego
INTENTOS_MAX = 6
LARGO_PALABRA = 5
ARCHIVO_STATS = "estadisticas.json"

LISTA_PALABRAS = [
    "medio", "fecha", "buena", "norma", "viven", "manga", "gafas", "dudar",
    "guste", "ideas", "mismo", "tarde", "quiso", "barra", "justa", "jefe",
    "leche", "igual", "mirar", "fines", "falla", "menos", "hayan", "hacer",
    "reino", "mismo", "tapar", "yates", "cerca", "estas", "gripe", "gusta",
    "redes", "ocaso", "viaje", "coche", "visto", "abrir", "vende", "entra",
    "bueno", "meses", "hecho", "vamos", "ubica", "forma", "tomar", "basta",
    "junto", "banco", "marca", "borde", "antes", "hagan", "unido", "poner",
    "largo", "aquel", "causa", "firme", "ideal", "final", "libre", "playa",
    "ayuda", "karma", "zumba", "casas", "quien", "novia", "viene", "yerba",
    "hijos", "usted", "usted", "hacia", "finca", "paso", "comer", "cinco",
    "puedo", "fuera", "lleno", "regla", "luego", "llena", "baile", "sobre",
    "idear", "calle", "zorro", "banca", "quema", "hacen", "bravo", "lucha",
    "casar", "saber", "gesto", "pueda", "siete", "bajas", "queto", "obrar",
    "corta", "bajar", "suele", "reina", "visto", "tales", "rumbo", "puedo",
    "creer", "carga", "misma", "deber", "tanto", "quien", "dicho", "donde",
    "pueda", "horas", "somos", "banco", "valle", "tiene", "toque", "renta",
    "radio", "punto", "mundo", "gozar", "hijo", "salir", "mayor", "ayuda",
    "reyes", "marco", "nadie", "quema", "mismo", "sigue", "nieve", "padre",
    "fotos", "gusta", "dejan", "ultra", "viven", "sirve", "urnas", "doble",
    "trata", "firma", "yerno", "poder", "yegua", "funda", "amiga", "corte",
    "yacen", "hacer", "hijos", "koala", "forma", "juego", "larga", "nieve",
    "amigo", "jugar", "joven", "junta", "juez", "kilos", "kiwis", "libro",
    "lista", "llama", "llega", "lleva", "manos", "marco", "media", "mejor",
    "monte", "mucho", "nadar", "niega", "notas", "nueva", "nueve", "nuevo",
    "obras", "obvio", "ocupa", "ojala", "oliva", "ondas", "opera", "opina",
    "orden", "oreja", "orina", "otras", "otros", "palma", "parar", "parir",
    "parte", "pasar", "queda", "queja", "queso", "quita", "quito", "resto",
    "rodea", "rompe", "ronda", "rosas", "rueda", "rutas", "saben", "sabio",
    "santa", "serie", "suelo", "tanto", "temas", "temer", "tener", "tenga",
    "tengo", "todas", "todos", "valer", "vendo", "venir", "vista", "vivir",
    "yacer", "yemas", "yendo", "zanja", "zetas", "zonas", "messi", "tapar"
]