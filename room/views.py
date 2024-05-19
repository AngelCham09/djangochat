from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Room, Message, ChatImage
from .forms import RoomForm
from django.contrib import messages
# Create your views here.

from .serializers import ChatImageSerializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

@login_required
def rooms(request):
    rooms = Room.objects.all()

    return render(request, 'room/rooms.html', {'rooms': rooms})


@login_required
def addRooms(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room_name = form.cleaned_data['name']
            if Room.objects.filter(name__iexact=room_name).exists():
                messages.error(request, 'Room with this title already exists.')
                return render(request, 'room/addRooms.html', {'form': form})
            else:
                room = form.save()
                return render(request, 'room/room.html', {'room': room})
        else:
            return render(request, 'room/addRooms.html', {'form': form})
    else:
        form = RoomForm()

    return render(request, 'room/addRooms.html', {'form': form})

@login_required
def room(request, slug):
    room = Room.objects.get(slug=slug)
    messages = Message.objects.filter(room=room)[0:25]

    return render(request, 'room/room.html', {'room': room, 'messages': messages})


class ChatImageApiView(APIView):
    def get(self, request, *args, **kwargs):
        images = ChatImage.objects.all()
        serializer = ChatImageSerializer(images, context = {'request':request}, many=True )
        return Response(serializer.data, status= status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        serializer = ChatImageSerializer(data=request.data)
        if serializer.is_valid():
            image_instance = serializer.save()
            return Response({'id': image_instance.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
