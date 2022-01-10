from django.contrib import admin
from .models import Wallets
from .models import History
# Register your models here.

admin.site.register(Wallets)
admin.site.register(History)