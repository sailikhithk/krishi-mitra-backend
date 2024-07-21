ALTER TABLE public.company ADD designations json NULL;

ALTER TABLE public.institution_master ADD interview_questions_mode varchar NULL;
ALTER TABLE public.institution_master ADD initial_configuration boolean NULL;
ALTER TABLE public.institution_master ADD configuration_version varchar NULL;
ALTER TABLE public.institution_master ADD latest_configuration_date timestamp NULL;

ALTER TABLE public.user_master ADD negative_emotions varchar NULL;

ALTER TABLE public.user_master ALTER COLUMN certifed_hard_skills TYPE varchar USING certifed_hard_skills::varchar;
ALTER TABLE public.user_master ALTER COLUMN certifed_soft_skills TYPE varchar USING certifed_soft_skills::varchar;
ALTER TABLE public.user_master ADD uncertified_hard_skills varchar NULL;
ALTER TABLE public.user_master ADD uncertified_soft_skills varchar NULL;

ALTER TABLE public.user_master RENAME COLUMN certifed_hard_skills TO certified_hard_skills;
ALTER TABLE public.user_master RENAME COLUMN certifed_soft_skills TO certified_soft_skills;

ALTER TABLE public.configuration_history ADD status varchar NULL;
ALTER TABLE public.configuration_history ADD error varchar NULL;

ALTER TABLE public.configuration_history DROP CONSTRAINT configuration_history_updated_by_fkey;
ALTER TABLE public.configuration_history DROP CONSTRAINT configuration_history_created_by_fkey;
ALTER TABLE public.institution_company_mapping ADD role_ids varchar NULL;
