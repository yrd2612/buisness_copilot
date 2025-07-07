from langchain_core.tools import tool
from agent.tools_utils.call import get_user_details
@tool
def call_user(message: str,parameter:str) -> str:
    """
    Call the user to discuss tasks or gather information.
    
    Args:
        message (str): The message to send to the user.
        
    Returns:
        str: Confirmation that the user has been called.
    """
    output = get_user_details(parameter)
    print(f"Parameter received: {parameter}")
    return f"Calling user with message: {message}"
@tool
def access_database(query: str,parameter:str) -> str:
    """
    Access the database to read or write information.
    
    Args:
        query (str): The query to execute on the database.
        
    Returns:
        str: Confirmation of the database operation.
    """
    print(f"Parameter received: {parameter}")
    return f"Accessing database with query: {query} and parameter: {parameter}"
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