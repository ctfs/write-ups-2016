from flask import Flask, flash
from flask import session, request, render_template, make_response, redirect, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import os, hmac, base64, pickle, hashlib

application = Flask(__name__)

#  static key for CGI
application.secret_key = '2c]E{&\xc0V\xd8\x8d(w\xb5<\x86 !\xda\x0css\xb7\xebAaK\x0e\xee]\xce\xa1VM\x9e"\x19<\xb9\xc6\xd4\x10\xadn\xd8\xcb\xee\tR\x0e\xc2\xcd\xd5\xd9\'\xa4\xd9\xe19\tl\x99&\x9d8\xa8R\xee\xccZ!\xb8\xa4\x94\x80/\x15\xa0\x90V\xc9\xe2OY\xdb\xbak\xe0,\x92\x0e2;\xca\'Kh\x0b\x0b\xd0\xc5\xe6l2\xccX\xe9;\xa5\xe1gK}q?A\xeb\xb7k1"\xc1\x03\x18\xcb\xed\xe4\xa6+\xa1\x18\x02\xa6K\xa2\x00s\x90JE\xd9\x05\'\xe0\x89`?\xee\xea\xb1\xbc^\xe2V\xe6\xb9\x86\xea6\xe2z\xe1Lv\xe7[\x11-\'\xdet}\xbc\x95M9\x88\xd8#A\rb8\x0e)NG\xb0:e\xa5\t\xad\xc3\xd6\x85\x1a\xa7\x98\x16\x81d\x20a\x92\xb9\x05y=\x82z\xd3S\xde\xec\x16\x08\xd9(\xbe\x0eDqo/\xda7\xa6A\x9e\xc2\xa0\x08\xba\xbc$,\xdd\x83N(\'\x1c\xe3\xc2lp\x98S*\xbb\x01\xe1\x1d\x88\x13\xeboQ\x10\x04\xdaSS\xba\x19RW\x98\xed\xcb\xae\x91\xb0SBw\xb7\xee\x15\xae\x01^\x8e\x1aJ\xc8\x03\x82\x08w\xce\xa6y\xb3e\x8d\xae@g\x7eEY\xe3x\xe4\xeewd&\xed\xc9\xde~\r\xb5\x0b\x10\x12\xa7\xa3r\xbe\xe8\xbbE\xa0\xd4|\xb1\x95\x00\xa6\xe3I\xe6.\xb5\xe0rSh\xc1\x18\xe1B\x05x\xb0\x92\xea\xd2\xa5\xc6\x97\x9cb\x84\x18\xb5P\xa2\xc6\xec\xee\xee\x11\xe1X\x1d\xe218 \xc6\xce\xcc\xed\x8c\xc9\xde\x00\x17\xe0`X![\xe88\xe2>LV\xe0\x0c\xd8\xbb\x05T\x8a'


application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/pentesterlab.db'


db = SQLAlchemy(application)


class Box:
  def __init__(self,name):
    self.name = name 
  def __str__(self):
    return "Object: Box[name=\""+self.name+"\"]"


class Table:
  def __init__(self,name):
    self.name = name
  def __str__(self):
    return "Object: Table[name=\""+self.name+"\"]"

class Category(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(255))
  
  def __init__(self, name):
    self.name = name

class DbObject(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(255))
  value = db.Column(db.String(255)) 
  cat_id = db.Column(db.Integer)

  def __init__(self, name,value, cat):
    self.name = name
    self.value = value 
    self.cat_id = cat

db.drop_all()
db.create_all()
a=Category('Usual objects')
b=Category('Unsual objects')
c=Category('Cool objects')
db.session.add(a)
db.session.add(b)
db.session.add(c)
db.session.commit()

x = DbObject("Object 1", None, a.id)
y = DbObject("Object 2", pickle.dumps(Box("Magic Box")).decode(encoding='ISO-8859-1') , b.id)
w = DbObject("Object 4", pickle.dumps(Table("Coffee Table")).decode(encoding='ISO-8859-1') , b.id)
z = DbObject("Object 3", None, c.id)
db.session.add(x)
db.session.add(y)
db.session.add(w)
db.session.add(z)
db.session.commit()

@application.route("/", methods=['GET'])
def index():
  sql = "SELECT * FROM db_object"
  if request.args != [] and request.args.get('cat') != None:
    sql = "SELECT * FROM db_object where cat_id="+request.args.get('cat')
  result = db.engine.execute(sql)
  objects = []
  for row in result:
    val = row[2]  
    if row[2]!= None:
      try:
        print(row[2])
        val = pickle.loads(row[2].encode(encoding='ISO-8859-1')) 
      except Exception as e:
        val = e
    objects.append([row[0],row[1],val,row[3]])
  return render_template('index.html', objects=objects)



if __name__ == "__main__":
  application.run(debug=True)

