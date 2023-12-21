{%- macro comparison_case_clause(compare_from, compare_to) -%}

case when {{ compare_from }} is null then (max_application_received - {{ compare_to }} ) < avg_time_of_pipeline else {{ compare_from }} is not null end

{%- endmacro -%}
