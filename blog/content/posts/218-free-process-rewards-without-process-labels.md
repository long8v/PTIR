---
title: "Free Process Rewards without Process Labels"
date: 2025-01-20
tags: ['25min', 'RL', '2024Q4']
paper: "https://arxiv.org/abs/2412.01981"
issue: 218
issueUrl: "https://github.com/long8v/PTIR/issues/218"
summary: "Prior knowledge before reading the paper PRIME. I'm interested in implicit dense reward because of my previous research lol - DPO is secretly... If Q-learning paper was limited to DPO, this can be applied to most loss terms."
---
<img width="655" alt="Image" src="https://github.com/user-attachments/assets/d1555c68-789b-47a9-885d-b8db3a98135e" />

[paper](https://arxiv.org/abs/2412.01981)

## TL;DR
- **I read this because.. :** Prior knowledge before reading the paper called PRIME. Interested in implicit dense reward because of previous research lol
- **task :** reward modeling 
- Problem :** PRM performs better but is too expensive compared to ORM
- **idea :** Can't we just learn ORMs and get sparse rewards like PRMs?
- **input/output :** prompt, y -> reward of y_t 
- **architecture :** Llama-3.1-8B-Instruct 
- **objective :** Put $\frac{\pi_\theta(y_i|y_{<i})}{\pi_{ref}(y_i|y_{<i})}$ where all q's go. dpo, kto, nca, ce
- **baseline :** MathShepherd, AutoPSV, RLHFlow, open ORM/ PRM models
- **data :** UltraInteract -- 8 rollouts per instruction from Llama-3.1-8B-instruct 
- **evaluation :** Math-500 BoN / Mistral-Instruct-v0.3, Llama-3.1-8B-Instruct, Llama-3.1-70B-Instruct
- **result :** Better performance than Math-Shepherd, AutoPSV.
- **contribution :** DPO is secretly... If the Q-learning thesis was limited to DPO, this can be applied to most loss terms.
- **etc. :**

## Details
- Letting advantage r be the ratio to reference ensures that q is exactly the exponential average of $r_\theta$ at step t
<img width="556" alt="Image" src="https://github.com/user-attachments/assets/3b05f1ea-739b-4b5c-9bb1-fc12ea8b1401" />

<img width="296" alt="Image" src="https://github.com/user-attachments/assets/af04e0dc-4158-42ba-bb6b-8ee44682a5d8" />

This means that when learning an ORM, if we give r like that, the $y_t$ for each step will be Q, like in PRM, so we can use this as a sparse reward

- second proposition

<img width="358" alt="Image" src="https://github.com/user-attachments/assets/286201f3-7bd5-4dcd-bbd6-edd8371a9d16" />

Does not understand he

- This also applies to CE loss

<img width="467" alt="Image" src="https://github.com/user-attachments/assets/0bb153de-1d92-4b21-af46-af516a95baca" />

- result


<img width="571" alt="Image" src="https://github.com/user-attachments/assets/aacbc6e8-892f-49cd-b160-4c28a84fe6df" />


- efficiancy

<img width="575" alt="Image" src="https://github.com/user-attachments/assets/ae1189c7-8087-4d3c-9673-ba6e20691fa6" />


- with majority vote

<img width="281" alt="Image" src="https://github.com/user-attachments/assets/08c891b1-ed03-4b52-a7e9-ed1b8439a9bd" />


c.f. UltraInteract
Math
<img width="553" alt="Image" src="https://github.com/user-attachments/assets/adf4da5f-4239-41f8-8db2-47e1b0b2617b" />
