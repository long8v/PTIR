---
title: "[204] DeepScaleR: Surpassing O1-Preview with a 1.5B Model by Scaling RL"
date: 2025-02-19
tags: ['25min', 'RL', 'reasoning', '2025Q1']
paper: ""
issue: 225
issueUrl: "https://github.com/long8v/PTIR/issues/225"
---
<img width="727" alt="Image" src="https://github.com/user-attachments/assets/a1b0a1d1-def0-4ce9-9bd1-ee013a2bc71e" />

[technical report](https://pretty-radio-b75.notion.site/DeepScaleR-Surpassing-O1-Preview-with-a-1-5B-Model-by-Scaling-RL-19681902c1468005bed8ca303013a4e2)

## TL;DR
- **I read this because.. :** 언급되어.
- **task :** math in llm 
- **problem :** 저렴하게 o1 replicate. 
- **idea :** 이미 distil된 qwen 사용, small model로 시도, context를 점차 늘려나가는 시도 
- **input/output :** question, answer
- **architecture :** DeepSeek-R1-Distill-Qwen-1.5B
- **objective :** GRPO
- **baseline :** DeepSeek-R1-Distill-Qwen-1.5B, rStar-Math-7B, o1-preview, ... 
- **data :** AIME, AMC, Omni-Math, Still
- **evaluation :** AIME2024, AMC2023, MATH-500, Minereva Math, Olympiad batch
- **result :** minerva math를 빼고 sota. aime, math에 대해서 o1-preview를 이기기도 
- **contribution :** context length를 점차 늘리는 트릭.
- **etc. :**

## Details
- thumbnail

<img width="746" alt="Image" src="https://github.com/user-attachments/assets/c700f432-8f8e-494b-b7f5-f08c45788b3e" />

### dataset curation 
  - source: AIME, AMC, Omni-Math, Still
  - gemini-1.5-pro-002로 풀이과정에서 answer 추출
  - `sentence-transformers/all-MiniLM-L6-v2` 사용해서 중복 질문 제거
  - `sympy`로 해결할 수 없는 문제는 filtering. llm judge 사용해야하는 다볍은 학습을 느리게 하고 noisy signal을 줄 수 있음.

### reward
 - 1: latext/sympy check ok
 - 0: if no formatted(`/think`), or answer is not correct.

### Iterative Context Lengthening: Think Shorter, then Longer
- First, we perform RL training with 8K max context for more effective reasoning and efficient training.
  - 이에 대한 직관은 Deepseek-R1-Distilled-Qwen-1.5B로 AIME을 풀어봤을 때 incorrect response가 correct response보다 3배나 답변길이가 긴 현상이 있었음. 즉 그냥 길게 학습하는건 대부분의 토큰이 낭비가 되고, 이 길어진 response에 대해서는 repetitive pattern이 보였기 때문임.
  - 이때 성능이 개선되고 이에 따라 answer response의 길이는 5,500에서 3,500으로 떨어짐
  - <img width="738" alt="Image" src="https://github.com/user-attachments/assets/fe7b689e-788b-4b50-90b2-cc998c616132" />
  - <img width="615" alt="Image" src="https://github.com/user-attachments/assets/ff5cc022-27f8-44cc-a5c2-849e7ed62f81" />
- Next, we scale up training to 16K and 24K contexts so that the model can solve more challenging, previously unsolved problems.
  - 8K를 학습하다가 갑자기 response length가 늘어나는 구간이 있음. 이는 context limit을 떨어뜨려 truncate되어 return을 떨어뜨리는 현상.
  - <img width="763" alt="Image" src="https://github.com/user-attachments/assets/c0bef471-8ea3-4fbf-99ad-9b2d06035dc8" />
  - 이제 think longer를 하는 현상이 있어서 context window를 16K로 늘려서 학습 
  - 500 step 학습 후 24K로 늘리고 학습

### evaluation

<img width="775" alt="Image" src="https://github.com/user-attachments/assets/9db0abf8-278d-414c-a7e2-ce987528b801" />

<img width="570" alt="Image" src="https://github.com/user-attachments/assets/43f3ec0e-e616-4b5d-b103-57dd6da5269d" />