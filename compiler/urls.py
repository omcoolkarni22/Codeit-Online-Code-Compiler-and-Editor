from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),  # Homepage
    path('login', Login, name='login'),  # Login URL
    path('registartion', Registration, name='registration'),  # Registration URL
    path('logout', Logout, name='logout'),  # Logout URL
    path('save_reset_password', save_reset_password, name='save_reset_password'),  # save the new password after reset
    path('send_email', send_email, name='send_email'),  # Send EMail
    path('save_code', SaveCode, name='save_code'),  # Save Code
    path('returnAllSavedCode', AllSavedCode, name='returnAllSavedCode'),  # return saved codes
    path('getCode', getCode, name='getCode'),  # get a particular code
    path('deleteSavedCode', deleteSavedCode, name='deleteSavedCode'),  # delete saved code
    path('returnAllSharedCode', AllSharedCode, name='returnAllSavedCode'),  # return shared saved codes
    path('saveShareCode', saveShareCode, name='saveShareCode'),  # Save the code that user want to share
    path('getSingleShareCode', getSingleShareCode, name='getSingleShareCode'),  # get the single shared code
    path('continue_as_a_guest', continue_as_a_guest, name='continue_as_a_guest'),  # continue as a guest with limited features
    path('reset/<str:unique_key>', forget_password, name='forget_password'),  # Forget Password HTML render
    path('<str:unique>', getShareCode, name='getShareCode'),  # for share url
]

