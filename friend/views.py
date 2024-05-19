from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from core.models import Profile
from django.contrib.auth.models import User

from friend.friend_request_status import FriendRequestStatus
from .models import FriendRequest, FriendList
from django.http import HttpResponse
import json
from friend.utils import get_friend_request_or_false

@login_required
def friends(request):
    user = request.user
    #get own friend list
    try: 
        friend_list = FriendList.objects.get(user=user)
    except FriendList.DoesNotExist:
        friend_list = FriendList(user=user)
        friend_list.save()

    my_friends = friend_list.friends.all()

    #get all list
    if 'q' in request.GET:
        q = request.GET.get('q')
        friends = Profile.objects.filter(user__is_superuser=False, user__username__icontains=q).exclude(user=user).select_related('user')
    else:
        friends = Profile.objects.filter(user__is_superuser=False).exclude(user=user).select_related('user')
    friend_list = []

    # 5 cases: 
    # is_me(already filter), is_friend, send_request, them_sent_request_to_you(you need accept/reject), you_send_request_to_them(can cancel request)
    is_friend = False
    request_sent = FriendRequestStatus.NO_REQUEST_SENT.value
    pending_friend_reqest_id = -1
    for friend in friends:
        if my_friends.filter(pk=friend.user.id):
            is_friend = True
        else: 
            is_friend = False
            #THEM_SENT_TO_YOU = 0
            if get_friend_request_or_false(sender=friend.user, receiver=user) != False:
                request_sent = FriendRequestStatus.THEM_SENT_TO_YOU.value
                pending_friend_reqest_id = get_friend_request_or_false(sender=friend.user, receiver=user).id
               #YOU_SENT_TO_THEM = 1 
            elif get_friend_request_or_false(sender=user, receiver=friend.user) != False:
                request_sent = FriendRequestStatus.YOU_SENT_TO_THEM.value
            else:
                #NO_REQUEST_SENT = -1
                request_sent = FriendRequestStatus.NO_REQUEST_SENT.value

        friend_data = {
            'friend_profile': friend,
            'is_friend': is_friend,
            'request_sent': request_sent,
            'pending_friend_reqest_id': pending_friend_reqest_id,
        }
        friend_list.append(friend_data)
    
    
    context = {'friends': friend_list}
    return render(request, 'friend/friends.html', context)


@login_required
def send_friend_request(request, *args, **kwargs):
    user = request.user
    payload = {}
    if request.method == 'POST':
        user_id = request.POST.get("receiver_user_id")
        if user_id:
            receiver = User.objects.get(pk=user_id)
            try:
                friend_requests = FriendRequest.objects.filter(sender=user, receiver=receiver)
                try:
                    for request in friend_requests:
                        if request.is_active:
                            raise Exception("You already sent them a friend request.")
                        
                    #if none are active
                    friend_requests = FriendRequest(sender=user, receiver=receiver)
                    friend_requests.save()
                    payload['result'] = "success"
                    payload['response'] = "Friend request sent."
                except Exception as e:
                    payload['result'] = "error"
                    payload['response'] = str(e)
            except FriendRequest.DoesNotExist:
                friend_requests = FriendRequest(sender=user, receiver=receiver)
                friend_requests.save()
                payload['result'] = "success"
                payload['response'] = "Friend request sent."

            if payload['response'] == None:
                payload['result'] = "error"
                payload['response'] = "Something went wrong."
        else:
            payload['result'] = "error"
            payload['response'] = "Unable to send a frind request."
    else:
        payload['result'] = "error"
        payload['response'] = "Unable to send a frind request."

    return HttpResponse(json.dumps(payload), content_type="application/json")


@login_required
def accept_friend_request(request, *args, **kwargs):
    user = request.user
    payload = {}
    if request.method == 'POST':
        friend_request_id = request.POST.get("friend_request_id")
        if friend_request_id:
            friend_request = FriendRequest.objects.get(pk=friend_request_id)
            if friend_request.receiver == user and friend_request.is_active == True:
                friend_request.accept()
                payload['result'] = "success"
                payload['response'] = "Friend request accepted."
            else:
                payload['result'] = "error"
                payload['response'] = "There is no request to accept."
        else:
            payload['result'] = "error"
            payload['response'] = "Unable to accept that frind request."  
    else:
        payload['result'] = "error"
        payload['response'] = "Unable to accept that frind request."

    return HttpResponse(json.dumps(payload), content_type="application/json")

@login_required
def reject_friend_request(request, *args, **kwargs):
    user = request.user
    payload = {}
    if request.method == 'POST':
        friend_request_id = request.POST.get("friend_request_id")
        if friend_request_id:
            friend_request = FriendRequest.objects.get(pk=friend_request_id)
            if friend_request.receiver == user and friend_request.is_active == True:
                friend_request.decline()
                payload['result'] = "success"
                payload['response'] = "Friend request rejected."
            else:
                payload['result'] = "error"
                payload['response'] = "There is no request to reject."
        else:
            payload['result'] = "error"
            payload['response'] = "Unable to reject that frind request."  
    else:
        payload['result'] = "error"
        payload['response'] = "Unable to reject that frind request."

    return HttpResponse(json.dumps(payload), content_type="application/json")

@login_required
def unfriend_request(request, *args, **kwargs):
    user = request.user
    payload = {}
    if request.method == 'POST':
        unfriend_user_id = request.POST.get("unfriend_user_id")
        if unfriend_user_id:
            try:
               removee = User.objects.get(pk=unfriend_user_id)
               friend_list = FriendList.objects.get(user=user)
               friend_list.unfriend(removee)
               payload['result'] = "success"
               payload['response'] = "Unfriend Successfully."
            except Exception as e:
                payload['result'] = "error"
                payload['response'] = f"Somthing went wrong: {str(e)}"
               
        else:
            payload['result'] = "error"
            payload['response'] = "Unable to unfriend."  
    else:
        payload['result'] = "error"
        payload['response'] = "Unable to unfriend."

    return HttpResponse(json.dumps(payload), content_type="application/json")


@login_required
def cancel_friend_request(request, *args, **kwargs):
    user = request.user
    payload = {}
    if request.method == 'POST':
        cancel_friend_user_id = request.POST.get("cancel_friend_user_id")
        if cancel_friend_user_id:
            cancel_user = User.objects.get(pk=cancel_friend_user_id)
            try:
                friend_request = FriendRequest.objects.filter(sender=user,   receiver=cancel_user, is_active=True)
                if len(friend_request) > 1:
                    for request in friend_request:
                        request.cancel()
                else:
                    friend_request.first().cancel()

                payload['result'] = "success"
                payload['response'] = "Unfriend Successfully."
            except Exception as e:
                payload['result'] = "error"
                payload['response'] = f"Somthing went wrong: {str(e)}"
               
        else:
            payload['result'] = "error"
            payload['response'] = "Unable to cancel friend request."  
    else:
        payload['result'] = "error"
        payload['response'] = "Unable to cancel friend request."

    return HttpResponse(json.dumps(payload), content_type="application/json")


