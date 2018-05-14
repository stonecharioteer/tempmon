from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
import requests
import os
import json

sqllite_file = os.path.join(os.path.dirname(
    os.path.realpath(__file__)), "tempcache.db")
uri = "sqlite:///" + sqllite_file
engine = create_engine(uri, echo=False)
Base = declarative_base()

class Record(Base):
    __tablename__ = "records"
    id = Column(Integer, primary_key=True)
    host_id = Column(String(20), nullable=False)
    host_ip = Column(String(20), nullable=False)
    host_type = Column(String(50), nullable=False)
    temperature = Column(Float, nullable=False)
    humidity = Column(Float)
    pressure = Column(Float)
    light = Column(Float)
    rgb = Column(String(100))
    timestamp = Column(DateTime, default=datetime.datetime.now)

Base.metadata.create_all(engine)

hosts = [("192.168.1.{}".format(x), "component") for x in range(100, 256)]# + [("192.168.1.4", "component")]

# After identifying all hosts on network, identify valid ones.
tempmon_hosts = []
for host in hosts:
    ip = host[0]
    hostname = host[1]
    # print("Scanning {}".format(ip))
    try:
        who_request = requests.get(
            "http://{}/whoami".format(ip), timeout=0.3)
        # check if response is valid.
        # If it is, then read the response and identify the host.
        if who_request.status_code == 200:
            try:
                response = who_request.json()
                host_type = response["type"]
                if host_type == "nodemcu":
                    host_id = response["name"]
                else:
                    host_id = response["id"]
                tempmon_hosts.append(
                    {"ip": ip, "type": host_type, "id": host_id})
                print("Detected: {} {} {}".format(ip, host_type, host_id))
            except ValueError:
                print("Invalid json. {}".format(who_request.text))
            except:
                raise
        else:
            print("{} : {}".format(ip, who_request.status_code))
            print("{} : {}".format(ip, who_request.reason))
            print("{} : {}".format(ip, who_request.text))
    except requests.exceptions.RequestException:
        print("No tempmon service running on {}".format(host[0]))
        pass
    except:
        raise

Session = sessionmaker(bind=engine)
session = Session()

for host in tempmon_hosts:
    host_id = host["id"]
    ip = host["ip"]
    host_type = host["type"]

    if host_type == "nodemcu":
        response = requests.get("http://{}/measure/3".format(ip))
        temperature = round(float(response.json()["temperature"]), 3)
        humidity = round(float(response.json()["humidity"]), 3)


    if host_type in ["sensehatpi"]:
        response = requests.get("http://{}/humidity".format(ip))
        humidity = round(float(response.json()["humidity"]), 3)

    if host_type in ["sensehatpi", "enviropi"]:
        response = requests.get("http://{}/pressure".format(ip))
        pressure = round(float(response.json()["pressure"]), 3)

    if host_type == "enviropi":
        response = requests.get("http://{}/light".format(ip))
        light = round(float(response.json()["light"]), 3)
        rgb = ",".join([str(x) for x in response.json()["rgb"]])
    if host_type == "nodemcu":
        # append to db.
        new_record = Record(host_id=host_id, host_ip=ip, host_type=host_type,
                            temperature=temperature, humidity=humidity)
        session.add(new_record)
    elif host_type == "sensehatpi":
        # append to db
        new_record = Record(host_id=host_id, host_ip=ip, host_type=host_type,
                            temperature=temperature, humidity=humidity, pressure=pressure)
        session.add(new_record)
    elif host_type == "enviropi":
        new_record = Record(host_id=host_id, host_ip=ip, host_type=host_type,
                            temperature=temperature, pressure=pressure, light=light, rgb=rgb)
        # append to db
        session.add(new_record)
        
session.commit()
