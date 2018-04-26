# -*- coding: UTF-8 -*-

import datetime
from flask_sqlalchemy impoort SQLAlchemy
from .tempmon import app

db = SQLAlchemy(app)

class Record(db.Model):
    __tablename__ = "records"
    id = Column(db.Integer, primary_key=True)
    host_id = Column(db.String(20), nullable=False)
    host_ip = Column(db.String(20), nullable=False)
    host_type = Column(db.String(50), nullable=False)
    temperature = Column(db.Float, nullable=False)
    humidity = Column(db.Float)
    pressure = Column(db.Float)
    light = Column(db.Float)
    rgb = Column(db.String(100))
    timestamp = Column(db.DateTime, default=datetime.datetime.now)

db.create_all()
