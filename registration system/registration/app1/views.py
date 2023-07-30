from django.shortcuts import redirect, render,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout 
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib import messages
# Create your views here.

@login_required(login_url='login')
#to make it dont go backward
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def HomePage(request):
    if 'username' in request.session:
        return render(request,'home.html')
    else:
           return redirect('login')

def SignupPage(request):
    if 'username' in request.session:
         return redirect('home')

    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if len(pass1)<8:
              messages.error(request,'password must contain atleast 8 characters')

        else:
               if pass1!=pass2:
                     messages.error(request,'password you re-entered is incorrect')
               else:
                     my_user=User.objects.create_user(uname,email,pass1)
                     my_user.save()
                     return redirect('login')
    
        # return HttpResponse("User Has Been Created Successfully !!")
        # print(uname,email,pass1,pass2)


    return render(request,'signup.html')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def LoginPage(request):
    if 'username' in request.session:
           return redirect('home')
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            request.session['username']=username
            return redirect('home')
        else:
            messages.error(request,'user name or password is incorrect')
        
    return render(request,'login.html')

#coming from the urls when calling views.logoutpage    
def LogoutPage(request):
    if 'username' in request.session:
          logout(request)
          request.session.flush()
    return redirect('login')

def NextPage(request):
     return render(request,'next.html')