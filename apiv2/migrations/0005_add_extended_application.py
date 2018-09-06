# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-19 17:08
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import oauth2_provider.generators
import oauth2_provider.validators


def migrate_data_forward(apps, schema_editor):
    extended_application_cls = apps.get_model('apiv2', 'ExtendedApplication')
    application_cls = apps.get_model('oauth2_provider', 'Application')
    for app in application_cls.objects.all():
        extended_application_cls.objects.create(
            id=app.id,
            client_id=app.client_id,
            redirect_uris=app.redirect_uris,
            client_type=app.client_type,
            authorization_grant_type=app.authorization_grant_type,
            client_secret=app.client_secret,
            name=app.name,
            skip_authorization=app.skip_authorization,
            user=app.user
        )


def migrate_data_backward(apps, schema_editor):
    extended_application_cls = apps.get_model('apiv2', 'ExtendedApplication')
    application_cls = apps.get_model('oauth2_provider', 'Application')
    original_application_ids = application_cls.objects.all().values_list('id', flat=True)
    for app in extended_application_cls.objects.all():
        if app.id not in original_application_ids:
            application_cls.objects.create(
                id=app.id,
                client_id=app.client_id,
                redirect_uris=app.redirect_uris,
                client_type=app.client_type,
                authorization_grant_type=app.authorization_grant_type,
                client_secret=app.client_secret,
                name=app.name,
                skip_authorization=app.skip_authorization,
                user=app.user
            )


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('apiv2', '0004_auto_20161019_1114'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExtendedApplication',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('client_id', models.CharField(db_index=True, default=oauth2_provider.generators.generate_client_id, max_length=100, unique=True)),
                ('redirect_uris', models.TextField(blank=True, help_text='Allowed URIs list, space separated', validators=[oauth2_provider.validators.validate_uris])),
                ('client_type', models.CharField(choices=[('confidential', 'Confidential'), ('public', 'Public')], max_length=32)),
                ('authorization_grant_type', models.CharField(choices=[('authorization-code', 'Authorization code'), ('implicit', 'Implicit'), ('password', 'Resource owner password-based'), ('client-credentials', 'Client credentials')], max_length=32)),
                ('client_secret', models.CharField(blank=True, db_index=True, default=oauth2_provider.generators.generate_client_secret, max_length=255)),
                ('name', models.CharField(blank=True, max_length=255)),
                ('skip_authorization', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='apiv2_extendedapplication', to=settings.AUTH_USER_MODEL)),
                ('redirect_uri_scheme', models.CharField(default=None, max_length=100))
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RunPython(migrate_data_forward, migrate_data_backward)
    ]