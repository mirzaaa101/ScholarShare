from django.contrib import admin
from .models import NewUser
from .models import FAQ
from .models import About
from .models import Message
from .models import LoanRequest
from .models import DonationRequest

admin.site.register(NewUser)
admin.site.register(FAQ)
admin.site.register(About)
admin.site.register(Message)
admin.site.register(LoanRequest)
admin.site.register(DonationRequest)

