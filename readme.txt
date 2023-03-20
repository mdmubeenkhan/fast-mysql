
Steps to run the Application:
---------------------------------
1. Configure the mysql database and make sure its up and running
2. Enter the required details in .env field
3. Create virtual environment
4. Install all required libraries using command = pip3 install -r requirements.txt
5. run command = uvicorn main:app --reload


Below end point will return access token when we pass 
1. username = email@address
2. password = user-password
http://localhost:8000/auth

Then pass the access token in subsequent request as Bearer token. 

Verify access token expiration time and adjust according to your project need.



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