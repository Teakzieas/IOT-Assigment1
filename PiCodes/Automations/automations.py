import requests
import database
from datetime import datetime
import time  # Add time module for sleep function

def get_sensordata():
    try:
        # Fetch data from the external API
        response = requests.get('http://divyessh.local:8001/api/sensors')
        response.raise_for_status()  # Raise an exception for HTTP errors
        sensors_data = response.json()

        
        # Return the fetched data
        return sensors_data
    except Exception as e:
        return {"status": "error", "message": str(e)}




def evaluate_trigger(automation, sensor_data):
    """Evaluate if a trigger condition is met based on sensor data"""
    trigger_type = automation['trigger_type']
    condition = automation['trigger_condition']
    value = automation['trigger_value']
    
    # Map trigger types to sensor data keys
    trigger_map = {
        'temperature': 'temperature',
        'humidity': 'humidity',
        'lightInside': 'light_in',
        'lightOutside': 'light_out',
        'humanPresence': 'human_presence',
        'time': None  # Special case for time
    }
    
    # Handle time trigger separately
    if trigger_type == 'time':
        current_time = datetime.now().strftime('%H:%M')
        if condition == '=' and current_time == value:
            return True
        return False
    
    # Get the corresponding sensor value
    sensor_key = trigger_map.get(trigger_type)
    if not sensor_key or 'data' not in sensor_data or sensor_key not in sensor_data['data']:
        return False
    
    sensor_value = sensor_data['data'][sensor_key]
    
    # Handle human presence which is boolean
    if trigger_type == 'humanPresence':
        
        
        if(int(sensor_value) == 0 and int(value) == 0):
            return True
        else:
            return False
    
    # Convert values for comparison
    try:
        sensor_value = float(sensor_value)
        trigger_value = float(value)
        
        if condition == '=':
            return sensor_value == trigger_value
        elif condition == '>':
            return sensor_value > trigger_value
        elif condition == '<':
            return sensor_value < trigger_value
        else:
            return False
    except (ValueError, TypeError):
        return False

# Main loop to run automations every 5 seconds
try:
    print("Starting automation loop. Press Ctrl+C to exit.")
    while True:
        # Get current sensor data
        sensor_data = get_sensordata()
        # Get all automations
        automations = database.get_automations()
        # Sort automations by priority (highest first)
        sorted_automations = sorted(automations, key=lambda x: x['priority'], reverse=True)

        # Check each automation until a condition is met
        curtain_updated = False
        for automation in sorted_automations:
            if evaluate_trigger(automation, sensor_data):
                new_curtain_pos = automation['action_value']
                print(f"Automation ID {automation['id']} triggered - Setting curtain position to {new_curtain_pos}")
                # Send a POST request to update the curtain position
                try:
                    curtain_url = f"http://divyessh.local:8001/curtain/set/{new_curtain_pos}"
                    curtain_response = requests.post(curtain_url)
                    curtain_response.raise_for_status()
                    print(f"Curtain position updated successfully: {curtain_response.text}")
                except Exception as e:
                    print(f"Failed to update curtain position: {e}")
                curtain_updated = True
                break

        if not curtain_updated:
            print("No automation conditions were met")
            
        # Wait for 5 seconds before the next check
        time.sleep(5)
        
except KeyboardInterrupt:
    print("Automation loop stopped by user.")
