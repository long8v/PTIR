---
title: "[221] Scaling Synthetic Data Creation with 1,000,000,000 Personas"
date: 2026-01-19
tags: ['dataset', 'LLM', '2024Q3']
paper: "http://arxiv.org/abs/2406.20094"
issue: 242
issueUrl: "https://github.com/long8v/PTIR/issues/242"
---
<img width="957" height="318" alt="Image" src="https://github.com/user-attachments/assets/b026f59f-393a-4e87-847f-16019c0923ef" />

[paper](http://arxiv.org/abs/2406.20094), [dataset](https://huggingface.co/datasets/proj-persona/PersonaHub/viewer/knowledge?row=4)

## TL;DR
- **I read this because.. :** data synthesis
- **task :** data synthesis, augmentation
- **problem :** more diverse data synthesis 
- **idea :** corpus-to-persona, persona-to-instruction data or person-to-text corpus
- **input/output :** corpus -> persona -> instruction data or personalized corpus
- **architecture :**  Qwen2-7B
- **objective :** ce loss 
- **baseline :** sota LLMs
- **data :** 200K persona hub, 150K problems (proposed)
- **evaluation :** held-out test set, MATH
- **result :** robust on MATH
- **contribution :**
- **etc. :**

## Details

<img width="907" height="513" alt="Image" src="https://github.com/user-attachments/assets/f75d0ec8-f3dd-4507-8175-43cdc91e574d" />

<img width="920" height="416" alt="Image" src="https://github.com/user-attachments/assets/e3842a37-0c68-418c-95da-e1d3e7e62b4e" />

<img width="926" height="425" alt="Image" src="https://github.com/user-attachments/assets/bf177404-60c5-4db9-b560-cc63a82161e5" />

<img width="880" height="440" alt="Image" src="https://github.com/user-attachments/assets/454e455c-6fd5-4871-8cf9-5e2d92c86b8a" />

<img width="935" height="399" alt="Image" src="https://github.com/user-attachments/assets/00adbd7f-878e-469b-92b3-65bf1db2ca89" />

<img width="837" height="904" alt="Image" src="https://github.com/user-attachments/assets/64a4ef6b-7e0c-463a-99cf-0fca7705fc64" />

<img width="737" height="475" alt="Image" src="https://github.com/user-attachments/assets/6b3c1b6c-ec80-4c81-b415-bb0e1715593b" />

### result 
<img width="790" height="415" alt="Image" src="https://github.com/user-attachments/assets/565fcfc4-46f7-469a-abcf-5ff9ccb5caa0" />

<img width="830" height="467" alt="Image" src="https://github.com/user-attachments/assets/d6486649-669a-496d-b205-8a2343f9380e" />

<img width="425" height="401" alt="Image" src="https://github.com/user-attachments/assets/d7ad268a-3c79-4abe-bd6c-2fa6454f1747" />