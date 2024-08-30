import argparse
import datetime
import pandas as pd

FILM_PERMITS_PATH = "input/Film_Permits.csv"
NOISE_COMPLAINTS_PATH = "input/Noise_Complaints.csv"

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

def main():
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

    print("reading files...")
    film_permits_data = pd.read_csv(FILM_PERMITS_PATH)
    # noise_complaints_data = pd.read_csv(NOISE_COMPLAINTS_PATH)

    print(f"film_permits_data row count: {film_permits_data.count()}")
    # print(f"noise_complaints_data row count: {noise_complaints_data.count()}")

    film_permits_data["StartDateTime"] = film_permits_data["StartDateTime"].astype("datetime64[ns]")
    film_permits_data["EndDateTime"] = film_permits_data["EndDateTime"].astype("datetime64[ns]")
    filtered_film_permits_data = film_permits_data.where((film_permits_data["StartDateTime"] >= startDate) & (film_permits_data["EndDateTime"] <= endDate))
    
    print(f"filtered_film_permits_data row count: {filtered_film_permits_data.count()}")
    

main()