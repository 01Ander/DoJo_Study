CREATE TABLE authors (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE articles (
    id INTEGER PRIMARY KEY,
    author_id INTEGER,
    title TEXT NOT NULL,
    views INTEGER NOT NULL,
    FOREIGN KEY (author_id) REFERENCES authors(id)
);

INSERT INTO authors VALUES (1, 'Gabriel'), (2, 'Isabel'), (3, 'Mario');
INSERT INTO articles VALUES 
(101, 1, 'Cien Años', 5000), 
(102, 1, 'El Coronel', 1200), 
(103, 2, 'La Casa', 4300),
(104, NULL, 'Anonimo', 800);


SELECT
    a.name AS author_name,
    COUNT(art.id) AS total_articles,
    COALESCE(SUM(art.views), 0) AS total_views
FROM authors AS a
LEFT JOIN articles AS art ON a.id = art.author_id
GROUP BY a.name;