{{ config(materialized= 'table', alias= 'metadata') }}


SELECT distinct
    user_id
    , "commit-timestamp"::timestamp as commit_timestamp
    , operation
    , "partition-key-type" as partition_key_type
    , "record-type" as record_type
    , "schema-name" as schema_name
    , "stream-position"::bigint as stream_position
    , "table-name" as table_name
    , "timestamp"::timestamp as metadata_timestamp
    , "transaction-id" as transaction_id
    , "transaction-record-id" as transaction_record_id
FROM {{ source('public', 'metadata') }}
