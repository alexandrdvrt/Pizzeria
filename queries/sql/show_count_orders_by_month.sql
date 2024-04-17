SELECT
    YEAR(DATE(order_time)) as year,
    MONTH(DATE(order_time)) as month,
    courier_id,
    courier_data,
    hire_date,
    MAX(delivery_time) as max,
    COUNT(courier_id) as count
FROM
    orders
    JOIN couriers USING(courier_id)
WHERE
    YEAR(DATE(order_time)) = YEAR('$date-01')
    AND MONTH(DATE(order_time)) = MONTH('$date-01')
GROUP BY
    YEAR(DATE(order_time)),
    MONTH(DATE(order_time)),
    courier_id