from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework import filters, mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.db import transaction
from .exceptions import RequestError
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from .filtersets import PhotoFilter
from .models import Photo
from .serializers import (PhotoSerializer, BatchPublishSerializer,
                          BatchEditSerializer, BatchDeleteSerializer)


class PhotoPagination(PageNumberPagination):
    """
    Class to define the pagination for photo list API
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50


class PhotoViewSet(
        mixins.CreateModelMixin,
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        mixins.DestroyModelMixin,
        viewsets.GenericViewSet):
    """
    Viewset that provides APIs to list, 
    filtering, and sorting photos
    """

    serializer_class = PhotoSerializer
    pagination_class = PhotoPagination
    queryset = Photo.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = PhotoFilter
    ordering_fields = ['published_at']

    @action(methods=['post'], detail=True)
    def publish(self, request, pk):
        """
        API to publish a photo
        """
        photo = self.get_object()
        photo.publish()

        serializer = self.get_serializer(photo)
        return Response(serializer.data)


class BatchPublishPhotoView(APIView):
    """
    API to upload a photo in batch
    """

    def get_serializer(self):
        return BatchPublishSerializer()

    def post(self, request):
        serializer = BatchPublishSerializer(
            data=request.data)
        serializer.is_valid(raise_exception=True)

        photos = []
        try:
            with transaction.atomic():
                for id in serializer.validated_data['ids']:
                    photo = Photo.objects.get(id=id)
                    photo.publish()

                    photos.append(photo)
        except Exception as error:
            raise RequestError(detail=str(error))

        serializer = PhotoSerializer(photos, many=True)

        return Response(serializer.data)


class BatchEditPhotoView(APIView):
    """
    API to edit photos in batch
    """

    def get_serializer(self):
        return BatchEditSerializer()

    def put(self, request):
        serializer = BatchEditSerializer(
            data=request.data, many=True)

        serializer.is_valid(raise_exception=True)

        photos = []
        try:
            with transaction.atomic():
                for item in serializer.validated_data:
                    id = item.get('id')
                    if not id:
                        raise RequestError(detail=dict(id='Id required'))
                    photo = Photo.objects.get(id=id)
                    if 'caption' in item:
                        photo.caption = item['caption']
                        photo.save()

                    photos.append(photo)
        except Exception as error:
            raise RequestError(detail=str(error))

        serializer = PhotoSerializer(photos, many=True)

        return Response(serializer.data)


class BatchDeletePhotoView(APIView):
    """
    API to upload a photo in batch
    """

    def get_serializer(self):
        return BatchDeleteSerializer()

    def post(self, request):
        serializer = BatchDeleteSerializer(
            data=request.data)

        serializer.is_valid(raise_exception=True)

        try:
            with transaction.atomic():
                for id in serializer.validated_data['ids']:
                    photo = Photo.objects.get(id=id)
                    photo.delete()

        except Exception as error:
            raise RequestError(detail=str(error))

        return Response(status=status.HTTP_204_NO_CONTENT)
