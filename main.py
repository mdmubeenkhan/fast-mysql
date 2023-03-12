from fastapi import FastAPI
from fastapi.params import Body
import schema
from database.mysql_database import MySQLConnection
import json

app = FastAPI()

db_conn = MySQLConnection()


#step 1 create cursor object
#dictionary = True will make the records in dictionary format which will have column name and data
cursor =db_conn.connection_object().cursor(dictionary=True)
# cursor = db_conn.cursor()
# print(f"Cursor object = {cursor}")

@app.get("/")
def get_data():
    query = "SELECT * FROM fastapi.Products;"
    #step2 execute query
    cursor.execute(query)
    #step3 fetch details
    rows = cursor.fetchall()

    #json.dumps(rows, default=str) 
    # -> Here default str converts unsupport data from DB to str like 
    # decimal.Decimal and date.Date
    data = (json.dumps(rows, default=str))
    #Here json loads removes the extra / slashes in string format
    formatted_data = json.loads(data)
    print(formatted_data)
    return {"data": formatted_data}

@app.post("/")
def post_data(payload:schema.Post):
    return payload