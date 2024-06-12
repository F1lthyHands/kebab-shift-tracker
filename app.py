from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shifts.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(80), unique=True, nullable=False)

class Shift(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(80), db.ForeignKey('user.user_id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=True)
    end_time = db.Column(db.DateTime, nullable=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_shift', methods=['POST'])
def start_shift():
    data = request.get_json()
    user_id = data['userId']
    user = User.query.filter_by(user_id=user_id).first()
    if not user:
        user = User(user_id=user_id)
        db.session.add(user)
        db.session.commit()
    new_shift = Shift(user_id=user_id, start_time=datetime.now())
    db.session.add(new_shift)
    db.session.commit()
    return jsonify({'message': 'Shift started'})

@app.route('/end_shift', methods=['POST'])
def end_shift():
    data = request.get_json()
    user_id = data['userId']
    shift = Shift.query.filter_by(user_id=user_id, end_time=None).first()
    if shift:
        shift.end_time = datetime.now()
        db.session.commit()
        return jsonify({'message': 'Shift ended'})
    return jsonify({'message': 'No active shift found'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
