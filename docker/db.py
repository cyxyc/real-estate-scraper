from fastapi import FastAPI, HTTPException
import psycopg2
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    value1: str
    value2: str

@app.post("/insert")
async def insert_item(item: Item):
    try:
    # Connect to your postgres DB
        connection = psycopg2.connect(
        dbname="db1",
        user="postgres",
        password="postgres",
        host="localhost",  # or the name of the postgres service if used in docker-compose
        port="5432"  # default postgres port
    )

        # Open a cursor to perform database operations
        cursor = connection.cursor()

        # Execute a query
        cursor.execute("INSERT INTO table1 (col1, col2) VALUES (%s, %s)", (item.value1, item.value2))

        # Commit the transaction
        connection.commit()

        # Close the cursor and connection
        cursor.close()
        connection.close()

        return {"message": "Values inserted successfully"}

    except psycopg2.Error as e:
        raise HTTPException(status_code=400, detail=str(e))

# http://localhost:8000/status
@app.get("/status")
async def status():
    return ("Service plsSSS runyng!")