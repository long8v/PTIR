---
title: "[209] SFT Memorizes, RL Generalizes: A Comparative Study of Foundation Model Post-training"
date: 2025-05-21
tags: ['google', 'RL', 'Berkley', '2025Q1']
paper: "https://arxiv.org/pdf/2501.17161#page=11&zoom=100,384,536"
issue: 230
issueUrl: "https://github.com/long8v/PTIR/issues/230"
summary: "Is it bad to do too much SFT? + [RL4VLM](https://rl4vlm.github.io/) Author's follow-up study - systematically breaking down tasks into not-too-complex, easy-to-understand tasks"
---
![Image](https://github.com/user-attachments/assets/97d87cd8-6221-49f5-8ffb-661d4b02f324)

[paper](https://arxiv.org/pdf/2501.17161#page=11&zoom=100,384,536), [page](https://tianzhechu.com/SFTvsRL/)

## TL;DR
- **I read this because.. :** Is it bad to do too much SFT? + [RL4VLM](https://rl4vlm.github.io/) author follow-up study
- **task :** card game(GeneralPoints), real-world navigation([V-IRL](https://virl-platform.github.io/))
- Problem :** Analysis of the data memorization phenomenon of SFT vs RL
- Idea :** Create an out-of-distribution with a small change in rules or environment and analyze how performance changes.
- **input/output :** {prompt, (image), previous prediction and result..} -> verifier output 
- **architecture :** Llama-3.2-Vision-11B
- **objective :** SFT loss -> PPO loss
- **baseline :** base model, (V-IRL) chatgpt, claude..
- **data :** (SFT) Looks like expert data exists
- **evaluation :** success rate
- **result :** 1) in-domian is SFT > RL. SFT has worse OOD, but RL is maintained or improved 2) SFT should be for instruction following 3) putting it in sequential revision affects performance 4) V-IRL achieves sota
- **contribution :** Systematically broken down into tasks that are not too complex and easy to understand.
- **etc. :** Thanks for doing VLM too ðŸ™'

## Details
- thumbnail

<img width="367" alt="Image" src="https://github.com/user-attachments/assets/90c52132-e5d0-4a98-bb43-9b4cf46c910f" />

### task 
- GeneralPoints (a game that uses 4 cards to make 24 through the arithmetic operation) : LLM / VLM
    - <img width="728" alt="Image" src="https://github.com/user-attachments/assets/1b64f17f-d303-4c90-b9b6-3a2fcf390ccc" />
    - OOD 
- Viewing Q,K,V as 10 vs 11,12,13
- Sampling from black cards / sampling from red cards
  - V-IRL
    -  <img width="691" alt="Image" src="https://github.com/user-attachments/assets/41b83f25-3308-49ae-9572-c1d3ff4e5d80" />
- The task of navigating around a city
    - OOD : 
- The action changes to Turn left, etc.
- Replace city
   
- sequential revision input
<img width="688" alt="Image" src="https://github.com/user-attachments/assets/350f21c7-bf84-4830-abf4-43b5a94bb74d" />

### training
  - SFT -> RL
- RL is a PPO
- No reasoning, just a straightforward return of the correct answer
- verifier appears to be rule-based
    - <img width="325" alt="Image" src="https://github.com/user-attachments/assets/34c868b9-3c89-4148-ad79-7cb280457197" />

### result 
- ood performance 
<img width="696" alt="Image" src="https://github.com/user-attachments/assets/43cfedf0-c844-442e-8731-cc09c7671af7" />

As learning progresses, OOD performance increases from RL > SFT
SFT deteriorates significantly with nothing maintained

<img width="665" alt="Image" src="https://github.com/user-attachments/assets/610fb8c1-86e8-4862-ab29-aba522a1119b" />

- result for visual OOD

<img width="671" alt="Image" src="https://github.com/user-attachments/assets/36797866-f6dc-48f8-af05-48a56d823884" />


- SFT is necessary for RL training when the backbone model does not follow instructions.
<img width="337" alt="Image" src="https://github.com/user-attachments/assets/1b27663d-7b5d-4322-ae5d-5a0376d39f40" />

- Scaling up verification improves generalization.

<img width="330" alt="Image" src="https://github.com/user-attachments/assets/d5eec6f2-dc95-43d5-bbe3-b61204c21844" />

+2.15% (3 steps), +2.99% (5 steps), +5.99% (10 steps).
<->  one verification step, we only observe a marginal improvement of +0.48% in OOD performance improvement.