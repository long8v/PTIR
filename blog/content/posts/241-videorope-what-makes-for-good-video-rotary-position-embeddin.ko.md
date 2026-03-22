---
title: "[220] VideoRoPE: What Makes for Good Video Rotary Position Embedding?"
date: 2025-11-25
tags: ['MLLM', '2025Q1', 'video']
paper: "https://arxiv.org/abs/2502.05173"
issue: 241
issueUrl: "https://github.com/long8v/PTIR/issues/241"
---
<img width="1290" height="301" alt="Image" src="https://github.com/user-attachments/assets/0919cd61-1734-4b55-8c5a-bb27e767b7b7" />

[paper](https://arxiv.org/abs/2502.05173)

## TL;DR
- **I read this because.. :** Qwen3-VL에서 사용했다는 [interleaved mRoPE](https://github.com/huggingface/transformers/blob/v4.57.1/src/transformers/models/qwen3_vl/modeling_qwen3_vl.py#L299-L314)가 이해가 안되어서.
- **task :** RoPE in video LLM
- **problem :** mRoPE에서 head dimension을 3등분 해서 사용하는데, temporal 차원이 앞부분에 할당되는게 이상하다.
- **idea :** temporal을 가장 뒤로 (low frequency)로 할당하자.
- **input/output :** {video, question} -> answer
- **architecture :** ViT from Qwen2-7B, Qwen-7B LLM
- **objective :** CE loss
- **baseline :** Vanilla RoPE, mRoPE, RoPE-TIE
- **data :** 1.3M video pair from LLaVA-Video-178k
- **evaluation :** LongVideoBench, MLVU, Video-MME, V-NIAH, V-NIAH-D(proposed)
- **result :** Video-MME를 제외하고 성능이 더 좋고, extrapolate도 더 잘한는듯.
- **contribution :** 간단 sota
- **etc. :**

## Details
### Exisiting 
- RoPE general
<img width="490" height="54" alt="Image" src="https://github.com/user-attachments/assets/03b755ad-8b2d-4d3c-a03a-bf9dbbb542a7" />

<img width="612" height="163" alt="Image" src="https://github.com/user-attachments/assets/6c7e6a41-6703-4854-b62f-b791aed60641" />

watch [here](http://youtube.com/watch?v=GQPOtyITy54)

Q와 K에 각각 각도 변환 (`[[cos, -sin], [sin, cos]]`) 을 시키는데, 이 각도 변환을 시킨걸 self-attention 연산을 하게 되면 (m-n) (상대 거리)에 대한 각도변환으로만 나오게 됨. 
이때 우리의 Q, K 벡터는 2차원이 아니라 n차원이기 때문에 이에 대한 trick으로 각각 2로 나눠서 저 rotation weight 연산을 해주게 됨. 

이때 저기 곱해지는 theta가 dimension이 높을수록 (뒤에 있는 dimension일 수록) 작아져서 (m-n)의 변화에 조금 씩 움직이는 low-frequency가 됨.

<img width="619" height="334" alt="Image" src="https://github.com/user-attachments/assets/68a8e5d2-59be-43e3-b7f3-1226eeae85e0" />

- mRoPE
https://github.com/huggingface/transformers/blob/v4.57.1/src/transformers/models/qwen2_5_vl/modeling_qwen2_5_vl.py#L545-L587

<img width="625" height="190" alt="Image" src="https://github.com/user-attachments/assets/dc06a088-af9d-481b-9a14-4b5f4ad4346d" />

위의 $R_{\theta,m}^d$ 에서 position ids(=m)을 구하는 계산식만 (w, h, t)로 나누어진다고 보면 됨. 

<img width="588" height="77" alt="Image" src="https://github.com/user-attachments/assets/0697a1a9-3e76-4fec-af1d-792a2e3a8883" />

<img width="600" height="504" alt="Image" src="https://github.com/user-attachments/assets/15ac006f-4cd5-4a66-a2d4-d24c6a3937df" />

```
# Q = [batch size, n heads, query len, head dim]
# K = [batch size, n heads, key len, head dim]
# V = [batch size, n heads, value len, head dim]
		
# k.permute(0, 1, 3, 2) = [batch size, n heads, head dim, key len]
energy = torch.matmul(Q, K.permute(0, 1, 3, 2)) / self.scale
# energy = [batch size, n heads, query len, key len]
```
부끄럽지만 헷갈렸는데 head_dim 끼리 dot product를 해서 scalar를 구하는 거기 때문에 이걸 나눠서 dot product로 해서 더해도 같은 것임 ㅎㅎ;

### why is this wrong?

Round and Round We Go! What makes Rotary Positional Encodings useful?  https://arxiv.org/abs/2410.06205
high frequency는 local 한 정보를 뽑고 low frequency는 long context를 뽑는다는 관찰.

<img width="600" height="761" alt="Image" src="https://github.com/user-attachments/assets/0c345fda-88ed-44ea-853b-53f862d31302" />

### Proposed

<img width="610" height="407" alt="Image" src="https://github.com/user-attachments/assets/2173166f-2176-46dd-8ce0-eed3ea589a3b" />

### Result

<img width="1225" height="793" alt="Image" src="https://github.com/user-attachments/assets/ba3018d8-4705-48b0-b5b4-41a7edf4373b" />

<img width="591" height="656" alt="Image" src="https://github.com/user-attachments/assets/b5cecfd3-b101-449f-a69e-49dc26694767" />