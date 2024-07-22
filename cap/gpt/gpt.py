import time



import openai
from cap import settings
import anthropic
# Assurez-vous que la clé API d'OpenAI est définie comme une variable d'environnement
openai.api_key = settings.OPENAI_API_KEY



def get_chatgpt_response2(prompt, enduser, top_p_val=0.2, model="gpt-3.5-turbo"):
    #return "Mock test content" ## For testing purposes only
    print(openai.api_key)
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
client = anthropic.Anthropic(
        # defaults to os.environ.get("ANTHROPIC_API_KEY")
        api_key="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",
    )
def get_chatgpt_response(prompt, enduser, top_p_val=0.2):
    
    message = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1000,
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": str(prompt)
                    }
                ]
            }
        ]
    )
    return  message.content[0].text