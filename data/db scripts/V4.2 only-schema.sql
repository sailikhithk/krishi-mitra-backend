--
-- PostgreSQL database dump
--

-- Dumped from database version 12.17 (Ubuntu 12.17-1.pgdg20.04+1)
-- Dumped by pg_dump version 16.1 (Ubuntu 16.1-1.pgdg20.04+1)

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

--
-- Name: public; Type: SCHEMA; Schema: -; Owner: postgres
--

-- *not* creating schema, since initdb creates it


ALTER SCHEMA public OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: assignment; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.assignment (
    id integer NOT NULL,
    name character varying,
    description character varying,
    skills_required character varying,
    max_time_min integer,
    always_open_submission boolean,
    deadline timestamp without time zone,
    auto_reminders boolean,
    auto_assignment_notification boolean,
    allows_late_submission boolean,
    number_of_reattempt integer,
    questions json,
    base_combination json,
    status character varying,
    is_active boolean,
    created_by integer,
    updated_by integer,
    created_date timestamp without time zone NOT NULL,
    updated_date timestamp without time zone NOT NULL
);


ALTER TABLE public.assignment OWNER TO postgres;

--
-- Name: assignment_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.assignment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.assignment_id_seq OWNER TO postgres;

--
-- Name: assignment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.assignment_id_seq OWNED BY public.assignment.id;


--
-- Name: assignment_user_mapping; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.assignment_user_mapping (
    id integer NOT NULL,
    assignment integer,
    user_by integer,
    assignment_attempt_history json,
    is_late_attempt boolean,
    is_qualified boolean,
    created_date timestamp without time zone NOT NULL,
    updated_date timestamp without time zone NOT NULL
);


ALTER TABLE public.assignment_user_mapping OWNER TO postgres;

--
-- Name: assignment_user_mapping_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.assignment_user_mapping_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.assignment_user_mapping_id_seq OWNER TO postgres;

--
-- Name: assignment_user_mapping_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.assignment_user_mapping_id_seq OWNED BY public.assignment_user_mapping.id;


--
-- Name: branch; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.branch (
    id integer NOT NULL,
    name character varying(100),
    created_date timestamp without time zone NOT NULL,
    updated_date timestamp without time zone NOT NULL
);


ALTER TABLE public.branch OWNER TO postgres;

--
-- Name: branch_course_mapping; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.branch_course_mapping (
    id integer NOT NULL,
    branch_id integer,
    course_id integer,
    is_active boolean,
    created_date timestamp without time zone NOT NULL,
    updated_date timestamp without time zone NOT NULL
);


ALTER TABLE public.branch_course_mapping OWNER TO postgres;

--
-- Name: branch_course_mapping_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.branch_course_mapping_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.branch_course_mapping_id_seq OWNER TO postgres;

--
-- Name: branch_course_mapping_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.branch_course_mapping_id_seq OWNED BY public.branch_course_mapping.id;


--
-- Name: branch_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.branch_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.branch_id_seq OWNER TO postgres;

--
-- Name: branch_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.branch_id_seq OWNED BY public.branch.id;


--
-- Name: company; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.company (
    id integer NOT NULL,
    name character varying(100),
    category character varying(100),
    spread_across json,
    working_domain character varying(100),
    about_company json,
    latest_news json,
    created_date timestamp without time zone NOT NULL,
    updated_date timestamp without time zone NOT NULL,
    industry_trends json,
    designations json
);


ALTER TABLE public.company OWNER TO postgres;

--
-- Name: company_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.company_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.company_id_seq OWNER TO postgres;

--
-- Name: company_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.company_id_seq OWNED BY public.company.id;


--
-- Name: configuration_history; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.configuration_history (
    id integer NOT NULL,
    category character varying,
    version character varying,
    details json,
    created_by integer,
    updated_by integer,
    created_date timestamp without time zone NOT NULL,
    updated_date timestamp without time zone NOT NULL,
    status character varying,
    error character varying
);


ALTER TABLE public.configuration_history OWNER TO postgres;

--
-- Name: configuration_history_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.configuration_history_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.configuration_history_id_seq OWNER TO postgres;

