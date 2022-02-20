from django.db import models

from django.contrib.auth.models import User


class AppUser(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='app_user'
    )  # user_id, related_name default : appuser
    FCM_token = models.CharField(max_length=100, default=None)

    class Meta:
        db_table = "app_user"

    def __str__(self):
        return f'(username: {self.user.username[:7]}.., id : {self.user.id})'


class Estimate(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='coordinates_id')
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name="Estimate")

    category = models.CharField(max_length=70)
    location = models.CharField(max_length=70)

    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)

    class Meta:
        db_table = 'estimate'

    def __str__(self):
        return f'{self.user} -> (estimate_id: {self.id}, category: {self.category})'
