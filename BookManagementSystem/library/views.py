from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Book, UserTable, UserProfile
from django.contrib.auth.models import User
from .forms import AddUpdateBook
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .permissions import allowed_users

# Create your views here.

def start(request):
    return redirect('/home')

def home(request):
    user_profile=None
    if request.user.is_authenticated:
         user_profile = UserProfile.objects.get(user_id=request.user.id)
    return render(request, 'library/index.html', context={'user_profile':user_profile})

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def go_to_admin(request):
    return redirect('/admin')


def explore(request):
    book = Book.objects.all()
    user_profile=None
    group = None
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user_id=request.user.id)
    
    if request.user.groups.exists():
            group = request.user.groups.all()[0].name
            group = group            
    context={'book':book, 'group':group, 'user_profile':user_profile}
    return render(request, 'library/explore.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def delete_book(request, id):
    book = Book.objects.get(id=id)
    book.delete()
    messages.success(request, 'Book was sucessfully deleted!')
    return redirect('/explore')

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def add_book(request):
    if request.method == 'POST':
        form = AddUpdateBook(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            bookname = form.cleaned_data.get('book_name')
            author = form.cleaned_data.get('author')
            messages.success(request, f'A Book named {bookname} whose author {author}, was added successfully!')
            return redirect('/explore')
    else:
        form = AddUpdateBook()
    
    context = {
        'form':form,
    }
    return render(request, 'library/add.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def update_book(request, id):
    book = Book.objects.get(id=id)
    print(request.POST)
    if request.method == 'POST':
        form = AddUpdateBook(request.POST or None,request.FILES or None, instance=book)
        if form.has_changed():
            if form.is_valid():
                form.save()
                messages.success(request,  'Book was updated successfully! ')
                messages.info(request, 'The following fields changed: %s.' % ", ".join(form.changed_data) )
                return redirect('/explore')
        else:
            messages.success(request,  'No changes made!')
            return redirect('/explore')
    else:
        form = AddUpdateBook(instance=book)

    context = {
        'form':form,
        'book':book,
    }
    return render(request, 'library/update.html', context)

def explore_filter(request, id):
    group = None
    if request.user.groups.exists():
            group = request.user.groups.all()[0].name
            group = group

    if id == 'high-to-low':
        book = Book.objects.order_by('-price')
    
    elif id == 'low-to-high':
        book = Book.objects.order_by('price')
    
    elif id == 'A to Z':
        book = Book.objects.order_by('author')
    
    elif id == 'Z to A':
        book = Book.objects.order_by('-author')

    elif id == 'Edited':
        book = Book.objects.filter(book_type='Edited').order_by('book_name', 'author')

    elif id == 'Reference':
        book = Book.objects.filter(book_type='Reference').order_by('book_name', 'author')

    elif id == 'Fictious':
        book = Book.objects.filter(book_type='Fictious').order_by('book_name', 'author')

    elif id == 'Non-Fictious':
        book = Book.objects.filter(book_type='Non-Fictious').order_by('book_name', 'author')

    elif id == 'search':
        search_value = request.GET['search']
        q1 = Q(book_name__startswith=search_value)
        q2 = Q(author__startswith=search_value)
        q3 = Q(book_type__startswith=search_value)
        q4 = Q(book_name__icontains=search_value)
        q5 = Q(author__icontains=search_value)
        q6 = Q(book_type__icontains=search_value)
        book = Book.objects.filter(q1|q2|q3|q4|q5|q6)
        return render(request, 'library/explore.html', {'book':book, 'search_value':search_value, 'group':group})
    
    return render(request, 'library/explore.html', {'book':book, 'group':group})


def no_permission(request):
    return render(request, 'library/reject.html')

# Functions for user-table pages.

@login_required(login_url='login')
def user_table(request):
    user = User.objects.get(id=request.user.id)
    user_table = user.usertable_set.all()
    user_profile = UserProfile.objects.get(user_id=request.user.id)
    context = {
        'user':user, 'user_table':user_table, 'user_profile':user_profile
    } 
    return render(request, 'library/user-table.html', context)

@login_required(login_url='login')
def add_book_to_userlist(request, id):
    user_table = UserTable(book_id=id, customer_id=request.user.id)
    user_table.save()
    messages.success(request, "Book was sucessfully added to your list.")
    return redirect('/explore')

@login_required(login_url='login')
def delete_from_userlist(request, id):
    user_table = UserTable.objects.get(id=id)
    user_table.delete()
    messages.success(request, "Book was removed from your table sucessfully!")
    return redirect('/user-table')

@login_required(login_url='login')  
def update_status(request, id, status):
    user_table = UserTable.objects.get(id=id)
    if status == 'Pending':
        user_table.status = 'Over'
        user_table.save()
        name = request.user.get_full_name().title()
        messages.success(request, f'Congratulations {name}! you have achieved a great milestone. Keep it up.')
        return redirect('/user-table')
    else:
        user_table.status = 'Pending'
        user_table.save()
        return redirect('/user-table')

def user_table_filter(request, filter):
    user_table =None
    id = request.user.id
    
    if filter == 'pending':
        user_table =  UserTable.objects.filter(customer_id=id, status='Pending')

    elif filter == 'over':
        user_table =  UserTable.objects.filter(customer_id=id, status='Over', )

    return render(request, 'library/user-table.html', {'user_table':user_table})
    
    
    