--
-- Name: configuration_history_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.configuration_history_id_seq OWNED BY public.configuration_history.id;


--
-- Name: country; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.country (
    id integer NOT NULL,
    name character varying(100),
    created_date timestamp without time zone NOT NULL,
    updated_date timestamp without time zone NOT NULL
);


ALTER TABLE public.country OWNER TO postgres;

--
-- Name: country_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.country_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.country_id_seq OWNER TO postgres;

--
-- Name: country_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.country_id_seq OWNED BY public.country.id;


--
-- Name: course; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.course (
    id integer NOT NULL,
    name character varying(100),
    created_date timestamp without time zone NOT NULL,
    updated_date timestamp without time zone NOT NULL
);


ALTER TABLE public.course OWNER TO postgres;

--
-- Name: course_department_mapping; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.course_department_mapping (
    id integer NOT NULL,
    course_id integer,
    department_id integer,
    is_active boolean,
    created_date timestamp without time zone NOT NULL,
    updated_date timestamp without time zone NOT NULL
);


ALTER TABLE public.course_department_mapping OWNER TO postgres;

--
-- Name: course_department_mapping_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.course_department_mapping_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.course_department_mapping_id_seq OWNER TO postgres;

--
-- Name: course_department_mapping_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.course_department_mapping_id_seq OWNED BY public.course_department_mapping.id;


--
-- Name: course_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.course_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.course_id_seq OWNER TO postgres;

--
-- Name: course_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.course_id_seq OWNED BY public.course.id;


--
-- Name: department; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.department (
    id integer NOT NULL,
    name character varying(100),
    created_date timestamp without time zone NOT NULL,
    updated_date timestamp without time zone NOT NULL
);


ALTER TABLE public.department OWNER TO postgres;

--
-- Name: department_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.department_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.department_id_seq OWNER TO postgres;

--
-- Name: department_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.department_id_seq OWNED BY public.department.id;


--
-- Name: hard_skill; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.hard_skill (
    id integer NOT NULL,
    name character varying(100),
    created_date timestamp without time zone NOT NULL,
    updated_date timestamp without time zone NOT NULL
);


ALTER TABLE public.hard_skill OWNER TO postgres;

--
-- Name: hard_skill_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.hard_skill_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.hard_skill_id_seq OWNER TO postgres;

--
-- Name: hard_skill_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.hard_skill_id_seq OWNED BY public.hard_skill.id;


--
-- Name: institution_branch_mapping; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.institution_branch_mapping (
    id integer NOT NULL,
    institution_id integer,
    branch_id integer,
    is_active boolean,
    created_date timestamp without time zone NOT NULL,
    updated_date timestamp without time zone NOT NULL
);


ALTER TABLE public.institution_branch_mapping OWNER TO postgres;

--
-- Name: institution_branch_mapping_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.institution_branch_mapping_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.institution_branch_mapping_id_seq OWNER TO postgres;

--
-- Name: institution_branch_mapping_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.institution_branch_mapping_id_seq OWNED BY public.institution_branch_mapping.id;


--
-- Name: institution_company_mapping; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.institution_company_mapping (
    id integer NOT NULL,
    institution_id integer,
    company_id integer,
    is_active boolean,
    created_date timestamp without time zone NOT NULL,
    updated_date timestamp without time zone NOT NULL,
    role_ids character varying
);


ALTER TABLE public.institution_company_mapping OWNER TO postgres;

--
-- Name: institution_company_mapping_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.institution_company_mapping_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.institution_company_mapping_id_seq OWNER TO postgres;

--
-- Name: institution_company_mapping_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.institution_company_mapping_id_seq OWNED BY public.institution_company_mapping.id;


--
-- Name: institution_hard_skill_mapping; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.institution_hard_skill_mapping (
    id integer NOT NULL,
    institution_id integer,
    skill_id integer,
    is_active boolean,
    created_date timestamp without time zone NOT NULL,
    updated_date timestamp without time zone NOT NULL
);


ALTER TABLE public.institution_hard_skill_mapping OWNER TO postgres;

