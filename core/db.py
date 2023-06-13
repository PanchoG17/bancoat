import os

BASE_DIR= os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SQL_LITE ={
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    },
}

SQL_SERVER_LOC = {
    "default": {
        "ENGINE": "mssql",
        "NAME": "db_name",
        "USER": "db_user",
        "PASSWORD": "db_pass",
        "HOST": "localhost",
       # "PORT": "1433",
        "OPTIONS": {"driver": "ODBC Driver 17 for SQL Server",
        },
    },
}

SQL_SERVER_PRD ={
    "default": {
        "ENGINE": "mssql",
        "NAME": "db_name",
        "USER": "db_user",
        "PASSWORD": "db_pass",
        "HOST":"db_host",
        "PORT": "1433",
        "OPTIONS": {"driver": "ODBC Driver 17 for SQL Server",
        },
    },
}

SQL_SERVER_PRD = {
    "default": {
        "ENGINE": "mssql",
        "NAME": "db_banco_prd",
        "USER": "sa",
        "PASSWORD": "8f43bdeFmzivyUEcyiyK",
        "HOST": "10.1.9.86",
        # "PORT": "1433",
        "OPTIONS": {"driver": "ODBC Driver 17 for SQL Server",
        },
    },
}