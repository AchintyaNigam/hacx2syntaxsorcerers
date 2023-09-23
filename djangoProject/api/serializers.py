from rest_framework import serializers
from .models import Userinfo, imgr

class UserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=100)
    name = serializers.CharField()
    def create(self, validated_data):
        return Userinfo.objects.create(**validated_data)
    def update(self, instance, validated_data):
        instance.email = validated_data.get('username', instance.username)
        instance.password = validated_data.get('password', instance.password)
        instance.name = validated_data.get('name', instance.name)

        return instance

class ImgSerializer(serializers.ModelSerializer):
    class Meta:
        model = imgr
        fields = '__all__'
