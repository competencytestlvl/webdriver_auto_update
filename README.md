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

1. Clone this repository from GitHub
2. Install the required package:

   ```
   pip install webdriver-auto-update
   ```

### Usage

1. Navigate to the directory where you've cloned or downloaded the repository
2. Run the following example

   ```
   from webdriver_auto_update.webdriver_auto_update import WebdriverAutoUpdate

   # Target directory to store chromedriver
   driver_directory = "/path/to/driver/directory"

   # Create an instance of WebdriverAutoUpdate
   driver_manager = WebdriverAutoUpdate(driver_directory)

   # Call the main method to manage chromedriver
   driver_manager.main()
   ```

### Note

- The objective of this program is to reduce redundancy of searching and downloading the updated version of chrome driver to the OpenSource community.
- Intended to be used in Selenium projects, browser testing or web automation.

## Contributing

Contributions are welcome! If you find any issues or want to add new features, feel free to submit a pull request or reach out to me.
