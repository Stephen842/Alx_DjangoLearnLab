from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group, Permission
from django.dispatch import receiver
from django.apps import apps

@receiver(post_migrate)
def create_groups(sender, **kwargs):
    if sender.name == "bookshelf":
        permissions = {
            "Viewers": ["can_view"],
            "Editors": ["can_view", "can_create", "can_edit"],
            "Admins": ["can_view", "can_create", "can_edit", "can_delete"],
        }

        for group_name, perms in permissions.items():
            group, _ = Group.objects.get_or_create(name=group_name)
            for perm_codename in perms:
                perm = Permission.objects.get(codename=perm_codename)
                group.permissions.add(perm)
