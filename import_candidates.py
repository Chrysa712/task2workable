import csv
import requests
import logging
import time
import sys

# Initialize variables to store subdomain and token
subdomain = None
api_token = None

# Open the file and read its contents
with open('credentials.txt', "r") as file:
    for line in file:
        # Split the line by ":" and strip whitespace
        key, value = map(str.strip, line.split(":"))
        # Check if the key is 'subdomain' or 'token'
        if key == 'subdomain':
            subdomain = value
        elif key == 'token':
            api_token = value

# Set up logging
logging.basicConfig(filename='import.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to modify email address based on the requirement
def modify_email(email, name):
    parts = name.split()
    prefix = parts[0][0] + parts[-1][:2] + '_'
    modified_email = prefix + email
    return modified_email.lower()

# Function to import candidates into Workable
def import_candidates(candidate_data, job_shortcode, to_talent_pool=False):
    url = f"https://{subdomain}.workable.com/spi/v3/jobs/{job_shortcode}/candidates"
    # Optionally, add candidate to talent pool
    if to_talent_pool:
        url = f"https://{subdomain}.workable.com/spi/v3/talent_pool/stage/candidates"
    headers = {
        "accept": "application/json",
        'Authorization': 'Bearer {}'.format(api_token),
        'Content-Type': 'application/json'
    }

    time_interval = 10 / 10  # Rate limit: 10 requests every 10 seconds

    for candidate in candidate_data:
        # Transform data as per requirements
        name = candidate['First Name'] + ' ' + candidate['Last Name']
        email = modify_email(candidate['Email'], 'Chrysa Rizeakou')
        address = f"{candidate['Address']}, {candidate['Address 2']}, {candidate['City']}, {candidate['State']}, {candidate['Country']}, {candidate['Zip']}"
        source = candidate['Referred By']
        job_title = candidate['Position'] #it matches exactly with the corresponding one in Workable.Is another check needed?
        disqualified = candidate['Status'] == 'Rejected'

        # Construct payload
        payload = {
            "sourced": True, #set to true so no email notifications be sent to candidates during the import process
            "candidate": {
                "name": name,
                "email": email,
                "phone": candidate['Phone'],
                "address": address,
                "source": source,
                "disqualified": disqualified
            }
        }
        # if payload['candidate']['name'] == 'John Doe':
        #     print(payload)
        print(payload)

        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            logging.info(f"Successfully imported candidate {name} for job {job_title}")
        except Exception as e:
            logging.error(f"Error importing candidate {name}: {e}")

        # Throttle requests
        time.sleep(time_interval)



# Read candidate data from CSV 2
with open('customer_import.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    candidate_data = list(reader)


# Determine job shortcode
# job_shortcode = <your_job_shortcode_here>
job_shortcode = "F8D1EA3849"

# Check if the script was called with the talent pool argument
to_talent_pool = False
if len(sys.argv) > 1 and sys.argv[1] == "--talent-pool":
    to_talent_pool = True

# Import candidates into Workable
import_candidates(candidate_data, job_shortcode)


