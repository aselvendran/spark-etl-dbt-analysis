{{ config(materialized= 'table', alias= 'approval_analysis') }}

with application_info as (

    select
        user_id
        , case when (applications.application_approved is null and applications.application_rejected is null and application_reviewed is not null) then true else null end as is_pending
        , application_rejected
        , application_reviewed
        , application_approved
    from {{ ref('stg__applications') }}
)
select

       (count(is_pending) + count(application_rejected))::decimal / count(application_reviewed) as not_approved
       , count(application_approved)::decimal/count(application_reviewed) as approved
from application_info
