python manage.py migrate


# Create The superuser

echo "Checking if the superuser with username 'fynder' already exists..."
python manage.py shell <<EOF
from django.contrib.auth import get_user_model

# Verifica se il superuser esiste già
User = get_user_model()
user, created = User.objects.get_or_create(username='fynder')

if created:
    print("Superuser created successfully!")
    user.set_password('fynder')
    user.is_superuser = True
    user.is_staff = True
    user.save()
else:
    print("The superuser already exists.")

EOF

# Starting the server
echo "Starting the server..."

gunicorn fynd.wsgi:application --bind 0.0.0.0:8000 --workers 3