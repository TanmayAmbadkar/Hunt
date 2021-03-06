from django.shortcuts import render
from rest_framework.response import Response
from api.models import *
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from rest_framework.views import APIView
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
import json
from datetime import datetime, timedelta
import pytz
from django.core import serializers
from django.utils import timezone

# Create your views here.
def get_posts(request):

    results = Post.objects.all()
    jsondata = serializers.serialize('json', results)
    return HttpResponse(jsondata)


class HomeView(TemplateView):

    template_name = 'api/home.html'

class RulesView(TemplateView):

    template_name = 'api/rules.html'

class LevelView(LoginRequiredMixin, TemplateView):

    template_name = 'api/level.html'

    def get_context_data(self, **kwargs):

        context = super(LevelView, self).get_context_data(**kwargs)
        student = Student.objects.get(user=self.request.user)
        level = student.current_level
        context['level'] = level
        context['student'] = student
        if student.attempt_time_stamp is not None:
            diff = timezone.now() - student.attempt_time_stamp
            seconds = diff.seconds + diff.days*86400
            if student.attempts>7 and seconds<60:
                context['banned']=1
            elif student.attempts>7 and seconds>60:
                student.attempts = 0
                student.save()
        return context

    def post(self, request):

        student = Student.objects.get(user=request.user)
        level = student.current_level

        if request.POST['answer'].casefold() == level.answer.casefold():

            if(datetime.now()<datetime(2021, 2, 20, 18, 0, 0, 0) and not student.first_year):
                student.score+=level.score
                student.time_stamp = datetime.now()
#datetime.now()<datetime(2021, 2, 21, 23, 59, 59, 0)
#datetime.now()>=datetime(2021, 2, 20, 0, 0, 0, 0)
            elif datetime.now()<datetime(2021, 2, 21, 12, 0, 0, 0) and student.first_year:
                student.score+=level.score
                student.time_stamp = datetime.now()
            try:
                student.current_level = Level.objects.get(level_number = level.level_number+1)
            except Level.DoesNotExist:
                student.finish=1
            print(student.current_level)
            print(student.score)
            student.save()

        else:
            if student.attempt_time_stamp is not None:
                diff = timezone.now() - student.attempt_time_stamp
                seconds = diff.seconds + diff.days*86400
                if seconds<60:
                    student.attempts+=1

                else:
                    student.attempt_time_stamp = timezone.now()
                    student.attempts=1

                if student.attempts > 7:
                    student.attempt_time_stamp = timezone.now() + timedelta(seconds=60*student.banned)
                    student.banned+=1

                student.save()
            else:
                student.attempt_time_stamp = timezone.now()
                student.attempts=1

                student.save()

        return HttpResponseRedirect("/level")

class LeaderboardView(TemplateView):

    template_name="api/leaderboard.html"

    def get_context_data(self, **kwargs):

        context = super(LeaderboardView, self).get_context_data(**kwargs)
        seniors = list(Student.objects.filter(first_year=False).order_by('-score', 'time_stamp'))
        juniors = list(Student.objects.filter(first_year=True).order_by('-score', 'time_stamp'))
        for i in range(len(seniors)):
            seniors[i].position=i+1
        for i in range(len(juniors)):
            juniors[i].position=i+1

        context['seniors']=seniors
        context['juniors']=juniors

        return context

class RegistrationAPI(APIView):

    def get(self, request):

        username = request.GET.get('username');
        try:
            User.objects.get(username=username)
            return JsonResponse(status=200, data={"message":"error"})
        except User.DoesNotExist:
            return JsonResponse(status=200, data={"message":"gg"})


    def post(self, request):
        data = json.loads(request.body)
        print(data)
        otpcode = data['code']
        rollno = data['rollno']
        first_name = data['firstname']
        last_name = data['lastname']
        email = data['email']
        username = data['username']
        password = data['password']
        fy = data['fy']
        fy = fy==1

        c = code(username)
        if c!=otpcode:
            return JsonResponse(status=400, data={"message":"code invalid"})

        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
        user.save()
        student = Student(user=user, roll_number=rollno, code=otpcode, current_level=Level.objects.get(level_number=1), first_year=fy)
        student.save()
        return JsonResponse(status=200, data={"message":"successfull"})


def code(username):

    sum=0
    for i in username:
        sum+=ord(i)
    a = 2310433
    c = 2342201
    m = 2147483648
    x = (a * sum + c) % m
    return x
