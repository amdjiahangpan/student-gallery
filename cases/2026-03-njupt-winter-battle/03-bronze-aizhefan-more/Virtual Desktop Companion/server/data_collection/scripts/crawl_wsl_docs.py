import requests
import re
import json
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

class WSLDocsCrawler:
    def __init__(self):
        self.base_url = "https://learn.microsoft.com"
        self.start_urls = [
            "https://learn.microsoft.com/en-us/windows/wsl/",
            "https://learn.microsoft.com/en-us/windows/wsl/basic-commands",
            "https://learn.microsoft.com/en-us/windows/wsl/wsl-config",
            "https://learn.microsoft.com/en-us/windows/wsl/troubleshooting",
            "https://learn.microsoft.com/en-us/windows/wsl/setup/environment"
        ]
        
        self.output_dir = "data_collection/raw_data/docs"
        os.makedirs(self.output_dir, exist_ok=True)
        
        self.visited_urls = set()
        self.data = []
        
        self.wsl_keywords = [
            "wsl", "wslconf", "wslconfig", "docker", "gpu", 
            "network", "performance", "memory", "cpu", "mount"
        ]
    
    def is_wsl_related(self, url):
        path = urlparse(url).path.lower()
        return any(keyword in path for keyword in self.wsl_keywords)
    
    def extract_commands(self, text):
        command_patterns = [
            r'wsl\s+[^\n]+',
            r'wsl\.exe\s+[^\n]+',
            r'wslconfig\.exe\s+[^\n]+',
            r'docker\s+[^\n]+',
            r'powershell\s+-command\s+[^\n]+'
        ]
        
        commands = []
        for pattern in command_patterns:
            commands.extend(re.findall(pattern, text, re.IGNORECASE))
        
        return commands
    
    def extract_config_examples(self, text):
        config_patterns = [
            r'$$wsl$$[^\[]+',
            r'$$wsl\.interop$$[^\[]+',
            r'$$wsl\.network$$[^\[]+',
            r'$$wsl\.autoMount$$[^\[]+',
            r'$$wsl\.memory$$[^\[]+',
            r'$$wsl\.processors$$[^\[]+'
        ]
        
        configs = []
        for pattern in config_patterns:
            configs.extend(re.findall(pattern, text, re.DOTALL | re.IGNORECASE))
        
        return configs
    
    def clean_text(self, text):
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        return text
    
    def crawl_page(self, url):
        if url in self.visited_urls:
            return
        
        self.visited_urls.add(url)
        print(f"Crawling: {url}")
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            title = soup.find('h1').get_text(strip=True) if soup.find('h1') else ""
            
            content = []
            for tag in soup.find_all(['p', 'ul', 'ol', 'pre', 'code', 'h2', 'h3', 'h4']):
                if tag.name == 'pre' or tag.name == 'code':
                    content.append(f"```\n{tag.get_text()}\n```")
                else:
                    content.append(tag.get_text(strip=True))
            
            page_content = '\n'.join(content)
            
            commands = self.extract_commands(page_content)
            configs = self.extract_config_examples(page_content)
            
            page_data = {
                "url": url,
                "title": title,
                "content": self.clean_text(page_content),
                "commands": commands,
                "configs": configs,
                "source": "microsoft_docs"
            }
            
            self.data.append(page_data)
            
            safe_title = re.sub(r'[^a-zA-Z0-9_]', '_', title)[:50]
            with open(os.path.join(self.output_dir, f"{safe_title}.json"), 'w', encoding='utf-8') as f:
                json.dump(page_data, f, ensure_ascii=False, indent=2)
            
            for link in soup.find_all('a', href=True):
                href = link['href']
                full_url = urljoin(self.base_url, href)
                
                if (full_url.startswith(self.base_url) and 
                    self.is_wsl_related(full_url) and 
                    full_url not in self.visited_urls):
                    self.crawl_page(full_url)
                    
        except Exception as e:
            print(f"Failed to crawl {url}: {e}")
    
    def run(self):
        print("Starting to crawl WSL documentation...")
        
        for start_url in self.start_urls:
            self.crawl_page(start_url)
        
        with open(os.path.join(self.output_dir, "all_docs.json"), 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
        
        print(f"Crawling completed. Collected {len(self.data)} pages")
        print(f"Data saved to: {self.output_dir}")

if __name__ == "__main__":
    crawler = WSLDocsCrawler()
    crawler.run()
