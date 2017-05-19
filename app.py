from flask import Flask, render_template, url_for, request, redirect, \
        session, make_response, g, flash, abort, Markup
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required
from datetime import datetime, timedelta, date
import requests, time, dateutil.parser, pytz, os, sqlite3
from flask.ext.mail import Message, Mail
from flask_wtf import Form
from flask.ext.wtf import Form
from wtforms import TextField, IntegerField, DecimalField, StringField, SelectField, TextAreaField, SubmitField, BooleanField, validators
from wtforms.validators import Required, DataRequired, ValidationError
from wtforms.validators import DataRequired
from wtforms.fields.html5 import DateField, EmailField
from flask.ext.admin.form import widgets
from flask_celery import make_celery
from flask.ext.sqlalchemy import get_debug_queries # works with the gist debugging sqlachemy
import pdfkit
from flask_login import current_user
#from flask_debugtoolbar import DebugToolbarExtension





###########################################################################
################ invoke-rc.d rabbitmq-server start ########################
################ celery -A app.celery worker --loglevel=info ##############
###########################################################################
###########################################################################
################ settings
###########################################################################
###########################################################################

########################################################################
##    ###     ###       ###       ###     ### ##### ####    #####    ###
# ####### ########## ######### ######## ##### # ### ### ######## #######
##  #####   ######## ######### ######## ##### ## ## ### #    ####  #####
####  ### ########## ######### ######## ##### ### # ### ### #######  ###
#    ####     ###### ######### ######     ### ####  ####    ####    ####
########################################################################



# Create app
app = Flask(__name__)
app.config.from_pyfile('config.py')
# Make sure debug = False in production
db = SQLAlchemy(app)
celery = make_celery(app)
#mail=Mail(app)
# Setup Flask-Mail
app.config.update(
    DEBUG=True,
    #EMAIL SETTINGS for google
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    # Dont forget to include user name and password
    MAIL_USERNAME = '',
    MAIL_PASSWORD = '',
    MAIL_FAIL_SILENTLY = 'False'
    )

mail=Mail(app)

######################################################
# ##### #####   #####   ######     ### ########    ###
#  ###  #### ### #### ### #### ####### ####### #######
# # # # ### ##### ### #### ###   ##### ########  #####
# ## ## #### ### #### ### #### ####### ##########  ###
# ##### #####   #####   ######     ###     ###    ####
######################################################




# Creates a many to many relationship for roles and users
roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


# User models
class Role(db.Model, RoleMixin):
    __tablename__= 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    __tablename__= 'user'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))
    confirmed_at = db.Column(db.DateTime())
    last_login_at = db.Column(db.DateTime(), default=datetime.now())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(24))
    current_login_ip = db.Column(db.String(24))
    login_count = db.Column(db.Integer())


# Setup Flask-Security 
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


