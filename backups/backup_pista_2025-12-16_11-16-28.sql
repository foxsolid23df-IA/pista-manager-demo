--
-- PostgreSQL database dump
--

\restrict x3efoEWZjysE2pKzGvcqrGBWfHRvkNRwzfazLVyfz7VAqJUMkbNkIv2tnciSHeU

-- Dumped from database version 15.15
-- Dumped by pg_dump version 15.15

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alumnos; Type: TABLE; Schema: public; Owner: admin_pista
--

CREATE TABLE public.alumnos (
    id integer NOT NULL,
    nombre character varying,
    telefono_contacto character varying,
    nivel character varying,
    fecha_nacimiento date,
    fecha_registro timestamp without time zone,
    vencimiento_mensualidad date
);


ALTER TABLE public.alumnos OWNER TO admin_pista;

--
-- Name: alumnos_id_seq; Type: SEQUENCE; Schema: public; Owner: admin_pista
--

CREATE SEQUENCE public.alumnos_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.alumnos_id_seq OWNER TO admin_pista;

--
-- Name: alumnos_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin_pista
--

ALTER SEQUENCE public.alumnos_id_seq OWNED BY public.alumnos.id;


--
-- Name: clases; Type: TABLE; Schema: public; Owner: admin_pista
--

CREATE TABLE public.clases (
    id integer NOT NULL,
    nombre character varying,
    dia_semana character varying,
    hora_inicio character varying,
    instructor_id integer
);


ALTER TABLE public.clases OWNER TO admin_pista;

--
-- Name: clases_id_seq; Type: SEQUENCE; Schema: public; Owner: admin_pista
--

CREATE SEQUENCE public.clases_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.clases_id_seq OWNER TO admin_pista;

--
-- Name: clases_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin_pista
--

ALTER SEQUENCE public.clases_id_seq OWNED BY public.clases.id;


--
-- Name: inscripciones; Type: TABLE; Schema: public; Owner: admin_pista
--

CREATE TABLE public.inscripciones (
    id integer NOT NULL,
    alumno_id integer,
    clase_id integer
);


ALTER TABLE public.inscripciones OWNER TO admin_pista;

--
-- Name: inscripciones_id_seq; Type: SEQUENCE; Schema: public; Owner: admin_pista
--

CREATE SEQUENCE public.inscripciones_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.inscripciones_id_seq OWNER TO admin_pista;

--
-- Name: inscripciones_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin_pista
--

ALTER SEQUENCE public.inscripciones_id_seq OWNED BY public.inscripciones.id;


--
-- Name: instructores; Type: TABLE; Schema: public; Owner: admin_pista
--

CREATE TABLE public.instructores (
    id integer NOT NULL,
    nombre character varying,
    especialidad character varying,
    activo boolean
);


ALTER TABLE public.instructores OWNER TO admin_pista;

--
-- Name: instructores_id_seq; Type: SEQUENCE; Schema: public; Owner: admin_pista
--

CREATE SEQUENCE public.instructores_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.instructores_id_seq OWNER TO admin_pista;

--
-- Name: instructores_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin_pista
--

ALTER SEQUENCE public.instructores_id_seq OWNED BY public.instructores.id;


--
-- Name: pagos_escuela; Type: TABLE; Schema: public; Owner: admin_pista
--

CREATE TABLE public.pagos_escuela (
    id integer NOT NULL,
    alumno_id integer,
    monto double precision,
    fecha_pago timestamp without time zone,
    concepto character varying
);


ALTER TABLE public.pagos_escuela OWNER TO admin_pista;

--
-- Name: pagos_escuela_id_seq; Type: SEQUENCE; Schema: public; Owner: admin_pista
--

CREATE SEQUENCE public.pagos_escuela_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.pagos_escuela_id_seq OWNER TO admin_pista;

--
-- Name: pagos_escuela_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin_pista
--

ALTER SEQUENCE public.pagos_escuela_id_seq OWNED BY public.pagos_escuela.id;


--
-- Name: sesiones_patinaje; Type: TABLE; Schema: public; Owner: admin_pista
--

