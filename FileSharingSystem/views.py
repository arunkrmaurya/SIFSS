from django.shortcuts import render , redirect
from django.contrib import messages
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate , login ,logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import boto3
from django.conf import settings
from file_app.models import uplodfiles
import os

s3_client=boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,region_name=settings.AWS_S3_REGION_NAME)



def generate_presigned_url(bucket_name, object_name, expiration=604800):
    """Generate a presigned URL for file download."""
    try:
        url = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket_name, "Key": object_name},
            ExpiresIn=min(expiration, 604800)  # Ensure it doesn't exceed 7 days
        )
        return url
    except Exception as e:
        print("Error generating pre-signed URL:", e)
        return None


@login_required(login_url='login')
def file_list(request):
    """View to display uploaded files with search functionality."""
    query = request.GET.get("searching", "").strip()  # Get search input
    user_files = uplodfiles.objects.filter()

    # Apply search filter if query exists
    if query:
        user_files = user_files.filter(file_name__icontains=query)  # Case-insensitive search

    # Generate pre-signed URLs for each file
    files = []
    for file in user_files:
        presigned_url = generate_presigned_url(
            settings.AWS_STORAGE_BUCKET_NAME, f"uploads/{request.user.username}/{file.file_name}"
        )
        files.append({
            "file_name": file.file_name,
            "file_size": file.file_size,
            "file_type": file.file_type,
            "uploaded_at": file.uploaded_at,
            "presigned_url": presigned_url
        })

    return render(request, "file_list.html", {"user_files": files, "search_query": query})

    
@login_required(login_url='login')
def upload_files(request):
    if request.method=='POST' and request.FILES.get('file') and request.POST.get('fname') and request.POST.get('types'):
      file=request.FILES.get('file')
      file_name=request.POST.get('fname')
      file_size=file.size
      file_type=request.POST.get('types')
    #   /creating the Buket to store the file
      bucket_name = settings.AWS_STORAGE_BUCKET_NAME
      s3_file_path = f"uploads/{request.user.username}/{file_name}"
    #   uploding the file in my s3 buket
      s3_client.upload_fileobj(file, bucket_name, s3_file_path)
    #   creating URL of uploded for downlod
      file_url = generate_presigned_url("my-secure-file-bucket", s3_file_path)


        # Save file metadata in MySQL (AWS RDS)
      uplodfiles.objects.create(
          user=request.user,
          file_name=file_name,
          file_size=file_size,
          file_type=file_type,
          file_url=file_url)
      return redirect('home')
    return render(request,'home.html')


   

@login_required(login_url='login')
def homepage(request):
    user_files = uplodfiles.objects.filter(user=request.user)
    return render(request,'home.html',{'user_files':user_files})
def loginpage(request):
    try:
       if request.method=="POST":
          username=request.POST.get('uname')
          password=request.POST.get('passw')
          if not User.objects.filter(username=username).exists():
             messages.error(request,'Invalid Crdential!!')
             return redirect('login')
          user = authenticate(username=username, password=password)
          if user is None:
           messages.error(request,'Inavlid Password')
           return redirect('login')
          else:
            login(request,user)
            print(user)
            return redirect('home')
    except:
       pass
    return render(request,'login.html')
def registerpage(request):
    # Check if the HTTP request method is POST (form submission)
    if request.method == 'POST':
        username = request.POST.get('uname')
        email = request.POST.get('email')
        password = request.POST.get('passw')
        
        # Check if a user with the provided username already exists
        user = User.objects.filter(username=username)
        
        if user.exists():
            # Display an information message if the username is taken
            messages.info(request, "Username already taken!")
            return redirect('register')
        
        # Create a new User object with the provided information
        user = User.objects.create_user(username=username, email=email, password=password)

        
        # Display an information message indicating successful account creation
        messages.info(request, "Account created Successfully!")
        return redirect('login')
    return render(request, 'register.html')
def logout_page(request):
    logout(request)
    return redirect('login')


   