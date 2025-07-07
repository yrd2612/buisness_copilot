from agent.configuration import agent_request_generator,start_agent
instruction = "Call abhishek and ask for attendance details"
result = agent_request_generator.invoke({"initial_request": instruction})
# print(result)
start_agent(instruction)