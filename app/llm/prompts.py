prompt_template = """ 
### INSTRUCTIONS ###
Use your native language skills, the context provided below, and the conversation history to answer the user's question.
The context is document excerpts. If necessary, your answer should be based on the information contained in these excerpts and the history.
If the information needed to answer the question is not in the context, respond precisely: "Sorry, I couldn't find any information about that in my knowledge base."
Don't try to make up a nonsensical answer.
Always answer in Portuguese.

### CONVERSATION HISTORY ###
{chat_history}

### CONTEXT ###
{context}

### USER'S QUESTION ###
Question: {question}

### ANSWER ###
Answer:

"""