import sqlite3
import os
from typing import List, Tuple, Dict, Any
from datetime import datetime
from pathlib import Path

class Database:
    
    def __init__(self, db_path: str = None):
        if db_path is None:
            current_dir = Path(__file__).parent
            db_dir = current_dir.parent / "data"
            db_dir.mkdir(exist_ok=True)
            db_path = str(db_dir / "useragent.db")
        
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chrome_versions (
                version TEXT PRIMARY KEY,
                release_date TEXT,
                last_updated TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS firefox_versions (
                version TEXT PRIMARY KEY,
                release_date TEXT,
                last_updated TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS opera_versions (
                version TEXT PRIMARY KEY,
                release_date TEXT,
                last_updated TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS android_versions (
                version TEXT PRIMARY KEY,
                release_date TEXT,
                last_updated TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS windows_versions (
                version TEXT PRIMARY KEY,
                release_date TEXT,
                last_updated TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS macos_versions (
                version TEXT PRIMARY KEY,
                release_date TEXT,
                last_updated TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS platforms (
                platform TEXT,
                system_info TEXT,
                PRIMARY KEY (platform, system_info)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS version_types (
                platform TEXT,
                version_type TEXT,
                PRIMARY KEY (platform, version_type)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def get_device_version(self) -> Dict[str, List[str]]:
        platforms = {}
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT platform, system_info FROM platforms")
            rows = cursor.fetchall()
            
            for platform, system_info in rows:
                if platform not in platforms:
                    platforms[platform] = []
                platforms[platform].append(system_info)
        finally:
            conn.close()
        
        return platforms
    
    def get_version_type_connect(self) -> Dict[str, List[str]]:
        version_types = {}
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT platform, version_type FROM version_types")
            rows = cursor.fetchall()
            
            for platform, version_type in rows:
                if platform not in version_types:
                    version_types[platform] = []
                version_types[platform].append(version_type)
        finally:
            conn.close()
        
        return version_types
    
    def get_chrome_vers(self) -> Tuple[List[str], List[Tuple]]:
        versions = []
        version_data = []
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT version, release_date, last_updated FROM chrome_versions")
            rows = cursor.fetchall()
            
            for version, release_date, last_updated in rows:
                versions.append(version)
                version_data.append((version, release_date, last_updated))
        finally:
            conn.close()
        
        return (versions, version_data)
    
    def get_firefox_vers(self) -> Tuple[List[str], List[Tuple]]:
        versions = []
        version_data = []
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT version, release_date, last_updated FROM firefox_versions")
            rows = cursor.fetchall()
            
            for version, release_date, last_updated in rows:
                versions.append(version)
                version_data.append((version, release_date, last_updated))
        finally:
            conn.close()
        
        return (versions, version_data)
    
    def get_opera_vers(self) -> Tuple[List[str], List[Tuple]]:
        versions = []
        version_data = []
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT version, release_date, last_updated FROM opera_versions")
            rows = cursor.fetchall()
            
            for version, release_date, last_updated in rows:
                versions.append(version)
                version_data.append((version, release_date, last_updated))
        finally:
            conn.close()
        
        return (versions, version_data)
    
    def get_android_vers(self) -> Tuple[List[str], List[Tuple]]:
        versions = []
        version_data = []
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT version, release_date, last_updated FROM android_versions")
            rows = cursor.fetchall()
            
            for version, release_date, last_updated in rows:
                versions.append(version)
                version_data.append((version, release_date, last_updated))
        finally:
            conn.close()
        
        return (versions, version_data)
    
    def get_windows_vers(self) -> Tuple[List[str], List[Tuple]]:
        versions = []
        version_data = []
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT version, release_date, last_updated FROM windows_versions")
            rows = cursor.fetchall()
            
            for version, release_date, last_updated in rows:
                versions.append(version)
                version_data.append((version, release_date, last_updated))
        finally:
            conn.close()
        
        return (versions, version_data)
    
    def get_macos_vers(self) -> Tuple[List[str], List[Tuple]]:
        versions = []
        version_data = []
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT version, release_date, last_updated FROM macos_versions")
            rows = cursor.fetchall()
            
            for version, release_date, last_updated in rows:
                versions.append(version)
                version_data.append((version, release_date, last_updated))
        finally:
            conn.close()
        
        return (versions, version_data)
    
    def add_chrome_versions(self, dt_add: list, dt_update: list = None):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            for version, release_date, last_updated in dt_add:
                cursor.execute('''
                    INSERT OR REPLACE INTO chrome_versions 
                    (version, release_date, last_updated) 
                    VALUES (?, ?, ?)
                ''', (version, release_date, last_updated))
            
            if dt_update:
                for version, release_date, last_updated in dt_update:
                    cursor.execute('''
                        UPDATE chrome_versions 
                        SET release_date = ?, last_updated = ?
                        WHERE version = ?
                    ''', (release_date, last_updated, version))
            
            conn.commit()
        finally:
            conn.close()
    
    def add_firefox_versions(self, dt_add: list, dt_update: list = None):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            for version, release_date, last_updated in dt_add:
                cursor.execute('''
                    INSERT OR REPLACE INTO firefox_versions 
                    (version, release_date, last_updated) 
                    VALUES (?, ?, ?)
                ''', (version, release_date, last_updated))
            
            if dt_update:
                for version, release_date, last_updated in dt_update:
                    cursor.execute('''
                        UPDATE firefox_versions 
                        SET release_date = ?, last_updated = ?
                        WHERE version = ?
                    ''', (release_date, last_updated, version))
            
            conn.commit()
        finally:
            conn.close()
 
    def add_opera_versions(self, dt_add: list, dt_update: list = None):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            for version, release_date, last_updated in dt_add:
                cursor.execute('''
                    INSERT OR REPLACE INTO opera_versions 
                    (version, release_date, last_updated) 
                    VALUES (?, ?, ?)
                ''', (version, release_date, last_updated))
            
            if dt_update:
                for version, release_date, last_updated in dt_update:
                    cursor.execute('''
                        UPDATE opera_versions 
                        SET release_date = ?, last_updated = ?
                        WHERE version = ?
                    ''', (release_date, last_updated, version))
            
            conn.commit()
        finally:
            conn.close()
    
    def add_android_versions(self, dt_add: list, dt_update: list = None):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            for version, release_date, last_updated in dt_add:
                cursor.execute('''
                    INSERT OR REPLACE INTO android_versions 
                    (version, release_date, last_updated) 
                    VALUES (?, ?, ?)
                ''', (version, release_date, last_updated))
            
            if dt_update:
                for version, release_date, last_updated in dt_update:
                    cursor.execute('''
                        UPDATE android_versions 
                        SET release_date = ?, last_updated = ?
                        WHERE version = ?
                    ''', (release_date, last_updated, version))
            
            conn.commit()
        finally:
            conn.close()
    
    def add_windows_versions(self, dt_add: list, dt_update: list = None):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            for version, release_date, last_updated in dt_add:
                cursor.execute('''
                    INSERT OR REPLACE INTO windows_versions 
                    (version, release_date, last_updated) 
                    VALUES (?, ?, ?)
                ''', (version, release_date, last_updated))
            
            if dt_update:
                for version, release_date, last_updated in dt_update:
                    cursor.execute('''
                        UPDATE windows_versions 
                        SET release_date = ?, last_updated = ?
                        WHERE version = ?
                    ''', (release_date, last_updated, version))
            
            conn.commit()
        finally:
            conn.close()
 
    def add_macos_versions(self, dt_add: list, dt_update: list = None):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            for version, release_date, last_updated in dt_add:
                cursor.execute('''
                    INSERT OR REPLACE INTO macos_versions 
                    (version, release_date, last_updated) 
                    VALUES (?, ?, ?)
                ''', (version, release_date, last_updated))
            
            if dt_update:
                for version, release_date, last_updated in dt_update:
                    cursor.execute('''
                        UPDATE macos_versions 
                        SET release_date = ?, last_updated = ?
                        WHERE version = ?
                    ''', (release_date, last_updated, version))
            
            conn.commit()
        finally:
            conn.close()
               
    def add_platforms(self, platforms_data: list):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("DELETE FROM platforms")
            
            for platform, system_info in platforms_data:
                cursor.execute(
                    "INSERT OR REPLACE INTO platforms (platform, system_info) VALUES (?, ?)",
                    (platform, system_info)
                )
            
            conn.commit()
        finally:
            conn.close()
    
    def add_version_types(self, version_types_data: list):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("DELETE FROM version_types")
            
            for platform, version_type in version_types_data:
                cursor.execute(
                    "INSERT OR REPLACE INTO version_types (platform, version_type) VALUES (?, ?)",
                    (platform, version_type)
                )
            
            conn.commit()
        finally:
            conn.close()