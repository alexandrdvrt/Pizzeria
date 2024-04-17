SELECT
    dish_name as name,
    dish_measure as measure,
    SUM(pr_amount) as amount,
    SUM(pr_amount * dish_price) as income,
    rep_year as year,
    rep_month as month
FROM
    reports
    JOIN dishes ON(dish_code = prod_id)
    JOIN sales ON(pr_id = prod_id)
WHERE
    rep_year = YEAR('$date-01')
    AND rep_month = MONTH('$date-01')
GROUP BY
    dish_name, dish_measure, rep_year, rep_month