--
-- Name: institution_hard_skill_mapping_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.institution_hard_skill_mapping_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.institution_hard_skill_mapping_id_seq OWNER TO postgres;

--
-- Name: institution_hard_skill_mapping_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.institution_hard_skill_mapping_id_seq OWNED BY public.institution_hard_skill_mapping.id;


--
-- Name: institution_master; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.institution_master (
    id integer NOT NULL,
    institution_name character varying(255),
    contact_name character varying(255),
    email character varying(255),
    phone_number character varying(255),
    country_id integer,
    city character varying(255),
    desiganation character varying(255),
    number_of_students integer,
    number_of_departments integer,
    registration_number character varying(255),
    domains character varying(255),
    preference_days character varying(255),
    preference_time character varying(255),
    password_hash character varying(255),
    is_active boolean,
    created_date timestamp without time zone NOT NULL,
    updated_date timestamp without time zone NOT NULL,
    password_modified_date timestamp without time zone,
    last_login_date timestamp without time zone,
    interview_questions_mode character varying,
    initial_configuration boolean,
    configuration_version json,
    latest_configuration_date timestamp without time zone
);


ALTER TABLE public.institution_master OWNER TO postgres;

--
-- Name: institution_master_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.institution_master_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.institution_master_id_seq OWNER TO postgres;

--
-- Name: institution_master_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.institution_master_id_seq OWNED BY public.institution_master.id;


--
-- Name: institution_soft_skill_mapping; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.institution_soft_skill_mapping (
    id integer NOT NULL,
    institution_id integer,
    skill_id integer,
    is_active boolean,
    created_date timestamp without time zone NOT NULL,
    updated_date timestamp without time zone NOT NULL
);


ALTER TABLE public.institution_soft_skill_mapping OWNER TO postgres;

--
-- Name: institution_soft_skill_mapping_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.institution_soft_skill_mapping_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.institution_soft_skill_mapping_id_seq OWNER TO postgres;

--
-- Name: institution_soft_skill_mapping_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.institution_soft_skill_mapping_id_seq OWNED BY public.institution_soft_skill_mapping.id;


--
-- Name: interview_master; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.interview_master (
    id integer NOT NULL,
    user_id integer,
    specifications json,
    level character varying(100),
    status character varying(100),
    path_json json,
    result_json json,
    report_json json,
    created_date timestamp without time zone NOT NULL,
    updated_date timestamp without time zone NOT NULL,
    prioritize boolean,
    improvement_areas_count integer,
    percentage real,
    marks real,
    max_marks real,
    skill_gap_rate real,
    improvement_areas json,
    un_relevant_answers integer,
    relevant_answers integer
);


ALTER TABLE public.interview_master OWNER TO postgres;

--
-- Name: interview_master_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.interview_master_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.interview_master_id_seq OWNER TO postgres;

--
-- Name: interview_master_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.interview_master_id_seq OWNED BY public.interview_master.id;


--
-- Name: question; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.question (
    id integer NOT NULL,
    role_name character varying(100),
    value json,
    created_date timestamp without time zone NOT NULL,
    updated_date timestamp without time zone NOT NULL
);


ALTER TABLE public.question OWNER TO postgres;

--
-- Name: question_bank; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.question_bank (
    id integer NOT NULL,
    name character varying,
    questions json,
    base_combination json,
    status character varying,
    is_active boolean,
    created_by integer,
    updated_by integer,
    created_date timestamp without time zone NOT NULL,
    updated_date timestamp without time zone NOT NULL
);


ALTER TABLE public.question_bank OWNER TO postgres;

--
-- Name: question_bank_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.question_bank_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.question_bank_id_seq OWNER TO postgres;

--
-- Name: question_bank_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.question_bank_id_seq OWNED BY public.question_bank.id;


--
-- Name: question_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.question_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.question_id_seq OWNER TO postgres;

--
-- Name: question_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.question_id_seq OWNED BY public.question.id;


--
-- Name: report_point; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.report_point (
    id integer NOT NULL,
    key character varying(100),
    value json,
    created_date timestamp without time zone NOT NULL,
    updated_date timestamp without time zone NOT NULL
);


ALTER TABLE public.report_point OWNER TO postgres;

