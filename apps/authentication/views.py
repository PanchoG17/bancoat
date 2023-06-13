# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from .forms import LoginForm, SignUpForm

from core.services import ADWSLogin

def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":
        # verifica el usuario
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            # compara con AD para dejar pasar el usuario
            if ADWSLogin(username, password):
                user = authenticate(username=username, password=password)
                if user is None:
                    try:
                        ### Usuario registrado con cambio de password
                        user = User.objects.get(username=username)
                        user.set_password(password)
                        user.save()
                        user = authenticate(username=username, password=password)
                        login(request, user)
                        return redirect("/")

                    except User.DoesNotExist:
                        msg = 'Usuario no registrado'
                else:
                    login(request, user)
                    return redirect("/")
            else:
                msg = 'Credenciales de acceso incorrectas.'
        else:
            msg = 'Error al validar los datos.'


    return render(request, "accounts/login.html", {"form": form, "msg": msg})


def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        # valida el formulario
        if form.is_valid():
            # obtiene los datos ingresados por el usuario
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            # compara con ad para registrar el usuario
            if ADWSLogin(username, raw_password):
                form.save()
                msg = 'Usuario registrado correctamente. <a href="/login" class="text-success">Iniciar sesión</a>'
                success = True
                return render(request, "accounts/register.html", {"success": success, "msg": msg, "form": SignUpForm()})
            else:
                msg = 'Las credenciales de usuario son incorrectas.'
        else:
            msg = 'Las credenciales de usuario son incorrectas.'
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})