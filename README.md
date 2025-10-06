# Smart Blind Stick - IoT Mobility Aid

A comprehensive Django-based web application for managing Smart Blind Stick devices, providing real-time obstacle detection, GPS tracking, emergency alerts, and analytics for visually impaired individuals.

## 🚀 Features

### Core Features
- **User Management**: Support for visually impaired users, guardians, and administrators
- **Device Management**: Real-time device status monitoring and configuration
- **GPS Tracking**: Live location tracking with geofencing capabilities
- **Emergency SOS**: Instant emergency alerts with guardian notifications
- **Obstacle Detection Analytics**: Comprehensive analytics and reporting
- **Guardian Portal**: Multi-user monitoring dashboard
- **Real-time Updates**: WebSocket support for live data

### Technical Features
- **Modern UI**: Responsive design with Tailwind CSS
- **Accessibility**: WCAG 2.1 compliant interface
- **Real-time**: Django Channels for WebSocket support
- **Maps**: Leaflet.js integration for GPS tracking
- **Charts**: Chart.js for analytics visualization
- **Notifications**: SMS integration via Twilio

## 🛠️ Tech Stack

- **Backend**: Django 5.0+, Django REST Framework
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla JS)
- **Styling**: Tailwind CSS with custom animations
- **Database**: SQLite (development) / PostgreSQL (production)
- **Real-time**: Django Channels
- **Maps**: Leaflet.js
- **Charts**: Chart.js
- **Icons**: Lucide Icons

## 📦 Installation

### Prerequisites
- Python 3.8+
- pip
- Git

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd smart-blind-stick
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment setup**
   ```bash
   cp env.example .env
   # Edit .env file with your settings
   ```

5. **Database setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Open http://localhost:8000 in your browser
   - Admin panel: http://localhost:8000/admin

## 🏗️ Project Structure

```
smart_blind_stick/
├── manage.py
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/
│   ├── users/          # User authentication & profiles
│   ├── devices/        # Device management
│   ├── tracking/       # GPS tracking & location history
│   ├── alerts/         # Emergency SOS system
│   ├── analytics/      # Data analytics & reports
│   └── guardians/      # Guardian portal features
├── templates/
│   ├── base.html
│   ├── landing.html
│   ├── dashboard.html
│   └── auth/
├── static/
└── media/
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Twilio Settings (for SMS notifications)
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=your_twilio_phone_number

# Email Settings
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_email_password
DEFAULT_FROM_EMAIL=your_email@gmail.com
```

### Twilio Setup (Optional)

For SMS notifications:
1. Sign up for Twilio account
2. Get your Account SID and Auth Token
3. Purchase a phone number
4. Update the environment variables

## 📱 Usage

### For Visually Impaired Users
1. Register an account
2. Add emergency contacts
3. Pair your Smart Blind Stick device
4. Configure device settings
5. Start using the device for navigation

### For Guardians
1. Register as a guardian
2. Connect with users you want to monitor
3. Set up notification preferences
4. Monitor real-time location and alerts

### For Administrators
1. Access admin panel at `/admin`
2. Manage users and devices
3. View system analytics
4. Handle support requests

## 🔌 API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout

### Devices
- `GET /api/devices/` - List user devices
- `POST /api/devices/register/` - Register new device
- `GET /api/devices/<id>/status/` - Get device status

### Tracking
- `POST /api/tracking/location/` - Update location
- `GET /api/tracking/history/` - Get location history
- `GET /api/tracking/live/<user_id>/` - WebSocket endpoint

### Alerts
- `POST /api/alerts/sos/` - Trigger SOS alert
- `GET /api/alerts/` - List alerts
- `PATCH /api/alerts/<id>/resolve/` - Resolve alert

### Analytics
- `GET /api/analytics/dashboard/` - Dashboard analytics
- `GET /api/analytics/obstacles/` - Obstacle analytics
- `GET /api/analytics/export/` - Export data

## 🎨 UI Components

### Design System
- **Colors**: Primary (#3B82F6), Secondary (#10B981), Accent (#F59E0B)
- **Typography**: Inter (body), Poppins (headings)
- **Components**: Cards, buttons, forms, modals
- **Animations**: Fade-in, slide-up, pulse effects

### Accessibility Features
- High contrast colors
- Screen reader friendly
- Keyboard navigation
- Large touch targets
- Semantic HTML

## 🚀 Deployment

### Production Setup

1. **Environment Variables**
   ```env
   DEBUG=False
   ALLOWED_HOSTS=yourdomain.com
   SECRET_KEY=your-production-secret-key
   ```

2. **Database**
   ```bash
   # Install PostgreSQL
   pip install psycopg2-binary
   
   # Update settings.py
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'smart_blind_stick',
           'USER': 'your_user',
           'PASSWORD': 'your_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

3. **Static Files**
   ```bash
   python manage.py collectstatic
   ```

4. **WebSocket Support**
   - Use Daphne as ASGI server
   - Configure Redis for channel layers

### Cloud Deployment

#### Heroku
```bash
# Install Heroku CLI
# Create Procfile
echo "web: daphne config.asgi:application --port $PORT --bind 0.0.0.0" > Procfile

# Deploy
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

#### Railway
```bash
# Connect GitHub repository
# Set environment variables
# Deploy automatically
```

## 📊 Analytics & Monitoring

### Key Metrics
- Device usage statistics
- Obstacle detection accuracy
- Emergency response times
- User safety scores
- Geographic heatmaps

### Reports
- Daily activity summaries
- Weekly safety reports
- Monthly analytics
- Custom date range reports

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

- Documentation: [Link to docs]
- Issues: [GitHub Issues]
- Email: support@smartblindstick.com

## 🙏 Acknowledgments

- WHO for visual impairment statistics
- OpenStreetMap for mapping data
- Django community for the framework
- Tailwind CSS for the design system

---

**Smart Blind Stick** - Empowering Independence Through Technology 🦯✨
