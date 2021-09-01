# PTIR
Paper Today I Read 

**2021-08-20**
Vocabulary Learning via Optimal Transport for Neural Machine Translation([arxiv](https://arxiv.org/pdf/2012.15671.pdf))
**problem :** vocabulary를 어떻게 설정하는지에 대해 비교하는 것에 대한 비용이 너무 크며, vocab에 따라 fine-tune 성능이 달라짐 
현재 vocab을 선정하는 기준은 frequency나 entropy기준으로 휴리스틱하게 설정됨
**solution :** 경제학의 Marginal Utility의 개념을 빌려, Marginal Utility of Vocabulary를 정의하여 이를 최대화하는 것을 목표로 함. MUV의 미분값은 vocab수를 늘렸을 때 marginal하게 늘렸을 때 entropy의 차이로 두어 일정 span에서 줄어든 엔트로피가 가장 작은 값에서 MUV가 최대화됨.
**result :** 1) 기존에 사용되던 vocab보다 MT 성능이 좋았음 2) 휴리스틱하게(실험) 선정된 vocab과 성능이 유사하였음 3) 다국어 vocab에서도 더 좋았음

**2021-09-01**
LayoutLM: Pre-training of Text and Layout for Document Image Understanding([arxiv](https://arxiv.org/pdf/1912.13318.pdf))
**problem :** 이전까지 문서 구조를 학습하기 위해 텍스트/이미지 정보만을 활용하였음
**solution :** BERT 아키텍쳐를 활용하여, 좌표, 텍스트로 프리트레이닝하고 바운딩박스내 이미지 정보를 Faster RCNN로 결합하여 finetuning 
**result :** information extraction, document classification 등의 태스크에서 SOTA
