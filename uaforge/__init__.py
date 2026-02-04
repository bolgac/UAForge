from .core.user_agent import UserAgentGenerator
from .core.database import Database
from .core.version_fetcher import VersionFetcher
from .core.version_updater import VersionUpdater

__version__ = "1.1.1"
__author__ = "bolgac"
__email__ = "bytearchsoft@gmail.com"

__all__ = ['UserAgentGenerator', 'Database', 'VersionFetcher', 'VersionUpdater']

def init_database():
    updater = VersionUpdater()
    return updater.initialize_database()

def update_versions(browser_type="all"):
    """
    Update browser version data for specified browser type(s).
    This function updates version information for various browsers by delegating
    to the appropriate update method of the VersionUpdater class.
    Args:
        browser_type (str, optional): The type of browser to update. Defaults to "all".
            Supported values:
            - "all": Updates all supported browsers
            - "chrome": Updates Chrome browser versions
            - "firefox": Updates Firefox browser versions
            - "opera": Updates Opera browser versions
            - "android": Updates Android browser versions
            - "mac": Updates Mac browser versions
    Returns:
        tuple or dict: 
            - If browser_type is "all": Returns the result from update_all()
            - If browser_type is a specific browser: Returns a tuple of (added, updated)
              where added is the number of newly added versions and updated is the
              number of updated versions
    Raises:
        ValueError: If an unsupported browser type is provided.
    Examples:
        >>> update_versions()  # Updates all browsers
        >>> update_versions("chrome")  # Updates Chrome only
        Chrome: +5 added, 3 updated
    """

    updater = VersionUpdater()
    
    if browser_type.lower() == "all":
        return updater.update_all()
    elif browser_type.lower() == "chrome":
        added, updated = updater.update_chrome()
        print(f"Chrome: +{added} added, {updated} updated")
        return added, updated
    elif browser_type.lower() == "firefox":
        added, updated = updater.update_firefox()
        print(f"Firefox: +{added} added, {updated} updated")
        return added, updated
    elif browser_type.lower() == "opera":
        added, updated = updater.update_opera()
        print(f"Opera: +{added} added, {updated} updated")
        return added, updated
    elif browser_type.lower() == "android":
        added, updated = updater.update_android()
        print(f"Android: +{added} added, {updated} updated")
        return added, updated
    elif browser_type.lower() == "mac":
        added, updated = updater.update_mac()
        print(f"Mac: +{added} added, {updated} updated")
        return added, updated
        
    else:
        raise ValueError(f"Unsupported browser type: {browser_type}")

def generate_user_agent(browser="Chrome"):
    """
    Generate a random user agent string for the specified browser.
    
    Args:
        browser (str, optional): The browser type to generate a user agent for.
            Defaults to "Chrome". Common options include "Chrome", "Firefox",
            "Safari", "Edge", etc.
    
    Returns:
        str: A randomly generated user agent string for the specified browser.
    
    Example:
        >>> ua = generate_user_agent("Firefox")
        >>> print(ua)
        Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0
    """
    generator = UserAgentGenerator()
    return generator.create_useragent(browser)

def generate_multiple(count=10):
    """
    Generate multiple random user agent strings.
    
    Args:
        count (int, optional): The number of user agent strings to generate. Defaults to 10.
    
    Returns:
        list: A list of randomly generated user agent strings.
    
    Example:
        >>> user_agents = generate_multiple(5)
        >>> len(user_agents)
        5
    """
    generator = UserAgentGenerator()
    return generator.get_list(count)

try:
    from .cli import main as cli_main
    __all__.append('cli_main')
except ImportError:
    pass

try:
    import os
    from pathlib import Path
    
    db_dir = Path(__file__).parent / "data"
    db_path = db_dir / "useragent.db"
    
    if not db_path.exists():
        print("Warning: Database not found.")
        print("Run the 'useragent-gen --init' command before first use.")
        
except Exception:
    pass