CREATE TABLE public.sesiones_patinaje (
    id integer NOT NULL,
    ticket_id character varying,
    hora_entrada timestamp without time zone,
    hora_salida timestamp without time zone,
    monto_total double precision,
    pagado boolean,
    tarifa_id integer
);


ALTER TABLE public.sesiones_patinaje OWNER TO admin_pista;

--
-- Name: sesiones_patinaje_id_seq; Type: SEQUENCE; Schema: public; Owner: admin_pista
--

CREATE SEQUENCE public.sesiones_patinaje_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.sesiones_patinaje_id_seq OWNER TO admin_pista;

--
-- Name: sesiones_patinaje_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin_pista
--

ALTER SEQUENCE public.sesiones_patinaje_id_seq OWNED BY public.sesiones_patinaje.id;


--
-- Name: tarifas; Type: TABLE; Schema: public; Owner: admin_pista
--

CREATE TABLE public.tarifas (
    id integer NOT NULL,
    nombre character varying,
    costo_base double precision,
    minutos_base integer,
    costo_minuto_extra double precision,
    activa boolean
);


ALTER TABLE public.tarifas OWNER TO admin_pista;

--
-- Name: tarifas_id_seq; Type: SEQUENCE; Schema: public; Owner: admin_pista
--

CREATE SEQUENCE public.tarifas_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tarifas_id_seq OWNER TO admin_pista;

--
-- Name: tarifas_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin_pista
--

ALTER SEQUENCE public.tarifas_id_seq OWNED BY public.tarifas.id;


--
-- Name: alumnos id; Type: DEFAULT; Schema: public; Owner: admin_pista
--

ALTER TABLE ONLY public.alumnos ALTER COLUMN id SET DEFAULT nextval('public.alumnos_id_seq'::regclass);


--
-- Name: clases id; Type: DEFAULT; Schema: public; Owner: admin_pista
--

ALTER TABLE ONLY public.clases ALTER COLUMN id SET DEFAULT nextval('public.clases_id_seq'::regclass);


--
-- Name: inscripciones id; Type: DEFAULT; Schema: public; Owner: admin_pista
--

ALTER TABLE ONLY public.inscripciones ALTER COLUMN id SET DEFAULT nextval('public.inscripciones_id_seq'::regclass);


--
-- Name: instructores id; Type: DEFAULT; Schema: public; Owner: admin_pista
--

ALTER TABLE ONLY public.instructores ALTER COLUMN id SET DEFAULT nextval('public.instructores_id_seq'::regclass);


--
-- Name: pagos_escuela id; Type: DEFAULT; Schema: public; Owner: admin_pista
--

ALTER TABLE ONLY public.pagos_escuela ALTER COLUMN id SET DEFAULT nextval('public.pagos_escuela_id_seq'::regclass);


--
-- Name: sesiones_patinaje id; Type: DEFAULT; Schema: public; Owner: admin_pista
--

ALTER TABLE ONLY public.sesiones_patinaje ALTER COLUMN id SET DEFAULT nextval('public.sesiones_patinaje_id_seq'::regclass);


--
-- Name: tarifas id; Type: DEFAULT; Schema: public; Owner: admin_pista
--

ALTER TABLE ONLY public.tarifas ALTER COLUMN id SET DEFAULT nextval('public.tarifas_id_seq'::regclass);


--
-- Data for Name: alumnos; Type: TABLE DATA; Schema: public; Owner: admin_pista
--

COPY public.alumnos (id, nombre, telefono_contacto, nivel, fecha_nacimiento, fecha_registro, vencimiento_mensualidad) FROM stdin;
2	PEPE EL TORO	6148429914	BASICO	2025-12-30	2025-12-16 16:06:17.199018	2025-12-31
3	JUAN PEREZ	string	string	2025-12-16	2025-12-16 16:12:32.126152	2026-02-14
1	PEPE EL TORO	6148429914	BASICO	2025-12-30	2025-12-16 16:06:14.473755	2026-01-15
\.


--
-- Data for Name: clases; Type: TABLE DATA; Schema: public; Owner: admin_pista
--

