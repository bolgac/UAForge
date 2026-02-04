import datetime
from typing import Dict, List, Tuple, Any

from .database import Database
from .version_fetcher import VersionFetcher
import random

class VersionUpdater:
    def __init__(self, db_path: str = None):
        self.db = Database(db_path)
        self.fetcher = VersionFetcher()
        
        self.windows_versions = [
            "Windows NT 6.0",  # Vista
            "Windows NT 6.1",  # 7
            "Windows NT 6.2",  # 8
            "Windows NT 6.3",  # 8.1
            "Windows NT 10.0"  # 10/11
        ]
        
        self.linux_versions = [
            "X11; Linux",
            "X11; Ubuntu; Linux"
        ]
        
        self.version_types = {
            "Windows": ["Win64; x64", "WOW64"],
            "Linux": ["i686", "x86_64", "i686 on x86_64"],
            "Mac": [""],
            "Android": ["armv7l", "armv8l"]
        }
        
        self.platforms = {
            "Windows": self.windows_versions,
            "Linux": self.linux_versions,
            "Mac": self._generate_mac_systems(),
            "Android": self._generate_android_systems()
        }
    
    def _generate_mac_systems(self) -> List[str]:
        """
        Generates a list of macOS system strings for various Apple devices and OS versions.
        Returns:
            List[str]: A list of strings representing different combinations of Apple devices
            (iPhone, iPad, Macintosh) and macOS versions, formatted as
            "<Device>; Intel Mac OS X <version>".
        """
        devices = ["iPhone", "iPad", "Macintosh"]
        versions = ["10_15_7", "11_6", "12_0", "13_0", "14_0"]
        systems = []
        
        for device in devices:
            for version in versions:
                systems.append(f"{device}; Intel Mac OS X {version}")
        
        return systems
    
    def _generate_android_systems(self) -> List[str]:
        devices = [
            "Linux; Android 10",
            "Linux; Android 11", 
            "Linux; Android 12",
            "Linux; Android 13", 
            "Linux; Android 14"
        ]
        return devices
    
    def update_chrome(self) -> Tuple[int, int]:
        """
        Updates the Chrome version information in the database by comparing fetched web data with current records.
        Fetches the latest Chrome version data using the fetcher, compares it with the versions stored in the database,
        and determines which versions need to be added or updated. If there are new or updated versions, it updates the
        database accordingly.
        Returns:
            Tuple[int, int]: A tuple containing the number of versions added and the number of versions updated.
        Exceptions:
            Catches all exceptions, prints an error message, and returns (0, 0) in case of failure.
        """
        try:
            web_data = self.fetcher.fetch_chrome_versions()
            current_versions, current_data = self.db.get_chrome_vers()
            
            dt_add = []
            dt_update = []
            now = datetime.datetime.now().isoformat()
            
            for version, date in web_data["Version_dict"].items():
                chrome_version = f"Chrome/{version.strip()}"
                
                if chrome_version in current_versions:
                    idx = current_versions.index(chrome_version)
                    original_date = current_data[idx][1]
                    
                    if date != original_date:
                        dt_update.append((chrome_version, date, now))
                else:
                    dt_add.append((chrome_version, date, now))
            
            if dt_add or dt_update:
                self.db.add_chrome_versions(dt_add, dt_update)
            
            return len(dt_add), len(dt_update)
            
        except Exception as e:
            print(f"Chrome update error: {e}")
            return 0, 0
    
    def update_firefox(self) -> Tuple[int, int]:
        """
        Updates the Firefox version information in the database by comparing fetched web data with current records.
        Fetches the latest Firefox version data from the web, compares it with the versions stored in the database,
        and determines which versions need to be added or updated based on their release dates. If there are new or
        updated versions, it updates the database accordingly.
        Returns:
            Tuple[int, int]: A tuple containing the number of versions added and the number of versions updated.
        Exceptions:
            Catches all exceptions, prints an error message, and returns (0, 0) in case of failure.
        """
        try:
            web_data = self.fetcher.fetch_firefox_versions()
            current_versions, current_data = self.db.get_firefox_vers()
            
            dt_add = []
            dt_update = []
            now = datetime.datetime.now().isoformat()
            for version, date in web_data["Version_dict"].items():
                if version in current_versions:
                    pass
                else:
                    dt_add.append((version, date.isoformat() if hasattr(date, 'isoformat') else str(date), now))
            
            if dt_add or dt_update:
                self.db.add_firefox_versions(dt_add, dt_update)
            
            return len(dt_add), len(dt_update)
            
        except Exception as e:
            print(f"Firefox update error: {e}")
            return 0, 0

    def update_opera(self) -> Tuple[int, int]:
        """
        Updates the Opera browser version information in the database by comparing fetched web data with current records.
        Fetches the latest Opera versions and their release dates from an external source, compares them with the versions stored in the database, and determines which versions need to be added or updated. New or updated versions are then written to the database.
        Returns:
            Tuple[int, int]: A tuple containing the number of new versions added and the number of existing versions updated.
        Exceptions:
            Catches and logs any exceptions that occur during the update process, returning (0, 0) in case of error.
        """
        try :
            web_data = self.fetcher.fetch_opera_versions()
            current_versions, current_data = self.db.get_opera_vers()
            
            dt_add = []
            dt_update = []
            now = datetime.datetime.now().isoformat()
            for version, date in web_data["Version_dict"].items():
                if version in current_versions:
                    idx = current_versions.index(version)
                    original_date = current_data[idx][1]
                    
                    if isinstance(original_date, str) and date != original_date:
                        dt_update.append((version, date.isoformat() if hasattr(date, 'isoformat') else str(date), now))
                else:
                    dt_add.append((version, date.isoformat() if hasattr(date, 'isoformat') else str(date), now))
                    
            if dt_add or dt_update:
                self.db.add_opera_versions(dt_add, dt_update)
            
            return len(dt_add), len(dt_update)
            
        except Exception as e:
            print(f"Opera update error: {e}")
            return 0, 0
            
    def update_android(self) -> Tuple[int, int]:
        """
        Update Android versions in the database with the latest data from the web.
        Fetches the latest Android versions from the web, compares them with the 
        current versions stored in the database, and updates or adds new versions 
        as needed.
        Returns:
            Tuple[int, int]: A tuple containing:
                - Number of new Android versions added (int)
                - Number of existing Android versions updated (int)
        Note:
            If an exception occurs during the update process, the method returns (0, 0)
            and prints an error message to the console.
        """
        try:
            web_data = self.fetcher.fetch_android_versions()
            current_versions, current_data = self.db.get_android_vers()
            
            dt_add = []
            dt_update = []
            now = datetime.datetime.now().isoformat()
            for version, date in web_data["Version_dict"].items():
                if version in current_versions:
                    pass
                else:
                    dt_add.append((version, date.isoformat() if hasattr(date, 'isoformat') else str(date), now))
            
            if dt_add or dt_update:
                self.db.add_android_versions(dt_add, dt_update)
            
            return len(dt_add), len(dt_update)
            
        except Exception as e:
            print(f"Android update error: {e}")
            return 0, 0
    
    def update_platforms(self):
        """
        Updates the platforms in the database with the current platforms and systems.
        Iterates over the platforms and their associated systems, prepares the data,
        and adds it to the database using the `add_platforms` method. Handles exceptions
        by printing an error message and returning False.
        Returns:
            bool: True if the platforms were updated successfully, False otherwise.
        """
        try:
            platforms_data = []
            for platform, systems in self.platforms.items():
                for system in systems:
                    platforms_data.append((platform, system))
            
            self.db.add_platforms(platforms_data)
            
            return True
            
        except Exception as e:
            print(f"Platform update error: {e}")
            return False
    
    def update_version_types(self):
        """
        Updates the version types in the database.
        Iterates over the `version_types` attribute, which is expected to be a dictionary
        mapping platforms to lists of version type strings. Collects all (platform, type)
        pairs and adds them to the database using the `add_version_types` method.
        Returns:
            bool: True if the update was successful, False otherwise.
        Exceptions:
            Catches all exceptions, prints an error message, and returns False if an error occurs.
        """
        try:
            version_types_data = []
            for platform, types in self.version_types.items():
                for type_str in types:
                    version_types_data.append((platform, type_str))
            
            self.db.add_version_types(version_types_data)
            
            return True
            
        except Exception as e:
            print(f"Version type update error: {e}")
            return False
    
    def update_windows(self) -> Tuple[int, int]:
        """
        Updates the Windows versions in the database by adding any new versions not already present.
        Returns:
            Tuple[int, int]: A tuple where the first element is the number of new versions added,
            and the second element is always 0. If an exception occurs, returns (0, 0).
        Exceptions:
            Catches all exceptions, prints an error message, and returns (0, 0).
        """
        try:
            dt_add = []
            now = datetime.datetime.now().isoformat()
            getting_current_versions = self.db.get_windows_vers()
            
            for version in self.windows_versions:
                if version not in getting_current_versions[0]:
                    dt_add.append((version, now, now))
            
            if dt_add:
                self.db.add_windows_versions(dt_add)
            
            return len(dt_add), 0
            
        except Exception as e:
            print(f"Windows update error: {e}")
            return 0, 0
    
    def update_linux(self) -> Tuple[int, int]:
        try:
            return 0, 0
        except Exception as e:
            print(f"Linux update error: {e}")
            return 0, 0
    
    def update_mac(self) -> Tuple[int, int]:
        """
        Updates the local database with new macOS versions fetched from an external source.
        Fetches the latest macOS version information using the fetcher, compares it with the
        versions currently stored in the database, and adds any new versions that are not already present.
        The method records the current timestamp for each new entry. If there are new or updated versions,
        they are added to the database.
        Returns:
            Tuple[int, int]: A tuple containing the number of new versions added and the number of versions updated.
        Exceptions:
            Catches all exceptions, prints an error message, and returns (0, 0) in case of failure.
        """
        try:
            web_data = self.fetcher.fetch_macos_versions()
            current_versions, current_data = self.db.get_macos_vers()
            
            dt_add = []
            dt_update = []
            now = datetime.datetime.now().isoformat()
            
            for version, date in web_data["Version_dict"].items():
                if version in current_versions:
                    pass
                else:
                    dt_add.append((version, date.isoformat() if hasattr(date, 'isoformat') else str(date), now))
            
            if dt_add or dt_update:
                self.db.add_macos_versions(dt_add, dt_update)
            
            return len(dt_add), len(dt_update)
            
        except Exception as e:
            print(f"Mac update error: {e}")
            return 0, 0
    
    def update_all(self):
        print("All versions are being updated...")
        
        self.update_platforms()
        self.update_version_types()
        
        results = {}
        
        results['Chrome'] = self.update_chrome()
        results['Firefox'] = self.update_firefox()
        results['Opera'] = self.update_opera()
        
        results['Android'] = self.update_android()
        results["Mac"] = self.update_mac()
        results['Windows'] = self.update_windows()
        results['Linux'] = self.update_linux()
        
        print("\nUpdate Results:")
        print("-" * 40)
        total_added = 0
        total_updated = 0
        
        for name, (added, updated) in results.items():
            print(f"  {name}: +{added} added, {updated} updated")
            total_added += added
            total_updated += updated
        
        print("-" * 40)
        print(f"  Total: +{total_added} added, {total_updated} updated")
        
        return results
    
    def initialize_database(self):
        print("The database is being populated with initial data...")
        
        chrome_versions = [
            ("Chrome/120.0.0.0", "2023-12-01", datetime.datetime.now().isoformat()),
            ("Chrome/119.0.0.0", "2023-11-01", datetime.datetime.now().isoformat()),
            ("Chrome/118.0.0.0", "2023-10-01", datetime.datetime.now().isoformat()),
        ]
        
        firefox_versions = [
            ("Firefox/121.0", "2023-12-01", datetime.datetime.now().isoformat()),
            ("Firefox/120.0", "2023-11-01", datetime.datetime.now().isoformat()),
            ("Firefox/119.0", "2023-10-01", datetime.datetime.now().isoformat()),
        ]
        
        android_versions = [
            ("Linux; Android 14", "2023-10-01", datetime.datetime.now().isoformat()),
            ("Linux; Android 13", "2022-10-01", datetime.datetime.now().isoformat()),
            ("Linux; Android 12", "2021-10-01", datetime.datetime.now().isoformat()),
        ]
        
        windows_versions = [
            ("Windows NT 10.0", datetime.datetime.now().isoformat(), datetime.datetime.now().isoformat()),
            ("Windows NT 6.3", datetime.datetime.now().isoformat(), datetime.datetime.now().isoformat()),
            ("Windows NT 6.1", datetime.datetime.now().isoformat(), datetime.datetime.now().isoformat()),
        ]
        
        try:
            self.db.add_chrome_versions(chrome_versions)
            self.db.add_firefox_versions(firefox_versions)
            self.db.add_android_versions(android_versions)
            self.db.add_windows_versions(windows_versions)
            
            self.update_platforms()
            
            self.update_version_types()
            
            print("Database successfully started!")
            print("  - Chrome:  3 Version")
            print("  - Firefox: 3 Version")
            print("  - Android: 3 Version")
            print("  - Platforms: 4 platform")
            print("  - Version types: 4 version type")
            
            return True
            
        except Exception as e:
            print(f"Database initialization error: {e}")
            import traceback
            traceback.print_exc()
            return False