import requests
import time

def download_rules(url, filename):
    """
    Download the Snort rules from a given URL and save them in a file.

    :param url: URL of the list of the rules to download.
    :param filename: Name of the file where the rules will be save.
    """
    print(f"Download of rules from {url}...")
    response = requests.get(url)
    if response.status_code == 200:
        with open("rules/" + filename, "w") as file:
            file.write(response.text)
        file.close()
        print(f"Rules saved in {filename}")
    else:
        print(f"Failed to download the rules from {url} (code statut: {response.status_code})")

def main():
    urls_and_filenames = {
        "https://sslbl.abuse.ch/blacklist/sslipblacklist.rules": "sslipblacklist.rules",
        "https://feodotracker.abuse.ch/downloads/feodotracker.rules": "feodotracker.rules",
        "https://urlhaus.abuse.ch/downloads/ids": "urlhaus.rules"
    }

    while True:
        for url, filename in urls_and_filenames.items():
            download_rules(url, filename)
        time.sleep(10)  # Break of 5 minutes

if __name__ == "__main__":
    main()
