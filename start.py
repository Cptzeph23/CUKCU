import os
import subprocess
import sys

def run_command(command):
    """Run a shell command and exit if it fails"""
    result = subprocess.run(command)
    if result.returncode != 0:
        sys.exit(result.returncode)

# 1. Make migrations and apply them
run_command(["python", "manage.py", "makemigrations", "--noinput"])
run_command(["python", "manage.py", "migrate", "--noinput"])

# 2. Get port from environment variable, default to 8000
port = os.environ.get("PORT")
if not port or not port.isdigit():
    port = "8000"

# 3. Start Gunicorn
run_command([
    "gunicorn",
    "CUKCU1.wsgi:application",
    "--bind", f"0.0.0.0:{port}"
])
