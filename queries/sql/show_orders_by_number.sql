SELECT
    order_time,
    phone_number,
    customer_lastname,
    dish_name,
    dish_price
FROM
    orders
    JOIN customers USING(customer_id)
    JOIN dishes USING(dish_code)
WHERE
    phone_number = '$phone_number'