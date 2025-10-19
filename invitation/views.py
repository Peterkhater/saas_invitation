from django.shortcuts import render


def invitation_create(request):
    return render(request,'invitation/get_invitation.html',{})