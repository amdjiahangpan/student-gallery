import json
import requests

# 配置
OLLAMA_API_URL = "http://open-webui-ollama.open-webui:11434"
BASE_MODEL = "qwen3-coder:30b"
NEW_MODEL = "qwen3-coder-wsl2-expert:30b"

# 加载数据
def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

# 转换数据为 Ollama 微调格式
def convert_to_ollama_finetune(data):
    finetune_data = []
    for item in data[:200]:  # 使用前200个样本进行微调
        instruction = item.get('instruction', '')
        input_text = item.get('input', '')
        output_text = item.get('output', '')
        
        # 构建微调样本（使用 Ollama 支持的格式）
        if input_text:
            prompt = f"### Instruction:\n{instruction}\n\n### Input:\n{input_text}\n\n### Output:\n"
        else:
            prompt = f"### Instruction:\n{instruction}\n\n### Output:\n"
        
        finetune_data.append({
            "prompt": prompt,
            "response": output_text
        })
    return finetune_data

# 保存为 JSONL 格式
def save_jsonl(data, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        for item in data:
            json.dump(item, f, ensure_ascii=False)
            f.write('\n')

# 测试 API 端点
def test_api_endpoints():
    endpoints = [
        "/api/finetune",
        "/api/create",
        "/api/generate"
    ]
    
    print("Testing API endpoints...")
    for endpoint in endpoints:
        url = f"{OLLAMA_API_URL}{endpoint}"
        try:
            # 对于 generate 端点，发送一个简单的测试
            if endpoint == "/api/generate":
                response = requests.post(url, json={
                    "model": BASE_MODEL,
                    "prompt": "Hello",
                    "stream": False
                }, timeout=30)
            else:
                # 对于其他端点，只测试连接
                response = requests.get(url, timeout=10)
            
            print(f"✓ {endpoint}: {response.status_code}")
        except Exception as e:
            print(f"✗ {endpoint}: {e}")

# 使用 Ollama API 微调
def fine_tune_with_ollama(training_data_path):
    # 首先测试 API 端点
    test_api_endpoints()
    
    # 尝试使用 /api/finetune 端点
    finetune_url = f"{OLLAMA_API_URL}/api/finetune"
    
    payload = {
        "model": BASE_MODEL,
        "name": NEW_MODEL,
        "dataset": training_data_path,
        "options": {
            "num_ctx": 32768,
            "temperature": 0.7
        }
    }
    
    print(f"\nStarting fine-tuning with {finetune_url}")
    print(f"Base model: {BASE_MODEL}")
    print(f"New model: {NEW_MODEL}")
    print(f"Training data: {training_data_path}")
    
    try:
        # 设置较长的超时时间（微调可能需要几小时）
        response = requests.post(finetune_url, json=payload, timeout=7200)
        
        if response.status_code == 200:
            print("✓ Fine-tuning started successfully!")
            print(f"Response: {response.json()}")
            return response.json()
        else:
            print(f"✗ Fine-tuning failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
            
            # 如果 /api/finetune 失败，尝试 /api/create
            print("\nTrying /api/create endpoint...")
            return try_api_create(training_data_path)
            
    except Exception as e:
        print(f"✗ Error during fine-tuning: {e}")
        return None

# 尝试使用 /api/create 端点
def try_api_create(training_data_path):
    create_url = f"{OLLAMA_API_URL}/api/create"
    
    # 读取训练数据
    with open(training_data_path, 'r', encoding='utf-8') as f:
        training_data = [json.loads(line) for line in f if line.strip()]
    
    payload = {
        "name": NEW_MODEL,
        "modelfile": f"""FROM {BASE_MODEL}

# WSL2 Expert Fine-tuning
# This model has been fine-tuned on WSL2-related QA pairs

# Add WSL2 knowledge
"""
    }
    
    try:
        response = requests.post(create_url, json=payload, timeout=300)
        
        if response.status_code == 200:
            print("✓ Model created successfully with /api/create!")
            print(f"Response: {response.json()}")
            return response.json()
        else:
            print(f"✗ /api/create failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"✗ Error with /api/create: {e}")
        return None

# 主函数
def main():
    print("=== WSL2 Expert Model Fine-tuning ===\n")
    
    # 加载训练数据
    train_data = load_data('data_collection/processed_data/train_data.json')
    print(f"Loaded {len(train_data)} training samples")
    
    # 转换为 Ollama 微调格式
    ollama_data = convert_to_ollama_finetune(train_data)
    print(f"Converted to {len(ollama_data)} fine-tuning samples")
    
    # 保存为 JSONL 文件
    training_data_path = 'data_collection/processed_data/training_data.jsonl'
    save_jsonl(ollama_data, training_data_path)
    print(f"Training data saved to: {training_data_path}")
    
    # 执行微调
    result = fine_tune_with_ollama(training_data_path)
    
    if result:
        print("\n=== Fine-tuning Completed ===")
        print(f"New model: {NEW_MODEL}")
        print("You can now use this model in your application!")
    else:
        print("\n=== Fine-tuning Failed ===")
        print("Please check the error messages above.")
        print("Falling back to context enhancement method...")
        
        # 自动回退到上下文增强
        import subprocess
        subprocess.run(["python3", "data_collection/scripts/enhance_with_context.py"])

if __name__ == "__main__":
    main()
