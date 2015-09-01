from django.db import models


class DEPT(models.Model):
    name = models.CharField(max_length=80, unique=True)
    comment = models.CharField(max_length=160, blank=True, null=True)

    def __unicode__(self):
        return self.name


class UserGroup(models.Model):
    name = models.CharField(max_length=80, unique=True)
    dept = models.ForeignKey(DEPT)
    comment = models.CharField(max_length=160, blank=True, null=True)

    def __unicode__(self):
        return self.name

class Account(models.Model):
    account = models.CharField(max_length=80, unique=True)
    comment = models.CharField(max_length=160, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    group = models.ManyToManyField(UserGroup)
    

    def __unicode__(self):
        return self.account

class Account_group(models.Model):
    account_id = models.CharField(max_length=80, unique=True)
    usergroup_id = models.CharField(max_length=160, unique=True)

    def __unicode__(self):
        return self.id

class User(models.Model):
    USER_ROLE_CHOICES = (
        ('SU', 'SuperUser'),
        ('DA', 'DeptAdmin'),
        ('CU', 'CommonUser'),
    )
    username = models.CharField(max_length=80, unique=True)
    password = models.CharField(max_length=100)
    name = models.CharField(max_length=80)
    email = models.EmailField(max_length=75)
    role = models.CharField(max_length=2, choices=USER_ROLE_CHOICES, default='CU')
    dept = models.ForeignKey(DEPT)
    group = models.ManyToManyField(UserGroup)
    ldap_pwd = models.CharField(max_length=100)
    ssh_key_pwd = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True)
    date_joined = models.DateTimeField(null=True)

    def __unicode__(self):
        return self.username
