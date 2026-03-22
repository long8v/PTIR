---
title: "[216] Emerging Properties in Unified Multimodal Pretraining"
date: 2025-09-04
tags: ['MLLM', '2025Q2', 'WORLD-MODEL']
paper: "https://arxiv.org/abs/2505.14683"
issue: 237
issueUrl: "https://github.com/long8v/PTIR/issues/237"
summary: "- **I read this because...**: unified multimodal model, open-source model against proprietary models like GPT-4o/Gemini 2.0. arXiv 2025. a.k.a. BAEGEL - - **contribution**:"
---
<img width="1278" height="575" alt="Image" src="https://github.com/user-attachments/assets/d6e7199d-e46a-46e1-91f4-c188b5e09aff" />

[paper](https://arxiv.org/abs/2505.14683)

## TL;DR
- **I read this because...**: unified multimodal model, open-source model against proprietary models like GPT-4o/Gemini 2.0. arXiv 2025. a.k.a. BAEGEL
- **task**: unified multimodal understanding & generation (text, image, video)
- Problem: Existing open-source models have separated understanding and generation, and have a large performance gap with proprietary models. Need a unified model trained on interleaved multimodal data
- Idea: Mixture-of-Transformer-Experts (MoT) architecture for both multimodal understanding and generation in a single model, unleashing emergent capabilities
- **input/output**: (understanding) {text, image, video} -> text response (generation) text prompt -> image/video (editing) {text instruction, image} -> edited image
- **architecture**: (visual encoder) VAE encoder (FLUX) + ViT (Siglip-SO400M) (Transformer) 14A7B Transformer(Qwen2.5 LLM) (visual decoder) VAE decoder (FLUX) 
- **objective**: next group of token prediction (text tokens + visual tokens) + reconstruction loss + generation loss
- **baseline**: (VLM understanding) Qwen2.5-VL, InternVL-2.5 (T2I generation) SD3-Medium, FLUX-1-dev (image editing) InstructPix2Pix, Janus-Pro-7B
- **data**: (pretraining) trillions of interleaved text, image, video, web data (continued training) refined multimodal datasets (supervised finetuning) specific task datasets
- **evaluation**: MME, MMBench, MM-Vet, MathVista (understanding), GenEval (T2I), GEdit-Bench-EN, IntelligentBench (editing)
- **results**: (1) outperforms top-tier open models (Qwen2.5-VL, InternVL-2.5) on VLM benchmarks (2) performs competitively with specialist T2I models with a GenEval of 0.88 (3) emergent capabilities: basic multimodal understanding/generation, traditional editing, intelligent editing + world modeling
- **contribution**: 
- Unify multimodal understanding + generation + editing in a single unified model
- Prove the scalability of your MoT architecture
- Express emergent capabilities (free-form editing, future frame prediction, 3D manipulation, world navigation)
- Demonstrate the effectiveness of interleaved multimodal pretraining
- **etc**: Fully open source with Apache 2.0 license. Developed by the ByteDance Seed team

## Details
### architecture

<img width="695" height="292" alt="Image" src="https://github.com/user-attachments/assets/6d799b1b-d70c-4680-b509-2686ec6869ce" />

There are methods such as quantized auto-regressive and external diffusion, but the former has too low performance and the latter has limited expressiveness because the vector must be compressed through an adapter. Therefore, an integrated transformer structure is used.

- arch design choice 
  - visual understanding: Siglip-SO400M/14, NaViT, 980x980 maximum input size
  - visual generation: pretrained VAE from FLUX -- down sample ratio 8 -- 2x2 patch embedding 
- causal attention
- noised VAE tokens: Diffusion noise added to the VAE latent. Created with Rectified flow and only used to score mse loss
- clean VAE tokens: clean VAE latents used as conditions for generating images or text.
- ViT tokens: Tokens for understanding images in interleaved data
- The above three clean VAE and ViT tokens are only causally attended to each other, so they can see each other (and would see each other if they came before), but the noisy VAE tokens are masked from attending.
- Mixture-of-Transformer
- Make two copies of the Qwen 2.5 LLM and use each as an expert for understanding and generation, but only share the attention layer.
- Explain that the learning curve was better than MoE, especially in generation loss
  - <img width="872" height="378" alt="Image" src="https://github.com/user-attachments/assets/6249949d-2e38-40f0-a7f0-17508fea13b6" />
 
### data
Trying to make a very complex and detailed Interleaved.

<img width="858" height="241" alt="Image" src="https://github.com/user-attachments/assets/cfbfc4f6-f37e-4847-88fb-58a243cd4879" />

- text-only data 
- vision-text paired data
- vision-text interleaved data 
- video data: [Koala36M](https://koala36m.github.io/) (looks like clean segmented video data), MVImgNet2.0 (images viewed in multi-view)
  - web data : OmniCorpus, image-editing data
- data filtering
- video data: breaking it into segments and clips with shot detection
- Merge segments based on visual semilarity
- logo, black border cleared
- Finally, filter by length, Resolution, claritiy, motion clarity, dedup with CLIP
- web data: Similar to DeepSeekMath, LLM is used to classify document topics, then fastText is used to train a classifier to filter, and then LLM is used for fine-grained filtering.
- data construction
  - interleaved data from videos
- Generate descriptions of visual changes in consecutive frames, creating captions with Qwen2.5-VL-7B (limiting generation to 30 tokens to reduce hallucination). Generate captions by pulling an average of 4 frames per video
  - interleaved data from webs
- Created with a captioner at the end to ensure the image and text align well
  - reasoning-augmented data
- t2i generation -> free-form image manipulation -> conceptual edits Generate this process using different models. for example, reasoning, generate with deepseek-r1.
  
<img width="867" height="268" alt="Image" src="https://github.com/user-attachments/assets/9fbce15b-88ec-4c5e-ab1f-0d57228951f8" />

<img width="874" height="390" alt="Image" src="https://github.com/user-attachments/assets/01ac9249-845e-47cc-8ffa-6f8e03ff1784" />

### training

<img width="617" height="447" alt="Image" src="https://github.com/user-attachments/assets/309b1b90-ead0-473c-a2db-3c87fad7bd24" />

<img width="647" height="330" alt="Image" src="https://github.com/user-attachments/assets/ba05fa0d-8b3f-4781-8369-f36081aec29f" />

### result 

<img width="661" height="612" alt="Image" src="https://github.com/user-attachments/assets/2991bdd6-e8c4-456f-b7f6-3743676ba524" />

<img width="634" height="525" alt="Image" src="https://github.com/user-attachments/assets/39dd28a5-c094-4eb9-af76-b05e16d4379e" />

<img width="642" height="740" alt="Image" src="https://github.com/user-attachments/assets/a511c5d2-235b-470a-afb9-e1df44d6092a" />

<img width="667" height="485" alt="Image" src="https://github.com/user-attachments/assets/52820953-d72f-40e3-ac27-bbcc595ff6f6" />

<img width="890" height="910" alt="Image" src="https://github.com/user-attachments/assets/ee59d9d0-cf54-4d03-ba44-d9452dfe69ff" />

<img width="991" height="289" alt="Image" src="https://github.com/user-attachments/assets/62c0d003-ac51-4bf0-9e33-dc5b5a4b91a8" />

<img width="904" height="346" alt="Image" src="https://github.com/user-attachments/assets/91d2c62c-f774-420c-8ef9-a5244db895c2" />

World modeling / world navigation skills manifested.
<img width="1020" height="675" alt="Image" src="https://github.com/user-attachments/assets/24bb2b7a-d8ee-4fad-8173-2a3831adc06c" />