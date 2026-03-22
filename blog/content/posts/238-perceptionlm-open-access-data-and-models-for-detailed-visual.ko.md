---
title: "[217] PerceptionLM: Open-Access Data and Models for Detailed Visual Understanding"
date: 2025-11-03
tags: ['meta', '2025Q2', 'video']
paper: "https://arxiv.org/abs/2504.13180"
issue: 238
issueUrl: "https://github.com/long8v/PTIR/issues/238"
---
<img width="869" height="463" alt="Image" src="https://github.com/user-attachments/assets/6e916cd8-2bd5-4dc5-af98-08a7fe87d559" />

[paper](https://arxiv.org/abs/2504.13180), [code](https://github.com/facebookresearch/perception_models), [dataset](https://huggingface.co/datasets/facebook/PLM-Video-Human)

## TL;DR
- **I read this because.. :** video language model. fully open-source model. 
- **task :** video language model
- **problem :** closed model 기반 synthetic model 말고 fully open source로 만들고 싶다.
- **idea :** 여러 open source model (거의 meta 모델)을 기반으로 한 모델 (molmo랑 비슷한 motivation)
- **input/output :** (video, image, (optional) mask) + question -> answer
- **architecture :** VE {PE L/14, PE G/14} + LLM {Llama3.2 1B-3B,  Llama3.1 8B}
- **objective :** ce loss (alignment, mid-training, SFT)
- **baseline :** GPT4o, Gemini 1.5 Pro, Gemini 2.0 Flash, Qwen2VL, InternVL2.5, Qwen 3.5VL, Llava-OV
- **data :** pretrain 1M (from SA-1B + caption), mid-training 64.7M synthetic caption (LLaMa-3V-90B), SFT human-annotated 2.87M
- **evaluation :** image bench, video bench
- **result :** 준수한 성능 
- **contribution :** fully open source model. data도 공개! 
- **etc. :** 

## Details
- thumbnail

<img width="823" height="266" alt="Image" src="https://github.com/user-attachments/assets/9459c967-d04b-4a08-b69f-ce25aa462061" />

- overview
<img width="413" height="207" alt="Image" src="https://github.com/user-attachments/assets/a2ac283e-cf9e-472a-9edd-7f0cae99ea4c" />

### data
- overall
  - <img width="788" height="503" alt="Image" src="https://github.com/user-attachments/assets/17d3a561-5254-457d-a97b-3ee7b0b56d7a" />
- details 
  - <img width="710" height="715" alt="Image" src="https://github.com/user-attachments/assets/84220dee-f5ab-49c9-90a2-bb7fdaf91c70" />
  - all training data[^1]

#### synthetic data pipeline (66.1M) 
- image data engine 
  - image -natural image, documents 
  - give {caption, OCR, meta} - Lllama -> caption, QA
- video data
  - https://www.scenedetect.com/ 사용하여 30초짜리 비디오 클립 추출, {caption from Lllama-3V, video caption from initial PLM, video meta(action, time tags)} -- Llama3 --> caption, QA
- scaling law  
  - <img width="799" height="348" alt="Image" src="https://github.com/user-attachments/assets/2632e59d-c020-4eef-9343-81fe8774969f" />
- Limitation of synthetic data
  - <img width="334" height="302" alt="Image" src="https://github.com/user-attachments/assets/b2b1a141-9855-4d1c-b8d9-6cd70f9300fa" />
  - 어려운 문제에 대한 scaling law는 뚜렷하지 않음 -> human annotated 가 필요하겠다.

### human-annotated high quality data
- PLM-FGQA
  - fine-grained human activity
  - <img width="792" height="369" alt="Image" src="https://github.com/user-attachments/assets/75b428ed-cf47-4620-b123-d7573909db7c" />
-  PLM-STC
  - spatial-teomporal 
  - SAM2 사용하여 mask tublet을 만들고 annotators 들이 흥미롭고 움직이는 object를 찾으라고 한뒤에 다른 어노테이터들에게 비디오의 시간 상 action 상의 움직임에 대해 적으라고 함.
  - video-region caption (522.7K / train 476.2 / others PLM-VideoBench)
    - RCap (194.2K): Given the video region and timestamps, the model generates a caption; 
    - RTLoc (194.2K): Given the video region and caption, the model localizes the action; and 
    - RDCap (122.3K): Given the video region, the model generates dense, localized caption
- <img width="788" height="332" alt="Image" src="https://github.com/user-attachments/assets/5e75d7a5-364b-492a-9692-bf4c6fc2fc04" />
- Fine-Grained Question Answering (FGQA) : fine-grained activity understanding (e.g., painting “vertically” vs. “horizontally” in Fig. 6, first) 
  - MBAcc
    - 4371 question
  - Smart Glasses Question Answering (SGQA) : 
    - answer open-ended questions about activities and objects visible in an egocentric video stream recorded by a smartglasses device
    - LLM as a judge (Llama3.3 70B)
    - 665, human annotated
  - Video Region Captioning (RCap).
    - LLM as a judge (Llama3.3 70B)
    - 10,060 human annotated
  - Region Dense Video Captioning (RDCap).
    - model must generate a detailed description of all events involving a specific subject of interest (e.g., person, animal, or object)
    - must produce a sequence of (start, end, caption) tuples that cover the entire duration of the video, including periods when the subject is not visible
    - 2620 samples
    - SODA score (Soda: Story oriented dense video captioning evaluation framework)

## Results
### benchmarks
- PLM-VideoBench
  - <img width="475" height="422" alt="Image" src="https://github.com/user-attachments/assets/9037397c-fd5f-4052-90df-bdfd64364c61" />
  - GPT-4o가 
- video bench
  - <img width="784" height="446" alt="Image" src="https://github.com/user-attachments/assets/9b4857cf-d808-456b-a721-b1c477dd40be" />
  - VideoMME 가 차이 많이 나는군 
  - Charades-STA
    - [Tall: Temporal activity localization via language query](https://arxiv.org/pdf/1705.02101)
    - <img width="448" height="213" alt="Image" src="https://github.com/user-attachments/assets/e6f47ae1-08a7-4f4f-bc27-76c7074f904b" /> 
- image bench
<img width="797" height="446" alt="Image" src="https://github.com/user-attachments/assets/ee0537c7-5e01-4ff5-be20-06b91afac2b4" />
  - 다른 오픈소스는 비슷한데 MMMU가 많이 차이나는군 ㅋㅋ 
  - RealWorldQA
    - basic real-world spatial understanding capabilities of multimodal models
    - consists of 765 images, with a question and easily verifiable answer for each image. The dataset consists of anonymized images taken from vehicles
    - https://huggingface.co/datasets/nirajandhakal/realworldqa
- Ablation studies 
  - <img width="795" height="301" alt="Image" src="https://github.com/user-attachments/assets/aa604c12-bfa3-4fa6-b6ee-b3ffcf010b40" />
- Long video bench
  - <img width="784" height="556" alt="Image" src="https://github.com/user-attachments/assets/7270b2dc-68b2-47df-89e9-12bdbfd29ea8" />
 

[^1]
<img width="811" height="649" alt="Image" src="https://github.com/user-attachments/assets/fac48c1f-313f-46e4-aa83-58406eec7362" />
