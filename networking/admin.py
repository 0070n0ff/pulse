from django.contrib import admin
from .models import NetPCInt,NetSWInt,Customer,RegGate,IPAddr,PC,SW,DevType,MyModel,Network

# Register your models here.

admin.site.register(Network)
admin.site.register(NetSWInt)
admin.site.register(NetPCInt)
admin.site.register(Customer)
admin.site.register(RegGate)
admin.site.register(IPAddr)
admin.site.register(PC)
admin.site.register(SW)
admin.site.register(DevType)





