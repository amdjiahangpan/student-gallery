import json
import os
import re
from bs4 import BeautifulSoup

class DataProcessor:
    def __init__(self):
        self.raw_data_dir = "data_collection/raw_data"
        self.processed_data_dir = "data_collection/processed_data"
        os.makedirs(self.processed_data_dir, exist_ok=True)
        
        self.data = []
        
        self.source_weights = {
            "microsoft_docs": 1.0,
            "stackoverflow": 0.8,
            "github": 0.6
        }
    
    def clean_text(self, text):
        soup = BeautifulSoup(text, 'html.parser')
        text = soup.get_text()
        
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\s\-\.,!\?()\[\]{}:;/]', '', text)
        text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
        text = re.sub(r'`.*?`', '', text)
        
        return text.strip()
    
    def extract_qa_from_docs(self):
        docs_dir = os.path.join(self.raw_data_dir, "docs")
        if not os.path.exists(docs_dir):
            return
        
        print("Processing Microsoft documentation...")
        
        for file_name in os.listdir(docs_dir):
            if file_name.endswith('.json'):
                file_path = os.path.join(docs_dir, file_name)
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        doc_data = json.load(f)
                    
                    title = doc_data.get("title", "")
                    content = doc_data.get("content", "")
                    commands = doc_data.get("commands", [])
                    configs = doc_data.get("configs", [])
                    
                    if title and content:
                        qa = {
                            "instruction": f"Explain {title}",
                            "input": "",
                            "output": content,
                            "source": "microsoft_docs",
                            "weight": self.source_weights["microsoft_docs"]
                        }
                        self.data.append(qa)
                    
                    for command in commands:
                        command = command.strip()
                        if command:
                            qa = {
                                "instruction": f"Explain command: {command}",
                                "input": "",
                                "output": f"This command is used for: {command}\n\nWhen executed, it will: TODO",
                                "source": "microsoft_docs",
                                "weight": self.source_weights["microsoft_docs"]
                            }
                            self.data.append(qa)
                    
                    for config in configs:
                        config = config.strip()
                        if config:
                            qa = {
                                "instruction": "Explain WSL configuration:",
                                "input": config,
                                "output": f"This configuration is used for: TODO\n\nConfiguration explanation: TODO",
                                "source": "microsoft_docs",
                                "weight": self.source_weights["microsoft_docs"]
                            }
                            self.data.append(qa)
                            
                except Exception as e:
                    print(f"  Failed to process {file_name}: {e}")
    
    def extract_qa_from_stackoverflow(self):
        so_dir = os.path.join(self.raw_data_dir, "stackoverflow")
        if not os.path.exists(so_dir):
            return
        
        print("Processing Stack Overflow questions...")
        
        for file_name in os.listdir(so_dir):
            if file_name.endswith('.json'):
                file_path = os.path.join(so_dir, file_name)
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        question_data = json.load(f)
                    
                    title = question_data.get("title", "")
                    body = question_data.get("body", "")
                    answers = question_data.get("answers", [])
                    
                    if title and answers:
                        clean_title = self.clean_text(title)
                        clean_body = self.clean_text(body)
                        
                        best_answer = answers[0] if answers else {}
                        clean_answer = self.clean_text(best_answer.get("body", ""))
                        
                        if clean_answer:
                            qa = {
                                "instruction": clean_title,
                                "input": clean_body,
                                "output": clean_answer,
                                "source": "stackoverflow",
                                "weight": self.source_weights["stackoverflow"]
                            }
                            self.data.append(qa)
                            
                except Exception as e:
                    print(f"  Failed to process {file_name}: {e}")
    
    def extract_qa_from_github(self):
        github_dir = os.path.join(self.raw_data_dir, "github")
        if not os.path.exists(github_dir):
            return
        
        print("Processing GitHub repositories...")
        
        for file_name in os.listdir(github_dir):
            if file_name.endswith('.json'):
                file_path = os.path.join(github_dir, file_name)
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        repo_data = json.load(f)
                    
                    name = repo_data.get("name", "")
                    description = repo_data.get("description", "")
                    wsl_info = repo_data.get("wsl_info", {})
                    
                    if name and description:
                        qa = {
                            "instruction": f"Introduce WSL tool: {name}",
                            "input": "",
                            "output": description,
                            "source": "github",
                            "weight": self.source_weights["github"]
                        }
                        self.data.append(qa)
                    
                    if wsl_info:
                        for config in wsl_info.get("config_examples", []):
                            config = self.clean_text(config)
                            if config:
                                qa = {
                                    "instruction": "Explain WSL configuration:",
                                    "input": config,
                                    "output": f"This configuration is used for: TODO\n\nConfiguration explanation: TODO",
                                    "source": "github",
                                    "weight": self.source_weights["github"]
                                }
                                self.data.append(qa)
                        
                        for command in wsl_info.get("commands", []):
                            command = self.clean_text(command)
                            if command:
                                qa = {
                                    "instruction": f"Explain command: {command}",
                                    "input": "",
                                    "output": f"This command is used for: TODO\n\nWhen executed, it will: TODO",
                                    "source": "github",
                                    "weight": self.source_weights["github"]
                                }
                                self.data.append(qa)
                                
                except Exception as e:
                    print(f"  Failed to process {file_name}: {e}")
    
    def filter_and_deduplicate(self):
        print("Filtering and deduplicating data...")
        
        filtered_data = []
        seen_questions = set()
        
        for item in self.data:
            instruction = item.get("instruction", "").strip()
            output = item.get("output", "").strip()
            
            if len(instruction) < 10 or len(output) < 20:
                continue
            
            if instruction not in seen_questions:
                seen_questions.add(instruction)
                filtered_data.append(item)
        
        self.data = filtered_data
        print(f"  Remaining {len(self.data)} items after filtering")
    
    def split_data(self):
        print("Splitting data...")
        
        total = len(self.data)
        train_size = int(total * 0.8)
        
        train_data = self.data[:train_size]
        val_data = self.data[train_size:]
        
        print(f"  Training set: {len(train_data)} items")
        print(f"  Validation set: {len(val_data)} items")
        
        return train_data, val_data
    
    def save_data(self, data, filename):
        output_path = os.path.join(self.processed_data_dir, filename)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"  Saved to: {output_path}")
    
    def run(self):
        print("Starting data processing...")
        
        self.extract_qa_from_docs()
        self.extract_qa_from_stackoverflow()
        self.extract_qa_from_github()
        
        self.filter_and_deduplicate()
        
        train_data, val_data = self.split_data()
        
        self.save_data(train_data, "train_data.json")
        self.save_data(val_data, "val_data.json")
        self.save_data(self.data, "all_data.json")
        
        print(f"\nData processing completed. Generated {len(self.data)} QA pairs")
        print(f"Data saved to: {self.processed_data_dir}")

if __name__ == "__main__":
    processor = DataProcessor()
    processor.run()
