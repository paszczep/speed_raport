# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models, connection
import pandas as pd
from tools.connect import get_raport_baza_engine
import uuid
from datetime import datetime
# from datetime import datetime
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


class Zlecenia(models.Model):
    id = models.CharField(db_column='id', max_length=36, primary_key=True, default=0)
    field_timestamp = models.DateTimeField(db_column='_TIMESTAMP', blank=True, null=True, verbose_name='DODANY')
    # field_timestamp = models.CharField(db_column='_TIMESTAMP', blank=True, null=True, max_length=19)
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

    netto_pln_przych = models.DecimalField(db_column='NETTO_PLN_PRZYCH', max_digits=8, decimal_places=2, blank=True, null=True)
    netto_pln_koszt = models.DecimalField(db_column='NETTO_PLN_KOSZT', max_digits=8, decimal_places=2, blank=True, null=True)
    noty_netto_pln = models.DecimalField(db_column='NOTY_NETTO_PLN', max_digits=8, decimal_places=2, blank=True, null=True)
    saldo_netto = models.DecimalField(db_column='SALDO_NETTO', max_digits=8, decimal_places=2, blank=True, null=True)
    # netto_pln_przych = models.CharField(db_column='NETTO_PLN_PRZYCH', blank=True, null=True, max_length=20)
    # netto_pln_koszt = models.CharField(db_column='NETTO_PLN_KOSZT', blank=True, null=True, max_length=20)
    # noty_netto_pln = models.CharField(db_column='NOTY_NETTO_PLN', blank=True, null=True, max_length=20)
    # saldo_netto = models.CharField(db_column='SALDO_NETTO', blank=True, null=True, max_length=20)

    class Meta:
        abstract = True


class ZleceniaRaport(Zlecenia):
    # id = models.AutoField(primary_key=True)
    # id = models.AutoField(primary_key=True, db_column='id')

    # def create_premie(self):
    #     engine = get_raport_baza_engine()
    #     osoby = str({self.spedytor, self.opiekun}).replace('{', '(').replace('}', ')')
    #     osoby_query = f"""SELECT * FROM "spedytorzy_osoby" WHERE "Osoba" IN {osoby}"""
    #     osoby_df = pd.read_sql_query(osoby_query, con=engine)
    #     print(osoby_df)
    #     spedytor = self.spedytor
    #     opiekun = self.opiekun
    #     saldo_netto = self.saldo_netto
    #     procent = int(1)
    #     premia = saldo_netto * procent
    #
    #     if spedytor == opiekun:
    #         pass

    def save(self, *args, **kwargs):
        engine = get_raport_baza_engine()
        raport_query = f"""SELECT * FROM "zlecenia_raport" WHERE "NR_ZLECENIA" = '{self.nr_zlecenia}'"""
        raport_df = pd.read_sql_query(raport_query, con=engine)
        archive_query = f"""SELECT * FROM "zlecenia_historia" WHERE "NR_ZLECENIA" = '{self.nr_zlecenia}'"""
        archive_df = pd.read_sql_query(archive_query, con=engine)
        new_archive_df = pd.concat([raport_df, archive_df])
        # Patrzę czy nie ma duplikatu zapisywanego rekordu w archiwum
        duplicates_cols = [el for el in new_archive_df.columns if el not in ['_TIMESTAMP', 'id', 'created']]
        new_archive_df.drop_duplicates(subset=duplicates_cols, keep=False, ignore_index=True, inplace=True)
        # Eliminuję wszystkie elementy które już są w archiwum
        existing_ids_list = archive_df['id'].to_list()
        new_archive_df = new_archive_df.loc[~(new_archive_df['id'].isin(existing_ids_list))]
        new_archive_df['created'] = datetime.now()
        new_archive_df['id'] = new_archive_df.apply(lambda _: uuid.uuid4(), axis=1)

        schema_name = 'public'
        table_name = 'zlecenia_historia'
        if len(new_archive_df) > 0:
            new_archive_df.to_sql(name=table_name, con=engine, schema=schema_name, if_exists='append', index=False)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.nr_zlecenia

    class Meta:
        managed = True
        db_table = 'zlecenia_raport'
        verbose_name = 'Zlecenie raport'
        verbose_name_plural = 'Zlecenia raport'


class ZleceniaHistoria(Zlecenia):
    # id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name='ZAPISANY')
    # raport_id = models.CharField(db_column='_id', blank=True, null=True, max_length=36,)

    def __str__(self):
        return self.nr_zlecenia

    class Meta:
        managed = True
        db_table = 'zlecenia_historia'
        verbose_name = 'Zlecenie historia'
        verbose_name_plural = 'Zlecenia historia'


class SpedytorzyOsoby(models.Model):
    osoba = models.CharField(blank=True, null=True, max_length=50, verbose_name='Osoba')
    premia_procent = models.SmallIntegerField(default=0, verbose_name='Procent premii')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    class Meta:
        managed = True
        db_table = 'spedytorzy_osoby'
        verbose_name = 'Osoba'
        verbose_name_plural = 'Osoby'

    def __str__(self):
        return str(self.osoba)


class SpedytorzyPremie(models.Model):
    # id = models.AutoField(primary_key=True)
    add_date = models.DateTimeField(auto_now_add=True, verbose_name='Data dodania')
    zlecenie = models.ForeignKey(ZleceniaRaport, on_delete=models.CASCADE, blank=True, null=True)
    spedytor = models.ForeignKey(SpedytorzyOsoby, on_delete=models.CASCADE, blank=True, null=True)
    kwota_premii = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)

    class Meta:
        managed = True
        db_table = 'spedytorzy_premie'
        verbose_name = 'Premia'
        verbose_name_plural = 'Premie'

    def __str__(self):
        return str(self.spedytor)


