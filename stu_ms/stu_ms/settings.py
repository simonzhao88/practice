"""
Django settings for stu_ms project.

Generated by 'django-admin startproject' using Django 1.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'k=9iaib_n_yd#vv6@=raj$l_wf@-)4(lhy1d#eddmq(p2414a0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'stu',
    'user',
    'mytest',
    'rest_framework',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 自定义中间件完成登录验证功能
    'utils.UserAuthMiddleware.UserAuthMiddle',
]

ROOT_URLCONF = 'stu_ms.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'stu_ms.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'stu',
        'HOST': '10.7.152.90',
        'PORT': '3306',
        'USER': 'root',
        'PASSWORD': '123456'
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/


STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# 创建日志保存文件地址
LOG_PATH = os.path.join(BASE_DIR, 'log')
# 如果地址日志文件夹不存在，则自动创建
if not os.path.isdir(LOG_PATH):
    os.mkdir(LOG_PATH)

LOGGING = {
    # version 只能为1
    'version': 1,
    # disable_existing_loggers 键为True（默认），那么默认配置中的所有logger都将禁用
    # Logger 的禁用与删除不同： logger 仍然存在，但是将默默丢弃任何传递给它的信息，也不会传播给上一级logger
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'

        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'stu_handlers': {
            # 如果loggers的处理级别小于handlers的处理级别，则handler忽略改信息
            'level': 'DEBUG',
            # 指定文件类型为RotatingFileHandler，当日志文件大小超过maxBytes以后会自动切割文件
            'class': 'logging.handlers.RotatingFileHandler',
            # 输出文件位置
            'filename': '%s/log.txt' % LOG_PATH,
            # 使用哪种日志格式化配置
            'formatter': 'verbose',
            # 指定日志文件大小
            'maxBytes': 1024 * 1024 * 5
        },
    },
    'loggers': {
        'console': {
            'handlers': ['stu_handlers'],
            'level': 'INFO',
            # propagate=0，表示输出日志，但消息不传递
            # propagate=1 是输出日志，同时消息向更高级别的地方传递，root为最高级别
            'propagate': False
        },
    },
}

# 没有登录跳转地址
LOGIN_URL = '/user/login/'


# rest分页配置
REST_FRAMEWORK = {
    # 配置分页
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 3,
    # 取消django的用户验证
    'DEFAULT_AUTHENTICATION_CLASSES': (),
    # 配置返回数据json格式
    'DEFAULT_RENDERER_CLASSES': (
        'utils.function.CustomJsonRenderer',
    ),
    # 配置过滤
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework.filters.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter'
    ),

}
