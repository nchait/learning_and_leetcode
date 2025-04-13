-- Write your PostgreSQL query statement below
WITH ranked as 
(
    SELECT
    DENSE_RANK() OVER (PARTITION BY departmentId ORDER BY SALARY DESC) as rnk,
    salary AS Salary,
    name AS Employee,
    departmentId
    FROM Employee
)
SELECT 
    Department.name as Department, ranked.Employee, ranked.Salary
FROM 
    ranked
INNER JOIN Department
    ON Department.id = ranked.departmentId
where rnk <=3
ORDER BY Department.name ASC, ranked.Salary DESC;


-- Write your PostgreSQL query statement below
WITH ranked as 
(
    SELECT
    DENSE_RANK() OVER (PARTITION BY E.departmentId ORDER BY E.salary DESC) as rnk,
    E.salary AS Salary,
    E.name AS Employee,
    D.name AS Department
    FROM Employee as E
    JOIN Department as D
        ON D.id = E.departmentId
)
SELECT 
    Department, Employee, Salary
FROM 
    ranked
where rnk <=3;



-- Department, 
-- Employee, 
-- Salary