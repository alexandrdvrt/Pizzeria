SELECT
    role
FROM
    external_users
WHERE
    login = '$login'
    AND password = '$password'