import bz2
import json
from datetime import datetime
import pandas as pd

def create_csv_file(data):
    date = datetime.now()
    date = date.strftime("%m-%d-%H:%M:%S")
    
    df = pd.DataFrame(data)
    df.set_index("qid").to_csv(date + ".csv")

    return {"qid":[], "Dfr":[]}

i = 0
data = {"qid":[], "Dfr":[]}
for line in bz2.BZ2File("latest-all.json.bz2", "r"):
    try:
        if i > 0:
            line = line.decode("utf-8").strip('\n').strip(',')
            js = json.loads(line)   
            if js["type"] == "item":
                if "P31" in js["claims"]:
                    if js["claims"]["P31"][0]["mainsnak"]["datavalue"]["value"]["id"] == "Q13442814": # Is a scholarly article
                        print(i)
                        if "fr" not in js["descriptions"]:
                            if "P577" in js["claims"]: # Date of publication exists
                                if js["claims"]["P577"][0]["mainsnak"]["datavalue"]["value"]["precision"] >= 9:
                                    year, _, _ = js["claims"]["P577"][0]["mainsnak"]["datavalue"]["value"]["time"].split("-")
                                    year = year[1:]
                                    if int(year) >= 1980:
                                        data["qid"].append(js["id"])
                                        data["Dfr"].append("article scientifique publié en {}".format(year))
                            else:
                                data["qid"].append(js["id"])
                                data["Dfr"].append("article scientifique")
                            
                            if len(data["qid"]) >= 25000:
                                data = create_csv_file(data)


        i += 1
    except Exception as e:
        pass

