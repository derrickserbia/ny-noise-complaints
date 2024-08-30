import argparse

def main():
    print("running...")
 
    # argparse — Parser for command-line options, arguments and sub-commands
    parser = argparse.ArgumentParser(
        prog="ny-noise-complaints",
        description="Analyzes Film Permits and Noise Complaints datasets to correlate them"
    )

    parser.add_argument("startDate", help="date in the format yyyy-MM-dd")
    parser.add_argument("endDate", help="date in the format yyyy-MM-dd")

    args = parser.parse_args()

main()