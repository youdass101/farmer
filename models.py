# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('FarmerUser', models.DO_NOTHING)
    action_flag = models.PositiveSmallIntegerField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class FarmerHarvest(models.Model):
    date = models.DateField()
    output = models.IntegerField()
    tray = models.ForeignKey('FarmerTray', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'farmer_harvest'


class FarmerMedium(models.Model):
    name = models.CharField(max_length=255)
    soil = models.IntegerField()
    coco = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'farmer_medium'


class FarmerOld(models.Model):
    id = models.IntegerField(blank=True, null=True)
    start = models.TextField(blank=True, null=True)
    medium_weight = models.IntegerField(blank=True, null=True)
    seeds_weight = models.IntegerField(blank=True, null=True)
    medium_id = models.IntegerField(blank=True, null=True)
    name_id = models.IntegerField(blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    fname = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'farmer_old'


class FarmerPlant(models.Model):
    name = models.CharField(max_length=255)
    seeds = models.IntegerField()
    pressure = models.IntegerField()
    blackout = models.IntegerField()
    harvest = models.IntegerField()
    output = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'farmer_plant'


class FarmerTray(models.Model):
    start = models.DateTimeField()
    medium_weight = models.IntegerField()
    seeds_weight = models.IntegerField()
    medium = models.ForeignKey(FarmerMedium, models.DO_NOTHING)
    name = models.ForeignKey(FarmerPlant, models.DO_NOTHING)
    number = models.IntegerField()
    fname = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'farmer_tray'


class FarmerUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'farmer_user'


class FarmerUserGroups(models.Model):
    user = models.ForeignKey(FarmerUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'farmer_user_groups'
        unique_together = (('user', 'group'),)


class FarmerUserUserPermissions(models.Model):
    user = models.ForeignKey(FarmerUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'farmer_user_user_permissions'
        unique_together = (('user', 'permission'),)
