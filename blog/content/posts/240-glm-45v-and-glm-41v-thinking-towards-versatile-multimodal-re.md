---
title: "[219] GLM-4.5V and GLM-4.1V-Thinking: Towards Versatile Multimodal Reasoning with Scalable Reinforcement Learning"
date: 2025-11-12
tags: ['RL', 'MLLM', '2025Q3']
paper: "https://arxiv.org/abs/2507.01006"
issue: 240
issueUrl: "https://github.com/long8v/PTIR/issues/240"
summary: "A relatively(?) new MLLM model with a hard cut of RL. I read it because an acquaintance said it was good. - Especially in the RL stage, he summarized various trial and error or lesson learned well. Like kimi, I love rl. Also, thanks for summarizing the problems with VLM... But why doesn't RL have a training step."
---
<img width="606" height="234" alt="Image" src="https://github.com/user-attachments/assets/0bb4672e-05c1-4cec-a0c8-f92f4eb065be" />

[paper](https://arxiv.org/abs/2507.01006), [code](https://github.com/zai-org/GLM-V)

## TL;DR
- **I read this because.. :** A relatively(?) new MLLM model and a model that has cut RL hard. I read it because an acquaintance said it was good.
- **task :** MLLM with thinking 
- **problem :** good MLLM model
- **idea :** multi-modal pretraining -> cold start SFT -> RL (RLVR + RLHF). Let's collect data hard
- **input/output :** {image, video, question} -> answering 
- **architecture :** VE (AIMv2-Huge), LLM (GLM-4-9B-0414, GLM-4.5-Air)
- **objective :** CE loss -> GRPO loss 
- **baseline :** Qwen2.5-VL, Kimi-VL, InternVL3, GPT-4o, Gemini... 
- **data :** pretraining data 50M -> SFT (??) -> RL (??)
- **evaluation :** (image) general VQA, STEM, OCR-chart, long-doc, grounding, GUI agent, coding(Design2Code, Flame-React-Eval), (video) VideoMME, MMVU, LVBench, MotionBench 
- **result :** Among comparable models, the SOTA
- **contribution :** Especially in the RL phase, you've done a good job of summarizing the various trials and errors and lessons learned. Like kimi, I like rl. Also, VLM problems are well summarized. But why RL has no training step.
- **etc. :**

## Details
### architecture

<img width="616" height="448" alt="Image" src="https://github.com/user-attachments/assets/2221d865-e5ee-41e2-b308-f6c21fe603ee" />

- VE (AIMv2-Huge), GLM-4-9B-0414, GLM-4.5-Air
- 3D conv (w, h, temporal) - if image is duplicated (stride 2, so a single image is just two copies and put on the temporal axis)
- 2D-RoPE in ViT + original absolute PE (bicubic interpolation)
- In LLM, replace RoPE with 3D-RoPE for spatial understanding (w, h, nth token?)

### pretraining stage
- data (eventually 50M)
image caption, interleaved, OCR data, Grounding data, Video data, instruction tuning data. 
  - Video data
    - corpus from academic, web, proprietary sources
- Developed a pipeline to annotate complex action or in-scene text with fine-grained human annotation, as standard captions are prone to hallucinations and omissions (sounds like you're not captioning, you're annotating something else?)
- Deeper visual understanding Annotate cinematic elements such as camera motion or shot composition with a human-in-the-loop workflow.
- No matter how long the video is
- training
  - multimodal pre-training (seq len 8192) — 120K step -> long-context continual pre-training (seq len 32K) — global step 10K 1.5 bs

### SFT stage
- high-quality CoT reasoning examples 
  - almost chinese and english
  - filter with pretrained model (too easy or excessively hard)
- Tight data filtering and iterative data enhancement (RL and re-create cold-start data with that model...)
- training 
  - full param tuning
  - seq len 32K 
  - global bs 32
  - also includes high-quality text-only long-form SFT data. 
- GLM-4.5V is a think / no-think model, so it learns that if you put /nothink as a user prompt, the thinking content will be empty.

### RL stage
- reward
- A combination of RLVR and model-based rewards (RLHF)
- The extraction of the final answer in RLVR : LLM extraction can be difficult if the think is long, so it was parsed as <|begin_of_box|>{FINAL_ANSWER}<|end_of_box|>. \boxed{} was also difficult as the final answer became longer.
- Reward shaving hard per domain...
  - <img width="841" height="321" alt="Image" src="https://github.com/user-attachments/assets/27808b2a-dc17-4ff3-908b-7fe362f0fe5a" />
- algorithm    
  - GRPO
- no KL (KL tended to rise faster than text-only, but putting in a kl term limited performance), no entropy bonus, clip higher, larger BS
- training recipe 
  - RL with Curriculum Sampling (RLCS), dynamic sampling extension with ratio EMA, no KL and entropy loss
- lesson learned
  - we discover that when training a unified VLM across diverse skills, any weakness in the reward signal for a single capability can derail the entire training (figure 5)
- This is the funny part, as we learned by combining multiple domains, if any of the rewards can be hacked, the model performs poorly across the board.
- That's why we say run for each domain -> check rollout to see if we're getting rewarded well, and so on and so forth.
    - A coarse or incomplete reward design can lead the model to discover shortcuts for boosting its reward rather than truly improving its task performance.
- For example, when using the llm-as-a-judge reward (RLHF here) and doing a "counting task", the response sometimes rolls out like "The correct answer is a number between 1 and 10"... lol
    - <img width="608" height="414" alt="Image" src="https://github.com/user-attachments/assets/ef426232-6e1a-4db5-adf4-46d4b64e0b79" />
  - The peak performance in the RL phase does not perfectly correlate with a cold-start SFT model’s performance.
  - Domain interference in RL is less pronounced than in SFT. 

### result 

<img width="561" height="854" alt="Image" src="https://github.com/user-attachments/assets/66f0d0bc-0ff2-4327-873e-ce2e21bc21a4" />

- In terms of evaluation, MMVU and VideoMMMU, which are close to academics, show an increase of about 4 and 6 points, respectively, when think is enabled, but for LVBench and MVBench, which are long video tasks, direct evaluation performs better, and VideoMME shows little performance improvement. Among the image benches, STEM types are still performing well, but general VQA is not so good.
- Mostly used vLLM for evaluation, but used sglang for video inference
- vision token max uses 6K for images and 48K for video.
- Use GPT4o for all cases where APIs are needed, such as parsing. Evaluate other models equally.

<img width="587" height="365" alt="Image" src="https://github.com/user-attachments/assets/64cd4f91-fe92-4656-821b-c186d4e5700f" />

- Effect of RL on cross-domain performance - better when all domains are mixed together

<img width="568" height="829" alt="Image" src="https://github.com/user-attachments/assets/e3417af6-0f17-4a82-9266-e90925ce398b" />

- It's almost sota under 10B.
