import os
import requests
import time

import os
import time
import requests

def get_illinoisFinance(url, destination, max_size_mb=99):
    max_size = max_size_mb * 1024 * 1024 

    try:
        directory = os.path.dirname(destination)
        if directory:
            os.makedirs(directory, exist_ok=True)

        start = time.time()
        part_num = 1
        bytes_written = 0

        # Split files
        base, ext = os.path.splitext(destination)

        with requests.get(url, stream=True, timeout=1200) as response:
            response.raise_for_status()

            output_path = destination
            f = open(output_path, "wb")

            try:
                for chunk in response.iter_content(chunk_size=1024 * 1024):
                    if not chunk:
                        continue

                    chunk_offset = 0

                    while chunk_offset < len(chunk):
                        remaining = max_size - bytes_written
                        bytes_to_write = min(
                            remaining,
                            len(chunk) - chunk_offset
                        )

                        f.write(chunk[chunk_offset:chunk_offset + bytes_to_write])
                        bytes_written += bytes_to_write
                        chunk_offset += bytes_to_write

                        
                        if bytes_written == max_size:
                            f.close()
                            part_num += 1
                            output_path = f"{base}_part{part_num}{ext}"
                            f = open(output_path, "wb")
                            bytes_written = 0

            finally:
                f.close()

        if bytes_written == 0 and part_num > 1:
            if os.path.exists(output_path):
                os.remove(output_path)

        end = time.time()
        time_used = round(end - start, 2)

        if part_num == 1:
            print(
                f"File downloaded successfully to: {destination}. "
                f"Took {time_used} seconds."
            )
        else:
            print(
                f"File downloaded and split into {part_num} parts. "
                f"Took {time_used} seconds."
            )
            for i in range(1, part_num + 1):
                part_path = (
                    destination if i == 1
                    else f"{base}_part{i}{ext}"
                )
                print(f"  {part_path}")

    except requests.exceptions.RequestException as e:
        print("Error downloading the file:", e)
    except OSError as e:
        print("Error saving the file:", e)

if __name__ == "__main__":
    url = 'https://www.elections.il.gov'
    destination = 'folder_path'
    get_illinoisFinance(url, destination)
