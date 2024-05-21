from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.views.generic import ListView
from .models import Question, Answer,Profile
from .forms import QuestionForm, AnswerForm, UserForm, ProfileForm,SignupForm, LoginForm


def home(request):
    questions = Question.objects.all().order_by('-date_posted')
    context = {'questions': questions}
    return render(request, 'base/home.html', context)


@login_required
def ask_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user
            question.save()
            return redirect('question_detail', pk=question.pk)
    else:
        form = QuestionForm()
    return render(request, 'base/ask_question.html', {'form': form})


@login_required
def edit_question(request, pk):
    question = get_object_or_404(Question, pk=pk, user=request.user)
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.save()
            return redirect('question_detail', pk=question.pk)
    else:
        form = QuestionForm(instance=question)
    return render(request, 'base/edit_question.html', {'form': form})


@login_required
def delete_question(request, pk):
    question = get_object_or_404(Question, pk=pk, user=request.user)
    question.delete()
    messages.success(request, "Question successfully deleted.")
    return redirect('home')


def question_detail(request, pk):
    question = get_object_or_404(Question, pk=pk)
    answers = Answer.objects.filter(question=question).order_by('-date_posted')
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.user = request.user
            answer.question = question
            answer.save()
            return redirect('base/question_detail', pk=question.pk)
    else:
        form = AnswerForm()
    return render(request, 'base/question_detail.html', {'question': question, 'answers': answers, 'form': form})


@login_required
def edit_answer(request, pk):
    answer = get_object_or_404(Answer, pk=pk, user=request.user)
    if request.method == 'POST':
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.save()
            return redirect('base/question_detail', pk=answer.question.pk)
    else:
        form = AnswerForm(instance=answer)
    return render(request, 'base/edit_answer.html', {'form': form})


@login_required
def delete_answer(request, pk):
    answer = get_object_or_404(Answer, pk=pk, user=request.user)
    question_pk = answer.question.pk
    answer.delete()
    messages.success(request, "Answer successfully deleted.")
    return redirect('base/question_detail', pk=question_pk) 


def search(request):
    query = request.GET.get('q')
    if query:
        questions = Question.objects.filter(title__icontains=query)
        context = {'questions': questions, 'query': query}
    else:
        context = {}
    return render(request, 'base/search.html', context )


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignupForm()
    return render(request, 'base/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'base/login.html', {'form': form})


@login_required
def answer_question(request, pk):
    question = get_object_or_404(Question, pk=pk)
    form = AnswerForm(request.POST or None)

    if form.is_valid():
        answer = form.save(commit=False)
        answer.author = request.user
        answer.question = question
        answer.save()

        # Update the question with the new answer count
    #    question.num_answers += 1
        question.save()

        messages.success(request, 'Your answer has been posted.')
        return redirect('question_detail', pk=question.pk)

    return render(request, 'base/answer_question.html', {'form': form, 'question': question})

@login_required
def answer_detail(request, pk):
    answer = get_object_or_404(Answer, pk=pk)
    question = answer.question
    user = request.user

    if request.method == 'POST':
        form = AnswerForm(request.POST)

        if form.is_valid():
            new_answer = form.save(commit=False)
            new_answer.question = question
            new_answer.user = user
            new_answer.save()

            return redirect('answer_detail', pk=answer.id)
    else:
        form = AnswerForm()

    context = {
        'answer': answer,
        'question': question,
        'form': form,
    }

    return render(request, 'base/answer_detail.html', context)

@login_required
def user_profile(request):
    user = request.user
    answers = Answer.objects.filter(author=request.user).order_by('-date_posted')
    return render(request, 'base/userprofile.html', {'answers': answers})


@login_required
def edit_profile(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile(user=request.user)
    if request.method=="POST":
        form = ProfileForm(data=request.POST, files=request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('user_profile')
    else:
        form=ProfileForm(instance=profile)
    return render(request, "base/edit_profile.html", {'form':form})


def logout_view(request):
    logout(request)
    return redirect('home')