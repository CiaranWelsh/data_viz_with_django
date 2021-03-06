# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    last_name = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Dct(models.Model):
    index = models.IntegerField(blank=True, null=True)
    cell_line = models.TextField(blank=True, null=True)
    replicate = models.IntegerField(blank=True, null=True)
    gene = models.TextField(blank=True, null=True)
    treatment = models.TextField(blank=True, null=True)
    time = models.FloatField(blank=True, null=True)
    value = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dct'


class DjangoAdminLog(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    action_flag = models.PositiveSmallIntegerField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
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


class Mean(models.Model):
    index = models.IntegerField(blank=True, primary_key=True)
    cell_line = models.TextField(blank=True, null=True)
    gene = models.TextField(blank=True, null=True)
    treatment = models.TextField(blank=True, null=True)
    time = models.FloatField(blank=True, null=True)
    value = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mean'


class PcaDct(models.Model):
    index = models.IntegerField(blank=True, primary_key=True)
    # sample = models.TextField(db_column='Sample', blank=True, null=True)  # Field name made lowercase.
    cell_id = models.TextField(blank=True, null=True)
    replicate = models.IntegerField(blank=True, null=True)
    treatment = models.TextField(blank=True, null=True)
    time_point = models.FloatField(blank=True, null=True)
    # treatment_start_date = models.TextField(db_column='Treatment Start Date', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    # sub_experiment = models.IntegerField(blank=True, null=True)
    filename = models.TextField(db_column='Filename', blank=True, null=True)  # Field name made lowercase.
    cell_line = models.TextField(blank=True, null=True)
    pc1 = models.FloatField(db_column='0', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    pc2 = models.FloatField(db_column='1', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    pc3 = models.FloatField(db_column='2', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.

    class Meta:
        managed = False
        db_table = 'pca_dct'


class PcaDctExplainedVar(models.Model):
    index = models.IntegerField(blank=True, primary_key=True)
    number_0 = models.FloatField(db_column='0', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.

    class Meta:
        managed = False
        db_table = 'pca_dct_explained_var'


class Sem(models.Model):
    index = models.IntegerField(blank=True, primary_key=True)
    cell_line = models.TextField(blank=True, null=True)
    gene = models.TextField(blank=True, null=True)
    treatment = models.TextField(blank=True, null=True)
    time = models.FloatField(blank=True, null=True)
    value = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sem'


class Std(models.Model):
    index = models.IntegerField(blank=True, primary_key=True)
    cell_line = models.TextField(blank=True, null=True)
    gene = models.TextField(blank=True, null=True)
    treatment = models.TextField(blank=True, null=True)
    time = models.FloatField(blank=True, null=True)
    value = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'std'
