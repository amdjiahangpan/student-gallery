# Project Title <!-- required -->

Intelligent Text Analysis and Reporting Assistant Based on LLM

[中文版本](./README_ZH.md)

## Project Overview <!-- required -->

This project is an intelligent assistant system designed for data processing and text mining. Relying on a locally deployed LLM cluster, it aims to perform deep structural extraction and multi-dimensional analysis on massive unstructured Chinese and English texts (e.g., course materials, academic papers, and assignments). Core features include intelligent summarization, sentiment analysis, and key feature extraction. Advanced features support batch processing pipelines and multi-document comparative analysis.

## Activity Information <!-- required -->

- **Competition / Workshop:** 2026 NJUPT Winter Battle <!-- required: replace with your activity name -->
- **Team Members:** Fengyi Li, Hongqing Du <!-- required: list all team members -->
- **Awarded:** Gold / Silver / Bronze / N/A <!-- required: use N/A if not yet announced -->

## Environment <!-- required -->

- **Base Image:** Basic GPU Environment (aup-learning-cloud)
- **Extra Dependencies:** Listed in `requirements.txt` <!-- required: briefly describe key packages if any, or write "None" -->

## Quick Start <!-- required -->

<!-- Step-by-step instructions to run your notebook. Be specific. -->

1. In aup-learning-cloud, select **Basic GPU Environment** and set the Git URL to this repository
2. Navigate to `cases/<activity-folder>/<your-folder>/`
3. Open `main.ipynb`
4. Run all cells from top to bottom

## Technical Highlights

1.Prompt Engineering Evolution: The prompt design went through four iterations, transitioning from simple zero-shot instructions to introducing System Roles and strict formatting constraints. It further utilized Few-shot prompting to anchor sentiment scoring scales and Chain-of-Thought (CoT) reasoning to overcome complex logical deduction tasks.
2.Context Window Management: To address the 32k token limit and Out-Of-Memory (OOM) exceptions caused by extremely long texts, the system implements a task-driven asymmetrical context dimensionality reduction strategy. This includes cascaded summary generation and an adaptive context window allocation algorithm using the formula $L_{alloc}=\lfloor\frac{L_{max}}{N}\rfloor
3.Cluster Resource and API Lifecycle Management: Designed a comprehensive API lifecycle management mechanism, including input validity checks, timeout control, exception catching, retry strategies, and rate-limiting handling. The system employs a linear backoff strategy to retry during server rate limits or transient network anomalies, effectively avoiding "retry storms".
4.Heterogeneous Data Parsing & Robust Pipeline: Achieved polymorphic data normalization by converting various underlying buffer structures (like memoryview) into immutable byte streams. It also features a pre-execution circuit breaker mechanism based on the observer pattern, utilizing lightweight probes to pre-scan file headers and content validity to isolate abnormal inputs without breaking the entire batch pipeline
5.Asynchronous Concurrency and I/O Masking: Adopts an asynchronous concurrent architecture based on ThreadPoolExecutor. It distributes the three independent subtasks (summarization, sentiment analysis, and keyword extraction) in parallel. This effectively masks network I/O wait times and significantly boosts pipeline throughput without increasing GPU memory load.
6.I/O Architecture Optimization and Frontend: To overcome the single-transfer rate bottleneck of WebSockets in the Jupyter environment (IOPub data rate exceeded) , the system implements a dual-modal I/O architecture and adds a server-side file system direct-read module. The frontend GUI is built with native ipywidgets, achieving an embedded interactive interface without requiring extra port mapping.

## Results / Demo

Real-time File Dashboard: Provides a real-time monitor for file parsing status, extracted character count, and estimated Token consumption, including smart alerts for exceeding text limits.
Batch Analysis Pipeline: Breaks single-request limits, automatically outputting standardized Markdown reports containing summaries, sentiment scores, and keywords to achieve machine-level efficient review.
Multi-Document Comparative Report: Overcomes single-text limitations; the system automatically summarizes and generates a structured deep analysis report encompassing "core themes, commonalities, and key differences" across multiple documents.

## References


