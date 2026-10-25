
from django.db import migrations


def assign_course_owners(apps, schema_editor):
    Course = apps.get_model("content", "Course")
    User = apps.get_model("users", "CustomUser")

    database = schema_editor.connection.alias

    admin = (
        User.objects.using(database)
        .filter(is_superuser=True)
        .order_by("id")
        .first()
    )

    if admin is None:
        return

    Course.objects.using(database).filter(
        owner__isnull=True
    ).update(owner_id=admin.pk)


class Migration(migrations.Migration):

    dependencies = [
        (
            "content",
            "0002_course_is_featured_course_owner_course_status_and_more",
        ),
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(
            assign_course_owners,
            reverse_code=migrations.RunPython.noop,
        ),
    ]
