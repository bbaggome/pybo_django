from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from ..forms import QuestionForm
from ..models import Question

PYBO_DETAIL = 'pybo:detail'

@login_required(login_url='common:login')
def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user   # author 속성에 로그인 계정 저장
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo:index')
    else:
        form = QuestionForm()
    context = {'form': form}    
    return render(request, 'pybo/question_form.html', context)


@login_required(login_url='common:login')
def question_modify(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다.')
        return redirect(PYBO_DETAIL, question_id=question.id)
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question) # instance 기준으로 QuestionForm 생성하지만 request.POST의 값으로 덮어쓰라는 의미
        if form.is_valid():
            question = form.save(commit=False)
            question.modify_date = timezone.now() #수정일시 저장
            question.save()
            return redirect(PYBO_DETAIL, question_id=question.id)
    else:
        form = QuestionForm(instance=question) # 폼의 속성 값이 instance의 값으로 채워짐
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)


@login_required(login_url='common:login')
def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다.')
        return redirect('pybo:detail', question_id=question.id)
    question.delete()
    return redirect('pybo:index')


@login_required(login_url='common:login')
def question_vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user == question.author:
        messages.error(request, '본인이 작성한 글은 추천 할 수 없습니다.')
    else:
        question.voter.add(request.user)
    return redirect(PYBO_DETAIL, question_id=question.id)