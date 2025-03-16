from agents import (GuardAgent ,ClassificationAgent , DetailsAgent , AgentProtocol, RecommendationAgent, OrderTakingAgent)
import os

def main():
    guard_agent = GuardAgent()
    classification_agent = ClassificationAgent()
    recommendation_agent =  RecommendationAgent(
    r'api/recommendation_objects/apriori_recommendation.json',
    r'api/recommendation_objects/popularity_recommendation.csv')

    agent_dict: dict[str, AgentProtocol] = {
        "details_agent": DetailsAgent(),
        "order_taking_agent": OrderTakingAgent(recommendation_agent),
        "recommendation_agent": recommendation_agent
    }
    
    messages = []
    while True:
        # Display the chat history
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("\n\nPrint Messages ...............")
        for message in messages:
            print(f"{message['role'].capitalize()}: {message['parts']}")

        # Get user input
        prompt = input("User: ")
        messages.append({"role": "user", "parts": prompt})

        # Get GuardAgent's response
        guard_agent_response = guard_agent.get_response(messages)
        if guard_agent_response["memory"]["guard_decision"] == "not allowed":
            messages.append({"role": "assistant", "parts": guard_agent_response["parts"]})
            continue


        # Get ClassificationAgent's response
        classification_agent_response = classification_agent.get_response(messages)
        chosen_agent = classification_agent_response['memory']['classification_decision']
        print("Chosen Agent" ,chosen_agent)


        # Get the chosen agent's response
        agent = agent_dict[chosen_agent]
        response = agent.get_response(messages)
        
        messages.append(response)

        
        

if __name__ == "__main__":
    main()

