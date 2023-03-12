from fastapi import FastAPI,status, HTTPException
from fastapi.params import Body
import schema
from database.mysql_database import MySQLConnection
import json


app = FastAPI()

db = MySQLConnection()


#step 1 create cursor object
#dictionary = True will make the records in dictionary format which will have column name and data
db_con = db.connection_object()
cursor =db_con.cursor(dictionary=True)
# cursor = db_conn.cursor()
# print(f"Cursor object = {cursor}")

@app.get("/", status_code=status.HTTP_200_OK)
def get_data():
    query = "SELECT * FROM fastapi.Products;"
    #step2 execute query
    cursor.execute(query)
    #step3 fetch details
    rows = cursor.fetchall()

    #json.dumps(rows, default=str) 
    # -> Here default str converts unsupport data from DB to str like 
    # decimal.Decimal and date.Date
    # data = (json.dumps(rows, default=str))
    #Here json loads removes the extra / slashes in string format
    # formatted_data = json.loads(data)
    # print(formatted_data)
    if not rows:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Currently no records available in the application.")
    return {"data": rows}

@app.post("/", status_code=status.HTTP_201_CREATED)
def post_data(payload:schema.Product):
    cursor.execute("INSERT INTO fastapi.Products(name, price, is_available, inventory) VALUES(%s, %s, %s, %s)",
        (payload.name, payload.price, payload.is_available, payload.inventory))
    product_id = cursor.lastrowid
    db_con.commit()
    cursor.execute(f"SELECT * FROM fastapi.Products WHERE id = {product_id};")
    return cursor.fetchone()


@app.get("/{id}", status_code=status.HTTP_200_OK)
def get_specific_data(id:int):
    query = f"SELECT * FROM fastapi.Products WHERE id = {id};"
    #step2 execute query
    cursor.execute(query)
    #step3 fetch details
    data = cursor.fetchone()
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id = {id} not found.")
    return {"data": data}

@app.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_data(id:int):
    cursor.execute(f"SELECT * FROM fastapi.Products WHERE id = {id};")
    data= cursor.fetchone()
    if data == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id = {id} not present in record.")
    query = f"DELETE FROM fastapi.Products WHERE id = {id};"
    #step2 execute query
    cursor.execute(query)
    db_con.commit()
    #return statement will not be executed when we return  status_code=status.HTTP_204_NO_CONTENT
    # delete  status_code=status.HTTP_204_NO_CONTENT from the status to execute below return statement  
    return {"data": "Product with id = {id} id deleted successfully."}


@app.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_data(payload:schema.Product, id:int):
    cursor.execute(f"SELECT * FROM fastapi.Products WHERE id = {id};")
    data= cursor.fetchone()
    if data == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id = {id} not present in record.")

    print(f"payload = {payload}")
    cursor.execute("UPDATE fastapi.Products SET name=%s, price=%s, is_available=%s, inventory=%s WHERE id=%s;", (payload.name, payload.price, payload.is_available, payload.inventory, id))
    db_con.commit()
    
    cursor.execute(f"SELECT * FROM fastapi.Products WHERE id = {id};")
    data= cursor.fetchone() 
    return {"data": data}