[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Flong8v%2FPTIR&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false)](https://hits.seeyoufarm.com) 
# π Paper Today I Read π
- 21λλκΉμ§ `readme.md` + `notion`, 22λλΆν° [issue](https://github.com/long8v/PTIR/issues)λ‘ κ΄λ¦¬
- 22λλ λͺ©νλ 100κ°! νμ¬  <img alt="issues" src="https://img.shields.io/github/issues/long8v/PTIR?color=0088ff"> κ°
- DL ν·κ°λ¦¬λ termμ μ¬κΈ° μ λ¦¬ν΄λμλ€. [velog](https://velog.io/@long8v/DL-%EC%9A%A9%EC%96%B4-%EC%A0%95%EB%A6%AC)
- κ°λ μ½λλ₯Ό μ½μ λλ [PR](https://github.com/long8v/PTIR/pulls)μ νμ©

## 2021λμ μ½μ λΌλ¬Έλ€ (28 papers)
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
  * [2021-11-29 WYVERN](#2021-11-29-spade)
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
**problem :** ViTλ λκ·λͺ¨ μ΄λ―Έμ§ λ°μ΄ν°μμΌλ‘ νμ΅ν΄μΌ μΌλ°ν κ°λ₯ν λͺ¨λΈμ νμ΅ν  μ μμ<br>
**solution :** ViTκ΅¬μ‘°μ distillation tokenμ μΆκ°νμ¬ CNN λ±μ teacher modelμ μ¬μ©νμ¬ distillation νμ΅μ μ§νν¨<br>
**result :** imageNetλ§μΌλ‘ νμ΅ν λͺ¨λΈμ΄ μ’μ μ νλλ₯Ό λ, ViT, ResNetμ λΉκ΅ν΄λ΄€μ λ λ μμ νλΌλ―Έν°λ‘ λμ μ±λ₯<br>
**details :** [notion](https://long8v.notion.site/DeiT-a045232cb9f4468e9b90e6a3efda8625)

## 2021-12-30 LeViT
LeViT: a Vision Transformer in ConvNet's Clothing for Faster Inference, 2021([arxiv](https://arxiv.org/pdf/2104.01136.pdf))<br>
**problem :** λ λμ μλ/μ±λ₯ trade-offλ₯Ό κ°μ§λ ViTλ₯Ό κ°λ°ν΄λ³΄μ<br>
**solution :** μ²μμ CNNμΌλ‘ resolutionμ μ€μΈ λ€, νΈλμ€ν¬λ¨Έλ₯Ό μμ λΆμ. μ΄λ, μ°λ¦¬λ CNNμ²λΌ pyramid κ΅¬μ‘°λ₯Ό κ°κΈ° μν΄ μ€κ°μ Queryλ₯Ό average-poolingμΌλ‘ sub-samplingμ νμ¬ resolutionμ μ€κ°μ€κ°μ μ€μ¬κ°. μΈμ MLP λμ  1 x 1 convolutionμ νκ³ , positional embedding λμ  attention biasλ₯Ό μΆκ°νλ λ± ν¨μ¨μ μΈ μ°μ°μ μν λνμΌμ μμ ν¨.<br>
**result :** DeiTλ EfficientNetκ³Ό μ μ¬ν μ±λ₯μΌλ‘ λ λΉ λ₯Έ μΈνΌλ°μ€ μλ.<br>
**details :** [notion](https://long8v.notion.site/LeViT-8dfba651c7e54430992ee79b2e3429c6)<br>

## 2021-12-28 Frozen
Multimodal Few-Shot Learning with Frozen Language Models, 2021([arxiv](https://papers.nips.cc/paper/2021/file/01b7575c38dac42f3cfb7d500438b875-Paper.pdf))<br>
**problem :** λν μΈμ΄λͺ¨λΈμκ² visual μ λ³΄λ₯Ό few-shotμΌλ‘ νμ΅ν  μ μκ² ν΄λ³΄μ<br>
**solution :** visual encoderλ₯Ό prefixμ²λΌ input μνμ€ μμ λκ³  κΈ°μ‘΄ μΈμ΄λͺ¨λΈμ νλΌλ―Έν°λ frozen μν€κ³  νμ΅μν΄. <br>
**result :** few-shotμΌλ‘λ μλΉν μ±λ₯, λ©ν°λͺ¨λ¬ few shot λ¬λ λ°΄μΉλ§ν¬λ₯Ό μ μ<br>
**details :** [notion](https://long8v.notion.site/Frozen-405d8913a0ea4779a503e8f61e21d835)<br>

## 2021-12-27 DETR
End-to-End Object Detection with Transformers, 2020([arxiv](https://arxiv.org/pdf/2005.12872.pdf))<br>
**problem :** object detection λ¬Έμ λ₯Ό νκΈ° μν΄μ  μμμ κ΅¬μ‘°/μ€κ³κ° νμν¨<br>
**solution :** object detectionμ΄ μ€λ³΅μ΄ μλ μμ μκ΄ μλ setμ μμΈ‘νλ κ²μ΄κΈ° λλ¬Έμ, CNN + transformer encoder-decoder + FFNμΌλ‘ νλ²μ bboxλ₯Ό μμΈ‘ν  μ μλλ‘ ν¨. μ΄ λ, lossλ μ°μ  μμΈ‘λ boxμ gt boxλ₯Ό bipartiteλ‘ μ΅μ  matchingμ κ΅¬ν λ€, μ΅μ  λ§€μΉ­μμ box lossμ ν΄λμ€ λ μ΄λΈμ ν©μΉ lossλ₯Ό μ¬μ©ν¨.<br>
**result :** FASTER RCNNκ³Ό μ μ¬ν μ±λ₯, panoptic segmentationμμ SOTA<br>
**details :** [notion](https://long8v.notion.site/DETR-5810bf27ec954498a3bdd95c15b116b7)<br>

## 2021-12-23 Pix2seq
Pix2seq: A Language Modeling Framework for Object Detection, 2021([arxiv](https://arxiv.org/pdf/2109.10852.pdf))<br>
**problem :** Object Detection λ¬Έμ λ₯Ό νκΈ° μν΄μ  νΉμν κ΅¬μ‘°/μ€κ³κ° νμν¨<br>
**solution :** object detection λ¬Έμ λ₯Ό μ΄λ―Έμ§λ₯Ό λ£μμ λ λ°μ΄λ© λ°μ€μ λ μ΄λΈμ ννν ν ν° sequenceλ₯Ό λ½λ μΈμ½λ-λμ½λ κ΅¬μ‘°λ‘ λ°κΏ. μ΄λ λͺ¨λ  objectλ₯Ό μ°Ύμ§ μκ³  λλλ²λ¦¬λ κ²μ λ§κΈ° μν΄ noiseλ₯Ό μμ augmentationμ μΆκ°νμ¬ λͺ¨λΈμ΄ noiseμΈμ§ μλμ§λ₯Ό κ΅¬λΆνλλ‘ νλ©΄μ κ³ μ λ κΈΈμ΄λ‘ μμΈ‘νλλ‘ ν¨. μ΄λ₯Ό ν΅ν΄ recallμ λμ΄μ¬λ¦Ό. <br>
**result :** Faster RCNN, DETRκ³Ό κ°μ λνμλ§μ μν΄ μ€κ³λμκ³  μ΅μ νλ λͺ¨λΈλ€κ³Ό μ±λ₯μ΄ μ μ¬νκ² λ¨<br>
**details :** [notion](https://long8v.notion.site/pix2seq-109e93c7ebb54104bbca96f16ddc4127)<br>

## 2021-12-21 Swin
Swin Transformer: Hiearchical Vision Transformer using Shifted Window, 2021([arxiv](https://arxiv.org/abs/2103.14030))<br>
**problem :** ViTμ κ°μ΄ λΉμ μ νΈλμ€ν¬λ¨Έλ₯Ό μ μ©νκ³ μ νλ μλκ° μμΌλ, νκ°μ ν ν° λ¨μλ₯Ό 16 by 16λ‘ κ³ μ νλ κ²μ pixel λ¨μμΈ semantic segmentationμ νκΈ°μ μ ν©νμ§ μμΌλ©° κ³ νμ§ λ°μ΄ν°μ κ²½μ° μ΄λ―Έμ§ ν¬κΈ°μ μ κ³±μΌλ‘ μ°μ°μ μμ΄ λ§μμ Έμ μ¬μ©μ νκ³κ° μμ <br>
**solution :** ViTμ²λΌ m by m ν¨μΉλ‘ μλ₯Έ λ€μ κ·Έ λ΄λΆμ ν½μ λ¨μλ‘ self-attentionμ ν¨. κ·Έ λ€μ ν¨μΉλ₯Ό M // 2λ§νΌ shift ν΄μ ν¨μΉλ₯Ό λλ λ€ self-attentionμ ν¨. μ΄ κ΅¬μ‘°λ₯Ό λ°λ³΅νμ¬ νλ¦¬νΈλ μ΄λ/νμΈνλμ μ§νν¨ <br>
**result :** ViTμ λ¬λ¦¬ μ°μ°λμ΄ μ΄λ―Έμ§ ν¬κΈ°μ μ νμ μΌλ‘ μ¦κ°νλ©΄μλ classification, detection, segmentationμμ SOTA <br>
**details :** [notion](https://long8v.notion.site/Swin-Transformer-99285aee1ff14e3ab5411c3427c50311)<br>

## 2021-12-20 SimpleDLM
Value Retrieval with Arbitrary Queries for Form-like Documents, 2021([arxiv](https://arxiv.org/abs/2112.07820))<br>
**problem :** λ¬Έμμμ μνλ μ λ³΄λ₯Ό λ½λ νμ€ν¬μμ μ΄μ  λ°©λ²λ‘ λ€μ λ―Έλ¦¬ μ μν΄λμ fieldλ₯Ό μμΈ‘νλ λ¬Έμ λ₯Ό νμλλ°, μ΄λ λ€λ₯Έ form νΉμ λλ©μΈμ μ μ©νκΈ° μ΄λ ΅λ€<br>
**solution :** μΏΌλ¦¬κ° μ£Όμ΄μ‘μ λ λ¬Έμμμ μνλ valueλ₯Ό μ°Ύλ λ¬Έμ λ‘ λ°κΏ. μΏΌλ¦¬μ OCR νμ€νΈλ₯Ό κ°μ μλ² λ©μ κ±°μΉ λ€ κ°μ΄ self-attentionμ νλλ‘ νκ³  κ°κ°μ λ§μ§λ§ μνμ΄νμ λ μ΄μ΄μ average-pooling, FCNμ κ±°μΉ λ€ λ΄μ μ νμ¬ κ° ν ν°μ΄ μνλ valueμΈμ§ μλμ§ μ΄μ§ λΆλ₯νλ λ¬Έμ λ‘ λ°κΏ. ν΄λΉ μν€νμ³λ‘ MLMμ νλ νλ¦¬νΈλ μ΄λ λͺ¨λΈ(simpleDLM)μ λ§λ¦.<br>
**result :** BERT, LayoutLM νλ¦¬νΈλ μ΄λμ κ°μ Έμ¨ κ²λ³΄λ€ simpleDLMμΌλ‘ νλ¦¬νΈλ μ΄λν κ²μ΄ F1 μ±λ₯μ΄ μ°μ. <br>
**details :** [notion](https://long8v.notion.site/simpleDLM-7c1edd8680584952a5c4a2dd2794cbfb)<br>

## 2021-12-17 METER
An Empirical Study of Training End-to-End Vision-and-Language Transformers, 2021([arxiv](https://arxiv.org/pdf/2111.02387.pdf))<br>
**problem :** Vison-and-Language(VL) νμ€ν¬μ λν΄μ end-to-end λ°©μμΌλ‘ νΈλμ€ν¬λ¨Έλ§ μ¬μ©ν λͺ¨λΈ μ€ region-based modelλ³΄λ€ λμ μ±λ₯μ λ³΄μΈ κ²μ΄ μμκ³ , κ° λͺ¨λλ€μ λν μ€νμ΄ λΆμ‘±ν¨<br>
**solution :** VLμ μ£Όμ λͺ¨λλ€μ λν΄ μμλ³΄κ³  Ablation studyν¨ <br>
**result :** VQA νμ€ν¬μμ SOTA, μ€νμ ν΅ν΄ λͺκ°μ§ λͺ¨λλ€μ λν μ±λ₯ μ°μλ₯Ό μμλ<br>
**details :** [notion](https://long8v.notion.site/METER-b9b1beb61f194ea5ba6d573b16328ead)<br>

## 2021-12-16 Gated MoE
Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer, 2017([arxiv](https://arxiv.org/pdf/1701.06538.pdf))<br>
**problem :** ν° λͺ¨λΈμ λ§λ€λ©΄ μ±λ₯μ΄ λμ΄λμ§λ§ λ©λͺ¨λ¦¬μ μ΄μλ‘ νκ³κ° μμ<br>
**solution :** κ° λλ¦½μ μΈ NNμΈ expertλ€μ λ§λ€κ³ , μΈνμ λ°λΌ μ΄λ€ expertλ₯Ό μ νν μ§ gating λ€νΈμν¬λ₯Ό κ΅¬μ±. μ΄λ top kκ°λ§ μ ννλλ‘ νμ¬ sparseν gatingμ κ° expertμ outputrκ³Ό weighted sumνμ¬ <br>
**result :** λ λ?μ λΉμ©μΌλ‘ λ ν° λͺ¨λΈ νμ΅. MTμμ SOTA<br>
**details :** [notion](https://long8v.notion.site/gated-MoE-ff42470ad545417795e82ea54fefbf3b)<br>

## 2021-12-15 GLaM
GLaM: Efficient Scaling of Language Models with Mixture-of-Experts([arxiv](https://arxiv.org/pdf/2112.06905.pdf))<br>
**problem :** NLPμμ ν° νλ¦¬νΈλ μ΄λ λͺ¨λΈμ μ’μ μ±λ₯μ λ³΄μ΄μ§λ§, νμ΅/μΆλ‘  λΉμ©μ΄ λλ¬΄ ν¬λ€<br>
**solution :** Mixture-of-Experts λͺ¨λΈμμ λ°μ νΈλμ€ν¬λ¨Έ κ΅¬μ‘° λ΄μ μ£Όμ΄μ§ ν ν°μ μ²λ¦¬νκΈ°μ μ΄λ€ expertκ° κ°μ₯ μ ν©νμ§λ₯Ό νμ΅νλ gatingμ λ§λ€κ³  μ μ λ expertμ outputμ ν©μΌλ‘ λͺ¨λΈμ outputμ λ΄λ±μ<br>
**result :** GPT-3λ³΄λ€ ν¬κΈ°κ° 7λ°° ν¬μ§λ§, μλμ§λ 1/3λ°° μ°μ΄λ©° zero-shot, one-shotμμ GPT-3λ³΄λ€ μ±λ₯ μ°μ<br>
**details :** [notion](https://long8v.notion.site/GLaM-051d25d6164b4d4bb4f6191beeeba81b)<br>

## 2021-12-14 PVT
Pyramid Vision Transformer: A Versatile Backbone for Dense Prediction without Convolutions([arxiv](https://arxiv.org/pdf/2102.12122.pdf))<br>
**problem :** λΉμ  νΈλμ€ν¬λ¨Έ λΆμΌμμ μ΄μ μ μ μλ ViTλ μ°μ°λμ΄ λ§κ³  μμνμ΄ μ μ°¨μμ΄μ΄μ ν½μ λ λ²¨μ νμ€ν¬λ₯Ό νκΈ°μ μ μ νμ§ μμ<br>
**solution :** 1) Feature Pyramid : CNNμ²λΌ 4λ¨κ³μ λ μ΄μ΄λ₯Ό μμμ κ° ν¬κΈ°μ νΌμ³λ₯Ό λͺ¨λ μ¬μ©ν  μ μκ² ν¨. 2) Spatial Reduction Attention(SRA) : Self-Attention μ°μ°μμ Keyμ Valueλ₯Ό reshape + FCλ₯Ό κ±°μ³ μ°¨μμ μ€μΈ λ€μ μ§νν¨<br>
**result :** μ΄λ―Έμ§ λΆλ₯ λΏ μλλΌ λνμ/μΈκ·Έλ©νμ΄μ κ°μ dense prediction νμ€ν¬μλ λ°λ‘ μ μ© κ°λ₯νλ©°, SRAλ₯Ό ν΅ν΄ κ³μΌ λΉμ©λ μ€μ. λ€μν λ€μ΄μ€νΈλ¦Ό νμ€ν¬μμ SOTA<br>
**details :** [notion](https://long8v.notion.site/PVT-6403ee04d45c4732a02f65c7924f1f08)<br>

## 2021-12-13 MixText
MixText: Linguistically-Informed Interpolation of Hidden Space for Semi-Supervised Text Classification([arxiv](https://aclanthology.org/2020.acl-main.194.pdf))<br>
**problem :** κΈ°μ‘΄μ semi-supervised λ°©λ²λ‘ λ€μ label λ°μ΄ν°μ unlabeled λ°μ΄ν°κ° λ°λ‘ μ¬μ©λμ΄, unlabeled λ°μ΄ν°μμ νμΈνλ μ μ¬μ ν κ³Όμ ν©λ  κ°λ₯μ±μ΄ λ§μ<br>
**solution :** λΉμ μμ μ¬μ©λλ mixup κΈ°λ²κ³Ό μ μ¬νκ², BERT λ±μ νλ¦¬νΈλ μΈ λͺ¨λΈμ μμμ λ κ°μ xμ hidden vectorλ₯Ό λ³΄κ°νκ³  yμ­μ λ³΄κ°νμ¬ νμ΅λ°μ΄ν°λ‘ λ μ΄λΈ λ°μ΄ν°μ ν¨κ» μ¬μ©. KL divergence lossμ unlabeled dataμ λν΄ λ μμ μκ² μμΈ‘ν  μ μλλ‘ λΆλ₯ μνΈλ‘νΌ λ‘μ€λ₯Ό ν©νμ¬ lossλ‘ μ¬μ©<br>
**result :** νμ€νΈ λΆλ₯ λ¬Έμ μμ μ νλ λ μ΄λΈ λ°μ΄ν°λ₯Ό κ°μ§κ³  μμ λ SOTA<br>
**details :** [notion](https://long8v.notion.site/MixText-c91fca74f6bb46fe9ef0aa8868fc5bd4)<br>

## 2021-12-09 Linformer
Linformer: Self-Attention with Linear Complexity([arxiv](https://arxiv.org/abs/2006.04768))<br>
**problem :** Transformerμ self-attention μ°μ°μ΄ μνμ€ κΈΈμ΄ nμ λνμ¬ O(n^2)λ‘ μκ°, κ³΅κ°λ³΅μ‘λκ° λμ΄λ¨. <br>
**solution :** self-attention layerμ κ²°κ³Ό matrixκ° low-rankλΌλ κ²μ λ°νλ. μ¦, μ μ°¨μμΌλ‘ ννν  μ μμΌλ―λ‘ linear projection λ μ΄μ΄λ₯Ό μΆκ°νμ¬ key, valueμ μ°¨μμ μ€μΈ λ€ μ°μ°μ μ§νν¨.<br>
**result :** RoBERTaμ μ±λ₯μ μ μ¬νκ±°λ λ λ«μ§λ§, μκ°/κ³΅κ°λ³΅μ‘λλ₯Ό O(n)μΌλ‘ μ€μ. <br>
**details :** [notion](https://long8v.notion.site/LinFormer-7aec3be7c2d349b6aa227806955dba61)<br>

## 2021-12-07 T5
Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer([arxiv](https://arxiv.org/pdf/1910.10683.pdf))<br>
**problem :** λ€μν NLP νλ¦¬νΈλ μ΄λ κΈ°λ²μ λ°μ΄ν°/λͺ©νν¨μ/κ΅¬μ‘° λ±μ΄ λ¬λΌ μλ‘μ μ±λ₯ νΉμ ν¨κ³Όμ±μ λΉκ΅νκΈ° μ΄λ €μ<br>
**solution :** encoder-decoder κ΅¬μ‘°λ‘ νλ¦¬νΈλ μ΄λ μμλ μμλ‘ μ νλ μ°μλ ν ν° κ°μΆ°λκ³  μ΄λ₯Ό λ§μΆλ λ¬Έμ λ₯Ό ν. νμΈνλ μμλ μΈν μμ finetuning νμ€ν¬λ₯Ό λνλ΄λ prefixλ₯Ό λΆμ΄κ³  decoderλ κ° νμ€ν¬λ³ outputμ μμ±νλλ‘ ν¨<br>
**result :** λ€μν νμ€ν¬μμ SOTA, νλμ text-to-text νλ μμν¬λ‘ νλ¦¬νΈλ μ΄λ/νμΈνλμ μ§ννμ¬ λͺ¨λΈ λ° λ°μ΄ν°μ λ³λμ λ°λ₯Έ μ±λ₯ μ°¨μ΄λ₯Ό λΆμν  μ μκ² ν¨<br>
**details :** [notion](https://long8v.notion.site/T5-9beb63d63a5c4a89acd524056d1bbe60)<br>

## 2021-12-06 StructuralLM
StructuralLM: Structural Pre-training for Form Understanding([arxiv](https://arxiv.org/abs/2105.11210))<br>
**problem :** λ¬Έμλ₯Ό μ΄ν΄νλ pretraining λͺ¨λΈμ κ²½μ° λ¬Έμμ μ(OCRμ λ°μ΄λ©λ°μ€)μ semanticν μ λ³΄λ₯Ό μΆ©λΆν μ¬μ©νμ§ μμ. (μ λ΄μ ν ν°λ€μ΄ κ°μ  <br>
**solution :** 2D poisitonal embddingμ νκ³  μ λ΄μ ν ν°μ μμμ λ°λ₯Έ 1D positional embeddingμ ν¨. pre-training taskμ μ¨κ²¨μ§ μμ΄ λ¬Έμμ μ΄λ μμ­μ μμΉνλμ§ λΆλ₯νλ Cell Poisition Classificationμ μΆκ°ν¨. <br>
**result :** μ΄λ―Έμ§ μ λ³΄λ₯Ό μ¬μ©νμ§ μμμμλ SOTA<br>
**details :** [notion](https://long8v.notion.site/structuralLM-64f16e02a47f4e2697b4f488dccf0db1)<br>

## 2021-12-03 BROS
BROS: A Pre-trained Language Model Focusing on Text and Layout for Better Key Information Extraction from Documentsr([arxiv](https://arxiv.org/pdf/2108.04539.pdf))<br>
**problem :** λ¬Έμμμ Key Informationλ₯Ό λ½λ νμ€ν¬μμ μ΅κ·Ό νμ€νΈ + λ μ΄μμμ μ΄λ―Έμ§ μ λ³΄κΉμ§ μ¬μ©νλλ° μ΄λ μ°μ°μ μΌλ‘ λΉμ©μ΄ λ§μ΄ λ λ€<br>
**solution :** LayoutLM + 2D encodingμ μ λμ’νκ° μλ νμ€νΈ λ°μ€ κ°μ 4 κΌ­μ§μ μ κ±°λ¦¬λ₯Ό sinν¨μλ‘ μλ² λ© + spanBERTμ μ μ¬νκ² 2Dμμ κ·Όμ² νμ€νΈ λ°μ€λ₯Ό maskνκ³  λ§μΆλλ‘ νλ Area-MLM νλ¦¬νΈλ μ΄λ νμ€ν¬λ₯Ό μΆκ°ν¨. decodingμ SPADEλ₯Ό ν΅ν΄ ν¨ <br>
**result :** entity linking, entity extraction νμ€ν¬μμ SOTA. λ°μ΄ν°μμ΄ μ μ κ²½μ°μλ μ±λ₯ μ νκ° λ€λ₯Έ λͺ¨λΈ λ³΄λ€ μ μ΄ ν¨μ¨μ μΈ layout + text κ΄κ³λ₯Ό μΈμ½λ©ν κ²μΌλ‘ <br>
**details :** [notion](https://long8v.notion.site/BROS-86b66bbdc6aa49c5914a3a93cd9bb4be)<br>

## 2021-12-02 Donut
Donut : Document Understanding Transformer without OCR([arxiv](https://arxiv.org/pdf/2111.15664.pdf))<br>
**problem :** κΈ°μ‘΄ μ¬μ§ κΈ°λ°μ λ¬Έμλ₯Ό μ΄ν΄νλ νμ€ν¬λ€μ μ κ·Ό λ°©μλ€μ OCRμ νλ² κ±°μΉ¨μΌλ‘μ κ³μ° λΉμ©μ΄ ν¬κ³  OCR μλ¬λ‘ μΈν΄ μκ²¨λλ μ±λ₯ μ νλ¬Έμ κ° μμ.<br>
**solution :** Swin Transformer μΈμ½λ + BART λμ½λλ‘ μ΄λ―Έμ§λ₯Ό μ½κ³  λ°λ‘ jsonμΌλ‘ ν¬λ§€ν κ°λ₯ν ν ν°μ λ΄λ±λλ‘ ν¨. μ΄λ νλ¦¬νΈλ μ΄λμ κ°μμ λ¬Έμ λ°μ΄ν°λ₯Ό λ§λ€κ³  λ¬Έμ λ΄ κΈμλ₯Ό λͺ¨λ μ½λ κ²μ ν΅ν΄ μ§νν¨.<br>
**result :** λ¬ΈμλΆλ₯ : OCR μλ λͺ¨λΈ μ€μμ SOTA, OCR κΈ°λ°μ νλ¦¬νΈλ μ΄λ λͺ¨λΈμΈ LayoutLMμ μ±λ₯μ κ·Όμ νμ§λ§ λͺ¨λΈ ν¬κΈ°μ μλ λ©΄μμ μ°μ. νμ±μμ SOTA.  <br>
**details :** [notion](https://long8v.notion.site/Donut-fbaf0e9e19624ae492108f1249a47aa1)<br>

## 2021-12-01 
Empirical Analysis of Unlabeled Entity Problem in Named Entity Recognition([arxiv](https://openreview.net/pdf?id=5jRVa89sZk))<br>
**problem :** NER λ¬Έμ μμ μ€μ νΉμ λ³΅μ‘μ± λλ¬Έμ unlabeldλ entityλ€μ positive sampleμ μ€μ¬ μ±λ₯μ μνμν€κΈ°λ νμ§λ§ μ΄λ BERTμ κ°μ PLMμΌλ‘ ν΄κ²° κ°λ₯ν λ°λ©΄μ, negative sampleλ‘ μ¬μ©λ¨μ λ°λΌ λ°μνλ μ±λ₯ μνλ ν΄κ²°νκΈ° μ΄λ €μ<br>
**solution :** labelλ spanμ λν cross entropy loss + unlabelλ spanμ λν΄ λλ€μΌλ‘ μνλ§νμ¬ cross-entropy lossλ₯Ό κ΅¬ν¨<br>
**result :** κ°μμ λ°μ΄ν°(μΌλΆλ¬ labled entity μΌλΆλ₯Ό λΉΌλ¨Ήμ)μμλ ν΄λΉ λ¬Έμ λ₯Ό λ€ ν΄κ²°, μ annotateλ λ°μ΄ν°μμλ SOTAμ κ±°μ κ·Όμ , real-world dataλ SOTA<br>

## 2021-11-30 Copying Network
Incorporating Copying Mechanism in Sequence-to-Sequence Learning([arxiv](https://arxiv.org/pdf/1603.06393.pdf))<br>
**problem :** Seq2Seqμμ sourceμ μλ ν ν°μμλ μ¬μ μ μ‘΄μ¬νμ§ μλ λ¨μ΄λΌλ©΄ OOV λ¬Έμ λ‘ μμΈ‘ν  μκ° μμ<br>
**solution :** μΌλ°μ μΌλ‘ Seq2Seqμμ decoderκ° λ€μ ν ν°μ generateνλ modeμΈμ sourceμμ ν ν°μ κ°μ Έμ€λ copy modeλ₯Ό μ μνκ³ , κ° modeμμ λμ¨ νλ₯ κ°μ ν©νμ¬ NLLμΌλ‘ κ΅¬ν¨<br>
**result :** μμ½ νμ€ν¬μμ κΈ°μ‘΄ RNN Seq2Seqλ³΄λ€ μ±λ₯ μ°μ<br>
**details :** [notion](https://long8v.notion.site/CopyNet-64e60ff497cb46eb9f1e99e0c6bddaa9)<br>

## 2021-11-29 WYVERN
Cost-effective End-to-end Information Extraction for Semi-structured Document Images([arxiv](https://arxiv.org/pdf/2104.08041.pdf))<br>
**problem :** Information Extractionμ νκΈ° μν κΈ°μ‘΄ μλΈνμ€ν¬λ₯Ό μ°κ²°ν pipelineμ λ°©λ²λ‘ μ κ²½μ° μ μ§λ³΄μκ° λ§μ΄ λ€κ³ , λͺ¨λΈ νμ΅μμλ κ° μλΈ νμ€ν¬λ€μ λν ν ν°λ³ annotationμ΄ νμνμ¬ λΉμ©μ΄ λ§μ΄ λ¦<br>
**solution :** 2D Transformer κ΅¬μ‘° + decoderμ copying mechanismμ λΆμ¬μ tree κ΅¬μ‘°(abstract syntax trees)λ₯Ό generateνλ end2end λͺ¨λΈ <br>
**result :** κΈ°μ‘΄ pipeline λ°©λ²λ‘ λ³΄λ€ λ μ μ λΉμ©, λμΌν μμ λ°μ΄ν°λ‘ λ μ’μ κ²°κ³Ό<br>
**details :** [notion](https://long8v.notion.site/WYVERN-07583648be9c4620a7c13924b8ed7f4a)

## 2021-11-26 SQLova
SQLova: A Comprehensive Exploration on WikiSQL with Table-Aware Word Contextualization([arxiv](https://arxiv.org/pdf/1902.01069.pdf))<br>
**problem :** μμ°μ΄λ₯Ό SQLλ‘ λ³ννλ task(NL2SQL)μμμ BERT μ μ©. μ΄λ, ν΅μμ  seq2seqλ₯Ό ν΅ν μΈμ΄μμ±μ syntaxκ° μμ΄ NL2SQL λ¬Έμ μ μ ν©νμ§ μμ.<br>
**solution :** μμ°μ΄ μ§λ¬Έκ³Ό νμ΄λΈμ μ»¬λΌλ€μ `[SEP]`ν ν°μΌλ‘ concatνμ¬ BERTμ λ£μ. λ§μ§λ§ BERTμ λκ° layerμ biLSTM μ μ©νμ¬ μΏΌλ¦¬μ λ€μ΄κ°λ μμλ€(selectλ¬Έμ λ€μ΄κ°λ μ»¬λΌ λ±)μ μμΈ‘νλ 6κ°μ§μ λͺ¨λλ€μ λν μ°μ° μ§ν. <br>
**result :** SOTA, ν¬λΌμ°λ μμ± λΆμ κ²°κ³Ό human performacneλ³΄λ€ μ°μ.<br>
**details :** [notion](https://long8v.notion.site/SQLova-6e14c9fecc5a420b9394288b14a463f4)

## 2021-11-25 SPADE
SPADE: Spatial Dependency Parsing for Semi-Structured Document Information Extraction([arxiv](https://arxiv.org/pdf/2005.00642.pdf))<br>
**problem :** Information Extraction λ¬Έμ λ₯Ό ν λμ ν λ¬Έμ₯μΌλ‘ νΌμΉ λ€(serialize), μ¬κΈ°μ NER λ¬Έμ λ₯Ό νμ΄μμΌλ ν΄λΉ λ°©λ²λ‘ μΌλ‘λ λ³΅μ‘ν κ³΅κ°μ  κ΄κ³, λ¬Έμμ κ΅¬μ‘°μ  μ λ³΄λ₯Ό λ€λ£° μ μλ€λ λ¬Έμ κ° μμ <br>
**solution :** serialize λ¨κ³ μμ΄ κ° ν ν°λ€κ³Ό fieldλ₯Ό λΈλλ‘ λκ³  κ·Έ κ΄κ³λ₯Ό μ£μ§λ‘ νλ κ·Έλν(=κ΄κ³κ° μμΌλ©΄ 1, μμΌλ©΄ 0μΈ binary matrixλ‘ ννλ¨)μΈ λ₯Ό λ§λλ κ²μ λͺ©νλ‘ ν¨. κ° λΈλλ€μ attention μ°μ°μ ν΅ν΄μ encoding λκ³  μ£μ§λ€μ μΈμ½λ©λ λ²‘ν°λ€μ λ΄μ μ ν΅ν΄ νλ₯  κ°μ κ°μ§.<br>
**result :** BERT base NERκ³Ό λΉμ·νκ±°λ λμ μ±λ₯<br>
**details :** [notion](https://long8v.notion.site/SPADE-6018bae80a514fc5b75a962fc69e39fd)

## 2021-09-05 TSDAE
TSDAE: Using Transformer-based Sequential Denoising Auto-Encoder for Unsupevised Sentence Embedding Learning([arxiv](https://arxiv.org/abs/2104.06979))<br>
**problem :** STS λ°μ΄ν°μμ μ»λ κ²μ μ΄λ €μ°λ©°, finetuning μμ νμ€νΈ λλ©μΈμ μ°¨μ΄ λλ¬Έμ STSμ μ±λ₯μ΄ finetuningμ μ±λ₯μ λ°λμ λΉλ‘νλ κ²μ μλ<br>
**solution :** auto-encoderμ²λΌ encoderκ° λΈμ΄μ¦κ° μλ νμ€νΈλ₯Ό λ°μ μ μ°¨μμ λ²‘ν°λ‘ νννλ©΄ μ΄λ₯Ό decoderκ° noiseκ° μλ νμ€νΈλ‘ λ³ννλ κ΅¬μ‘°λ₯Ό κ°μ§<br>k μΈ΅μ self-attentionμ νκ³  Queryμ Valueλ λ¬Έμ₯μλ² λ©, Keyλ μ΄μ  (k-1)μΈ΅μ tμμ  λμ½λ νλ μ€νμ μ¬μ©ν¨ (BARTμ λ€λ₯΄κ² μΈμ½λμ λͺ¨λ  time-stepμ νλ λ²‘ν°κ° μ°Έμ‘° λμ§ μμ) <br>
**result :** unsupervised sentence embedding λ°©λ²λ‘ μΈ MLM, GloVe, Sent2Vecκ³Ό λΉκ΅νμ λ μ±λ₯μ μ°μ

## 2021-09-04 Faster R-CNN
Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Network([arxiv](https://arxiv.org/abs/1506.01497))<br>
**problem :** Objective Detectionμμ μ¬λ¬Όμ μμΉλ₯Ό μ°Ύλ Region Proposalλ¨κ³μμ selective searchκ° λλ¬΄ μ€λκ±Έλ¦Ό<br>
**solution :** CNN + anchorμΌλ‘ Region Porposalλ₯Ό ν λ€ μ΄ν ROI poolingκ³Ό classifierμ μμ°¨μ μΌλ‘ νμ΅μν΄. μ΄λ feature mapμ κ³΅μ νλ©° λμ lossλ ν©νμ¬ multi-task learning λ¨<br>
**result :** fast RCNNλ³΄λ€ μ±λ₯μ΄ κ°μ λ¬μΌλ©° μΆλ‘ μλλ 2λ°° μ΄μ λΉ¨λΌμ§<br>

## 2021-09-03 ViT
An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale ([arxiv](https://arxiv.org/abs/2010.11929))<br>
**problem :** Transformer κ΅¬μ‘°λ₯Ό image λλ©μΈμ μ μ©<br>
**solution :** μ΄λ―Έμ§λ₯Ό 16 by 16 blockμΌλ‘ λλ λ€ μ­ ν μλ² λ©μ positional embeddingμ λν λ€ νΈλμ€ν¬λ¨Έ μΈμ½λ + FCNμΌλ‘ κ΅¬μ±. μ΄ν `[CLS]`ν ν°μΌλ‘ μ΄λ―Έμ§ λΆλ₯ νμ€ν¬<br>
**result :** λΆλ₯ λ¬Έμ μμ SOTA. κ°μ₯ μλ λ μ΄μ΄μμλ κΈλ‘λ²ν μ λ³΄λ₯Ό μ¬μ©νκ³  μμμ μ μ μμμ. CNNλ³΄λ€ localityλΌλ inductive biasκ° μ μ<br>
**further work :** NLPμ²λΌ semi-supervised pretrainingμ νμ§ λͺ»ν¨

## 2021-09-01 LayoutLM
LayoutLM: Pre-training of Text and Layout for Document Image Understanding([arxiv](https://arxiv.org/pdf/1912.13318.pdf))<br>
**problem :** μ΄μ κΉμ§ λ¬Έμ κ΅¬μ‘°λ₯Ό νμ΅νκΈ° μν΄ νμ€νΈ/μ΄λ―Έμ§ μ λ³΄λ§μ νμ©νμμ<br>
**solution :** BERT μν€νμ³λ₯Ό νμ©νμ¬, μ’ν, νμ€νΈλ₯Ό μλ² λ©νμ¬ MLM, MDC(λ¬ΈμλΆλ₯)λ‘ νλ¦¬νΈλ μ΄λνκ³  λ°μ΄λ©λ°μ€λ΄ μ΄λ―Έμ§ μ λ³΄λ₯Ό Faster RCNNμμ featureλ₯Ό λ½μ κ²°ν©νμ¬ finetuning <br>
**result :** information extraction, document classification λ±μ νμ€ν¬μμ SOTA<br>

## 2021-08-30 BART
BART: Denoising Sequence-to-Sequence Pre-training for Natural Language Generation, Translation, and Comprehension([arxiv](https://arxiv.org/abs/1910.13461))<br>
**problem :** BERTλ νΈλμ€ν¬λ¨Έμ μΈμ½λλ§ μ¬μ©, GPTλ λμ½λλ§ μ¬μ©. λ λͺ¨λΈμ μΌλ°νλ λͺ¨λΈμ λ§λ€κ³  μΆμ <br>
**solution :** νΈλμ€ν¬λ¨Έμ encoder-decoder κ΅¬μ‘°λ₯Ό λͺ¨λ μ¬μ©νμ¬ noiseκ° λ€μ΄κ° νμ€νΈλ₯Ό μλ νμ€νΈλ‘ μλ³΅νλ©΄μ pre-trainingλ¨. fine-tuningμμλ inputκ³Ό ouputμ sdame inputμ λ£μ λ€ decoderμ λ§μ§λ§ ouputμ fcnμ λ£μ΄μ μ¬μ©ν¨<br>
**result :** MNLIλ₯Ό μ μΈνκ³  λͺ¨λ  GLUE  taskμμ BERTλ³΄λ€ μ°μ

## 2021-08-20 
Vocabulary Learning via Optimal Transport for Neural Machine Translation([arxiv](https://arxiv.org/pdf/2012.15671.pdf))<br>
**problem :** vocabularyλ₯Ό μ΄λ»κ² μ€μ νλμ§μ λν΄ λΉκ΅νλ κ²μ λν λΉμ©μ΄ λλ¬΄ ν¬λ©°, vocabμ λ°λΌ fine-tune μ±λ₯μ΄ λ¬λΌμ§ <br>
νμ¬ vocabμ μ μ νλ κΈ°μ€μ frequencyλ entropyκΈ°μ€μΌλ‘ ν΄λ¦¬μ€ν±νκ² μ€μ λ¨<br>
**solution :** κ²½μ νμ Marginal Utilityμ κ°λμ λΉλ €, Marginal Utility of Vocabularyλ₯Ό μ μνμ¬ μ΄λ₯Ό μ΅λννλ κ²μ λͺ©νλ‘ ν¨. MUVμ λ―ΈλΆκ°μ vocabμλ₯Ό λλ Έμ λ marginalνκ² λλ Έμ λ entropyμ μ°¨μ΄λ‘ λμ΄ μΌμ  spanμμ μ€μ΄λ  μνΈλ‘νΌκ° κ°μ₯ μμ κ°μμ MUVκ° μ΅λνλ¨.<br>
**result :** 1) κΈ°μ‘΄μ μ¬μ©λλ vocabλ³΄λ€ MT μ±λ₯μ΄ μ’μμ 2) ν΄λ¦¬μ€ν±νκ²(μ€ν) μ μ λ vocabκ³Ό μ±λ₯μ΄ μ μ¬νμμ 3) λ€κ΅­μ΄ vocabμμλ λ μ’μμ<br>
