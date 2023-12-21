{{ config(materialized= 'table', alias= 'stage_funnel') }}

select
     count(application_submitted) as count_of_application_submitted
    , count(application_received) as count_of_application_received
    , count(application_reviewed) as count_of_application_reviewed
    , count(application_rejected) as count_of_application_rejected
    , count(application_approved) as count_of_application_approved
    , count(application_complete) as count_of_application_complete

from {{ ref('stg__applications') }}
where cdc_rank = 1
