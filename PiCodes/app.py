from flask import Flask, render_template, request, jsonify
import requests
from datetime import datetime, timedelta
import mysql.connector
import databaseManager
import serial
import time
from Curtain import Data as CurtainData
import humanDetect

# Initialize database
databaseManager.create_database()
databaseManager.create_table()
last_save_time = time.time()
sensor_data = CurtainData(
    curtain_pos=0,
    temperature=0.0,
    humidity=0.0,
    light_in=0.0,
    light_out=0.0,
)
# Initialize Flask app
app = Flask(__name__)

@app.route('/')
def home():
    API_KEY = "34cc98b3b16e72fe6ffbf9a6916d4202"  # Replace with your actual API key

    
    try:
        url = f"https://api.openweathermap.org/data/2.5/forecast/daily?q=Kuching&cnt=8&appid={API_KEY}"
        response = requests.get(url)
        data = response.json()
        
        forecast = []
        for i in range(7):
            day = datetime.now() + timedelta(days=i)
            day_name = day.strftime("%a")
            
            weather_condition = data['list'][i]['weather'][0]['main']
            icon_map = {
                "Clear": "fas fa-sun",
                "Clouds": "fas fa-cloud",
                "Rain": "fas fa-cloud-showers-heavy",
                "Snow": "fas fa-snowflake"
            }
            icon = icon_map.get(weather_condition, "fas fa-cloud-sun")
            
            temp = round(data['list'][i]['temp']['day'] - 273.15)
            
            forecast.append({"day": day_name, "icon": icon, "temp": temp})
    except Exception as e:
        print(f"Error fetching weather data: {e}")
        forecast = [
            {"day": "error", "icon": "fas fa-cloud", "temp": 25},
            {"day": "Tues", "icon": "fas fa-cloud", "temp": 22},
            {"day": "Wed", "icon": "fas fa-cloud-sun", "temp": 24},
            {"day": "Thur", "icon": "fas fa-cloud-showers-heavy", "temp": 18},
            {"day": "Fri", "icon": "fas fa-sun", "temp": 27},
            {"day": "Sat", "icon": "fas fa-cloud", "temp": 20},
            {"day": "Sun", "icon": "fas fa-sun", "temp": 26}
        ]

    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat=1.5533&lon=110.3592&appid={API_KEY}"
        response = requests.get(url)
        data = response.json()
        
        weather_condition = data['weather'][0]['main']
        icon = icon_map.get(weather_condition, "fas fa-cloud-sun")
        
        current = {
            "temp": round(data['main']['temp'] - 273.15),
            "icon": icon,
            "description": data['weather'][0]['main']
        }
        
        sunset = datetime.fromtimestamp(data['sys']['sunset']).strftime('%I:%M %p')
        sunrise = datetime.fromtimestamp(data['sys']['sunrise']).strftime('%I:%M %p')
    except Exception as e:
        print(f"Error fetching weather data: {e}")
        current = {"temp": "Api Error", "icon": "fas fa-sun", "description": "Error"}
    
    return render_template("index.html", current=current, forecast=forecast, sunrise=sunrise, sunset=sunset)

@app.route('/temp/<time_range>')
def get_temp(time_range):
    return databaseManager.getTemp(time_range) if time_range in ['20min', 'hour', 'today'] else databaseManager.getTemp('today')

@app.route('/humidity/<time_range>')
def get_humidity(time_range):
    return databaseManager.getHumidity(time_range) if time_range in ['20min', 'hour', 'today'] else databaseManager.getHumidity('today')

@app.route('/curtain/<time_range>')
def get_curtain(time_range):
    return databaseManager.getCurtain(time_range) if time_range in ['20min', 'hour', 'today'] else databaseManager.getCurtain('today')

@app.route('/light/<time_range>')
def get_light(time_range):
    return databaseManager.getLight(time_range) if time_range in ['20min', 'hour', 'today'] else databaseManager.getLight('today')

@app.route('/curtain/set/<int:value>', methods=['POST'])
def set_curtain(value):
    try:
        ser.write(f'{value}\n'.encode('utf-8'))
        return {"status": "success", "message": f"Curtain position set to {value}"}, 200
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500
    
@app.route('/curtain/get', methods=['GET'])
def get_curtain_position():
    return {"curtain_pos": sensor_data.curtain_pos}, 200

