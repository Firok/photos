from django.db import models
from django.utils import timezone
from stdimage import StdImageField


class TimestampedModel(models.Model):
    """
    Abstract model for adding created and updated timestamps.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Photo(TimestampedModel):
    """
    A model that represents photo 
    """
    # user
    user = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE)

    # photo
    photo = StdImageField(upload_to='photos/', variations={
        'large': (1000, 1000),
        'thumbnail': (100, 100, True)
    }, delete_orphans=True)

    # caption
    caption = models.CharField(max_length=255)

    # When the photo is published. If None it means the photo is
    # unpublished.
    published_at = models.DateTimeField(
        blank=True,
        null=True)

    class Meta:
        verbose_name = 'Photo'
        verbose_name_plural = 'Photos'

    def publish(self):
        self.published_at = timezone.now()
        self.save(update_fields=['published_at'])
