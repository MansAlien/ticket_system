from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group, Permission

@receiver(post_save, sender=User)
def assign_user_to_group(sender, instance, created, **kwargs):
    if created:
        # Get the "Normal Users" group
        group, created = Group.objects.get_or_create(name='Normal User')
        # Add the user to the group
        instance.groups.add(group)
        instance.is_staff = True
        instance.save()