@app.route('/api/sensors', methods=['GET'])
def get_sensor_data():
    try:
        return jsonify({
            "status": "success",
            "data": {
                "temperature": sensor_data.temperature,
                "humidity": sensor_data.humidity,
                "light_in": sensor_data.light_in,
                "light_out": sensor_data.light_out,
                "curtain_pos": sensor_data.curtain_pos,
                "human_presence": sensor_data.human_presence if hasattr(sensor_data, 'human_presence') else False,
                "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/automation')
def automations():
    return render_template("automation.html")

@app.route('/api/automation', methods=['POST'])
def save_automation():
    if request.method == 'POST':
        try:
            data = request.json
            
            # Extract trigger data
            trigger_type = data['trigger']['type']
            action_type = data['action']['type']
            action_value = data['action']['value']
            
            # Get the lowest priority (highest number) for new automations
            automations = databaseManager.get_automations()
            new_priority = 1  # Default if no automations exist
            if automations:
                priorities = [a['priority'] for a in automations]
                new_priority = max(priorities) + 1
            
            # Process trigger condition and value based on trigger type
            trigger_condition = "="  # Default
            trigger_value = ""
            
            if trigger_type == 'time':
                trigger_value = data['trigger']['value']
            elif trigger_type == 'humanPresence':
                trigger_value = "1" if data['trigger']['value'] == 'detected' else "0"
            else:  # temperature, humidity, light sensors
                trigger_condition = ">" if data['trigger']['condition'] == 'above' else "<"
                trigger_value = data['trigger']['value']
            
            # Save to database
            result = databaseManager.save_automation(
                trigger_type, 
                trigger_condition, 
                trigger_value, 
                action_type, 
                action_value,
                new_priority  # Use automatic priority
            )
            
            return jsonify(result), 200 if result['status'] == 'success' else 500
            
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/automation', methods=['GET'])
def get_automations():
    try:
        automations = databaseManager.get_automations()
        return jsonify({"status": "success", "data": automations}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/automations')
def list_automations():
    try:
        automations = databaseManager.get_automations()
        return render_template(
            "automation-list.html", 
            automations=automations,
            get_trigger_icon=get_trigger_icon,
            get_action_icon=get_action_icon,
            get_trigger_description=get_trigger_description,
            get_action_description=get_action_description,
            get_automation_title=get_automation_title
        )
    except Exception as e:
        print(f"Error listing automations: {e}")
        return render_template("automation-list.html", automations=[])

@app.route('/api/automation/<int:id>', methods=['DELETE'])
def delete_automation(id):
    try:
        result = databaseManager.delete_automation(id)
        return jsonify(result), 200 if result['status'] == 'success' else 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/automations/reorder', methods=['POST'])
def reorder_automations():
    try:
        data = request.json
        automations = data['automations']
        
        # Update priorities based on new order
        results = []
        for i, automation in enumerate(automations):
            # Set priority in reverse order (highest index = highest priority)
            new_priority = len(automations) - i
            result = databaseManager.update_automation_priority(
                automation['id'], 
                new_priority
            )
            results.append(result)
        
        # Check if all updates were successful
        if all(r['status'] == 'success' for r in results):
            return jsonify({"status": "success", "message": "Automation order updated successfully"}), 200
        else:
            return jsonify({"status": "error", "message": "Some automations could not be updated"}), 500
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/automation/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def manage_automation(id):
    if request.method == 'GET':
        try:
            automation = databaseManager.get_automation(id)
            if automation:
                return jsonify({"status": "success", "data": automation}), 200
            else:
                return jsonify({"status": "error", "message": f"No automation found with ID {id}"}), 404
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500
            
    elif request.method == 'PUT':
        try:
            data = request.json
            
            # Extract trigger data
            trigger_type = data['trigger']['type']
            action_type = data['action']['type']
            action_value = data['action']['value']
            
            # Get the current priority value to preserve it
            current_automation = databaseManager.get_automation(id)
            priority = current_automation['priority'] if current_automation else 0
            
            # Process trigger condition and value based on trigger type
            trigger_condition = "="  # Default
            trigger_value = ""
            
            if trigger_type == 'time':
                trigger_value = data['trigger']['value']
            elif trigger_type == 'humanPresence':
                trigger_value = "1" if data['trigger']['value'] == 'detected' else "0"
            else:  # temperature, humidity, light sensors
                trigger_condition = ">" if data['trigger']['condition'] == 'above' else "<"
                trigger_value = data['trigger']['value']
            
            # Update in database
            result = databaseManager.update_automation(
                id,
                trigger_type, 
                trigger_condition, 
                trigger_value, 
                action_type, 
                action_value,
                priority  # Keep the existing priority
            )
            
            return jsonify(result), 200 if result['status'] == 'success' else 500
            
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500
            
    elif request.method == 'DELETE':
        try:
            # First get the priority of the automation to be deleted
            automation_to_delete = databaseManager.get_automation(id)
            if not automation_to_delete:
                return jsonify({"status": "error", "message": f"No automation found with ID {id}"}), 404
                
            deleted_priority = automation_to_delete['priority']
            
            # Delete the automation
            result = databaseManager.delete_automation(id)
            
            # If deletion was successful, update other automations' priorities
            if result['status'] == 'success':
                # Get all remaining automations
                all_automations = databaseManager.get_automations()
                
                # Update priorities for automations with higher priority than the deleted one
                for automation in all_automations:
                    if automation['priority'] > deleted_priority:
                        databaseManager.update_automation_priority(
                            automation['id'],
                            automation['priority'] - 1
                        )
                
            return jsonify(result), 200 if result['status'] == 'success' else 500
            
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500

# Helper functions for template rendering
def get_trigger_icon(trigger_type):
    icons = {
        'time': 'fa-clock',
        'temperature': 'fa-temperature-half',
        'humidity': 'fa-droplet',
        'lightInside': 'fa-lightbulb',
        'lightOutside': 'fa-sun',
        'humanPresence': 'fa-person'
    }
    return icons.get(trigger_type, 'fa-question')

def get_action_icon(action_type):
    icons = {
        'curtain': 'fa-blinds'
    }
    return icons.get(action_type, 'fa-question')

def get_trigger_description(automation):
    trigger_type = automation['trigger_type']
    trigger_condition = automation['trigger_condition']
    trigger_value = automation['trigger_value']
    
    if trigger_type == 'time':
        # Convert 24h format to 12h if needed
        return f"At {trigger_value}"
    
    elif trigger_type == 'humanPresence':
        presence = "detected" if trigger_value == "1" else "not detected"
        return f"When human presence is {presence}"
    
    else:  # sensors like temperature, humidity, light
        condition_symbol = ">" if trigger_condition == ">" else "<"
        
        if trigger_type == 'temperature':
            return f"When temperature is {condition_symbol} {trigger_value}°C"
        elif trigger_type == 'humidity':
            return f"When humidity is {condition_symbol} {trigger_value}%"
        elif trigger_type == 'lightInside':
            return f"When indoor light is {condition_symbol} {trigger_value} lux"
        elif trigger_type == 'lightOutside':
            return f"When outdoor light is {condition_symbol} {trigger_value} lux"
    
    return "Unknown trigger"

def get_action_description(automation):
    action_type = automation['action_type']
    action_value = automation['action_value']
    
    if action_type == 'curtain':
        return f"Set curtain position to {action_value}%"
    
    return "Unknown action"

def get_automation_title(automation):
    trigger_type = automation['trigger_type']
    action_type = automation['action_type']
    
    trigger_names = {
        'time': 'Time',
        'temperature': 'Temperature',
        'humidity': 'Humidity',
        'lightInside': 'Indoor Light',
        'lightOutside': 'Outdoor Light',
        'humanPresence': 'Presence'
    }
    
    action_names = {
        'curtain': 'Curtain'
    }
    
    trigger_name = trigger_names.get(trigger_type, 'Unknown')
    action_name = action_names.get(action_type, 'Unknown')
    
    return f"{trigger_name} → {action_name}"

last_val = 0
if __name__ == "__main__":
    from threading import Thread

    # Initialize database
    databaseManager.create_database()
    databaseManager.create_table()
    databaseManager.create_automations_table()  # Add this line to create the automations table
    
    # Run Flask in a separate thread without debug mode
    flask_thread = Thread(target=lambda: app.run(port=8001, host='0.0.0.0', use_reloader=False))
    flask_thread.start()

    # Initialize Serial Communication
    ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
    time.sleep(3)
    

    while True:
        try:
            data = ser.readline().decode('utf-8').strip()
            if data:
                dataArray = data.split("|")
                if dataArray[0] == "S" and dataArray[6] == "E":

                    sensor_data = CurtainData(
                        curtain_pos=int(dataArray[1]),
                        temperature=float(dataArray[4]),
                        humidity=float(dataArray[5]),
                        light_in=float(dataArray[2]),
                        light_out=float(dataArray[3]),
                        human_presence = last_val
                        
                    )
                    current_time = time.time()
                    if current_time - last_save_time >= 10:
                        last_val = humanDetect.detect_human()
                        sensor_data.human_presence = last_val
                        
                        
                        databaseManager.insert_curtain_data(sensor_data)
                        print("Data saved to database")
                        last_save_time = current_time
        except Exception as e:
            print(f"Error: {e}")
