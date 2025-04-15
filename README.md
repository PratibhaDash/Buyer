🧑‍🌾 Farm Management Backend (DRF)
A Django REST Framework-based backend system for managing users, buyers, farms, and agricultural products. The project follows a modular architecture with clearly separated apps and support for user authentication, permissions, and mailing features.

📁 Project Structure
├── buyer/               # Buyer-related APIs
├── env/                 # Virtual environment (not tracked)
├── farm/                # Main project config (settings, mailing, utils)
├── farm_app/            # General farm operations or logic
├── product/             # Product-related endpoints and logic
├── user_management/     # User registration, login, and permissions
├── .env.example         # Sample environment variables
├── manage.py
├── requirements.txt

🚀 Features :
    🔐 JWT-based authentication system
    👤 User management with custom permissions
    📦 Product CRUD APIs
    🧾 Buyer APIs
    🌾 Farm logic and utilities
    📧 Mailing utility (farm/mailing.py)
    📄 Modular app structure for scalability
    🧪 Unit testing support per app

⚙️ Setup Instructions
1. Clone the Repo
    git clone https://github.com/your-username/farm-backend.git
    cd farm-backend
2. Create & Activate Virtual Environment
    python -m venv env
    source env/bin/activate  # Windows: env\Scripts\activate
3. Install Dependencies
    pip install -r requirements.txt
4. Environment Variables
    Create a .env file and configure it based on .env.example:
    DEBUG=True
    SECRET_KEY=your-secret-key
    DATABASE_URL=postgres://user:password@localhost:5432/db_name
    EMAIL_HOST=smtp.example.com
    EMAIL_PORT=587
    EMAIL_HOST_USER=your-email@example.com
    EMAIL_HOST_PASSWORD=your-password
5. Migrations & Superuser
    python manage.py makemigrations
    python manage.py migrate
    python manage.py createsuperuser
6. Run Server
    python manage.py runserver


🗂 App Responsibilities :
user_management -	Handles registration, login, roles, permissions
buyer -	APIs for managing buyers
farm_app -	Farm-related operations (general logic)
product -	CRUD for farm products

