import json
import boto3

def lambda_handler(event, context):
    # Extract the 'body' part of the event
    data = event['body']

    # Create a client to interact with the AWS Bedrock Agent Runtime service
    client = boto3.client('bedrock-agent-runtime')

    # Parse the JSON body string into a Python dictionary
    data_dict = json.loads(data)

    # Extract the input text and session ID
    input_text = data_dict['text']
    session_id = data_dict['sessionId']

    try:
        # Invoke the Bedrock Agent with the provided session and input text
        response = client.invoke_agent(
            agentId='E61P3FRKRC',       
            agentAliasId='ZPLEU9BGWX',  
            sessionId=session_id,       
            inputText=input_text,       
            endSession=False            
        )

        # Initialize an empty string to store the agent’s response text
        reponse_text = ""

        # The response is streamed in chunks; iterate over them to assemble the full text
        for event in response.get('completion', []):
            if "chunk" in event and "bytes" in event["chunk"]:
                # Decode each chunk from bytes to UTF-8 text and append it to the full response
                reponse_text += event['chunk']['bytes'].decode('utf8')

        # Print the complete response for debugging/logging purposes
        print(reponse_text)

        # Return the response text as a JSON payload with HTTP 200 OK status
        return {
            'statusCode': 200,
            'body': json.dumps({
                "response": reponse_text
            })
        }

    except Exception as e:
        # Catch any exceptions, log them, and return a 500 error response
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
