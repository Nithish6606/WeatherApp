# Agri-Weather Full Stack Application

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![License](https://img.shields.io/badge/license-MIT-blue)
![Version](https://img.shields.io/badge/version-1.0.0-orange)

> **Empowering farmers with precise, location-based weather insights.**
> This application provides real-time weather data and forecasts tailored for agricultural needs, leveraging a hybrid API approach for maximum reliability.

---

## 🌟 Key Features

*   **Hybrid Weather API**: Seamlessly switches between **OpenWeatherMap** (Primary) and **Open-Meteo** (Secondary) to ensure zero downtime.
*   **PostGIS Geolocation**: Advanced spatial database capabilities for precise location tracking and future geospatial features.
*   **JWT Authentication**: Secure, stateless authentication using JSON Web Tokens.
*   **Offline-Ready Dashboard**: A responsive React frontend designed to work reliably even in low-connectivity rural areas.

---

## 🛠 Tech Stack

| Category | Technologies |
| :--- | :--- |
| **Frontend** | React 18, Vite, Leaflet, Axios, CSS Modules |
| **Backend** | Django 5.0, Django Rest Framework (DRF), SimpleJWT |
| **Database** | PostgreSQL 15 + PostGIS 3.3 |
| **DevOps** | Docker Compose, Nginx (Alpine), Gunicorn |

---

## 📂 Project Structure

```text
agri-weather-app/
├── backend/                # Django Project Root
│   ├── apps/               # Django Apps
│   │   ├── users/          # Authentication App
│   │   └── weather/        # Weather Logic App
│   ├── config/             # Project Configuration (settings, urls)
│   ├── manage.py           # Django Management Script
│   ├── Dockerfile          # Backend Dockerfile
│   └── requirements.txt    # Python Dependencies
├── frontend/               # React Frontend
│   ├── src/                # Source Code
│   ├── Dockerfile          # Frontend Dockerfile
│   └── package.json        # Node Dependencies
├── nginx/                  # Nginx Configuration
├── docker-compose.yml      # Docker Orchestration
└── README.md               # Project Documentation
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root with the following keys:

| Variable | Description | Example |
| :--- | :--- | :--- |
| `OPENWEATHER_API_KEY` | Your API key from OpenWeatherMap | `a1b2c3d4e5...` |
| `DB_NAME` | PostgreSQL Database Name | `weather_db` |
| `DB_USER` | PostgreSQL User | `postgres` |
| `DB_PASSWORD` | PostgreSQL Password | `postgres` |
| `SECRET_KEY` | Django Secret Key | `django-insecure-...` |
| `POSTGRES_HOST` | Database Host (Docker service name) | `db` |
| `POSTGRES_PORT` | Database Port | `5432` |

---

## 🚀 Installation Guide

### Method 1: Docker (Recommended)

The easiest way to get up and running. Requires **Docker** and **Docker Compose**.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/agri-weather-app.git
    cd agri-weather-app
    ```

2.  **Configure Environment:**
    Copy the example env file and add your API key.
    ```bash
    cp .env.example .env
    # Edit .env and add your OPENWEATHER_API_KEY
    ```

3.  **Launch the Application:**
    ```bash
    docker-compose up --build
    ```

4.  **Initialize Database:**
    Open a new terminal and run:
    ```bash
    docker-compose exec backend python manage.py migrate
    docker-compose exec backend python manage.py createsuperuser
    ```

5.  **Access the App:**
    *   **Frontend**: [http://localhost](http://localhost)
    *   **Backend API**: [http://localhost:8000/api/](http://localhost:8000/api/)
    *   **Admin Panel**: [http://localhost:8000/admin/](http://localhost:8000/admin/)

---

### Method 2: Manual Setup (Development)

For local development without Docker.

#### Backend Setup

1.  **Navigate to backend:**
    ```bash
    cd backend
    ```

2.  **Create Virtual Environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run Migrations & Server:**
    ```bash
    python manage.py migrate
    python manage.py runserver
    ```

#### Frontend Setup

1.  **Navigate to frontend:**
    ```bash
    cd ../frontend
    ```

2.  **Install Dependencies:**
    ```bash
    npm install
    ```

3.  **Start Dev Server:**
    ```bash
    npm run dev
    ```
    Access at [http://localhost:5173](http://localhost:5173).

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
