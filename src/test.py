import pandas as pd

noise_complaints_data = pd.DataFrame(
        {
            "Created Date": [
                pd.Timestamp('2024-01-01 00:01:00'),
                pd.Timestamp('2024-01-01 00:01:00'),
                pd.Timestamp('2024-01-01 00:01:00'),
                pd.Timestamp('2024-01-01 00:01:00'),
                pd.Timestamp('2024-01-01 00:01:00'),
                pd.Timestamp('2024-01-02 00:01:00'),
                pd.Timestamp('2024-01-02 00:01:00'),
                pd.Timestamp('2024-01-02 00:01:00'),
                pd.Timestamp('2024-01-02 00:01:00'),
                pd.Timestamp('2024-01-02 00:01:00')
            ],
            "Incident Zip": [
                "12345",
                "12345",
                "12345",
                "12345",
                "12346",
                "12346",
                "12344",
                "12344",
                "12344",
                "12344"
            ]
        }
    )

def getCountOfNoiseComplaints(filming_start, filming_end, filming_zip_codes):
    global noise_complaints_data
    zips = filming_zip_codes.split(",")
    count = 0
    for zip in zips:
        s = noise_complaints_data.loc[(noise_complaints_data["Incident Zip"] == zip) 
                                      & (noise_complaints_data["Created Date"] >= filming_start)
                                      & (noise_complaints_data["Created Date"] <= filming_end)]
        print(f"s.count().count()=\n{s.value_counts().count()}\n")
        count += s.shape[0]
    return count

def main():
    df_film_permits = pd.DataFrame(
        {
            "StartDateTime": [
                pd.Timestamp('2024-01-01 00:00:00'),
                pd.Timestamp('2024-01-02 00:00:00')
            ],
            "EndDateTime": [
                pd.Timestamp('2024-01-02 00:00:00'),
                pd.Timestamp('2024-01-03 00:01:00')
            ],
            "ZipCodes": [
                "12345, 12344",
                "12346"
            ]
        }
    )

    print(df_film_permits)
    print("\n")

    global noise_complaints_data
    print(noise_complaints_data)
    print("\n")

    df_film_permits["NumNoiseComplaints"] = df_film_permits.apply(lambda row: getCountOfNoiseComplaints(row["StartDateTime"], row["EndDateTime"], row["ZipCodes"]), axis=1)

    print(df_film_permits)


main()