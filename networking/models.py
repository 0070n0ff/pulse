from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class MyModel(models.Model):
    name = models.CharField("Name", max_length=150)
    created_at = models.DateTimeField("created",auto_now_add=True)
    updated_at = models.DateTimeField("updated",auto_now=True)
    owner = models.ForeignKey(User,on_delete=models.CASCADE,default=User)
    is_active = models.BooleanField("is_Active", default=True)

    def __str__(self):
        return self.name

#    def save(self,*args,**kwargs):
 #       if not self.id:
  #          self.created_at = timezone.now()
   #     self.updated_at = timezone.now()
    #    return super(User,self).save(*args,**kwargs)

    class Meta:
        abstract = True

class Customer(MyModel):
    description = models.TextField("Description")
    address = models.TextField("Address")
    email = models.CharField("E-mail", max_length=250)



class DevType(MyModel):

    description = models.TextField("Description")







#RG
class RegGate(MyModel):

    customer = models.ForeignKey(Customer,on_delete=models.PROTECT)
    address = models.TextField("Address")
    description = models.TextField("Description")

#Network
class Network(MyModel):
    net_name = models.CharField("Network", max_length=15)
    LOCAL = []
    for x in range(1,31):
        f=str(x)
        LOCAL.append((x,'/'+f))
    cidr = models.PositiveIntegerField("CIDR", choices=LOCAL,default=24)
    rg = models.ManyToManyField(RegGate)
    type = models.ForeignKey(DevType,on_delete=models.CASCADE)

    def __str__(self):
        return "%s/%s - %s" % (self.net_name, self.cidr, self.type)

    class Meta:
        verbose_name = "Network"
        verbose_name_plural = "Network"


#ip-address
class IPAddr(MyModel):
    net = models.ForeignKey(Network,on_delete=models.PROTECT)
    dns_name = models.CharField("DNS name", max_length=15)

    def __str__(self):
        return "%s (%s)" % (self.name,self.dns_name)


class PC(MyModel):
    SN = models.CharField("S/N", max_length=32)
    type = models.ForeignKey(DevType, on_delete=models.PROTECT)
    master = models.ForeignKey(Customer, on_delete=models.PROTECT)


class SW(MyModel):
    SN = models.CharField("S/N", max_length=32)
    type = models.ForeignKey(DevType,on_delete=models.PROTECT)
    master = models.ForeignKey(Customer, on_delete=models.PROTECT)

class NetPCInt(MyModel):
    net_obj = models.ForeignKey(PC,on_delete=models.CASCADE)
    mac = models.CharField("MAC:", max_length=25)
    ip = models.ManyToManyField(IPAddr,blank=True)
    def __str__(self):
        return "%s (%s)" % (self.net_obj.name, self.name)

class NetSWInt(MyModel):
    net_obj = models.ForeignKey(SW,on_delete=models.CASCADE)
    mac = models.CharField("MAC:", max_length=25)
    ip = models.ManyToManyField(IPAddr,blank=True)

    def __str__(self):
        return "%s (%s)" % (self.net_obj.name, self.name)
