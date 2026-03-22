---
title: "VinePPO: Unlocking RL Potential For LLM Reasoning Through Refined Credit Assignment"
date: 2025-02-08
tags: ['RL', 'reasoning', '2025Q1']
paper: "https://openreview.net/forum?id=5mJrGtXVwz"
issue: 222
issueUrl: "https://github.com/long8v/PTIR/issues/222"
summary: "Mentioned - similar to GRPO/RLOO, but borrowing from PPO's value network to do credit assignment."
---
<img width="578" alt="Image" src="https://github.com/user-attachments/assets/e9928169-f85b-4f34-9ab2-a146ce4ffa17" />

[paper](https://openreview.net/forum?id=5mJrGtXVwz)

## TL;DR
- **I read this because.. :** because it mentions
- **task :** RL for reasoning 
- **problem :** The value model being used in the PPO to solve credit assignment does not seem to be learning well.
- **idea :** Use MC to get value instead of value model
- **architecture :** DeepSeekMath 7B, Rho Math 1.1B
- **objective :** PPO loss -- No value network learning.
- **baseline :** PPO, DPO+, RestEM
- **data :** GSM8K, MATH
- **evaluation :** Pass@1 accuracy
- **result :** 1) Better than PPO in performance 2) Takes longer time per step but converges faster because it makes inferences in the middle (wall-clock efficiency) 3) Lower KL-divergence for the same performance (KL divergence efficiency)
- **contribution :** Similar to GRPO/RLOO, but borrowing from PPO's value network to credit assignment.
- **etc. :** Supps were well organized, so it was nice to see. iclr open review, reviewers dive in and get bored.

## Details
### intro
   - <img width="683" alt="Image" src="https://github.com/user-attachments/assets/b1e32651-d13a-4cdb-bd82-1e2b7ff47efb" />
- There are steps that are critically important and should be weighted more heavily, and there is a delay between action and reward, which is the most important problem in Rl, the credit assignment problem.
- PPOs learn value networks, but there have been studies that show that they don't learn well and act as a baseline for policy gradients, or that it's better to replace them with average rewards.
- How well is the value network learning?
- I want to get an unbiased value estimate -> VinePPO
### thumbnail
<img width="695" alt="Image" src="https://github.com/user-attachments/assets/4ddd9eb2-12e7-493b-8a71-bf6ba725f5ce" />

<img width="722" alt="Image" src="https://github.com/user-attachments/assets/caaf9c64-b570-418b-99e3-9013cf8a552a" />

### Accurate Credit Assignment with VinePPO
Keep the PPO's term [^1], but measure only the value per step in MC.
How often to step is determined by the hparm.

<img width="442" alt="Image" src="https://github.com/user-attachments/assets/0e038537-5712-410c-ac1d-237c1b3ad565" />

K is how many times to sample, but it works fine at 1 [^2].

<img width="387" alt="Image" src="https://github.com/user-attachments/assets/1cee4d59-33eb-4068-a9e9-7cad13f7a85f" />

### Result
- Step-by-step acc in VinePPO and PPO
<img width="693" alt="Image" src="https://github.com/user-attachments/assets/407c8430-7623-419a-8ccb-dd27a8a87f88" />

- acc by wallclock for VinePPOs and PPOs

<img width="711" alt="Image" src="https://github.com/user-attachments/assets/3dd4242f-ab50-4f9a-b853-18c0da4e36c5" />

vinePPO takes longer to iterate but converges faster

- acc by KL divergence

<img width="689" alt="Image" src="https://github.com/user-attachments/assets/adeedc7c-d925-4b19-bec2-3d5269bf857a" />

Why low KL divergence is good (also from https://github.com/long8v/PTIR/issues/221)
It is said that it is evaluated as good because it can be seen that the knowledge of the pretrained model is not lost and the performance is improved by utilizing the knowledge well (similar to adding a KL divergence term).

- temperature tolerance

<img width="255" alt="Image" src="https://github.com/user-attachments/assets/208fd796-d8a7-4763-8023-53ea36811da0" />

https://github.com/long8v/PTIR/issues/221 Here I increased the temperature from which the sampling trajectory is drawn to 1.2, which is usually <1 as a practice.
PPOs also have lower performance on day 1. However, this is not the case with VinePPO.

- acc in the value model

<img width="710" alt="Image" src="https://github.com/user-attachments/assets/2fe6324e-f8a1-4bc7-88b2-42500d3bef83" />

I did 256 MC to get GT value, and the horizontal axis is the predicted value, but PPO has many false positives and false negatives, and VPPO has high gt and corr.

<img width="690" alt="Image" src="https://github.com/user-attachments/assets/eaba828d-8849-428b-83fb-6c54f6437660" />

We measured the export of incorrect trajectories and found that for PPO, the longer the reasoning, the higher the error, which is explained by the fact that the initial trajectory (far left) has less diversity along the training data and therefore the value may have been memorized.


### Some details

<img width="576" alt="Image" src="https://github.com/user-attachments/assets/730a11bd-9a91-4a07-861b-508785205b29" />

End-of-Sequence (EOS) Trick: As detailed in Appendix A, rewards are only applied at the final token of a response, which corresponds to the EOS token when the response is complete. For responses that exceed the maximum length, we truncate the response to the maximum length and apply the reward to the last token of the truncated sequence

How did you do this? The generation is longer than the max length.


### footnote

[^1]: <img width="697" alt="Image" src="https://github.com/user-attachments/assets/c5b5703c-6ae4-4826-92a5-9f9432adba7a" />
[^2]: <img width="726" alt="Image" src="https://github.com/user-attachments/assets/34614eb0-a5c3-41d8-aaf3-c3d973c5a09b" />