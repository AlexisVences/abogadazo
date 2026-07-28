-- PostgreSQL version para Neon.tech
-- Nota: Eliminamos configuraciones específicas de MySQL como ENGINE, CHARSET, etc.

-- Creación de tablas (sintaxis PostgreSQL)
CREATE TABLE usuario (
  id SERIAL PRIMARY KEY,
  usuario VARCHAR(100) NOT NULL UNIQUE,
  nombre VARCHAR(100) NOT NULL,
  apellido VARCHAR(100) NOT NULL,
  rol VARCHAR(100) NOT NULL,
  email VARCHAR(100) NOT NULL UNIQUE,
  password VARCHAR(100) NOT NULL
);

CREATE TABLE agentes_facultados (
  id SERIAL PRIMARY KEY,
  placa VARCHAR(50) NOT NULL,
  nombre VARCHAR(255) NOT NULL
);

CREATE TABLE consulta_agentes (
  id SERIAL PRIMARY KEY,
  fecha DATE NOT NULL,
  id_usuario INT,
  id_agente INT,
  CONSTRAINT fk_usuario FOREIGN KEY (id_usuario) REFERENCES usuario(id)
    ON DELETE SET NULL
    ON UPDATE CASCADE,
  CONSTRAINT fk_agente FOREIGN KEY (id_agente) REFERENCES agentes_facultados(id)
    ON DELETE SET NULL
    ON UPDATE CASCADE
);

CREATE TABLE consulta (
  id SERIAL PRIMARY KEY,
  fecha DATE NOT NULL,
  texto TEXT NOT NULL,
  id_usuario INT,
  CONSTRAINT fk_consulta_usuario FOREIGN KEY (id_usuario) REFERENCES usuario(id)
    ON DELETE SET NULL
    ON UPDATE CASCADE
);

CREATE TABLE respuesta (
  id SERIAL PRIMARY KEY,
  texto TEXT NOT NULL,
  tipo VARCHAR(50) NOT NULL,
  id_consulta INT,
  CONSTRAINT fk_respuesta_consulta FOREIGN KEY (id_consulta) REFERENCES consulta(id)
    ON DELETE SET NULL
    ON UPDATE CASCADE
);

CREATE TABLE retroalimentacion (
  id SERIAL PRIMARY KEY,
  estrellas INT NOT NULL CHECK (estrellas BETWEEN 1 AND 5),
  id_respuesta INT,
  CONSTRAINT fk_retroalimentacion_respuesta FOREIGN KEY (id_respuesta) REFERENCES respuesta(id)
    ON DELETE SET NULL
    ON UPDATE CASCADE
);