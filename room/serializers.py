from rest_framework import serializers
from .models import ChatImage

class ChatImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ChatImage
        fields = '__all__'

        def get_photo_url(self, obj):
            request = self.context.get('request')
            photo_url = obj.fingerprint.url
            return request.build_absolute_uri(photo_url)
