# Permissions and Groups Setup

This project uses Django's built-in permission system.

## Custom Permissions
Defined in `Book` model (`models.py`):
- can_view
- can_create
- can_edit
- can_delete

## Groups
Created via admin or `signals.py`:
- **Viewers** → can_view
- **Editors** → can_view, can_create, can_edit
- **Admins** → can_view, can_create, can_edit, can_delete

## Enforced in Views
Each view uses `@permission_required` with the proper codename.
