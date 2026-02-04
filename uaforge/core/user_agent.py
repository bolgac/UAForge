import random
from typing import List, Optional
from .database import Database

class UserAgentGenerator:
    """
    UserAgentGenerator
    A class for generating realistic user agent strings for different web browsers across various platforms.
    This class retrieves browser version information and device platform data from a database and uses them
    to create authentic-looking user agent strings that can be used for web scraping, testing, or other purposes.
    The generator supports three major browser types:
    - Chrome (including iOS variant CriOS)
    - Firefox (including iOS variant FxiOS)
    - Opera
    Attributes:
        db (Database): Database instance for retrieving browser versions and platform information.
        platform_list (dict): Dictionary mapping platform keys to available systems/versions.
        CHROME_VERS (list): List of available Chrome browser versions.
        OPERA_VERS (list): List of available Opera browser versions.
        FIREFOX_VERS (list): List of available Firefox browser versions.
    Example:
        >>> generator = UserAgentGenerator()
        >>> chrome_agent = generator.create_useragent("Chrome")
        >>> firefox_agent = generator.create_useragent("Firefox")
        >>> agents_list = generator.get_list(10)
    """    
    def __init__(self, db_path: str = None):
        self.db = Database(db_path)
        self._initialize_data()
    
    def _initialize_data(self):
        """
        Initializes user agent data by retrieving platform and browser version information from the database.

        This method sets the following instance attributes:
            - platform_list: List of device platforms and versions.
            - CHROME_VERS: Latest Chrome browser version.
            - OPERA_VERS: Latest Opera browser version.
            - FIREFOX_VERS: Latest Firefox browser version.
        """
        self.platform_list = self.db.get_device_version()
        self.CHROME_VERS = self.db.get_chrome_vers()[0]
        self.OPERA_VERS = self.db.get_opera_vers()[0]
        self.FIREFOX_VERS = self.db.get_firefox_vers()[0]
    
    def _select_random_platform(self) -> tuple:
        """
        Selects a random platform, system, and version type.
        This method randomly chooses a platform key from the available platforms,
        then selects a random system associated with that platform. It also retrieves
        the available version types from the database and selects a random version type
        corresponding to the chosen platform.
        Returns:
            tuple: A tuple containing:
                - select_key (str): The randomly selected platform key.
                - system_select (str): The randomly selected system for the platform.
                - type_select (str): The randomly selected version type for the platform.
        """
        select_key = random.choice(list(self.platform_list.keys()))
        system_select = random.choice(self.platform_list[select_key])
        
        version_types = self.db.get_version_type_connect()
        type_select = random.choice(version_types.get(select_key, [""]))
        
        return select_key, system_select, type_select
    
    def create_useragent(self, browser_type: str = "Chrome") -> str:
        """
        Generates a user agent string for the specified browser type.
        Args:
            browser_type (str, optional): The type of browser for which to generate the user agent.
                Supported values are "Chrome", "Firefox", and "Opera". Defaults to "Chrome".
        Returns:
            str: A user agent string corresponding to the specified browser type and a randomly selected platform.
        Raises:
            ValueError: If an unsupported browser type is provided.
        """
        select_key, system_select, type_select = self._select_random_platform()
        
        if browser_type == "Chrome":
            return self._create_chrome_agent(select_key, system_select, type_select)
        elif browser_type == "Firefox":
            return self._create_firefox_agent(select_key, system_select, type_select)
        elif browser_type == "Opera":
            return self._create_opera_agent(select_key, system_select, type_select)
        else:
            raise ValueError(f"Desteklenmeyen tarayıcı tipi: {browser_type}")
    
    def _create_chrome_agent(self, select_key: str, system_select: str, type_select: str) -> str:
        """
        Generates a Chrome-based User-Agent string based on the provided system and type selections.
        Args:
            system_select (str): The system information string (e.g., OS and device type).
            type_select (str): The type information string (e.g., locale or device type).
        Returns:
            str: A formatted User-Agent string for Chrome or Chrome on iOS devices.
        Notes:
            - If the system is identified as an iPhone or iPad, the User-Agent is formatted to mimic Chrome on iOS (CriOS).
            - Otherwise, a standard Chrome User-Agent string is generated.
        """
        Moz = "Mozilla"
        Mozilla_vers = "5.0"
        
        if "iPhone" in system_select or "iPad" in system_select:
            if "iPad" in system_select:
                system_select = system_select.strip(";").replace("Intel Mac OS X", "CPU OS") + " like Mac OS X"
            else:
                system_select = system_select.strip(";").replace("Intel Mac OS X", "CPU iPhone OS") + " like Mac OS X"
            
            CHROME_VERS_SELECT = str(random.choice(self.CHROME_VERS)).replace("Chrome", "CriOS")
            return f"{Moz}/{Mozilla_vers} ({system_select}; {type_select}) AppleWebKit/605.1.15 (KHTML, like Gecko) {CHROME_VERS_SELECT} Mobile/15E148 Safari/604.1"
        else:
            CHROME_VERS_SELECT = random.choice(self.CHROME_VERS)
            return f"{Moz}/{Mozilla_vers} ({system_select}; {type_select}) AppleWebKit/537.36 (KHTML, like Gecko) {CHROME_VERS_SELECT} Safari/537.36"
    
    def _create_firefox_agent(self, select_key: str, system_select: str, type_select: str) -> str:
        """
        Generates a Firefox user agent string based on the provided system and type selections.
        Args:
            system_select (str): The system information to include in the user agent (e.g., "Windows NT 10.0", "iPhone", "iPad").
            type_select (str): The type or locale information to include in the user agent (e.g., "en-US").
        Returns:
            str: A formatted Firefox user agent string tailored to the specified system and type.
        Notes:
            - For iPhone and iPad systems, the user agent is formatted to mimic Firefox on iOS (FxiOS).
            - For other systems, a standard Firefox user agent string is generated.
            - The Firefox version is randomly selected from the self.FIREFOX_VERS list.
        """
        Moz = "Mozilla"
        Mozilla_vers = "5.0"
        
        if "iPhone" in system_select or "iPad" in system_select:
            if "iPad" in system_select:
                system_select = system_select.strip(";").replace("Intel Mac OS X", "CPU OS") + " like Mac OS X"
            else:
                system_select = system_select.strip(";").replace("Intel Mac OS X", "CPU iPhone OS") + " like Mac OS X"
            
            FIREFOX_VERS_SELECT = str(random.choice(self.FIREFOX_VERS)).replace("Firefox", "FxiOS")
            return f"{Moz}/{Mozilla_vers} ({system_select}; {type_select}) Gecko/20100101 {FIREFOX_VERS_SELECT} Mobile/15E148"
        else:
            FIREFOX_VERS_SELECT = random.choice(self.FIREFOX_VERS)
            return f"{Moz}/{Mozilla_vers} ({system_select}; {type_select}; rv:109.0) Gecko/20100101 {FIREFOX_VERS_SELECT}"
    
    def _create_opera_agent(self,select_key: str, system_select: str, type_select: str) -> str:
        """
        Generates an Opera browser User-Agent string based on the provided system and type selections.
        Args:
            system_select (str): The system information string (e.g., "iPhone", "iPad", or other OS descriptors).
            type_select (str): The type information string (e.g., device type or architecture).
        Returns:
            str: A formatted Opera User-Agent string appropriate for the specified system and type.
        Notes:
            - If the system is an iPhone or iPad, the User-Agent string is tailored for iOS devices.
            - Otherwise, a standard Opera User-Agent string is generated.
            - Random Opera and Chrome version numbers are selected from predefined lists.
        """
        Moz = "Mozilla"
        Mozilla_vers = "5.0"
        
        if "iPhone" in system_select or "iPad" in system_select:
            if "iPad" in system_select:
                system_select = system_select.strip(";").replace("Intel Mac OS X", "CPU OS") + " like Mac OS X"
            else:
                system_select = system_select.strip(";").replace("Intel Mac OS X", "CPU iPhone OS") + " like Mac OS X"
            
            OPERA_VERS_SELECT = random.choice(self.OPERA_VERS)
            CHROME_VERS_SELECT = random.choice(self.CHROME_VERS)
            return f"{Moz}/{Mozilla_vers} ({system_select}; {type_select}) AppleWebKit/537.36 (KHTML, like Gecko) {CHROME_VERS_SELECT} Mobile Safari/537.36 OPR/{OPERA_VERS_SELECT.split('/')[0]}"
        else:
            OPERA_VERS_SELECT = random.choice(self.OPERA_VERS)
            CHROME_VERS_SELECT = random.choice(self.CHROME_VERS)
            return f"{Moz}/{Mozilla_vers} ({system_select}; {type_select}) AppleWebKit/537.36 (KHTML, like Gecko) {CHROME_VERS_SELECT} Safari/537.36 OPR/{OPERA_VERS_SELECT.split('/')[0]}"
    
    def get_list(self, count: int) -> List[str]:
        """
        Generate a list of unique user agent strings.
        Args:
            count (int): The number of user agent strings to generate.
        Returns:
            List[str]: A list of unique user agent strings for randomly selected browsers
                       (Chrome, Firefox, or Opera).
        Note:
            The method attempts to generate `count` user agents, but the returned list
            may contain fewer items if duplicate user agents are generated, as only
            unique agents are included in the result.
        """

        user_agent_list = []
        browsers = ["Chrome", "Firefox", "Opera"]
        
        for i in range(count):
            try :
                browser_select = random.choice(browsers)
                user_agent = self.create_useragent(browser_select)
                
                if user_agent not in user_agent_list:
                    user_agent_list.append(user_agent)
            except Exception as e:
                print(f"Error generating user agent: {e}")
        
        return user_agent_list