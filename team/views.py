from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from account.models import User
from django.utils import timezone
from .models import Team, TeamMember, TeamTimeTable, TeamChat
from django.contrib.auth.decorators import login_required
from .forms import TeamForm, AddForm
from django.core.paginator import Paginator

import simplejson as json

# Create your views here.

# 2진 데이터를 or로 비교
def or_gate(a, b):      
    result = ""
    for i in range(len(a)):
        if (a[i] == b[i]) and a[i] == '0':
            result += '0'
        else:
            result += '1'

    return result

# 2진 데이터를 not으로 변환
def not_gate(binary):
    result = ""
    for i in binary:
        if i == '1':
            result += '0'
        else:
            result += '1'
    return result

# or게이트와 not게이트를 이용해서 팀에 소속된 유저들의 시간표를 각각 비교해서 원하는 이진데이터를 구함
def get_time_table(team_id):
    team = get_object_or_404(Team, pk=team_id)
    team_members = team.members.all()
    result_time_table = team_members[0].time_table
    for member in team_members[1:]:
        result_time_table = or_gate(result_time_table, member.time_table)

    return not_gate(result_time_table)

@login_required
def detail_team(request, team_id):
   details = get_object_or_404(Team, pk=team_id)
   user = request.user
   user_team = TeamMember.objects.filter(user=user)
   team_member = TeamMember.objects.filter(team=details)
   team_time_table = TeamTimeTable.objects.filter(team=details)
   team_chat = TeamChat.objects.filter(team=details)
   for i in TeamMember.objects.filter(team__pk=details.pk):
      if i.user.pk == user.pk:         
         return render(request, 'team/detail_team.html',{
            'details': details, 
            'team_member':team_member,
            'user':user, 
            'user_team':user_team,
            'team_chat':team_chat,
             })
   
   return redirect('account:user_home', login_user.pk)
   
@login_required
def create_team(request):
   # user = get_object_or_404(User, pk=user_id)
    user = request.user
    data = 0
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            team = form.save()
            TeamMember.objects.create(team=team, user=user)
         # team.members.add(user)
            team.team_leader.add(user)
            team.team_name = form.cleaned_data['team_name']
            team.introduce = form.cleaned_data['introduce']
            team.created_date = timezone.now()
            team.save()
            return redirect('team:detail_team', team.pk)
    # else:
    form = TeamForm()
    return render(request, 'team/create_team.html', {'form': form,'user':user})

@login_required
def add_member(request, team_id):
    team1 = get_object_or_404(Team, pk=team_id)
    login_user = request.user
   
    if request.method == 'POST':
        form = AddForm(request.POST)
        if form.is_valid():
            member = form.save(commit=False)
            member.team = team1 #팀에대한 정보를 가져와 TeamMember의 team 에다가 저장을 하고.
            if User.objects.filter(username=form.cleaned_data['username']):
                member.user = User.objects.get(username=form.cleaned_data['username']) #해당유저에 대한 데이터를 가져오고
                if TeamMember.objects.filter(team=team1, user=member.user).count()>0: #해당 팀에 user가 이미 존재해 있는 경우
                    return HttpResponse('해당사용자가 팀에 존재합니다!')
               
                else: # 해당 팀에 user가 존재하지 않는다면 멤버로 추가
                    tm = TeamMember(team=team1, user=member.user) 
                    tm.save()
                    return redirect('team:detail_team', team_id)
            else:
                return HttpResponse('해당 사용자가 존재하지 않습니다!')
    else:
        for i in TeamMember.objects.filter(team__pk=team1.pk):
            if i.user.pk == login_user.pk: 
                form = AddForm()
                return render(request, 'team/add_member.html', {'form':form})
        return redirect('account:uset_home', login_user.pk)

def add_member1(request, team_pk):
    team = get_object_or_404(Team, pk=team_pk)
    user = request.user
    member = TeamMember()
    invite_username = request.GET['username']
    if User.objects.filter(username=request.GET['username']).count() >0 : #해당 유저 정보가 전체 유저 중에 있을 때 
        invite_user = User.objects.get(username=invite_username)

        if TeamMember.objects.filter(team=team, user=invite_user): # 해당 유저가 팀에 있을 경우
            data = 1
            return HttpResponse(json.dumps(data), content_type='application/json')
            
        else: # 해당 유저가 팀에 없을 경우
            data = 2
            member.team = team
            member.user = invite_user
            member.save()
            return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        data = 3
        return HttpResponse(json.dumps(data), content_type='application/json')


