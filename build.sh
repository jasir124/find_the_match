#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# Automatically create admin user for Render Free Tier
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')
admin = User.objects.get(username='admin')
admin.role = 'ADMIN'
admin.status = 'ACTIVE'
admin.save()

from skills.models import Skill
default_skills = ['Python', 'JavaScript', 'Java', 'C++', 'UI/UX Design', 'Graphic Design', 'Video Editing', 'Public Speaking', 'Marketing', 'Data Analysis', 'Web Development', 'Mobile App Development']
for skill_name in default_skills:
    Skill.objects.get_or_create(name=skill_name)

if not User.objects.filter(username='organizer').exists():
    org = User.objects.create_user(username='organizer', email='organizer@example.com', password='admin')
    org.role = 'ORGANIZER'
    org.status = 'ACTIVE'
    org.save()
"
