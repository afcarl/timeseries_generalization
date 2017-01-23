from app import app
from app import db
from flask import render_template,request
from app.models import *
from app.timeseries_analysis import main
import json
from app.ingest_data import ingest
from app.prediction import main


def prepare_data_for_plotting(data, fitted_values):
    #When x = Contract.objects.all()[0]; is x.contract_start the same as Being Date in the spreadsheet?
    data_object = []
    date_lookup = {}
    import code
    code.interact(local=locals())
    for index in data.index:
        tmp = {}
        timestamp = str(data.ix[index]["Date"])
        timestamp = timestamp.split(" ")[0]
        tmp["date"] = timestamp
        date_lookup[timestamp] = index
        tmp["observed"] = float(datum.hourly_rate_year1)
        data_object.append(tmp)
    for ind,value in enumerate(fitted_values):
        tmp = {}
        timestamp = str(value.start_date)
        timestamp = timestamp.split(" ")[0]
        if timestamp in date_lookup.keys():
            data_object[date_lookup[timestamp]]["fitted"] = float(value.fittedvalue)
            data_object[date_lookup[timestamp]]["lower_bound"] = float(value.lower_bound)
            data_object[date_lookup[timestamp]]["upper_bound"] = float(value.upper_bound)
        else:
            tmp["date"] = timestamp
            tmp["fitted"] = float(value.fittedvalue)
            tmp["lower_bound"] = float(value.lower_bound)
            tmp["upper_bound"] = float(value.upper_bound)
            data_object.append(tmp)
        
    return {"data_object": json.dumps(data_object)}

@app.route("/", methods=["GET","POST"])
def index():
    return "render"

@app.route("/ingest_data",methods=["GET","POST"])
def ingest_data():
    #saving file locally goes here
    csv_file = "nac_events_Y5_fortimeseries.csv"
    ingest("data/"+csv_file)
    return "success"

