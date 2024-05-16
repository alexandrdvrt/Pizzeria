![image](https://github.com/alexandrdvrt/Pizzeria/assets/94928103/65f3feb8-2d94-4830-a715-5a5a75c21bcd)
Procedure for reports:  
CREATE DEFINER=root`@`localhost PROCEDURE fillReports(IN rep_date DATE)  
BEGIN  
DECLARE r_year, r_month, prd_id INTEGER;  
DECLARE done INTEGER DEFAULT 0;  
DECLARE exit_flag INTEGER DEFAULT 0;  
DECLARE C1 CURSOR FOR SELECT pr_id  
FROM dishes JOIN sales ON(pr_id = dish_code)  
WHERE YEAR(s_date) = r_year AND MONTH(s_date) = r_month;  
DECLARE exit HANDLER for SQLSTATE '02000' SET done = 1;  
  
SET r_year = YEAR(rep_date);  
SET r_month = MONTH(rep_date);  
SELECT COUNT(*) INTO exit_flag FROM reports WHERE  
rep_year = r_year AND rep_month = r_month;  
  
IF exit_flag = 0 THEN  
OPEN C1;  
WHILE done = 0 DO  
FETCH C1 INTO prd_id;  
INSERT INTO reports(rep_year, rep_month, prod_id) VALUES (r_year, r_month, prd_id);  
END WHILE;  
CLOSE C1;  
ELSE  
SET @result_message = "Отчет уже существует";  
END IF;  
END  
