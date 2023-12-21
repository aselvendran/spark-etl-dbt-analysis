{{ config(materialized= 'table', alias= 'applications') }}


SELECT
    user_id
    , application_approved::timestamp as application_approved
    , application_complete::timestamp as application_complete
    , application_received::timestamp as application_received
    , application_rejected::timestamp as application_rejected
    , application_reviewed::timestamp as application_reviewed
    , application_submitted::timestamp as application_submitted
    , dense_rank() OVER (PARTITION BY user_id ORDER BY metadata_timestamp DESC ) as cdc_rank
FROM {{ source('public', 'applications') }} application
inner join {{ ref('stg__metadata') }} metadata
using(user_id)
where
    (length(application_approved) is null or length(application_approved) = 19)
    and (length(application_complete) is null or length(application_complete) = 19)
    and (length(application_received) is null or length(application_received) = 19)
    and (length(application_rejected) is null or length(application_rejected) = 19)
    and (length(application_reviewed) is null or length(application_reviewed) = 19)
    and (length(application_submitted) is null or length(application_submitted) = 19)
    and operation != 'delete'
