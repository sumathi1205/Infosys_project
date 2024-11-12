from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm




def home(request):
    return render(request, 'home.html')


def login(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == "POST":
        un = request.POST['username']
        pw = request.POST['password']
        user = authenticate(request, username=un, password=pw)

        if user is not None:
            return redirect('/profile')
        else:
            msg = 'Error in login. Invalid username/password'
            form = AuthenticationForm()
            return render(request, 'login.html', {'form': form, 'msg': msg})
    else:
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})


def register(request):
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            un = form.cleaned_data.get('username')
            pw = form.cleaned_data.get('password1')
            user = authenticate(username=un, password=pw)
            return redirect('/Login')
        else:
            return render(request, 'register.html', {'form': form})
    else:
        form = UserCreationForm()
        return render(request, 'register.html', {'form': form})





from django.shortcuts import render
from django.core.files.uploadedfile import InMemoryUploadedFile
import base64

def profile(request):
    if request.method == "POST" and "abo_image" in request.FILES:
        # Get the uploaded file
        abo_image = request.FILES["abo_image"]
        
        # Convert the uploaded image to a Base64 string
        if isinstance(abo_image, InMemoryUploadedFile):
            image_data = abo_image.read()
            base64_image = base64.b64encode(image_data).decode("utf-8")
            mime_type = abo_image.content_type
            img_url = f"data:{mime_type};base64,{base64_image}"
        else:
            img_url = None

        # Pass the Base64-encoded image URL to the template
        return render(request, "profile.html", {"img": img_url})

    return render(request, "profile.html", {"img": None})






