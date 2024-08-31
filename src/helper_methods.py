import datetime, argparse, os

class Arguments:
    start_date: str
    end_date: str
    film_permits_path: str
    noise_complaints_path: str

def parse_date(text: str) -> datetime:
    t = text.split("-")
    if len(t) != 3:
        raise ValueError("could not convert input to date")
    return datetime.datetime(int(t[0]), int(t[1]), int(t[2]))

def file_path(string):
    if os.path.isfile(string):
        return string
    else:
        raise FileNotFoundError(string)

def parse_arguments():
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

def initialize_arguments():
    arguments = parse_arguments()
    start_date = parse_date(arguments.start_date)
    end_date = parse_date(arguments.end_date)
    film_permits_path = arguments.film_permits_path
    noise_complaints_path = arguments.noise_complaints_path
    if start_date > end_date:
        print("InputError: start_date cannot be greater than end_date")
        print("stopping...")
        return

    print(f"start_date: {start_date}")
    print(f"end_date: {end_date}")

    return start_date, end_date, film_permits_path, noise_complaints_path

def get_count_of_noise_complaints(filming_start, filming_end, filming_zip_codes, noise_complaints_data):
    zips = filming_zip_codes.split(",")
    count = 0
    for zip in zips:
        s = noise_complaints_data.loc[(noise_complaints_data["Incident Zip"] == zip.strip()) 
                                      & (noise_complaints_data["Created Date"] >= filming_start)
                                      & (noise_complaints_data["Created Date"] <= filming_end)]
        count += s.shape[0]
    return count