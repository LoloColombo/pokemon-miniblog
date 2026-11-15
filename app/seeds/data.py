import os

SEED_PASSWORD = os.getenv("SEED_PASSWORD", "pokemon123")

USERS = [
    {"username": "profesor-oak", "email": "oak@pokeblog.com", "role": "admin"},
    {"username": "misty", "email": "misty@pokeblog.com", "role": "editor"},
    {"username": "brock", "email": "brock@pokeblog.com", "role": "editor"},
    {"username": "ash", "email": "ash@pokeblog.com", "role": "user"},
]

CATEGORIES = [
    {"name": "Fuego", "slug": "fuego"},
    {"name": "Agua", "slug": "agua"},
    {"name": "Planta", "slug": "planta"},
    {"name": "Eléctrico", "slug": "electrico"},
    {"name": "Psíquico", "slug": "psiquico"},
    {"name": "Roca", "slug": "roca"},
    {"name": "Dragón", "slug": "dragon"},
    {"name": "Fantasma", "slug": "fantasma"},
    {"name": "Normal", "slug": "normal"},
]

TAGS = [
    "kanto",
    "johto",
    "hoenn",
    "inicial",
    "legendario",
    "competitivo",
    "evolucion",
    "shiny",
]

POSTS = [
    {
        "title": "Pikachu: el ratón eléctrico más famoso",
        "content": "Pikachu es un Pokémon de tipo Eléctrico que evoluciona de Pichu y puede evolucionar a Raichu con una Piedra Trueno.",
        "category": "electrico",
        "tags": ["kanto", "evolucion"],
        "author": "ash",
    },
    {
        "title": "Charmander, Squirtle o Bulbasaur: cuál elegir",
        "content": "Guía rápida para elegir tu inicial de Kanto según tu estilo de juego y los primeros gimnasios.",
        "category": "fuego",
        "tags": ["kanto", "inicial"],
        "author": "profesor-oak",
    },
    {
        "title": "Starmie en el equipo de Misty",
        "content": "Starmie es un Pokémon de tipo Agua y Psíquico, rápido y con gran variedad de movimientos especiales.",
        "category": "agua",
        "tags": ["kanto", "competitivo"],
        "author": "misty",
    },
    {
        "title": "Onix y la defensa de los Pokémon tipo Roca",
        "content": "Onix tiene una defensa física muy alta, pero sufre mucho contra ataques de tipo Agua y Planta.",
        "category": "roca",
        "tags": ["kanto", "evolucion"],
        "author": "brock",
    },
    {
        "title": "Mewtwo, el legendario creado en un laboratorio",
        "content": "Mewtwo es un Pokémon legendario de tipo Psíquico creado a partir del ADN de Mew.",
        "category": "psiquico",
        "tags": ["kanto", "legendario", "competitivo"],
        "author": "profesor-oak",
    },
    {
        "title": "Gengar y las estrategias con tipo Fantasma",
        "content": "Gengar combina los tipos Fantasma y Veneno y es muy usado por su velocidad y su ataque especial.",
        "category": "fantasma",
        "tags": ["kanto", "competitivo", "shiny"],
        "author": "misty",
    },
]
