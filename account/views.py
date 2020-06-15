from django.shortcuts import render, redirect,get_object_or_404, HttpResponse
from django.contrib import auth
from .forms import *
from .models import User
from team.models import TeamMember
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.paginator import Paginator
import simplejson as json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

# 회원가입
def sign_up(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        # 폼이 검증되면 로그인 되고 sign_up url로 넘어감(이 부분은 메인 화면으로 넘어  가도록 수정할 예정)
        if form.is_valid():
            form.save()
            auth.login(request, User.objects.get(username=form.cleaned_data['username']))
            user = request.user
            return redirect('account:user_home', user.pk)
        # 폼이 검증이 안되면 22번째 줄로 넘어가 에러메세지를 포함한 폼을 보내 템플릿을 렌더링함
    # request가 get이면 빈폼을 생성하고 22번째로 넘어가 템플릿 렌더링
    else:
        form = SignUpForm()
    return render(request, 'account/sign_up.html', {'form': form})

# 로그인
def sign_in(request):
    if request.method == "POST":
        form = SignInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # 폼이 검증되고 입력받은 아이디와 비밀번호가 일치하는 User모델을 user 변수에 저장
            user = auth.authenticate(username=username, password=password)
            print(user)
            # user가 존재하면 로그인을 하고 메인화면으로 넘어감(메인이 구현안되있어 로그인으로 넘어가게 수정함)
            if user:
                auth.login(request, user)
                return redirect('account:user_home', user.pk)
            # 만약 존재하지 않으면 form에 에러메세지를 추가하고 46번째 줄로넘어가 템플릿을 렌더링함
            elif user == None:
                form.add_error(None, '아이디 또는 비밀번호가 올바르지 않습니다.')
    # 방식이 get일때 빈폼을 생성하고 46번째 줄로넘어가 로그인 템플릿을 폼을 포함하여 렌더링한다

    else:
        form = SignInForm()
    return render(request, 'account/sign_in.html', {'form': form})
# @csrf_exempt
# def sign_in(request):
#     if request.method == "POST":
#         form = SignInForm(request.POST)
#         if form.is_valid():
#             username = request.POST['username']
#             password = request.POST['password']
#             # 폼이 검증되고 입력받은 아이디와 비밀번호가 일치하는 User모델을 user 변수에 저장
#             user = auth.authenticate(username=username, password=password)
#             print(password)
#             # user가 존재하면 로그인을 하고 메인화면으로 넘어감(메인이 구현안되있어 로그인으로 넘어가게 수정함)
#             if user:
#                 data = {
#                     'data' : 1,
#                     'user_pk' : user.pk
#                 }
#                 auth.login(request, user)
#                 # return redirect('account:user_home', user.pk)
#                 return HttpResponse(json.dumps(data), content_type='application/json')
#             # 만약 존재하지 않으면 form에 에러메세지를 추가하고 46번째 줄로넘어가 템플릿을 렌더링함
#             else:
#                 data = {
#                     'data' : 2
#                 }
#                 # form.add_error(None, '아이디 또는 비밀번호가 올바르지 않습니다.')
#                 return HttpResponse(json.dumps(data), content_type='application/json')
#     # 방식이 get일때 빈폼을 생성하고 46번째 줄로넘어가 로그인 템플릿을 폼을 포함하여 렌더링한다

#     else:
#         form = SignInForm()
#     return render(request, 'account/sign_in.html', {'form': form})
def user_home(request, user_pk):
    user = request.user
    if user.id == user_pk:
        user = get_object_or_404(User, pk=user_pk)
        user_team = TeamMember.objects.filter(user=user) #팀의 목록을 출력해줄것임!
        team_count = user_team.count()
        team_paginator = Paginator(user_team,8)
        team_page_number = request.GET.get('page',1)
        team_page_obj = team_paginator.get_page(team_page_number)
        form = ScheduleForm(instance=request.user)
        return render(request, 'account/user_home.html', {'user':user, 'user_team':user_team, 'form':form,'count':team_count, 'url_page_obj':team_page_obj})
    
    else: # 현재사용자가 다른 사용자의 홈을 들어갈경우 로그인창으로 돌아가게 함
        return redirect('account:sign_in')

# 로그아웃
def sign_out(request):
    auth.logout(request)
    return redirect('account:sign_in')

# 팀 유저의 개인정보를 보여주는 창
def user_info(request, user_pk):
   user = get_object_or_404(User, pk=user_pk)
   return render(request, 'account/user_info.html', {'user':user})

# 개인정보수정
@login_required
def edit_user(request):
    if request.method =="POST":
        form = userChangeform(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('account:user_home', request.user.pk)
        
    else:
        form = userChangeform(instance=request.user)
    return render(request, 'account/edit_user.html',{'form':form,'user':request.user})

# 시간표 설정
@login_required
def set_schedule(request):
    user = get_object_or_404(User, pk=request.user.id)
    user_team = TeamMember.objects.filter(user=user) #팀의 목록을 출력해줄것임!

    if request.method == "POST":
        form = ScheduleForm(request.POST)
        if form.is_valid():
            user.time_table = form.cleaned_data['time_table']
            user.save()
        return redirect("account:user_home", user.pk)
    else:
        form = ScheduleForm(instance=request.user)
  
def user_team(request, user_pk):
    login_user = request.user
    if login_user.pk == user_pk:
        user = get_object_or_404(User, pk=user_pk)
        user_team = TeamMember.objects.filter(user=user)
        return render(request, 'account/user_team.html',{'user_team':user_team, 'user':user})
    else:
        return redirect("account:user_home", user.pk)
#아이디 중복체크
def overlap_username(request):
    username = request.GET["username"]
    if User.objects.filter(username=username).exists():
        data = 0
        return HttpResponse(json.dumps(data), content_type='application/json')
    data = 1
    return HttpResponse(json.dumps(data), content_type='application/json')
