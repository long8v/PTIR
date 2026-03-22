---
title: "[172] RLHF-V: Towards Trustworthy MLLMs via Behavior Alignment from Fine-grained Correctional Human Feedback"
date: 2024-08-30
tags: ['CVPR', 'RL', 'MLLM', '2024Q2']
paper: "https://arxiv.org/abs/2312.00849"
issue: 191
issueUrl: "https://github.com/long8v/PTIR/issues/191"
---
<img width="702" alt="image" src="https://github.com/user-attachments/assets/1331c895-4427-4f7f-baa9-e619afc49d33">

[paper](https://arxiv.org/abs/2312.00849), [data](https://huggingface.co/datasets/openbmb/RLHF-V-Dataset?row=0), [code](https://github.com/RLHF-V)

## TL;DR
- **I read this because.. :** VLM + RLHF
- **task :** MLLM
- **problem :** MLLM의 hallucination 문제. GPT4-V의 경우에도 45.9%가 hallucination이더라 
- **idea :** DPO 학습을 하자. 그런데 이때 정확하게 어떤 segment가 틀렸는지를 정답을 매기자.
- **input/output :** {image, question} -> answer
- **architecture :** 저자들의 전작인 [Muffin](https://arxiv.org/abs/2310.00653). BEiT-3 + 13B Vicnuna 1.0 기반의 모델 
- **objective :** 살짝 수정된 DPO. DPO loss term에 들어가는 log-propb 부분 가중치가 조금 달라짐. 
- **baseline :** QwenVL-Chat, LLaVA, LLaVA1.5, Muffin, InstructBLIP, LLaVA-RLHF
- **data :** human annotated 1.4K data 
- **evaluation :** Object HalBench, MMHAL-Bench, MHumanEval, LLaVA Bench, VQAv2
- **result :** hallucination 관점에서 open model 중 sota.(일부 GPT4V를 이기도 함). LLAVA Bench의 경우 LLavA-RLHF가 좀더 좋긴 하지만 비등비등하게 좋음. 
- **contribution :** 효율적인 DPO 학습. 데이터 공개 
- **etc. :**

## Details
### overall
<img width="879" alt="image" src="https://github.com/user-attachments/assets/c6c28612-1726-4d48-a574-ca80ab0da125">

### underlying challenges in human preference data
1) ambiguity 
두 답변이 있을 때 각각의 장점, 단점이 있는데 둘중에 무엇을 선호하게 할지가 문제
2) learning efficiency 
reponse하나로 긴 답변에 대해 feedback을 해야하기 때문에 학습하기 어려워서 많은 데이터를 필요로 하고, 이러한 credit misallocation 문제로 reward hacking 등의 문제가 생김 

### fine-grained correctional human preference collection
segment level로 human annotation 시킴. hallucinated segments를 정정하는 방식. 정정 전/후가 $y_w$, $y_l$이 됨. 
이때 데이터는 instruction data 소스에서 image description prompt를 GPT4로 만들고(?) answer는 muffin을 통해 받음(??)

이렇게 만들어진 데이터 통계는 64.4 단어의 2.65 corrected segments. 
hallucination type은 objects(41.2%), positions(20.3%), numbers(16.5%), attributes(10.0%), actions(5.3%), misc 가 있었음

### Dense Direct Preference Optimization
- DPO loss recap
<img width="401" alt="image" src="https://github.com/user-attachments/assets/0819f53a-51f5-4de3-8b23-f8a9ecc80387">

($\beta$ 0.5)

여기서 log-prob 부분에서 corrected segment($y_c$)에 속하는지 아닌지(unchanged, $y_u$)에 따라 가중을 두자고 하는게 proposed DDPO

<img width="547" alt="image" src="https://github.com/user-attachments/assets/76ea3796-7eab-40bf-9cd6-2c00ff38eb94">

- $\gamma$ : 5 
- $N$: len($y_u$) + $\gamma$ len($y_c$)
  - 1/N은 길어지는 longer response에 대한 선호를 통제하기 위해 있음

### Result 

<img width="1216" alt="image" src="https://github.com/user-attachments/assets/5d949e13-5ac8-4aae-99c5-7667028314d2">

<img width="1091" alt="image" src="https://github.com/user-attachments/assets/3293996f-58c5-4822-bef8-4b8d44b792c3">

<img width="800" alt="image" src="https://github.com/user-attachments/assets/69589a46-f611-4ed8-bae0-1e3e5ae05d45">

<img width="500" alt="image" src="https://github.com/user-attachments/assets/a0083a42-3e45-41db-b520-06d2016843ee">

<img width="500" alt="image" src="https://github.com/user-attachments/assets/35b8e49b-35cd-47fc-87ac-feb4585ba527">


#### Ablations
<img width="607" alt="image" src="https://github.com/user-attachments/assets/44383afc-8028-44b5-9b08-683347eb394f">

<img width="400" alt="image" src="https://github.com/user-attachments/assets/fde462be-8c6c-4037-aa50-39b6ef05ee54">

