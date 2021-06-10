# Generated by Django 3.1 on 2021-06-10 10:56
import os
from django.db import migrations


def create_premier_tenant(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Client = apps.get_model('Customers', 'Client')
    Domain = apps.get_model('Customers', 'Domain')
    DNS = os.getenv('DOMAIN')

    tenant_public = Client.objects.get_or_create(schema_name='public',
                                                 name='Tibillet Public',
                                                 paid_until='2200-12-05',
                                                 on_trial=False)[0]

    # Add one or more domains for the tenant
    domaine_seul = Domain.objects.get_or_create(domain=DNS,
                                                tenant=tenant_public,
                                                is_primary=True,
                                                )

    domaine_www = Domain.objects.get_or_create(domain=f'www.{DNS}',
                                               tenant=tenant_public,
                                               is_primary=False,
                                               )

    return tenant_public, domaine_seul[0], domaine_www[0]


def reverse(apps, schema_editor):
    tenant_public, domaine_seul, domaine_www = create_premier_tenant(apps, schema_editor)
    tenant_public.delete()
    domaine_seul.delete()
    domaine_www.delete()


class Migration(migrations.Migration):
    dependencies = [
        ('Customers', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_premier_tenant, reverse),
    ]
