from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .models import UserCode, ShareCode, ForgetPassword
from django.http.response import JsonResponse
from .serializers import UserCodeSerializers, UserShareCodeSerializers
import random
import string
from .sendEmail import send
from django.contrib.auth.hashers import make_password


def home(request):
    if request.user.is_authenticated:
        return render(request, 'compiler.html')
    return render(request, 'index.html')


# User Login
@csrf_exempt
def Login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            if User.objects.filter(username=email).exists():
                messages.success(request, "Wrong Password!")
            else:
                messages.success(request, "User won't Exist, Please sign up")
            return redirect('/')
    return render(request, 'index.html')


# Registration
def Registration(request):
    if request.method == 'POST':
        firstName = request.POST['firstName']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if confirm_password == password:
            if not User.objects.filter(username=email).exists():
                user = User.objects.create_user(
                    username=email,
                    password=confirm_password,
                    email=email,
                    first_name=firstName,
                )
                user.save()
                user_4log = authenticate(request, username=email, password=confirm_password)
                login(request, user_4log)
                return redirect('/')
            else:
                messages.success(request, "User Already Exist, Please Login")
                return redirect('login')
        else:
            messages.success(request, "Password & Confirm Password doesn't Match...")
            return redirect('login')
    else:
        return render(request, 'index.html')


# Logout
def Logout(request):
    logout(request)
    return redirect('/')


# Send Email for Forgot password
@csrf_exempt
def send_email(request):
    if request.is_ajax() and request.method == "POST":
        email = request.POST['email']
        if not User.objects.filter(email=email).exists():
            return JsonResponse({"exist": False})
        else:
            url_reset = random.choices(population=string.ascii_lowercase + string.ascii_uppercase + string.digits, k=16)

            domain = 'http://127.0.0.1:8000/reset/'
            url = domain + ''.join(url_reset)
            is_sent = send(to=email, url=url)  # call send function to send email

            if is_sent:
                # save link only if mail is sent
                user = User.objects.get(email=email)  # get user object to save it
                ForgetPassword.objects.create(user=user, link=''.join(url_reset))  # save object
                return JsonResponse({"exist": True, "sent": True})
            else:
                return JsonResponse({"exist": True, "sent": False})


# Continue as a guest
def continue_as_a_guest(request):
    return render(request, 'continue_as_a_guest.html')


# render forgot password template
@csrf_exempt
def forget_password(request, unique_key):
    if request.method == 'GET':
        if ForgetPassword.objects.filter(link=unique_key).exists():  # chk if the unique key exists
            return render(request, 'forgetpassword.html',
                          {"email": ForgetPassword.objects.get(link=unique_key).user.email})
        else:  # return not found response
            return HttpResponse('<h2>Code-it Message: This link might be expired or already used!</h2>')
    elif request.method == 'POST':
        unique_url = request.POST['unique_url']
        password = request.POST['password']
        user = ForgetPassword.objects.get(link=unique_url).user
        User.objects.filter(email=user).update(password=make_password(password))
        ForgetPassword.objects.filter(link=unique_url).delete()  # delete unique link so it's no longer accessible
        return JsonResponse({"success": True})


# Save the password
@csrf_exempt
def save_reset_password(request):
    if request.method == 'POST':
        unique_url = request.POST['unique_url']
        password = request.POST['password']
        user = ForgetPassword.objects.get(link=unique_url).user
        User.objects.filter(email=user).update(password=make_password(password))
        ForgetPassword.objects.filter(link=unique_url).delete()  # delete unique link so it's no longer accessible
        return JsonResponse({"success": True})


# Save Code
@csrf_exempt
def SaveCode(request):
    if request.is_ajax() and request.method == 'POST':
        code = request.POST['code']
        language = request.POST['language']
        name = request.POST['name']
        user = request.user
        if language == 'py':
            language = 'python'

        UserCode.objects.create(
            user=user,
            code=code,
            language=language,
            name=name,
            slug=''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        )
        json = {
            "is_saved": False
        }
        return JsonResponse(json)


# return all saved codes by a user
@csrf_exempt
def AllSavedCode(request):
    if request.is_ajax() and request.method == 'POST':
        user = request.user
        all_codes = UserCode.objects.filter(user=user).order_by('-id')
        serializer = UserCodeSerializers(all_codes, many=True)
        return JsonResponse(serializer.data, safe=False)


# Return Single Code
@csrf_exempt
def getCode(request):
    if request.method == 'POST':
        slug = request.POST['slug']
        code = UserCode.objects.filter(slug=slug)
        serializer = UserCodeSerializers(code, many=True)
        return JsonResponse(serializer.data, safe=False)


# delete saved code
@csrf_exempt
def deleteSavedCode(request):
    if request.is_ajax() and request.method == 'POST':
        unique_url = request.POST['unique_url']
        try:
            UserCode.objects.get(slug=unique_url).delete()
            return JsonResponse({
                "success": True
            })
        except Exception as e:
            return JsonResponse({
                "success": False
            })


# Return all shared codes
@csrf_exempt
def AllSharedCode(request):
    if request.is_ajax() and request.method == 'POST':
        user = request.user
        all_codes = ShareCode.objects.filter(user=user).order_by('-id')
        serializer = UserShareCodeSerializers(all_codes, many=True)
        return JsonResponse(serializer.data, safe=False)


# Share & Save Code
@csrf_exempt
def saveShareCode(request):
    if request.is_ajax() and request.method == 'POST':
        user = request.user
        code = request.POST['code']
        permission = request.POST['permission']
        language = request.POST['language']
        uniqueShareUrl = request.POST['uniqueShareUrl'][-8:]
        ShareCode.objects.create(
            user=user,
            code=code,
            permission=permission,
            language=language,
            uniqueShareUrl=uniqueShareUrl
        )
        json = {
            'saved': True
        }
        return JsonResponse(json)


# return share URL and HTML
def getShareCode(request, unique):
    if request.method == 'GET':
        try:
            code = ShareCode.objects.get(uniqueShareUrl=unique)
        except ShareCode.DoesNotExist:
            return HttpResponse("URL doesn't exist")
        return render(request, 'share_code.html')


# this will be called once HTML page loads for shared URL
@csrf_exempt
def getSingleShareCode(request):
    if request.is_ajax() and request.method == 'POST':
        uniqueShareUrl = request.POST['uniqueShareUrl']
        try:
            code = ShareCode.objects.filter(uniqueShareUrl=uniqueShareUrl)
            code = UserShareCodeSerializers(code, many=True)
            # print(code.data)
            return JsonResponse(code.data, safe=False)
        except ShareCode.DoesNotExist:
            return JsonResponse({"exist": False})
