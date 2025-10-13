import json
import boto3
import pandas as pd
from io import StringIO

# Define constants for the S3 bucket and the paths to the hotel and Airbnb CSV files
S3_BUCKET = 'testmath-agents'
HOTEL_CSV_KEY = 'hotel.csv'
AIRBNB_CSV_KEY = 'airbnb.csv'

def lambda_handler(event, context):
    print('Lambda function started')  # Log that the function has started

    try:
        # Extract key metadata fields from the event payload
        agent = event.get('agent', '')
        actionGroup = event.get('actionGroup', '')
        function = event.get('function', '')

        # Get the list of parameters sent in the event
        parameters = event.get('parameters', [])

        # Convert the list of parameters (name/value pairs) into a Python dictionary
        # Example: [{'name': 'location', 'value': 'Miami'}] → {'location': 'Miami'}
        param_dict = {param['name']: param['value'] for param in parameters}

        # --- Branch logic depending on which function was called by the agent ---
        if function == "list-hotels":
            # Extract parameters relevant to hotel listings
            location = param_dict.get('location', None)
            print(location)

            # Use the hotel CSV as the data source
            s3_key = HOTEL_CSV_KEY

            # Define the column to filter by and create a filter dictionary
            filter_column = 'Location'
            filters = {filter_column: location}

        elif function == "list-airbnbs":
            # Extract parameters relevant to Airbnb listings
            location = param_dict.get('location', None)
            pets = param_dict.get('pets', None)
            pool = param_dict.get('pool', None)
            sauna = param_dict.get('sauna', None)
            print(location, pets, pool, sauna)

            # Use the Airbnb CSV as the data source
            s3_key = AIRBNB_CSV_KEY

            # Build a dictionary of filters based on available parameters
            filters = {
                'Location': location,
                'Pets': pets,
                'Pool': pool,
                'Sauna': sauna
            }
        else:
            # If the function name is not recognized, return an error
            return {"error": "Invalid function name."}

        # --- Read CSV data from S3 ---
        s3_client = boto3.client('s3')  # Create an S3 client
        response = s3_client.get_object(Bucket=S3_BUCKET, Key=s3_key)  # Fetch the CSV file

        # Decode the CSV data from bytes to string
        csv_data = response['Body'].read().decode('utf-8')

        # Load the CSV data into a Pandas DataFrame for easy filtering
        df = pd.read_csv(StringIO(csv_data))

        # Clean up all string data in the DataFrame: remove extra spaces and make lowercase
        df = df.applymap(lambda x: x.strip().lower() if isinstance(x, str) else x)

        # --- Apply filters dynamically based on user-provided parameters ---
        for col, val in filters.items():
            if val is not None:
                # Compare case-insensitively and filter the DataFrame
                df = df[df[col].astype(str).str.lower() == str(val).lower()]

        # Convert the filtered DataFrame into a JSON string for returning
        filtered_data = json.dumps(df.to_dict(orient='records'), default=str)

        # Log the filtered data for debugging
        print(filtered_data)

        # Build the body of the response to send back to the caller
        responseBody = {
            "TEXT": {
                "body": filtered_data,
            }
        }

        # Construct the complete action response structure (expected by AWS Bedrock or other services)
        action_response = {
            'agent': agent,
            'actionGroup': actionGroup,
            'function': function,
            'functionResponse': {
                'responseBody': responseBody
            }
        }

        # Include message version metadata for compatibility with the caller
        accommodation_function_response = {
            'response': action_response,
            'messageVersion': event['messageVersion']
        }

        # Log and return the structured response
        print("Response: {}".format(accommodation_function_response))
        return accommodation_function_response

    except Exception as e:
        # Catch and log any errors during execution
        print("Error: {}".format(e))
        return {"error": str(e)}
