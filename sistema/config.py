
SECRET_KEY = 'dodocs-eng'
SQLALCHEMY_DATABASE_URI = \
    '{SGDB}://{user}:{senha}@{server}/{database}'.format(
        SGDB= 'mysql+mysqlconnector',
        user = 'root',
        senha = 'trance15',
        server = 'localhost',
        database = 'domanager')

