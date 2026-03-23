import json
import requests

# 配置
OLLAMA_API_URL = "http://open-webui-ollama.open-webui:11434"
MODEL_NAME = "qwen3-coder:30b"
NEW_MODEL_NAME = "qwen3-coder-wsl2-expert:30b"

# 加载数据
def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

# 转换数据为 Ollama 格式
def convert_to_ollama_format(data):
    ollama_data = []
    for item in data:
        instruction = item.get('instruction', '')
        input_text = item.get('input', '')
        output_text = item.get('output', '')
        
        # 构建训练样本
        prompt = f"### Instruction:\n{instruction}\n\n### Input:\n{input_text}\n\n### Output:\n"
        ollama_data.append({
            "prompt": prompt,
            "response": output_text
        })
    return ollama_data

# 保存为 JSONL 格式
def save_jsonl(data, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        for item in data:
            json.dump(item, f, ensure_ascii=False)
            f.write('\n')

# 使用 Ollama API 微调
def fine_tune_with_ollama(training_data_path):
    url = f"{OLLAMA_API_URL}/api/create"
    
    payload = {
        "name": NEW_MODEL_NAME,
        "model": MODEL_NAME,
        "files": [training_data_path],
        "parameters": {
            "num_ctx": 32768,
            "temperature": 0.7
        }
    }
    
    try:
        response = requests.post(url, json=payload, timeout=3600)
        response.raise_for_status()
        print("微调成功！")
        print(f"新模型名称: {NEW_MODEL_NAME}")
        return response.json()
    except Exception as e:
        print(f"微调失败: {e}")
        return None

# 主函数
def main():
    # 加载训练数据
    train_data = load_data('data_collection/processed_data/train_data.json')
    
    # 转换为 Ollama 格式
    ollama_data = convert_to_ollama_format(train_data)
    
    # 保存为 JSONL 文件
    training_data_path = 'data_collection/processed_data/training_data.jsonl'
    save_jsonl(ollama_data, training_data_path)
    print(f"训练数据已保存到: {training_data_path}")
    
    # 执行微调
    result = fine_tune_with_ollama(training_data_path)
    if result:
        print("微调完成！")
        print(f"新模型: {NEW_MODEL_NAME}")
    else:
        print("微调失败，请检查错误信息。")

if __name__ == "__main__":
    main()
