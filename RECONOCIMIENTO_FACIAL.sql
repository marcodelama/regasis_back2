CREATE TABLE asistencia (
    n_id_asistencia        INTEGER NOT NULL PRIMARY KEY,
    t_hora_inicio          TIMESTAMP,
    t_hora_fin             TIMESTAMP,
    c_estado               CHAR(1 CHAR),
    d_fecha                DATE,
    personal_n_id_personal INTEGER NOT NULL
);

CREATE TABLE dependencia (
    n_id_dependencia INTEGER NOT NULL PRIMARY KEY,
    v_descripcion    VARCHAR2(70),
    v_abreviatura    VARCHAR2(70)
);

CREATE TABLE espacio_aula (
    n_id_espacio_aula            INTEGER NOT NULL PRIMARY KEY,
    n_capacidad                  INTEGER,
    dependencia_n_id_dependencia INTEGER NOT NULL
);

CREATE TABLE espacio_aula_personal (
    n_id_aula_personal             INTEGER NOT NULL PRIMARY KEY,
    personal_n_id_personal         INTEGER NOT NULL,
    espacio_aula_n_id_espacio_aula INTEGER NOT NULL
);

CREATE TABLE espacio_turno (
    n_id_espacio_turno             INTEGER NOT NULL PRIMARY KEY,
    espacio_aula_n_id_espacio_aula INTEGER NOT NULL,
    turno_n_id_turno               INTEGER NOT NULL
);

CREATE TABLE evento (
    n_id_evento    INTEGER NOT NULL PRIMARY KEY,
    v_cod_evento   CHAR(7),
    v_nombre       VARCHAR2(90),
    d_fecha_inicio DATE,
    d_fecha_fin    DATE,
    c_estado       CHAR(1 CHAR)
);

CREATE TABLE personal (
    n_id_personal          INTEGER NOT NULL PRIMARY KEY,
    v_cod_personal         NCHAR(7),
    v_nombre               VARCHAR2(70),
    v_apellido_paterno     VARCHAR2(70),
    v_apellido_materno     VARCHAR2(70),
    v_correo_institucional VARCHAR2(80),
    n_telefono_contacto    INTEGER,
    n_num_doc              INTEGER,
    v_disponibilidad       VARCHAR2(20),
    c_estado               CHAR(1 CHAR)
);

CREATE TABLE reporte (
    n_id_reporte       INTEGER NOT NULL PRIMARY KEY,
    v_tipo_reporte     VARCHAR2(70),
    d_fecha_generacion TIMESTAMP,
    evento_n_id_evento INTEGER NOT NULL
);

CREATE TABLE repositorio_imagen (
    n_id_rep_imagen        INTEGER NOT NULL PRIMARY KEY,
    imagen_biometrica      VARCHAR2(200),
    personal_n_id_personal INTEGER NOT NULL
);

CREATE TABLE log_reconocimiento(
    n_id_log_reconocimiento INTEGER NOT NULL PRIMARY KEY,
    v_evento VARCHAR2(55),
    v_tabla VARCHAR2(55),
    cl_row_data CLOB,
    d_fec_registro DATE,
    d_fec_actividad DATE,
    v_ip_usuario VARCHAR2(55),
    personal_n_id_personal INTEGER
);

CREATE TABLE tipo_personal (
    n_id_tipo_personal INTEGER NOT NULL PRIMARY KEY,
    v_descripcion      VARCHAR2(50)
);

CREATE TABLE turno (
    n_id_turno         INTEGER NOT NULL PRIMARY KEY,
    t_hora_inicio      TIMESTAMP,
    t_hora_fin         TIMESTAMP,
    d_fecha            DATE,
    c_estado           CHAR(1),
    evento_n_id_evento INTEGER NOT NULL
);

ALTER TABLE asistencia
    ADD CONSTRAINT asistencia_personal_fk FOREIGN KEY ( personal_n_id_personal )
        REFERENCES personal ( n_id_personal );

ALTER TABLE espacio_aula
    ADD CONSTRAINT espacio_aula_dependencia_fk FOREIGN KEY ( dependencia_n_id_dependencia )
        REFERENCES dependencia ( n_id_dependencia );

--  ERROR: FK name length exceeds maximum allowed length(30) 
ALTER TABLE espacio_aula_personal
    ADD CONSTRAINT espacio_aula_personal_espacio_aula_fk FOREIGN KEY ( espacio_aula_n_id_espacio_aula )
        REFERENCES espacio_aula ( n_id_espacio_aula );

--  ERROR: FK name length exceeds maximum allowed length(30) 
ALTER TABLE espacio_aula_personal
    ADD CONSTRAINT espacio_aula_personal_personal_fk FOREIGN KEY ( personal_n_id_personal )
        REFERENCES personal ( n_id_personal );

ALTER TABLE espacio_turno
    ADD CONSTRAINT espacio_turno_espacio_aula_fk FOREIGN KEY ( espacio_aula_n_id_espacio_aula )
        REFERENCES espacio_aula ( n_id_espacio_aula );

ALTER TABLE espacio_turno
    ADD CONSTRAINT espacio_turno_turno_fk FOREIGN KEY ( turno_n_id_turno )
        REFERENCES turno ( n_id_turno );

