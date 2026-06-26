import os

# Configuración básica
INTENTOS_MAX = 6
LARGO_PALABRA = 5
ARCHIVO_STATS = "estadisticas.json"

LISTA_PALABRAS = [
    "abrir","acaba","aguar","ahora","aires","ambos","amiga","amigo","antes","apoyo","aquel","ayuda",
    "baile","bajar","bajas","banca","banco","banda","barra","basar","bases","basta","borde","buena",
    "bueno","busca","busco","calle","carga","casar","casas","causa","cerca","china","cinco","clave",
    "coche","comer","corta","corte","cosas","creer","datos","deben","deber","decir","dejan","dejar",
    "dicen","dicho","doble","donde","dudar","echar","ellas","ellos","entra","entre","estar","estas",
    "estos","estoy","falla","falta","fecha","feria","ficha","final","finca","fines","firma","firme",
    "forma","fotos","fuera","fuese","funda","gafas","ganar","ganas","gasto","gesto","gozar","grafo",
    "grasa","grave","gripe","gusta","guste","gusto","haber","habla","hacen","hacer","hagan","hasta",
    "hayan","hecho","hijos","horas","ideal","idear","ideas","igual","imita","india","irnos","islas",
    "jefes","joven","juega","juego","jugar","junta","junto","jurar","justa","justo","karma","kilos",
    "kiwis","koala","larga","largo","leche","libre","libro","lista","llama","llega","llena","lleno",
    "lleva","lucha","luego","manga","manos","marca","marco","mayor","media","medio","mejor","menos",
    "meses","mirar","misma","mismo","monte","mucho","nadar","nadie","niega","nieve","norma","notas",
    "novia","nueva","nueve","nuevo","obrar","obras","obvio","ocupa","ojala","oliva","ondas","opera",
    "opina","orden","oreja","orina","otras","otros","padre","palma","parar","parir","parte","pasar",
    "playa","poder","poner","pueda","puede","puedo","punto","queda","queja","quema","queso","quien",
    "quiso","quita","quito","radio","redes","regla","reina","reino","renta","resto","reyes","rodea",
    "rompe","ronda","rosas","rueda","rutas","saben","saber","sabio","salir","santa","serie","siete",
    "sigue","sirve","sobre","somos","suele","suelo","tales","tanto","tarde","temas","temer","tener",
    "tenga","tengo","tiene","todas","todos","tomar","toque","trata","ubica","ultra","unido","urnas",
    "usaba","usado","usted","valer","valle","vamos","veces","vende","vendo","venir","viaje","viene",
    "vista","visto","viven","vivir","yacen","yacer","yates","yegua","yemas","yendo","yerba","yerno",
    "zanja","zetas","zonas","zorro","zumba","messi","tapar","ocaso"
]