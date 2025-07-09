from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.messages import AIMessage
from langgraph.graph import END, StateGraph
import os
from pydantic import BaseModel, Field
from typing import TypedDict
from termcolor import colored
from agent.constants import model_name
from agent.tools import invalid,access_database,call_user
from agent.prompt import system_prompt,categorize_prompt

class AgentState(TypedDict):
    research_question: str
    tool_response: str
    agent_response: AIMessage
    agent_call_count: int = 0
    tool_call_count: int = 0

model = ChatGoogleGenerativeAI(
    model=model_name,
    temperature=0.1,
    )

model_with_tools = model.bind_tools(
    tools=[invalid,access_database,call_user],
)

tool_mapping = {
    'invalid': invalid,
    'access_database': access_database,
    'call_user': call_user,
}

user_message = HumanMessagePromptTemplate.from_template(
    """
    Conduct a comprehensive analysis of the request provided.
    USER REQUEST:{initial_request}
    """
)
system_message = SystemMessagePromptTemplate.from_template(
    system_prompt()
)
agent_request_generator_prompt = ChatPromptTemplate.from_messages([system_message, user_message])

agent_request_generator = agent_request_generator_prompt | model_with_tools

def agent(state: AgentState):
    print(colored("STATE at agent start:", "magenta"), colored(state, "cyan"))
    input("Paused ... Hit Enter to Execute Agent Logic...")
    last_ai_message = agent_request_generator.invoke({"initial_request": state["research_question"]})
    print("Agent invoked")
    state["agent_call_count"] += 1
    #append the response to the agent_response list in the state
    if last_ai_message is not None:
        state["agent_response"] = last_ai_message 
        if last_ai_message.content is not None and last_ai_message.content != "" :
            state["tool_response"]=last_ai_message.content
    print(colored("STATE at agent end:", "magenta"), colored(state, "cyan"))
    input("Paused Hit Enter to go to Should Continue Logic...")    
    return state

def call_tool(state: AgentState):
    print(colored("STATE at call_tool start:", "magenta"), colored(state, "cyan"))
    input("Paused at call_tool Start")
    agent_response = state["agent_response"]
    
    if hasattr(agent_response, 'tool_calls') and len(agent_response.tool_calls) > 0:
        tool_call = agent_response.tool_calls[0]
        tool = tool_mapping[tool_call["name"].lower()]
        try:
            tool_output = tool.invoke(tool_call["args"])
            state["tool_call_count"] += 1
            print(colored("Tool output:", "magenta"), colored(tool_output, "green"))
            print(f"Tool output is {tool_output} and type is {type(tool_output)}")
            # Store the tool output in the state
            if tool_output is not None:
                state["tool_response"] = tool_output
        except Exception as e:
            print(f"Error invoking tool: {e}")
            # Handle the error or log it as needed
    else:
        print("No tool calls found in agent response.")
    print(colored("STATE at call_tool end:", "magenta"), colored(state, "cyan"))
    input("Paused at call_tool End")
    return state
class Evaluation(BaseModel):
    result: bool = Field(description="True or False", required=True)

category_system_message = SystemMessagePromptTemplate.from_template(
    categorize_prompt()
)
category_user_message = HumanMessagePromptTemplate.from_template(
    """
    CONTEXT: Conduct a comprehensive analysis of the Initial Request from user and Tool Response and route the request into boolean true or false: 
    INITIAL REQUEST: {research_question}
    TOOL RESPONSE:{tool_response}
    """
)

# Define Agent Prompt template
category_generator_prompt = ChatPromptTemplate.from_messages([category_system_message, category_user_message])
structured_llm = model.with_structured_output(Evaluation)
category_generator = category_generator_prompt | structured_llm
def should_continue(state: AgentState):
    print(colored("STATE at should_continue start:", "magenta"), colored(state, "cyan"))
    input("Paused at Should Continue Start")
    print(colored("Evaluating whether the Question is Answered by the tool response or not... Please wait...", "red"))
    result = category_generator.invoke({"research_question": state["research_question"],
                                         "tool_response":state["tool_response"]
                                        })
    if isinstance(result, Evaluation):
        # Access the 'result' attribute from Evaluation
        print(colored("Is tool response good and should the flow go to END node? ", "cyan"), colored(result.result, "yellow"))
        input("Paused at Should Continue Mid")
        
        if result.result:  # If result is True
            print(colored("Return end", "red"))
            return "end"
        else:  # If result is False
            print(colored("Return continue", "green"))
            return "continue"
    else:
        print("Result is not an Evaluation instance, returning 'end' as default.")
        return "end"

def start_agent(instruction: str):
    workflow = StateGraph(AgentState)

    workflow.add_node("agent", agent)
    workflow.add_node("action", call_tool)

    workflow.set_entry_point("agent")

    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "continue": "action",
            "end": END,
        },
    )
    workflow.add_edge("action", "agent")

    app = workflow.compile()
    state : AgentState = {"research_question": instruction,
                      "tool_response": [] ,
                      "agent_response": [],
                      "agent_call_count": 0,
                      "tool_call_count": 0
                      }
    result = app.invoke(state)
    print(colored("Final Result:", "yellow"), colored(result, "green"))

    #helper method to visualize graph
    # def save_graph_to_file(runnable_graph, output_file_path):
    #     png_bytes = runnable_graph.get_graph().draw_mermaid_png()
    #     with open(output_file_path, 'wb') as file:
    #         file.write(png_bytes)

    # save_graph_to_file(app, "output-05.png")