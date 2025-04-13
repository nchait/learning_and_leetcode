-- Write your PostgreSQL query statement below
select 
    sum (case when income < 20000 then 1 else 0 end) as "Low Salary",
    sum (case when income >= 20000 and income < 50000 then 1 else 0 end) as "Average Salary",
    sum (case when income > 50000 then 1 else 0 end) as "High Salary"
from accounts;

select 
'Low Salary' as category, 
count (account_id) as accounts_count
from accounts
where income < 20000
UNION ALL 

select 
'Average Salary' as category, 
count (account_id) as accounts_count
sum (case when then 1 else 0 end) as accounts_count
from accounts
where income >= 20000 and income <= 50000 
UNION ALL 
select 
'High Salary' as category, 
count (account_id) as accounts_count
from accounts
where income > 50000 ;


-- perfect
WITH salary_categories AS (
    SELECT 'Low Salary' AS category
    UNION ALL
    SELECT 'Average Salary'
    UNION ALL
    SELECT 'High Salary'
)
SELECT 
    sc.category,
    COUNT(a.account_id) AS accounts_count
FROM salary_categories sc
LEFT JOIN accounts a
    ON CASE
        WHEN sc.category = 'Low Salary' THEN a.income < 20000
        WHEN sc.category = 'Average Salary' THEN a.income BETWEEN 20000 AND 50000
        WHEN sc.category = 'High Salary' THEN a.income > 50000
    END
GROUP BY sc.category
ORDER BY accounts_count DESC