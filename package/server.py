from flask import Flask, request, Response
from flask_mail import Mail, Message
from flask_ipban import IpBan
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from datetime import datetime
import logging

app = Flask(__name__)

#IpBan for maintaining a list of blacklisted IPs 
ip_ban = IpBan(ban_seconds=200)
ip_ban.init_app(app) 

# Mailtrap.io testing mail server, configure as : https://mailtrap.io/blog/flask-email-sending/
app.config['MAIL_SERVER']='smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = '750a841d7f6c5c' #Please update the mailtrap username with your own testing account 
app.config['MAIL_PASSWORD'] = '1ab4df7491eda9'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)

#database connection
engine = create_engine("postgresql://postgres:postgres@postgres:5432")
database = scoped_session(sessionmaker(bind=engine))
#Db Creation
database.execute("SELECT 'CREATE DATABASE denied_access' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'denied_access')")
database.close()

db_engine = create_engine("postgresql://postgres:postgres@postgres:5432/denied_access")
db = scoped_session(sessionmaker(bind=db_engine))
#Db initilization
db.execute("CREATE TABLE IF NOT EXISTS denied_access_ledger(path VARCHAR, ip_address INET,  time TIMESTAMP);")
db.commit()

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

# Feature a) App responds to the URL like 'http://host:port/?n=x' and returns n*n.
@app.route('/')
def data():
    # n is the value passed as a query
    data = request.args.get('n')
    result = float(data)**2
    return str(result)
    
# Feature b) App responds to the URL 'http://host:port/blacklisted' with Db operations
@app.route('/blacklisted')
def index():
  user_ip = request.remote_addr
  ip_ban.block(user_ip, permanent=False)
  msg = Message('Access Blocked!', sender =  'admin@domain.com', recipients = ['test@domain.com'])
  msg.body = f'Response from admin@domain.com, Your IP address {user_ip} is blocked on our systems!!'
  mail.send(msg)
  ip_ban.add()
  path = '/blacklisted'
  ip_address=str(user_ip)
  now = datetime.now()
  #inserting the detail for denied access with timestamp
  db.execute("INSERT INTO denied_access_ledger (path, ip_address, time) VALUES (:path, :ip_address, :time)",
        {"path": path, "ip_address": user_ip, "time": now }) 
  db.commit() 
  app.logger.error('Access to this endpoint is blocked!')

  return Response(status=444)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5004,debug=True)