COPY public.clases (id, nombre, dia_semana, hora_inicio, instructor_id) FROM stdin;
\.


--
-- Data for Name: inscripciones; Type: TABLE DATA; Schema: public; Owner: admin_pista
--

COPY public.inscripciones (id, alumno_id, clase_id) FROM stdin;
\.


--
-- Data for Name: instructores; Type: TABLE DATA; Schema: public; Owner: admin_pista
--

COPY public.instructores (id, nombre, especialidad, activo) FROM stdin;
\.


--
-- Data for Name: pagos_escuela; Type: TABLE DATA; Schema: public; Owner: admin_pista
--

COPY public.pagos_escuela (id, alumno_id, monto, fecha_pago, concepto) FROM stdin;
1	2	500	2025-12-16 16:11:01.448065	PAGO
2	3	500	2025-12-16 16:12:51.424773	string
3	3	500	2025-12-16 16:12:53.308714	string
4	1	500	2025-12-16 16:45:03.377748	Mensualidad
\.


--
-- Data for Name: sesiones_patinaje; Type: TABLE DATA; Schema: public; Owner: admin_pista
--

COPY public.sesiones_patinaje (id, ticket_id, hora_entrada, hora_salida, monto_total, pagado, tarifa_id) FROM stdin;
1	1803F23C	2025-12-16 16:44:26.795036	2025-12-16 16:44:37.172352	100	t	1
\.


--
-- Data for Name: tarifas; Type: TABLE DATA; Schema: public; Owner: admin_pista
--

COPY public.tarifas (id, nombre, costo_base, minutos_base, costo_minuto_extra, activa) FROM stdin;
1	Hora Libre General	100	60	2.5	t
\.


--
-- Name: alumnos_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin_pista
--

SELECT pg_catalog.setval('public.alumnos_id_seq', 3, true);


--
-- Name: clases_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin_pista
--

SELECT pg_catalog.setval('public.clases_id_seq', 1, false);


--
-- Name: inscripciones_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin_pista
--

SELECT pg_catalog.setval('public.inscripciones_id_seq', 1, false);


--
-- Name: instructores_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin_pista
--

SELECT pg_catalog.setval('public.instructores_id_seq', 1, false);


--
-- Name: pagos_escuela_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin_pista
--

SELECT pg_catalog.setval('public.pagos_escuela_id_seq', 4, true);


--
-- Name: sesiones_patinaje_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin_pista
--

SELECT pg_catalog.setval('public.sesiones_patinaje_id_seq', 1, true);


--
-- Name: tarifas_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin_pista
--

SELECT pg_catalog.setval('public.tarifas_id_seq', 1, true);


--
-- Name: alumnos alumnos_pkey; Type: CONSTRAINT; Schema: public; Owner: admin_pista
--

ALTER TABLE ONLY public.alumnos
    ADD CONSTRAINT alumnos_pkey PRIMARY KEY (id);


--
-- Name: clases clases_pkey; Type: CONSTRAINT; Schema: public; Owner: admin_pista
--

ALTER TABLE ONLY public.clases
    ADD CONSTRAINT clases_pkey PRIMARY KEY (id);


--
-- Name: inscripciones inscripciones_pkey; Type: CONSTRAINT; Schema: public; Owner: admin_pista
--

ALTER TABLE ONLY public.inscripciones
    ADD CONSTRAINT inscripciones_pkey PRIMARY KEY (id);


--
-- Name: instructores instructores_pkey; Type: CONSTRAINT; Schema: public; Owner: admin_pista
--

ALTER TABLE ONLY public.instructores
    ADD CONSTRAINT instructores_pkey PRIMARY KEY (id);


--
-- Name: pagos_escuela pagos_escuela_pkey; Type: CONSTRAINT; Schema: public; Owner: admin_pista
--

ALTER TABLE ONLY public.pagos_escuela
    ADD CONSTRAINT pagos_escuela_pkey PRIMARY KEY (id);


--
-- Name: sesiones_patinaje sesiones_patinaje_pkey; Type: CONSTRAINT; Schema: public; Owner: admin_pista
--

