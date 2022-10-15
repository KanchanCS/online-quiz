from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import *
from .models import *

# Create your views here.


# def home(request):
#     return render(request, "home.html")


def home(request):
    if request.method == "POST":
        print(request.POST)
        questions = QuesModel.objects.all()
        score = 0
        wrong = 0
        correct = 0
        total = 0
        for q in questions:
            total += 1
            print(request.POST.get(q.question))
            print(q.ans)
            print()
            if q.ans == request.POST.get(q.question):
                score += 10
                correct += 1
            else:
                wrong += 1
        percent = score / (total * 10) * 100
        context = {
            "score": score,
            "correct": correct,
            "wrong": wrong,
            "percent": percent,
            "total": total,
        }
        return render(request, "result.html", context)
    else:
        questions = QuesModel.objects.all()
        context = {"questions": questions}
        return render(request, "home.html", context)


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("quiz:quiz")
    else:
        form = RegisterForm()

    context = {
        "form": form,
    }
    return render(request, "register.html", context)


def login_req(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:

                login(request, user)
                if "next" in request.POST:
                    return redirect(request.POST.get("next"))
                else:
                    return redirect("quiz:quiz")
    else:
        form = LoginForm()

    context = {"login_form": form}
    return render(request, "login.html", context)


def logout_request(request):
    logout(request)
    return redirect("quiz:login")


def addQuestion(request):
    if request.user.is_staff:
        form = addQuestionform()
        if request.method == "POST":
            form = addQuestionform(request.POST)
            if form.is_valid():
                form.save()
                return redirect("/")
        context = {"form": form}
        return render(request, "addQuestion.html", context)
    else:
        return redirect("home")
