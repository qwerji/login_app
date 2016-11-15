from django.shortcuts import render, redirect
from django.contrib import messages
from models import User

def session_check(request):
    if 'user' in request.session:
        return True
    else:
        return False

def index(request):
    if session_check(request):
        # VV REDIRECT TO APP VV
        return redirect('success')
    else:
        return render(request,'login/index.html')

def login_reg(request):
    if request.POST['action'] == 'register':
        result = User.objects.validate_reg(request)

    elif request.POST['action'] == 'login':
        result = User.objects.validate_login(request)

    if result[0] == False:
        print_errors(request, result[1])
        return redirect('index')

    return log_user_in(request, result[1])

def print_errors(request, error_list):
    for error in error_list:
        messages.add_message(request, messages.INFO, error)

def log_user_in(request, user):
    request.session['user'] = {
        'user_id': user.id,
        'first_name': user.first_name
    }

    # VV REDIRECT TO APP VV
    return redirect('success')

def logout(request):
    request.session.clear()

    return redirect('index')

def success(request):
    return render(request, 'login/success.html')
