from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from .models import Mail
from account.models import User
from .forms import MailForm
from django.utils import timezone
# Create your views here.

def send_mail(request, from_id):
    from_user = get_object_or_404(User, pk=from_id)
    if request.method == 'POST':
        form = MailForm(request.POST)
        if form.is_valid():
            mail = form.save(commit=False)
            mail.from_user = from_user
            if User.objects.filter(username=form.cleaned_data['username']):
                mail.to_user = User.objects.get(username=form.cleaned_data['username'])
                mail.created_data = timezone.now()
                mail.modified_data = timezone.now()
                mail.save()
                return redirect('main:home')
            else:
                return HttpResponse('사용자가 없습니다.')
    else:
        form = MailForm()
        return render(request, 'mail/send_mail.html', {'form': form})


def mailbox(request, user_id):
    mails = get_object_or_404(User, pk=user_id)
    mail_count = Mail.objects.filter(to_user__username=mails.username).count()
    return render(request, 'mail/mailbox.html', {'mails': mails, 'mail_count': mail_count})

def delete_mail(request, mail_id):
    mail = get_object_or_404(Mail, pk=mail_id)
    mail.delete()
    return redirect('main:home')

def detail_mail(request, mail_id):
    mails = get_object_or_404(Mail, pk=mail_id)
    return render(request, 'mail/detail_mail.html', {'mails': mails})