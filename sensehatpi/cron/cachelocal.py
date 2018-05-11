from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
import os
import sense_hat

sqlite_file = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), "tempcache.db")
uri = "sqlite:///" + sqlite_file
engine = create_engine(uri, echo=False)
Base = declarative_base()

class Record(Base):
    __tablename__ = "records"
    id = Column(Integer, primary_key=True)
    temperature_h = Column(Float, nullable=False)
    temperature_p = Column(Float, nullable=False)
    humidity = Column(Float)
    pressure = Column(Float)
    light = Column(Float)
    rgb = Column(String(100))
    timestamp = Column(DateTime, default=datetime.datetime.now)

Base.metadata.create_all(engine)


def summarize():
    import pandas as pd
    import sqlite3
    import datetime
    import logging 
    logging.basicConfig(format="%(message)s", level=logging.INFO)
    global sqlite_file
        
    with sqlite3.connect(sqlite_file) as con:
        df = pd.read_sql("SELECT * from records", con)
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    last_day = (datetime.datetime.now() - datetime.timedelta(minutes=24*60))
    df_one_day = df.loc[df["timestamp"] >= last_day]
    logging.info(df_one_day.describe())


def detect_increase():
    import pandas as pd
    import sqlite3
    import datetime
    from sense_hat import SenseHat

    global sqlite_file
    
    with sqlite3.connect(sqlite_file) as con:
        df = pd.read_sql("SELECT * from records", con)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    # If the moving mean for the last two days is much higher or lower than
    # that of the last one day.
    last_two_days = (datetime.datetime.now()-datetime.timedelta(minutes=24*60*2))
    df_two_days = df.loc[df["timestamp"] >= last_two_days]
    h_mean_two_days = df_two_days["humidity"].mean()

    last_day = (datetime.datetime.now() - datetime.timedelta(minutes=24*60))
    df_one_day = df.loc[df["timestamp"] >= last_day]
    h_mean_one_day = df_one_day["humidity"].mean()
    difference_percentage = (h_mean_one_day - h_mean_two_days)/h_mean_two_days*100.00
    abs_diff = abs(difference_percentage)

    if abs_diff >= 100:
        # if the absolute difference has doubled:
        s = SenseHat()
        s.set_rotation(180)
        for i in range(5):
            s.show_message("H: {}% ({}) in 48h".format(difference_percentage, 
                "Decrease" if difference_percentage<0 else "Increase"), 
                    text_colour=[255,0,0],scroll_speed=0.3)
        s.clear()
        s.set_rotation(0)


def record_sensors():
    import sense_hat
    s = sense_hat.SenseHat()
    temp_h = s.get_temperature_from_humidity() - 4 # correction factor.
    temp_p = s.get_temperature_from_pressure() - 4 # correction factor.
    humidity = s.get_humidity()
    pressure = s.get_pressure()

    Session = sessionmaker(bind=engine)
    session = Session()

    # append to db
    new_record = Record(
            temperature_h=temp_h, 
            humidity=humidity,
            temperature_p=temp_p,
            pressure=pressure)
    session.add(new_record)
        
    session.commit()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-c","--check_humidity_change", action="store_true")
    parser.add_argument("-s","--summary",action="store_true")
    args = parser.parse_args()
    if not args.summary:
        if not args.check_humidity_change:
            record_sensors()
        else:
            detect_increase()
    else:
        summarize()
    
