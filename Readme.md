# Weather-Based Travel Recommendation System

A lightweight Django-based web application designed to provide travel recommendations based on weather and air quality data. It incorporates user authentication, automated data updates, and a minimalistic setup using SQLite and Django Simple JWT for secure access.

---

### Key Features

- **Weather-Based Travel Recommendations**: Provides travel recommendations based on weather and air quality data for different districts.
- **District Ranking**: Lists the top 10 districts for travel based on average temperature and PM2.5 levels over the next 7 days.
- **Daily Data Updates**: Automatically updates weather and air quality data every day at 12:00 AM using APScheduler.
- **Health Check Endpoint**: Includes a `/health/` endpoint to monitor the application's health and database connectivity.
- **User Authentication**: Implements user authentication using Django Simple JWT for secure access to APIs.
- **User Management**: Supports user registration, password change, and listing all registered users.
- **SQLite Database**: Uses SQLite for a lightweight and minimalistic database setup, suitable for development and small-scale projects.
- **Postman Collection**: Provides a Postman collection for easy testing of all API endpoints.
- **Dockerized Setup**: Includes a Docker configuration for containerized deployment and simplified setup.

---

### Local Setup Instructions

1. **Clone the Repository**:

   ```bash
      git clone https://github.com/Mehedi182/weather-based-travel-recommendation.git
      cd weather-based-travel-recommendation
   ```

2. **Create a Virtual Environment and Install Dependencies**:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # For Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Apply Database Migrations**:

   ```bash
   python manage.py migrate
   ```

4. **Load The Districts Info, Weather, and Air Quality Data for the First Time**:

   ```bash
   python manage.py load_districts
   # It will call every day at 12:00 AM automatically to load 7 days of temperature and air quality data. Used APScheduler for this.
   ```

5. **Start the Development Server**:

   ```bash
   python manage.py runserver
   ```

6. **To Run Tests**:

   ```bash
   python manage.py test
   ```

7. **Test the API via Postman (Postman Collection Provided)**:

   **Auth Section**:
   - **User Registration** – `POST /api/auth/user-registration/`
   - **Access Token** – `POST /api/auth/token/`
   - **Change Password** – `PUT /api/auth/change-password/`
   - **List Users** – `GET /api/auth/users/`
   - **Refresh Token** – `POST /api/auth/token-refresh/`

   **APIs**:
   - **HealthCheck** – `GET /api/health/`
   - **Best Districts** – `GET /api/best-districts/`
   - **Travel Recommendation** – `POST /api/travel-recommendation/`
     - API requires authentication. Token needs to be passed through Bearer Token. Example API information is available in the Postman collection.

---

### To Run Using Docker

1. **Build and Start the Docker Container**:

   ```bash
   docker-compose up --build
   ```

2. **Stop and Clean Up**:

   ```bash
   docker-compose down
   ```
