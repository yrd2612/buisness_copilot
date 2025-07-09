from agent.neo4j_setup import connect_neo4j
from twilio.rest import Client
from agent.constants import twilio_access_token, twilio_account_sid, twilio_number
def send_message(instruction: str, phone_number: str) -> None:
    account_sid = twilio_account_sid
    auth_token = twilio_access_token
    client = Client(account_sid, auth_token)

    message = client.messages.create(
    from_=f'whatsapp:{twilio_number}',
    body=instruction,
    to=f'whatsapp:+91{phone_number}'
    )

    print(message.sid)
def get_user_details(parameter: dict) -> str:
    """
    Retrieve user details from neo4j database.
    
    Args:
        parameter (str): The name to use for retrieving user details.
        
    Returns:
        str: The user details.
    """
    # Simulate a database lookup or API call to get user details
    _driver = connect_neo4j().driver
    query = f"MATCH (n:{parameter['node_type']} {{name: '{parameter['name']}'}}) RETURN n"
    with _driver.session() as session:
            results = session.run(query).data()
            print("DB Call Results are",results)
    message_recieved = send_message(parameter['instruction'],results[0]['n']['phone_number'])
    # user_details = f"Details for user with parameter: {parameter}"


    return message_recieved