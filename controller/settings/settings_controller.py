import jinja2
import os
import webapp2
import MySQLdb
import logging   # console loglib
import json
#from  climate_control import climateControl


from google.appengine.api import urlfetch  # request  lib
from google.appengine.api import taskqueue



jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__),'/home/infinity/google_appengine/home/view')),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

'''
class Test(webapp2.RequestHandler):

    def get(self):
        climateControl.check=True
        taskqueue.add(url='/tasks', method='POST')
        template = jinja_environment.get_template('test.html')
        self.response.out.write(template.render())

    def post(self):
        climateControl.check=False
        q = taskqueue.Queue('default')
        q.purge()
        return webapp2.redirect('/settings')
'''

class Main_Settings(webapp2.RequestHandler):

    roomcheck = False
    typecheck = False

    def get(self):
        templatevalues = {
            'roomcheck' : Main_Settings.roomcheck,
            'typecheck' : Main_Settings.typecheck,
        }
        template = jinja_environment.get_template('set_main.html')
        self.response.out.write(template.render({'templatevalues':templatevalues}))
        if (Main_Settings.roomcheck == True):
            Main_Settings.roomcheck = False
        if (Main_Settings.typecheck == True):
            Main_Settings.typecheck = False

    def post(self):
        db = MySQLdb.connect(host='127.0.0.1', port=3306, db='home', user='root', passwd='')
        cursor = db.cursor()
        if (self.request.get('roomname') == ''):
            cursor.execute('INSERT INTO Type (devicetype) VALUES (%s)', (self.request.get('devicetype')))
            Main_Settings.typecheck = True
        else:
            cursor.execute('INSERT INTO Room (roomname) VALUES (%s)', (self.request.get('roomname')))
            Main_Settings.roomcheck = True
        db.commit()
        db.close()
        return webapp2.redirect('/settings')

class Device_Settings(webapp2.RequestHandler):
    check = False
    def get(self):
        db = MySQLdb.connect(host='127.0.0.1', port=3306, db='home', user='root', passwd='')
        cursor = db.cursor()
        cursor.execute('SELECT devicetype FROM Type')
        devicetype = cursor.fetchall()
        cursor.execute('SELECT roomname FROM Room')
        room = cursor.fetchall()
        templatevalues = {
            'rooms' : room,
            'devicetypes' : devicetype,
            'pin' : 16,
            'check' : Device_Settings.check,
        }
        if (Device_Settings.check == True):
            Device_Settings.check = False 
        db.close()
        template = jinja_environment.get_template('set_device.html')
        self.response.out.write(template.render({'templatevalues':templatevalues}))
    
    def post(self):
        db = MySQLdb.connect(host='127.0.0.1', port=3306, db='home', user='root', passwd='')
        cursor = db.cursor()
        cursor.execute('INSERT INTO Device (pin,devicetype,roomname) VALUES (%s,%s,%s)',(self.request.get('pin'),self.request.get('devicetype'),self.request.get('room')))
        db.commit()
        Device_Settings.check = True
        db.close()
        return webapp2.redirect('/add-device')
