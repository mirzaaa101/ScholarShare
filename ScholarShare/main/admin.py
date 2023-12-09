from django.contrib import admin
from .models import NewUser
from .models import FAQ
from .models import About
from .models import Message
from .models import LoanRequest
from .models import DonationRequest
from .models import Comment
from .models import AddBalance
from .models import AddDonation
from .models import Report

admin.site.register(NewUser)
admin.site.register(FAQ)
admin.site.register(About)
admin.site.register(Message)
admin.site.register(LoanRequest)
admin.site.register(DonationRequest)
admin.site.register(Comment)
admin.site.register(AddBalance)
admin.site.register(AddDonation)
admin.site.register(Report)