--
-- Name: report_point_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.report_point_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.report_point_id_seq OWNER TO postgres;

--
-- Name: report_point_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.report_point_id_seq OWNED BY public.report_point.id;


--
-- Name: role; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.role (
    id integer NOT NULL,
    name character varying(64),
    created_date timestamp without time zone NOT NULL,
    updated_date timestamp without time zone NOT NULL
);


ALTER TABLE public.role OWNER TO postgres;

--
-- Name: role_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.role_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.role_id_seq OWNER TO postgres;

--
-- Name: role_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.role_id_seq OWNED BY public.role.id;


--
-- Name: soft_skill; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.soft_skill (
    id integer NOT NULL,
    name character varying(100),
    created_date timestamp without time zone NOT NULL,
    updated_date timestamp without time zone NOT NULL
);


ALTER TABLE public.soft_skill OWNER TO postgres;

--
-- Name: soft_skill_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.soft_skill_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.soft_skill_id_seq OWNER TO postgres;

--
-- Name: soft_skill_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.soft_skill_id_seq OWNED BY public.soft_skill.id;


--
-- Name: user_master; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_master (
    id integer NOT NULL,
    first_name character varying(255),
    last_name character varying(255),
    phone_number character varying(255),
    address character varying(255),
    email character varying(255),
    branch_id integer,
    department_id integer,
    institution_id integer,
    programme character varying(255),
    course_id integer,
    password_hash character varying(128),
    role_id integer,
    number_of_interviews integer,
    is_active boolean,
    created_date timestamp without time zone NOT NULL,
    updated_date timestamp without time zone NOT NULL,
    initial_password_reset boolean,
    password_modified_date timestamp without time zone,
    last_login_date timestamp without time zone,
    certified_hard_skills character varying,
    certified_soft_skills character varying,
    hard_skill_avg_score character varying,
    soft_skill_avg_score character varying,
    negative_emotions character varying,
    uncertified_hard_skills character varying,
    uncertified_soft_skills character varying
);


ALTER TABLE public.user_master OWNER TO postgres;

--
-- Name: user_master_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.user_master_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.user_master_id_seq OWNER TO postgres;

--
-- Name: user_master_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.user_master_id_seq OWNED BY public.user_master.id;


--
-- Name: working_role; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.working_role (
    id integer NOT NULL,
    name character varying(100),
    responsibilities json,
    skills json,
    created_date timestamp without time zone NOT NULL,
    updated_date timestamp without time zone NOT NULL
);


ALTER TABLE public.working_role OWNER TO postgres;

--
-- Name: working_role_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.working_role_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.working_role_id_seq OWNER TO postgres;

--
-- Name: working_role_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.working_role_id_seq OWNED BY public.working_role.id;


--
-- Name: assignment id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.assignment ALTER COLUMN id SET DEFAULT nextval('public.assignment_id_seq'::regclass);


--
-- Name: assignment_user_mapping id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.assignment_user_mapping ALTER COLUMN id SET DEFAULT nextval('public.assignment_user_mapping_id_seq'::regclass);


--
-- Name: branch id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.branch ALTER COLUMN id SET DEFAULT nextval('public.branch_id_seq'::regclass);


--
-- Name: branch_course_mapping id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.branch_course_mapping ALTER COLUMN id SET DEFAULT nextval('public.branch_course_mapping_id_seq'::regclass);


--
-- Name: company id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.company ALTER COLUMN id SET DEFAULT nextval('public.company_id_seq'::regclass);


--
-- Name: configuration_history id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.configuration_history ALTER COLUMN id SET DEFAULT nextval('public.configuration_history_id_seq'::regclass);


--
-- Name: country id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.country ALTER COLUMN id SET DEFAULT nextval('public.country_id_seq'::regclass);


--
-- Name: course id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.course ALTER COLUMN id SET DEFAULT nextval('public.course_id_seq'::regclass);


--
-- Name: course_department_mapping id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.course_department_mapping ALTER COLUMN id SET DEFAULT nextval('public.course_department_mapping_id_seq'::regclass);


