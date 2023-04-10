import os
import platform
import requests
import subprocess
import sys
import wget
import zipfile
from pathlib import Path


def download_latest_version(version_number, driver_directory):
    """
    Download latest version of chromedriver to a specified directory.

    Args:
        version_number (str): Latest online chromedriver release from chromedriver.storage.googleapis.com.
        driver_directory (str): Directory to save and download chromedriver files into.

    Returns:
        None
    """ 
    download_url = "https://chromedriver.storage.googleapis.com/" + version_number + "/chromedriver_" + obtain_os() + ".zip"
    print("Attempting to download latest available driver ......")
    print(download_url)
    # Download driver as a zip file to specified folder
    latest_driver_zip = wget.download(download_url, out=driver_directory)
    # Read zip file
    with zipfile.ZipFile(latest_driver_zip, 'r') as downloaded_zip:
        # Extract contents from downloaded zip file to specified folder path
        downloaded_zip.extractall(path=driver_directory)
    # Delete the zip file downloaded
    os.remove(latest_driver_zip)
    print(f"\nSuccessfully downloaded chromedriver version {version_number} to:\n{driver_directory}")
    return


def check_driver(driver_directory):
    """
    Check local chromedriver version and compare it with latest available version online.

    Args:
        driver_directory (str): Directory to store chromedriver executable. Required to add driver_directory to path before using.

    Returns:
        bool: True if chromedriver executable is already in driver_directory, else it is automatically downloaded.
    """
    # Strip '/' and '\' 
    if (driver_directory[0] == '/' or driver_directory[0] == '\\'):
        driver_directory = driver_directory[1:]
    # Creating the Directory if it doesn't exits
    Path(driver_directory).mkdir(parents=True, exist_ok=True)
    # Storing base directory for navigation purpose
    base_directory = os.getcwd()
    online_driver_version = get_latest_chromedriver_release()
    try:
        # Executes cmd line entry to check for existing web-driver version locally
        os.chdir(driver_directory)
        driver_directory = os.getcwd()
        cmd_run = subprocess.run("chromedriver --version",
                                 capture_output=True,
                                 text=True)
        # Extract local driver version number as string from terminal output
        local_driver_version = cmd_run.stdout.split()[1]   
        os.chdir(base_directory)  
    except (FileNotFoundError, IndexError):
        print("No chromedriver executable found in specified path\n")
        download_latest_version(online_driver_version, driver_directory)
    else:
        print(f"Local chromedriver version: {local_driver_version}")
        print(f"Latest online chromedriver version: {online_driver_version}")
        if local_driver_version == online_driver_version:
            return True
        # Download the latest version if local driver is outdated
        download_latest_version(online_driver_version, driver_directory)


def get_latest_chromedriver_release():
    """ 
    Check for latest chromedriver release version online.

    Returns:
        str: Latest chromedriver version available for download.
    """
    latest_release_url = "https://chromedriver.storage.googleapis.com/LATEST_RELEASE"
    response = requests.get(latest_release_url)
    return response.text.strip()

            
def obtain_os():
    """
    Obtain operating system based on chromedriver supported by https://chromedriver.chromium.org/
    
    Returns:
        str: Operating system identifier string.
    """
    if sys.platform.startswith('win32') or sys.platform.startswith('cygwin'):
        return 'win32'
    elif sys.platform.startswith('linux'):
        return 'linux64'
    elif sys.platform.startswith('darwin'):
        return 'mac_arm64' if platform.machine() == 'arm64' else 'mac64'


def main(driver_directory):
    """Check if chromedriver is already installed and up to date, otherwise download and install it"""
    check_driver(driver_directory)


if __name__ == '__main__':
    # Set driver directory to user's home directory
    driver_directory = str(Path.home())
    main(driver_directory)
