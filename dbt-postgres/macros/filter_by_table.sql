{%- macro filter_by_table(filter_clause, table_name) -%}

inner join {{ ref('metadata') }} metadata
    on {{ filter_clause }} = metadata.user_id
where table_name = '{{ table_name  }}'

{%- endmacro -%}