---
title: "[201] VinePPO: Unlocking RL Potential For LLM Reasoning Through Refined Credit Assignment"
date: 2025-02-08
tags: ['RL', 'reasoning', '2025Q1']
paper: "https://openreview.net/forum?id=5mJrGtXVwz"
issue: 222
issueUrl: "https://github.com/long8v/PTIR/issues/222"
---
<img width="578" alt="Image" src="https://github.com/user-attachments/assets/e9928169-f85b-4f34-9ab2-a146ce4ffa17" />

[paper](https://openreview.net/forum?id=5mJrGtXVwz)

## TL;DR
- **I read this because.. :** 언급되어 
- **task :** RL for reasoning 
- **problem :** credit assignment를 해결하기 위해 PPO 에서 사용되고 있는 value model이 학습이 잘 안되는 것 같다
- **idea :** value model 대신 MC를 사용해서 value를 구하자
- **architecture :** DeepSeekMath 7B, Rho Math 1.1B
- **objective :** PPO loss -- Value network 학습이 없음.
- **baseline :** PPO, DPO+, RestEM
- **data :** GSM8K, MATH
- **evaluation :** Pass@1 accuracy
- **result :** 1) 성능상 PPO보다 우위 2) 중간에 inference를 하므로 per step당 시간은 더 오래걸리지만 더 빨리 수렴한다 (wall-clock efficiency) 3) 같은 성능에 KL-divergence가 낮다. (KL divergence efficiency) 
- **contribution :** GRPO/RLOO랑 비슷하면서 PPO의 value network가 credit assignment를 하는것까지 차용.
- **etc. :** supp까지 잘 정리되어 있어서 좋았다. iclr 오픈 리뷰보면 리뷰어들 잠수타서 지못미ㅜㅜ

## Details
### intro
   - <img width="683" alt="Image" src="https://github.com/user-attachments/assets/b1e32651-d13a-4cdb-bd82-1e2b7ff47efb" />
   - critical하게 중요한 step이 있고 이에 대해 더 가중치를 부가해야되는데 action과 reward 사이의 delay가 있고 이는 Rl의 가장 중요한 문제인 credit assignment problem이다. 
   - PPO는 value 네트워크를 학습하지만 이게 잘 학습이 안되어 policy gradient의 baseline 정도로 동작한다거나 average reward로 대체하는게 낫다는 연구들이 있었다.
   - value network는 얼마나 잘 학습되고 있는것일까?
   - unbiased value estimiate를 구하고 싶다 -> VinePPO
### thumbnail
<img width="695" alt="Image" src="https://github.com/user-attachments/assets/4ddd9eb2-12e7-493b-8a71-bf6ba725f5ce" />

<img width="722" alt="Image" src="https://github.com/user-attachments/assets/caaf9c64-b570-418b-99e3-9013cf8a552a" />

### Accurate Credit Assignment with VinePPO
PPO의 term은 그대로 가져가되[^1], step별 value만 MC로 측정. 
step을 얼마 간격으로 할지는 hparm.

<img width="442" alt="Image" src="https://github.com/user-attachments/assets/0e038537-5712-410c-ac1d-237c1b3ad565" />

K는 몇번 샘플링할지인데 1에서도 잘동작[^2]

<img width="387" alt="Image" src="https://github.com/user-attachments/assets/1cee4d59-33eb-4068-a9e9-7cad13f7a85f" />

### Result
- VinePPO와 PPO의 step별 acc
<img width="693" alt="Image" src="https://github.com/user-attachments/assets/407c8430-7623-419a-8ccb-dd27a8a87f88" />

- VinePPO와 PPO의 wallclock별 acc 

<img width="711" alt="Image" src="https://github.com/user-attachments/assets/3dd4242f-ab50-4f9a-b853-18c0da4e36c5" />

vinePPO가 iteration이 더 오래걸리지만 수렴이 더 빠름

- KL diveregence 별 acc

<img width="689" alt="Image" src="https://github.com/user-attachments/assets/adeedc7c-d925-4b19-bec2-3d5269bf857a" />

kl divergence가 낮으면 왜 좋은가 (https://github.com/long8v/PTIR/issues/221 에서도 궁금)
pretrained model의 지식을 잃어버리지 않고 그 지식을 잘 활용하며 성능을 개선 시켰다고 볼 수 있어서 좋게 평가된다고 함 (KL divergence term을 넣는것과 비슷할까)

- temperature tolerance

<img width="255" alt="Image" src="https://github.com/user-attachments/assets/208fd796-d8a7-4763-8023-53ea36811da0" />

https://github.com/long8v/PTIR/issues/221 여기서 sampling trajectory를 뽑는 temperature를 1.2까지 높였는데 보통은 <1로 하는게 practice라고 함
PPO도 보면 1일 때 성능이 낮아짐. 그런데 VinePPO는 그렇지 않다고 하는게 장점.

- Value model의 acc

<img width="710" alt="Image" src="https://github.com/user-attachments/assets/2fe6324e-f8a1-4bc7-88b2-42500d3bef83" />

256 MC를 해서 GT value를 구한게 가로축 세로축이 predicted value인데 PPO는 false positive, false negative가 많은데 VPPO는 gt와 corr이 높았다

<img width="690" alt="Image" src="https://github.com/user-attachments/assets/eaba828d-8849-428b-83fb-6c54f6437660" />

잘못된 trajectory를 내보내는 걸 측정해봤는데 PPO의 경우 reasoning 이 길어질수록 에러가 늘었는데, 이는 특히 초기 일수록 (맨 왼쪽) trajectory가 트레이닝 데이터를 따라서 diversity가 낮고 그래서 value가 memorization을 했었을 수 있다고 설명. 


### Some details

<img width="576" alt="Image" src="https://github.com/user-attachments/assets/730a11bd-9a91-4a07-861b-508785205b29" />

End-of-Sequence (EOS) Trick: As detailed in Appendix A, rewards are only applied at the final token of a response, which corresponds to the EOS token when the response is complete. For responses that exceed the maximum length, we truncate the response to the maximum length and apply the reward to the last token of the truncated sequence

이거 어떻게 한거지 generation은 max length보다 더 길게 한건강


### footnote

[^1]: <img width="697" alt="Image" src="https://github.com/user-attachments/assets/c5b5703c-6ae4-4826-92a5-9f9432adba7a" />
[^2]: <img width="726" alt="Image" src="https://github.com/user-attachments/assets/34614eb0-a5c3-41d8-aaf3-c3d973c5a09b" />