ALTER TABLE reporte
    ADD CONSTRAINT reporte_evento_fk FOREIGN KEY ( evento_n_id_evento )
        REFERENCES evento ( n_id_evento );

ALTER TABLE repositorio_imagen
    ADD CONSTRAINT repositorio_imagen_personal_fk FOREIGN KEY ( personal_n_id_personal )
        REFERENCES personal ( n_id_personal );
        
ALTER TABLE log_reconocimiento
    ADD CONSTRAINT log_reconocimiento_personal_fk FOREIGN KEY ( personal_n_id_personal )
        REFERENCES personal ( n_id_personal );

ALTER TABLE turno
    ADD CONSTRAINT turno_evento_fk FOREIGN KEY ( evento_n_id_evento )
        REFERENCES evento ( n_id_evento );

CREATE SEQUENCE asistencia_n_id_asistencia_seq START WITH 1 NOCACHE ORDER;

CREATE OR REPLACE TRIGGER asistencia_n_id_asistencia_trg BEFORE
    INSERT ON asistencia
    FOR EACH ROW
    WHEN ( new.n_id_asistencia IS NULL )
BEGIN
    :new.n_id_asistencia := asistencia_n_id_asistencia_seq.nextval;
END;
/

CREATE SEQUENCE dependencia_n_id_dependencia START WITH 1 NOCACHE ORDER;

CREATE OR REPLACE TRIGGER dependencia_n_id_dependencia BEFORE
    INSERT ON dependencia
    FOR EACH ROW
    WHEN ( new.n_id_dependencia IS NULL )
BEGIN
    :new.n_id_dependencia := dependencia_n_id_dependencia.nextval;
END;
/

CREATE SEQUENCE espacio_aula_n_id_espacio_aula START WITH 1 NOCACHE ORDER;

CREATE OR REPLACE TRIGGER espacio_aula_n_id_espacio_aula BEFORE
    INSERT ON espacio_aula
    FOR EACH ROW
    WHEN ( new.n_id_espacio_aula IS NULL )
BEGIN
    :new.n_id_espacio_aula := espacio_aula_n_id_espacio_aula.nextval;
END;
/

CREATE SEQUENCE espacio_aula_personal_n_id_aul START WITH 1 NOCACHE ORDER;

CREATE OR REPLACE TRIGGER espacio_aula_personal_n_id_aul BEFORE
    INSERT ON espacio_aula_personal
    FOR EACH ROW
    WHEN ( new.n_id_aula_personal IS NULL )
BEGIN
    :new.n_id_aula_personal := espacio_aula_personal_n_id_aul.nextval;
END;
/

CREATE SEQUENCE espacio_turno_n_id_espacio_tur START WITH 1 NOCACHE ORDER;

CREATE OR REPLACE TRIGGER espacio_turno_n_id_espacio_tur BEFORE
    INSERT ON espacio_turno
    FOR EACH ROW
    WHEN ( new.n_id_espacio_turno IS NULL )
BEGIN
    :new.n_id_espacio_turno := espacio_turno_n_id_espacio_tur.nextval;
END;
/

CREATE SEQUENCE evento_n_id_evento_seq START WITH 1 NOCACHE ORDER;

CREATE OR REPLACE TRIGGER evento_n_id_evento_trg BEFORE
    INSERT ON evento
    FOR EACH ROW
    WHEN ( new.n_id_evento IS NULL )
BEGIN
    :new.n_id_evento := evento_n_id_evento_seq.nextval;
END;
/

CREATE SEQUENCE personal_n_id_personal_seq START WITH 1 NOCACHE ORDER;

CREATE OR REPLACE TRIGGER personal_n_id_personal_trg BEFORE
    INSERT ON personal
    FOR EACH ROW
    WHEN ( new.n_id_personal IS NULL )
BEGIN
    :new.n_id_personal := personal_n_id_personal_seq.nextval;
END;
/

CREATE SEQUENCE reporte_n_id_reporte_seq START WITH 1 NOCACHE ORDER;

CREATE OR REPLACE TRIGGER reporte_n_id_reporte_trg BEFORE
    INSERT ON reporte
    FOR EACH ROW
    WHEN ( new.n_id_reporte IS NULL )
BEGIN
    :new.n_id_reporte := reporte_n_id_reporte_seq.nextval;
END;
/

CREATE SEQUENCE log_reconocimiento_n_id_log_reconocimiento START WITH 1 NOCACHE ORDER;

CREATE SEQUENCE repositorio_imagen_n_id_rep_im START WITH 1 NOCACHE ORDER;

CREATE OR REPLACE TRIGGER repositorio_imagen_n_id_rep_im BEFORE
    INSERT ON repositorio_imagen
    FOR EACH ROW
    WHEN ( new.n_id_rep_imagen IS NULL )
BEGIN
    :new.n_id_rep_imagen := repositorio_imagen_n_id_rep_im.nextval;
END;
/

CREATE SEQUENCE turno_n_id_turno_seq START WITH 1 NOCACHE ORDER;

CREATE OR REPLACE TRIGGER turno_n_id_turno_trg BEFORE
    INSERT ON turno
    FOR EACH ROW
    WHEN ( new.n_id_turno IS NULL )
BEGIN
    :new.n_id_turno := turno_n_id_turno_seq.nextval;
END;
/