import argparse
import datetime
import pandas as pd
import time
import os

noise_complaints_data = None

class Arguments:
    start_date: str
    end_date: str
    film_permits_path: str
    noise_complaints_path: str


def parseDate(text: str) -> datetime:
    t = text.split("-")
    if len(t) != 3:
        raise ValueError("could not convert input to date")
    return datetime.datetime(int(t[0]), int(t[1]), int(t[2]))

def file_path(string):
    if os.path.isfile(string):
        return string
    else:
        raise NotADirectoryError(string)

def parseArguments():
    parser = argparse.ArgumentParser(
        prog="ny-noise-complaints",
        description="Analyzes Film Permits and Noise Complaints datasets to correlate them"
    )
    parser.add_argument("--start_date", help="date in the format yyyy-MM-dd")
    parser.add_argument("--end_date", help="date in the format yyyy-MM-dd")
    parser.add_argument("--film_permits_path", default="input/Film_Permits.csv", type=file_path)
    parser.add_argument("--noise_complaints_path", default="input/Noise_Complaints.csv", type=file_path)

    arguments = Arguments()
    parser.parse_args(namespace=arguments)

    return arguments

def initializeArguments():
    arguments = parseArguments()
    start_date = parseDate(arguments.start_date)
    end_date = parseDate(arguments.end_date)
    film_permits_path = arguments.film_permits_path
    noise_complaints_path = arguments.noise_complaints_path
    if start_date > end_date:
        print("InputError: start_date cannot be greater than end_date")
        print("stopping...")
        return

    print(f"start_date: {start_date}")
    print(f"end_date: {end_date}")

    return start_date, end_date, film_permits_path, noise_complaints_path

def getCountOfNoiseComplaints(filming_start, filming_end, filming_zip_codes):
    global noise_complaints_data
    zips = filming_zip_codes.split(",")
    count = 0
    for zip in zips:
        s = noise_complaints_data.loc[(noise_complaints_data["Incident Zip"] == zip.strip()) 
                                      & (noise_complaints_data["Created Date"] >= filming_start)
                                      & (noise_complaints_data["Created Date"] <= filming_end)]
        count += s.shape[0]
    return count



def main():
    startTimer = time.perf_counter()
    print("running...")
 
    start_date, end_date, film_permits_path, noise_complaints_path = initializeArguments()

    print(f"reading {film_permits_path}...")
    film_permits_data = pd.read_csv(film_permits_path, parse_dates=["StartDateTime", "EndDateTime"], na_filter=False)
    
    # filter permits by dates
    filtered_film_permits_data = film_permits_data.loc[(film_permits_data["StartDateTime"] >= start_date)
                                                       & (film_permits_data["StartDateTime"] <= end_date)]
    
    print(f"reading {noise_complaints_path}...")
    global noise_complaints_data
    noise_complaints_data = pd.read_csv(noise_complaints_path, dtype={"Incident Zip": str}, parse_dates=["Created Date"], low_memory=False, na_filter=False)

    noise_complaints_data = noise_complaints_data.loc[(noise_complaints_data["Created Date"] >= start_date)
                                                       & (noise_complaints_data["Created Date"] <= end_date)]
    
    # create new NumNoiseComplaints column applying the getCountOfNoiseComplaints formula on ZipCodes
    filtered_film_permits_data["NumNoiseComplaints"] = filtered_film_permits_data.apply(lambda row: getCountOfNoiseComplaints(row["StartDateTime"], row["EndDateTime"], row["ZipCode(s)"]), axis=1)

    filtered_film_permits_data.sort_values(by=["NumNoiseComplaints", "StartDateTime", "EventID"], ascending=[False, True, True], inplace=True)

    print(filtered_film_permits_data)

    filtered_film_permits_data.to_csv("output.csv", index=False)

    stopTimer = time.perf_counter()
    print(f"running time={stopTimer - startTimer:0.4f} seconds")

    # pop(item) - Return item and drop from frame.

main()