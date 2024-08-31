import unittest, datetime, pandas as pd, numpy as np

from helper_methods import parse_date, get_count_of_noise_complaints

class TestHelperMethods(unittest.TestCase):

    def test_parse_date_success(self):
        text = "2024-01-01"
        d = parse_date(text)
        self.assertEqual(d, datetime.datetime(2024,1,1))

    def test_parse_date_missing_date_values(self):
        text = "2024-01"
        with self.assertRaises(ValueError):
            parse_date(text)

    def test_parse_date_too_many_date_values(self):
        text = "2024-01-01 01"
        with self.assertRaises(ValueError):
            parse_date(text)
    
    def test_parse_date_invalid_date_values(self):
        text = "2024-01-32"
        with self.assertRaises(ValueError):
            parse_date(text)

    def test_get_count_of_noise_complaints_all_applicable_to_one_film_permit(self):
        noise_complaints_data = pd.DataFrame({
            "Incident Zip": np.array(["12345"] * 5, dtype=str),
            "Created Date": pd.Timestamp("20240101")
        })
        start_date = datetime.datetime(2024, 1, 1)
        end_date = datetime.datetime(2024, 1, 2)
        filming_zip_codes = "12345"
        c = get_count_of_noise_complaints(start_date, end_date, filming_zip_codes, noise_complaints_data)
        self.assertEqual(c, 5)

    def test_get_count_of_noise_complaints_all_applicable_to_one_film_permit_multiple_zips(self):
        noise_complaints_data = pd.DataFrame({
            "Incident Zip": np.concatenate((np.array(["12345"] * 5, dtype=str), np.array(["54321"] * 5, dtype=str))),
            "Created Date": np.concatenate((np.array([pd.Timestamp("20240101")] * 5), np.array([pd.Timestamp("20240102")] * 5)))
        })
        start_date = datetime.datetime(2024, 1, 1)
        end_date = datetime.datetime(2024, 1, 2)
        filming_zip_codes = "12345, 54321"
        c = get_count_of_noise_complaints(start_date, end_date, filming_zip_codes, noise_complaints_data)
        self.assertEqual(c, 10)

    def test_get_count_of_noise_complaints_not_all_applicable_to_one_film_permit_multiple_zips(self):
        noise_complaints_data = pd.DataFrame({
            "Incident Zip": np.concatenate((np.array(["12345"] * 5, dtype=str), np.array(["54321"] * 5, dtype=str))),
            "Created Date": np.concatenate((np.array([pd.Timestamp("20240101")] * 5), np.array([pd.Timestamp("20240102")] * 5)))
        })
        start_date = datetime.datetime(2024, 1, 1)
        end_date = datetime.datetime(2024, 1, 2)
        filming_zip_codes = "12345, 12346"
        c = get_count_of_noise_complaints(start_date, end_date, filming_zip_codes, noise_complaints_data)
        self.assertEqual(c, 5)

if __name__ == "__main__":
    unittest.main()