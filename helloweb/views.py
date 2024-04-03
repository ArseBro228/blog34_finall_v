from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.


def index(request):
    name = "Python"
    return HttpResponse(f'''
     <h1>Hello from Django</h1>
     <p>{name}</p>
     <a href='main'>main</a>
    ''')
def main(request):
    name = "Main"
    return HttpResponse(f'''
     <h1>Main</h1>
     <p>{name}</p>
     <a href='/'>index</a>
    ''')
