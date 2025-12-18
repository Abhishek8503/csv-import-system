# Async CSV Import System (Django + Celery + Redis)

A backend-focused system to upload and asynchronously process large CSV files (100k–500k rows) using Django, Celery, Redis, and PostgreSQL (Supabase).

This project demonstrates **real-world backend engineering patterns**:
- Background job processing
- Chunked CSV parsing
- Bulk database operations
- Job status & progress tracking
- Non-blocking APIs

---

## 🧱 Tech Stack

- **Backend**: Django, Django REST Framework
- **Async Processing**: Celery
- **Message Broker**: Redis (via Docker)
- **Database**: PostgreSQL (Supabase)
- **Environment**: Windows (development)
- **Containerization**: Docker (Redis only)

---

## 📁 Project Structure

csv-import-system/
├── backend/
│ ├── apps/
│ │ ├── products/
│ │ └── imports/
│ ├── config/
│ │ ├── celery.py
│ │ ├── settings.py
│ │ └── urls.py
│ ├── media/
│ │ └── imports/
│ ├── manage.py
│ └── requirements.txt
└── README.md

yaml
 

---

## ⚙️ Setup Instructions (Windows)

### 1️⃣ Clone the repository

``` 
git clone <your-repo-url>
cd csv-import-system/backend
2️⃣ Create and activate virtual environment
 
 
python -m venv venv
venv\Scripts\activate
3️⃣ Install dependencies
 
 
pip install -r requirements.txt
4️⃣ Environment Variables (.env)
Create a .env file in backend/:

env
 
DEBUG=True
SECRET_KEY=your-secret-key

DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=your-supabase-host
DB_PORT=5432
5️⃣ Run migrations
 
 
python manage.py makemigrations
python manage.py migrate
6️⃣ Create superuser (for admin)
 
 
python manage.py createsuperuser
🐳 Redis Setup (Docker)
Install Docker Desktop
Download from:
https://www.docker.com/products/docker-desktop/

Make sure virtualization is enabled and Docker Desktop is running.

Run Redis in Docker (background)
 
 
docker run -d -p 6379:6379 --name redis redis
Verify Redis is running:

 
 
docker ps
🔁 Celery Setup
Celery Configuration (already included)
Broker: Redis

Pool: solo (Windows-compatible)

In settings.py:

python
 
CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_RESULT_BACKEND = "django-db"
CELERY_WORKER_POOL = "solo"
Start Celery Worker
Open a new terminal, activate venv, then:

 
 
cd backend
celery -A config worker -l info --pool=solo
You should see:

arduino
 
celery@<machine-name> ready.
⚠️ Keep this terminal running.

▶️ Run Django Server
In another terminal:

 
 
python manage.py runserver
📤 CSV Upload API
Endpoint
swift
 
POST /api/imports/upload/
Upload CSV using curl (Free, No Postman)
 
 
curl -X POST "http://127.0.0.1:8000/api/imports/upload/" -F "file=@products.csv"  
Example CSV format:

csv
 
sku,name,price
ABC001,Keyboard,999.99
ABC002,Mouse,499.50
abc001,Keyboard Updated,1099.99
🔄 Async Processing Flow
 
 
CSV Upload
 → ImportJob created (PENDING)
 → Celery task triggered
 → CSV parsed in background
 → Products inserted/updated
 → Progress tracked
 → Job marked COMPLETED or FAILED
The API returns immediately — no blocking.

🧪 Monitoring & Debugging
Celery Logs
Watch the Celery terminal for:

arduino
 
Task apps.imports.tasks.process_csv_import[...] received
Task ... succeeded
Django Admin
Visit:

arduino
 
http://127.0.0.1:8000/admin/
View Import Jobs

Check status & progress

Inspect Products table

❗ Important Notes
CSV processing is not triggered from Django Admin

Celery is triggered only via API

This avoids accidental reprocessing

Admin is for inspection, not workflow execution

📌 Key Backend Concepts Demonstrated
Asynchronous task execution

Message queues

Chunked data processing

Bulk database inserts

Case-insensitive uniqueness constraints

Job-based architecture

🚀 Future Improvements (Phase 5)
Import job status API (GET /api/imports/{id})

Frontend upload UI with progress bar

Retry failed imports

Deployment (Render / Railway / Fly.io)

👨‍💻 Author
Abhishek Rao
Backend Engineer (Python, Django, Async Systems)

yaml
 

---

## ✅ What You Should Do Now

1. Create `README.md` at project root
2. Paste the above content
3. Commit it:

``` 
git add README.md
git commit -m "Add comprehensive project README with setup and usage instructions"