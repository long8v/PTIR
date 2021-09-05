# PTIR
Paper Today I Read 

## 2021-08-20
Vocabulary Learning via Optimal Transport for Neural Machine Translation([arxiv](https://arxiv.org/pdf/2012.15671.pdf))<br>
**problem :** vocabulary를 어떻게 설정하는지에 대해 비교하는 것에 대한 비용이 너무 크며, vocab에 따라 fine-tune 성능이 달라짐 <br>
현재 vocab을 선정하는 기준은 frequency나 entropy기준으로 휴리스틱하게 설정됨<br>
**solution :** 경제학의 Marginal Utility의 개념을 빌려, Marginal Utility of Vocabulary를 정의하여 이를 최대화하는 것을 목표로 함. MUV의 미분값은 vocab수를 늘렸을 때 marginal하게 늘렸을 때 entropy의 차이로 두어 일정 span에서 줄어든 엔트로피가 가장 작은 값에서 MUV가 최대화됨.<br>
**result :** 1) 기존에 사용되던 vocab보다 MT 성능이 좋았음 2) 휴리스틱하게(실험) 선정된 vocab과 성능이 유사하였음 3) 다국어 vocab에서도 더 좋았음<br>

## 2021-09-01
LayoutLM: Pre-training of Text and Layout for Document Image Understanding([arxiv](https://arxiv.org/pdf/1912.13318.pdf))<br>
**problem :** 이전까지 문서 구조를 학습하기 위해 텍스트/이미지 정보만을 활용하였음<br>
**solution :** BERT 아키텍쳐를 활용하여, 좌표, 텍스트로 프리트레이닝하고 바운딩박스내 이미지 정보를 Faster RCNN로 결합하여 finetuning <br>
**result :** information extraction, document classification 등의 태스크에서 SOTA<br>

## 2021-09-03
An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale([arxiv](https://arxiv.org/abs/2010.11929))<br>
**problem :** Transformer 구조를 image 도메인에 적용<br>
**solution :** 이미지를 4 by 4 block으로 나눈 뒤 쭉 핀 임베딩에 positional embedding을 더한 뒤 트랜스포머 인코더 + FCN으로 구성. 이후 `[CLS]`토큰으로 이미지 분류 태스크<br>
**result :** 분류 문제에서 SOTA. 가장 아래 레이어에서도 글로벌한 정보를 사용하고 있음을 알 수 있었음. CNN보다 locality라는 inductive bias가 적음<br>
**further work :** NLP처럼 semi-supervised pretraining은 하지 못함

## 2021-09-04
Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Network([arxiv](https://arxiv.org/abs/1506.01497))<br>
**problem :** Objective Detection에서 사물의 위치를 찾는 Region Proposal단계에서 selective search가 너무 오래걸림<br>
**solution :** CNN + anchor으로 Region Porposal를 한 뒤 이후 ROI pooling과 classifier을 순차적으로 학습시킴. 이때 feature map은 공유하며 둘의 loss는 합하여 multi-task learning 됨<br>
**result :** fast RCNN보다 성능이 개선됬으며 추론속도도 2배 이상 빨라짐<br>

## 2021-09-05
TSDAE: Using Transformer-based Sequential Denoising Auto-Encoder for Unsupevised Sentence Embedding Learning([arxiv](https://arxiv.org/abs/2104.06979))<br>
**problem :** STS<br>
**solution :** auto-encoder처럼 encoder가 노이즈가 있는 텍스트를 받아 저차원의 벡터로 표현하면 이를 decoder가 noise가 없는 텍스트로 변화하는 구조를 가짐<br>k 층의 self-attention을 하고 Query와 Value는 문장임베딩, Key는 이전 (k-1)층의 t시점 디코더 히든스텝을 사용함 (BART와 다르게 모든 time-step의 히든벡터가 참조 되지 않음) <br>
**result :** unsupervised sentence embedding 방법론인 MLM, GloVe, Sent2Vec과 비교했을 때 성능상 우위
