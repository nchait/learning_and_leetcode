-- Coding 


-- t.recordDate - INTERVAL '1 DAY' = y.recordDate
--     COUNT(CASE WHEN rsp_ind = 0 then 1 ELSE NULL END) as "New",

with first_orders as (
    select
        customer_id,
        order_date = customer_pref_delivery_date as immed,
        ROW_NUMBER()
            over (
                partition by customer_id
                order by order_date asc
            )
        as rank
    from delivery
)

select
    ROUND(
        AVG(case when immed and rank = 1 then 1.0 else 0 end) * 100, 2
    ) as immediate_percentage
from first_orders
where rank = 1;

select
    city,
    date,
    precipitation,
    SUM(precipitation) over (
        partition by city
        order by date
        rows 2 preceding
    ) as running_total_3d_city
from weather
order by city, date;

select person_name
from (
    select
        person_name,
        SUM(weight)
            over (
                order by turn asc
            )
        as cumulative_weight
    from queue
)
where cumulative_weight <= 1000
order by cumulative_weight desc
limit 2
