import argparse
import datetime
import pandas as pd
import time
import requests

FILM_PERMITS_URL = "https://data.cityofnewyork.us/resource/tg4x-b46p.json?$offset={offset}&$where=startdatetime between '{startDate}' and '{endDate}'"
NOISE_COMPLAINTS_URL = "https://data.cityofnewyork.us/resource/p5f6-bkga.json?$offset={offset}&$where=created_date between '{startDate}' and '{endDate}' and Incident Zip in ({zips})"
OFFSET = 1000
noise_complaints_data = None

class Arguments:
    startDate: str
    endDate: str

def parseDate(text: str) -> datetime:
    t = text.split("-")
    if len(t) != 3:
        raise ValueError("could not convert input to date")
    return datetime.datetime(int(t[0]), int(t[1]), int(t[2]))

def parseArguments():
    parser = argparse.ArgumentParser(
        prog="ny-noise-complaints",
        description="Analyzes Film Permits and Noise Complaints datasets to correlate them"
    )
    parser.add_argument("startDate", help="date in the format yyyy-MM-dd")
    parser.add_argument("endDate", help="date in the format yyyy-MM-dd")

    arguments = Arguments()
    parser.parse_args(namespace=arguments)

    return arguments

def getCountOfNoiseComplaints(filming_start, filming_end, filming_zip_codes):
    global noise_complaints_data
    zips = filming_zip_codes.split(",")
    count = 0
    for zip in zips:
        # s = noise_complaints_data.loc[(noise_complaints_data["Incident Zip"] == zip) 
        #                               & (noise_complaints_data["Created Date"] >= filming_start)
        #                               & (noise_complaints_data["Created Date"] <= filming_end)]

        s = noise_complaints_data.loc[(noise_complaints_data["incident_zip"] == zip) 
                                      & (noise_complaints_data["created_date"] >= filming_start)
                                      & (noise_complaints_data["created_date"] <= filming_end)]
        count += s.shape[0]
    return count

def get_all_rows_from_endpoint(url: str, start_date: str, end_date: str) -> list:
    i = 0
    json = []
    while True:
        offset = OFFSET * i
        request_url = url.replace("{startDate}", start_date).replace("{endDate}", end_date).replace("{offset}", str(offset))
        req = requests.request(url=request_url, method="GET")
        res = req.json()
        json.extend(res)
        i += 1

        if res == []:
            break
    
    return json

def main():
    startTimer = time.perf_counter()
    print("running...")
 
    arguments = parseArguments()

    startDate = parseDate(arguments.startDate)
    endDate = parseDate(arguments.endDate)
    if startDate > endDate:
        print("InputError: startDate cannot be greater than endDate")
        print("stopping...")
        return

    print(f"startDate: {startDate}")
    print(f"endDate: {endDate}")

    print("GET /Film-Permit")
    json = get_all_rows_from_endpoint(FILM_PERMITS_URL, arguments.startDate, arguments.endDate)
    film_permits_data = pd.json_normalize(json) # eventid, startdatetime, enddatetime, zipcode_s
    unique_zips_list = film_permits_data["zipcode_s"].str.split(", ").explode().unique().tolist()
    zips_str = "'" + "','".join(unique_zips_list) + "'"
    print(zips_str)

    print("GET /Noise-Complaint")
    json = get_all_rows_from_endpoint(NOISE_COMPLAINTS_URL.replace("{zips}", zips_str), arguments.startDate, arguments.endDate)
    global noise_complaints_data
    noise_complaints_data = pd.json_normalize(json) #incident_zip

    
    # create new NumNoiseComplaints column applying the getCountOfNoiseComplaints formula on ZipCodes
    film_permits_data["NumNoiseComplaints"] = film_permits_data.apply(lambda row: getCountOfNoiseComplaints(row["startdatetime"], row["enddatetime"], row["zipcode_s"]), axis=1)

    film_permits_data.sort_values(by=["NumNoiseComplaints", "startdatetime", "eventid"], ascending=[False, True, True], inplace=True)

    print(film_permits_data)

    film_permits_data.to_csv("output.csv", index=False)

    stopTimer = time.perf_counter()
    print(f"running time={stopTimer - startTimer:0.4f} seconds")

main()