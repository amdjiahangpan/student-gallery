import requests
import json
import os
import base64

class GitHubAnalyzer:
    def __init__(self):
        self.base_url = "https://api.github.com"
        self.output_dir = "data_collection/raw_data/github"
        os.makedirs(self.output_dir, exist_ok=True)
        
        self.data = []
        self.max_repos = 50
        
        self.wsl_keywords = ["wsl", "windows-subsystem-for-linux", "wsl2"]
    
    def search_repos(self, keyword):
        print(f"Searching repositories with keyword '{keyword}'...")
        
        url = f"{self.base_url}/search/repositories"
        params = {
            "q": f"{keyword} in:name,description,readme",
            "sort": "stars",
            "order": "desc",
            "per_page": 30
        }
        
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            for repo in data.get("items", [])[:self.max_repos]:
                self.analyze_repo(repo)
                
            print(f"  Found {len(data.get('items', []))} related repositories")
            
        except Exception as e:
            print(f"  Search failed: {e}")
    
    def analyze_repo(self, repo):
        repo_name = repo.get("full_name")
        print(f"  Analyzing repository: {repo_name}")
        
        try:
            readme_url = f"{self.base_url}/repos/{repo_name}/readme"
            readme_response = requests.get(readme_url, timeout=30)
            
            if readme_response.status_code == 200:
                readme_data = readme_response.json()
                readme_content = base64.b64decode(readme_data.get("content", "")).decode('utf-8', errors='ignore')
            else:
                readme_content = ""
            
            repo_data = {
                "id": repo.get("id"),
                "name": repo.get("name"),
                "full_name": repo.get("full_name"),
                "description": repo.get("description"),
                "stars": repo.get("stargazers_count"),
                "forks": repo.get("forks_count"),
                "open_issues": repo.get("open_issues_count"),
                "url": repo.get("html_url"),
                "clone_url": repo.get("clone_url"),
                "readme_content": readme_content,
                "created_at": repo.get("created_at"),
                "updated_at": repo.get("updated_at"),
                "source": "github"
            }
            
            self.extract_wsl_info(repo_data)
            
            self.data.append(repo_data)
            
            safe_name = repo_name.replace('/', '_')[:50]
            with open(os.path.join(self.output_dir, f"repo_{safe_name}.json"), 'w', encoding='utf-8') as f:
                json.dump(repo_data, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f"  Failed to analyze repository {repo_name}: {e}")
    
    def extract_wsl_info(self, repo_data):
        content = repo_data.get("readme_content", "")
        
        wsl_info = {
            "config_examples": [],
            "commands": [],
            "tips": [],
            "troubleshooting": []
        }
        
        lines = content.split('\n')
        for i, line in enumerate(lines):
            line_lower = line.lower()
            
            if any(keyword in line_lower for keyword in ["wsl.conf", ".wslconfig", "wslconfig"]):
                config_lines = []
                for j in range(i, min(i + 20, len(lines))):
                    config_lines.append(lines[j])
                    if lines[j].strip() == '' and j > i + 5:
                        break
                wsl_info["config_examples"].append('\n'.join(config_lines))
            
            elif any(keyword in line_lower for keyword in ["wsl ", "wsl.exe"]):
                wsl_info["commands"].append(line.strip())
            
            elif any(keyword in line_lower for keyword in ["tip", "trick", "best practice"]):
                wsl_info["tips"].append(line.strip())
            
            elif any(keyword in line_lower for keyword in ["troubleshoot", "error", "fix"]):
                wsl_info["troubleshooting"].append(line.strip())
        
        repo_data["wsl_info"] = wsl_info
    
    def run(self):
        print("Starting to analyze GitHub WSL repositories...")
        
        for keyword in self.wsl_keywords:
            self.search_repos(keyword)
        
        seen_ids = set()
        unique_data = []
        for item in self.data:
            if item["id"] not in seen_ids:
                seen_ids.add(item["id"])
                unique_data.append(item)
        
        self.data = unique_data
        
        with open(os.path.join(self.output_dir, "all_repos.json"), 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
        
        print(f"\nAnalysis completed. Processed {len(self.data)} repositories")
        print(f"Data saved to: {self.output_dir}")

if __name__ == "__main__":
    analyzer = GitHubAnalyzer()
    analyzer.run()