ALTER TABLE ONLY public.sesiones_patinaje
    ADD CONSTRAINT sesiones_patinaje_pkey PRIMARY KEY (id);


--
-- Name: tarifas tarifas_nombre_key; Type: CONSTRAINT; Schema: public; Owner: admin_pista
--

ALTER TABLE ONLY public.tarifas
    ADD CONSTRAINT tarifas_nombre_key UNIQUE (nombre);


--
-- Name: tarifas tarifas_pkey; Type: CONSTRAINT; Schema: public; Owner: admin_pista
--

ALTER TABLE ONLY public.tarifas
    ADD CONSTRAINT tarifas_pkey PRIMARY KEY (id);


--
-- Name: ix_alumnos_id; Type: INDEX; Schema: public; Owner: admin_pista
--

CREATE INDEX ix_alumnos_id ON public.alumnos USING btree (id);


--
-- Name: ix_alumnos_nombre; Type: INDEX; Schema: public; Owner: admin_pista
--

CREATE INDEX ix_alumnos_nombre ON public.alumnos USING btree (nombre);


--
-- Name: ix_clases_id; Type: INDEX; Schema: public; Owner: admin_pista
--

CREATE INDEX ix_clases_id ON public.clases USING btree (id);


--
-- Name: ix_inscripciones_id; Type: INDEX; Schema: public; Owner: admin_pista
--

CREATE INDEX ix_inscripciones_id ON public.inscripciones USING btree (id);


--
-- Name: ix_instructores_id; Type: INDEX; Schema: public; Owner: admin_pista
--

CREATE INDEX ix_instructores_id ON public.instructores USING btree (id);


--
-- Name: ix_pagos_escuela_id; Type: INDEX; Schema: public; Owner: admin_pista
--

CREATE INDEX ix_pagos_escuela_id ON public.pagos_escuela USING btree (id);


--
-- Name: ix_sesiones_patinaje_id; Type: INDEX; Schema: public; Owner: admin_pista
--

CREATE INDEX ix_sesiones_patinaje_id ON public.sesiones_patinaje USING btree (id);


--
-- Name: ix_sesiones_patinaje_ticket_id; Type: INDEX; Schema: public; Owner: admin_pista
--

CREATE UNIQUE INDEX ix_sesiones_patinaje_ticket_id ON public.sesiones_patinaje USING btree (ticket_id);


--
-- Name: ix_tarifas_id; Type: INDEX; Schema: public; Owner: admin_pista
--

CREATE INDEX ix_tarifas_id ON public.tarifas USING btree (id);


--
-- Name: clases clases_instructor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin_pista
--

ALTER TABLE ONLY public.clases
    ADD CONSTRAINT clases_instructor_id_fkey FOREIGN KEY (instructor_id) REFERENCES public.instructores(id);


--
-- Name: inscripciones inscripciones_alumno_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin_pista
--

ALTER TABLE ONLY public.inscripciones
    ADD CONSTRAINT inscripciones_alumno_id_fkey FOREIGN KEY (alumno_id) REFERENCES public.alumnos(id);


--
-- Name: inscripciones inscripciones_clase_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin_pista
--

ALTER TABLE ONLY public.inscripciones
    ADD CONSTRAINT inscripciones_clase_id_fkey FOREIGN KEY (clase_id) REFERENCES public.clases(id);


--
-- Name: pagos_escuela pagos_escuela_alumno_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin_pista
--

ALTER TABLE ONLY public.pagos_escuela
    ADD CONSTRAINT pagos_escuela_alumno_id_fkey FOREIGN KEY (alumno_id) REFERENCES public.alumnos(id);


--
-- Name: sesiones_patinaje sesiones_patinaje_tarifa_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin_pista
--

ALTER TABLE ONLY public.sesiones_patinaje
    ADD CONSTRAINT sesiones_patinaje_tarifa_id_fkey FOREIGN KEY (tarifa_id) REFERENCES public.tarifas(id);


--
-- PostgreSQL database dump complete
--

\unrestrict x3efoEWZjysE2pKzGvcqrGBWfHRvkNRwzfazLVyfz7VAqJUMkbNkIv2tnciSHeU

