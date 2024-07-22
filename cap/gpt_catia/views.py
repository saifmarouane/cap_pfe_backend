import json
from django.shortcuts import render
#from toolkit import check_set_cookies
from django.shortcuts import redirect
from django.http import HttpResponse
from toolkit import check_set_cookies
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_protect

from service.service import generate_report, handle_feedback, get_feedback_conversation
#from database.dataconn import get_db_conn
# Create your views here.

def index_view(request):
    # Vous pouvez passer des variables de contexte si nécessaire, par exemple : {'variable': valeur}
    
    return render(request, 'index.html')
def bots_view(request):
    return render(request, 'bots.html') 
import uuid

def generate_user_id():
    """
    Génère et renvoie un nouvel identifiant utilisateur unique.
    """
    return str(uuid.uuid4())

def generate_session_id():
    """
    Génère et renvoie un nouvel identifiant de session unique.
    """
    return str(uuid.uuid4())
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt

def chat_view(request):
    user = request.GET.get('user')
    session = request.GET.get('session')
    print("user",user)
    if not user or not session:
        # Si les cookies 'user' ou 'session' ne sont pas présents, générez-les et définissez-les
        user = generate_user_id()  # Générer un nouvel identifiant utilisateur
        session = generate_session_id()  # Générer un nouvel identifiant de session
        response = HttpResponse(render(request, "chat.html"))
        response.set_cookie('user', user, max_age=3600*24*365*10)  # 10 ans de cookie utilisateur
        response.set_cookie('session', session, max_age=3600*6)  # 6 heures de cookie de session
        print("got problem")
        return response
    else:
        print("user,session")
    if request.method == "POST":
        print("posting")

        user_response = request.POST.get("jawab")
        handle_feedback("bot1", user, session, user_response)
        print("you are trying to post ")
        #return redirect("chat")
        return  HttpResponse("user_response")
    else:
        print("but you are trying to get")

        # Récupérer et afficher la conversation
        conversation = get_feedback_conversation('bot1', user, session)
        return render(request, "chat.html", {'chat': conversation})
        #return HttpResponse(conversation)
        #return JsonResponse(conversation, safe=False,content_type='application/json')

def reset_session_cookie(request):
    redirection = "chat"
    assert redirection == "chat", f"Redirection value should be 'chat' but received '{redirection}'"
    
    # Crée une réponse de redirection vers la page spécifiée
    response = redirect(redirection)
    
    # Supprime le cookie de session en définissant sa date d'expiration à une date passée
    response.set_cookie('session', '', expires=0)
    
    return response
  


## asuprimer 
from django.http import JsonResponse
@csrf_exempt
def test_chat_api(request):
    #user = request.COOKIES.get('user')
    #session = request.COOKIES.get('session')
    #user = "31b35056-4f4a-4d04-a64a-b6ab7c1b46e0"
    #session = "0e63373e-6aff-4545-a08b-0da963945a4d"

    if request.method == "POST":
        try:
            # Récupérer les données JSON de la requête POST
            data = json.loads(request.body.decode('utf-8'))
            # Extraire le message de la requête
            user_response = data.get('message')
            user = data.get('user')
            session=data.get('session')
            
            if not user or not session:
                print(" no : user,session")
            else :
                print("get info succied")

            # Afficher le message dans le terminal
            a=handle_feedback("bot1", user, session, user_response)
            #return redirect("chat")
            print(a)
            return  HttpResponse(user_response)
        except json.JSONDecodeError:
            # Si les données JSON ne peuvent pas être décodées, renvoyer une réponse d'erreur
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)


    else:
        user =request.GET.get('user') 
        session = request.GET.get('session')
        if not user or not session:
            print(" no : user,session")
        else :
            print("get info succied")
            #print(user,session)

            # Récupérer et afficher la conversation
            conversation = get_feedback_conversation('bot1', user, session)
            #return render(request, "chat.html", {'chat': conversation})
            #return HttpResponse(conversation)
            return JsonResponse(conversation, safe=False,content_type='application/json')
@csrf_exempt
def summary(request):
        user =request.GET.get('user') 
        session = request.GET.get('session')
        print(user)

        if not user or not session:
            print(" no :summar  user,session")
        else :
            print("summary get info succied**********************************************")
            #print(user,session)

            # Récupérer et afficher la conversation
            summary = generate_report('bot1', user, session)
            print("prinsummary get info succied/////////////////////////////////////")

            print(summary)
            #return render(request, "chat.html", {'chat': conversation})
            #return HttpResponse(conversation)
            return JsonResponse(summary, safe=False)
import os
from django.http import StreamingHttpResponse, HttpResponseNotFound

def file_iterator(file_path, chunk_size=8192):
    with open(file_path, 'rb') as file:
        while chunk := file.read(chunk_size):
            yield chunk
@csrf_exempt
def generate_step_file(request):
    file_path = 'C:\\Users\\GO\\Desktop\cap\\cap_pfe_backend\\cap\\text-to-cad-output.step'
    #file_path="C:/Users/mosaif/Desktop/s.stl"
    #print(file_path)
    if os.path.exists(file_path):
        response = StreamingHttpResponse(file_iterator(file_path), content_type="application/octet-stream")
        response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
        print(response)
        return response
    else:
        print("hihihiihihihihih")
        return HttpResponseNotFound("File not found.")

