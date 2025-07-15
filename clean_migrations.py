import os
import shutil

for root, dirs, files in os.walk('.'):
    # Delete all migration .py and .pyc files except __init__.py
    if 'migrations' in root:
        for file in files:
            if file != '__init__.py' and file.endswith(('.py', '.pyc')):
                os.remove(os.path.join(root, file))
    
    # Delete __pycache__ folders
    if '__pycache__' in dirs:
        shutil.rmtree(os.path.join(root, '__pycache__'))
