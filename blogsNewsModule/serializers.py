from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    """Serializes a post object"""
    class Meta:
        model = Post
        fields = '__all__'
