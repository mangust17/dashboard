from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def dash_graph(request):
    return render(request, "dashboards/graph.html")


def plotly_dash(request):
    context = {}
    return render(request, "dashboards/plotly_dash.html", context)

def info(request):
    return render(request, "info.html")


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Неверный логин или пароль')
            return render(request, 'login.html')

    return render(request, 'login.html')