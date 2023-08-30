import os
import platform
import requests
import shutil
import subprocess
import sys
import wget
import zipfile
from pathlib import Path

# Constants
CHROMEDRIVER_BASE_URL = "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing"
LAST_KNOWN_GOOD_VERSIONS_URL = "https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions.json"

class WebdriverAutoUpdate:
    """
    A class for managing ChromeDriver downloads and updates.

    Args:
        driver_directory (str): The directory to store ChromeDriver and its resources.

    Attributes:
        driver_directory (str): The directory to store ChromeDriver and its resources.
        current_os_platform (str): The identifier for the current operating system.
        online_driver_version (str): The latest online version of ChromeDriver.

    Methods:
        obtain_os(): Obtain the operating system identifier.
        get_latest_chromedriver_release(): Get the latest stable ChromeDriver version.
        download_latest_version(): Download the latest version of ChromeDriver.
        transfer_chromedriver_file(): Transfer the downloaded ChromeDriver executable.
        check_driver(): Check local ChromeDriver version and update if necessary.
        get_local_driver_version(): Get the version of locally installed ChromeDriver.
        update_driver(): Update ChromeDriver to the latest version.
        main(): The main entry point to manage ChromeDriver.

    Usage:
        driver_directory = str(Path.home())
        driver_manager = DriverManager(driver_directory)
        driver_manager.main()
    """
        
    def __init__(self, driver_directory):
        self.driver_directory = driver_directory
        self.current_os_platform = self.obtain_os()
        self.online_driver_version = self.get_latest_chromedriver_release()
        self.base_directory = os.path.dirname(os.path.abspath(__file__))


    def obtain_os(self):
        """
        Obtain the operating system identifier based on the platform.

        Returns:
            str: The operating system identifier.
        """
        if sys.platform.startswith('win32') or sys.platform.startswith('cygwin'):
            return 'win32'
        elif sys.platform.startswith('linux'):
            return 'linux64'
        elif sys.platform.startswith('darwin'):
            return 'mac_arm64' if platform.machine() == 'arm64' else 'mac64'


    def get_latest_chromedriver_release(self):
        """
        Get the latest stable ChromeDriver version from an online source.

        Returns:
            str: The latest ChromeDriver version.
        """
        response = requests.get(LAST_KNOWN_GOOD_VERSIONS_URL).json()
        return response["channels"]["Stable"]["version"]


    def download_latest_version(self):
        """
        Download the latest version of ChromeDriver.

        Returns:
            None
        """
        download_url = f"{CHROMEDRIVER_BASE_URL}/{self.online_driver_version}/{self.current_os_platform}/chromedriver-{self.current_os_platform}.zip"
        print(f"Latest stable driver: {download_url}")
        latest_driver_zip = wget.download(download_url, out=self.driver_directory)
        with zipfile.ZipFile(latest_driver_zip, 'r') as downloaded_zip:
            downloaded_zip.extractall(path=self.driver_directory)
        os.remove(latest_driver_zip)
        self.transfer_chromedriver_file()
        print(f"\nSuccessfully downloaded chromedriver version {self.online_driver_version} to:\n{driver_directory}")


    def transfer_chromedriver_file(self):
        """
        Transfer the downloaded ChromeDriver executable to the target directory.

        Returns:
            None
        """
        download_folder_name = f"chromedriver-{self.current_os_platform}"
        chromedriver_download_path = os.path.join(self.driver_directory, download_folder_name, "chromedriver.exe")
        if os.path.exists(chromedriver_download_path):
            shutil.copy(chromedriver_download_path, self.driver_directory)


    def check_driver(self):
        """
        Check local ChromeDriver version and update if necessary.

        Returns:
            None
        """
        Path(self.driver_directory).mkdir(parents=True, exist_ok=True)
        self.base_directory = os.getcwd()
        local_driver_version = self.get_local_driver_version()
        if local_driver_version is None:
            print("No chromedriver executable found in specified path\n")
            self.download_latest_version()
        else:
            print(f"Local chromedriver version: {local_driver_version}")
            print(f"Latest online chromedriver version: {self.online_driver_version}")
            if local_driver_version != self.online_driver_version:
                self.update_driver()


    def get_local_driver_version(self):
        """
        Get the version of locally installed ChromeDriver.

        Returns:
            str: The local ChromeDriver version, or None if not found.
        """
        try:
            os.chdir(self.driver_directory)
            cmd_run = subprocess.run("chromedriver --version", capture_output=True, text=True)
            local_driver_version = cmd_run.stdout.split()[1]
            os.chdir(self.base_directory)
            return local_driver_version
        except (FileNotFoundError, IndexError):
            return None


    def update_driver(self):
        """
        Update ChromeDriver to the latest version.

        Returns:
            None
        """
        self.download_latest_version()
        print(f"\nSuccessfully updated chromedriver version to {self.online_driver_version}")


    def main(self):
        """
        Main entry point to manage ChromeDriver.

        Returns:
            None
        """
        self.check_driver()


if __name__ == '__main__':
    driver_directory = str(Path.home())
    driver_manager = WebdriverAutoUpdate(driver_directory)
    driver_manager.main()
