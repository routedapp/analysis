
# Import necessary modules or packages
import requests
from data import processData

# Define functions or classes if required
def main():
    # Your code here
    service_calls_base_url = 'https://data.sfgov.org/resource/RowID.json'

    filters = {
        'call_type': 'Medical Incident',
        '$order': 'call_date DESC',

    }

    api_key = "1t43a568i2ojhn4rpgthr7o3u"
    api_secret = "3fmtl0ym0tfl0riykpkmsty9vtixktsy6bd6gsbm5wwkwzl5mp"

    credentials = (api_key, api_secret)

    response = requests.get(service_calls_base_url, params=filters, auth=credentials)
    if response.status_code == 200:
        # Request was successful
        data = response.json()  # Get the response data as JSON
        # Process the data as needed
        processData(data)
        #print(json.dumps(data, indent=2))
    else:
        # Request failed
        print('Request failed with status code:', response.status_code)


# Call the main function to execute your script
if __name__ == '__main__':
    main()