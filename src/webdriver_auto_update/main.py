from pathlib import Path
from chrome_app_utils import ChromeAppUtils
from webdriver_manager import WebDriverManager


def main():
    # Using ChromeAppUtils to get Chrome application version
    chrome_app_utils = ChromeAppUtils()
    chrome_app_version = chrome_app_utils.get_chrome_version()
    print("Chrome application version found: ", chrome_app_version)

    driver_directory = str(Path.home())
    driver_manager = WebDriverManager(driver_directory)
    driver_manager.main()


if __name__ == '__main__':
    main()
