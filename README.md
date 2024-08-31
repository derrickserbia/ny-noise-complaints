# NYC Noise Complaints and Film Permits Analysis

This tool analyzes the relationship between film permits and noise complaints in New York City. It uses two datasets:

- **Film_Permits.csv**: Each row represents a permit granted for filming at a specific location and period of time.
- **Noise_Complaints.csv**: Each row contains noise complaints lodged by NYC residents.

The tool identifies noise complaints that occurred within the same ZIP code and time frame of an active filming permit.

## Prerequisites

- [Python3](https://www.python.org/downloads/)
- [Pandas](https://pandas.pydata.org/): `pip install pandas`
- [Requests](https://pypi.org/project/requests/): `pip install requests`

## How to Run

1. **Download the data:**

   - Film Permits data can be downloaded from: [https://data.cityofnewyork.us/City-Government/Film-Permits/tg4x-b46p/about_data](https://data.cityofnewyork.us/City-Government/Film-Permits/tg4x-b46p/about_data)
   - Noise Complaints data can be downloaded from: [https://data.cityofnewyork.us/Social-Services/311-Noise-Complaints/p5f6-bkga/about_data](https://data.cityofnewyork.us/Social-Services/311-Noise-Complaints/p5f6-bkga/about_data)
   - Keep in mind that filtering the data by dates before downloading can improve performance.
   - After downloading, rename the files to `Film_Permits.csv` and `Noise_Complaints.csv` accordingly.

2. **Place your input files:**

   - Make sure `Film_Permits.csv` and `Noise_Complaints.csv` are located in an `input` folder within the same directory as your scripts.

3. **Run the script:**

   - Open your terminal or command prompt.
   - Navigate to the directory where you have `main.py` and `helper_methods.py`.
   - Execute the following command, providing the required arguments:

   ```bash
   python main.py --start_date yyyy-MM-dd --end_date yyyy-MM-dd
   ```

   - Replace `yyyy-MM-dd` with your desired start and end dates for the analysis (in the format year-month-day).

   - **Optional Arguments**

   - `--film_permits_path`: Specify a different path for the film permits file (default: `input/Film_Permits.csv`).
   - `--noise_complaints_path`: Specify a different path for the noise complaints file (default: `input/Noise_Complaints.csv`).

4. **View the output:**
   - The script will save the results in a file named `output.csv` in the same directory.

## Important Notes

- The script assumes specific column names in your input files (e.g., "StartDateTime", "EndDateTime", "ZipCode(s)" in `Film_Permits.csv`, and "Created Date", "Incident Zip" in `Noise_Complaints.csv`). If your files have different column names, you'll need to adjust the code accordingly.
- The script handles potential errors like invalid date formats or missing files.
- The analysis might take some time depending on the size of your input files.

## Example

```bash
python main.py --start_date 2023-01-01 --end_date 2023-12-31
```

```bash
python main.py --start_date 2023-01-01 --end_date 2023-12-31 --film_permits_path "input/Film_Permits_001.csv" --noise_complaints_path "input/Complaints_001.csv"
```

This will analyze film permits and noise complaints between January 1, 2023, and December 31, 2023.

**Please let me know if you have any other questions or need modifications to the README!**
