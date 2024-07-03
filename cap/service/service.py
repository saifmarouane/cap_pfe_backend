import datetime
from django.utils.timezone import make_aware
# Remplacez les imports suivants par les chemins d'accès corrects selon votre structure de projet
from prompts.prompts import get_feedback_summarizer_prompt
from gpt.gpt import get_chatgpt_response, generate_new_conversation_context
from database.datafuncs import get_user_conversation_session_data, insert_user_data, get_last_summary_context
from gpt.gpt_prompt import get_chatgpt_feedback_response, generate_new_conversation_context
from kitty.texttocad import kittycad_prompt
def handle_feedback(app, user, session, user_response):
    """
    Traite le feedback de l'utilisateur, génère une réponse de l'assistant et met à jour la base de données.
    """
    # Génère un résumé de la conversation si nécessaire
    #handle_summary(app, user, session)
    
    # Obtient la réponse de l'assistant basée sur le feedback de l'utilisateur

    assistant_response = get_chatgpt_feedback_response(app, user, session, user_response)
    # Enregistre la réponse de l'utilisateur et de l'assistant dans la base de données
    insert_user_data(app, user, session, user_response, 'user')
    insert_user_data(app, user, session, assistant_response, 'assistant')

def get_feedback_conversation(app, user, session):
    """
    Renvoie les données de la conversation pour une session donnée.
    """

    return get_user_conversation_session_data(app, user, session)

def handle_suggestion(user, session, user_response):
    """
    Gère les suggestions des utilisateurs en les enregistrant dans la base de données.
    """
    insert_user_data('feedback', user, session, user_response, 'suggestion')

def handle_summary(app, user, session):
    """
    Vérifie si un nouveau résumé de conversation est nécessaire et le génère le cas échéant.
    """
    last_summary = get_last_summary_context(user, app)
    now = make_aware(datetime.datetime.now())
    
    # Crée un nouveau résumé si le dernier résumé date de plus de 6 heures
    if not last_summary or (now - last_summary[0][1] > datetime.timedelta(hours=6)):
        response = generate_new_conversation_context(app, user)
        
        insert_user_data(app, user, session, response, 'summary')

def generate_report(app, user, session):
    """
    Génère un rapport de la conversation pour une session donnée.
    """
    conversation=get_user_conversation_session_data(app, user, session)
    summary=get_feedback_summarizer_prompt(app, conversation)
    prompt="A SPUR GEAR WITH 4 TEETH"
    
    prompt=get_chatgpt_feedback_response(app, user, session, summary)
    print("this is the summary", prompt)

    kittycad_prompt(prompt)

    return prompt
def download_cad(prompt):
    return kittycad_prompt(prompt)
