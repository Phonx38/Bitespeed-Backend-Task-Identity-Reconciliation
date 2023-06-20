# Bitespeed-Backend-Task-Identity-Reconciliation

Make sure you have the following tools installed on your machine:

- Docker
- Docker Compose

# Getting Started

1. Clone the repository:

   ```bash
   git clone https://github.com/Phonx38/Bitespeed-Backend-Task-Identity-Reconciliation.git
   ```

2. Navigate to the project directory:

   ```bash
   cd bitespeed_task
   ```

3. Build Docker Image and start detached containers:

   ```bash
   docker compose -f local.yml up --build -d
   ```

4. Apply DB migrations:

   ```bash
   docker compose -f local.yml run --rm django python manage.py makemigrations
   ```

   ```bash
   docker compose -f local.yml run --rm django python manage.py migrate
   ```

Now you're ready to access Identity endpoint!

4. Shutting down containers:

   ```bash
   docker compose -f local.yml down
   ```

# Accessing Identify endpoint

- Identify endpoint can be accessed via

```bash
   http://localhost:8000/identify/
```

# Resume

- I have added my resume file as resume.pdf in the repo