class Subscribers(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    email = db.Column(db.String(255), unique=False)
    area = db.Column(db.String(255))

    def __init__(self, email=email, area=area):
        self.email = email
        self.area = area


#############################################
#     #####   #####    #### ##### ####    ###
# ######## ### #### ### ###  ###  ### #######
#   ##### ##### ###    #### # # # ####  #####
# ######## ### #### ### ### ## ## ######  ###
# #########   ##### ### ### ##### ###    ####
#############################################

#class ContactForm(Form):
#    firstName = TextField('First Name', [validators.DataRequired("Enter your first name")])
#    lastName = TextField('Last Name', [validators.DataRequired("Enter your last name")])
#    email = TextField('E-mail', [validators.DataRequired("Enter a valid email address"), validators.Email("Enter a valid email address")])
#    subject = TextField('Subject', [validators.DataRequired("What's the nature of your message?")])
#    message = TextAreaField('Message', [validators.DataRequired("Didn't you want to say something?")])
#    submit = SubmitField('Send')



# Contact Form
class ContactForm(Form):
    email = TextField('E-mail', [validators.DataRequired("Enter a valid email address"), validators.Email("Enter a valid email address")])
    message = TextAreaField('Message', [validators.DataRequired("Didn't you want to say something?")])
    submit = SubmitField('Send')
    


####################################################################################
#       ###     ####    ###       #### ##### ###     ###     ### ####### ####    ###
#### ###### ####### ########## ####### ##### ##### ##### ####### ####### ### #######
#### ######   ######  ######## ######## ### ###### #####   ##### ### ### ####  #####
#### ###### ##########  ###### ######### # ####### ##### ######## ## ## #######  ###
#### ######     ###    ####### ########## ######     ###     ##### ### #####    ####
####################################################################################



@app.route('/cu')
def cu():
    return render_template('cu.html', current_user=current_user)

@app.route('/googlef5ce05674f2c2ab6.html')
def googleverify():
    return render_template('googlef5ce05674f2c2ab6.html')


###############################################
# ##### ###     ###     ### ####### ####    ###
# ##### ##### ##### ####### ####### ### #######
## ### ###### #####   ##### ### ### ####  #####
### # ####### ##### ######## ## ## #######  ###
#### ######     ###     ##### ### #####    ####
###############################################
#@app.route('/', methods=('GET', 'POST'))
#def index():
#
#    form = ContactForm()
#    if request.method == 'POST':
#        if form.validate() == False:
#            flash('You must enter something into all of the fields')
#            return render_template('index.html', form = form)
#        else:
#            msg = Message(form.subject.data, sender='vaughndevilliers@gmail.com', recipients=['vaughndevilliers@gmail.com'])
#            msg.body = """
#            From: %s %s <%s>
#            %s
#            """ % (form.firstName.data, form.lastName.data, form.email.data, form.message.data)
#            mail.send(msg)
#            return render_template('index.html', success=True)
#    elif request.method == 'GET':
#        return render_template('index.html',
#            title = 'Contact Us',
#            form = form)

# landing page, no login required
@app.route('/developer', methods=('GET', 'POST'))
def home():

    form = ContactForm()
    if request.method == 'POST':
        if form.validate() == False:
            flash('You must enter something into all of the fields')
            return render_template('index.html', form = form)
        else:
            msg = Message(subject="Little Web", sender='vaughndevilliers@gmail.com', recipients=['vaughndevilliers@gmail.com'])
            msg.body = """
            From: <%s>
            %s
            """ % (form.email.data, form.message.data)
            # Without Celery
            mail.send(msg)
            # With Celery
            #send_async_email.delay(msg)
            return render_template('index.html', success=True)
    elif request.method == 'GET':
            return render_template(
                'index.html',
                title='Home',
                year=datetime.now().year,
                message='Your contact page.',
                form=form)



############################################
#       ###     ###   ######     ####    ###
#### ######## ##### ### #### ####### #######
#### ######## ##### #### ###   ######  #####
#### ######## ##### ### #### ##########  ###
#### ######     ###   ######     ###    ####
############################################


@app.route('/', methods=['GET', 'POST'])
def tides():
    if request.method == 'POST':

        area = request.form['area']

        if request.form['email'] != '':
            email = request.form['email']
            newSubscriber = Subscribers(email, area)
            db.session.add(newSubscriber)
            db.session.commit()


        if area == 'Margate' or 'Port Edward' or 'Port Shepstone' or 'Ramsgate' or 'Southbroom' or 'Amazimtoti' or 'Durban Central' or 'Umhlanga' or 'Richards Bay' or 'Ballito' or 'Kingsburgh' or 'Scottsburgh' or 'St Lucia':
            if area == "Richards Bay" or area == "St Lucia":
                current = requests.get("http://api.wunderground.com/api/408fe6a2816fb9d0/conditions/q/ZA/Richards_Bay.json")
            elif area == "Hibberdene" or area == "Port Shepstone":
                current = requests.get("http://api.wunderground.com/api/408fe6a2816fb9d0/conditions/q/ZA/Port_Shepstone.json")
            elif area == "Port Edward" or area == "Southbroom":
                current = requests.get("http://api.wunderground.com/api/408fe6a2816fb9d0/conditions/q/ZA/Port_Edward.json")
            elif area == "Ramsgate" or area == "Margate":
                current = requests.get("http://api.wunderground.com/api/408fe6a2816fb9d0/conditions/q/ZA/Margate.json")
            else:
                current = requests.get("http://api.wunderground.com/api/408fe6a2816fb9d0/conditions/q/ZA/Durban.json")

            tides = requests.get("https://www.worldtides.info/api?extremes&lat=-29.850833&lon=30.993056&key=7438a1be-d38c-45f5-91dd-ef96f379d048")

            if area == "Hibberdene" or area == "Port Shepstone":
                forecast = requests.get("http://api.wunderground.com/api/408fe6a2816fb9d0/forecast/q/ZA/Port_Shepstone.json")
            elif area == "Port Edward" or area == "Southbroom":
                forecast = requests.get("http://api.wunderground.com/api/408fe6a2816fb9d0/forecast/q/ZA/Port_Edward.json")
            elif area == "Ramsgate" or area == "Margate":
                forecast = requests.get("http://api.wunderground.com/api/408fe6a2816fb9d0/forecast/q/ZA/Margate.json")
            elif area == "Richards Bay" or area == "St Lucia":
                forecast = requests.get("http://api.wunderground.com/api/408fe6a2816fb9d0/forecast/q/ZA/Richards_Bay.json")
            else:
                forecast = requests.get("http://api.wunderground.com/api/408fe6a2816fb9d0/forecast/q/ZA/Durban.json")


        elif area == 'Port St Johns' or 'East London' or 'Port Alfred' or 'Port Elizabeth' or 'Jefferys Bay':
            if area == "Port St Johns":
                current = requests.get("http://api.wunderground.com/api/408fe6a2816fb9d0/conditions/q/ZA/Port_Saint_Johns.json")
            elif area == "East London":
                current = requests.get("http://api.wunderground.com/api/408fe6a2816fb9d0/conditions/q/ZA/East_London.json")
            elif area == "Port Alfred":
                current = requests.get("http://api.wunderground.com/api/408fe6a2816fb9d0/conditions/q/ZA/Port_Alfred.json")
            elif area == "Port Elizabeth":
                current = requests.get("http://api.wunderground.com/api/408fe6a2816fb9d0/conditions/q/ZA/Port_Elizabeth.json")    
            elif area == "Port Alfred" or area == "Jefferys Bay":
                current = requests.get("http://api.wunderground.com/api/408fe6a2816fb9d0/conditions/q/ZA/Port_Alfred.json")

            tides = requests.get("https://www.worldtides.info/api?extremes&lat=-33.029&lon=27.855&key=7438a1be-d38c-45f5-91dd-ef96f379d048")

            if area == "Port St Johns":
                forecast = requests.get("http://api.wunderground.com/api/408fe6a2816fb9d0/forecast/q/ZA/Port_Saint_Johns.json")
            elif area == "East London":
                forecast = requests.get("http://api.wunderground.com/api/408fe6a2816fb9d0/forecast/q/ZA/East_London.json")
            elif area == "Port Alfred":
                forecast = requests.get("http://api.wunderground.com/api/408fe6a2816fb9d0/forecast/q/ZA/Port_Alfred.json")
            elif area == "Port Elizabeth":
                forecast = requests.get("http://api.wunderground.com/api/408fe6a2816fb9d0/forecast/q/ZA/Port_Elizabeth.json")    
            elif area == "Port Alfred" or area == "Jefferys Bay":
                forecast = requests.get("http://api.wunderground.com/api/408fe6a2816fb9d0/forecast/q/ZA/Port_Alfred.json")

        elif area == 'Simons Town' or 'Hout Bay' or 'Camps Bay' or 'Green Point' or 'Hermanus' or 'Mossel Bay' or 'George' or 'Plettenberg Bay':

            if area == "Hermanus":
                current = requests.get("http://api.wunderground.com/api/408fe6a2816fb9d0/conditions/q/ZA/Hermanus.json")
            elif area == "Mossel Bay":
                current = requests.get("http://api.wunderground.com/api/408fe6a2816fb9d0/conditions/q/ZA/Mossel_Bay.json")
            elif area == "George":
                current = requests.get("http://api.wunderground.com/api/408fe6a2816fb9d0/conditions/q/ZA/George.json")
            elif area == "Plettenberg Bay":
                current = requests.get("http://api.wunderground.com/api/408fe6a2816fb9d0/conditions/q/ZA/Plettenberg_Bay.json")
            else:
                current = requests.get("http://api.wunderground.com/api/408fe6a2816fb9d0/conditions/q/ZA/Cape_Town.json")   

            tides = requests.get("https://www.worldtides.info/api?extremes&lat=-33.925&lon=18.424&key=7438a1be-d38c-45f5-91dd-ef96f379d048")

            if area == "Hibberdene":
                forecast = requests.get("http://api.wunderground.com/api/408fe6a2816fb9d0/forecast/q/ZA/Hermanus.json")
            elif area == "Mossel Bay":
                forecast = requests.get("http://api.wunderground.com/api/408fe6a2816fb9d0/forecast/q/ZA/Mossel_Bay.json")
            elif area == "George":
                forecast = requests.get("http://api.wunderground.com/api/408fe6a2816fb9d0/forecast/q/ZA/George.json")
            elif area == "Plettenberg Bay":
                forecast = requests.get("http://api.wunderground.com/api/408fe6a2816fb9d0/forecast/q/ZA/Plettenberg_Bay.json")
            else:
                forecast = requests.get("http://api.wunderground.com/api/408fe6a2816fb9d0/forecast/q/ZA/Cape_Town.json")


        json_object = current.json()
        json_object2 = tides.json()
        json_object3 = forecast.json()

        tides = []
        #time0 = dateutil.parser.parse(time0)
        tz = pytz.timezone('Africa/Johannesburg')
        today_counter = 0
        tomorrow_counter = 0
        day_after_counter = 0
        today = datetime.now().strftime('%Y-%m-%d ')
        tomorrow = datetime.today() + timedelta(days=1)
        tomorrow = tomorrow.strftime('%Y-%m-%d ')
        
        for digit in range(0, 7):

            tide = json_object2['extremes'][digit]['type']
            time = datetime.fromtimestamp(json_object2['extremes'][digit]['dt'], tz)
            date = time.strftime('%Y-%m-%d ')


            if date == today:
                if today_counter == 0:
                    time = time.strftime('%H:%M' + ' today')
                    tides.append({tide:time})
                    today_counter = 1
                else:
                    time = time.strftime('%H:%M')
                    tides.append({tide:time})

            elif date == tomorrow:
                if tomorrow_counter == 0:
                    time = time.strftime('%H:%M' + ' tomorrow')
                    tides.append({tide:time})
                    tomorrow_counter = 1
                else:
                    time = time.strftime('%H:%M')
                    tides.append({tide:time})

            else:
                if day_after_counter == 0:
                    time = time.strftime('%H:%M' + ' day after')
                    tides.append({tide:time})
                    day_after_counter = 1
                else:
                    time = time.strftime('%H:%M')
                    tides.append({tide:time})



        weather = json_object['current_observation']['weather']
        temp = json_object['current_observation']['temp_c']
        wind_kph = json_object['current_observation']['wind_kph']
        wind_dir = json_object['current_observation']['wind_dir']
        icon_url1 = json_object['current_observation']['icon_url']

        today = json_object3['forecast']['txt_forecast']['forecastday'][0]['fcttext_metric']
        tomorrow = json_object3['forecast']['txt_forecast']['forecastday'][2]['fcttext_metric']
        icon_url2 = json_object3['forecast']['txt_forecast']['forecastday'][0]['icon_url']
        icon_url3 = json_object3['forecast']['txt_forecast']['forecastday'][2]['icon_url']

        copyright = json_object2['copyright']

        if area:
            return render_template('tides.html',
                                     area=area,
                                     weather=weather,
                                     temp=temp,
                                     wind_dir=wind_dir,
                                     wind_kph=wind_kph,
                                     icon_url1=icon_url1,
                                     icon_url2=icon_url2,
                                     icon_url3=icon_url3,
                                     tides=tides,
                                     today=today,
                                     tomorrow=tomorrow,
                                     copyright=copyright,
                                     date=datetime.now(),
                                     title='Easy Tides'
                                     )



    else:
        return render_template('fetchtides.html', title='Easy Tides')



if __name__ == '__main__':
    app.run()
