---
title: "[180] Phantom of Latent for Large Language and Vision Models"
date: 2024-09-30
tags: ['MLLM', '2024Q3']
paper: "https://github.com/ByungKwanLee/Phantom/tree/master"
issue: 199
issueUrl: "https://github.com/long8v/PTIR/issues/199"
---
<img width="814" alt="image" src="https://github.com/user-attachments/assets/fe76c938-f583-494e-b32d-288ddc397da0">

[paper](https://github.com/ByungKwanLee/Phantom/tree/master), [code](https://github.com/ByungKwanLee/Phantom/tree/master), [dataset](https://huggingface.co/datasets/BK-Lee/Phantom)

## TL;DR
- **I read this because.. :** 최신 LVLM. 높은 성능
- **task :** LVLM
- **problem :** efficient LVLM
- **idea :** [sos] token의 representation을 사용하여 중간 dimension을 높였다가 낮춤. DPO-like한 phantom optimization 제안 
- **input/output :** image, question -> answer
- **architecture :** VE(Intern-ViT 300M), Projector MLP,  LLM(Qwen2-0.5B, InternLM2-1.8B, Phi-3-mini-3.8B, InternLM2.5-7B)
- **objective :** SFT loss + SimPO
- **baseline :** closed and open LVLM models 
- **data :** ShareGPT4o-Images(57K), ShareGPT4V(755K), ALLaVA-VFLAN/Text(548K), MiniGemini(DocVQA, ChartQA, DVQA, AI2D), Science and Mathematical Reasoning([SMR](https://huggingface.co/datasets/yifanzhang114/SMR?row=50) -- Arxiv-QA,  TextBookQA), GLLaVA, MathVision, [MathInstruct](https://huggingface.co/datasets/TIGER-Lab/MathInstruct), [MathPlus](https://huggingface.co/datasets/TIGER-Lab/MATH-plus)
- **evaluation :** Science QA, AI2D, ChartQA, SEED, POPE, HallB, MME, MathVista, MMB, MM-Vet, LLaVA-w
- **result :** 비슷한 스케일의 모델 중에 좋은 성능 
- **contribution :**
- **etc. :**

## Details
### proposed
- Phantom Dimension
<img width="768" alt="image" src="https://github.com/user-attachments/assets/8ccab835-d4c7-413f-a954-a5cb578f3fcd">


- Phantom Optimization 
<img width="631" alt="image" src="https://github.com/user-attachments/assets/a7780e93-5c30-4ae3-b07e-8c45353ba405">

SimplePO objective와 아예 같은듯?

<img width="493" alt="image" src="https://github.com/user-attachments/assets/9118aef2-9df7-435e-998d-e8a8ac243d3f">


{question, chosen, rejected} triplet은 GPT4o-mini로 생성 뒤 GPT4-o로 validate
e.g. 
<img width="504" alt="image" src="https://github.com/user-attachments/assets/a975a113-c1f8-4ac7-8262-3863c880f984">

<img width="760" alt="image" src="https://github.com/user-attachments/assets/f689993c-d7b8-4cca-ac20-736fd89590c8">



### result
<img width="767" alt="image" src="https://github.com/user-attachments/assets/7a0caa1f-5062-4c74-b8dc-84c110b4f7a5">

<img width="762" alt="image" src="https://github.com/user-attachments/assets/5fe501b8-8b84-4f71-8775-cebf9392ee0f">

ChartQA, 

### data links 
https://github.com/ByungKwanLee/Phantom/tree/master?tab=readme-ov-file#-download-training-datasets
- ShareGPT4V [[link](https://github.com/InternLM/InternLM-XComposer/blob/main/projects/ShareGPT4V/docs/Data.md)]
- ALLAVA4V-VFLAN[[link](https://huggingface.co/datasets/Vision-Flan/vision-flan_191-task_1k/tree/main)]
- ALLAVA4V-Text [[link](https://huggingface.co/datasets/FreedomIntelligence/ALLaVA-4V/viewer/allava_text)]
- MiniGemini [[link](https://github.com/dvlab-research/MiniGemini)]
- SMR [[link](https://huggingface.co/datasets/yifanzhang114/SMR)]
- DocDownstream [[link](https://huggingface.co/datasets/mPLUG/DocDownstream-1.0)]
- DocReason [[link](https://huggingface.co/datasets/mPLUG/DocReason25K)]
- GLLaVA [[link](https://huggingface.co/datasets/Luckyjhg/Geo170K)]
- MathVision [[link](https://huggingface.co/datasets/mathvision/mathvision)]
- MathInstruct [[link](https://huggingface.co/datasets/TIGER-Lab/MathInstruct)]
- MathPlus [[link](https://huggingface.co/datasets/TIGER-Lab/MATH-plus)]
