import uuid
from django.db import models
from django.contrib.auth.models import User

STATUS = {
    'O': 'open',
    'C' : "Close"
}

class Ticket(models.Model):
    name = models.CharField(max_length=255)
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=STATUS, default="O")
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class TicketReply(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    reply = models.TextField()

    def __str__(self):
        return self.reply