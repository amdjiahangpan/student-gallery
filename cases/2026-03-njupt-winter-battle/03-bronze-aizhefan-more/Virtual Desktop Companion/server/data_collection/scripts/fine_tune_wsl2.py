import json
import torch
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    BitsAndBytesConfig,
    TrainingArguments,
    Trainer
)
from peft import LoraConfig, get_peft_model

# 加载数据
def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

# 数据预处理
def preprocess_data(data):
    formatted_data = []
    for item in data:
        instruction = item.get('instruction', '')
        input_text = item.get('input', '')
        output_text = item.get('output', '')
        
        # 构建训练样本
        prompt = f"### Instruction:\n{instruction}\n\n### Input:\n{input_text}\n\n### Output:\n"
        formatted_data.append({
            'prompt': prompt,
            'completion': output_text
        })
    return formatted_data

# 主函数
def main():
    # 加载数据
    train_data = load_data('data_collection/processed_data/train_data.json')
    val_data = load_data('data_collection/processed_data/val_data.json')
    
    # 预处理数据
    train_dataset = preprocess_data(train_data)
    val_dataset = preprocess_data(val_data)
    
    # 配置模型
    model_name = "Qwen/Qwen2.5-Coder-3B-Instruct"  # 示例模型，替换为实际使用的模型
    
    # 配置量化
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16
    )
    
    # 加载模型和分词器
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        quantization_config=bnb_config,
        device_map="auto"
    )
    
    # 配置LoRA
    lora_config = LoraConfig(
        r=64,
        lora_alpha=16,
        target_modules=["q_proj", "v_proj"],
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM"
    )
    
    # 创建Peft模型
    model = get_peft_model(model, lora_config)
    
    # 配置训练参数
    training_args = TrainingArguments(
        output_dir="./results",
        num_train_epochs=3,
        per_device_train_batch_size=4,
        per_device_eval_batch_size=4,
        gradient_accumulation_steps=2,
        learning_rate=2e-4,
        lr_scheduler_type="cosine",
        warmup_ratio=0.05,
        weight_decay=0.01,
        logging_steps=10,
        eval_strategy="steps",
        eval_steps=50,
        save_strategy="steps",
        save_steps=50,
        load_best_model_at_end=True,
        fp16=True,
        optim="adamw_torch"
    )
    
    # 创建训练器
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        tokenizer=tokenizer
    )
    
    # 开始训练
    trainer.train()
    
    # 保存模型
    model.save_pretrained("./wsl2-expert-model")
    tokenizer.save_pretrained("./wsl2-expert-model")
    
    print("微调完成！模型已保存到 ./wsl2-expert-model")

if __name__ == "__main__":
    main()
