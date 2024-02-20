import os
import platform
import re
import requests
import shutil
import subprocess
import sys
import wget
import zipfile
from pathlib import Path

# Constants
CHROMEDRIVER_BASE_URL = "https://storage.googleapis.com/chrome-for-testing-public"
LAST_KNOWN_GOOD_VERSIONS_URL = "https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions.json"


class WebDriverManager:
    """
    A class for managing ChromeDriver downloads and updates.

    Args:
        driver_directory (str): The directory to store ChromeDriver and its resources.

    Attributes:
        driver_directory (str): The directory to store ChromeDriver and its resources.
        current_os_platform (str): The identifier for the current operating system.
        online_driver_version (str): The latest online version of ChromeDriver.
        base_directory (str): The absolute directory path of the current script.

    Methods:
        check_driver(): Check local ChromeDriver version and update if necessary.
        download_latest_version(): Download the latest version of ChromeDriver.
        get_latest_chromedriver_release(): Get the latest stable ChromeDriver version.
        get_local_driver_version(): Get the version of locally installed ChromeDriver.
        is_mac(): Determine if the system is a macOS.
        is_unix(): Determine if the system is Windows or a Unix based system.

        obtain_os(): Obtain the operating system identifier.
        obtain_os_executable(): Obtain the name of the chromedriver executable.
        set_execution_bit_on_chromedriver(): Set execution bit for Unix based system.
        _transfer_chromedriver_file(): Transfer the downloaded ChromeDriver executable.
        _unquarantine_chromedriver(): Delete quarantine attribute for macOS and Linux.
        update_driver(): Update ChromeDriver to the latest version.
        main(): The main entry point to manage ChromeDriver.

    Usage:
        driver_directory = str(Path.home())
        driver_manager = WebdriverAutoUpdate(driver_directory)
        driver_manager.main()
    """

    CHROMEDRIVER = 'chromedriver'  # For Unix-based systems
    CHROMEDRIVER_WIN = 'chromedriver.exe'  # For Windows

    def __init__(self, driver_directory: str, quarantine_extended_attribute=None):
        self.driver_directory = str(os.path.abspath(driver_directory))
        self.current_os_platform = self.obtain_os()
        self.online_driver_version = self.get_latest_chromedriver_release()
        self.base_directory = os.path.dirname(os.path.abspath(__file__))
        # Determine the quarantine attribute
        if quarantine_extended_attribute is not None:
            self.quarantine_attribute = (
                # Extended attribute must be preceded by a namespace
                quarantine_extended_attribute if "." in str(quarantine_extended_attribute)
                # Take the user namespace
                else f"user.{quarantine_extended_attribute}"
            )
        else:
            self.quarantine_attribute = quarantine_extended_attribute

    def obtain_os(self):
        """
        Obtain the operating system identifier based on the platform.

        Returns:
            str: The operating system identifier.
        """
        bit_architecture = platform.architecture()[0]
        bit_number = re.findall(r"\d+", bit_architecture)
        os_bit = bit_number[0] if bit_number else "32"

        if sys.platform.startswith('win') or sys.platform.startswith('cygwin'):
            return 'win' + os_bit
        elif sys.platform.startswith('darwin'):
            return 'mac-arm64' if platform.machine() == 'arm64' else 'mac-x64'
        elif sys.platform.startswith('linux'):
            # There are ARM64 chromedrivers on the web, but not on
            # https://googlechromelabs.github.io/chrome-for-testing/
            if platform.machine() == 'aarch64':
                sys.exit("\nSorry, there are currently no ARM64 chromedrivers on "
                         "https://googlechromelabs.github.io/chrome-for-testing/.")
            else:
                return 'linux64'

    def obtain_os_executable(self):
        """
        Obtain the appropriate chromedriver executable for either Windows or Unix-based systems (with or without a suffix)

        Returns:
            str: the name of the executable
        """
        if self.is_unix():
            return WebDriverManager.CHROMEDRIVER
        else:
            return WebDriverManager.CHROMEDRIVER_WIN

    def is_mac(self) -> bool:
        """
        Determine if the system is a macOS.

        Returns:
            boolean: True if os is mac, otherwise False
        """
        if sys.platform.startswith('darwin'):
            return True
        else:
            return False

    def is_unix(self) -> bool:
        """
        Determine if the system is Windows or a Unix based system.

        Returns:
            boolean: True if os is linux or darwin, otherwise False.
        """
        if sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
            return True
        else:
            return False

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
        latest_driver_zip = wget.download(
            download_url, out=self.driver_directory)
        with zipfile.ZipFile(latest_driver_zip, 'r') as downloaded_zip:
            downloaded_zip.extractall(path=self.driver_directory)
        os.remove(latest_driver_zip)
        self._transfer_chromedriver_file()
        print(
            f"\nSuccessfully downloaded chromedriver version {self.online_driver_version} to:\n{self.driver_directory}")

    def _transfer_chromedriver_file(self):
        """
        Transfer the downloaded ChromeDriver executable to the target directory.

        Returns:
            None
        """
        download_folder_name = f"chromedriver-{self.current_os_platform}"
        chromedriver_download_path = os.path.join(
            self.driver_directory, download_folder_name, self.obtain_os_executable())
        if os.path.exists(chromedriver_download_path):
            shutil.copy(chromedriver_download_path, self.driver_directory)

        chromedriver_executable = os.path.join(
            self.driver_directory, self.obtain_os_executable())
        # Set execution bit for unix based systems
        self.set_execution_bit_on_chromedriver(chromedriver_executable)
        # un-quarantine web downloads of chromedriver version >= 117
        self._unquarantine_chromedriver(chromedriver_executable)

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
            print("Chromedriver executable not found in specified path\n")
            self.download_latest_version()
        else:
            print(f"Local chromedriver version: {local_driver_version}")
            print(
                f"Latest online chromedriver version: {self.online_driver_version}")
            if local_driver_version != self.online_driver_version:
                self.update_driver()

    def get_local_driver_version(self):
        """
        Get the version of locally installed ChromeDriver.

        Returns:
            str: The local ChromeDriver version, or None if not found.
        """
        try:
            chromedriver_executable = os.path.join(
                self.driver_directory, self.obtain_os_executable())
            if os.path.isfile(chromedriver_executable):
                self.set_execution_bit_on_chromedriver(chromedriver_executable)
                self._unquarantine_chromedriver(chromedriver_executable)
                cmd_run = subprocess.run(args=[chromedriver_executable, "--version"],
                                         capture_output=True,
                                         text=True)
                local_driver_version = cmd_run.stdout.split()[1]
                return local_driver_version
            else:
                return None
        except (FileNotFoundError, IndexError):
            return None

    def _unquarantine_chromedriver(self, chromedriver_executable: str):
        """
        Delete the quarantine attribute on chromedriver executable if Unix OS

        Returns:
            None
        """
        if self.is_unix():
            if self.is_mac():
                # on macOS we know the name of extended attribute
                subprocess.run(args=["xattr", "-d", "com.apple.quarantine", chromedriver_executable],
                               capture_output=True)
            else:
                # Linux does not implement attr
                # setfattr is able to delete extended attributes, but requires the name of the attribute
                # A few Linux OS can set a quarantine attribute like macOS.
                if self.quarantine_attribute is not None:
                    subprocess.run(
                        args=["setfattr", "-x", self.quarantine_attribute, chromedriver_executable])

    def set_execution_bit_on_chromedriver(self, chromedriver_executable: str):
        """
        Set the permission on chromedriver executable for Unix based system

        Returns:
            None
        """
        if self.is_unix():
            subprocess.run(args=["chmod", "+x", chromedriver_executable])

    def update_driver(self):
        """
        Update ChromeDriver to the latest version.

        Returns:
            None
        """
        self.download_latest_version()
        print(
            f"\nSuccessfully updated chromedriver version to {self.online_driver_version}")

    def main(self):
        """
        Main entry point to manage ChromeDriver.

        Returns:
            None
        """
        self.check_driver()
