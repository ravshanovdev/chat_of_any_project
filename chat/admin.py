from django.contrib import admin
from .models import Message, ChatSession

admin.site.register([Message, ChatSession])



