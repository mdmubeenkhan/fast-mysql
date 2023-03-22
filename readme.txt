
Steps to run the Application:
---------------------------------
1. Configure the mysql database and make sure its up and running
2. Enter the required details in .env field
3. Create virtual environment
4. Install all required libraries using command = pip3 install -r requirements.txt
5. run command = uvicorn main:app --reload





DB Notes:
============
SHOW COLUMNS FROM fastapi.Users;
SHOW COLUMNS FROM fastapi.Products;


#On purchase table made both columns as PRIMARY KEY, which is called COMPOSIT PRIMARY KEY to prevent user from buying same item again and again
#User can buy items only once. So combination of user_id and product_id will always UNIQUE.

SHOW COLUMNS FROM fastapi.Purchase;
CREATE TABLE fastapi.Purchase(user_id int NOT NULL, product_id int NOT NULL, PRIMARY KEY (user_id, product_id));
ALTER TABLE fastapi.Purchase ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES fastapi.Users(id) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE fastapi.Purchase ADD CONSTRAINT fk_product_id FOREIGN KEY (product_id) REFERENCES fastapi.Products(id) ON DELETE CASCADE ON UPDATE CASCADE;

SELECT * FROM fastapi.Users;
SELECT * from fastapi.Products;
SELECT * From fastapi.Purchase;
INSERT INTO fastapi.Purchase(user_id, product_id)VALUES(2, 5);


data = db.query(models.Products, func.count(models.Products.id).label("NoOfProductAddedByUser")).join(models.Users, models.Products.user_id==models.Users.id, isouter=True).group_by(models.Users.name).all()
    

Join
------
SELECT Users.name, Users.email, Products.name, Products.price, Products.inventory FROM fastapi.Users JOIN fastapi.Products ON Users.id=Products.user_id;


count
-------
SELECT Products.user_id, Users.name, COUNT(Products.user_id) from fastapi.Products JOIN fastapi.Users ON Users.id=Products.user_id GROUP BY Products.user_id;
SELECT Users.id as USER_ID, Users.name, COUNT(Products.user_id) from fastapi.Products JOIN fastapi.Users ON Users.id=Products.user_id GROUP BY Products.user_id;


