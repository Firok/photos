from rest_framework.routers import SimpleRouter
from django.urls import path
from . import views

router = SimpleRouter()
router.register(
    prefix=r'photos',
    viewset=views.PhotoViewSet,
    base_name='photos'
)

urlpatterns = [path('photos/batch_publish/',
                    views.BatchPublishPhotoView.as_view(),
                    name='batch_publish'),
               path('photos/batch_edit/',
                    views.BatchEditPhotoView.as_view(),
                    name='batch_edit'),
               path('photos/batch_delete/',
                    views.BatchDeletePhotoView.as_view(),
                    name='batch_delete')] + router.urls
