import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.workers.event_handlers import celery_app

if __name__ == '__main__':
    # Remove the script name from sys.argv so Celery doesn't get confused
    sys.argv.pop(0)
    celery_app.worker_main() 