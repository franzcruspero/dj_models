from datetime import timedelta, datetime, date

from django.db import models
from django.utils import timezone
from django.utils.encoding import smart_text
from django.utils.text import slugify
from django.utils.timesince import timesince

from django.db.models.signals import pre_save, post_save

from .validators import validate_justin

PUBLISH_CHOICES = (
    ("draft", "Draft"),
    ("publish", "Publish"),
    ("private", "Private")
)


class PostModelQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)
    def post_title_items(self, value):
        return self.filter(title__icontains=value)

class PostModelManager(models.Manager):
    def get_queryset(self):
        return PostModelQuerySet(self.model, using=self._db)

    def all(self, *args, **kwargs):
        # qs = super(PostModelManager, self).all(*args, **kwargs).active()  #filter(active=True)
        # print(qs)
        qs = self.get_queryset().active()
        return qs


class Post(models.Model):
    active = models.BooleanField(default=True)
    title = models.CharField(
        max_length=240, 
        verbose_name="Post title", 
        unique=True,
        error_messages={
            "unique": "This title is not unique, please try again.",
            "blank": "This field is not full, please try again."
        },
        help_text="Must be a unique title.")
    slug = models.SlugField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    publish = models.CharField(max_length=120, choices=PUBLISH_CHOICES, default="draft")
    view_count = models.IntegerField(default=0)
    publish_date = models.DateField(auto_now=False, auto_now_add=False, default=timezone.now)
    author_email = models.EmailField(max_length=240, validators=[validate_justin], null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = PostModelManager()
    other = PostModelManager()

    def save(self, *args, **kwargs):
        # if not self.slug:
        #     self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    class Meta:
        # unique_togeter = [("title", "slug")]
        pass

    def __str__(self):
        return smart_text(f"{self.title}")

    # def age(self):
    #     now = timezone.now()
    #     guessed_age = timesince(self.publish_date)
    #     if guessed_age == "0 minutes":
    #         return "Unknown"
    #     return f"{timesince(self.publish_date)} ago"

    @property
    def age(self):
        if self.publish == "publish":
            now = datetime.now()
            publish_time = datetime.combine(
                self.publish_date,
                datetime.now().min.time()
            )
            try:
                difference = now - publish_time
            except:
                return "Unknown"
            if difference <= timedelta(minutes=1):
                return "Just now."
            return f"{timesince(self.publish_date)} ago"
        return "Not published"

def blog_post_model_pre_save_receiver(sender, instance, *args, **kwargs):
    print("before save")
    if not instance.slug and instance.title:
        instance.slug = slugify(instance.title)

pre_save.connect(blog_post_model_pre_save_receiver, sender=Post)

def blog_post_model_post_save_receiver(sender, instance, created, *args, **kwargs):
    print("after save")
    if not instance.slug and instance.title:
        instance.slug = slugify(instance.title)
        instance.save()

post_save.connect(blog_post_model_post_save_receiver, sender=Post)
