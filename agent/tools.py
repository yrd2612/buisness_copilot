from langchain_core.tools import tool
import json
from agent.tools_utils.call import get_user_details
from agent.tools_utils.db_utils import perform_db_actions
@tool
def call_user(message: str, parameter: str) -> str:
    """
    Call the user to discuss tasks or gather information.
    
    Args:
        message (str): The message to send to the user.
        paratmeter (dict): The parameter to use in the database operation.
        {
            "node_type": "customer" or "employee",
            "name": "name_of_the_concerned_person",
            "instruction": "message_to_be_sent_to_the_user",
        }
        
    Returns:
        str: Confirmation that the user has been called.
    Note: the "instruction" field should be formed in such a way that exact message will be sent to the user.
    """
    if isinstance(parameter, str):
        try:
            parameter = json.loads(parameter)
        except Exception as e:
            return f"Invalid parameter format: {e}"
    output = get_user_details(parameter)
    print(f"Parameter received: {parameter} with message: {message}")
    return f"Calling user with message SUCCESSFUL"
@tool
def access_database(query: str,parameter:dict) -> str:
    """
    Access the database to read or write information.
    
    Args:
        query (str): The query to execute on the database.
        paratmeter (dict): The parameter to use in the database operation.
        {
            "node_type": "customer" or "employee",
            "name": "name_of_the_concerned_person",
            "amount": "amount_to_be_paid_or_received",
            "query_type": "read" or "write" 
            "comparison": "greater_than" or "less_than" or "equal_to" or "not_equal_to" or "Not Applicable"
        }
        Note: The 'comparison' field is optional and can be used to specify the type of comparison for the amount. It is used only for query_type 'read'.
    Returns:
        str: Confirmation of the database operation.
    """
    print(f"Parameter received: {parameter}")
    db_output = perform_db_actions(parameter)
    return f"Accessing database with query: {query}\nParameter: {parameter} and type is {type(db_output)}\nOutput: {db_output}"
@tool
def invalid(message: str) -> str:
    """
    Use this tool when the user asks for something that is not supported by the available tools.
    
    Args:
        message (str): The message indicating the unsupported request.
        
    Returns:
        str: Confirmation that the request is invalid.
    """
    return f"Invalid request: {message}"