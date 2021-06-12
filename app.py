from flask import Flask,render_template,request,redirect, jsonify
from models import db, Timer, Log
from datetime import datetime
 
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///timetable.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
 
@app.before_first_request
def create_table():
    db.create_all()

starttime = None

@app.route('/' , methods = ['GET','POST'])
def index():
	if request.method == 'GET':
		timers = Timer.query.all()
		return render_template('index.html', timers=timers)

@app.route('/add', methods=['POST'])
def add():
	timer_name = request.form['name']
	new_timer = Timer(minutes=0, name=timer_name)
	db.session.add(new_timer)
	db.session.commit()
	return render_template('index.html', timers=Timer.query.all())



@app.route('/delete' , methods = ['POST'])
def delete():
	full_id = request.form['id']
	id_num = int(full_id[-1])
	timer = Timer.query.filter_by(id = id_num).first()
	#delete timer entires
	logs = Log.query.with_parent(timer).all()
	for log in logs:
		db.session.delete(log)
	#delete timer
	db.session.delete(timer)
	db.session.commit()
	return jsonify({'hide': "timer" + str(id_num)})

@app.route('/start' , methods = ['POST'])
def start():
	global starttime
	starttime = datetime.now()
	return jsonify("success");

@app.route('/save' , methods = ['POST'])
def save():
	print(starttime)
	if starttime:
		id_num = int(request.form['id'])
		worktime = int(request.form['running'])
		timer = Timer.query.filter_by(id = id_num).first()
		endtime = datetime.now()
		log = Log(start = starttime, end=endtime, worktime = worktime, timer=timer.name)
		db.session.add(log)
		timer.minutes = timer.minutes + worktime
		db.session.commit()
		return jsonify("success");
	return jsonify("failure");

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

