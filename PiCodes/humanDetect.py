import boto3
import requests

def detect_human():
    try:
        # AWS credentials & region
        aws_access_key_id = 'AKIAZU6BCQVM5OPQY2VF'
        aws_secret_access_key = 'UR913vZ3iBGClqEu2JnhWM2RS7u7DhpAiwCwtuTg'
        region_name = 'ap-southeast-2'  # e.g., 'us-west-2'

        # Fetch image from IP camera
        url = "http://192.168.156.203/capture"
        response = requests.get(url)
        image_bytes = response.content

        # Initialize AWS Rekognition client
        client = boto3.client(
            'rekognition',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name
        )

        # Call Rekognition to detect labels (like 'Person')
        response = client.detect_labels(
            Image={'Bytes': image_bytes},
            MaxLabels=10,
            MinConfidence=70
        )

        # Process detected labels
        detected_people = []
        for label in response['Labels']:
            if label['Name'] == 'Person':
                detected_people.append(label)

        # Output result
        if detected_people:
            print("Human Detected")
            return 1
            
        else:
            print("No Human Detected")
            return 0

    except Exception as e:
        print(f"Error: {e}")
        return 0
