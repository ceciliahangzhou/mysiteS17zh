from django.contrib import admin
from  .models import Author, Book, Course, Student, Topic


# Register your models here.
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'numpages',]

class StudentAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name']
    #TODO

admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Course)
admin.site.register(Student)
admin.site.register(Topic)
