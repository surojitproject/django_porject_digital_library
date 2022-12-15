from django.contrib import admin
from .models import Book, UserTable, UserProfile

# Register your models here.

class BookAdmin(admin.ModelAdmin):
    list_display = ['book_name', 'author', 'book_pic', 'book_type', 'price', 'rating']
    search_fields = ['book_name', 'author', 'book_type']
    list_filter = ['book_name', 'author', 'book_type', 'rating']

class UserTableAdmin(admin.ModelAdmin):
    list_display = ['customer', 'book', 'status']
    search_fields = ['customer', 'book', 'status']
    list_filter = ['customer', 'book', 'status']
    
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'profile_pic']
    
admin.site.register(Book, BookAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserTable, UserTableAdmin)

