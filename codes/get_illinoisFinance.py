import os
import requests
import time

def get_illinoisFinance(url, destination):
    try:
        directory = os.path.dirname(destination)
        if directory:
            os.makedirs(directory, exist_ok=True)

        with requests.get(url, stream=True, timeout=1200) as response:
            start = time.time()
            response.raise_for_status()

            with open(destination, 'wb') as f:
                for chunk in response.iter_content(chunk_size=2500):
                    if chunk:
                        f.write(chunk)
        end = time.time()
        time_used = round((end - start), 2)
        print(f"File downloaded successfully to: {destination}. Took {time_used} seconds.")

    except requests.exceptions.RequestException as e:
        print("Error downloading the file:", e)
    except OSError as e:
        print("Error saving the file:", e)

if __name__ == "__main__":
    url = 'https://www.elections.il.gov'
    destination = 'folder_path'
    get_illinoisFinance(url, destination)
