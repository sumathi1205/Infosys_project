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
import cv2
import numpy as np

def profile(request):
    blood_type = "Unknown"
    contour_length = None
    Rh_factor = "Unknown"
    if request.method == "POST" and "abo_image" in request.FILES:
        # Get the uploaded file
        abo_image = request.FILES["abo_image"]
        
        # Convert the uploaded image to a Base64 string
        if isinstance(abo_image, InMemoryUploadedFile):
            image_data = abo_image.read()
            base64_image = base64.b64encode(image_data).decode("utf-8")
            mime_type = abo_image.content_type
            img_url = f"data:{mime_type};base64,{base64_image}"
             # Convert image data to OpenCV format for processing
            np_image = np.frombuffer(image_data, np.uint8)
            cv_image = cv2.imdecode(np_image, cv2.IMREAD_COLOR)
  

            if cv_image is not None:
                # Convert to grayscale
                gray_img = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
                # Apply Gaussian blur
                blur_img = cv2.GaussianBlur(gray_img, (5, 5), 0)
                # Enhance contrast
                enhance_img = cv2.equalizeHist(blur_img)
                # Thresholding with Otsu's method
                _, bin_img = cv2.threshold(enhance_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

                # Morphological operations
                kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
                bin_img = cv2.morphologyEx(bin_img, cv2.MORPH_OPEN, kernel)
                bin_img = cv2.morphologyEx(bin_img, cv2.MORPH_CLOSE, kernel)
                
                hei,wid = bin_img.shape
                mid_wid = wid//3

                region_A = bin_img[0:mid_wid]
                region_B = bin_img[mid_wid:2*mid_wid]
                region_D = bin_img[2*mid_wid:]

                def cal_agg(region):
                    num_labels,labels,stats,var = cv2.connectedComponentsWithStats(region,connectivity=8)
                    return num_labels-1
                
                num_region_A = cal_agg(region_A)
                num_region_B = cal_agg(region_B)
                num_region_D = cal_agg(region_D)

                print(num_region_A,num_region_B,num_region_D)

                if num_region_D > 0:
                    rh_factor = "Positive"
                else:
                    rh_factor = "Negative"

                # Determine blood type
                if num_region_A > 0 and num_region_B == 0:
                    blood_type = "A"
                elif num_region_A == 0 and num_region_B > 0:
                    blood_type = "B"
                elif num_region_A > 0 and num_region_B > 0:
                    blood_type = "AB"
                elif num_region_A == 0 and num_region_B == 0:
                    blood_type = "O"
                else:
                    blood_type = "Unknown"

                # Convert processed image back to Base64
                _, buffer = cv2.imencode('.png', bin_img)
                processed_img_data = base64.b64encode(buffer).decode("utf-8")
                processed_img_url = f"data:image/png;base64,{processed_img_data}"
            else:
                processed_img_url = "Error: Could not process the image."

        else:
            img_url = None

        # Pass the original and processed image to the template
        return render(request, "profile.html", {
            "img": img_url,
            "processed_img": processed_img_url,
            "blood_type": blood_type,
            "rh_factor": rh_factor
        })

    return render(request, "profile.html", {"img": None, "processed_img": None, "blood_type": None, "rh_factor": None})


