from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User,AbstractBaseUser
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib import messages
from django.contrib.auth import authenticate, login , logout   
from ConnectSphere import settings 
from django.core.mail import send_mail, EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str
from .tokens import generate_token
from.models import Post,Postpic
# from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.decorators import login_required




def home(request):
    return render(request,'core/getstart.html')

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname =  request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request, "USER ALREADY EXIST")
            return redirect('signup')
        if User.objects.filter(email=email):
            messages.error(request , "EMAIL ALREADY EXIST")
            return redirect('signup')
        if len(username)>20:
            messages.error(request , "LENGTH OF USERNAME SHOULD BE LESS THAN 20 CHARECTERS")
        if pass1 != pass2:
            messages.error(request, " PASSWORD DIN'T MATCH")
        if not username.isalnum():
            messages.error(request, "USER NAME MUST BE ALPHANUMERIC")
            return redirect('signup')

        myuser = User.objects.create_user(username,email,pass1)

        myuser.first_name = fname 
        myuser.last_name = lname
        myuser.is_active = False

        myuser.save()

        messages.success(request, "your Action has been Successfully created")

        subject = "WELCOME to ConnectSphere"

        message = "HELLO"+ myuser.first_name + "!! \n" +"WELCOME to ConnectSphere!! \n"+"WE HAVE ALSO SENT A CONFIRMATION EMAIL, PLEASE CONFIRM EMAIL ADERESS"

        from_email = settings.EMAIL_HOST_USER

        to_list=[myuser.email]

        send_mail(subject,message,from_email,to_list,fail_silently=True,)

        # Email Address Confirmation Email

        current_site = get_current_site(request)

        email_subject = "confrim your email"

        message2= render_to_string('email_confirmation.html',{
            'name':myuser.first_name,
            'domain': current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token':generate_token.make_token(myuser),

        })

        email= EmailMessage (
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [myuser.email],
        )
        
        email.fail_silently = True
        email.send()


    return render(request,'core/signup.html')

def activate(request,uid64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uid64))
        myuser = User.objects.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        myuser =None 
    if myuser is not None and generate_token.check_token(myuser,token):
        myuser.is_active=True
        myuser.save()
        login(request,myuser)
        return redirect('home')
    else:
        return render(request,'activation_failed.html')
    

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:

            login(request,user)

            fname = user.first_name

            return redirect('getstart')

        else:
            messages.error(request,"add Credentials")
            return redirect('getstart')

    


    return render(request,'core/signin.html')

def getstart(request):
    context={
        'posts':Post.objects.all(),
        'postspic':Postpic.objects.all()
    }
    return render(request,'core/home.html',context)

# class PostListView(ListView):
#     model=Post
#     template_name='core/home.html'
#     context_object_name='posts'
#     ordering=['-date_posted']
#     paginate_by=4

# class UserPostListView(ListView):
#     model=Post
#     template_name='core/users_posts.html'
#     context_object_name='posts' 
#     paginate_by=4
#     def get_queryset(self):
#         user=get_object_or_404(User,username=self.kwargs.get('username'))
#         return Post.objects.filter(author=user).order_by('-date_posted')





#     #<app>/<model>_<viewtype>.html
# class PostDetailView(DetailView):
#     model=Post
    
# class PostCreateView(LoginRequiredMixin,CreateView):
#     model=Post
#     fields=['title','content']
#     def form_valid(self,form):
#         form.instance.author=self.request.user
#         return super().form_valid(form)


# class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
#     model=Post
#     fields=['title','content']
#     def form_valid(self,form):
#         form.instance.author=self.request.user
#         return super().form_valid(form)
#     def test_func(self):
#         post = self.get_object()
#         if self.request.user==post.author:
#            return True
#         return False 

# class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
#     model=Post
#     success_url='/home'
#     def test_func(self):
#         post = self.get_object()
#         if self.request.user==post.author:
#            return True
#         return False

def createpost(request):
    return render(request,'core/post_form.html') 
def createpostpic(request):
    return render(request,'core/pic_post_form.html') 

@login_required(login_url='signin')
def uploadtext(request):
    if request.method == 'POST':
        user = request.user.username
        print(user)
        title=request.POST['title']
        content = request.POST['content']
        new_post = Post.objects.create(user=user, title=title, content=content)
        new_post.save()
        return redirect('/createpost')
    else:
        return redirect('/createpost')
    
@login_required(login_url='signin')
def uploadpic(request):
    if request.method == 'POST':
        user = request.user.username
        print(user)
        title=request.POST['title']
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']
        new_post = Postpic.objects.create(user=user, title=title,image=image, caption=caption)
        new_post.save()
        return redirect('/createpostpic')
    else:
        return redirect('/createpostpic')


