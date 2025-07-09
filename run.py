from agent.configuration import start_agent

if __name__ == "__main__":
    # initialize_application()
    instruction = "Check if any Raj Paper Mills have balance 50000"
    instruction = "Call Manu and ask if he has reached the office"

    start_agent(instruction)