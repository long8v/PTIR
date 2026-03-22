---
title: "[214] Learning to Model the World With Language"
date: 2025-07-17
tags: ['ICML', 'RL', '2023Q3', 'WORLD-MODEL']
paper: "https://arxiv.org/pdf/2308.01399"
issue: 235
issueUrl: "https://github.com/long8v/PTIR/issues/235"
summary: "Came across this while searching for agent + VLM. I'm interested in gaming rl. ICML'24 oral - Effective world model learning for streaming incoming information (single \"text\" modality pretraining seems to be the most contribution?) -- learning with world model + actor-critic seems to be a contribution of dreamer v3 (https://arxiv.org/abs/2301.04104)."
---
<img width="731" height="152" alt="Image" src="https://github.com/user-attachments/assets/89b7f195-bb42-45ef-8505-a05859ea4b23" />

[paper](https://arxiv.org/pdf/2308.01399)

## TL;DR
- **I read this because.. :** Came across this while searching for agent + VLM. Because I'm interested in gaming rl. ICML'24 oral
- **task :** world modeling, embodied agent (agent that performs language instructions)
- **problem :** The existing method is given a language and performs an action, but the real-world is more like a continuous input/output of language, action, and video.
- **IDEA :** Couldn't we use language not only for instruction, but also for acquiring knowledge and predicting the future?
- **input/output :** (world model) {video, text, action} -> {representation of future, (optional) language} (agent) state -> action 
- **architecture :** (vision encoder) strided image encoder (vision decoder) strided image decoder (text embedding) embedding from scratch or T5 (sequence modeling) GRU /// (policy model) DreamerV3
- **objective :** (world model) reconstruction error + regularization + next representation prediction (policy model) maximize expected reward 
- **baseline :** (model-free RL) IMPALA, R2D2,  (task-specific model) EMMA (Messenger)
- **data :** (world model) replay buffer from {homegrid, messenger, vln-ce, langroom} (pretraining) messenger manual(in-domain), tiny stories(general)
- **evaluation :** HomeGrid (proposed), Messenger, VLM-CE, LangRoom (proposed)
- **result :** 
- **contribution :** Effective world model learning for information coming in streaming (single "text" modality pretraining seems to be the most contribution?) -- Learning with world model + actor-critic seems to be a contribution of dreamer v3 (https://arxiv.org/abs/2301.04104).
- **etc. :**

## Details

<img width="986" height="445" alt="Image" src="https://github.com/user-attachments/assets/94dd13f5-174e-4a8c-a352-5036e77d198b" />

<img width="1014" height="547" alt="Image" src="https://github.com/user-attachments/assets/c4264c59-edcf-4780-8617-9e014ae7ac0f" />

### problem setting
- action: $a_t$ -- discrete action
- reward $r_t$
- episode end $c_t$ ($c_t$=0 when ends)
- observation $o_t$ -> multimodal observation (visual $x_t$, textual $l_t$)

<img width="493" height="594" alt="Image" src="https://github.com/user-attachments/assets/2b332119-9149-470a-a4bc-7f26f6b1c809" />


<img width="700" height="321" alt="Image" src="https://github.com/user-attachments/assets/15958fa9-e22f-4a50-8ffd-a216f851a9c3" />

### world model learning
  - <img width="504" height="128" alt="Image" src="https://github.com/user-attachments/assets/f37f5b70-3b5a-4f7f-a623-80895230c0fd" />
- Recurrent State Space Model (RSSM) -- uses a GRU-based sequence model
- Predicts $z_t$ : reresentation representation -> $\hat{z_{t+1}}$
  - $h_t$ : recurrent state
- multimodal representation
- Compress $z_t$ with a variational autoencoder objective. Then predict reward $\hat r_t$ and $\hat c_t$ for $z_t$ as well.
  - <img width="515" height="176" alt="Image" src="https://github.com/user-attachments/assets/38bfc0c6-45a7-4cbb-b11c-848626c4cbde" />
- Additionally add regularize to prevent $z_t$ and $\hat z_t$ from being too different
- future prediction 
  - <img width="497" height="42" alt="Image" src="https://github.com/user-attachments/assets/8308dbee-f3c6-4972-9886-7d1bb419ddd1" />
- Learn to make the model's predicted $\hat {z_t}$ in the current model state $z_{t-1}$, $h_{t-1}$ match the actual $z_t$ in the next step.
- Let the world model predict $\hat z_t$ for future representations, allowing it to predict future images, languages, and rewards and learn correlations across multiple modalities
- single modality pretraining
- World models can be trained offline, so you can train world models with text-only and video-only data
- For text only, you can pretrain by setting the image, action input to zero and the decoder loss coefficient to zero.
- Unlike language modeling loss, it is trained in a way that predicts the representation of
- You can initialize actor, critic, and then pretrain them for each modality like this
  
### policy learning
- Replicating Dreamer V3's structure with actor-critic

<img width="451" height="24" alt="Image" src="https://github.com/user-attachments/assets/79db9c84-0401-4d80-be2f-ee8964089928" />

 ### experiment
- RQ1: It would be better to put {image, language} as a pair per timestep
- RQ2: Since we use a variety of languages when training, performance will be better when we include different types of languages compared to the model-free baseline.
- RQ3: Putting instructions into the world model is no worse than using language-conditioned policies.
- RQ4: Show that a multimodal generative model enables grounded language generation and learning from offline text-only data

- RQ1: It would be better to put {image, language} as a pair per timestep
  - <img width="539" height="378" alt="Image" src="https://github.com/user-attachments/assets/a062dd81-d5ce-405f-82cc-e346ef82eae9" />
- Dynalang performed best compared to other baselines that were language conditioned (~10M).

- RQ2 & 3:
- Suggested HomeGrid, an environment with language hints in addition to language instruction.
  - <img width="780" height="563" alt="Image" src="https://github.com/user-attachments/assets/eb8dcac4-e830-4351-bbe8-2043ec8ffef8" />
- Reward for completing many quests within 100 steps
- future observation : where object is
- dynamics: what action must be taken to open the trash can
- correction: Say something like "no, turn around" when you're getting farther away from your current goal
- It performs better when hinted, and it also performs better with task-only instructions.
  - <img width="790" height="153" alt="Image" src="https://github.com/user-attachments/assets/c1105eef-9278-4429-b225-314ad424f9e5" />
- Performance for Messenger games for which a game manual is provided
 - <img width="1085" height="249" alt="Image" src="https://github.com/user-attachments/assets/4184a948-4989-4d9c-89cc-458457f8d61f" />

- Vision language navigation continuous environment 
  - <img width="771" height="216" alt="Image" src="https://github.com/user-attachments/assets/5f910a70-db6f-4958-8887-c94978d92793" />
- A setting with a wayfinding task and a lower-level action would be the continuous environment
- Dense rewards related to distance to goal, with success rewards if successful
- No, let's make sure R2D2 doesn't succeed at all. lol Is this the baseline?
- LangRoom : embodied question answering 
- Demonstrate that you can also create a language in the middle
- A setting where questions are answered but utterances are made via perception
  - <img width="786" height="203" alt="Image" src="https://github.com/user-attachments/assets/67da1aa7-f931-4544-9e75-ade8a5d6759e" />
- If we increased the vocab size too much, performance did not converge without prior
  - <img width="397" height="258" alt="Image" src="https://github.com/user-attachments/assets/5073042a-bfdd-4cd9-94ec-ca9fc8fc2b3b" />
- Added an entropy regularizer to the world model to resolve this
  - <img width="513" height="53" alt="Image" src="https://github.com/user-attachments/assets/25c8b624-3224-48f3-bf35-65173c559b1e" />
- text-only pretraining
- I tried text only pretraining because it was an experiment with the experience online and I thought I needed offline as well.
  - <img width="386" height="229" alt="Image" src="https://github.com/user-attachments/assets/1658e95b-ab22-49b0-8359-414513e5fa72" />
- in-domain is manuals from Messenger S2 games
- domain-general text is a 2M short story generated with GPT-4
- Learning the general domain from scratch one-hot performed better than using T5.

  
---
- actor model config
  - <img width="1069" height="687" alt="Image" src="https://github.com/user-attachments/assets/3e10ebf3-1fec-4724-903b-fad88b2fc20b" />

  