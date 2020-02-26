import json
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from bangazon_customer_api.models import Customer

@csrf_exempt
def login_user(request):
    """ Handles User Auth

    Method Args:
        request full object
    """
    # load JSON string of text body into a dictionary.
    req_body = json.loads(request.body.decode())

    if request.method == 'POST':

        username = req_body['username']
        password = req_body['password']
        authenticated_user = authenticate(username=username, password=password)

        if authenticated_user is not None:
            # This generates or gives tokens based on authentications for users.
            token = Token.objects.get(user=authenticated_user)
            data = json.dumps({'valid': True, 'token': token.key})
            return HttpResponse(data, content_type='applications/json')

        else:
            # what happens when login credentials are not correct
            # dumps() method converts dictionary object of python into JSON string data format. Now lets we perform our first encoding example with Python
            data = json.dumps({'valid': False})
            return HttpResponse(data, content_type='applications/json')

# CSRF_exempt is a feature of django which allows bypassing csrf verification by django.
# Cross Site Request Forgery protection
@csrf_exempt
def register_user(request):
    """Handles creation of a new user for auth

        Args:
        request = full http object
    """

    # JSON string of body reqested turned into a Dictionary
    req_body = json.loads(request.body.decode())

    # create a new user using django's built in craziness. create a user is a method in django.
    new_user = User.objects.create_user(
        username=req_body['username'],
        email=req_body['email'],
        password=req_body['password'],
        first_name=req_body['first_name'],
        last_name=req_body['last_name']
    )

    # make a customer after a user as well
    customer = Customer.objects.create(
        user=new_user
    )

    # Generate a Token for new user acct
    token = Token.objects.create(user=new_user)

    # give token and return to the user/cust/client app
    data = json.dumps({'token': token.key})
    return HttpResponse(data, content_type='application/json')
