# Job Management System

This is a Job Management System built using Django with Redis Queue (RQ) for asynchronous task processing. The application includes authentication, job management, and job result tracking features.

## Prerequisites

Ensure you have the following installed on your system:

- Python (3.8+)
- PostgreSQL
- Redis
- pipenv (optional but recommended for virtual environments)

---

## Installation and Setup

### Clone the Repository

```bash
git clone git@github.com:SaboorSohaib/job_system.git
cd job_system
```

### Set Up Virtual Environment

```bash
pip install pipenv
pipenv shell
```

Alternatively, you can use `venv`:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

## Configuration

### 1. PostgreSQL Database Setup

1. Create a PostgreSQL database:

   ```sql
   CREATE DATABASE job_system;
   CREATE USER job_system WITH PASSWORD 'job_system';
   ALTER ROLE job_system SET client_encoding TO 'utf8';
   ALTER ROLE job_system SET default_transaction_isolation TO 'read committed';
   ALTER ROLE job_system SET timezone TO 'UTC';
   GRANT ALL PRIVILEGES ON DATABASE job_management TO job_system;
   ```

2. Update the `DATABASES` configuration in `settings.py` or `.env`:

   ```env
   DATABASE_URL=postgres://job_system:job_system@localhost/job_system
   ```

### 2. Email Setup for OTP

1. Configure email settings in `settings.py`:

   ```env
   EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=your_email@gmail.com
   EMAIL_HOST_PASSWORD=your_email_password
   ```

2. Ensure that your email account allows less secure app access or set up an app-specific password.

### 3. Redis Configuration

1. Install Redis on your system.

   - On Ubuntu:

     ```bash
     sudo apt update
     sudo apt install redis
     ```

   - On macOS:

     ```bash
     brew install redis
     ```

2. Start Redis:

   ```bash
   redis-server
   ```

3. Update Redis settings in `setting.py`:

   ```env
   REDIS_URL=redis://localhost:6379/0
   ```

---

## Running the Application

### 1. Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 2. Start the Redis Worker

```bash
rq worker --with-scheduler
```

### 3. Run the Django Development Server

```bash
python manage.py runserver
```

---

## Troubleshooting

- **Redis Connection Errors:**
  Ensure Redis is running and accessible at the specified `REDIS_URL`.

- **Email Errors:**
  Verify your email credentials and check if the email provider blocks suspicious logins.

---

## License

This project is licensed under the MIT License.
