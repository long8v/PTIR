---
title: "DeepScaleR: Surpassing O1-Preview with a 1.5B Model by Scaling RL"
date: 2025-02-19
tags: ['25min', 'RL', 'reasoning', '2025Q1']
paper: ""
issue: 225
issueUrl: "https://github.com/long8v/PTIR/issues/225"
summary: "Mentioned. - A trick to gradually increase the context length."
---
<img width="727" alt="Image" src="https://github.com/user-attachments/assets/a1b0a1d1-def0-4ce9-9bd1-ee013a2bc71e" />

[technical report](https://pretty-radio-b75.notion.site/DeepScaleR-Surpassing-O1-Preview-with-a-1-5B-Model-by-Scaling-RL-19681902c1468005bed8ca303013a4e2)

## TL;DR
- **I read this because.. :** was mentioned.
- **task :** math in llm 
- **problem :** cheap o1 replicate.
- **idea :** use qwen already distil, try with small model, gradually increase context
- **input/output :** question, answer
- **architecture :** DeepSeek-R1-Distill-Qwen-1.5B
- **objective :** GRPO
- **baseline :** DeepSeek-R1-Distill-Qwen-1.5B, rStar-Math-7B, o1-preview, ... 
- **data :** AIME, AMC, Omni-Math, Still
- **evaluation :** AIME2024, AMC2023, MATH-500, Minereva Math, Olympiad batch
- **result :** minerva math minus sota. aime, also beats o1-preview for math
- Trick to gradually increase the **contribution :** context length.
- **etc. :**

## Details
- thumbnail

<img width="746" alt="Image" src="https://github.com/user-attachments/assets/c700f432-8f8e-494b-b7f5-f08c45788b3e" />

### dataset curation 
  - source: AIME, AMC, Omni-Math, Still
- Extracting the answer from the solution with gemini-1.5-pro-002
- Use `sentence-transformers/all-MiniLM-L6-v2` to remove duplicate questions
- Problems that can't be solved with `sympy` are filtered. llm judge The many layers that must be used can slow down learning and give a noisy signal.

### reward
 - 1: latext/sympy check ok
 - 0: if no formatted(`/think`), or answer is not correct.

### Iterative Context Lengthening: Think Shorter, then Longer
- First, we perform RL training with 8K max context for more effective reasoning and efficient training.
- Our intuition for this was that when we solved AIME with Deepseek-R1-Distilled-Qwen-1.5B, incorrect responses were three times longer than correct responses, meaning that just learning longer responses would waste most of the tokens, and we saw a repetitive pattern for these longer responses.
- This improves performance and the length of the answer response drops from 5,500 to 3,500
  - <img width="738" alt="Image" src="https://github.com/user-attachments/assets/fe7b689e-788b-4b50-90b2-cc998c616132" />
  - <img width="615" alt="Image" src="https://github.com/user-attachments/assets/ff5cc022-27f8-44cc-a5c2-849e7ed62f81" />
- Next, we scale up training to 16K and 24K contexts so that the model can solve more challenging, previously unsolved problems.
- While learning 8K, there is a sudden increase in response length. This is due to dropping the context limit, which is truncated and causes the return to drop.
  - <img width="763" alt="Image" src="https://github.com/user-attachments/assets/c0bef471-8ea3-4fbf-99ad-9b2d06035dc8" />
- Now I'm thinking longer, so I've increased the context window to 16K, so I'm using the Learning
- Learn 500 steps, then increase to 24K and learn

### evaluation

<img width="775" alt="Image" src="https://github.com/user-attachments/assets/9db0abf8-278d-414c-a7e2-ce987528b801" />

<img width="570" alt="Image" src="https://github.com/user-attachments/assets/43f3ec0e-e616-4b5d-b103-57dd6da5269d" />