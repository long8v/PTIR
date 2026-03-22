---
title: "[216] Emerging Properties in Unified Multimodal Pretraining"
date: 2025-09-04
tags: ['MLLM', '2025Q2', 'WORLD-MODEL']
paper: "https://arxiv.org/abs/2505.14683"
issue: 237
issueUrl: "https://github.com/long8v/PTIR/issues/237"
---
<img width="1278" height="575" alt="Image" src="https://github.com/user-attachments/assets/d6e7199d-e46a-46e1-91f4-c188b5e09aff" />

[paper](https://arxiv.org/abs/2505.14683)

## TL;DR
- **I read this because..**: unified multimodal model, GPT-4o/Gemini 2.0 같은 proprietary 모델 대항하는 open-source 모델. arXiv 2025. a.k.a. BAEGEL
- **task**: unified multimodal understanding & generation (text, image, video)
- **problem**: 기존 open-source 모델들은 understanding과 generation이 분리되어 있고, proprietary 모델들과 성능 격차가 큼. interleaved multimodal data로 학습된 unified model이 필요
- **idea**: MoT(Mixture-of-Transformer-Experts) 아키텍처로 하나의 모델에서 multimodal understanding과 generation을 모두 수행하면서, emergent capabilities 발현
- **input/output**: (understanding) {text, image, video} -> text response (generation) text prompt -> image/video (editing) {text instruction, image} -> edited image
- **architecture**: (visual encoder) VAE encoder (FLUX) + ViT (Siglip-SO400M) (Transformer) 14A7B Transformer(Qwen2.5 LLM) (visual decoder) VAE decoder (FLUX) 
- **objective**: next group of token prediction (text tokens + visual tokens) + reconstruction loss + generation loss
- **baseline**: (VLM understanding) Qwen2.5-VL, InternVL-2.5 (T2I generation) SD3-Medium, FLUX-1-dev (image editing) InstructPix2Pix, Janus-Pro-7B
- **data**: (pretraining) trillions of interleaved text, image, video, web data (continued training) refined multimodal datasets (supervised finetuning) specific task datasets
- **evaluation**: MME, MMBench, MM-Vet, MathVista (understanding), GenEval (T2I), GEdit-Bench-EN, IntelligentBench (editing)
- **result**: (1) VLM 벤치마크에서 top-tier open models (Qwen2.5-VL, InternVL-2.5) 능가 (2) GenEval 0.88점으로 specialist T2I models와 경쟁적 성능(3) emergent capabilities: basic multimodal understanding/generation, traditional editing, intelligent editing + world modeling
- **contribution**: 
  - single unified model로 multimodal understanding + generation + editing 통합
  - MoT 아키텍처의 scalability 증명
  - emergent capabilities (free-form editing, future frame prediction, 3D manipulation, world navigation) 발현
  - interleaved multimodal pretraining의 효과 입증
- **etc**: Apache 2.0 license로 완전 오픈소스. ByteDance Seed팀 개발

## Details
### architecture

<img width="695" height="292" alt="Image" src="https://github.com/user-attachments/assets/6d799b1b-d70c-4680-b509-2686ec6869ce" />

quantized auto-regressive, external diffusion 등의 방법이 있지만 전자는 성능이 너무 낮고 후자는 adapter를 통해 벡터가 압축되어야만 하는 형태이기 때문에 표현력의 한계가 있음. 해서 통합된 트랜스포머 구조를 가지고 감.

- arch design choice 
  - visual understanding: Siglip-SO400M/14, NaViT, 980x980 maximum input size
  - visual generation: pretrained VAE from FLUX -- down sample ratio 8 -- 2x2 patch embedding 
- causal attention
  - noised VAE tokens : VAE latent 에 diffusion noise 추가한 부분. Rectified flow로 생성하고 mse loss를 매기는데만 사용됨
  - clean VAE tokens : 이미지나 텍스트를 생성하기 위한 condition으로 사용되는 clean VAE latent.
  - ViT tokens : interleaved data의 이미지 이해를 위한 토큰 
  - 위 세개가 clean VAE, ViT 토큰은 서로 causal attention만 적용되어 서로 볼 수 있는 구조지만 (이전에 나온다면 볼 수 있는 구조), noised VAE tokens는 attend하지 않도록 masking
- Mixture-of-Transformer
  - Qwen 2.5 LLM을 두개 복사해서 각각 understanding, generation을 위한 expert로 쓰되 attention layer만 공유하는 형태임. 
  - MoE 보다 특히 generation loss에서 학습 커브가 더 좋았다고 설명
  - <img width="872" height="378" alt="Image" src="https://github.com/user-attachments/assets/6249949d-2e38-40f0-a7f0-17508fea13b6" />
 
### data
엄청 복잡하고 세밀한 Interleaved를 만드려고 노력함.

<img width="858" height="241" alt="Image" src="https://github.com/user-attachments/assets/cfbfc4f6-f37e-4847-88fb-58a243cd4879" />

- text-only data 
- vision-text paired data
- vision-text interleaved data 
  - video data: [Koala36M](https://koala36m.github.io/)(clean한 segment video data인듯), MVImgNet2.0(multi-view로 본 이미지들)
  - web data : OmniCorpus, image-editing data
- data filtering
 - video data: shot detection을 통해 segment로 나누고 clip으로 만든다
   - visual semilarity 기반으로 segment를 합침
   - logo, black border 지움
   - 최종적으로 길이, Resolution, claritiy,  motion clarity, dedup with CLIP으로 filter
 - web data: DeepSeekMath와 비슷하게 LLM으로  document 주제로 분류하라고 한 뒤 fastText로 분류기 학습해서 필터링 하고 그 뒤에 또 LLM으로 fine-grained filtering을 함 
- data construction
  - interleaved data from videos
    - 연속되는 프레임에서 visual changes 에 대한 설명을 생성, Qwen2.5-VL-7B로 캡션을 만들고 (hallucination을 줄이기 위해 30 토큰으로 생성을 제한). 비디오당 평균적으로 4 프레임 정도 뽑아서 캡션 생성
  - interleaved data from webs
    - 이미지와 텍스트가 잘 align되게 하기 위해서 중간중간 captioner로 생성함
  - reasoning-augmented data
    - t2i generation -> free-form image manipulation -> coneceptual edits이 공정을 여러가지 모델들 사용하여 생성. reasoning 같은 경우 deepseek-r1으로 생성.   
  
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

world modeling / world navigation 능력이 발현됨. 
<img width="1020" height="675" alt="Image" src="https://github.com/user-attachments/assets/24bb2b7a-d8ee-4fad-8173-2a3831adc06c" />