--
-- Name: department id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.department ALTER COLUMN id SET DEFAULT nextval('public.department_id_seq'::regclass);


--
-- Name: hard_skill id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.hard_skill ALTER COLUMN id SET DEFAULT nextval('public.hard_skill_id_seq'::regclass);


--
-- Name: institution_branch_mapping id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.institution_branch_mapping ALTER COLUMN id SET DEFAULT nextval('public.institution_branch_mapping_id_seq'::regclass);


--
-- Name: institution_company_mapping id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.institution_company_mapping ALTER COLUMN id SET DEFAULT nextval('public.institution_company_mapping_id_seq'::regclass);


--
-- Name: institution_hard_skill_mapping id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.institution_hard_skill_mapping ALTER COLUMN id SET DEFAULT nextval('public.institution_hard_skill_mapping_id_seq'::regclass);


--
-- Name: institution_master id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.institution_master ALTER COLUMN id SET DEFAULT nextval('public.institution_master_id_seq'::regclass);


--
-- Name: institution_soft_skill_mapping id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.institution_soft_skill_mapping ALTER COLUMN id SET DEFAULT nextval('public.institution_soft_skill_mapping_id_seq'::regclass);


--
-- Name: interview_master id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.interview_master ALTER COLUMN id SET DEFAULT nextval('public.interview_master_id_seq'::regclass);


--
-- Name: question id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.question ALTER COLUMN id SET DEFAULT nextval('public.question_id_seq'::regclass);


--
-- Name: question_bank id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.question_bank ALTER COLUMN id SET DEFAULT nextval('public.question_bank_id_seq'::regclass);


--
-- Name: report_point id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.report_point ALTER COLUMN id SET DEFAULT nextval('public.report_point_id_seq'::regclass);


--
-- Name: role id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.role ALTER COLUMN id SET DEFAULT nextval('public.role_id_seq'::regclass);


--
-- Name: soft_skill id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.soft_skill ALTER COLUMN id SET DEFAULT nextval('public.soft_skill_id_seq'::regclass);


--
-- Name: user_master id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_master ALTER COLUMN id SET DEFAULT nextval('public.user_master_id_seq'::regclass);


--
-- Name: working_role id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.working_role ALTER COLUMN id SET DEFAULT nextval('public.working_role_id_seq'::regclass);


--
-- Name: assignment assignment_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.assignment
    ADD CONSTRAINT assignment_pkey PRIMARY KEY (id);


--
-- Name: assignment_user_mapping assignment_user_mapping_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.assignment_user_mapping
    ADD CONSTRAINT assignment_user_mapping_pkey PRIMARY KEY (id);


--
-- Name: branch_course_mapping branch_course_mapping_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.branch_course_mapping
    ADD CONSTRAINT branch_course_mapping_pkey PRIMARY KEY (id);


--
-- Name: branch branch_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.branch
    ADD CONSTRAINT branch_name_key UNIQUE (name);


--
-- Name: branch branch_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.branch
    ADD CONSTRAINT branch_pkey PRIMARY KEY (id);


--
-- Name: company company_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.company
    ADD CONSTRAINT company_name_key UNIQUE (name);


--
-- Name: company company_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.company
    ADD CONSTRAINT company_pkey PRIMARY KEY (id);


--
-- Name: configuration_history configuration_history_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.configuration_history
    ADD CONSTRAINT configuration_history_pkey PRIMARY KEY (id);


--
-- Name: country country_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.country
    ADD CONSTRAINT country_name_key UNIQUE (name);


--
-- Name: country country_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.country
    ADD CONSTRAINT country_pkey PRIMARY KEY (id);


--
-- Name: course_department_mapping course_department_mapping_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.course_department_mapping
    ADD CONSTRAINT course_department_mapping_pkey PRIMARY KEY (id);


--
-- Name: course course_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.course
    ADD CONSTRAINT course_name_key UNIQUE (name);


--
-- Name: course course_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.course
    ADD CONSTRAINT course_pkey PRIMARY KEY (id);


--
-- Name: department department_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.department
    ADD CONSTRAINT department_name_key UNIQUE (name);


