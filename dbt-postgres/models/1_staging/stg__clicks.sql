{{ config(materialized= 'table', alias= 'clicks') }}


SELECT
    user_id
    , click_screen
    , click_ts::timestamp as click_ts
    , click_verified
    , click_xy
FROM {{ source('public', 'clicks') }} clicks
inner join {{ source('public', 'metadata') }} metadata
using(user_id)
