# PTIR
Paper Today I Read(13 papers)

## 2021-MM-DD
paper([arxiv](aa.pdf))<br>
**problem :**<br>
**solution :**<br>
**result :**<br>
**details :** [notion](www)<br>

## 2021-12-02
Donut : Document Understanding Transformer without OCR([arxiv](https://arxiv.org/pdf/2111.15664.pdf))<br>
**problem :** 기존 사진 기반의 문서를 이해하는 태스크들의 접근 방식들은 OCR을 한번 거침으로서 계산 비용이 크고 OCR 에러로 인해 생겨나는 성능 저하문제가 있음.<br>
**solution :** Swin Transformer 인코더 + BART 디코더로 이미지를 읽고 바로 json으로 포매팅 가능한 토큰을 내뱉도록 함. 이때 프리트레이닝은 가상의 문서 데이터를 만들고 문서 내 글자를 모두 읽는 것을 통해 진행함.<br>
**result :** 문서분류 : OCR 없는 모델 중에서 SOTA, OCR 기반의 프리트레이닝 모델인 LayoutLM의 성능에 근접하지만 모델 크기와 속도 면에서 우위. 파싱에서 SOTA.  <br>
**details :** [notion](https://long8v.notion.site/Donut-fbaf0e9e19624ae492108f1249a47aa1)<br>

## 2021-12-01
Empirical Analysis of Unlabeled Entity Problem in Named Entity Recognition([arxiv](https://openreview.net/pdf?id=5jRVa89sZk))<br>
**problem :** NER 문제에서 실수 혹은 복잡성 때문에 unlabeld된 entity들은 positive sample을 줄여 성능을 악회시키기도 하지만 이는 BERT와 같은 PLM으로 해결 가능한 반면에, negative sample로 사용됨에 따라 발생하는 성능 악화는 해결하기 어려움<br>
**solution :** label된 span에 대한 cross entropy loss + unlabel된 span에 대해 랜덤으로 샘플링하여 cross-entropy loss를 구함<br>
**result :** 가상의 데이터(일부러 labled entity 일부를 빼먹음)에서는 해당 문제를 다 해결, 잘 annotate된 데이터에서는 SOTA에 거의 근접, real-world data는 SOTA<br>

## 2021-11-30
Incorporating Copying Mechanism in Sequence-to-Sequence Learning([arxiv](https://arxiv.org/pdf/1603.06393.pdf))<br>
**problem :** Seq2Seq에서 source에 있는 토큰임에도 사전에 존재하지 않는 단어라면 OOV 문제로 예측할 수가 없음<br>
**solution :** 일반적으로 Seq2Seq에서 decoder가 다음 토큰을 generate하는 mode외에 source에서 토큰을 가져오는 copy mode를 정의하고, 각 mode에서 나온 확률값을 합하여 NLL으로 구함<br>
**result :** 요약 태스크에서 기존 RNN Seq2Seq보다 성능 우위<br>
**details :** [notion](https://long8v.notion.site/CopyNet-64e60ff497cb46eb9f1e99e0c6bddaa9)<br>

## 2021-11-29
Cost-effective End-to-end Information Extraction for Semi-structured Document Images([arxiv](https://arxiv.org/pdf/2104.08041.pdf))<br>
**problem :** Information Extraction을 하기 위한 기존 서브태스크를 연결한 pipeline의 방법론의 경우 유지보수가 많이 들고, 모델 학습시에도 각 서브 태스크들에 대한 토큰별 annotation이 필요하여 비용이 많이 듦<br>
**solution :** 2D Transformer 구조 + decoder에 copying mechanism을 붙여서 tree 구조(abstract syntax trees)를 generate하는 end2end 모델 <br>
**result :** 기존 pipeline 방법론보다 더 적은 비용, 동일한 양의 데이터로 더 좋은 결과<br>
**details :** [notion](https://long8v.notion.site/WYVERN-07583648be9c4620a7c13924b8ed7f4a)

## 2021-11-26
SQLova: A Comprehensive Exploration on WikiSQL with Table-Aware Word Contextualization([arxiv](https://arxiv.org/pdf/1902.01069.pdf))<br>
**problem :** 자연어를 SQL로 변환하는 task(NL2SQL)에서의 BERT 적용. 이때, 통상적 seq2seq를 통한 언어생성은 syntax가 없어 NL2SQL 문제에 적합하지 않음.<br>
**solution :** 자연어 질문과 테이블의 컬럼들을 `[SEP]`토큰으로 concat하여 BERT에 넣음. 마지막 BERT의 두개 layer에 biLSTM 적용하여 쿼리에 들어가는 요소들(select문에 들어가는 컬럼 등)을 예측하는 6가지의 모듈들에 대한 연산 진행. <br>
**result :** SOTA, 크라우드 소싱 분석 결과 human performacne보다 우위.<br>
**details :** [notion](https://long8v.notion.site/SQLova-6e14c9fecc5a420b9394288b14a463f4)

## 2021-11-25
SPADE: Spatial Dependency Parsing for Semi-Structured Document Information Extraction([arxiv](https://arxiv.org/pdf/2005.00642.pdf))<br>
**problem :** Information Extraction 문제를 풀 때에 한 문장으로 펼친 뒤(serialize), 여기서 NER 문제를 풀어왔으나 해당 방법론으로는 복잡한 공간적 관계, 문서의 구조적 정보를 다룰 수 없다는 문제가 있음 <br>
**solution :** serialize 단계 없이 각 토큰들과 field를 노드로 두고 그 관계를 엣지로 하는 그래프(=관계가 있으면 1, 없으면 0인 binary matrix로 표현됨)인 를 만드는 것을 목표로 함. 각 노드들은 attention 연산을 통해서 encoding 되고 엣지들은 인코딩된 벡터들의 내적을 통해 확률 값을 가짐.<br>
**result :** BERT base NER과 비슷하거나 나은 성능<br>
**details :** [notion](https://long8v.notion.site/SPADE-6018bae80a514fc5b75a962fc69e39fd)

## 2021-09-14 
Swin Transformer: Hiearchical Vision Transformer using Shifted Window([arxiv](https://arxiv.org/abs/2103.14030))<br>
**problem :** ViT와 같이 비전에 트랜스포머를 적용하고자 하는 시도가 있으나, 한개의 토큰 단위를 16 by 16로 고정하는 것은 pixel 단위인 semantic segmentation을 하기엔 적합하지 않으며 고화질 데이터의 경우 이미지 크기에 제곱으로 연산의 양이 많아져서 사용에 한계가 있음 <br>
**solution :** ViT처럼 m by m 패치로 자른 뒤에 그 내부의 픽셀 단위로 slef-attention을 함. 이후에 패치를 M // 2만큼 shift 해서 self-attention을 함. 이 구조를 반복하여 프리트레이닝/파인튜닝을 진행함 <br>
**result :** ViT와 달리 연산량이 이미지 크기의 선형적으로 증가하면서도 classification, detection, segmentation에서 SOTA <br>

## 2021-09-05 
TSDAE: Using Transformer-based Sequential Denoising Auto-Encoder for Unsupevised Sentence Embedding Learning([arxiv](https://arxiv.org/abs/2104.06979))<br>
**problem :** STS 데이터셋을 얻는 것은 어려우며, finetuning 시에 텍스트 도메인의 차이 때문에 STS의 성능이 finetuning의 성능에 반드시 비례하는 것은 아님<br>
**solution :** auto-encoder처럼 encoder가 노이즈가 있는 텍스트를 받아 저차원의 벡터로 표현하면 이를 decoder가 noise가 없는 텍스트로 변화하는 구조를 가짐<br>k 층의 self-attention을 하고 Query와 Value는 문장임베딩, Key는 이전 (k-1)층의 t시점 디코더 히든스텝을 사용함 (BART와 다르게 인코더의 모든 time-step의 히든벡터가 참조 되지 않음) <br>
**result :** unsupervised sentence embedding 방법론인 MLM, GloVe, Sent2Vec과 비교했을 때 성능상 우위

## 2021-09-04 
Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Network([arxiv](https://arxiv.org/abs/1506.01497))<br>
**problem :** Objective Detection에서 사물의 위치를 찾는 Region Proposal단계에서 selective search가 너무 오래걸림<br>
**solution :** CNN + anchor으로 Region Porposal를 한 뒤 이후 ROI pooling과 classifier을 순차적으로 학습시킴. 이때 feature map은 공유하며 둘의 loss는 합하여 multi-task learning 됨<br>
**result :** fast RCNN보다 성능이 개선됬으며 추론속도도 2배 이상 빨라짐<br>

## 2021-09-03 
An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale ([arxiv](https://arxiv.org/abs/2010.11929))<br>
**problem :** Transformer 구조를 image 도메인에 적용<br>
**solution :** 이미지를 16 by 16 block으로 나눈 뒤 쭉 핀 임베딩에 positional embedding을 더한 뒤 트랜스포머 인코더 + FCN으로 구성. 이후 `[CLS]`토큰으로 이미지 분류 태스크<br>
**result :** 분류 문제에서 SOTA. 가장 아래 레이어에서도 글로벌한 정보를 사용하고 있음을 알 수 있었음. CNN보다 locality라는 inductive bias가 적음<br>
**further work :** NLP처럼 semi-supervised pretraining은 하지 못함

## 2021-09-01 
LayoutLM: Pre-training of Text and Layout for Document Image Understanding([arxiv](https://arxiv.org/pdf/1912.13318.pdf))<br>
**problem :** 이전까지 문서 구조를 학습하기 위해 텍스트/이미지 정보만을 활용하였음<br>
**solution :** BERT 아키텍쳐를 활용하여, 좌표, 텍스트를 임베딩하여 MLM, MDC(문서분류)로 프리트레이닝하고 바운딩박스내 이미지 정보를 Faster RCNN에서 feature를 뽑아 결합하여 finetuning <br>
**result :** information extraction, document classification 등의 태스크에서 SOTA<br>

## 2021-08-30 
BART: Denoising Sequence-to-Sequence Pre-training for Natural Language Generation, Translation, and Comprehension([arxiv](https://arxiv.org/abs/1910.13461))<br>
**problem :** BERT는 트랜스포머의 인코더만 사용, GPT는 디코더만 사용. 두 모델의 일반화된 모델을 만들고 싶음 <br>
**solution :** 트랜스포머의 encoder-decoder 구조를 모두 사용하여 noise가 들어간 텍스트를 원래 텍스트로 원복하면서 pre-training됨. fine-tuning시에는 input과 ouput에 sdame input을 넣은 뒤 decoder에 마지막 ouput에 fcn을 넣어서 사용함<br>
**result :** MNLI를 제외하고 모든 GLUE  task에서 BERT보다 우위

## 2021-08-20 
Vocabulary Learning via Optimal Transport for Neural Machine Translation([arxiv](https://arxiv.org/pdf/2012.15671.pdf))<br>
**problem :** vocabulary를 어떻게 설정하는지에 대해 비교하는 것에 대한 비용이 너무 크며, vocab에 따라 fine-tune 성능이 달라짐 <br>
현재 vocab을 선정하는 기준은 frequency나 entropy기준으로 휴리스틱하게 설정됨<br>
**solution :** 경제학의 Marginal Utility의 개념을 빌려, Marginal Utility of Vocabulary를 정의하여 이를 최대화하는 것을 목표로 함. MUV의 미분값은 vocab수를 늘렸을 때 marginal하게 늘렸을 때 entropy의 차이로 두어 일정 span에서 줄어든 엔트로피가 가장 작은 값에서 MUV가 최대화됨.<br>
**result :** 1) 기존에 사용되던 vocab보다 MT 성능이 좋았음 2) 휴리스틱하게(실험) 선정된 vocab과 성능이 유사하였음 3) 다국어 vocab에서도 더 좋았음<br>
