{{ config(materialized= 'table', alias= 'dropoff_analysis') }}

with application_agg as
    (
        select
            max(application_received) max_application_received
            , avg(application_submitted-application_received) avg_time_of_pipeline
            , count(application_approved) as application_approved_ct
            , count(application_complete) as application_complete_ct
            , count(application_received) as application_received_ct
            , count(application_rejected) as application_rejected_ct
            , count(application_reviewed) as application_reviewed_ct
            , count(application_submitted) as application_submitted_ct
        from {{ ref('stg__applications') }}
    )
, drop_off_breakout as (
    select
        {{ comparison_case_clause('application_submitted', 'application_received') }} as dropoff_submmision
        , {{ comparison_case_clause('application_complete', 'application_submitted') }} as dropoff_complete
        , {{ comparison_case_clause('application_reviewed', 'application_complete') }} as dropoff_review
        , {{ comparison_case_clause('application_approved', 'application_reviewed') }} as dropoff_approved
        , {{ comparison_case_clause('application_rejected', 'application_reviewed') }} as dropoff_rejected

    from {{ ref('stg__applications') }}
    cross join application_agg
        where application_received is not null
)

select
    sum(case when dropoff_submmision is False then 1 else 0 end)::decimal/ application_received_ct as dropoff_submmision_pt
    , sum(case when dropoff_complete is False then 1 else 0 end)::decimal/ application_submitted_ct as dropoff_complete_pt
    , sum(case when dropoff_review is False then 1 else 0 end)::decimal/ application_complete_ct as dropoff_review_pt
    , sum(case when dropoff_approved is False then 1 else 0 end)::decimal/ application_reviewed_ct as dropoff_approved_pt
    , sum(case when dropoff_rejected is False then 1 else 0 end)::decimal/ application_reviewed_ct as dropoff_rejected_pt
from drop_off_breakout
cross join application_agg
group by application_received_ct, application_submitted_ct, application_complete_ct, application_reviewed_ct, application_reviewed_ct
