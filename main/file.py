import os
import random
import datetime

def GenerateName(number=None):
    """
    Generate a random name for a file.
    """
    now = datetime.datetime.now()
    date = now.strftime("%Y%m%d")
    random_number = random.randint(1000, 9999)

    return f"urls-{date}-{str(random_number)}.txt"

def WriteFile(urls, filename, path=None, test=None) -> None:
    """
    Write URLs to a file.
    """
    if not urls or len(urls) == 0:
        if not test:
            print("Data urls is empty, nothing to write to file, skipping process")
        return

    path = path or 'output'

    if not os.path.exists(path):
        os.makedirs(path)
    if not os.path.exists(f"{path}/{filename}"):
        open(f"{path}/{filename}", "w").close()

    with open(f"{path}/{filename}", "w") as file:
        for url in urls:
            file.write(f"{url}\n")

    if not test:
        print(f"File {filename} has been created with {len(urls)} urls")