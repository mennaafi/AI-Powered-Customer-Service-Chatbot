<div align="center">  

## Multi Agentic Rag with Recommendation Engines Customer Service Chatbot

##### Welcome to the Coffee Shop Customer Service Chatbot.The chatbot handles real-time order-taking, answers menu queries using a Retrieval-Augmented Generation (RAG) system, and offers personalized product recommendations via a market basket analysis engine. It integrates specialized agents, including Guard, Order Taking, Details, and Recommendation agents, to ensure efficient, safe, and relevant interactions.

![Project Overview](https://github.com/user-attachments/assets/60316d88-5481-4e8f-a5fa-a9e68ce7ad37)

 
 </div>



## Datasets Overview :

 
- **In datasets folder** : You can find all datasets about customers transactions i will use them to **build recommendation engines** .
- **dataset link** : https://www.kaggle.com/datasets/ylchang/coffee-shop-sample-data-1113
- **In products folder** : You can find all information about our coffee shop and menu items and prices and all products descriptions.


## Recommendation Engines :
### In this project , I will use two recommendation engines


- **Apriori Recommendation Engine :**  
 will be used to leverages market basket analysis to suggest complementary products based on customers' previous purchases or preferences. By analyzing item associations and patterns in transaction data, it identifies products that are frequently bought together and recommends them to users.

- **Popularity Recommendation Engine :**  
This is useful for customers who visit our shop for the first time since we don't have any information about them.
Customer can choose to be recommended by specific product or category.


## Knowledge base :

The Knowledge Base is powered by Pinecone, where embeddings of data about our coffee shop and menu items, ingredients and other relevant product details  are stored in Pinecone. When a customer asks specific questions through the chatbot, such as asking about a product’s ingredients or prices information, the Retrieval-Augmented Generation (RAG) system retrieves the most relevant data from Pinecone


## All about Agents :


The chatbot utilizes a modular architecture with specialized agents, each designed to handle specific tasks, ensuring efficient and accurate customer service. Here’s an overview of each key agent:

>- **Guard Agent :**  The first line of defense, this agent filters all incoming user queries. It ensures that only relevant, safe, and appropriate queries are processed by other agents, blocking harmful or irrelevant inputs to protect the system and maintain smooth conversations.

>- **Classification Agent** : Acting as the decision-making layer, the Classification Agent determines the intent behind incoming user queries. By classifying the queries into categories (e.g., order-related, product inquiries, or recommendations), it routes the query to the most appropriate agent for processing.

>- **Details Agent (RAG System):**  Powered by a Retrieval-Augmented Generation (RAG) system, this agent provides detailed responses to customer queries about menu items, ingredients, allergens, and more. It retrieves relevant data stored in the vector database and combines it with language generation to deliver precise and informative answers.

>- **Recommendation Agent :** Triggered by the Order Taking Agent, this agent suggests personalized product recommendations. It leverages a market basket analysis engine to analyze the customer’s order or preferences, suggesting complementary products and enhancing upselling opportunities.


>- **Order Taking Agent** : This agent guides customers through the order placement process. Using chain-of-thought prompt engineering, it simulates human-like reasoning to gather all necessary order details step by step. The agent ensures that orders are structured correctly and reflect customer preferences, enhancing the accuracy and reliability of the order.



## Pipline of work :

When a customer submits a query, the Guard Agent first evaluates its relevance and appropriateness.
If the query is deemed valid, the Classification Agent analyzes it to determine the user's intent, such as placing an order, inquiring about a product, or seeking a recommendation.
Depending on the identified intent, the query is routed to the appropriate agent:
The Order Taking Agent handles all order-related tasks, guiding the user through the process.
If necessary, the Order Taking Agent may also forward the order to the Recommendation Agent, which suggests complementary items to enhance the order.
The Details Agent is responsible for retrieving detailed product information, such as ingredients or allergens.
The Recommendation Agent provides personalized product suggestions based on the user's preferences or current order.






### Install Dependencies :

 > - Before running the code, make sure you have all the required dependencies installed. 


```
pip install -r requirements.txt  
```
 > - then run script :


```
python api\development.py
```
 > - After running the script, you can interact with the chatbot by entering your queries directly into the terminal. The chatbot will process your inputs and provide appropriate responses based on the system's agents and their respective functions.


 


   











