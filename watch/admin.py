from django.contrib import admin
from .models import Neighbourhood,Profile,Business,Posts,Join,Comments

# Register your models here.
admin.site.register(Neighbourhood)
admin.site.register(Profile)
admin.site.register(Business)
admin.site.register(Join)
admin.site.register(Posts)
admin.site.register(Comments)