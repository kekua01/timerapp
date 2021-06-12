from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
 
db = SQLAlchemy()
 
class Timer(db.Model):

	id = db.Column(db.Integer, primary_key=True)
	minutes = db.Column(db.Integer)
	name = db.Column(db.String())

	entries = db.relationship('Log', backref='parent', cascade="all, delete")

	def __repr__(self):
		return '<Timer {}>'.format(self.name)


class Log(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	start = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	end = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	worktime = db.Column(db.Integer)

	timer = db.Column(db.String(), db.ForeignKey('timer.name'))

	def __repr__(self):
		return '<Timer {}>'.format(self.id)
