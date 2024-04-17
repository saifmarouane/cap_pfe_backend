import os
import openai

from cap import settings

# Assurez-vous que la clé API d'OpenAI est définie comme une variable d'environnement
openai.api_key = settings.OPENAI_API_KEY



def get_chatgpt_response(prompt, enduser, top_p_val=0.2, model="gpt-3.5-turbo"):
    #return "Mock test content" ## For testing purposes only

    openai_response = openai.ChatCompletion.create(
            model=model,
            messages=prompt,
            top_p=top_p_val,
            presence_penalty=-1.0,
            frequency_penalty=1.0,
            user=enduser,
        )

    return openai_response.choices[0].message.content
def generate_new_conversation_context(app, user):
    return "hello"