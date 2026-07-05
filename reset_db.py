# reset_db.py
import os
import shutil
import subprocess

print("🔄 Resetting database...")

# Delete database
if os.path.exists('db.sqlite3'):
    os.remove('db.sqlite3')
    print("✅ Deleted db.sqlite3")

# Delete migration files
migration_dirs = [
    'accounts/migrations',
    'core/migrations', 
    'admin_dashboard/migrations',
    'dashboard/migrations',
    'transactions/migrations'
]

for dir_path in migration_dirs:
    if os.path.exists(dir_path):
        for file in os.listdir(dir_path):
            if file.endswith('.py') and file != '__init__.py':
                os.remove(os.path.join(dir_path, file))
                print(f"✅ Deleted {file} from {dir_path}")

# Run migrations
print("📦 Creating migrations...")
subprocess.run(['python', 'manage.py', 'makemigrations', 'accounts'])
subprocess.run(['python', 'manage.py', 'makemigrations', 'core'])
subprocess.run(['python', 'manage.py', 'makemigrations', 'admin_dashboard'])
subprocess.run(['python', 'manage.py', 'makemigrations', 'dashboard'])
subprocess.run(['python', 'manage.py', 'makemigrations', 'transactions'])

print("📦 Applying migrations...")
subprocess.run(['python', 'manage.py', 'migrate'])

print("👤 Creating superuser...")
subprocess.run(['python', 'manage.py', 'createsuperuser'])

print("✅ Done!")