--
-- Name: department department_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.department
    ADD CONSTRAINT department_pkey PRIMARY KEY (id);


--
-- Name: hard_skill hard_skill_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.hard_skill
    ADD CONSTRAINT hard_skill_name_key UNIQUE (name);


--
-- Name: hard_skill hard_skill_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.hard_skill
    ADD CONSTRAINT hard_skill_pkey PRIMARY KEY (id);


--
-- Name: institution_branch_mapping institution_branch_mapping_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.institution_branch_mapping
    ADD CONSTRAINT institution_branch_mapping_pkey PRIMARY KEY (id);


--
-- Name: institution_company_mapping institution_company_mapping_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.institution_company_mapping
    ADD CONSTRAINT institution_company_mapping_pkey PRIMARY KEY (id);


--
-- Name: institution_hard_skill_mapping institution_hard_skill_mapping_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.institution_hard_skill_mapping
    ADD CONSTRAINT institution_hard_skill_mapping_pkey PRIMARY KEY (id);


--
-- Name: institution_master institution_master_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.institution_master
    ADD CONSTRAINT institution_master_email_key UNIQUE (email);


--
-- Name: institution_master institution_master_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.institution_master
    ADD CONSTRAINT institution_master_pkey PRIMARY KEY (id);


--
-- Name: institution_soft_skill_mapping institution_soft_skill_mapping_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.institution_soft_skill_mapping
    ADD CONSTRAINT institution_soft_skill_mapping_pkey PRIMARY KEY (id);


--
-- Name: interview_master interview_master_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.interview_master
    ADD CONSTRAINT interview_master_pkey PRIMARY KEY (id);


--
-- Name: question_bank question_bank_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.question_bank
    ADD CONSTRAINT question_bank_pkey PRIMARY KEY (id);


--
-- Name: question question_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.question
    ADD CONSTRAINT question_pkey PRIMARY KEY (id);


--
-- Name: report_point report_point_key_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.report_point
    ADD CONSTRAINT report_point_key_key UNIQUE (key);


--
-- Name: report_point report_point_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.report_point
    ADD CONSTRAINT report_point_pkey PRIMARY KEY (id);


--
-- Name: role role_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.role
    ADD CONSTRAINT role_name_key UNIQUE (name);


--
-- Name: role role_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.role
    ADD CONSTRAINT role_pkey PRIMARY KEY (id);


--
-- Name: soft_skill soft_skill_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.soft_skill
    ADD CONSTRAINT soft_skill_name_key UNIQUE (name);


--
-- Name: soft_skill soft_skill_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.soft_skill
    ADD CONSTRAINT soft_skill_pkey PRIMARY KEY (id);


--
-- Name: user_master user_master_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_master
    ADD CONSTRAINT user_master_email_key UNIQUE (email);


--
-- Name: user_master user_master_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_master
    ADD CONSTRAINT user_master_pkey PRIMARY KEY (id);


--
-- Name: working_role working_role_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.working_role
    ADD CONSTRAINT working_role_name_key UNIQUE (name);


--
-- Name: working_role working_role_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.working_role
    ADD CONSTRAINT working_role_pkey PRIMARY KEY (id);


--
-- Name: ix_institution_master_institution_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_institution_master_institution_name ON public.institution_master USING btree (institution_name);


--
-- Name: assignment assignment_created_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.assignment
    ADD CONSTRAINT assignment_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.user_master(id);


--
-- Name: assignment assignment_updated_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.assignment
    ADD CONSTRAINT assignment_updated_by_fkey FOREIGN KEY (updated_by) REFERENCES public.user_master(id);


--
-- Name: assignment_user_mapping assignment_user_mapping_assignment_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.assignment_user_mapping
    ADD CONSTRAINT assignment_user_mapping_assignment_fkey FOREIGN KEY (assignment) REFERENCES public.assignment(id);


--
-- Name: assignment_user_mapping assignment_user_mapping_user_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.assignment_user_mapping
    ADD CONSTRAINT assignment_user_mapping_user_by_fkey FOREIGN KEY (user_by) REFERENCES public.user_master(id);


