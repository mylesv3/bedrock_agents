import json
import boto3
import pandas as pd
from io import StringIO

# Define constants for the S3 bucket and CSV file location
S3_BUCKET = "testmath-agents"
S3_KEY = "restaurant.csv"

def lambda_handler(event, context):
    print("Lambda function started")  # Log that the Lambda function has been invoked

    try:
        # Extract key fields
        agent = event.get('agent', '')
        actionGroup = event.get('actionGroup', '')
        function = event.get('function', '')
        parameters = event.get('parameters', [])

        # Convert the list of parameter objects into a simple dictionary
        # Example: [{'name': 'city', 'value': 'Miami'}] → {'city': 'Miami'}
        param_dict = {param['name']: param['value'] for param in parameters}

        # Retrieve specific parameters (city and fine_dine)
        city = param_dict.get('city', None)
        fine_dine = param_dict.get('fine_dine', None)

        # Log the received filter values for debugging
        print(city, fine_dine)

        # Initialize an S3 client using boto3
        s3_client = boto3.client('s3')

        # Retrieve the CSV file (restaurant data) from S3
        response = s3_client.get_object(Bucket=S3_BUCKET, Key=S3_KEY)

        # Read and decode the CSV data from bytes to string
        csv_data = response['Body'].read().decode('utf-8')

        # Load the CSV data into a pandas DataFrame
        df = pd.read_csv(StringIO(csv_data))

        # Clean and normalize text data for consistent filtering (remove spaces and lowercase)
        df['Fine Dining'] = df['Fine Dining'].str.strip().str.lower()
        df['City'] = df['City'].str.strip().str.lower()

        # Apply filters based on provided parameters (if they exist)
        if city:
            df = df[df['City'] == city.strip().lower()]
        if fine_dine:
            df = df[df['Fine Dining'] == fine_dine.strip().lower()]

        # Convert the filtered DataFrame to a JSON string
        # orient='records' → list of dictionaries, one per row
        filtered_data = json.dumps(df.to_dict(orient='records'), default=str)

        # Structure the response body in the format expected by the calling service
        responseBody = {
            "TEXT": {
                "body": filtered_data,
            }
        }

        # Wrap the response in the expected format with metadata
        action_response = {
            'actionGroup': actionGroup,
            'function': function,
            'functionResponse': {
                'responseBody': responseBody
            }
        }

        # Final structured response including message version for compatibility
        restaurant_function_response = {
            'response': action_response,
            'messageVersion': event['messageVersion']
        }

        # Return the full response to the caller (e.g., AWS Bedrock Agent)
        return restaurant_function_response

    except Exception as e:
        # Log any errors and return an HTTP 400 response with the error message
        print(e)
        return {
            'statusCode': 400,
            'body': json.dumps(f'Error processing the request, error: {e}]')
        }
