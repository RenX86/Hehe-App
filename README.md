# Hehe App v2 - Digital Collection Manager

![Hehe App](https://img.shields.io/badge/Hehe%20App-v2.0-blue)
![Flask](https://img.shields.io/badge/Flask-2.0.1-green)
![Python](https://img.shields.io/badge/Python-3.9+-yellow)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple)

A modern Flask web application for managing digital collections with a focus on artist-centric organization, powerful filtering, and a responsive UI with dark mode support.

## ✨ Key Features

- **Collection Management**
  - 🎨 Artist-centric view with parent-child layout
  - 🔍 Advanced filtering by rating, source, and artist
  - 📊 Pagination for improved performance with large collections
  - 🏷️ Custom badge system for works

- **User Experience**
  - 🌓 Beautiful dark/light mode theme switching
  - 📱 Fully responsive design for all device sizes
  - ⚡ Optimized for performance with large collections
  - 🖼️ Modern, intuitive UI with animations

- **Security & Authentication**
  - 🔐 Secure user authentication (login/register)
  - ✉️ Email verification system
  - 🔒 Input sanitization to prevent SQL injection
  - 🛡️ CSRF protection and secure password handling

## 🚀 Live Demo

Visit [Hehe App v2 Demo](https://hehe-app-v2.example.com) to see the application in action.

## 💻 Tech Stack

- **Backend**
  - Flask 2.0.1
  - SQLAlchemy ORM
  - Flask-Login for authentication
  - Flask-Mail for email verification
  - Flask-WTF for forms and CSRF protection

- **Frontend**
  - Bootstrap 5.3
  - Custom CSS with CSS variables for theming
  - JavaScript for interactive features
  - Responsive design principles

- **Database**
  - PostgreSQL
  - SQLAlchemy migrations

- **Deployment**
  - Gunicorn with Gevent
  - Ready for Render.com deployment

## 📋 Prerequisites

- Python 3.9+
- PostgreSQL
- SMTP server for email verification
- Git

## 🔧 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/Hehe2.git
   cd Hehe2
   ```

2. **Set up a virtual environment**
   ```bash
   # For Windows
   python -m venv venv
   venv\Scripts\activate

   # For macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   Create a `.env` file in the root directory with the following variables:
   ```env
   FLASK_APP=run.py
   FLASK_ENV=development
   SECRET_KEY=your-secure-secret-key

   # Database
   DATABASE_URL=postgresql://username:password@localhost/hehe2db

   # Email Configuration
   MAIL_SERVER=smtp.example.com
   MAIL_PORT=587
   MAIL_USE_TLS=True
   MAIL_USERNAME=your-email@example.com
   MAIL_PASSWORD=your-email-password
   MAIL_DEFAULT_SENDER=your-email@example.com
   ```

5. **Initialize the database**
   ```bash
   flask db upgrade
   ```

6. **Start the development server**
   ```bash
   flask run
   ```

7. **Access the application**
   Open your browser and navigate to `http://localhost:5000`

## 🏗️ Project Structure

```
Hehe2/
├── app/                  # Application package
│   ├── __init__.py       # Application factory
│   ├── models/           # Database models
│   │   ├── user.py       # User model
│   │   └── work.py       # Work and Artist models
│   ├── routes/           # Route blueprints
│   │   ├── auth.py       # Authentication routes
│   │   └── main.py       # Main page routes
│   ├── static/           # Static assets
│   │   ├── css/          # CSS styles
│   │   ├── js/           # JavaScript files
│   │   └── images/       # Images and icons
│   ├── templates/        # Jinja2 templates
│   │   ├── auth/         # Authentication templates
│   │   └── main/         # Main page templates
│   └── utils/            # Utility modules
│       ├── email.py      # Email functionality
│       └── security.py   # Security utilities
├── migrations/           # Database migrations
├── .env                  # Environment variables
├── config.py             # Application configuration
├── Procfile              # Deployment configuration
├── requirements.txt      # Python dependencies
└── run.py                # Application entry point
```

## 🌐 Deployment

### Render.com Deployment

This application is pre-configured for deployment on Render.com:

1. Push your code to GitHub
2. Create a new Web Service on Render
3. Connect to your GitHub repository
4. Set the following:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn -w 4 -b 0.0.0.0:$PORT run:app`
5. Add your environment variables in the Render dashboard
6. Deploy!

## 🧰 Development

### Adding New Features

1. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes

3. Test thoroughly

4. Submit a pull request

### Database Migrations

When changing models:

```bash
# Create a migration
flask db migrate -m "Description of changes"

# Apply the migration
flask db upgrade
```

## 🔍 Troubleshooting

### Common Issues

- **Email verification not working**
  - Check your SMTP settings in .env
  - Ensure port 587 is not blocked by your firewall
  - Try using a different email provider

- **Database connection errors**
  - Verify PostgreSQL is running
  - Check database credentials in .env
  - Ensure the database exists

- **Styling issues**
  - Clear browser cache
  - Check for CSS conflicts
  - Test in different browsers

### Logs

Check the application logs for detailed error information:

```bash
# In development
flask run --debug

# In production
heroku logs --tail  # If using Heroku
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For support, please:
- Open an issue in the GitHub repository
- Contact the maintainers at support@heheapp.example.com

---

<p align="center">Made with ❤️ using Flask and Python</p>
<p align="center">
  <a href="https://flask.palletsprojects.com/">Flask</a> •
  <a href="https://www.postgresql.org/">PostgreSQL</a> •
  <a href="https://getbootstrap.com/">Bootstrap</a>
</p> 