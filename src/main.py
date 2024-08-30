import argparse
import datetime

class Arguments:
    startDate: str
    endDate: str

def parseDate(text: str) -> datetime:
    t = text.split("-")
    if len(t) != 3:
        raise ValueError("could not convert input to date")
    return datetime.datetime(int(t[0]), int(t[1]), int(t[2]))

def parseArguments():
    # argparse — Parser for command-line options, arguments and sub-commands
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
    

main()