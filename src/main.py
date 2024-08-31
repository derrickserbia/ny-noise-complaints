import pandas as pd
import time
from helper_methods import initialize_arguments, get_count_of_noise_complaints


def main():
    startTimer = time.perf_counter()
    print("running...")
 
    start_date, end_date, film_permits_path, noise_complaints_path = initialize_arguments()

    print(f"reading {film_permits_path}...")
    film_permits_data = pd.read_csv(film_permits_path, parse_dates=["StartDateTime", "EndDateTime"], na_filter=False)
    filtered_film_permits_data = film_permits_data.loc[(film_permits_data["StartDateTime"] >= start_date)
                                                       & (film_permits_data["StartDateTime"] <= end_date)]
    
    print(f"reading {noise_complaints_path}...")
    noise_complaints_data = pd.read_csv(noise_complaints_path, dtype={"Incident Zip": str}, parse_dates=["Created Date"], low_memory=False, na_filter=False)
    noise_complaints_data = noise_complaints_data.loc[(noise_complaints_data["Created Date"] >= start_date)
                                                       & (noise_complaints_data["Created Date"] <= end_date)]
    
    # create new NumNoiseComplaints column applying the get_count_of_noise_complaints formula on ZipCodes
    filtered_film_permits_data["NumNoiseComplaints"] = filtered_film_permits_data.apply(lambda row: get_count_of_noise_complaints(row["StartDateTime"], row["EndDateTime"], row["ZipCode(s)"], noise_complaints_data), axis=1)

    filtered_film_permits_data.sort_values(by=["NumNoiseComplaints", "StartDateTime", "EventID"], ascending=[False, True, True], inplace=True)

    print(filtered_film_permits_data)

    filtered_film_permits_data.to_csv("output.csv", index=False)

    stopTimer = time.perf_counter()
    print(f"running time={stopTimer - startTimer:0.4f} seconds")

main()
