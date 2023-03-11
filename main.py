from fastapi import FastAPI
from fastapi.params import Body
import schema
from database.mysql_database import MySQLConnection
import json

app = FastAPI()

db_conn = MySQLConnection()
cursor =db_conn.connection_object().cursor()
# cursor = db_conn.cursor()
# print(f"Cursor object = {cursor}")

@app.get("/")
def get_data():
    query = "SELECT * FROM fastapi.Products;"
    cursor.execute(query)
    rows = cursor.fetchall()
    print(json.dumps(rows, default=str))
    
    # print(f"db obj value = {rows}")
    # count = 1
    # for each in rows:
    #     id, name, price, is_available, inventory, created_at = each
    #     print(f" Record = {count} and details are \nid ={id} \t name = {name} \t price = {int(price)} \t isavailable = {is_available} \t inventory = {inventory} \t created_at={str(created_at)}\n")
    #     count = count +1
    # print(str(cursor))

    #json.dumps(rows, default=str) -> Here default str converts unsupport data from DB to str like decimal.Decimal and date.Date
    return {"data": json.dumps(rows, default=str)}

@app.post("/")
def post_data(payload:schema.Post):
    return payload