from .gpt import get_chatgpt_response
# Adaptez cet import selon l'emplacement de votre modèle Log
from gpt_catia.models import Log
import yaml
from prompts.prompts import get_feedback_conversation_prompt

def generate_prompt_base(app, user, session):
    # Récupère les données de la session de conversation depuis la base de données
    conversation_logs = Log.objects.filter(app=app, enduser=user, sess=session).order_by('-ts')[:50]
    conversation_prompt = [{"role": "user" if log.speaker == "enduser" else "assistant", "content": log.msg} for log in conversation_logs]
    print(conversation_prompt)
    # Générer le contexte de base pour le prompte
    #clean_context = "Pas de contexte"  # Mettre à jour selon la logique souhaitée pour déterminer le contexte
    #prompt = [{"role": "system", "content": clean_context}] + conversation_prompt
    prompt=get_feedback_conversation_prompt(app)+ conversation_prompt
    return prompt

def generate_new_conversation_context(app, user):
    # Récupère l'historique complet des conversations de l'utilisateur
    conversation_logs = Log.objects.filter(app=app, enduser=user).order_by('-ts')
    conversation_prompt = [f"{log.speaker.capitalize()}: {log.msg}" for log in conversation_logs]

    # Construire le prompt pour la génération du résumé
    prompt_summary = "Résumez la conversation suivante:\n" + '\n'.join(conversation_prompt)
    return get_chatgpt_response([{"role": "system", "content": prompt_summary}], user, top_p_val=0.5)

def get_chatgpt_feedback_response(app, user, session, jawab):
    prompt = generate_prompt_base(app, user, session)
    prompt_with_temp_response = prompt + [{"role": "user", "content": jawab}]
    return get_chatgpt_response(prompt_with_temp_response, user, top_p_val=0.5)
