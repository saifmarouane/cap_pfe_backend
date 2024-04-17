from gpt_catia.models import Log

def insert_user_data(app, user, session, message, speaker):
    """
    Insère une entrée de log dans la base de données.
    """
    log_entry = Log(app=app, enduser=user, sess=session, msg=message, speaker=speaker)
    log_entry.save()

def get_user_conversation_session_data(app, user, session):
    """
    Récupère les données de conversation pour une session donnée.
    """
    #return Log.objects.filter(app=app, enduser=user, sess=session).order_by('ts')
    conversation_data = Log.objects.filter(app=app, enduser=user, sess=session,speaker__in=['user', 'assistant']).order_by('ts')


    # Créer une liste pour stocker les données à afficher
    conversation_list = []

    # Boucler sur les données de la conversation et les ajouter à la liste
    for log in conversation_data:
        conversation_list.append({
            'role': log.speaker,  # Rôle de l'orateur (user ou assistant)
            'message': log.msg  # Message de l'orateur
        })

    # Passer la liste des données de la conversation au template
    return conversation_list
     
def get_last_summary_context(user, app):
    """
    Récupère le dernier contexte de résumé pour un utilisateur et une application donnés.
    """
    return Log.objects.filter(enduser=user, app=app, speaker='summary').order_by('-ts').first()
