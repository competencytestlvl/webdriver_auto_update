import os
import re
from sys import platform


class ChromeAppUtils:
    def __init__(self) -> None:
        if platform.startswith("Darwin"):
            self.install_path = "/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome"
        elif platform.startswith("linux"):
            self.install_path = "/usr/bin/google-chrome"
        elif platform.startswith("win"):
            self.install_path = fr"C:\Program Files\Google\Chrome\Application"
        else:
            raise NotImplemented(f"Unidentified OS: '{platform}'")
        
    def get_default_install_path(self) -> str:
        """
        Default installation path of Chrome application according to platform.

        Returns:
            str: Default installation path.
        """
        return self.install_path

    def get_chrome_version(self, path: str = None):
        """
        Obtain Chrome application version number in a valid directory.

        Returns:
            str: Version number.
        """
        if path is None:
            path = self.install_path
        if os.path.isdir(path):
            paths = [f.path for f in os.scandir(path) if f.is_dir()]
            for path in paths:
                file_name = os.path.basename(path)
                # Looks for the period delimiated version number in groups of 4 e.g. 121.0.6167.140
                pattern = '\d+\.\d+\.\d+\.\d+'
                match = re.search(pattern, file_name)
                if match and match.group():
                    # Chrome version matched.
                    return match.group(0)
