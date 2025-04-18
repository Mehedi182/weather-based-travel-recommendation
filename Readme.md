### Local Setup Instructions

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/Mehedi182/weather-based-travel-recommendation.git
   cd customer_support_service_app
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

4. **Load The Districts info, wheater and air quality data for the first time**

   ```bash
   python manage.py load_districts
   # it will call every day 12:00AM automatically to load 7days temparature air quality data. Used APsScheduler for this.
   ```

5. **Start the Development Server**:

   ```bash
   python manage.py runserver
   ```

6. **Run Test**:

   ```bash
   python manage.py test
   ```

7. **Test The api via postman(Postman collection provided)**


### To Run Using Docker

To run the application using Docker:

1. **Build and Start the Docker Container**:

   ```bash
   docker-compose up --build
   ```

2. **Stop and Clean Up**:
   ```bash
   docker-compose down
   ```
