PRAGMA foreign_keys = ON; 
BEGIN TRANSACTION;

-- Tabla principal de miniaturas
CREATE TABLE miniature (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT
);

-- Metadatos visuales de cada miniatura
CREATE TABLE visual_metadata (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    miniature_id INTEGER NOT NULL,
    main_color TEXT,
    secondary_color TEXT,
    shape TEXT,
    bioform TEXT,
    material TEXT,
    weight REAL,
    height REAL,
    radius_of_base REAL,
    FOREIGN KEY (miniature_id) REFERENCES miniature(id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Información de "lore" o trasfondo
CREATE TABLE lore (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    miniature_id INTEGER NOT NULL,
    designer TEXT,
    painted_by TEXT,
    label TEXT,
    lore_is_canon INTEGER,            -- 0/1 en vez de TINYINT
    character_origin TEXT,
    story TEXT,
    comment TEXT,
    year TEXT,
    code_or_reference TEXT,
    url TEXT,
    FOREIGN KEY (miniature_id) REFERENCES miniature(id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Tabla de etiquetas (tags)
CREATE TABLE tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tag TEXT
);

-- Relación de muchos-a-muchos entre miniaturas y tags
CREATE TABLE miniature_tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    miniature_id INTEGER NOT NULL,
    tag_id INTEGER NOT NULL,
    FOREIGN KEY (miniature_id) REFERENCES miniature(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Tipos de vista (por ejemplo, "frontal", "lateral", etc.)
CREATE TABLE view_types (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    view_type TEXT
);

-- Tabla para almacenar vistas específicas de la miniatura
CREATE TABLE miniature_views (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    miniature_id INTEGER NOT NULL,
    view_type_id INTEGER NOT NULL,
    url TEXT,
    FOREIGN KEY (miniature_id) REFERENCES miniature(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (view_type_id) REFERENCES view_types(id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Insertar los valores en la tabla
INSERT INTO View_Types (view_type)
VALUES 
    ('Frontal'),
    ('Black Background'),
    ('White Background'),
    ('Lateral View 1'),
    ('Lateral View 2'),
    ('Back View'),
    ('Top View'),
    ('Bottom View'),
    ('Close-up View'),
    ('Isometric View'),
    ('3D Model View'),
    ('Video or GIF'),
    ('Other View');

-- Insertar los valores en la tabla
INSERT INTO tags (tag)
VALUES
    ('Sci-Fi'),
    ('Fantasy'),
    ('Horror'),
    ('Cyberpunk'),
    ('Space Opera'),
    ('Anime'),
    ('Cartoon'),
    ('Comics'),
    ('Adult Animation'),
    ('Videogames'),
    ('D&D'),
    ('Warhammer40k'),
    ('Marvel'),
    ('DC'),
    ('Star Wars'),
    ('Starfinder'),
    ('Pathfinder'),
    ('Stargrave'),
    ('General Culture'),
    ('Aliens'),
    ('Creatures'),
    ('Robots'),
    ('Tech'),
    ('Folklore'),
    ('Terror'),
    ('Mythology'),
    ('History'),
    ('Medieval'),
    ('Renaissance'),
    ('Modern'),
    ('Future'),
    ('Post-Apocalyptic'),
    ('Steampunk'),
    ('Tabletop Games'),
    ('Board Games');
-- Aqui se pueden agregar mas tags si es necesario
COMMIT;
