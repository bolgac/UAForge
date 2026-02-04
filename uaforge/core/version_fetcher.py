from bs4 import BeautifulSoup
import datetime,random, requests
from typing import Dict, List, Any

class VersionFetcher:
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def fetch_chrome_versions(self) -> Dict[str, Any]:
        url = "https://chromedriver.storage.googleapis.com"
        req = self.session.get(url)
        soup = BeautifulSoup(req.content, "xml")
        
        key_list = soup.find_all("Key")
        date_list = soup.find_all("LastModified")
        
        version_list = []
        version_dicts = {}
        
        for ky in range(len(key_list)):
            version = str(key_list[ky].text).split("/")[0]
            date = str(date_list[ky].text).strip()
            
            if (version and "RELEASE" not in version and "icons" not in version 
                and "index" not in version and version[0].isdigit()):
                try:
                    if int(version.split(".")[0]) > 79:
                        version_list.append(f"Chrome/{version.strip()}")
                        version_dicts[version] = date
                except (ValueError, IndexError):
                    continue
        
        return {"Version_list": version_list, "Version_dict": version_dicts}
    
    def fetch_firefox_versions(self) -> Dict[str, Any]:
        url = "https://www.mozilla.org/en-US/firefox/releases/"
        req = self.session.get(url)
        soup = BeautifulSoup(req.content, "html.parser")
        
        version_list = []
        version_dicts = {}
        
        release = soup.find("ol", {"class": "c-release-list"})
        if release:
            li_list = release.find_all("li")
            
            for li in li_list:
                try:
                    strong = li.find("a").text
                    if float(strong) > 70.0:
                        version_list.append(f"Firefox/{strong}")
                        version_dicts[f"Firefox/{strong}"] = datetime.datetime.now()
                        
                        for ol_li in li.find_all("li"):
                            version_list.append(f"Firefox/{ol_li.text}")
                            version_dicts[f"Firefox/{ol_li.text}"] = datetime.datetime.now()
                except (ValueError, AttributeError):
                    continue
        
        return {"Version_list": version_list, "Version_dict": version_dicts}
    
    def fetch_opera_versions(self) -> Dict[str, Any]:
        url = "https://blogs.opera.com/desktop/changelog-for-"
        session = requests.Session()
        session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.5304 Safari/537.36'})
        version_list = []
        version_dicts = {}
        for ver_count in [x for x in range(60,99)]:
            req = session.get(url+str(ver_count)+"/")
            soup = BeautifulSoup(req.content,"html.parser") 
            content = soup.find("div",{"class":"content"})
            for strong in content.find_all("h4") :
                splt = str(strong.text).split("– 20")
                if len(splt) > 1 :
                    version_list.append("OPR/%s"%splt[0].strip())
                    version_dicts.update({splt[0].strip():splt[1].strip().split(" ")[0]})

        return {"Version_list":version_list,"Version_dict":version_dicts}
    
    def fetch_android_versions(self) -> Dict[str, Any]:
        url = "https://tr.wikipedia.org/wiki/Android"
        req = self.session.get(url)
        soup = BeautifulSoup(req.content, "html.parser")
        
        version_list = []
        version_dicts = {}
        skipped_version = ['1.0', '1.1', '1.5', '1.6', '2.0', '2.1', '2.2', '2.2.3', 
                          '2.3', '2.3.7', '3.0', '3.2.6', '4.0', '4.0.4', '4.1', '4.3.1']
        
        table = soup.find("table", {"class": "wikitable"})
        if table:
            tr_list = table.find("tbody").find_all("tr")
            
            for tr in tr_list:
                try:
                    tds = tr.find_all("td")
                    if tds:
                        versions = str(tds[0].text).strip().split("-")
                        for version in versions:
                            version_clean = version.strip()
                            if version_clean and version_clean not in skipped_version:
                                android_str = f"Linux;Android {version_clean}"
                                version_list.append(android_str)
                                version_dicts[android_str] = datetime.datetime.now()
                except (IndexError, AttributeError):
                    continue
        
        return {"Version_list": version_list, "Version_dict": version_dicts}
    
    def fetch_macos_versions(self) -> Dict[str, Any]:
        urls = ["https://en.wikipedia.org/wiki/OS_X_Mountain_Lion","https://en.wikipedia.org/wiki/OS_X_Mavericks","https://en.wikipedia.org/wiki/OS_X_Yosemite",
            "https://en.wikipedia.org/wiki/OS_X_El_Capitan","https://en.wikipedia.org/wiki/MacOS_Sierra","https://en.wikipedia.org/wiki/MacOS_High_Sierra",
            "https://en.wikipedia.org/wiki/MacOS_Mojave","https://en.wikipedia.org/wiki/MacOS_Catalina"]
        urls2 = ["https://en.wikipedia.org/wiki/MacOS_Big_Sur","https://en.wikipedia.org/wiki/MacOS_Monterey","https://en.wikipedia.org/wiki/MacOS_Ventura"]
        session = requests.Session()
        session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.5304 Safari/537.36'})
        version_list = []
        version_dicts = {}
        devices = ["iPhone","iPad","Macintosh"]
        for url in urls :
            req = session.get(url)
            soup = BeautifulSoup(req.content,"html.parser")  
            tr_list = soup.find_all("table",{"class":"wikitable"})[0].find("tbody").find_all("tr")
            for tr in tr_list :
                try :
                    if "." in tr.find_all("td")[0].text :
                        rdm_chc = random.choice(devices)
                        version_list.append("%s; Intel Mac OS X %s"%(rdm_chc,str(tr.find_all("td")[0].text).strip()))
                        version_dicts.update({"%s; Intel Mac OS X %s"%(rdm_chc,str(tr.find_all("td")[0].text).strip()):datetime.datetime.now()})

                except:
                    pass
        for url in urls2 :
            req = session.get(url)
            soup = BeautifulSoup(req.content,"html.parser")  
            tr_list = soup.find_all("table",{"class":"wikitable"})[1].find("tbody").find_all("tr")
            for tr in tr_list :
                try :
                    if "." in str(tr.find("th").text).strip() :
                        rdm_chc = random.choice(devices)
                        version_list.append("%s; Intel Mac OS X %s"%(rdm_chc,str(tr.find("th").text).strip().split("[")[0]))
                        version_dicts.update({"%s; Intel Mac OS X %s"%(rdm_chc,str(tr.find("th").text).strip().split("[")[0]):datetime.datetime.now()})
                except:
                    pass     
        pop_index = version_list[-1]
        version_list.pop(-1)
        version_dicts.pop(pop_index)
        return {"Version_list":version_list,"Version_dict":version_dicts}      
