'''Banco de preguntas - CULTURA E HISTORIA
Las preguntas están alojadas en diccionarios, cada diccionario tiene tres claves: 
1. texto: el valor corresponde a la pregunta que estamos haciendo 
2. opciones: es una lista con las opciones de respuesta que se le proporcionan al usuario
3. correcta: el valor corresponde al índice de la respuesta correcta en la lista "opciones" 

Los diccionarios de cada pregunta están alojados en tres listas: 
1. preguntas_faciles: preguntas de menor dificultad
2. preguntas_intermedias: preguntas de dificultad media
3. preguntas_dificiles: preguntas de mayor dificultad'''


preguntas_faciles = [
    {
        "texto": "¿En qué año llegó Cristóbal Colón a América?",
        "opciones": ["1492", "1500", "1482", "1510"],
        "correcta": 0
    },
    {
        "texto": "¿Cuál es la capital de Francia?",
        "opciones": ["Londres", "Berlín", "París", "Madrid"],
        "correcta": 2
    },
    {
        "texto": "¿Quién escribió 'Don Quijote de la Mancha'?",
        "opciones": ["Lope de Vega", "Miguel de Cervantes", "García Lorca", "Calderón de la Barca"],
        "correcta": 1
    },
    {
        "texto": "¿En qué continente está Egipto?",
        "opciones": ["Asia", "Europa", "África", "América"],
        "correcta": 2
    },
    {
        "texto": "¿Cuántos continentes hay en el mundo?",
        "opciones": ["5", "6", "7", "8"],
        "correcta": 2
    }
]


preguntas_intermedias = [
    {
        "texto": "¿Quién pintó 'La última cena'?",
        "opciones": ["Miguel Ángel", "Leonardo da Vinci", "Rafael", "Donatello"],
        "correcta": 1
    },
    {
        "texto": "¿En qué año comenzó la Segunda Guerra Mundial?",
        "opciones": ["1939", "1941", "1914", "1945"],
        "correcta": 0
    },
    {
        "texto": "¿Qué civilización construyó Machu Picchu?",
        "opciones": ["Aztecas", "Mayas", "Incas", "Olmecas"],
        "correcta": 2
    },
    {
        "texto": "¿Quién fue el primer presidente de Estados Unidos?",
        "opciones": ["Thomas Jefferson", "George Washington", "Abraham Lincoln", "Benjamin Franklin"],
        "correcta": 1
    },
    {
        "texto": "¿En qué país se encuentra la Torre de Pisa?",
        "opciones": ["Francia", "España", "Italia", "Grecia"],
        "correcta": 2
    }
]


preguntas_dificiles = [
    {
        "texto": "¿En qué año cayó el Imperio Romano de Occidente?",
        "opciones": ["476 d.C.", "410 d.C.", "395 d.C.", "500 d.C."],
        "correcta": 0
    },
    {
        "texto": "¿Quién escribió 'Cien años de soledad'?",
        "opciones": ["Mario Vargas Llosa", "Gabriel García Márquez", "Pablo Neruda", "Julio Cortázar"],
        "correcta": 1
    },
    {
        "texto": "¿En qué batalla fue derrotado definitivamente Napoleón Bonaparte?",
        "opciones": ["Austerlitz", "Leipzig", "Waterloo", "Jena"],
        "correcta": 2
    },
    {
        "texto": "¿Qué filósofo griego fue maestro de Platón?",
        "opciones": ["Aristóteles", "Sócrates", "Pitágoras", "Heráclito"],
        "correcta": 1
    },
    {
        "texto": "¿En qué año se firmó la Declaración de Independencia de Estados Unidos?",
        "opciones": ["1776", "1789", "1783", "1765"],
        "correcta": 0
    }
]