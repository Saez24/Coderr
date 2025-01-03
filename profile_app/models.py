from django.db import models


class Profile(models.Model):
    # Kann leer sein, bis `pk` zugewiesen wird
    user = models.IntegerField(blank=True, null=True)
    username = models.CharField(max_length=100, default="")
    first_name = models.CharField(max_length=100, default="")
    last_name = models.CharField(max_length=100, default="", blank=True)
    file = models.ImageField(
        upload_to='profile_pictures/', default="", blank=True)
    location = models.CharField(max_length=255, default="", blank=True)
    tel = models.CharField(max_length=20, default="", blank=True)
    description = models.TextField(default="", blank=True)
    working_hours = models.CharField(max_length=50, default="", blank=True)
    type = models.CharField(max_length=20, default="")
    email = models.EmailField(default="")
    created_at = models.DateTimeField(auto_now_add=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.user:
            self.user = self.pk
            super().save(update_fields=['user'])

    def __str__(self):
        return self.username
