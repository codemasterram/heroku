from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.contrib import messages
from django.contrib import auth
from todos.models import Todo 
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from todos.serializers import TodoSerializer
from rest_framework import generics


from .utils import redirect_back



class TodoListView(generics.ListCreateAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer



def index(request):
    items=[]
    filter=None
    # tags=[]
    if request.user.is_authenticated:
        filter = request.GET.get('filter')
        print(filter)
        items = filter_results(request.user, filter)
    return render(request, 'index.html', {

        'items': items,
        'filter':filter

        })
class TodoItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer


def filter_results(user,filter):
    if filter == 'completed':
        return Todo.objects.filter(
            user=user,
            completed=True).order_by('-created_at')
    elif filter=='pending':
        return Todo.objects.filter(user=user,completed=False).order_by('-created_at')
    else:
        return Todo.objects.filter(user=user).order_by('-created_at','-completed')

def hastagg(request,id):



    return render(request,'hastagg.html')

@login_required
def create(request):
    return render(request, 'create.html', {
    'form_type': 'create'     
    })

@login_required
def save(request):
    user=request.user
    # Get the form data from the request.
    title = request.POST.get('title')
    description = request.POST.get('description')
    completed = True if (request.POST.get('completed') == 'True') else False


    if title is None or title.strip() == '':
        messages.error(request, 'Item not saved. Please provide the title.')
        return redirect_back(request)



    # Get hidden form data.
    form_type = request.POST.get('form_type')
    id = request.POST.get('id')

    print('Form type received:', form_type)
    print('Form todo id received:', id)
    print('Form todo completed received:', completed)

    if form_type == 'create':
        # Create a new todo item with the data.
        todo = Todo.objects.create(
            user=user,
            title=title,
            description=description,
            created_at=timezone.now(),
            completed=completed
        )
        print('New Todo created: ', todo.__dict__)
        
    elif form_type == 'edit' and id.isdigit():
        todo = Todo.objects.get(pk = id)
        print('Got todo item: ', todo.__dict__)

        # Save logic
        todo.title = title
        todo.description = description
        todo.completed = completed

        todo.save()
        print('Todo updated: ', todo.__dict__)
    messages.info(request , 'Todo Item Saved')
    # Redirect back to index page
    return redirect('index')

@login_required
def edit(request, id):

        print('Received Id: ' + str(id))

        # Fetch todo item by id
        todo = Todo.objects.get(pk = id)
        print('Got todo item: ', todo.__dict__)
        if request.user.id==todo.user.id or request.user.username=='admin': # here edit url works for admin also

            return render(request, 'create.html', {
                'form_type': 'edit',
                'todo': todo
            })
        else:
            messages.error(request, 'You are not authorised to edit this item')
            return redirect('index')
@login_required
def remove(request, id):
    todo = Todo.objects.get(pk = id)
    
    if request.user.id==todo.user.id or request.user.username=='admin': # here edit url works for admin also:
    # Fetch todo item by id
        
        todo.delete()

        return redirect('index')
    else:
        messages.error(request, 'You are not authorised to Delete this item')
        return redirect('index')

def about(request):
    return render(request, 'about.html')

def login(request):
    return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    messages.info(request,'You are out of the page') 
    return redirect('index')
  
def submission(request):
    #get the data from the form
    userr = request.POST.get('username')
    passs = request.POST.get('password')

    #todo: login 
    user =auth.authenticate(request,
        username=userr,
        password=passs)

    if not user :
        messages.info(request,'Login Failed') 
        return redirect_back(request)

    #if authentication was successful
    auth.login(request,user)
    print('ligin was successful')

    messages.info(request,'login successful')    
    return redirect('index')
def signup(request):
    return render(request, 'signup.html')


def signupdetails(request):
    username = request.POST.get('username')
    firstname = request.POST.get('firstname')
    lastname = request.POST.get('lastname')
    password = request.POST.get('password')
    email = request.POST.get('email')

    
    if User.objects.filter(username=username).exists():
        messages.info(request,'Username already exists!!')
        return redirect_back(request)

    if User.objects.filter(email=email).exists():
        messages.info(request,'Email already exists!!')
        return redirect_back(request)


    User.objects.create_user(
        username= username,
        password=password,
        first_name=firstname,
        last_name=lastname,
        email=email

    )
    messages.info(request,'Sing Up Successful!! You may now login!!')
    return render(request, 'login.html')
    

    # check = User.objects.get(username=userr)
    # if check:
    #     messages.info(request,'Username already exists!!')
    #     return redirect(request.META.get('HTTP_REFERER'))
    # user = User.objects.create_user(userr,email,password) 
    # user.first_name = firstname
    # user.last_name = lastname
    # user.save()
    # messages.info(request,'singup successful')
    # return render(request, 'login.html')
    
        
    # user =auth.authenticate(request,
    #     username=userr,
    #     email=email)
    # print(user)
    # if user :
    #     messages.info(request,'Username already exists!!')
    #     return redirect(request.META.get('HTTP_REFERER'))
        
    # else:
    #     userrr = User.objects.create_user(userr,email,password) 
    #     userrr.first_name = firstname
    #     userrr.last_name = lastname
    #     userrr.save()
    #     messages.info(request,'singup successful')
    #     return render(request, 'login.html')
        

    




