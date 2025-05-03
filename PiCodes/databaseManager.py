from datetime import datetime
from datetime import timedelta

import mysql.connector

host = "127.0.0.1"  # Change to your MySQL host
user = "root"  # Change to your MySQL username
password = "root"  # Change to your MySQL password
database = "HomeIotSystem"  # Change to your database name


def getTemp(time):
    db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="root",
    database="HomeIotSystem"
    )   
    cursor = db.cursor(dictionary=True)
    if(time == "hour"):
        cursor.execute("SELECT DATE_FORMAT(CONVERT_TZ(timestamp, '+00:00', '+08:00'), '%h:%i:%s %p') as timestamp, temperature FROM curtain WHERE timestamp >= NOW() - INTERVAL 1 HOUR ORDER BY id ASC")
    elif(time == "today"):
        cursor.execute("SELECT DATE_FORMAT(CONVERT_TZ(timestamp, '+00:00', '+08:00'), '%h:%i:%s %p') as timestamp, temperature FROM curtain WHERE DATE(timestamp) = DATE(NOW()) ORDER BY id ASC")
    elif(time == "20min"):
        cursor.execute("SELECT DATE_FORMAT(CONVERT_TZ(timestamp, '+00:00', '+08:00'), '%h:%i:%s %p') as timestamp, temperature FROM curtain WHERE timestamp >= NOW() - INTERVAL 20 MINUTE ORDER BY id ASC")
    data = cursor.fetchall()
    cursor.close()
    # Process data to fill gaps (assuming 10s intervals)
    processed_data = []
    if data:
        for i in range(len(data)):
            processed_data.append(data[i])
            
            # If not the last entry, check for gap with next entry
            if i < len(data) - 1:
                current_time = data[i]['timestamp']
                next_time = data[i+1]['timestamp']
                
                # Convert time strings to datetime objects for comparison
                current_dt = datetime.strptime(current_time, '%I:%M:%S %p')
                next_dt = datetime.strptime(next_time, '%I:%M:%S %p')
                
                # Calculate difference in seconds
                time_diff = (next_dt - current_dt).total_seconds()
                
                # If gap is more than 20 seconds (double the normal interval)
                if time_diff > 20:
                    # Calculate how many 10s intervals to insert
                    intervals = int(time_diff // 10) - 1
                    for j in range(1, intervals + 1):
                        # Create a new timestamp by adding j*10 seconds
                        gap_dt = current_dt + timedelta(seconds=j*10)
                        gap_time = gap_dt.strftime('%I:%M:%S %p')
                        
                        # Insert placeholder with 0 temperature
                        processed_data.append({'timestamp': gap_time, 'null': 0})
        
        # Sort the processed data by timestamp
        processed_data.sort(key=lambda x: datetime.strptime(x['timestamp'], '%I:%M:%S %p'))
        
    # Add padding to the end until current time
    if processed_data:
        last_entry = processed_data[-1]
        last_time = datetime.strptime(last_entry['timestamp'], '%I:%M:%S %p')
        
        # Get current time in the same format (without date)
        now = datetime.now()
        current_time = datetime(1900, 1, 1, now.hour, now.minute, now.second)
        
        # If the last entry is before current time, add padding
        if last_time < current_time:
            time_diff = (current_time - last_time).total_seconds()
            intervals = int(time_diff // 15)
            
            for j in range(1, intervals + 1):
                pad_time = last_time + timedelta(seconds=j*10)
                pad_time_str = pad_time.strftime('%I:%M:%S %p')
                processed_data.append({'timestamp': pad_time_str, 'null': 0})
    
    data = processed_data
    return data

def getHumidity(time):
    db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="root",
    database="HomeIotSystem"
    )   
    cursor = db.cursor(dictionary=True)
    if(time == "hour"):
        cursor.execute("SELECT DATE_FORMAT(CONVERT_TZ(timestamp, '+00:00', '+08:00'), '%h:%i:%s %p') as timestamp, humidity FROM curtain WHERE timestamp >= NOW() - INTERVAL 1 HOUR ORDER BY id ASC")
    elif(time == "today"):
        cursor.execute("SELECT DATE_FORMAT(CONVERT_TZ(timestamp, '+00:00', '+08:00'), '%h:%i:%s %p') as timestamp, humidity FROM curtain WHERE DATE(timestamp) = DATE(NOW()) ORDER BY id ASC")
    elif(time == "20min"):
        cursor.execute("SELECT DATE_FORMAT(CONVERT_TZ(timestamp, '+00:00', '+08:00'), '%h:%i:%s %p') as timestamp, humidity FROM curtain WHERE timestamp >= NOW() - INTERVAL 20 MINUTE ORDER BY id ASC")
    data = cursor.fetchall()
    cursor.close()
    # Process data to fill gaps (assuming 10s intervals)
    processed_data = []
    if data:
        for i in range(len(data)):
            processed_data.append(data[i])
            
            # If not the last entry, check for gap with next entry
            if i < len(data) - 1:
                current_time = data[i]['timestamp']
                next_time = data[i+1]['timestamp']
                
                # Convert time strings to datetime objects for comparison
                current_dt = datetime.strptime(current_time, '%I:%M:%S %p')
                next_dt = datetime.strptime(next_time, '%I:%M:%S %p')
                
                # Calculate difference in seconds
                time_diff = (next_dt - current_dt).total_seconds()
                
                # If gap is more than 20 seconds (double the normal interval)
                if time_diff > 20:
                    # Calculate how many 10s intervals to insert
                    intervals = int(time_diff // 10) - 1
                    for j in range(1, intervals + 1):
                        # Create a new timestamp by adding j*10 seconds
                        gap_dt = current_dt + timedelta(seconds=j*10)
                        gap_time = gap_dt.strftime('%I:%M:%S %p')
                        
                        # Insert placeholder with 0 temperature
                        processed_data.append({'timestamp': gap_time, 'null': 0})
        
        # Sort the processed data by timestamp
        processed_data.sort(key=lambda x: datetime.strptime(x['timestamp'], '%I:%M:%S %p'))
        
    # Add padding to the end until current time
    if processed_data:
        last_entry = processed_data[-1]
        last_time = datetime.strptime(last_entry['timestamp'], '%I:%M:%S %p')
        
        # Get current time in the same format (without date)
        now = datetime.now()
        current_time = datetime(1900, 1, 1, now.hour, now.minute, now.second)
        
        # If the last entry is before current time, add padding
        if last_time < current_time:
            time_diff = (current_time - last_time).total_seconds()
            intervals = int(time_diff // 15)
            
            for j in range(1, intervals + 1):
                pad_time = last_time + timedelta(seconds=j*10)
                pad_time_str = pad_time.strftime('%I:%M:%S %p')
                processed_data.append({'timestamp': pad_time_str, 'null': 0})
    
    data = processed_data
    return data

def getCurtain(time):
    db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="root",
    database="HomeIotSystem"
    )
   
    cursor = db.cursor(dictionary=True)
    if(time == "hour"):
        cursor.execute("SELECT DATE_FORMAT(CONVERT_TZ(timestamp, '+00:00', '+08:00'), '%h:%i:%s %p') as timestamp, curtain_pos FROM curtain WHERE timestamp >= NOW() - INTERVAL 1 HOUR ORDER BY id ASC")
    elif(time == "today"):
        cursor.execute("SELECT DATE_FORMAT(CONVERT_TZ(timestamp, '+00:00', '+08:00'), '%h:%i:%s %p') as timestamp, curtain_pos FROM curtain WHERE DATE(timestamp) = DATE(NOW()) ORDER BY id ASC")
    elif(time == "20min"):
        cursor.execute("SELECT DATE_FORMAT(CONVERT_TZ(timestamp, '+00:00', '+08:00'), '%h:%i:%s %p') as timestamp, curtain_pos FROM curtain WHERE timestamp >= NOW() - INTERVAL 20 MINUTE ORDER BY id ASC")
    data = cursor.fetchall()
    cursor.close()
    # Process data to fill gaps (assuming 10s intervals)
    processed_data = []
    if data:
        for i in range(len(data)):
            processed_data.append(data[i])
            
            # If not the last entry, check for gap with next entry
            if i < len(data) - 1:
                current_time = data[i]['timestamp']
                next_time = data[i+1]['timestamp']
                
                # Convert time strings to datetime objects for comparison
                current_dt = datetime.strptime(current_time, '%I:%M:%S %p')
                next_dt = datetime.strptime(next_time, '%I:%M:%S %p')
                
                # Calculate difference in seconds
                time_diff = (next_dt - current_dt).total_seconds()
                
                # If gap is more than 20 seconds (double the normal interval)
                if time_diff > 20:
                    # Calculate how many 10s intervals to insert
                    intervals = int(time_diff // 10) - 1
                    for j in range(1, intervals + 1):
                        # Create a new timestamp by adding j*10 seconds
                        gap_dt = current_dt + timedelta(seconds=j*10)
                        gap_time = gap_dt.strftime('%I:%M:%S %p')
                        
                        # Insert placeholder with 0 temperature
                        processed_data.append({'timestamp': gap_time, 'null': 0})
        
        # Sort the processed data by timestamp
        processed_data.sort(key=lambda x: datetime.strptime(x['timestamp'], '%I:%M:%S %p'))
        
    # Add padding to the end until current time
    if processed_data:
        last_entry = processed_data[-1]
        last_time = datetime.strptime(last_entry['timestamp'], '%I:%M:%S %p')
        
        # Get current time in the same format (without date)
        now = datetime.now()
        current_time = datetime(1900, 1, 1, now.hour, now.minute, now.second)
        
        # If the last entry is before current time, add padding
        if last_time < current_time:
            time_diff = (current_time - last_time).total_seconds()
            intervals = int(time_diff // 15)
            
            for j in range(1, intervals + 1):
                pad_time = last_time + timedelta(seconds=j*10)
                pad_time_str = pad_time.strftime('%I:%M:%S %p')
                processed_data.append({'timestamp': pad_time_str, 'null': 0})
    
    data = processed_data
    return data

def getLight(time):
    db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="root",
    database="HomeIotSystem"
    )
   
    cursor = db.cursor(dictionary=True)
    if(time == "hour"):
        cursor.execute("SELECT DATE_FORMAT(CONVERT_TZ(timestamp, '+00:00', '+08:00'), '%h:%i:%s %p') as timestamp, light_in as inside_light, light_out as outside_light FROM curtain WHERE timestamp >= NOW() - INTERVAL 1 HOUR ORDER BY id ASC")
    elif(time == "today"):
        cursor.execute("SELECT DATE_FORMAT(CONVERT_TZ(timestamp, '+00:00', '+08:00'), '%h:%i:%s %p') as timestamp, light_in as inside_light, light_out as outside_light FROM curtain WHERE DATE(timestamp) = DATE(NOW()) ORDER BY id ASC")
    elif(time == "20min"):
        cursor.execute("SELECT DATE_FORMAT(CONVERT_TZ(timestamp, '+00:00', '+08:00'), '%h:%i:%s %p') as timestamp, light_in as inside_light, light_out as outside_light FROM curtain WHERE timestamp >= NOW() - INTERVAL 20 MINUTE ORDER BY id ASC")
    data = cursor.fetchall()
    cursor.close()
    # Process data to fill gaps (assuming 10s intervals)
    processed_data = []
    if data:
        for i in range(len(data)):
            processed_data.append(data[i])
            
            # If not the last entry, check for gap with next entry
            if i < len(data) - 1:
                current_time = data[i]['timestamp']
                next_time = data[i+1]['timestamp']
                
                # Convert time strings to datetime objects for comparison
                current_dt = datetime.strptime(current_time, '%I:%M:%S %p')
                next_dt = datetime.strptime(next_time, '%I:%M:%S %p')
                
                # Calculate difference in seconds
                time_diff = (next_dt - current_dt).total_seconds()
                
                # If gap is more than 20 seconds (double the normal interval)
                if time_diff > 20:
                    # Calculate how many 10s intervals to insert
                    intervals = int(time_diff // 10) - 1
                    for j in range(1, intervals + 1):
                        # Create a new timestamp by adding j*10 seconds
                        gap_dt = current_dt + timedelta(seconds=j*10)
                        gap_time = gap_dt.strftime('%I:%M:%S %p')
                        
                        # Insert placeholder with null values for the lights
                        processed_data.append({'timestamp': gap_time, 'inside_light': None, 'outside_light': None})
        
        # Sort the processed data by timestamp
        processed_data.sort(key=lambda x: datetime.strptime(x['timestamp'], '%I:%M:%S %p'))
        
    # Add padding to the end until current time
    if processed_data:
        last_entry = processed_data[-1]
        last_time = datetime.strptime(last_entry['timestamp'], '%I:%M:%S %p')
        
        # Get current time in the same format (without date)
        now = datetime.now()
        current_time = datetime(1900, 1, 1, now.hour, now.minute, now.second)
        
        # If the last entry is before current time, add padding
        if last_time < current_time:
            time_diff = (current_time - last_time).total_seconds()
            intervals = int(time_diff // 15)
            
            for j in range(1, intervals + 1):
                pad_time = last_time + timedelta(seconds=j*10)
                pad_time_str = pad_time.strftime('%I:%M:%S %p')
                processed_data.append({'timestamp': pad_time_str, 'inside_light': None, 'outside_light': None})
    
    data = processed_data
    return data

def create_connection():
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        return connection
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def create_database():
    connection = create_connection()
    if connection is None:
        return
    
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS "+database)
        print("Database 'HomeIotSystem' checked/created successfully.")
    except mysql.connector.Error as e:
        print(f"Error creating database: {e}")
    finally:
        cursor.close()
        connection.close()

def create_table():
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    
    try:
        cursor = connection.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS curtain (
            id INT AUTO_INCREMENT PRIMARY KEY,
            temperature FLOAT,
            humidity FLOAT,
            light_in INT,
            light_out INT,
            curtain_pos INT,
            human_presence BOOLEAN,
            
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        print("Table 'curtain' checked/created successfully.")
    except mysql.connector.Error as e:
        print(f"Error creating table: {e}")
    finally:
        cursor.close()
        connection.close()

def insert_curtain_data(data):
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    if connection is None:
        return
    
    try:
        cursor = connection.cursor()
        sql = """
        INSERT INTO curtain (temperature, humidity, light_in, light_out, curtain_pos, human_presence)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (data.temperature, data.humidity, data.light_in, data.light_out, data.curtain_pos, data.human_presence)
        
        cursor.execute(sql, values)
        connection.commit()
        print("Data inserted successfully into 'curtain' table.")
    except mysql.connector.Error as e:
        print(f"Error inserting data: {e}")
    finally:
        cursor.close()
        connection.close()

def create_automations_table():
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    
    try:
        cursor = connection.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS automations (
            id INT AUTO_INCREMENT PRIMARY KEY,
            trigger_type VARCHAR(50) NOT NULL,
            trigger_condition VARCHAR(10),
            trigger_value VARCHAR(50) NOT NULL,
            action_type VARCHAR(50) NOT NULL,
            action_value VARCHAR(50) NOT NULL,
            priority INT DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        print("Table 'automations' checked/created successfully.")
    except mysql.connector.Error as e:
        print(f"Error creating automations table: {e}")
    finally:
        cursor.close()
        connection.close()

def save_automation(trigger_type, trigger_condition, trigger_value, action_type, action_value, priority=0):
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    if connection is None:
        return {"status": "error", "message": "Database connection failed"}
    
    try:
        cursor = connection.cursor()
        sql = """
        INSERT INTO automations (trigger_type, trigger_condition, trigger_value, action_type, action_value, priority)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (trigger_type, trigger_condition, trigger_value, action_type, action_value, priority)
        
        cursor.execute(sql, values)
        connection.commit()
        new_id = cursor.lastrowid
        print("Automation saved successfully.")
        return {"status": "success", "id": new_id}
    except mysql.connector.Error as e:
        print(f"Error saving automation: {e}")
        return {"status": "error", "message": str(e)}
    finally:
        cursor.close()
        connection.close()

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
        # Order by priority DESC (highest priority first)
        cursor.execute("SELECT * FROM automations ORDER BY priority DESC")
        automations = cursor.fetchall()
        return automations
    except mysql.connector.Error as e:
        print(f"Error retrieving automations: {e}")
        return []
    finally:
        cursor.close()
        connection.close()

def delete_automation(automation_id):
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    if connection is None:
        return {"status": "error", "message": "Database connection failed"}
    
    try:
        cursor = connection.cursor()
        sql = "DELETE FROM automations WHERE id = %s"
        cursor.execute(sql, (automation_id,))
        
        if cursor.rowcount == 0:
            return {"status": "error", "message": f"No automation found with ID {automation_id}"}
            
        connection.commit()
        print(f"Automation {automation_id} deleted successfully.")
        return {"status": "success", "message": f"Automation {automation_id} deleted successfully"}
    except mysql.connector.Error as e:
        print(f"Error deleting automation: {e}")
        return {"status": "error", "message": str(e)}
    finally:
        cursor.close()
        connection.close()

def get_automation(automation_id):
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    if connection is None:
        return None
    
    try:
        cursor = connection.cursor(dictionary=True)
        sql = "SELECT * FROM automations WHERE id = %s"
        cursor.execute(sql, (automation_id,))
        automation = cursor.fetchone()
        return automation
    except mysql.connector.Error as e:
        print(f"Error retrieving automation: {e}")
        return None
    finally:
        cursor.close()
        connection.close()

def update_automation(automation_id, trigger_type, trigger_condition, trigger_value, action_type, action_value, priority=0):
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    if connection is None:
        return {"status": "error", "message": "Database connection failed"}
    
    try:
        cursor = connection.cursor()
        sql = """
        UPDATE automations 
        SET trigger_type = %s, trigger_condition = %s, trigger_value = %s, 
            action_type = %s, action_value = %s, priority = %s 
        WHERE id = %s
        """
        values = (trigger_type, trigger_condition, trigger_value, action_type, action_value, priority, automation_id)
        
        cursor.execute(sql, values)
        
        if cursor.rowcount == 0:
            return {"status": "error", "message": f"No automation found with ID {automation_id}"}
            
        connection.commit()
        print(f"Automation {automation_id} updated successfully.")
        return {"status": "success", "id": automation_id}
    except mysql.connector.Error as e:
        print(f"Error updating automation: {e}")
        return {"status": "error", "message": str(e)}
    finally:
        cursor.close()
        connection.close()

def update_automation_priority(automation_id, priority):
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    if connection is None:
        return {"status": "error", "message": "Database connection failed"}
    
    try:
        cursor = connection.cursor()
        sql = "UPDATE automations SET priority = %s WHERE id = %s"
        cursor.execute(sql, (priority, automation_id))
        
        if cursor.rowcount == 0:
            return {"status": "error", "message": f"No automation found with ID {automation_id}"}
            
        connection.commit()
        print(f"Automation {automation_id} priority updated to {priority}.")
        return {"status": "success", "id": automation_id, "priority": priority}
    except mysql.connector.Error as e:
        print(f"Error updating automation priority: {e}")
        return {"status": "error", "message": str(e)}
    finally:
        cursor.close()
        connection.close()

