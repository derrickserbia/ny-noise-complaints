import argparse
import datetime
import pandas as pd
import time

FILM_PERMITS_PATH = "input/Film_Permits.csv"
NOISE_COMPLAINTS_PATH = "input/Noise_Complaints.csv"

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
        s = noise_complaints_data.loc[(noise_complaints_data["Incident Zip"] == zip) 
                                      & (noise_complaints_data["Created Date"] >= filming_start)
                                      & (noise_complaints_data["Created Date"] <= filming_end)]
        count += s.shape[0]
    return count


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

    print("reading Film_Permits.csv...")
    film_permits_data = pd.read_csv(FILM_PERMITS_PATH, parse_dates=["StartDateTime", "EndDateTime"], na_filter=False)
    
    # filter permits by dates
    filtered_film_permits_data = film_permits_data.loc[(film_permits_data["StartDateTime"] >= startDate)
                                                       & (film_permits_data["StartDateTime"] <= endDate)]
    
    # rename ZipCode(s) colum to ZipCodes
    filtered_film_permits_data = filtered_film_permits_data.rename(columns={"ZipCode(s)": "ZipCodes"})
    
    print("reading Noise_Complaints.csv...")
    global noise_complaints_data
    noise_complaints_data = pd.read_csv(NOISE_COMPLAINTS_PATH, dtype={"Incident Zip": str}, parse_dates=["Created Date"], low_memory=False, na_filter=False)

    noise_complaints_data = noise_complaints_data.loc[(noise_complaints_data["Created Date"] >= startDate)
                                                       & (noise_complaints_data["Created Date"] <= endDate)]
    
    # create new NumNoiseComplaints column applying the getCountOfNoiseComplaints formula on ZipCodes
    filtered_film_permits_data["NumNoiseComplaints"] = filtered_film_permits_data.apply(lambda row: getCountOfNoiseComplaints(row["StartDateTime"], row["EndDateTime"], row["ZipCodes"]), axis=1)

    filtered_film_permits_data.sort_values(by=["NumNoiseComplaints", "StartDateTime", "EventID"], ascending=[False, True, True], inplace=True)

    print(filtered_film_permits_data)

    filtered_film_permits_data.to_csv("output.csv", index=False)

    stopTimer = time.perf_counter()
    print(f"running time={stopTimer - startTimer:0.4f} seconds")

    # pop(item) - Return item and drop from frame.

main()