--
-- Name: branch_course_mapping branch_course_mapping_branch_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.branch_course_mapping
    ADD CONSTRAINT branch_course_mapping_branch_id_fkey FOREIGN KEY (branch_id) REFERENCES public.branch(id);


--
-- Name: branch_course_mapping branch_course_mapping_course_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.branch_course_mapping
    ADD CONSTRAINT branch_course_mapping_course_id_fkey FOREIGN KEY (course_id) REFERENCES public.course(id);


--
-- Name: course_department_mapping course_department_mapping_course_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.course_department_mapping
    ADD CONSTRAINT course_department_mapping_course_id_fkey FOREIGN KEY (course_id) REFERENCES public.course(id);


--
-- Name: course_department_mapping course_department_mapping_department_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.course_department_mapping
    ADD CONSTRAINT course_department_mapping_department_id_fkey FOREIGN KEY (department_id) REFERENCES public.department(id);


--
-- Name: institution_branch_mapping institution_branch_mapping_branch_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.institution_branch_mapping
    ADD CONSTRAINT institution_branch_mapping_branch_id_fkey FOREIGN KEY (branch_id) REFERENCES public.branch(id);


--
-- Name: institution_branch_mapping institution_branch_mapping_institution_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.institution_branch_mapping
    ADD CONSTRAINT institution_branch_mapping_institution_id_fkey FOREIGN KEY (institution_id) REFERENCES public.institution_master(id);


--
-- Name: institution_company_mapping institution_company_mapping_company_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.institution_company_mapping
    ADD CONSTRAINT institution_company_mapping_company_id_fkey FOREIGN KEY (company_id) REFERENCES public.company(id);


--
-- Name: institution_company_mapping institution_company_mapping_institution_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.institution_company_mapping
    ADD CONSTRAINT institution_company_mapping_institution_id_fkey FOREIGN KEY (institution_id) REFERENCES public.institution_master(id);


--
-- Name: institution_hard_skill_mapping institution_hard_skill_mapping_institution_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.institution_hard_skill_mapping
    ADD CONSTRAINT institution_hard_skill_mapping_institution_id_fkey FOREIGN KEY (institution_id) REFERENCES public.institution_master(id);


--
-- Name: institution_hard_skill_mapping institution_hard_skill_mapping_skill_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.institution_hard_skill_mapping
    ADD CONSTRAINT institution_hard_skill_mapping_skill_id_fkey FOREIGN KEY (skill_id) REFERENCES public.hard_skill(id);


--
-- Name: institution_soft_skill_mapping institution_soft_skill_mapping_institution_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.institution_soft_skill_mapping
    ADD CONSTRAINT institution_soft_skill_mapping_institution_id_fkey FOREIGN KEY (institution_id) REFERENCES public.institution_master(id);


--
-- Name: institution_soft_skill_mapping institution_soft_skill_mapping_skill_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.institution_soft_skill_mapping
    ADD CONSTRAINT institution_soft_skill_mapping_skill_id_fkey FOREIGN KEY (skill_id) REFERENCES public.soft_skill(id);


--
-- Name: question_bank question_bank_created_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.question_bank
    ADD CONSTRAINT question_bank_created_by_fkey FOREIGN KEY (created_by) REFERENCES public.user_master(id);


--
-- Name: question_bank question_bank_updated_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.question_bank
    ADD CONSTRAINT question_bank_updated_by_fkey FOREIGN KEY (updated_by) REFERENCES public.user_master(id);


--
-- Name: user_master user_master_branch_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_master
    ADD CONSTRAINT user_master_branch_id_fkey FOREIGN KEY (branch_id) REFERENCES public.branch(id);


--
-- Name: user_master user_master_department_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_master
    ADD CONSTRAINT user_master_department_id_fkey FOREIGN KEY (department_id) REFERENCES public.department(id);


--
-- Name: user_master user_master_institution_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_master
    ADD CONSTRAINT user_master_institution_id_fkey FOREIGN KEY (institution_id) REFERENCES public.institution_master(id);


--
-- Name: user_master user_master_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_master
    ADD CONSTRAINT user_master_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.role(id);


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE USAGE ON SCHEMA public FROM PUBLIC;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--
