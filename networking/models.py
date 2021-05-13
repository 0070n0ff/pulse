from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save
import ipaddress

class MyModel(models.Model):
    name = models.CharField("Name", max_length=150)
    created_at = models.DateTimeField("created", auto_now_add=True)
    updated_at = models.DateTimeField("updated", auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.PROTECT, blank=True)
    is_active = models.BooleanField("is_Active", default=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True

"""
 #   def save(self, *args, **kwargs):
 #       if not self.id:
 #           self.created_at = timezone.now()
 #       self.updated_at = timezone.now()
 #       return super(User, self).save(*args, **kwargs)
   """


class Customer(MyModel):
    description = models.TextField("Description", blank=True)
    address = models.TextField("Address", blank=True)
    email = models.CharField("E-mail", max_length=250, blank=True)


class DevType(MyModel):
    description = models.TextField("Description", blank=True)


# RG
class RegGate(MyModel):
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, blank=True)
    address = models.TextField("Address", blank=True)
    description = models.TextField("Description", blank=True)


# Network
class Network(MyModel):
    LOCAL = []
    for x in range(1, 31):
        LOCAL.append((x, '/' + str(x)))

    cidr = models.PositiveIntegerField("CIDR", choices=LOCAL, default=24)
    rg = models.ManyToManyField(RegGate, blank=True)
    type = models.ForeignKey(DevType, on_delete=models.CASCADE, blank=True)
    #parent = models.ForeignKey("self", on_delete=models.PROTECT, blank=True)

    def __str__(self):
        return "%s/%s - %s, %s" % (self.name, self.cidr.__str__(), self.rg.name, self.type.name)

    def tostr(self):
        return "%s/%s" % (self.name, self.cidr.__str__())

    class Meta:
        verbose_name = "Network"
        verbose_name_plural = "Network"




# ip-address
class IPAddr(MyModel):
    dns_name = models.CharField("DNS name", max_length=15, default="blank")
    netw = models.ForeignKey(Network, on_delete=models.PROTECT, blank=True)
    def __str__(self):
        return "%s (%s)" % (self.name, self.dns_name)

    class Meta:
        verbose_name = "IPAddr"
        verbose_name_plural = "IPAddr"
#PC
class PC(MyModel):
    SN = models.CharField("S/N", max_length=32, blank=True)
    type = models.ForeignKey(DevType, on_delete=models.PROTECT, blank=True)
    master = models.ForeignKey(Customer, on_delete=models.PROTECT, blank=True)


class SW(MyModel):
    SN = models.CharField("S/N", max_length=32, blank=True)
    type = models.ForeignKey(DevType, on_delete=models.PROTECT, blank=True)
    master = models.ForeignKey(Customer, on_delete=models.PROTECT, blank=True)


class NetPCInt(MyModel):
    net_obj = models.ForeignKey(PC, on_delete=models.CASCADE)
    mac = models.CharField("MAC:", max_length=25, blank=True)
    ip = models.ForeignKey(IPAddr, on_delete=models.CASCADE,blank=True)
    #ip = models.ManyToManyField(IPAddr,blank=True, related_name="ipaddr")

    def __str__(self):
        return "%s (%s) : %s" % (self.net_obj.name, self.name, self.ip.name)


class NetSWInt(MyModel):
    net_obj = models.ForeignKey(SW, on_delete=models.CASCADE)
    mac = models.CharField("MAC:", max_length=25, blank=True)
    ip = models.ForeignKey(IPAddr, on_delete=models.CASCADE,blank=True)

    def __str__(self):
        return "%s (%s) : %s" % (self.net_obj.name, self.name, self.ip.name)

@receiver(post_save, sender=Network)
def create_ip_addr(sender, instance:Network, created, **kwargs):
     if created:

        subnet = ipaddress.ip_network(instance.tostr())

        for ipn in subnet.hosts():
            ip1=IPAddr(name=ipn, dns_name="blank", owner=instance.owner, netw=instance)
            ip1.save()
