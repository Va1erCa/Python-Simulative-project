-- SQL query for pySimulative1 app (This text are already integrated into a python script)
with rep_day as (
	select 
		user_id,
		created_at::date as created_at,
		is_correct,
		attempt_type 
	from lms_activities
	where created_at::date = '2024-11-02'  
)
select
	1 as rep_param_index,
	'total_unique_users' as rep_param_name,
	count(distinct user_id) as rep_param_value 
from rep_day
union
select 
	2 as rep_param_index,
	'total_runs' as rep_param_name,
	count(*) as rep_param_value
from rep_day 
where attempt_type = 'run'
union
select 
	3 as rep_param_index,
	'total_submits' as rep_param_name,
	count(*) as rep_param_value
from rep_day 
where attempt_type = 'submit'
union
select 
	4 as rep_param_index,
	'total_success_submits' as rep_param_name,
	count(*) as rep_param_value
from rep_day 
where attempt_type = 'submit' and is_correct
order by rep_param_index


