select salary as SecondHighestSalary
from (
select distinct salary from Employee
order by salary desc 
limit 1 offset 1
) as sub
union all
select null as SecondHighestSalary
limit 1;

-- Write your PostgreSQL query statement below
with sorted_salaries as (
    select distinct salary
    from Employee as e
    order by e.salary desc
    offset 1
), second_salary as (
    select t.salary as SecondHighestSalary
    from sorted_salaries as t
    order by t.salary desc
    limit 1
), salary_count as (
    select count(*) as count
    from sorted_salaries
)
select case when count < 1 then null
            else (select * from second_salary)
            end
from salary_count;

