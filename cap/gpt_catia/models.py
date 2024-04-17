from django.db import models

class Log(models.Model):
    app = models.TextField(null=False)  # Service used, feedback, language, skill, etc.
    enduser = models.TextField(null=False)  # User whose conversation it is
    sess = models.TextField(null=False)  # Session of the conversation
    msg = models.TextField(null=False)  # Stored message
    speaker = models.TextField(null=False)  # Origin of the message
    ts = models.DateTimeField(auto_now_add=True,null=True)  # Timestamp with timezone
