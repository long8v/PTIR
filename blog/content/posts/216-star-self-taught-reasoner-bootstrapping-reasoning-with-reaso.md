---
title: "STaR: Self-Taught Reasoner Bootstrapping Reasoning With Reasoning"
date: 2025-01-09
tags: ['2022Q1', 'google', '25min', 'reasoning']
paper: "https://arxiv.org/abs/2203.14465"
issue: 216
issueUrl: "https://github.com/long8v/PTIR/issues/216"
summary: "The star of Q* is this and so on and so forth - self-improvement? self-evolution? emphasizing rationale?"
---

<img width="1196" alt="image" src="https://github.com/user-attachments/assets/fd8c2a2e-a15e-4ea7-b8df-c5080cb54d01" />

[paper](https://arxiv.org/abs/2203.14465)

## TL;DR
- **I read this because.. :** q*'s star is this and so on and so forth.
- **task :** problem solving
- **PROBLEM :** Wouldn't the model perform better if we learned the rationale?
- **idea :** Let the model generate a rationale, since heuristics can only go so far. If it can't, hint at the correct answer.
- **input/output :** Q -> rationale - A
- **architecture :** GPT-J
- **objective :** CE loss 
- **baseline :** direct answer tuned GPT-J, Few-shot GPT-J, Few-shot LaMDA 137B
- **data :** (source) GSM, CommonsenceQA, arithmetic problem 
- **evaluation :** accuracy
- Result :** Accuracy improves faster. Solve problems you couldn't solve (final accuracy increases).
- **contribution :** self-improvement? self-evolution? emphasize rationale?
- **etc. :**

## Details
### STaR
 
<img width="1134" alt="image" src="https://github.com/user-attachments/assets/5d900a1a-dcf2-4b61-b854-80bda068e446" />

<img width="1076" alt="image" src="https://github.com/user-attachments/assets/68e0c73d-cc27-4218-bb86-82cc6fb1cbcd" />

The details are 1) hinting only for questions that are not answered correctly 2) model finetuning is done in the base model, not iteratively. Is the rationale getting better and better as we go along? It seems like this is a little different from other models...

Claim that the process of filtering for incorrect rationales is similar to RL objectvie

<img width="1034" alt="image" src="https://github.com/user-attachments/assets/df3346be-7712-4521-9dd7-1b47c2f9b733" />


### Result
<img width="1121" alt="image" src="https://github.com/user-attachments/assets/bf6fd52e-560d-4671-8d63-e578fb219f32" />

color is the number of digits problem

<img width="524" alt="image" src="https://github.com/user-attachments/assets/d852e10f-295c-4be2-a74e-ddf387a21a23" />

Ability to solve for digits you've never seen before

<img width="1066" alt="image" src="https://github.com/user-attachments/assets/4658b20a-b089-4c0e-bbdd-113455bf9319" />

<img width="1123" alt="image" src="https://github.com/user-attachments/assets/4d3e2a38-a8b5-4e0d-bf93-a9357816d831" />


