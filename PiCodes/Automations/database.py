import mysql.connector

host = "127.0.0.1"  # Change to your MySQL host
user = "root"  # Change to your MySQL username
password = "root"  # Change to your MySQL password
database = "HomeIotSystem"  # Change to your database name

def get_automations():
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    if connection is None:
        return []
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM automations ORDER BY id DESC")
        automations = cursor.fetchall()
        return automations
    except mysql.connector.Error as e:
        print(f"Error retrieving automations: {e}")
        return []
    finally:
        cursor.close()
        connection.close()

