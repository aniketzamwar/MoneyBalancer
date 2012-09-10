from django.contrib import admin
from balance.bal.models import Transaction, Balancer, Comments, Frelation

admin.site.register(Transaction)
admin.site.register(Balancer)
admin.site.register(Comments)
admin.site.register(Frelation)
