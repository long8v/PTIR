---
title: "[12] BBPE: Neural Machine Translation with Byte-Level Subwords"
date: 2022-02-18
tags: ['NLP', '2019', 'tokenizing', 'facebook', 'AAAI']
paper: "https://arxiv.org/pdf/1909.03341.pdf"
issue: 12
issueUrl: "https://github.com/long8v/PTIR/issues/12"
---
<img width="698" alt="image" src="https://user-images.githubusercontent.com/46675408/154601678-8904d7b3-9b89-4b24-b564-916177b61374.png">

[paper](https://arxiv.org/pdf/1909.03341.pdf)
**problem :** multi-lingual 셋팅에서 BPE를 하면, 잘 나오지 않는 캐릭터들 때문에 vocab수를 잡아먹는다. 중국어의 경우에는 글자가 다른 글자의 일부인 경우도 있는데(虫, 蟲), 캐릭터 레벨에서는 이러한 관계를 알기 어렵다.
**solution :** 글자들을 'utf-8'로 인코딩한 뒤에 BPE를 적용하자.
**result :** 1) 더 적은 파라미터로 BPE와 비슷한 성능 2) BPE보다 더 짧은 sequence length을 만들어 train / inference 속도에도 용이 3) transfer learning에 용이(OOV문제를 해결) 
**details :** 
- multi-lingual을 할 때, 중국어나 일본어에서 잘 나오지 않는 캐릭터들 때문에 vocab수를 잡아먹음.
```
>>> '蟲'.encode('utf-8')
b'\xe8\x9f\xb2'
>>> '虫'.encode('utf-8')
b'\xe8\x99\xab'
```
```
>>> '안'.encode('utf-8')
b'\xec\x95\x88'
>>> '않'.encode('utf-8')
b'\xec\x95\x8a'
```
- utf-8 인코딩을 한 뒤, n-gram을 통한 BPE vocab set을 만듦 
- encoding은 transformer를 사용함
- decoder는 encoder에 비해 BBPE를 적용하기가 어려운데, 모든 캐릭터는 byte sequence로 표현할 수 있지만, 반대의 경우에는 invalid한 byte sequence가 나올 수 있기 때문이다. 학습된 모델에서 이러한 현상은 거의 발생하지 않았다.
  - 학습 중간에는 불필요하게 byte를 반복하는 현상이 있었는데, 우리는 이러한 error pattern을 최대한 많은 character로 원복하는 시스템을 만들었다.
- 여러 MT 데이터셋으로 학습했고, beam search 4 사용, 평가로는 tokenized BLEU([sacreBLEU](https://github.com/mjpost/sacrebleu))를 사용했다.
- Symbol Frequency Distribution : 가로가 symbol, 세로가 frequency. BBPE가 frequency에서 더 consistent한 distribution을 가짐.
<img width="1071" alt="image" src="https://user-images.githubusercontent.com/46675408/154605740-975e9f91-30c6-4ccb-b550-9aee4ea389b2.png">

- Cross-Lingual Sharing : 다른 언어 사이에서도 writing 하는 방법이 다르지만 같은 symbol을 공유하는 경우가 생김.
<img width="558" alt="image" src="https://user-images.githubusercontent.com/46675408/154606441-84b25d7a-8a6b-4db3-a68c-e2bd9e88dd28.png">

- Impact on Sequence Length : BPE와 달리 BBPE는 단위가 짧기 때문에, sequence가 길어지고 이에 따라 train, inference가 더 오래 걸린다. 하지만 BPE와 마찬가지로 압축을 하기 때문에, BPE보다 더 짧은 시퀀스를 가질 수 있다. (X-En의 경우 1/5)
- BBPE on Nosiy Character Set : En-De에서는 nosiy 한 문장이 몇개 있었는데, En-De 모두 30개의 알파벳으로 이루어져있기 때문에 더 낭비가 심했다. BBPE를 통해 2K, 4K로 만들었을 때 BPE 32K로 만든것과 모델 크기는 작지만 비슷한 성능을 내는 것을 확인했다.
<img width="427" alt="image" src="https://user-images.githubusercontent.com/46675408/154608469-59ee8cc4-bdd2-40f3-bd69-2454be3336ad.png">

- BBPE on Character-Rich Languages
중국어나 일본어 같은 경우에 50K의 글자를 가지고 있지만 일부분만 많이 사용된다. Ja-En 데이터셋에서 7.9K의 캐릭터 중에 2.4K의 캐릭터가 빈도의 99.99%를 차지했다. BBPE로 전체 캐릭터의 반인 4K를 사용했다. 이때 BPE 16K를 사용한 것과 성능이 유사했으며, big model에서는 더 좋은 성능을 보였다. 
<img width="546" alt="image" src="https://user-images.githubusercontent.com/46675408/154608950-a428f827-6d8b-4323-ac12-d048e15230e1.png">

- BBPE on Many-to-En Translation
multilingual setting에서 BBPE는 BPE보다 파라미터를 적게 쓰면서 성능을 개선했다. 이는 BBPE가 sequence length가 더 짧기 때문일 수도 있지만, 어쨌든 성능과 속도가 더 좋기 때문에 괜찮다 ^^ 
<img width="1032" alt="image" src="https://user-images.githubusercontent.com/46675408/154609130-f9e77b8a-0190-4638-9ae8-5ce1bd965e3d.png">

- Transfer Learning on Unseen Characters
BBPE는 모든 utf-8 bytes를 가지고 있고, OOV token이 없기 때문에, BBPE 모델은 다른 언어로 transfer가 가능하다. 반면에 character-based vocab은 새로운 character가 추가되면 vocab을 바꾸고 처음부터 다시 학습해야한다. X-En에 없는 캐릭터 셋인 Si(Sinhala)-En 데이터로 BBPE 모델로 transfer-learning을 한 것은 (심지어 공유하는 char 없는데도) baseline 보다 성능이 좋았다. 
<img width="509" alt="image" src="https://user-images.githubusercontent.com/46675408/154609805-753cb57f-6daf-4136-b43d-48780eff720d.png">