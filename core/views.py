from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required

from .forms import SignUpForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib import messages


from friend.models import FriendList, FriendRequest

# Create your views here.
def frontpage(request):
    return render(request, 'core/frontpage.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()
            auth.login(request, user)
            return redirect('frontpage')
        else:
            return render(request, 'core/signup.html', {'form': form})
    else:
        form = SignUpForm()

    return render(request, 'core/signup.html', {'form': form})

def logout(request):
    auth.logout(request)
    return redirect('login')

@login_required
def profile(request):
   
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)


    return render(request, 'core/profile.html')

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'core/changePwd.html'
    success_url = reverse_lazy('changePwd')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Your password was successfully changed!')
        return super().form_valid(form)
    
@login_required
def my_friend(request):
    context = {}
    try: 
        friend_list = FriendList.objects.get(user=request.user)
    except FriendList.DoesNotExist:
        friend_list = FriendList(user=request.user)
        friend_list.save()
    
    friends = friend_list.friends.all()
    if 'q' in request.GET:
        q = request.GET.get('q')
        friends = friends.filter(username__icontains=q)
    context['friends'] = friends
    
    return render(request, 'core/myFriend.html', context)

@login_required
def friend_request(request):
    context = {}
    try: 
        if 'q' in request.GET:
            q = request.GET.get('q')
            friend_list = FriendRequest.objects.filter(receiver=request.user, is_active=True, sender__username__icontains=q)
        else:
            friend_list = FriendRequest.objects.filter(receiver=request.user, is_active=True)
    except FriendRequest.DoesNotExist:
        friend_list = []
 
    context['friend_list'] = friend_list
    
    return render(request, 'core/friendRequest.html', context)

