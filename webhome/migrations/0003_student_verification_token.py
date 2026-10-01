import uuid

from django.db import migrations, models


def populate_verification_tokens(apps, schema_editor):
    Student = apps.get_model('webhome', 'Student')
    for student in Student.objects.filter(verification_token__isnull=True):
        student.verification_token = uuid.uuid4()
        student.save(update_fields=['verification_token'])


class Migration(migrations.Migration):

    dependencies = [
        ('webhome', '0002_student'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='verification_token',
            field=models.UUIDField(default=uuid.uuid4, editable=False, null=True, unique=True),
        ),
        migrations.RunPython(populate_verification_tokens, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='student',
            name='verification_token',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
