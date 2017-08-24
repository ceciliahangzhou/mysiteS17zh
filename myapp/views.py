from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from myapp.models import Author, Book, Course, Topic
from myapp.forms import TopicForm, InterestForm,RegisterForm
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from datetime import datetime


# Create your views here.

# def index(request):
#     # courselist = Course.objects.all() [:10]
#     Authorlist = Author.objects.all().order_by('-birthdate')[:5]
#     response = HttpResponse()
#     heading1 = '<p>' + 'List of Author: ' + '</p>'
#     response.write(heading1)
#     for author in Authorlist:
#         para = '<p>' + str(author) + str(author.birthdate) + '</p>'
#         response.write(para)
#     return response

def index(request):
    courselist = Course.objects.all().order_by('title')[:10]
    return render(request, 'myapp/index.html', {'courselist': courselist})

# use class_based view
class IndexView(View):
    def get(self, request):
        course_list = Course.objects.all()[:10]

        # Deal with cookies
        if request.session.get('last_visit'):
            last_visit_time = request.session.get('last_visit')
            visits = request.session.get('visits', 0)

            # Use seconds instead of days for testing
            if (datetime.now() - datetime.strptime(last_visit_time[:-7], "%Y-%m-%d %H:%M:%S")).seconds > 0:
                request.session['visits'] = visits + 1
                request.session['last_visit'] = str(datetime.now())
        else:
            # this code was never reached, so the session was not being set
            request.session['last_visit'] = str(datetime.now())
            request.session['visits'] = 1
        if request.session.get('visits'):
            count = request.session.get('visits')
        else:
            count = 0
        context = {
                'course_list':course_list,
                'count': count
            }
        return render(request,'myapp/index.html',context)


# def about(request):
#     response = HttpResponse()
#     heading2 = '<p>' + 'This is a Course Listing APP.' + '<p>'
#     response.write(heading2)
#     return response

def about(request):
    return render(request, 'myapp/about.html')


# def detail(request, course_no):
#     titlelist = Course.objects.get(course_no=course_no)
#     response = HttpResponse()
#     heading1 = '<p>' + 'Details' + '<p>'
#     response.write(heading1)
#     response.write(titlelist.course_no)
#     response.write(titlelist.title)
#     response.write(titlelist.textbook)
#     return response

# def detail(request, course_no):
#     titlelist = Course.objects.get(course_no=course_no)
#     return render(request, 'myapp/detail.html', {'title': titlelist})

def detail(request, course_no):
    # course_title = Course.objects.get(course_no = course_no)
    course_title = get_object_or_404(Course, course_no=course_no)
    course_number = course_title.course_no
    textbook = course_title.textbook
    return render(request, 'myapp/detail0.html', {'coursetitle':course_title})
    # return render(request, 'myapp/detail.html', {'coursetitle': course_title})


# use class_based view
class CourseDetailView(View):
    def get(self,request,course_no):
        course = get_object_or_404(Course, course_no=course_no)
        return render(request, 'myapp/detail.html', {'course':course})


def topics(request):
    topiclist = Topic.objects.all()[:10]
    return render(request, 'myapp/topic.html', {'topiclist': topiclist})

def topic_part1(request):
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            return render()
    else:
        form = TopicForm()
        return render(request, 'myapp/topic_part1.html', {'form':form})

# def topic1_part1(request):#test
#     form = InterestForm()
#     return  render(request, 'myapp/topic_part1.html', {'form':form})

def topics_view(request):
    topiclist = Topic.objects.all().order_by("-num_responses")[:10]
    return render(request,'myapp/topic.html', {'topiclist':topiclist})


def addtopic(request):
    topiclist = Topic.objects.all().order_by("-num_responses")
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.num_responses = 1
            topic.save()
            return HttpResponseRedirect(reverse('myapp:topics'))
    else:
        form = TopicForm()
    return render(request, 'myapp/addtopic.html', {'form':form, 'topiclist':topiclist} )

def topicdetail(request, topic_id):
    topic = get_object_or_404(Topic,pk=topic_id)
    if request.method=='POST':
        form = InterestForm(request.POST)
        if form.is_valid():
            # the cleaned_data attribute only creates after validated
            if form.cleaned_data['interested'] == 1:
                #topic = form.save(commit=False)
                num = topic.num_responses
                topic.num_responses += 1
                topic.avg_age = int((form.cleaned_data['age'] + topic.avg_age *num)/(num+1))
                topic.save()
            return HttpResponseRedirect(reverse('myapp:topics'))
    else:
        form = InterestForm()
    return render(request,'myapp/topicdetail.html',{'form':form,'topic':topic})

def register(request):
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            # save form content to database if it is validated
            # stu= Student.objects.create_user(register_form.cleaned_data['username'])
            # stu.set_password(register_form.cleaned_data['password1'])
            register_form.save()
            return HttpResponseRedirect(reverse('myapp:login'))
    else:
        register_form = RegisterForm()
        return render(request,'myapp/register.html',{'register_form':register_form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                #print(request.user.first_name)
                return HttpResponseRedirect(reverse('myapp:index')) #
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        return render(request, 'myapp/login.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse(('myapp:index')))


def mycourses(request):
    course_list = Course.objects.filter(students__username=request.user)
    return render(request,'myapp/mycourses.html',{'course_list': course_list})
