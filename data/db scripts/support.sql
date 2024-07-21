SELECT * FROM pg_locks WHERE relation = 'institution_master'::regclass;

-- finds any running query for that table
SELECT pid, now() - pg_stat_activity.query_start AS duration, query, state
FROM pg_stat_activity
WHERE (now() - pg_stat_activity.query_start) > interval '5 minutes'
  AND state != 'idle'
  AND query LIKE '%institution_master%';

-- deletes running query for that table 
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE pid = 1813146;  -- Replace [process ID] with the actual process ID
