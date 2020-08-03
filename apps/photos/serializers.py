from rest_framework import serializers

from .models import Photo


class PhotoSerializer(serializers.ModelSerializer):
    """
    Serializer for Photo model
    """

    class Meta:
        model = Photo
        fields = '__all__'


class BatchPublishSerializer(serializers.Serializer):
    """
     Serializer for batch Photo upload
    """
    ids = serializers.ListField(
        child=serializers.IntegerField(), required=True)


class BatchEditSerializer(serializers.Serializer):
    """
     Serializer for batch Photo edit
    """
    id = serializers.IntegerField(required=True)
    caption = serializers.CharField(required=True)


class BatchDeleteSerializer(serializers.Serializer):
    """
     Serializer for batch Photo delete
    """
    ids = serializers.ListField(
        child=serializers.IntegerField(), required=True)