@login_required
def expulsion_member(request, team_id, user_id):  # 어느 팀에서 몇번 째 유저를 삭제할지.
    login_user = request.user
    team = get_object_or_404(Team, pk=team_id)  # 어느 팀 객체인지 가져오고
    user = get_object_or_404(User, pk=user_id)  # 어느 유저 객체인지 가져온 다음에
    delete_member = TeamMember.objects.filter(team=team, user=user)  # 외래키 설정 되어있는 team과 user 에 각각을 매칭 시켜주기
    delete_member.delete()
    return redirect('team:detail_team', team_id)

@login_required
def leave_team(request, team_pk, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    team = get_object_or_404(Team, pk=team_pk)
    leave = TeamMember.objects.filter(team=team, user=user)
    leave.delete()
    if TeamMember.objects.filter(team__team_name=team.team_name).count() != 0: # 팀 멤버들이 존재한다면!
        if team.team_leader == user:
            if Team.objects.filter(team_leader__pk=user_pk): # 
                next_leader = TeamMember.objects.filter(team__team_name=team.team_name).first()
                leader = get_object_or_404(User, pk=next_leader.user.pk)
                team.team_leader.set([leader])
                team.save()
                return redirect('account:user_home', user_pk)
            return HttpResponse('리더 위임 실패')
        else:
            return redirect('account:user_home', user_pk)
    else:
        team.delete()
        return redirect('account:user_home', user_pk)

def edit_team(request, team_pk):
   team = get_object_or_404(Team, pk=team_pk)
   user = request.user
   if request.method == "POST":
      form = TeamForm(request.POST)
      if form.is_valid():
         team.team_name = form.cleaned_data['team_name']
         team.introduce = form.cleaned_data['introduce']
         team.team_photho_url = form.cleaned_data['team_photo_url']
         team.save()
         return redirect('team:detail_team',team_pk)
   else:
      teamform = TeamForm(instance=team)
      return render(request, 'team/create_team.html', {'teamform':teamform})
    
def add_time_table(request, team_pk):
    team = get_object_or_404(Team, pk=team_pk)
    user = request.user
    data = TeamTimeTable.objects.filter(team=team, user=user).count()
    if data > 0:
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        ttt = TeamTimeTable(team=team, user=user, total_time_table=user.time_table)
        ttt.time = timezone.now()
        ttt.save()
        return HttpResponse(json.dumps(data), content_type='application/json')


def delete_time_table(request, team_pk):
    team = get_object_or_404(Team, pk=team_pk)
    user = request.user
    delete_time_table = TeamTimeTable.objects.filter(team=team, user=user)
    data = 0
    if TeamTimeTable.objects.filter(team=team, user=user):
        data = 1  #시간표가 팀 시간에 등록되어있을 경우
        delete_time_table.delete()
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        data = 2
        return HttpResponse(json.dumps(data), content_type='application/json')

def team_user_timetable(request, team_pk):
    team = get_object_or_404(Team, pk=team_pk)
    user_team = TeamMember.objects.filter(team=team)
    member_time_table = TeamTimeTable.objects.filter(team=team)
    user = request.user
    user_time_table =  TeamTimeTable.objects.filter(team=team, user=user)
    return render(request, "team/teamtimetable.html",{'user_team':member_time_table, 'user':user, 'team':team,'time':user_time_table})

def team_meeting_place(request):
    return render(request, "team/team_meeting_place.html")

def all_team_member(request, team_pk):
    team = get_object_or_404(Team, pk=team_pk)
    user_team = TeamMember.objects.filter(team=team)
    return render(request, "team/all_team_member.html", {'user_team':user_team, 'team':team})

def team_chat(request, team_pk):
    user = request.user
    team = get_object_or_404(Team, pk=team_pk)
    data = 0
    chat = TeamChat()
    chat.team = team
    chat.user = user
    chat.message = request.GET['message']
    if chat.message == "":
        context = {'team_pk': team_pk,'data': data,}
        return HttpResponse(json.dumps(context), content_type='application/json')
    else:
        data = 1
        context = {'team_pk': team_pk,'data': data,}
        chat.send_message = timezone.now()
        chat.save()
        # return redirect('team:detail_team', team_pk)
        return HttpResponse(json.dumps(context), content_type='application/json')

def team_chat_delete(request, team_pk):
    team = get_object_or_404(Team, pk = team_pk)
    chat = TeamChat.objects.filter(team=team)
    chat.delete()
    return redirect('team:detail_team', team.pk)