from django.contrib import admin
from .models import NewUser
from .models import FAQ
from .models import About

admin.site.register(NewUser)
admin.site.register(FAQ)
admin.site.register(About)
