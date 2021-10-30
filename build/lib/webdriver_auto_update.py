import os
import requests
import subprocess
import wget
import zipfile


def download_latest_version(version_number, driver_directory):
    """Download latest version of chromedriver to a specified directory.

    :param driver_directory: Directory to save and download chromedriver.exe into.
    :type driver_directory: str
    :param version_number: Latest chromedriver release from chromedriver.storage.googleapis.com.
    :type version_number: str
    :return: None
    """
    print("Attempting to download latest driver online......")
    download_url = "https://chromedriver.storage.googleapis.com/" + version_number + "/chromedriver_win32.zip"
    print(download_url)
    # Download driver as a zip file to specified folder
    latest_driver_zip = wget.download(download_url, out=driver_directory)
    # Read zip file
    with zipfile.ZipFile(latest_driver_zip, 'r') as downloaded_zip:
        # Extract contents from downloaded zip file to specified folder path
        downloaded_zip.extractall(path=driver_directory)
        print(f"\nSuccessfully downloaded version {version_number} to:\n{driver_directory}")
    # Delete the zip file downloaded
    os.remove(latest_driver_zip)
    return


def check_driver(driver_directory):
    """Check local chromedriver version and compare it with latest available version online.

    :param driver_directory: Directory to store chromedriver.exe. Required to add driver_directory to path before using.
    :type driver_directory: str
    :return: True if chromedriver.exe is already in driver_directory, else chromedriver is automatically downloaded.
    """
    # Check for latest chromedriver version online
    latest_release_url = "https://chromedriver.storage.googleapis.com/LATEST_RELEASE"
    response = requests.get(latest_release_url)
    online_driver_version = response.text
    try:
        # Executes cmd line entry to check for existing web-driver version locally
        cmd_run = subprocess.run("chromedriver --version",
                                 capture_output=True,
                                 text=True)
    except FileNotFoundError:
        # Handling case if chromedriver not found in path
        print("No chromedriver.exe found in specified path\n")
        download_latest_version(online_driver_version, driver_directory)
    else:
        # Extract local driver version number as string from terminal output
        local_driver_version = cmd_run.stdout.split()[1]
        print(f"Local chromedriver version: {local_driver_version}")
        print(f"Latest online chromedriver version: {online_driver_version}")
        if local_driver_version == online_driver_version:
            return True
        else:
            download_latest_version(online_driver_version, driver_directory)
