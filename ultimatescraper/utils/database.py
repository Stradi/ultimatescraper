from scrapy.utils.project import get_project_settings

_PROJECT_SETTINGS = get_project_settings()


def get_connection_args_for_peewee():
    return {
        'host': _PROJECT_SETTINGS.get('DB_HOST'),
        'user': _PROJECT_SETTINGS.get('DB_USER'),
        'password': _PROJECT_SETTINGS.get('DB_PASS'),
        'ssl_ca': _PROJECT_SETTINGS.get('DB_SSL_CERT'),
    }


def get_database_name():
    return _PROJECT_SETTINGS.get('DB_NAME')
