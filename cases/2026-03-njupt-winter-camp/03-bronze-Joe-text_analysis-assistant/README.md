# AMD ROCm-based Universal Text Depth Analysis Assistant
[中文版本](./README_ZH.md)

## Project Introduction
This project is a high-performance intelligent text analysis tool built for the **2026 NJUPT Winter Camp - AMD ROCm Special Event**, deeply optimized for the **aup-learning-cloud Basic GPU Environment**. Based on the Jupyter Notebook interactive development environment, the project provides an out-of-the-box experience with zero-configuration deployment. By deeply leveraging AMD ROCm GPU acceleration, it improves overall text analysis efficiency by **3–5 times** compared with traditional CPU solutions, effectively solving practical engineering pain points such as long text lag, cumbersome multi-text comparison, unstructured analysis results, and context truncation.

The project constructs a complete workflow covering **single-text parsing, multi-text comparison, ultra-long text processing, and structured report export**:
- Single-text analysis supports 10-dimensional structured parsing, including abstract extraction, keyword extraction, sentiment analysis, topic recognition, core argument induction, logical structure decomposition, evidence extraction, potential assumption mining, application scenario analysis, and limitation evaluation.
- Multi-text comparison automatically mines common features, compares differences, analyzes logical relationships, and evaluates complementary values, generating standardized comparison tables and analysis reports.
- Ultra-long text processing adopts a three-level strategy: semantic segmentation, sliding window merging, and block summarization, breaking through model context length limits and achieving complete, continuous analysis of 10,000+ word texts.
- Dual-format report export (Markdown/JSON) balances readability and reusability for learning, research, and engineering scenarios.

Technically, the project adopts a fully asynchronous high-availability architecture with asynchronous API calls based on aiohttp, combined with automatic retry, rate limiting, result caching, and other engineering mechanisms to ensure stability in multi-user concurrent scenarios. Through prompt engineering optimization (Chain-of-Thought + bilingual Few-shot examples), the accuracy and structured integrity of outputs are greatly improved. The solution is lightweight and compatible with office-grade AMD GPUs, making ROCm acceleration accessible without high-end hardware, suitable for both beginners and advanced developers.

## Competition Information
- Competition Name: 2026 NJUPT Winter Camp - AMD ROCm Special Event
- Author: Joe
- Award: Bronze Award (Third Prize)
- Run Files: main.ipynb (English), main_zh.ipynb (Chinese)

## Runtime Environment
### Basic Requirements
- Platform: aup-learning-cloud Basic GPU Environment
- Acceleration: AMD GPU (ROCm gfx906 or above)
- IDE: JupyterLab / Jupyter Notebook
- Built-in Services: Ollama, PyTorch, ROCm SDK (pre-installed)

### Core Dependencies
| Package | Version | Core Purpose |
| ---- | ---- | ---- |
| tiktoken | ≥0.7.0 | Token counting & intelligent long text segmentation |
| aiohttp | ≥3.9.0 | Asynchronous API calls & concurrent performance |
| ipywidgets | ≥8.1.2 | Interactive UI components & visual panels |
| nest_asyncio | ≥1.6.0 | Fix async loop compatibility in Jupyter |

Installation Command:
```bash
pip install -r requirements.txt
```

## Quick Start Guide
1. Log in to the aup-learning-cloud platform and launch the Basic GPU Environment.
2. Enter the project directory and install dependencies.
3. Open main.ipynb (English) or main_zh.ipynb (Chinese) in JupyterLab.
4. Run all cells sequentially and wait for the UI to load (≈30 seconds).
5. Upload TXT files via the interactive panel and select the analysis module.
6. View structured results and export reports in Markdown/JSON format.

## Core Features
### 1. ROCm Environment One-Stop Detection
Automatically verifies GPU recognition, ROCm acceleration status, Ollama connectivity, model availability, and network status, with visual diagnostics and repair guidance.

### 2. 10-Dimensional Single-Text Deep Analysis
- Abstract: 50–100 word objective summary
- Keywords: 10–15 high-value terms extraction
- Sentiment: Polarity classification with confidence
- Topic: Core theme and subfield recognition
- Arguments: Key claims and viewpoints induction
- Logic: Paragraph relationship and reasoning structure
- Evidence: Data, cases, and factual support extraction
- Assumptions: Implied premises and hidden assumptions
- Scenarios: Applicable domains and usage boundaries
- Limitations: Objective evaluation of biases and flaws

### 3. Multi-Text In-Depth Comparison
Supports batch upload of 2–5 texts and automatically performs:
- Common feature extraction
- Multi-dimensional difference comparison table
- Logical relationship analysis (complementary, progressive, conflicting)
- Integrated application recommendations

### 4. Ultra-Long Text Intelligent Engine
Three-stage processing for extremely long documents:
1. Semantic & token-based intelligent segmentation
2. Block parallel analysis with context preservation
3. Sliding window merging & global summarization
Eliminates context truncation completely.

### 5. Dual-Format Structured Report Export
- Markdown: Clean, readable layout for documentation
- JSON: Standardized structure for program parsing & development
Covers all analysis dimensions without manual formatting.

### 6. Zero-Code Interactive Interface
Full web-based visual operation: upload, run, preview, history, export—all via clicks. No CLI required, extremely beginner-friendly.

## Technical Innovations & Highlights
1. **Lightweight ROCm Acceleration**
Optimized for office AMD GPUs; 3–5x speedup without high-end hardware.

2. **Long Text Processing Algorithm**
Innovative semantic segmentation + sliding window + block summarization supports 32k+ tokens.

3. **Fully Asynchronous High-Availability Architecture**
Asynchronous I/O, retry, rate limit, timeout, and caching ensure stable concurrent usage.

4. **Advanced Prompt Engineering**
Built-in CoT reasoning, structured constraints, and bilingual Few-shot examples improve accuracy and consistency.

5. **End-to-End Engineering Reliability**
Input validation, sensitive info filtering, exception catching, logging, and error handling.

6. **Single-File Out-of-the-Box Design**
All logic embedded in Notebook; simple deployment, easy demonstration, and learning-friendly.

## Demo Flow & Expected Performance
### Standard Demo Steps
1. Environment check: Show ROCm acceleration status
2. Single-text analysis: Generate 10-dimensional report
3. Multi-text comparison: Display contrast table
4. Long-text processing: Verify no truncation
5. Report export: Show formatted Markdown output

### Expected Results
- Short text: Full analysis within 30 seconds
- Long text: 10,000+ words processed within 2 minutes
- Acceleration: 3x+ speedup over CPU
- Quality: Structured, logical, accuracy ≥90%

## Project Notes
- Fully compliant with 2026 NJUPT Winter Camp AMD ROCm submission specifications
- Includes bilingual docs, runnable code, full dependencies, and user guide
- Fully tested on the official aup-learning-cloud environment
- Well-commented code suitable for ROCm and NLP learning
- Extensible for text classification, generation, and knowledge extraction

## Author Information
- Author: Joe
- Award: Bronze Award (Third Prize)
- Project Path: cases/03-bronze-Joe-text_analysis-assistant
- Troubleshooting: Refer to Ollama API, AMD ROCm, JupyterLab official docs

## References
- Ollama API Docs: https://ollama.readthedocs.io/api/
- AMD ROCm Docs: https://rocm.docs.amd.com/
- JupyterLab Docs: https://jupyterlab.readthedocs.io/
