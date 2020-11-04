from django.db import models
from django.utils.text import slugify

from apps.authentication.models import User
from apps.common.utils import base_concrete_model


class Slugged(models.Model):
    slug = models.SlugField(max_length=255)

    def save(self, *args, **kwargs):
        """
        Generate new slug if it is missing
        """
        if not self.slug:
            self.slug = self.generate_unique_slug()
        super(Slugged, self).save(*args, **kwargs)

    def generate_unique_slug(self):
        """
        Create a unique slug by passing the result of get_slug() to utils.urls.unique_slug.
        """
        concrete_model = base_concrete_model(Slugged, self)
        slug_qs = concrete_model.objects.exclude(id=self.id)
        return self.unique_slug(slug_qs, self.get_slug())

    def unique_slug(self, queryset, slug):
        """
        Ensures a slug is unique for the given queryset, appending an integer to its end until the slug is unique.
        """
        index = 2
        unique_slug = slug
        while queryset.filter(slug=unique_slug).exists():
            unique_slug = f"{slug}-{index}"
            index += 1
        return unique_slug

    def get_slug(self):
        """
        Allows subclasses to implement their own slug creation logic.
        """
        attr = "title"
        return slugify(getattr(self, attr, None))

    class Meta:
        abstract = True


class Ownable(models.Model):
    """
    Abstract model that provides ownership of an object for a user.
    """
    user = models.ForeignKey(to=User, verbose_name="Creator", on_delete=models.SET_NULL, null=True)

    class Meta:
        abstract = True

    def is_editable(self, request):
        """
        Restrict in-line editing to the objects's owner and superusers.
        """
        return request.user.is_superuser or request.user.id == self.user_id
