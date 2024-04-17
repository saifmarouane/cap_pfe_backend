import random
import string
from django.http import HttpResponse

def get_random_str():
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(64))

def check_set_cookies(request, response):
    response = HttpResponse()

    user_cookie = request.COOKIES.get('user')
    if not user_cookie:
        user_cookie = get_random_str()
        response.set_cookie('user', user_cookie, max_age=3600*24*365*10)  # 10 years of user cookie

    session_cookie = request.COOKIES.get('session')
    if not session_cookie:
        session_cookie = get_random_str()
        response.set_cookie('session', session_cookie, max_age=3600*6)  # 6 hours of session cookie

    return response
