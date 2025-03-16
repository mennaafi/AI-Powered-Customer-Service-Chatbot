from fastapi import APIRouter, HTTPException
from api.agents import GuardAgent, ClassificationAgent, DetailsAgent, OrderTakingAgent, RecommendationAgent

router = APIRouter(prefix="/chat", tags=["Chat"])

guard_agent = GuardAgent()
classification_agent = ClassificationAgent()
recommendation_agent = RecommendationAgent(
    "api/recommendation_objects/apriori_recommendation.json",
    "api/recommendation_objects/popularity_recommendation.csv"
)

agent_dict = {
    "details_agent": DetailsAgent(),
    "order_taking_agent": OrderTakingAgent(recommendation_agent),
    "recommendation_agent": recommendation_agent
}

@router.get("/")
async def chat(query: str):
    """
    Chatbot endpoint that takes a user message and returns a response.
    """
    try:
        messages = [{"role": "user", "parts": query}]  

        # Guard Agent: Check if the message is allowed
        guard_response = guard_agent.get_response(messages)
        if guard_response["memory"]["guard_decision"] == "not allowed":
            return {"response": guard_response["parts"]}

        # Classification Agent: Decide which agent to use
        classification_response = classification_agent.get_response(messages)
        chosen_agent = classification_response["memory"]["classification_decision"]

        # Get the corresponding agent
        agent = agent_dict.get(chosen_agent)
        if not agent:
            raise HTTPException(status_code=400, detail="Invalid agent selected")

        # Get response from the chosen agent
        response = agent.get_response(messages)
        return {"response": response.get("parts", "No response available")}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
