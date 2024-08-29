# Project Details

**Requirements:**

- **Input:** The tool should allow the user to input a specific date range.

- **Output:**
  - The tool should generate a list of filming permits along with the number of correlated noise complaints.
  - The results should be sorted by the number of complaints in descending order. In case of ties, sort first by StartDateTime in ascending order, and then by EventID in ascending order.
  - The sorted list should be exported to a CSV file containing all filming permits for the user-specified date range. The format should match the original Filming Permit data, with the addition of a column named NumNoiseComplaints to represent the number of correlated noise complaints.

**Deliverable:**

- A zip file containing:
  - The source code for the command-line tool.
  - Documentation that explains how to use the tool and how to set up any prerequisites.
  - A CSV file containing the sorted results for all filming permits from July 1 - September 30, 2023.

**Considerations:**

- Don't worry about gathering or displaying any data from before 2023.
- Some film permits can span multiple ZIP codes at once. Make sure to count up all the complaints from all the relevant ZIP codes!
- The primary user of this tool will be a technically-capable user who is expected to run it once every few months. Consider tradeoffs accordingly.
- Use any language, technology, or process that you see fit, as long as you document how it should be used.
