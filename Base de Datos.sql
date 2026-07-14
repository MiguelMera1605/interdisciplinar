USE proyectointerdisciplinar

CREATE TABLE Proyecto (
    id_proyecto INT IDENTITY(1,1) PRIMARY KEY,
    nombre NVARCHAR(100) NOT NULL,
    descripcion NVARCHAR(MAX),
    objetivos NVARCHAR(MAX),
    funcionamiento NVARCHAR(MAX),
    fecha_creacion DATE
);

CREATE TABLE Materiales (
    id_material INT IDENTITY(1,1) PRIMARY KEY,
    id_proyecto INT NOT NULL,
    nombre NVARCHAR(100) NOT NULL,
    cantidad INT,
    descripcion NVARCHAR(MAX),
    CONSTRAINT FK_Materiales_Proyecto
        FOREIGN KEY (id_proyecto) REFERENCES Proyecto(id_proyecto)
);

CREATE TABLE Fotografias (
    id_foto INT IDENTITY(1,1) PRIMARY KEY,
    id_proyecto INT NOT NULL,
    titulo NVARCHAR(100),
    ruta_imagen NVARCHAR(255),
    descripcion NVARCHAR(MAX),
    CONSTRAINT FK_Fotografias_Proyecto
        FOREIGN KEY (id_proyecto) REFERENCES Proyecto(id_proyecto)
        );

CREATE TABLE Mantenimiento (
    id_mantenimiento INT IDENTITY(1,1) PRIMARY KEY,
    id_proyecto INT NOT NULL,
    actividad NVARCHAR(150),
    descripcion NVARCHAR(MAX),
    frecuencia NVARCHAR(50),
    CONSTRAINT FK_Mantenimiento_Proyecto
        FOREIGN KEY (id_proyecto) REFERENCES Proyecto(id_proyecto)
);


CREATE TABLE Caracteristicas (
    id_caracteristica INT IDENTITY(1,1) PRIMARY KEY,
    id_proyecto INT NOT NULL,
    nombre NVARCHAR(100),
    valor NVARCHAR(100),
    CONSTRAINT FK_Caracteristicas_Proyecto
        FOREIGN KEY (id_proyecto) REFERENCES Proyecto(id_proyecto)
);
