---
title: "Smaug: Fixing Failure Modes of Preference Optimisation with DPO-Positive"
date: 2024-09-05
tags: ['LLM', 'RL', '2024Q1']
paper: "https://arxiv.org/pdf/2402.13228"
issue: 195
issueUrl: "https://github.com/long8v/PTIR/issues/195"
summary: "I wonder if it's dense RLHF related - it's intuitively easy to understand what's going on and the solution is intuitive."
---
<img width="663" alt="image" src="https://github.com/user-attachments/assets/ada18676-8bca-4f04-9698-13dbb6b3eb89">

[paper](https://arxiv.org/pdf/2402.13228), [code](https://github.com/abacusai/smaug)

## TL;DR
- **I read this because.. :** I wondered if it was dense RLHF related.
- **task :** RLHF
- **problem :** DPO adds a loss to the relative log prob, so for pairs with small edit distances, we observe that the log prob is lower even for those that are not wrong.
- **IDEA:** Add a penalty to prevent the log prob for the preferred answer from getting too low.
- **input/output :** query -> answer
- **architecture :** Llama-2-7B-Chat, Bagel-34B-v0.2, MoMo-72b-lora-1.8.7-DPO
- **objective :** proposed DPOP loss(DPO loss + $\max\left(0, \log \frac{\pi_{\text{ref}}(y_w|x)}{\pi_{\theta}(y_w|x)}\right)$ )
- **baseline :** DPO, IPO, SLiC
- **data :** GSM8K, MetaMath, ARC, and Hellaswag were recreated by deliberately creating incorrect pairs.
- **evaluation :** GSM8K / ARC / Hellaswag test split 
- **result :** Better performance than baseline on both low and high edit distance datasets.
- **contribution :** It's intuitively easy to understand what's going on and how to fix it.
- **etc. :** It had nothing to do with dense RLHF, but it does...?!

## Details
### motivation
<img width="511" alt="image" src="https://github.com/user-attachments/assets/e5803e03-078c-4d3e-be9a-def613e58b2c">

DPO's loss is the same as above
The problem the authors emphasize here is that the loss depends only on the relative log prob. (expressed as $\pi_{ratio}$ in the paper)
This relative ratio only needs to be higher for preferred to be higher than dispreferred, so $\pi_{ratio}(y_w)$ can still be lower for $y_w$.
The only time this becomes an issue is when you DPO on a pair with a small edit distance.

<img width="682" alt="image" src="https://github.com/user-attachments/assets/e51277fd-8a8f-411c-968c-8f57fbf77646">

When we get the Gradient for DPO loss, it looks like this
<img width="375" alt="image" src="https://github.com/user-attachments/assets/f05c59ed-5d9d-4927-87bb-59e14f9ccb11">

For simplicity, let's assume that $y_w$, $y_l$ are different for the first token only, then the gradient for the subsequent tokens $k$ will be
<img width="379" alt="image" src="https://github.com/user-attachments/assets/59dede43-4750-4685-b86f-fc57768fb730">

- s_j^{x}$ is the probability of predicting the jth token given x

Since we usually start the DPO at the weight where the SFT is complete, the log prob is bound to be low for tokens that come after the false token.
The later tokens will then have a loss due to the difference in log prob between the two, even though they are in fact correct.
This means that the probability distribution is corrected for incorrect tokens, but unnecessarily lowers log prob for subsequent correct tokens.

### Propose DPOP

<img width="633" alt="image" src="https://github.com/user-attachments/assets/ed9f19e5-7d0d-4fb2-b8d1-b586b97c7d1a">

Add a penalty term. to avoid going lower than $\pi_{ref}$ for the preferred answer.

### Result

<img width="681" alt="image" src="https://github.com/user-attachments/assets/305a4736-bd61-4803-952d-11f91222a023">

<img width="680" alt="image" src="https://github.com/user-attachments/assets/afcd6923-1c97-4327-b6c0-bafe17948333">
