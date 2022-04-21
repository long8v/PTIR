[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Flong8v%2FPTIR&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false)](https://hits.seeyoufarm.com) 
# 📚 Paper Today I Read 📓
- 21년도까지 `readme.md` + `notion`, 22년부터 [issue](https://github.com/long8v/PTIR/issues)로 관리
- 22년도 목표는 100개! 현재  <img alt="issues" src="https://img.shields.io/github/issues/long8v/PTIR?color=0088ff"> 개

## 2021년에 읽은 논문들 (28 papers)
  * [2021-12-31 DeiT](#2021-12-31-deit)
  * [2021-12-30 LeViT](#2021-12-30-levit)
  * [2021-12-28 Frozen](#2021-12-28-frozen)
  * [2021-12-27 DETR](#2021-12-27-detr)
  * [2021-12-23 Pix2seq](#2021-12-23-pix2seq)
  * [2021-12-21 Swin](#2021-12-21-swin)
  * [2021-12-20 SimpleDLM](#2021-12-20-simpledlm)
  * [2021-12-17 METER](#2021-12-17-meter)
  * [2021-12-16 Gated MoE](#2021-12-16-gated-moe)
  * [2021-12-15 GLaM](#2021-12-15-glam)
  * [2021-12-14 PVT](#2021-12-14-pvt)
  * [2021-12-13 MixText](#2021-12-13-mixtext)
  * [2021-12-09 Linformer](#2021-12-09-linformer)
  * [2021-12-07 T5](#2021-12-07-t5)
  * [2021-12-06 StructuralLM](#2021-12-06-structurallm)
  * [2021-12-03 BROS](#2021-12-03-bros)
  * [2021-12-02 Donut](#2021-12-02-donut)
  * [2021-12-01](#2021-12-01)
  * [2021-11-30 Copying Network](#2021-11-30-copying-network)
  * [2021-11-29 SPADE](#2021-11-29-spade)
  * [2021-11-26 SQLova](#2021-11-26-sqlova)
  * [2021-11-25 SPADE](#2021-11-25-spade)
  * [2021-09-05 TSDAE](#2021-09-05-tsdae)
  * [2021-09-04 Faster R-CNN](#2021-09-04-faster-r-cnn)
  * [2021-09-03 ViT](#2021-09-03-vit)
  * [2021-09-01 LayoutLM](#2021-09-01-layoutlm)
  * [2021-08-30 BART](#2021-08-30-bart)
  * [2021-08-20](#2021-08-20)

## 2021-12-31 DeiT
Training data-efficient image transformers & distillation through attention, 2021([arxiv](https://arxiv.org/abs/2012.12877))<br>
**problem :** ViT는 대규모 이미지 데이터셋으로 학습해야 일반화 가능한 모델을 학습할 수 있음<br>
**solution :** ViT구조에 distillation token을 추가하여 CNN 등의 teacher model을 사용하여 distillation 학습을 진행함<br>
**result :** imageNet만으로 학습한 모델이 좋은 정확도를 냄, ViT, ResNet와 비교해봤을 때 더 작은 파라미터로 나은 성능<br>
**details :** [notion](https://long8v.notion.site/DeiT-a045232cb9f4468e9b90e6a3efda8625)

## 2021-12-30 LeViT
LeViT: a Vision Transformer in ConvNet's Clothing for Faster Inference, 2021([arxiv](https://arxiv.org/pdf/2104.01136.pdf))<br>
**problem :** 더 나은 속도/성능 trade-off를 가지는 ViT를 개발해보자<br>
**solution :** 처음에 CNN으로 resolution을 줄인 뒤, 트랜스포머를 위에 붙임. 이때, 우리는 CNN처럼 pyramid 구조를 갖기 위해 중간에 Query를 average-pooling으로 sub-sampling을 하여 resolution을 중간중간에 줄여감. 외에 MLP 대신 1 x 1 convolution을 하고, positional embedding 대신 attention bias를 추가하는 등 효율적인 연산을 위한 디테일을 수정함.<br>
**result :** DeiT나 EfficientNet과 유사한 성능으로 더 빠른 인퍼런스 속도.<br>
**details :** [notion](https://long8v.notion.site/LeViT-8dfba651c7e54430992ee79b2e3429c6)<br>

## 2021-12-28 Frozen
Multimodal Few-Shot Learning with Frozen Language Models, 2021([arxiv](https://papers.nips.cc/paper/2021/file/01b7575c38dac42f3cfb7d500438b875-Paper.pdf))<br>
**problem :** 대형 언어모델에게 visual 정보를 few-shot으로 학습할 수 있게 해보자<br>
**solution :** visual encoder를 prefix처럼 input 시퀀스 앞에 두고 기존 언어모델의 파라미터는 frozen 시키고 학습시킴. <br>
**result :** few-shot으로도 상당한 성능, 멀티모달 few shot 러닝 밴치마크를 제안<br>
**details :** [notion](https://long8v.notion.site/Frozen-405d8913a0ea4779a503e8f61e21d835)<br>

## 2021-12-27 DETR
End-to-End Object Detection with Transformers, 2020([arxiv](https://arxiv.org/pdf/2005.12872.pdf))<br>
**problem :** object detection 문제를 풀기 위해선 수작업 구조/설계가 필요함<br>
**solution :** object detection이 중복이 없는 순서 상관 없는 set을 예측하는 것이기 때문에, CNN + transformer encoder-decoder + FFN으로 한번에 bbox를 예측할 수 있도록 함. 이 때, loss는 우선 예측된 box와 gt box를 bipartite로 최적 matching을 구한 뒤, 최적 매칭에서 box loss와 클래스 레이블을 합친 loss를 사용함.<br>
**result :** FASTER RCNN과 유사한 성능, panoptic segmentation에서 SOTA<br>
**details :** [notion](https://long8v.notion.site/DETR-5810bf27ec954498a3bdd95c15b116b7)<br>

## 2021-12-23 Pix2seq
Pix2seq: A Language Modeling Framework for Object Detection, 2021([arxiv](https://arxiv.org/pdf/2109.10852.pdf))<br>
**problem :** Object Detection 문제를 풀기 위해선 특수한 구조/설계가 필요함<br>
**solution :** object detection 문제를 이미지를 넣었을 때 바운딩 박스와 레이블을 표현한 토큰 sequence를 뽑는 인코더-디코더 구조로 바꿈. 이때 모든 object를 찾지 않고 끝나버리는 것을 막기 위해 noise를 섞은 augmentation을 추가하여 모델이 noise인지 아닌지를 구분하도록 하면서 고정된 길이로 예측하도록 함. 이를 통해 recall을 끌어올림. <br>
**result :** Faster RCNN, DETR과 같은 디텍션만을 위해 설계되었고 최적화된 모델들과 성능이 유사하게 남<br>
**details :** [notion](https://long8v.notion.site/pix2seq-109e93c7ebb54104bbca96f16ddc4127)<br>

## 2021-12-21 Swin
Swin Transformer: Hiearchical Vision Transformer using Shifted Window, 2021([arxiv](https://arxiv.org/abs/2103.14030))<br>
**problem :** ViT와 같이 비전에 트랜스포머를 적용하고자 하는 시도가 있으나, 한개의 토큰 단위를 16 by 16로 고정하는 것은 pixel 단위인 semantic segmentation을 하기엔 적합하지 않으며 고화질 데이터의 경우 이미지 크기에 제곱으로 연산의 양이 많아져서 사용에 한계가 있음 <br>
**solution :** ViT처럼 m by m 패치로 자른 뒤에 그 내부의 픽셀 단위로 self-attention을 함. 그 뒤에 패치를 M // 2만큼 shift 해서 패치를 나눈 뒤 self-attention을 함. 이 구조를 반복하여 프리트레이닝/파인튜닝을 진행함 <br>
**result :** ViT와 달리 연산량이 이미지 크기의 선형적으로 증가하면서도 classification, detection, segmentation에서 SOTA <br>
**details :** [notion](https://long8v.notion.site/Swin-Transformer-99285aee1ff14e3ab5411c3427c50311)<br>

## 2021-12-20 SimpleDLM
Value Retrieval with Arbitrary Queries for Form-like Documents, 2021([arxiv](https://arxiv.org/abs/2112.07820))<br>
**problem :** 문서에서 원하는 정보를 뽑는 태스크에서 이전 방법론들은 미리 정의해놓은 field를 예측하는 문제를 풀었는데, 이는 다른 form 혹은 도메인에 적용하기 어렵다<br>
**solution :** 쿼리가 주어졌을 때 문서에서 원하는 value를 찾는 문제로 바꿈. 쿼리와 OCR 텍스트를 같은 임베딩을 거친 뒤 같이 self-attention을 하도록 하고 각각의 마지막 셀프어텐션 레이어에 average-pooling, FCN을 거친 뒤 내적을 하여 각 토큰이 원하는 value인지 아닌지 이진 분류하는 문제로 바꿈. 해당 아키텍쳐로 MLM을 하는 프리트레이닝 모델(simpleDLM)을 만듦.<br>
**result :** BERT, LayoutLM 프리트레이닝을 가져온 것보다 simpleDLM으로 프리트레이닝한 것이 F1 성능이 우위. <br>
**details :** [notion](https://long8v.notion.site/simpleDLM-7c1edd8680584952a5c4a2dd2794cbfb)<br>

## 2021-12-17 METER
An Empirical Study of Training End-to-End Vision-and-Language Transformers, 2021([arxiv](https://arxiv.org/pdf/2111.02387.pdf))<br>
**problem :** Vison-and-Language(VL) 태스크에 대해서 end-to-end 방식으로 트랜스포머만 사용한 모델 중 region-based model보다 나은 성능을 보인 것이 없었고, 각 모듈들에 대한 실험이 부족함<br>
**solution :** VL의 주요 모듈들에 대해 알아보고 Ablation study함 <br>
**result :** VQA 태스크에서 SOTA, 실험을 통해 몇가지 모듈들에 대한 성능 우위를 알아냄<br>
**details :** [notion](https://long8v.notion.site/METER-b9b1beb61f194ea5ba6d573b16328ead)<br>

## 2021-12-16 Gated MoE
Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer, 2017([arxiv](https://arxiv.org/pdf/1701.06538.pdf))<br>
**problem :** 큰 모델을 만들면 성능이 늘어나지만 메모리의 이슈로 한계가 있음<br>
**solution :** 각 독립적인 NN인 expert들을 만들고, 인풋에 따라 어떤 expert를 선택할지 gating 네트워크를 구성. 이때 top k개만 선택하도록 하여 sparse한 gating을 각 expert의 outputr과 weighted sum하여 <br>
**result :** 더 낮은 비용으로 더 큰 모델 학습. MT에서 SOTA<br>
**details :** [notion](https://long8v.notion.site/gated-MoE-ff42470ad545417795e82ea54fefbf3b)<br>

## 2021-12-15 GLaM
GLaM: Efficient Scaling of Language Models with Mixture-of-Experts([arxiv](https://arxiv.org/pdf/2112.06905.pdf))<br>
**problem :** NLP에서 큰 프리트레이닝 모델은 좋은 성능을 보이지만, 학습/추론 비용이 너무 크다<br>
**solution :** Mixture-of-Experts 모델에서 따와 트랜스포머 구조 내에 주어진 토큰을 처리하기에 어떤 expert가 가장 적합한지를 학습하는 gating을 만들고 선정된 expert의 output의 합으로 모델의 output을 내뱉음<br>
**result :** GPT-3보다 크기가 7배 크지만, 에너지는 1/3배 쓰이며 zero-shot, one-shot에서 GPT-3보다 성능 우위<br>
**details :** [notion](https://long8v.notion.site/GLaM-051d25d6164b4d4bb4f6191beeeba81b)<br>

## 2021-12-14 PVT
Pyramid Vision Transformer: A Versatile Backbone for Dense Prediction without Convolutions([arxiv](https://arxiv.org/pdf/2102.12122.pdf))<br>
**problem :** 비전 트랜스포머 분야에서 이전에 제시된 ViT는 연산량이 많고 아웃풋이 저차원이어서 픽셀 레벨의 태스크를 하기에 적절하지 않음<br>
**solution :** 1) Feature Pyramid : CNN처럼 4단계의 레이어를 쌓아서 각 크기의 피쳐를 모두 사용할 수 있게 함. 2) Spatial Reduction Attention(SRA) : Self-Attention 연산에서 Key와 Value를 reshape + FC를 거쳐 차원을 줄인 뒤에 진행함<br>
**result :** 이미지 분류 뿐 아니라 디텍션/세그멘테이션 같은 dense prediction 태스크에도 바로 적용 가능하며, SRA를 통해 계싼 비용도 줄임. 다양한 다운스트림 태스크에서 SOTA<br>
**details :** [notion](https://long8v.notion.site/PVT-6403ee04d45c4732a02f65c7924f1f08)<br>

## 2021-12-13 MixText
MixText: Linguistically-Informed Interpolation of Hidden Space for Semi-Supervised Text Classification([arxiv](https://aclanthology.org/2020.acl-main.194.pdf))<br>
**problem :** 기존의 semi-supervised 방법론들은 label 데이터와 unlabeled 데이터가 따로 사용되어, unlabeled 데이터에서 파인튜닝 시 여전히 과적합될 가능성이 많음<br>
**solution :** 비전에서 사용되는 mixup 기법과 유사하게, BERT 등의 프리트레인 모델에 임의의 두 개의 x의 hidden vector를 보간하고 y역시 보간하여 학습데이터로 레이블 데이터와 함께 사용. KL divergence loss에 unlabeled data에 대해 더 자신있게 예측할 수 있도록 분류 엔트로피 로스를 합하여 loss로 사용<br>
**result :** 텍스트 분류 문제에서 제한된 레이블 데이터를 가지고 있을 때 SOTA<br>
**details :** [notion](https://long8v.notion.site/MixText-c91fca74f6bb46fe9ef0aa8868fc5bd4)<br>

## 2021-12-09 Linformer
Linformer: Self-Attention with Linear Complexity([arxiv](https://arxiv.org/abs/2006.04768))<br>
**problem :** Transformer의 self-attention 연산이 시퀀스 길이 n에 대하여 O(n^2)로 시간, 공간복잡도가 늘어남. <br>
**solution :** self-attention layer의 결과 matrix가 low-rank라는 것을 밝혀냄. 즉, 저차원으로 표현할 수 있으므로 linear projection 레이어를 추가하여 key, value의 차원을 줄인 뒤 연산을 진행함.<br>
**result :** RoBERTa와 성능은 유사하거나 더 낫지만, 시간/공간복잡도를 O(n)으로 줄임. <br>
**details :** [notion](https://long8v.notion.site/LinFormer-7aec3be7c2d349b6aa227806955dba61)<br>

## 2021-12-07 T5
Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer([arxiv](https://arxiv.org/pdf/1910.10683.pdf))<br>
**problem :** 다양한 NLP 프리트레이닝 기법은 데이터/목표함수/구조 등이 달라 서로의 성능 혹은 효과성을 비교하기 어려움<br>
**solution :** encoder-decoder 구조로 프리트레이닝 시에는 임의로 선택된 연속된 토큰 감춰놓고 이를 맞추는 문제를 품. 파인튜닝 시에는 인풋 앞에 finetuning 태스크를 나타내는 prefix를 붙이고 decoder는 각 태스크별 output을 생성하도록 함<br>
**result :** 다양한 태스크에서 SOTA, 하나의 text-to-text 프레임워크로 프리트레이닝/파인튜닝을 진행하여 모델 및 데이터의 변동에 따른 성능 차이를 분석할 수 있게 함<br>
**details :** [notion](https://long8v.notion.site/T5-9beb63d63a5c4a89acd524056d1bbe60)<br>

## 2021-12-06 StructuralLM
StructuralLM: Structural Pre-training for Form Understanding([arxiv](https://arxiv.org/abs/2105.11210))<br>
**problem :** 문서를 이해하는 pretraining 모델의 경우 문서의 셀(OCR의 바운딩박스)의 semantic한 정보를 충분히 사용하지 않음. (셀 내의 토큰들이 같은  <br>
**solution :** 2D poisitonal embdding을 하고 셀 내의 토큰은 순서에 따른 1D positional embedding을 함. pre-training task에 숨겨진 셀이 문서의 어느 영역에 위치하는지 분류하는 Cell Poisition Classification을 추가함. <br>
**result :** 이미지 정보를 사용하지 않았음에도 SOTA<br>
**details :** [notion](https://long8v.notion.site/structuralLM-64f16e02a47f4e2697b4f488dccf0db1)<br>

## 2021-12-03 BROS
BROS: A Pre-trained Language Model Focusing on Text and Layout for Better Key Information Extraction from Documentsr([arxiv](https://arxiv.org/pdf/2108.04539.pdf))<br>
**problem :** 문서에서 Key Information를 뽑는 태스크에서 최근 텍스트 + 레이아웃에 이미지 정보까지 사용하는데 이는 연산적으로 비용이 많이 든다<br>
**solution :** LayoutLM + 2D encoding을 절대좌표가 아닌 텍스트 박스 간의 4 꼭지점의 거리를 sin함수로 임베딩 + spanBERT와 유사하게 2D에서 근처 텍스트 박스를 mask하고 맞추도록 하는 Area-MLM 프리트레이닝 태스크를 추가함. decoding은 SPADE를 통해 함 <br>
**result :** entity linking, entity extraction 태스크에서 SOTA. 데이터셋이 적을 경우에도 성능 저하가 다른 모델 보다 적어 효율적인 layout + text 관계를 인코딩한 것으로 <br>
**details :** [notion](https://long8v.notion.site/BROS-86b66bbdc6aa49c5914a3a93cd9bb4be)<br>

## 2021-12-02 Donut
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

## 2021-11-30 Copying Network
Incorporating Copying Mechanism in Sequence-to-Sequence Learning([arxiv](https://arxiv.org/pdf/1603.06393.pdf))<br>
**problem :** Seq2Seq에서 source에 있는 토큰임에도 사전에 존재하지 않는 단어라면 OOV 문제로 예측할 수가 없음<br>
**solution :** 일반적으로 Seq2Seq에서 decoder가 다음 토큰을 generate하는 mode외에 source에서 토큰을 가져오는 copy mode를 정의하고, 각 mode에서 나온 확률값을 합하여 NLL으로 구함<br>
**result :** 요약 태스크에서 기존 RNN Seq2Seq보다 성능 우위<br>
**details :** [notion](https://long8v.notion.site/CopyNet-64e60ff497cb46eb9f1e99e0c6bddaa9)<br>

## 2021-11-29 SPADE
Cost-effective End-to-end Information Extraction for Semi-structured Document Images([arxiv](https://arxiv.org/pdf/2104.08041.pdf))<br>
**problem :** Information Extraction을 하기 위한 기존 서브태스크를 연결한 pipeline의 방법론의 경우 유지보수가 많이 들고, 모델 학습시에도 각 서브 태스크들에 대한 토큰별 annotation이 필요하여 비용이 많이 듦<br>
**solution :** 2D Transformer 구조 + decoder에 copying mechanism을 붙여서 tree 구조(abstract syntax trees)를 generate하는 end2end 모델 <br>
**result :** 기존 pipeline 방법론보다 더 적은 비용, 동일한 양의 데이터로 더 좋은 결과<br>
**details :** [notion](https://long8v.notion.site/WYVERN-07583648be9c4620a7c13924b8ed7f4a)

## 2021-11-26 SQLova
SQLova: A Comprehensive Exploration on WikiSQL with Table-Aware Word Contextualization([arxiv](https://arxiv.org/pdf/1902.01069.pdf))<br>
**problem :** 자연어를 SQL로 변환하는 task(NL2SQL)에서의 BERT 적용. 이때, 통상적 seq2seq를 통한 언어생성은 syntax가 없어 NL2SQL 문제에 적합하지 않음.<br>
**solution :** 자연어 질문과 테이블의 컬럼들을 `[SEP]`토큰으로 concat하여 BERT에 넣음. 마지막 BERT의 두개 layer에 biLSTM 적용하여 쿼리에 들어가는 요소들(select문에 들어가는 컬럼 등)을 예측하는 6가지의 모듈들에 대한 연산 진행. <br>
**result :** SOTA, 크라우드 소싱 분석 결과 human performacne보다 우위.<br>
**details :** [notion](https://long8v.notion.site/SQLova-6e14c9fecc5a420b9394288b14a463f4)

## 2021-11-25 SPADE
SPADE: Spatial Dependency Parsing for Semi-Structured Document Information Extraction([arxiv](https://arxiv.org/pdf/2005.00642.pdf))<br>
**problem :** Information Extraction 문제를 풀 때에 한 문장으로 펼친 뒤(serialize), 여기서 NER 문제를 풀어왔으나 해당 방법론으로는 복잡한 공간적 관계, 문서의 구조적 정보를 다룰 수 없다는 문제가 있음 <br>
**solution :** serialize 단계 없이 각 토큰들과 field를 노드로 두고 그 관계를 엣지로 하는 그래프(=관계가 있으면 1, 없으면 0인 binary matrix로 표현됨)인 를 만드는 것을 목표로 함. 각 노드들은 attention 연산을 통해서 encoding 되고 엣지들은 인코딩된 벡터들의 내적을 통해 확률 값을 가짐.<br>
**result :** BERT base NER과 비슷하거나 나은 성능<br>
**details :** [notion](https://long8v.notion.site/SPADE-6018bae80a514fc5b75a962fc69e39fd)

## 2021-09-05 TSDAE
TSDAE: Using Transformer-based Sequential Denoising Auto-Encoder for Unsupevised Sentence Embedding Learning([arxiv](https://arxiv.org/abs/2104.06979))<br>
**problem :** STS 데이터셋을 얻는 것은 어려우며, finetuning 시에 텍스트 도메인의 차이 때문에 STS의 성능이 finetuning의 성능에 반드시 비례하는 것은 아님<br>
**solution :** auto-encoder처럼 encoder가 노이즈가 있는 텍스트를 받아 저차원의 벡터로 표현하면 이를 decoder가 noise가 없는 텍스트로 변화하는 구조를 가짐<br>k 층의 self-attention을 하고 Query와 Value는 문장임베딩, Key는 이전 (k-1)층의 t시점 디코더 히든스텝을 사용함 (BART와 다르게 인코더의 모든 time-step의 히든벡터가 참조 되지 않음) <br>
**result :** unsupervised sentence embedding 방법론인 MLM, GloVe, Sent2Vec과 비교했을 때 성능상 우위

## 2021-09-04 Faster R-CNN
Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Network([arxiv](https://arxiv.org/abs/1506.01497))<br>
**problem :** Objective Detection에서 사물의 위치를 찾는 Region Proposal단계에서 selective search가 너무 오래걸림<br>
**solution :** CNN + anchor으로 Region Porposal를 한 뒤 이후 ROI pooling과 classifier을 순차적으로 학습시킴. 이때 feature map은 공유하며 둘의 loss는 합하여 multi-task learning 됨<br>
**result :** fast RCNN보다 성능이 개선됬으며 추론속도도 2배 이상 빨라짐<br>

## 2021-09-03 ViT
An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale ([arxiv](https://arxiv.org/abs/2010.11929))<br>
**problem :** Transformer 구조를 image 도메인에 적용<br>
**solution :** 이미지를 16 by 16 block으로 나눈 뒤 쭉 핀 임베딩에 positional embedding을 더한 뒤 트랜스포머 인코더 + FCN으로 구성. 이후 `[CLS]`토큰으로 이미지 분류 태스크<br>
**result :** 분류 문제에서 SOTA. 가장 아래 레이어에서도 글로벌한 정보를 사용하고 있음을 알 수 있었음. CNN보다 locality라는 inductive bias가 적음<br>
**further work :** NLP처럼 semi-supervised pretraining은 하지 못함

## 2021-09-01 LayoutLM
LayoutLM: Pre-training of Text and Layout for Document Image Understanding([arxiv](https://arxiv.org/pdf/1912.13318.pdf))<br>
**problem :** 이전까지 문서 구조를 학습하기 위해 텍스트/이미지 정보만을 활용하였음<br>
**solution :** BERT 아키텍쳐를 활용하여, 좌표, 텍스트를 임베딩하여 MLM, MDC(문서분류)로 프리트레이닝하고 바운딩박스내 이미지 정보를 Faster RCNN에서 feature를 뽑아 결합하여 finetuning <br>
**result :** information extraction, document classification 등의 태스크에서 SOTA<br>

## 2021-08-30 BART
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
