from . import db

class Connectors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(50))
    worker_port = db.Column(db.Integer)
    
class Brokers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    broker_hostname = db.Column(db.Text(40))
    broker_ssl_port = db.Column(db.Integer)
    broker_plain_text_port = db.Column(db.Integer)
