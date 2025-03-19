from django.shortcuts import render
from django.http import HttpResponse, HttpRequest

# Create your views here.


def set_value_in_cookie(request):
    response = HttpResponse('<h1> Hello universes </h1>')
    response.set_cookie('name', 'Toxir', expires=3600)
    return response


def get_value_from_cookie(request:HttpRequest):
    name = request.COOKIES.get("name")
    session_id = request.COOKIES.get("sessionid")
    csrftoken = request.COOKIES.get("csrftoken")
    print(name)
    return HttpResponse(f"{name} | {session_id} | {csrftoken}")


def update_value_in_cookie(request):
    response = HttpResponse('<h1> Hello universes </h1>')
    response.set_cookie('name', 'Sobir', expires=3600)
    return response


def delete(request):
    response = HttpResponse("O'chirildi!")
    response.delete_cookie("name")
    return response