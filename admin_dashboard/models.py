from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class AdminActionLog(models.Model):
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_actions')
    action = models.CharField(max_length=200)
    details = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.admin.username} - {self.action} - {self.created_at}"