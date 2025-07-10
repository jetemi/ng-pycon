# PyCon Nigeria Website

A PyCon Nigeria conference management platform built with Wagtail CMS and Django, featuring a yearly theming system for visual customization while maintaining consistent backend functionality.

## Features

- **Conference Management**: Speaker submissions, ticketing, sponsorships, financial aid
- **Yearly Theming**: Complete visual customization per conference year using CSS custom properties
- **Wagtail CMS**: Flexible content management system
- **Modern Frontend**: Tailwind CSS + Alpine.js for responsive and interactive UI
- **Docker Support**: Containerized development environment

## Tech Stack

### Backend
- **Django 5.2.3**: Web framework
- **Wagtail 7.0.1**: CMS framework
- **PostgreSQL**: Database
- **Python 3.12**: Programming language

### Frontend
- **Tailwind CSS**: Utility-first CSS framework
- **Alpine.js**: Lightweight JavaScript framework
- **PostCSS**: CSS processing
- **Custom theming system**: Year-based visual customization

## Setup Instructions

### Prerequisites

- Docker and Docker Compose
- Node.js 18+ and npm
- Python 3.12+ (for local development)

### Quick Start

1. **Clone and setup**:
   ```bash
   git clone <repository-url>
   cd ng-pycon
   ./scripts/setup-dev.sh
   ```

### Manual Setup

1. **Copy environment file**:
   ```bash
   cp .env.example .env
   ```

2. **Update environment variables** in `.env`:
   - Change `SECRET_KEY` to a secure random string
   - Update database credentials if needed
   - Set `DEBUG=False` for production

3. **Install Node.js dependencies**:
   ```bash
   npm install
   ```

4. **Build frontend assets**:
   ```bash
   npm run build-css-prod
   ```

5. **Start services**:
   ```bash
   docker-compose up --build
   ```

6. **Run migrations** (in a new terminal):
   ```bash
   docker-compose exec web python manage.py migrate
   ```

7. **Create superuser**:
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

8. **Access the application**:
   - Website: http://localhost:8000
   - Wagtail Admin: http://localhost:8000/admin

## Development

### Frontend Development

- **Watch CSS changes**: `npm run build-css` (watches for changes)
- **Build production CSS**: `npm run build-css-prod`
- **Development with hot reload**: `npm run dev`

### Backend Development

- **Custom applications**: Place in `pyconng/apps/`
- **Templates**: Located in `pyconng/templates/`
- **Static files**: Located in `pyconng/static/`

### Yearly Theming System

The theming system uses CSS custom properties and data attributes:

```html
<!-- Set theme in template -->
<html data-theme="2024">

<!-- CSS custom properties -->
[data-theme="2024"] {
  --theme-primary: theme('colors.blue.600');
  --theme-secondary: theme('colors.green.600');
}

[data-theme="2025"] {
  --theme-primary: theme('colors.purple.600');
  --theme-secondary: theme('colors.pink.600');
}
```

### Project Structure

```
├── pyconng/
│   ├── apps/              # Custom Django applications
│   ├── settings/          # Django settings (base, dev, production)
│   ├── static/
│   │   ├── css/
│   │   │   ├── src/       # Tailwind CSS source files
│   │   │   └── pyconng.css # Generated CSS
│   │   └── js/
│   │       ├── pyconng.js  # Custom JavaScript
│   │       └── alpine.min.js # Alpine.js
│   └── templates/         # Django templates
├── scripts/               # Development scripts
├── docker-compose.yml     # Docker services
├── Dockerfile            # Multi-stage build
├── package.json          # Node.js dependencies
├── tailwind.config.js    # Tailwind CSS configuration
└── postcss.config.js     # PostCSS configuration
```

## Docker Services

- **web**: Django application server
- **db**: PostgreSQL 16 database
- **frontend**: Node.js for CSS building (dev profile)

## Available Scripts

- `npm run build-css`: Watch and build CSS during development
- `npm run build-css-prod`: Build minified CSS for production
- `npm run dev`: Start development server with CSS watching
- `./scripts/setup-dev.sh`: Complete development environment setup

## Environment Variables

Key environment variables (see `.env.example`):

```env
# Database
DB_NAME=pyconng_db
DB_USER=pyconng_user
DB_PASSWORD=pyconng_password
DB_HOST=db
DB_PORT=5432

# Django
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License. 