--
-- PostgreSQL database dump
--

\restrict iijOU1JYYrfMpz3LeEgRU834NeALtYjL8Vb0kRTusRJgSIVmNsCdYHg76k36rPN

-- Dumped from database version 18.2
-- Dumped by pg_dump version 18.2

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
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
-- Name: audit_logs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.audit_logs (
    id integer NOT NULL,
    username character varying(50) NOT NULL,
    action character varying(100) NOT NULL,
    details text,
    "timestamp" timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.audit_logs OWNER TO postgres;

--
-- Name: audit_logs_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.audit_logs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.audit_logs_id_seq OWNER TO postgres;

--
-- Name: audit_logs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.audit_logs_id_seq OWNED BY public.audit_logs.id;


--
-- Name: departments; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.departments (
    id integer NOT NULL,
    name character varying(100) NOT NULL
);


ALTER TABLE public.departments OWNER TO postgres;

--
-- Name: departments_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.departments_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.departments_id_seq OWNER TO postgres;

--
-- Name: departments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.departments_id_seq OWNED BY public.departments.id;


--
-- Name: students; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.students (
    student_id character varying(50) NOT NULL,
    name character varying(100) NOT NULL,
    email character varying(100) NOT NULL,
    phone character varying(20) NOT NULL,
    department character varying(100) NOT NULL,
    semester integer NOT NULL,
    cgpa numeric(3,2) NOT NULL,
    marks_json jsonb,
    total_marks numeric(6,2),
    maximum_marks numeric(6,2),
    percentage numeric(5,2),
    grade character varying(10)
);


ALTER TABLE public.students OWNER TO postgres;

--
-- Name: subjects; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.subjects (
    id integer NOT NULL,
    department_name character varying(100),
    subject_name character varying(100) NOT NULL
);


ALTER TABLE public.subjects OWNER TO postgres;

--
-- Name: subjects_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.subjects_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.subjects_id_seq OWNER TO postgres;

--
-- Name: subjects_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.subjects_id_seq OWNED BY public.subjects.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying(50) NOT NULL,
    email character varying(100) NOT NULL,
    password_hash character varying(255) NOT NULL,
    role character varying(20) DEFAULT 'student'::character varying NOT NULL,
    student_id character varying(50)
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: audit_logs id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.audit_logs ALTER COLUMN id SET DEFAULT nextval('public.audit_logs_id_seq'::regclass);


--
-- Name: departments id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.departments ALTER COLUMN id SET DEFAULT nextval('public.departments_id_seq'::regclass);


--
-- Name: subjects id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subjects ALTER COLUMN id SET DEFAULT nextval('public.subjects_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: audit_logs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.audit_logs (id, username, action, details, "timestamp") FROM stdin;
1	admin	Add Student	Added student ID 12	2026-09-05 23:16:53.359556
2	admin	User Login	Logged into system	2026-09-05 23:26:50.03358
3	admin	Add Student	Added student ID 13	2026-09-05 23:29:17.395489
4	admin	Export Data	Exported student records to Excel	2026-09-05 23:29:37.069215
5	admin	User Logout	Logged out	2026-09-05 23:54:37.082312
6	System	User Register	Registered uzair (student)	2026-09-05 23:58:29.881512
7	uzair	User Login	Logged in as student	2026-09-05 23:58:41.064828
8	admin	User Login	Logged in as admin	2026-09-07 10:50:07.41993
9	admin	User Login	Logged in as admin	2026-09-07 20:34:11.474864
10	admin	User Login	Logged in as admin	2026-09-07 20:37:20.290916
11	admin	Update Student	Updated student ID 6	2026-09-07 20:39:49.105338
12	admin	Update Student	Updated student ID 6	2026-09-07 20:40:22.974668
13	admin	Update Student	Updated student ID 1	2026-09-07 20:40:47.486806
14	admin	User Logout	Logged out	2026-09-07 20:42:44.35566
15	admin	User Login	Logged in as admin	2026-09-07 20:44:20.667323
16	admin	User Logout	Logged out	2026-09-07 20:44:39.578511
17	System	User Register	Registered muzammil (student)	2026-09-07 20:44:59.063129
18	muzammil	User Login	Logged in as student	2026-09-07 20:45:09.19739
19	muzammil	User Logout	Logged out	2026-09-07 20:53:31.86956
20	admin	User Login	Logged in as admin	2026-09-07 20:53:36.615411
21	admin	Update Student	Updated student ID 1	2026-09-07 20:54:03.252177
22	admin	User Logout	Logged out	2026-09-07 20:54:43.061274
23	uzair	User Login	Logged in as student	2026-09-07 20:54:47.083426
24	uzair	User Logout	Logged out	2026-09-07 20:55:46.774238
25	admin	User Login	Logged in as admin	2026-09-07 20:55:50.538051
26	admin	User Login	Logged in as admin	2026-09-07 20:58:14.70389
27	admin	User Login	Logged in as admin	2026-09-07 20:59:56.536667
28	admin	User Login	Logged in as admin	2026-09-07 21:09:13.763094
29	admin	Add Department	Added department Artificial Intelligence	2026-09-07 21:12:11.744057
30	admin	Add Subject	Added subject 'Deep learning' to Artificial Intelligence	2026-09-07 21:12:23.180774
31	admin	Add Subject	Added subject 'Machine Learning' to Artificial Intelligence	2026-09-07 21:12:45.005695
32	admin	Add Subject	Added subject 'Discrete Structures' to Artificial Intelligence	2026-09-07 21:12:56.634382
33	admin	Add Subject	Added subject 'Calculus' to Artificial Intelligence	2026-09-07 21:13:06.590379
34	admin	Update Student	Updated student ID 5	2026-09-07 21:13:40.926513
35	admin	Update Student	Updated student ID 5	2026-09-07 21:17:52.186861
36	admin	Update Student	Updated student ID 5	2026-09-07 21:18:06.574062
37	admin	User Login	Logged in as admin	2026-09-07 21:19:48.559267
38	admin	Bulk Import	Imported 0 students via file upload	2026-09-07 21:27:11.314338
39	admin	User Login	Logged in as admin	2026-09-08 00:12:12.364514
40	admin	User Login	Logged in as admin	2026-09-08 00:14:21.071843
41	admin	User Login	Logged in as admin	2026-09-19 18:21:12.085758
42	admin	Update Student	Updated student ID 1	2026-09-19 18:47:03.061763
43	admin	User Logout	Logged out	2026-09-19 18:47:26.649419
\.


--
-- Data for Name: departments; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.departments (id, name) FROM stdin;
1	Computer Science
2	Data Science
3	Software Engineering
4	Information Technology
5	Artificial Intelligence
\.


--
-- Data for Name: students; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.students (student_id, name, email, phone, department, semester, cgpa, marks_json, total_marks, maximum_marks, percentage, grade) FROM stdin;
2	rehan	rehan@gmail.com	03000000001	Computer Science	4	3.38	{"DLD": 88.0, "DBMS": 88.0, "Python": 77.0, "Calculus": 67.0, "Statistics": 78.0, "Mathematics": 89.0}	487.00	600.00	81.17	A
3	ayan	ayan@gmail.com	03000000002	Software Engineering	5	3.95	{}	\N	\N	\N	\N
4	ali	ali@gmail.com	03000000003	Information Technology	6	3.42	{}	\N	\N	\N	\N
7	abdul	abdul@gmail.com	03000000006	Computer Science	4	3.44	{"DLD": 78.0, "DBMS": 87.0, "Python": 77.0, "Calculus": 56.0, "Statistics": 67.0, "Mathematics": 97.0}	462.00	600.00	77.00	B
8	sameer	sameer@gmail.com	03000000007	Data Science	3	3.64	{"DLD": 56.0, "DBMS": 78.0, "Python": 88.0, "Calculus": 76.0, "Statistics": 77.0, "Mathematics": 67.0}	442.00	600.00	73.67	B
9	moiz	moiz@gmail.com	03000000008	Computer Science	4	3.77	{"DLD": 66.0, "DBMS": 77.0, "Python": 88.0, "Calculus": 87.0, "Statistics": 76.0, "Mathematics": 67.0}	461.00	600.00	76.83	B
10	waqas	waqas@gmail.com	03000000009	Software Engineering	3	3.31	{"DLD": 77.0, "DBMS": 65.0, "Python": 66.0, "Calculus": 54.0, "Statistics": 55.0, "Mathematics": 50.0}	367.00	600.00	61.17	C
11	arsalan	arsalan@gmail.com	03000000010	Data Science	2	3.86	{"DLD": 65.0, "DBMS": 87.0, "Python": 77.0, "Calculus": 76.0, "Statistics": 67.0, "Mathematics": 55.0}	427.00	600.00	71.17	B
12	sohaib	sohaib@gmail.com	03000000011	Software Engineering	7	3.11	{"SQA": 77.0, "DBMS": 76.0, "Software Design": 56.0, "Web Engineering": 87.0}	296.00	400.00	74.00	B
13	asif	asif@gmail.com	03000000012	Information Technology	8	3.67	{"Web Tech": 88.0, "Networking": 67.0, "Cyber Security": 77.0, "Cloud Computing": 99.0}	331.00	400.00	82.75	A
6	muzammil	bzumuzamil345@gmail.com	03000000005	Information Technology	3	3.04	{"Web Tech": 87.0, "Networking": 67.0, "Cyber Security": 78.0, "Cloud Computing": 72.0}	304.00	400.00	76.00	B
5	ukasha	hanai.imran913@gmail.com	03000000004	Data Science	3	3.62	{"Python": 66.0, "Statistics": 79.0, "Linear Algebra": 78.0, "Machine Learning": 66.0}	289.00	400.00	72.25	B
1	uzair	iqbaluzair507@gmail.com	03000000000	Data Science	3	3.57	{"Python": 91.0, "Statistics": 99.0, "Linear Algebra": 92.0, "Machine Learning": 88.0}	370.00	400.00	92.50	A+
\.


--
-- Data for Name: subjects; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.subjects (id, department_name, subject_name) FROM stdin;
1	Computer Science	Programming Fundamentals
2	Computer Science	Data Structures
3	Computer Science	Algorithms
4	Computer Science	Operating Systems
5	Data Science	Python Programming
6	Data Science	Statistics & Probability
7	Data Science	Machine Learning
8	Data Science	Data Mining
9	Software Engineering	Software Architecture
10	Software Engineering	Agile Methodologies
11	Software Engineering	Software Testing
12	Software Engineering	DBMS
13	Information Technology	Computer Networks
14	Information Technology	Cyber Security
15	Information Technology	Cloud Computing
16	Information Technology	Web Technologies
17	Artificial Intelligence	Deep learning
18	Artificial Intelligence	Machine Learning
19	Artificial Intelligence	Discrete Structures
20	Artificial Intelligence	Calculus
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, username, email, password_hash, role, student_id) FROM stdin;
1	admin	admin@school.com	scrypt:32768:8:1$0kQxwE1luAQo2nQY$1f22dedc8b6cf5186f70fd3679d9a5517de137b1a2abb00436fc1683e778a1dc6846ba80e28f0dcd3e7ce81af312cf17dfc17efe59f48cb4b175a8a14901b70b	admin	\N
2	uzair	uzair@gmail.com	scrypt:32768:8:1$i7Drqsr69CJEgRMQ$0b09c7ccfb238978ffc3784cabfaf5c6350f4c00faef05c5429c07c1bee516753717aff9f620905332dcf6f814c1f58eba5d5aa78c45dba7bcda9ca1ac9f7480	student	1
3	muzammil	bzumuzamil345@gmail.com	scrypt:32768:8:1$RDF5EqLW4Zu7MIOS$c1888135f05b35320eabb69a1cff056ac373b486e067eb08dae7f8e0681cfaf06adad9a83c9e08f60ec259bf8273493b2eeef4c23ea26411ff256220f036ef26	student	6
\.


--
-- Name: audit_logs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.audit_logs_id_seq', 43, true);


--
-- Name: departments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.departments_id_seq', 5, true);


--
-- Name: subjects_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.subjects_id_seq', 20, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 3, true);


--
-- Name: audit_logs audit_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.audit_logs
    ADD CONSTRAINT audit_logs_pkey PRIMARY KEY (id);


--
-- Name: departments departments_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.departments
    ADD CONSTRAINT departments_name_key UNIQUE (name);


--
-- Name: departments departments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.departments
    ADD CONSTRAINT departments_pkey PRIMARY KEY (id);


--
-- Name: students students_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.students
    ADD CONSTRAINT students_email_key UNIQUE (email);


--
-- Name: students students_phone_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.students
    ADD CONSTRAINT students_phone_key UNIQUE (phone);


--
-- Name: students students_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.students
    ADD CONSTRAINT students_pkey PRIMARY KEY (student_id);


--
-- Name: subjects subjects_department_name_subject_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subjects
    ADD CONSTRAINT subjects_department_name_subject_name_key UNIQUE (department_name, subject_name);


--
-- Name: subjects subjects_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subjects
    ADD CONSTRAINT subjects_pkey PRIMARY KEY (id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: subjects subjects_department_name_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subjects
    ADD CONSTRAINT subjects_department_name_fkey FOREIGN KEY (department_name) REFERENCES public.departments(name) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

\unrestrict iijOU1JYYrfMpz3LeEgRU834NeALtYjL8Vb0kRTusRJgSIVmNsCdYHg76k36rPN

