import psycopg2  
from psycopg2 import sql  
  
def create_table(conn, cur):  
    cur.execute('''  
    CREATE TABLE IF NOT EXISTS employees (  
        id SERIAL PRIMARY KEY,  
        name VARCHAR(100),  
        position VARCHAR(50),  
        hire_date DATE  
    )  
    ''')  
    conn.commit()  
    print("Table created successfully")  
  
def insert_employee(conn, cur, name, position, hire_date):  
    insert = sql.SQL('''  
        INSERT INTO employees (name, position, hire_date)  
        VALUES ({}, {}, {})  
    ''').format(sql.Identifier(name), sql.Identifier(position), sql.Identifier(hire_date))  
  
    cur.execute(insert)  
    conn.commit()  
    print("Data inserted successfully")  
  
def main():  
    # Establish a connection to the database  
    conn = psycopg2.connect(  
        dbname="your_database_name",  
        user="your_username",  
        password="your_password",  
        host="localhost"  
    )  
  
    # Create a cursor object  
    cur = conn.cursor()  
  
    create_table(conn, cur)  
    insert_employee(conn, cur, 'John Doe', 'Software Developer', '2022-01-01')  
  
    # Close the cursor and connection  
    cur.close()  
    conn.close()  
  
if __name__ == '__main__':  
    main()  
