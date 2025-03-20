# MaintenanceTrackPro

MaintenanceTrackPro is a comprehensive equipment maintenance management system designed to help organizations monitor equipment health, schedule maintenance tasks, and improve overall equipment reliability.

## Features

- **Multi-Role Access**: Customized dashboards for Managers (Boss), Administrators, and Technicians (Engineers)
- **Equipment Management**: Add, view, edit, and delete equipment with health monitoring
- **Maintenance Tracking**: Schedule, monitor, and complete maintenance tasks
- **QR Code Integration**: Quick access to equipment details via generated QR codes
- **Health Monitoring**: Track equipment health with visual indicators
- **Notifications**: Stay informed about equipment status and maintenance tasks

## Technology Stack

- **Backend**: Python Flask
- **Database**: SQLite (easy to set up, no external dependencies)
- **Frontend**: Bootstrap 5, HTML/CSS, JavaScript
- **Authentication**: Flask-Login
- **Forms**: Flask-WTF, WTForms
- **ORM**: SQLAlchemy

## Installation

1. Clone the repository
```bash
git clone <repository-url>
cd maintenancetrackpro
```

2. Create and activate a virtual environment
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Run the application
```bash
python app.py
```

5. Access the application at `http://localhost:5000`

## Initial Setup

After running the application for the first time:

1. Register a new user with the "Boss" role
2. Add equipment and start scheduling maintenance tasks
3. Register additional users as needed

## Project Structure

- `/app`: Main application package
  - `/models`: Database models
  - `/routes`: Route handlers
  - `/templates`: HTML templates
  - `/static`: CSS, JavaScript, and images
  - `__init__.py`: Application factory and configuration

## License

This project is licensed under the MIT License - see the LICENSE file for details. 