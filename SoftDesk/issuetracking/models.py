from django.db import models
from django.conf import settings
from authentication.models import User


class Project(models.Model):

    PROJET = 'PJ'
    PRODUCT = 'PR'
    APP = 'AP'
    TYPE = [
        (PROJET, 'PROJET'),
        (PRODUCT, 'PRODUIT'),
        (APP, 'APPLICATION'),
    ]

    DEV = 'DV'
    PROD = 'PR'
    STATUS = [
        (DEV, 'DEVELOPMENT'),
        (PROD, 'PRODUCTION')
    ]

    title = models.CharField(max_length=250)
    desc = models.CharField(max_length=500, blank=True)
    type = models.CharField(choices=TYPE, max_length=2)
    status = models.CharField(choices=STATUS, max_length=2)

    author = models.ForeignKey(User, on_delete=models.CASCADE)


class Contributor(models.Model):

    READ = 'RD'
    WRITE = 'WR'
    ADMIN = 'AD'
    PERMISSIONS = [
        (READ, 'READ'),
        (WRITE, 'WRITE'),
        (ADMIN, 'ADMIN'),
    ]

    AUTHOR = 'AU'
    COLLAB = 'CO'
    ROLES = [
        (AUTHOR, 'AUTHOR'),
        (COLLAB, 'COLLAB'),
    ]

    permission = models.CharField(choices=PERMISSIONS, default='READ', max_length=2)
    role = models.CharField(choices=ROLES, max_length=2)

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('project', 'user')


class Issue(models.Model):

    title = models.CharField(max_length=255)
    desc = models.CharField(max_length=500)
    tag = models.CharField(max_length=255)
    priority = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    created_time = models.DateTimeField(auto_now_add=True)

    project_id = models.ForeignKey(Project, on_delete=models.CASCADE,
                                   related_name='issues')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='author')
    assign = models.ForeignKey(User,
                               null=True,
                               on_delete=models.CASCADE,
                               related_name='assign')


class Comments(models.Model):

    desc = models.CharField(max_length=500)
    created_time = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
