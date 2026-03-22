---
title: "[186] The Llama 3 Herd of Models "
date: 2024-11-15
tags: ['LLM', 'meta', '2024Q3']
paper: "https://scontent-nrt1-1.xx.fbcdn.net/v/t39.2365-6/463020162_522238820565582_8192401983671993921_n.pdf?_nc_cat=108&ccb=1-7&_nc_sid=3c67a6&_nc_ohc=6V_W4zoVlq0Q7kNvgHWuJ7j&_nc_zt=14&_nc_ht=scontent-nrt1-1.xx&_nc_gid=AyU86C3DYuf-4PmOosJFbYv&oh=00_AYDGekjv4Wb1d1PVWmRzuYLeVW9wLE9u4YJKFjCuah0Dew&oe=673CC719"
issue: 205
issueUrl: "https://github.com/long8v/PTIR/issues/205"
---
<img width="666" alt="image" src="https://github.com/user-attachments/assets/dc6c8b45-f694-4815-acc7-693c9333259b">

[paper](https://scontent-nrt1-1.xx.fbcdn.net/v/t39.2365-6/463020162_522238820565582_8192401983671993921_n.pdf?_nc_cat=108&ccb=1-7&_nc_sid=3c67a6&_nc_ohc=6V_W4zoVlq0Q7kNvgHWuJ7j&_nc_zt=14&_nc_ht=scontent-nrt1-1.xx&_nc_gid=AyU86C3DYuf-4PmOosJFbYv&oh=00_AYDGekjv4Wb1d1PVWmRzuYLeVW9wLE9u4YJKFjCuah0Dew&oe=673CC719), [page](https://ai.meta.com/research/publications/the-llama-3-herd-of-models/)

## TL;DR
- **I read this because.. :** 4D parallelism 등 자주 언급되어
- **task :** foundation model
- **idea :** 더 많은 데이터. 더 최적화. 다양한 모달리티 
- **architecture :** Llama2와 대동소이. GQA 사용한 것과 vocab 증가 RoPE frequency 증가 정도가 차이라고 함. 8B, 70B, 405B 정도 셋. // vision의 경우 cross attention 레이어
- **objective :** ce loss / DPO loss 
- **baseline :** llama2, claude, chatgpt, mistral, mixtral, gemini, gemma
- **data :** pretraining data, SFT data(via rejection sampling), RM data(human annotation), 
- **evaluation :** ..
- **result :** 
- **contribution :** 좋은 성능의 오픈소스 모델. 다양한 분야에서의 최적화 + 탐색
- **etc. :** 정말 자잘한 것까지 적어놔서 재밌었다. 

## Details
내용이 많아서 흥미 위주로 정리
### pretraining
- model arch
<img width="658" alt="image" src="https://github.com/user-attachments/assets/1bed1297-d839-4ab1-8125-2fc2fdb2d4ab">

- training recipe
처음에 낮은 bs로 시작했다가 점점 bs를 높이는게 성능 안정성에 좋았다고 함 (bs 4M tokens with 4096 length -> 8M sequences of 8192 length  -> 16M .. 
학습 중간에 non-english와 수학 데이터의 비율을 높였다고 함. 

- annealing data
pretraining 단계에서 high-quality의 mathematical data를 마지막에 많이 보여주는 방식으로 성능을 개선 (GSM8K와 MATH val을 24%, 6.4% 개선)
이걸 반대로 사용해서 small data annealing을 해보고 성능이 안오르면 좋은 데이터가 아니구나하고 판단하기도

- parallelism for model scaling
{TP, CP, PP, DP} 순으로 했다고 함 -- TP로 갈 수록 더 통신이 잦아서
MFU는 38~43% 정도 나왔다고 함. 
<img width="658" alt="image" src="https://github.com/user-attachments/assets/83d30f6b-3b6b-426f-9a82-36d536a1b6e3">

configuration은 이러함. TP: PP비율이 1:2이고 DP는 그냥 나머지!
PP 개선에 대해서도 나와있는데, bubble을 줄이기 위해 interleaved schedule을 적용했고, 첫 레이어의 임베딩과 마지막의 Output 예측 부분은 그냥 하나의 gpu가 담당하도록 했다고함. 그리고 PP에서 asynch Point-to-point communication 썼다고 함. 

bs에 대해 gpu 개수로 제약이 생기는건 아래와 같이 해결했다는데 이해를 못함

<img width="656" alt="image" src="https://github.com/user-attachments/assets/1466670a-5a53-4f67-8afc-dddf37659bea">

- numerical stability 
reduce-scatter 할 때 FP32, accum할 때 FP32등을 신경썼다고 함 

- collective communication
NCCL의 개선된 버전인 NCCLX이라는 패키지를 만들어썼다고 함. 주요기능은 data chunking / data transfer를 튜닝했다고 하고 작은 control message를 더 우선순위 높게 했다고 함. 

### Post Training
- Reward Model
edited > chosen > rejected 순으로 Prefer 데이터라고 보고 학습. concat해서 하나의 Row에서 처리하도록 했고 이 때 성능상 열화는 없었다고 함

- SFT
RFT data + synthetic data + small amount of human-curated data
RFT data (rejection sampling으로 표현) human annotated prompt로 가장 최근의 모델에게 K개의 샘플을 받아서 rejection sampling 해서 학습에 사용. 
-> 대부분의 데이터가 이런 식으로 생성되어서 여러 필터링을 거쳤다고 함.

synthetic data는 대부분 코드 관련된 내용이었는데 재밌었던건 prompt의 다양화를 위해 코드 스니펫을 주고 '이거에 영감ㄱ받아서 prompt 생성해봐'했던 것 + pretraining data를 사용하여 QA 형태로 만들기도 한다고 함 

- DPO 
large-scale에서 PPO 보다 효율적이어서 DPO 채택. 이 때 아래와 같은 변경사항 추가
1) formatting token -- 갑자기 대답을 끝낸다던지 끝 부분에 Repetition이 되는 부분을 개선시킴. win / reject 둘다 같은 토큰이 있을 경우에 loss에서 conflict 이 있는 부분을 개선시킨다고함.
2) regularization of NLL loss: 0.2 coeff으로 넣었을 때 안정성이 늘어난다고 함.

