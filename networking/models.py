from django.db import models




#Company
class Company(models.Model):

    name = models.CharField("Name", max_length=150)
    description = models.TextField("Description")
    address = models.TextField("Address")
    email = models.CharField("E-mail", max_length=250)
    is_active = models.BooleanField("is_Active", default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Company"



#Place
class Place(models.Model):

    address = models.TextField("Address")
    code = models.CharField("Code", max_length=100)
    description = models.TextField("Description")
    company = models.ManyToManyField(Company, verbose_name="Company", related_name="place_company")
    is_active = models.BooleanField("is_Active", default=True)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = "Place"
        verbose_name_plural = "Place"





#Network
class Network(models.Model):
    network = models.CharField("Network", max_length=15)
    mask = models.CharField("Mask", max_length=15)
    cidr = models.PositiveIntegerField("CIDR", default=24)
    pl = models.ForeignKey(Place, on_delete=models.PROTECT)

    def __str__(self):
        return "%s/%s" % (self.network, self.cidr)

    class Meta:
        verbose_name = "Network"
        verbose_name_plural = "Network"

#Net_Obj
class NetObj(models.Model):
    dns_name = models.CharField("DNS name", max_length=15)
    ip_address = models.CharField("IP-address", max_length=15)
    network = models.ForeignKey(Network, on_delete=models.PROTECT)

    def __str__(self):
        return self.ip_address

    class Meta:
        verbose_name = "Net_Obj"
        verbose_name_plural = "Net_Obj"


#Dev_PC
class DevObjPC(models.Model):
    sn = models.CharField("S/N", max_length=100)
    cpu_model = models.CharField("CPU model", max_length=100)
    cpu_core_c = models.PositiveIntegerField("Core count", default=1)

    def __str__(self):
        return self.sn

    class Meta:
        verbose_name = "DevObjPC"
        verbose_name_plural = "DevObjPC"

#Dev_PC_INT

class DevObjPCInt(models.Model):
    name = models.CharField("Name", max_length=100)
    desc = models.CharField("Desc", max_length=100)
    pc = models.ForeignKey(DevObjPC, on_delete=models.PROTECT)
    ip = models.ManyToManyField(NetObj, verbose_name="Net_Obj",related_name="PC_Net_Obj")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "DevObjPCInt"
        verbose_name_plural = "DevObjPCInt"


        
#Dev_SW
class DevObjSW(models.Model):
    sn = models.CharField("S/N", max_length=100)
   

    def __str__(self):
        return self.sn

    class Meta:
        verbose_name = "DevObjSW"
        verbose_name_plural = "DevObjSW"

#Dev_SW_INT

class DevObjSWInt(models.Model):
    name = models.CharField("Name", max_length=100)
    desc = models.CharField("Desc", max_length=100)
    pc = models.ForeignKey(DevObjSW, on_delete=models.PROTECT)
    ip = models.ManyToManyField(NetObj, verbose_name="Net_Obj",related_name="SW_Net_Obj")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "DevObjSWInt"
        verbose_name_plural = "DevObjSWInt"
