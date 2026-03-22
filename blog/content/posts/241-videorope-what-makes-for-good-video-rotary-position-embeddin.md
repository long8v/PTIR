---
title: "[220] VideoRoPE: What Makes for Good Video Rotary Position Embedding?"
date: 2025-11-25
tags: ['MLLM', '2025Q1', 'video']
paper: "https://arxiv.org/abs/2502.05173"
issue: 241
issueUrl: "https://github.com/long8v/PTIR/issues/241"
summary: "I don't understand the [interleaved mRoPE](https://github.com/huggingface/transformers/blob/v4.57.1/src/transformers/models/qwen3_vl/modeling_qwen3_vl.py#L299-L314) you used in Qwen3-VL. - Simple sota"
---
<img width="1290" height="301" alt="Image" src="https://github.com/user-attachments/assets/0919cd61-1734-4b55-8c5a-bb27e767b7b7" />

[paper](https://arxiv.org/abs/2502.05173)

## TL;DR
- **I read this because.. :** I didn't understand the [interleaved mRoPE](https://github.com/huggingface/transformers/blob/v4.57.1/src/transformers/models/qwen3_vl/modeling_qwen3_vl.py#L299-L314) that you used in Qwen3-VL.
- **task :** RoPE in video LLM
- **problem :** mRoPE uses the head dimension in thirds, but it's strange that the temporal dimension is assigned to the front.
- Idea :** assign temporal to the back of the line (lowest frequency).
- **input/output :** {video, question} -> answer
- **architecture :** ViT from Qwen2-7B, Qwen-7B LLM
- **objective :** CE loss
- **baseline :** Vanilla RoPE, mRoPE, RoPE-TIE
- **data :** 1.3M video pair from LLaVA-Video-178k
- **evaluation :** LongVideoBench, MLVU, Video-MME, V-NIAH, V-NIAH-D(proposed)
- **result :** Better performance except for Video-MME, and extrapolate seems to work better.
- **contribution :** simple sota
- **etc. :**

## Details
### Exisiting 
- RoPE general
<img width="490" height="54" alt="Image" src="https://github.com/user-attachments/assets/03b755ad-8b2d-4d3c-a03a-bf9dbbb542a7" />

<img width="612" height="163" alt="Image" src="https://github.com/user-attachments/assets/6c7e6a41-6703-4854-b62f-b791aed60641" />

watch [here](http://youtube.com/watch?v=GQPOtyITy54)

We give Q and K an angular transformation (`[[cos, -sin], [sin, cos]]`), but when we run the self-attention operation, the angular transformation only comes out as an angular transformation for (m-n) (relative distance).
Since our Q and K vectors are n-dimensional instead of 2-dimensional, the trick is to divide each by 2 to perform the low rotation weight operation.

The theta that gets multiplied there gets smaller the higher the dimension (the later the dimension), resulting in a low-frequency that moves slightly with changes in (m-n).

<img width="619" height="334" alt="Image" src="https://github.com/user-attachments/assets/68a8e5d2-59be-43e3-b7f3-1226eeae85e0" />

- mRoPE
https://github.com/huggingface/transformers/blob/v4.57.1/src/transformers/models/qwen2_5_vl/modeling_qwen2_5_vl.py#L545-L587

<img width="625" height="190" alt="Image" src="https://github.com/user-attachments/assets/dc06a088-af9d-481b-9a14-4b5f4ad4346d" />

Only the formula above for finding the position ids(=m) in $R_{\theta,m}^d$ is divided by (w, h, t).

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
I'm embarrassed to say I was confused, but there's a dot product between head_dim to get a scalar, so it's the same thing if you divide it and add it with dot product lol;

### why is this wrong?

Round and Round We Go! What makes Rotary Positional Encodings useful?  https://arxiv.org/abs/2410.06205
The observation that high frequency pulls local information and low frequency pulls long context.

<img width="600" height="761" alt="Image" src="https://github.com/user-attachments/assets/0c345fda-88ed-44ea-853b-53f862d31302" />

### Proposed

<img width="610" height="407" alt="Image" src="https://github.com/user-attachments/assets/2173166f-2176-46dd-8ce0-eed3ea589a3b" />

### Result

<img width="1225" height="793" alt="Image" src="https://github.com/user-attachments/assets/ba3018d8-4705-48b0-b5b4-41a7edf4373b" />

<img width="591" height="656" alt="Image" src="https://github.com/user-attachments/assets/b5cecfd3-b101-449f-a69e-49dc26694767" />