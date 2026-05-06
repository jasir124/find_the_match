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
default_skills = ['Python', 'Java', 'C++', 'Web Development', 'Django', 'Networking', 'Cloud Computing', 'DevOps', 'Cybersecurity', 'AI', 'Machine Learning', 'Singing', 'Acting', 'Mimicry', 'Stand-up Comedy', 'Drawing', 'Painting', 'Dance', 'Public Speaking', 'Anchoring', 'Video Editing', 'Photography', 'Content Creation', 'Script Writing', 'Basketball', 'Volleyball', 'Football', 'Cricket', 'Hockey', 'Sprinting (100m/200m/400m)', 'Middle Distance Running', 'Long Distance Running', 'Relay Running', 'High Jump', 'Long Jump', 'Triple Jump', 'Shot Put', 'Discus Throw', 'Javelin Throw', 'Badminton', 'Table Tennis', 'Tennis', 'Chess', 'Carrom']
for skill_name in default_skills:
    Skill.objects.get_or_create(name=skill_name)

if not User.objects.filter(username='organizer').exists():
    org = User.objects.create_user(username='organizer', email='organizer@example.com', password='admin')
    org.role = 'ORGANIZER'
    org.status = 'ACTIVE'
    org.save()
"
