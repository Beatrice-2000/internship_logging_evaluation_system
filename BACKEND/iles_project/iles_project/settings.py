from pathlib import Path

# ---------------------
# Basic paths
# ---------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------
# Security
# ---------------------
SECRET_KEY = 'django-insecure-tq_=z=os6r2(c)_l84do*cg%h9jl(_gjtxks#)36hvwzqo20k%'
DEBUG = True
ALLOWED_HOSTS = []

# ---------------------
# Installed apps
# ---------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'core',  # your app
]

# ---------------------
# Middleware
# ---------------------
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # MUST be first
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ---------------------
# URL config
# ---------------------
ROOT_URLCONF = 'iles_project.urls'

# ---------------------
# Templates
# ---------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'iles_project.wsgi.application'

# ---------------------
# Database (PostgreSQL)
# ---------------------
AUTH_USER_MODEL = 'core.User'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'iles_db',        # your DB name
        'USER': 'postgres',       # your PostgreSQL username
        'PASSWORD': 'yourpassword', # your PostgreSQL password
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# ---------------------
# Password validation
# ---------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ---------------------
# Internationalization
# ---------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ---------------------
# Static files
# ---------------------
STATIC_URL = 'static/'

# ---------------------
# CORS
# ---------------------
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # React frontend
]
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}