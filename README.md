# webdriver_auto_update

A tool for managing ChromeDriver downloads and updates

## Features

- Automatically downloads the latest stable version of ChromeDriver.
- Compares the local ChromeDriver version with the latest online version.
- Updates ChromeDriver to the latest version if necessary.
- Works on Windows, Linux, and macOS.

## Getting Started

### Pre-requisites:

1. Python 3
2. Download Google Chrome
3. pip install selenium
4. Additional required packages listed in `requirements.txt`.

### Installation (Option 1)

Clone this repository from GitHub

```
git clone https://github.com/competencytestlvl/webdriver_auto_update.git
```

### Installation (Option 2)

Install the required package from PyPI:

```
pip install webdriver-auto-update
```

### Usage

1. Navigate to the directory where you've cloned or downloaded the repository
2. Run the following example:

   ```
   from webdriver_auto_update.chrome_app_utils import ChromeAppUtils
   from webdriver_auto_update.webdriver_manager import WebDriverManager

   # Using ChromeAppUtils to inspect Chrome application version
   chrome_app_utils = ChromeAppUtils()
   chrome_app_version = chrome_app_utils.get_chrome_version()
   print("Chrome application version: ", chrome_app_version)

   # Target directory to store chromedriver
   driver_directory = "/path/to/driver/directory"

   # Create an instance of WebDriverManager
   driver_manager = WebDriverManager(driver_directory)

   # Call the main method to manage chromedriver
   driver_manager.main()
   ```

### Note

- The objective of this program is to reduce redundancy of searching and downloading the updated version of chrome driver to the OpenSource community.
- Intended to be used in Selenium projects, browser testing or web automation.

## Contributing

Contributions are welcome! If you find any issues or want to add new features, feel free to submit a pull request or reach out to me.