- Model averaging -- 이걸 여러 데이터와 하이퍼파라미터로 해서 다 averaging 했다고 함
- 이걸.. 또 6번에 걸쳐서 했다고 함

## Visual Experiments
- ViT-H/14 사용.
- cross-attention 사용. 이때 finegrained ability를 쓰기 위해서 {4, 9, 16, 24, 31}번째 레이어의 히든을 final layer feature와 같이 썼다고 함
- 6B scale의 image-text pair를 336 x 336에 최대 4개 grid를 가지는 anyres로 pretraining
- 이후에 언어모델과 비슷하게 SFT + RM + DPO + very high quality의 데이터만으로 DPO 학습을 했다고 함
- 벤치마크 성능
<img width="672" alt="image" src="https://github.com/user-attachments/assets/46227f98-dbd5-42e4-a8da-c01161db3e68">


---- 
성현님 요약
The Llama 3 Herd of Models
Llama 3 405B 모델 공개와 함께 기대했던 테크니컬 리포트가 나왔다. Llama 2 리포트보다 훨씬 더 많은 정보가 포함되어 있어 굉장히 흥미롭다.
1. 프리트레이닝
웹 데이터 전처리에 대해 비교적 상세하게 기술하고 있다. 자체 개발한 Main Content Extractor를 사용했다. 전체 데이터에 대한 Deduplication을 수행했다고 하는데 Global Deduplication을 시사하는 것인지 궁금한 점이 있다. 추가적으로 CCNet 스타일의 Line Deduplication으로 Boilerplate를 추가 제거. C4/Gopher 스타일 휴리스틱 필터와 (아마도 LM 기반의) 텍스트 분포에서의 아웃라이어들에 대한 필터링도 사용.
Wikipedia를 레퍼런스로 잡은 fastText, Llama 2 예측 기반의 DistilRobert 분류기로 퀄리티 필터링.
DeepSeek 스타일의 수학과 코드 도메인에 특화한 웹 페이지 추출.
분류기를 사용해 웹 데이터의 도메인을 분류하고 Scaling Law 추정을 통해 데이터 믹스를 결정. 일반 지식 50%, 수학 및 추론 관련 25%, 코드 17%, 다국어 8%.
고품질 데이터로 학습 최종 단계에서 Annealing 적용. 역으로 Annealing을 사용해 데이터셋의 퀄리티를 검증하기도 함.
문서 간 Attention을 차단하기 위한 마스킹 적용. Long Context 추가 학습에 유용했다고 언급. Polyak Averaging도 적용.
다운스트림 과제에 대한 Likelihood에 대해 Scaling Law를 추정한 다음 Likelihood와 과제에 대한 스코어의 함수를 추정하는 방식으로 다운스트림 과제에 대한 Scaling Law를 추정.
Pipeline Parallel의 배치 크기 제약을 완화하고 Ring 대신 All-Gather 기반 Context Parallel을 사용.
2. 포스트트레이닝
Reward Modeling에서 시작해서 Rejection Sampling으로 생성한 데이터로 SFT를 하고 DPO를 하는 흐름. 즉 PPO를 쓰지 않고 SFT 단계에서도 모델 생성 데이터가 주축이 된다.
포스트트레이닝 데이터에 대해서는 강하게 퀄리티 컨트롤을 했다. 수작업으로 데이터를 필터링하고, 모델 기반의 퀄리티 필터링과 난이도에 따른 비율 조정, 그리고 Semantic Deduplication을 적용.
포스트트레이닝 시점에서는 각 도메인에 대해 특화된 데이터 구축 작업들을 진행했다.
2.1 코드
코드 특화 모델을 구축하는 것에서 시작. 레포 레벨 데이터도 활용했다. 컴파일러 피드백과 모델로 생성한 유닛 테스트를 사용한 피드백을 사용해 데이터를 개선하고 학습.
서로 다른 프로그래밍 언어간 번역, 코드 설명, 생성, 문서화, 디버깅 등의 과제에 대해서 모델이 응답을 생성하게 한 다음 원 코드로 Backtranslation을 하게 하고 출력 결과의 퀄리티를 사용해 필터링.
2.2 다국어
다국어에 대해서도 특화 모델을 학습. NLP 데이터셋과 사람이 작성한 프롬프트를 사용하고 Rejection Sampling을 적용한 다음 룰 기반 퀄리티 필터링. 기계 번역은 의도적으로 제외하려고 노력.
2.3 수학
프리트레이닝 데이터와 사람을 통해 프롬프트를 구축. 모델로 CoT 응답을 생성한 다음 모델 기반으로 검증. Process Reward Model을 사용해 필터링하고, 어려운 문제의 경우에는 MCTS와 Process Reward Model을 사용해 응답을 생성.
2.4 추론
텍스트와 코드를 사용해 추론 문제를 풀도록 학습. 코드 실행 피드백을 사용하고 잘못된 생성 결과를 모델을 통해 오류를 교정.
2.5 Long Context
긴 문서를 청킹한 다음 각 청크에 대해 QA를 생성하고 합치는 전통적인 방식에 마찬가지로 청크에 대해 요약한 다음 이 요약을 요약하는 방법을 사용. 파이썬 코드에 대해 Dependency Sorting을 하고 가장 많이 참조된 파일을 지운 다음 이 파일의 코드를 생성하도록 하는 방법도 사용.
2.6 도구 사용
웹 검색, 파이썬 인터프리터, Wolfram Alpha에 대한 도구 사용 능력을 학습시켰음. 이쪽은 사람이 직접 데이터를 작성하는 방식. 다만 합성 데이터를 사용해 기본적인 도구 사용 능력을 습득시킨 다음에 시작.
2.7 Factuality
프리트레이닝에서 문서를 가져와서 질문을 생성하게 한 다음 응답을 샘플링. 문서와 응답을 통해 Llama 3 기반으로 정확성과 정보의 품질을 평가. 지속적으로 오답이 발생하는 경우에는 Refusal을 생성.
2.8 Steerability
어노테이터들이 시스템 프롬프트를 만들게 한 다음 대화를 진행하고 어노테이션을 하도록 함.
2.9 Safety
어노테이터를 통해 Adversarial 프롬프트를 구축하고 Automatic Red Teaming도 적용.
3. 비전, 오디오
비전의 경우에는 이미지 인코더에 대한 Cross Attention, 오디오의 경우에는 인코더 출력을 모델 입력으로 바로 Projection.
소감
웹 데이터 처리는 높은 차원에서는 현재 정석적으로 여겨지는 방법들을 채택. DeepSeek 스타일의 코드 및 수학 도메인 데이터 발굴이 중요한 수단이라는 것이 재차 검증됨. 추가적으로 Scaling Law를 사용한 데이터 믹스 결정 등 체계적인 방법도 흥미로운 지점.
안정적이고 효율적인 학습 인프라 구축을 위해서는 통신과 Parallelism의 바닥부터 직접 손을 대어야 한다는 것을 증명.
포스트트레이닝은 더 확연하게 Preference Data로 무게중심이 옮겨짐. SFT도 대부분이 모델 생성 데이터를 Reward Model로 Rejection Sampling한 샘플에 대해 학습시키는 것으로 구성됨. 사실상 온라인 샘플을 통해 학습하게 되면서 PPO 없이 DPO만으로 학습하는 것이 충분히 좋은 선택이 됨.
코드와 수학에 대해 코드 실행/컴파일러 피드백과 Process Reward Model/MCTS가 중요한 구성 요소가 됨.
포스트트레이닝에 언급된 방법 하나하나가 모두 각각 한 편의 논문이 될 수 있는 테크닉들. 그리고 이 모든 테크닉들을 종합해서 포스트트레이닝이 구성됨. 사실 이것은 프리트레이닝과 학습 인프라 구축에서도 마찬가지. 지금 시점의 프런티어 모델은 최첨단을 달리는 다양한 기술들을 종합적으로 모델 하나에 집중해서 만들어지고 있음. GPU 숫자 같은 명시적인 연산력에 밀려 흔히 가려지는 부분이지만 이 수많은 노력들을 효과적으로 집중하는 것이 굉장히 중요한 요소라는 것을 시사하는 것일 것.