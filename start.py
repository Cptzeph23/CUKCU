import os
import subprocess

# Run migrations
subprocess.run(["python", "manage.py", "makemigrations", "--noinput"], check=True)
subprocess.run(["python", "manage.py", "migrate", "--noinput"], check=True)

# Get port from environment, default to 8000
port = os.environ.get("PORT", "8000")

# Start Gunicorn
subprocess.run([
    "gunicorn",
    "CUKCU1.wsgi:application",
    "--bind", f"0.0.0.0:{port}"
])
