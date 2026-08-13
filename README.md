## Backend Setup
### Prerequisites
Install:

- Git
- Docker Desktop

### 1. Clone the repository

git clone https://github.com/DTB-Interns-Project/payment-gateway-backend.git

cd payment-gateway-backend

### 2. Create environment file

Copy-Item .env.example .env

Update `.env` with your local configuration.

### 3. Build and start containers

docker compose up -d --build

### 4. Run migrations

docker compose exec backend python manage.py migrate

### 5. Create an admin user

docker compose exec backend python manage.py createsuperuser

### 6. Check the application

docker compose exec backend python manage.py check

### 7. View running containers

docker compose ps
