import requests
import json
import os
from datetime import datetime

class StackOverflowCrawler:
    def __init__(self):
        self.base_url = "https://api.stackexchange.com/2.3"
        self.output_dir = "data_collection/raw_data/stackoverflow"
        os.makedirs(self.output_dir, exist_ok=True)
        
        self.data = []
        self.max_pages = 50
        self.page_size = 100
        
        self.wsl_tags = ["wsl", "wsl-2", "windows-subsystem-for-linux"]
    
    def fetch_questions(self, tag):
        print(f"Fetching questions with tag '{tag}'...")
        
        for page in range(1, self.max_pages + 1):
            url = f"{self.base_url}/questions"
            params = {
                "tagged": tag,
                "sort": "votes",
                "order": "desc",
                "site": "stackoverflow",
                "pagesize": self.page_size,
                "page": page,
                "filter": "withbody"
            }
            
            try:
                response = requests.get(url, params=params, timeout=30)
                response.raise_for_status()
                
                data = response.json()
                
                if not data.get("items"):
                    break
                
                for item in data["items"]:
                    self.process_question(item)
                
                if not data.get("has_more", False):
                    break
                
                print(f"  Fetched {len(data['items'])} questions (page {page})")
                
            except Exception as e:
                print(f"  Failed: {e}")
                break
    
    def process_question(self, question):
        if (question.get("is_answered") and 
            question.get("score", 0) >= 1 and
            question.get("answer_count", 0) >= 1):
            
            question_data = {
                "id": question.get("question_id"),
                "title": question.get("title"),
                "body": question.get("body"),
                "score": question.get("score"),
                "answer_count": question.get("answer_count"),
                "view_count": question.get("view_count"),
                "tags": question.get("tags"),
                "creation_date": datetime.fromtimestamp(question.get("creation_date")).isoformat(),
                "answers": [],
                "source": "stackoverflow"
            }
            
            best_answer = self.get_best_answer(question.get("question_id"))
            if best_answer:
                question_data["answers"].append(best_answer)
            
            self.data.append(question_data)
            
            with open(os.path.join(self.output_dir, f"q_{question.get('question_id')}.json"), 'w', encoding='utf-8') as f:
                json.dump(question_data, f, ensure_ascii=False, indent=2)
    
    def get_best_answer(self, question_id):
        url = f"{self.base_url}/questions/{question_id}/answers"
        params = {
            "sort": "votes",
            "order": "desc",
            "site": "stackoverflow",
            "filter": "withbody",
            "pagesize": 1
        }
        
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get("items"):
                answer = data["items"][0]
                return {
                    "id": answer.get("answer_id"),
                    "body": answer.get("body"),
                    "score": answer.get("score"),
                    "creation_date": datetime.fromtimestamp(answer.get("creation_date")).isoformat()
                }
        
        except Exception as e:
            print(f"  Failed to get answer: {e}")
        
        return None
    
    def run(self):
        print("Starting to fetch Stack Overflow WSL questions...")
        
        for tag in self.wsl_tags:
            self.fetch_questions(tag)
        
        seen_ids = set()
        unique_data = []
        for item in self.data:
            if item["id"] not in seen_ids:
                seen_ids.add(item["id"])
                unique_data.append(item)
        
        self.data = unique_data
        
        with open(os.path.join(self.output_dir, "all_questions.json"), 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
        
        print(f"\nFetching completed. Collected {len(self.data)} high-quality questions")
        print(f"Data saved to: {self.output_dir}")

if __name__ == "__main__":
    crawler = StackOverflowCrawler()
    crawler.run()
