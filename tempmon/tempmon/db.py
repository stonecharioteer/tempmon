# -*- coding: UTF-8 -*-

import datetime
from flask_sqlalchemy import SQLAlchemy
from .tempmon import app

db = SQLAlchemy(app)

class Record(db.Model):
    __tablename__ = "records"
    id = db.Column(db.Integer, primary_key=True)
    host_id = db.Column(db.String(20), nullable=False)
    host_ip = db.Column(db.String(20), nullable=False)
    host_type = db.Column(db.String(50), nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Float)
    pressure = db.Column(db.Float)
    light = db.Column(db.Float)
    rgb = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now)

db.create_all()
