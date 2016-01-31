import sys
sys.path.insert(0, "/var/www/")
from vulnerable import application,Category,DbObject,Box,Table
from vulnerable import db
import pickle
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
