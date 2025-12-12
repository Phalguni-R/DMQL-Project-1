{{ config(materialized='table') }}

SELECT
    label_id,
    label_name
FROM {{ source('public', 'Labels') }}