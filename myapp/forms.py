from django import forms
from django.contrib.auth.forms import UserCreationForm
from myapp.models import Topic, Student

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['subject', 'intro_course', 'time', 'avg_age',]
        widgets = {'time': forms.RadioSelect(),}
        labels = {'avg_age': u'What is your age?', 'intro_course': u'This should be an introductory level course',
               'time': u'Preferred Time',}

class InterestForm(forms.Form):
    interest = forms.TypedChoiceField(widget=forms.RadioSelect, coerce=int, choices=((1, 'Yes'),(0, 'No')))
    age = forms.IntegerField(initial=20)
    comments = forms.CharField(widget=forms.Textarea, label='Additional Comments')

class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Student
        fields = ['username', 'first_name', 'last_name', 'email', 'address', 'city', 'province', 'age']


