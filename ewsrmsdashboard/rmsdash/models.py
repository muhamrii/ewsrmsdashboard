# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class DbReport(models.Model):
    report_id = models.CharField(max_length=20)
    report_name = models.CharField(max_length=20)
    botid = models.CharField(max_length=50)
    groupid = models.IntegerField()
    list_display = ('report_name', 'bot_id', 'groupid')

    class Meta:
        managed = False
        db_table = 'db_report'
        unique_together = (('id', 'report_id', 'botid'),)

class TbCpuRamLoad(models.Model):
    timeid = models.DateTimeField(primary_key=True)
    servername = models.CharField(max_length=5)
    memload = models.FloatField(blank=True, null=True)
    cpuload = models.FloatField(blank=True, null=True)
    sshstatus = models.CharField(max_length=2)

    class Meta:
        managed = False
        db_table = 'tb_cpu_ram_load'
        unique_together = (('timeid', 'servername'),)


class TbDiskCapacity(models.Model):
    timeid = models.DateTimeField(primary_key=True)
    servername = models.CharField(max_length=20)
    filesystem = models.CharField(max_length=50)
    size = models.CharField(max_length=20, blank=True, null=True)
    used = models.CharField(max_length=20, blank=True, null=True)
    avail = models.CharField(max_length=20, blank=True, null=True)
    percentageusage = models.IntegerField(blank=True, null=True)
    mounted = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'tb_disk_capacity'
        unique_together = (('timeid', 'servername', 'mounted'),)


class TbInodesUsage(models.Model):
    timeid = models.DateTimeField(primary_key=True)
    servername = models.CharField(max_length=20)
    filesystem = models.CharField(max_length=50)
    inodestotal = models.IntegerField(blank=True, null=True)
    used = models.IntegerField(blank=True, null=True)
    inodesfree = models.IntegerField(blank=True, null=True)
    percentageiusage = models.IntegerField(blank=True, null=True)
    mounted = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'tb_inodes_usage'
        unique_together = (('timeid', 'servername', 'mounted'),)


class TbServer(models.Model):
    servername = models.CharField(max_length=20)
    ipaddress = models.CharField(max_length=20)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    port = models.IntegerField()
    list_display = ('servername','ipaddress', 'username')

    def __str__(self):
        return self.servername

    class Meta:
        managed = False
        db_table = 'tb_server'
        unique_together = (('id', 'servername'),)
