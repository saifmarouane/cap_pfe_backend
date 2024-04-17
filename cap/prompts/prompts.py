import yaml
import os

# Chemin vers le dossier contenant les fichiers YAML
current_directory = os.path.dirname(__file__)

# Construisez le chemin relatif vers prompt_bot1.yml
YAML_FILE_PATH = os.path.join(current_directory, 'Yaml_Files', 'prompt_bot1.yml')
# Chargement du fichier YAML
with open(YAML_FILE_PATH, 'r', encoding='utf-8') as f:
    yml_bot1 = yaml.safe_load(f)

def return_yml(app):
    # Générer automatiquement le fichier YAML correspondant pour l'application spécifiée
    if app == 'bot1':
        return yml_bot1
    # Ajouter d'autres conditions pour d'autres applications si nécessaire
 
def get_feedback_conversation_prompt(app):
    # Utiliser la prompte associée au fichier YAML de l'application
    yml = return_yml(app)
    # Extraire les descriptions des niveaux
    #level_descriptions = {f"level{i}": yml['prompts']['levels'][f"level{i}"] for i in range(1, 6)}
    return [
        {"role": "system", "content": yml['prompts']['base']['system']},
        {"role": "assistant", "content": yml['prompts']['base']['assistant']},
    
        ]

def get_feedback_summarizer_prompt(app, conversation):
    yml = return_yml(app)
    return [{"role": "assistant", "content": yml['prompts']['monitoring']['summarizer'].replace("$conversation", conversation)}]

def get_feedback_level_choose():
    return None
