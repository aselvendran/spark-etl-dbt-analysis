{{ config(materialized= 'table', alias= 'users') }}


SELECT
    user_id
    , id
    , first_name
    , last_name
    , phone_verified
    , profile_finished::timestamp as profile_finished
    , spam_opt_in
    , text_opt_in
    , user_flag::bool
    , user_onboarded::timestamp as user_onboarded
    , username
FROM {{ source('public', 'users') }} users
inner join {{ source('public', 'metadata') }} metadata
using(user_id)
