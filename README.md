
# Importing Tool from one ATS to Workable ATS

This Python script allows you to import candidate data from a CSV file into your Workable account, following specific requirements.

Developed for Workable for candidate assessment.


## Requirements

- Python 3.x
- Requests library (pip install requests)
- CSV file containing candidate data
- Credentials file (credentials.txt) containing necessary information to connect with the Workable API (Workable API integration token, subdomain)
## Usage/Examples

1. Ensure you have installed Python 3.x and the Requests library.
2. Obtain your Workable API integration token and save it in credentials.txt file.
3. Ensure you have the candidate data in a CSV file named customer_import.csv.
4. Don't forget to replace <your_job_shortcode_here> with the actual job shortcode retrieved from the Workable API.
5. Run the script with the following command:

```python
python import_candidates.py [--talent-pool]
```

- Add --talent-pool argument to import candidates into the Talent Pool.

## Features

- Import candidate data into existing jobs in Workable.
- Appends a 4-letter prefix to candidate email addresses.
- Ensures no email notifications are sent to candidates during the import process.
- Handles errors gracefully and logs relevant information.
- Throttles requests to adhere to the rate limit imposed by the Workable API.
- Provides an option to import candidates into the Talent Pool.

## Notes

- Make sure that `credentials.txt`, `customer_import.csv` and `import_candidates.py` are in the same directory.

## License

This script is licensed under the
[MIT License](https://choosealicense.com/licenses/mit/)

