from django.db import models

from django.contrib.auth.models import User


class AppUser(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='app_user'
    )  # user_id, related_name default : appuser

    homelike_latitude = models.FloatField(default=0.0)
    homelike_longitude = models.FloatField(default=0.0)
    workingplacelike_latitude = models.FloatField(default=0.0)
    workingplacelike_longitude = models.FloatField(default=0.0)

    class Meta:
        db_table = "app_user"

    def __str__(self):
        return f'(username: {self.user.username[:7]}.., id : {self.user.id})'
