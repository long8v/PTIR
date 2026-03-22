---
title: "[215] Group Sequence Policy Optimization"
date: 2025-08-01
tags: ['LLM', 'RL', '2025Q3']
paper: "https://arxiv.org/abs/2507.18071v2"
issue: 236
issueUrl: "https://github.com/long8v/PTIR/issues/236"
summary: "Viral as a GRPO alternative"
---
<img width="1058" height="278" alt="Image" src="https://github.com/user-attachments/assets/ad1ad42b-ff14-4afb-ad76-27a5b9ddba10" />

[paper](https://arxiv.org/abs/2507.18071v2)

## TL;DR
- **I read this because:** It came out as a GRPO alternative and was viral.
- **Task:** large reasoning model 
- **Problem:** Training instability and model collapse due to per-token importance ratio in the existing GRPO algorithm.
- **Idea:** Use per-sequence rather than per-token importance ratio for reliable RL training
- **Input/Output:** query ->  {reasoning, answer}
- **Architecture:** Qwen3-30B-A3B-Base
- **Objective:** GSPO(proposed)
- **Baseline:** GRPO
- **Data:** RL training on math (AIME'24), coding (LiveCodeBench, CodeForces) tasks
- **Evaluation:** Training stability, efficiency metrics, downstream task performance
- **Result:** Superior training stability, efficiency, stabilized MoE models, and significantly improved Qwen3 model performance
- **Contribution:** Stabilizes RL training with sequence-wise importance sampling, simplifies MoE RL training
- **Etc:** Developed by Alibaba Qwen team, applied to real Qwen3 models to achieve performance improvements

## Details

### Problem Analysis
- GRPO 

<img width="646" height="169" alt="Image" src="https://github.com/user-attachments/assets/7b5520fc-650f-44e0-9362-23ff8455ae00" />

where $w_{i,t}$ corrects for this probability because we did not sample from the original distribution, $\pi_{tar}$, in the form
For normal importance sampling, it is common to let N be greater than 1 and give the mean.

<img width="274" height="41" alt="Image" src="https://github.com/user-attachments/assets/925e7908-4527-4268-98ed-3df9f42a8af7" />

However, in GRPO, we only get the next token probability 1) from a single sample 2) (not the entire probability distribution), which makes the model very sensitive to noise.
Also, as this noise accumulates in long sequences, the noise gets louder, making it harder to reverse once it converges incorrectly and very sensitive to hparams (clipping hparam, rl prompt, .. etc).
There is also a mismatch where the reward comes for one sequence but the optimization objective comes per token.

### GSPO Algorithm

<img width="1314" height="431" alt="Image" src="https://github.com/user-attachments/assets/043f9042-2e43-4ec3-a926-af48d6a3e163" />

- Determine clipping for the entire sequence, not per token
- Apply equal weight to all tokens
- Divide $s_i$ by the length of $|y_i|$ and length normalize (to get a similar clip range regardless of length)

gradient

<img width="1297" height="323" alt="Image" src="https://github.com/user-attachments/assets/81ffa8dc-fd1d-4a77-8c1c-518266807460" />

<img width="1327" height="262" alt="Image" src="https://github.com/user-attachments/assets/458c75da-c5a9-4f24-ad25-eb528c44603b" />

### Experimental Results
**Training Efficiency**:

<img width="855" height="520" alt="Image" src="https://github.com/user-attachments/assets/9dcabfcc-9154-4cf1-8aaf-acf1a88e4b53" />

- Achieve higher training rewards compared to GRPO
- Better performance for the same amount of computation
- More stable convergence curves
- Better bench performance on AIME'24, LiveCodeBench, and CodeForces

**Clipping Analysis**:

<img width="576" height="197" alt="Image" src="https://github.com/user-attachments/assets/9f880325-aa9e-4c66-bb90-9c823d52e9cb" />

- GSPO: 15% token clipping
- GRPO: 0.13% token clipping
- Paradoxically, more clipping leads to better performance

### MoE Training Benefits
When training MoE-Qwen3 with GRPO, it tended to be unstable because the experts activated in the previous policy and the experts activated in the current policy were different, resulting in much higher variability in the importance ratio.
To solve this, we cache the active expert for $\pi _{old}$ and do a trick to make sure that $\pi$ and $\pi _{old}$ have the same expert.

<img width="1041" height="405" alt="Image" src="https://github.com/user-attachments/assets/bb165550-2bc9-460d-9091-889a33ba9245" />

<img width="1041" height="334" alt="Image" src="https://github.com/user-attachments/assets/2582acc5-c98e-4930-bc0a-e4fd3222acb0" />

GSPO was better than that. The resulting complexity is lower.

### Benefit of GSPO for RL Infrastructure
Should have recalculated likelihood for old policy due to precision issue while using sglang, vllm for rollout and megatron for training engine. (old policy is not a target for updating, so it shouldn't have been necessary in the first place)
However, compared to token-level likelihood, sequence-level likelihood is not as sensitive to precision and does not require recalculation.
This makes it slightly more efficient in partial rollout and multi-turn RL and in the training-inference disaggregated frameworks situation

c.f. DAPO
It's different because it's about normalize

<img width="655" height="139" alt="Image" src="https://github.com/user-attachments/assets/97efd436-977d-4e40-9c42-1c0c94ce9168" />