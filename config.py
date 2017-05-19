
########################################################################
##    ###     ###       ###       ###     ### ##### ####    #####    ###
# ####### ########## ######### ######## ##### # ### ### ######## #######
##  #####   ######## ######### ######## ##### ## ## ### #    ####  #####
####  ### ########## ######### ######## ##### ### # ### ### #######  ###
#    ####     ###### ######### ######     ### ####  ####    ####    ####
########################################################################


DEBUG = True

# Make sure the SECRET_KEY is bigger and random and keep it somewhere safe
SECRET_KEY = 'super-secret'


# Flask-Security features
SECURITY_REGISTERABLE = False
SECURITY_SEND_REGISTER_EMAIL = False
SECURITY_RECOVERABLE = False
SECURITY_TRACKABLE = False
SECURITY_CONFIRMABLE = False

# Create in-memory database
#dialect+driver://username:password@host:port/database
SQLALCHEMY_DATABASE_URI = 'sqlite:///./skeleton.db'


# Celery settings
#CELERY_BROKER_URL = 'amqp://localhost//'
#dialect+driver://username:password@host:port/database
#CELERY_BACKEND = 'sqlite:///' + DATABASE_FILE

CELERY_BROKER_URL = 'amqp://localhost//'
#dialect+driver://username:password@host:port/database
CELERY_BACKEND = 'sqlite:///./skeleton.db'



