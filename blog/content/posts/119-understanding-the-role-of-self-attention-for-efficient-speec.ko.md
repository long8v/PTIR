---
title: "[110] Understanding the Role of Self Attention for Efficient Speech Recognition"
date: 2023-04-17
tags: ['2022Q1', 'ICLR', '25min', 'transformer']
paper: "https://openreview.net/pdf?id=AvcfxqRy4Y"
issue: 119
issueUrl: "https://github.com/long8v/PTIR/issues/119"
---
<img width="824" alt="image" src="https://user-images.githubusercontent.com/46675408/232624306-a8454f82-92a0-4e9e-a80b-cb5e9cadbd26.png">

[paper](https://openreview.net/pdf?id=AvcfxqRy4Y)

## TL;DR
- **I read this because.. :** 논문 모임에 발제됨. SA의 특성 분석이라 재밌어 보이넹~
- **task :** ASR
- **problem :** ASR에 transformer가 사용되나 self-attention이 어떤 특성을 가지고 있는지는 분석된 바가 없음
- **idea :** diagonality를 측정하는 measure를 측정하여 레이어 별로 비교 / 비슷한 음소끼리 attend 하는 경향 관찰 / 레이어별 phoneme 분류 태스크 -> attention map 재사용할 수 있을듯  
- **architecture :** Conformer-M + attention map reuse
- **objective :** CTC loss
- **baseline :** Conformer-M w/o reuse
- **data :** LibriSpeech
- **evaluation :** 
- **result :** 1.96 times of speedup in inference and 33% reduced training time
- **contribution :** ASR 분야에서 SA 최초로 분석! 이 분석 방법론으로 다른 도메인에도 적용이 가능하려나? 
- **limitation / things I cannot understand :** 아키텍쳐에 대한 자세한 내용은 모름

## Details

<img width="666" alt="image" src="https://user-images.githubusercontent.com/46675408/232624567-98d7d7fa-e140-4872-9fcf-2ae31529acc5.png">


- cumulative attention diagonality
<img width="543" alt="image" src="https://user-images.githubusercontent.com/46675408/232624748-0182221a-d459-47e6-803b-ddc13d188896.png">


<img width="682" alt="image" src="https://user-images.githubusercontent.com/46675408/232624601-eab77e7d-29d0-449b-991f-088a62d1d64d.png">

audio-to-text transition을 할 때 근처에 있는 (neighbor) 것들에 attend하는 경향이 있다. -> neighbor에 많이 attend하면 diagonality가 커짐
근데 upper layers에서 diagnolatiy가 처치므로 위의 레이어에서 linguistic을 보고 있음을 알 수 있다

그러면 밑에 layer들은 뭘 담당하냐면 Phoneme을 담당하는데 이건 아래 두개 그림을 보면 알 수 있다
<img width="698" alt="image" src="https://user-images.githubusercontent.com/46675408/232625482-433bdd15-98cd-419d-9469-1cea0076da58.png">

음소 단위로 attention map을 봤는데 비슷한 발음끼리 attend하는 경향이 위의 레이어에서는 안나타남

(음소단위로 attention map 측정하는 수식
<img width="527" alt="image" src="https://user-images.githubusercontent.com/46675408/232626282-1db577b0-df83-4176-851c-3341733ad7d5.png"> )

<img width="871" alt="image" src="https://user-images.githubusercontent.com/46675408/232625386-1b94bc1e-5945-49ea-b78e-11b7d8bcd624.png">

아래 레이어들이 Phoneme classification를 더 잘함. 위의 레이어 가서 성능이 안좋아짐.

이러한 발견들을 기반으로 SA를 재사용하는 아키텍쳐를 제안한다. 
<img width="714" alt="image" src="https://user-images.githubusercontent.com/46675408/232625570-2dd562c1-824c-45ac-847f-7503c45de245.png">

attention map reuse는 여기서 처음 제안된건 아니고 NLP 쪽에는 있었는데 왜 재사용되는지는 분석을 안했다. 근데 이 논문에서는 분석했으니 의미가 있다. 

<img width="969" alt="image" src="https://user-images.githubusercontent.com/46675408/232772635-96d856d4-3c64-4614-8402-72e50b3b3cb2.png">

V만 레이어별로 새로 project되는 꼴
Sharing Attention Weights for Fast Transformer

https://arxiv.org/pdf/1906.11024.pdf

c.f. ConFormer 
conv + SA + conv
<img width="463" alt="image" src="https://user-images.githubusercontent.com/46675408/232773068-ba22c881-892b-4534-8b09-8c89a527112e.png">

