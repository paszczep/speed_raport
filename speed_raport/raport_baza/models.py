# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from datetime import datetime
# from speed_raport.tools.insert import insert_into_database


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
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
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

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
    id = models.BigAutoField(primary_key=True)
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


class ZleceniaRaport(models.Model):
    id = models.CharField(db_column='id', max_length=36, primary_key=True, serialize=False, unique=True)
    # field_timestamp = models.DateTimeField(db_column='_TIMESTAMP', blank=True, null=True)
    field_timestamp = models.CharField(db_column='_TIMESTAMP', blank=True, null=True, max_length=19)
    nr_zlecenia = models.CharField(db_column='NR_ZLECENIA', blank=True, null=True, max_length=50)
    spedytor = models.CharField(db_column='SPEDYTOR', blank=True, null=True, max_length=50)
    opiekun = models.CharField(db_column='OPIEKUN', blank=True, null=True, max_length=50)
    za_miejsce = models.CharField(db_column='ZA_MIEJSCE', blank=True, null=True, max_length=150, verbose_name='Miejsce załadunku')
    za_miasto = models.CharField(db_column='ZA_MIASTO', blank=True, null=True, max_length=50, verbose_name='Miasto załadunku')
    za_kraj = models.CharField(db_column='ZA_KRAJ', blank=True, null=True, max_length=5, verbose_name='Kraj załadunku')
    za_kod = models.CharField(db_column='ZA_KOD', blank=True, null=True, max_length=20, verbose_name='Kod załadunku')
    za_data = models.DateField(db_column='ZA_DATA', blank=True, null=True, verbose_name='Data załadunku')
    wy_data = models.DateField(db_column='WY_DATA', blank=True, null=True, verbose_name='Data wyładunku')
    wy_miejsce = models.CharField(db_column='WY_MIEJSCE', blank=True, null=True, max_length=150, verbose_name='Miejsce wyładunku')
    wy_miasto = models.CharField(db_column='WY_MIASTO', blank=True, null=True, max_length=50, verbose_name='Miasto wyładunku')
    wy_kraj = models.CharField(db_column='WY_KRAJ', blank=True, null=True, max_length=5, verbose_name='Kraj wyładunku')
    wy_kod = models.CharField(db_column='WY_KOD', blank=True, null=True, max_length=20, verbose_name='Miejsce wyładunku')
    trasa = models.CharField(db_column='TRASA', blank=True, null=True, max_length=150)
    opis = models.CharField(db_column='OPIS', blank=True, null=True, max_length=50)
    informacje = models.CharField(db_column='INFORMACJE', blank=True, null=True, max_length=250)
    data_wystawienia_koszt = models.CharField(db_column='DATA_WYSTAWIENIA_KOSZT', blank=True, null=True, max_length=10)
    data_platnosci_koszt = models.CharField(db_column='DATA_PLATNOSCI_KOSZT', blank=True, null=True, max_length=10)
    data_wystawienia_przych = models.CharField(db_column='DATA_WYSTAWIENIA_PRZYCH', blank=True, null=True, max_length=10)
    data_platnosci_przych = models.CharField(db_column='DATA_PLATNOSCI_PRZYCH', blank=True, null=True, max_length=10)
    netto_pln_przych = models.CharField(db_column='NETTO_PLN_PRZYCH', blank=True, null=True, max_length=20)
    netto_pln_koszt = models.CharField(db_column='NETTO_PLN_KOSZT', blank=True, null=True, max_length=20)
    noty_netto_pln = models.CharField(db_column='NOTY_NETTO_PLN', blank=True, null=True, max_length=20)
    saldo_netto = models.CharField(db_column='SALDO_NETTO', blank=True, null=True, max_length=20)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nr_zlecenia


    class Meta:
        managed = True
        db_table = 'zlecenia_raport'

# class Refresh(models.Model):
#     code = models.TextField()
#     was_executed_before = models.BooleanField(default=False)
#
#     def execute(self):
#         insert_into_database()



