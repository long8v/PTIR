---
title: "BBPE: Neural Machine Translation with Byte-Level Subwords"
date: 2022-02-18
tags: ['NLP', '2019', 'tokenizing', 'facebook', 'AAAI']
paper: "https://arxiv.org/pdf/1909.03341.pdf"
issue: 12
issueUrl: "https://github.com/long8v/PTIR/issues/12"
---
<img width="698" alt="image" src="https://user-images.githubusercontent.com/46675408/154601678-8904d7b3-9b89-4b24-b564-916177b61374.png">

[paper](https://arxiv.org/pdf/1909.03341.pdf)
**Problem :** When using BPE in a multi-lingual setting, the vocab count is eaten up by characters that don't appear well. In Chinese, some characters are part of other characters (虫, 蟲), and these relationships are hard to see at the character level.
**solution :** Encode the characters as 'utf-8' and then apply BPE.
**result :** 1) Similar performance to BPE with fewer parameters 2) Shorter sequence length than BPE, which makes it easier to train/inference faster 3) Easy to transfer learning (solves OOV problem)
**details :** 
- When multi-lingual, characters that don't appear well in Chinese or Japanese eat up vocab counts.
```
>>> '蟲'.encode('utf-8')
b'\xe8\x9f\xb2'
>>> '虫'.encode('utf-8')
b'\xe8\x99\xab'
```
```
>>> 'not'.encode('utf-8')
b'\xec\x95\x88'
>>> 'not'.encode('utf-8')
b'\xec\x95\x8a'
```
- Create a BPE vocab set via n-grams with utf-8 encoding
- encoding uses transformer
- Compared to encoders, decoders have a harder time applying BBPE because every character can be represented by a byte sequence, but the reverse can result in an invalid byte sequence. This rarely happened in the trained models.
- Halfway through our training, we realized that we were repeating bytes unnecessarily, so we created a system that circumnavigates this error pattern with as many characters as possible.
- We trained with multiple MT datasets, used beam search 4, and used tokenized BLEU ([sacreBLEU](https://github.com/mjpost/sacrebleu)) for evaluation.
- Symbol Frequency Distribution: Horizontal is symbol, vertical is frequency. BBPE has a more consistent distribution in frequency.
<img width="1071" alt="image" src="https://user-images.githubusercontent.com/46675408/154605740-975e9f91-30c6-4ccb-b550-9aee4ea389b2.png">

- Cross-Lingual Sharing: Different languages may have different ways of writing but share the same symbols.
<img width="558" alt="image" src="https://user-images.githubusercontent.com/46675408/154606441-84b25d7a-8a6b-4db3-a68c-e2bd9e88dd28.png">

- Impact on Sequence Length: Unlike BPE, BBPE has shorter units, which results in longer sequences and hence longer train and inference times. However, since it compresses like BPE, it is possible to have shorter sequences than BPE. (1/5 for X-En)
- BBPE on Nosiy Character Set : In En-De, there were a few sentences with nosiy, which was more wasteful because En-De has 30 alphabets. We found that BBPE performed similarly to BPE 32K at 2K and 4K, despite the smaller model size.
<img width="427" alt="image" src="https://user-images.githubusercontent.com/46675408/154608469-59ee8cc4-bdd2-40f3-bd69-2454be3336ad.png">

- BBPE on Character-Rich Languages
Languages like Chinese and Japanese have 50K characters, but only a small fraction of them are used a lot. In the Ja-En dataset, out of 7.9K characters, 2.4K characters accounted for 99.99% of the frequency. With BBPE, we used 4K, half of the total characters. The performance was similar to using 16K BPEs, with better performance on the big model.
<img width="546" alt="image" src="https://user-images.githubusercontent.com/46675408/154608950-a428f827-6d8b-4323-ac12-d048e15230e1.png">

- BBPE on Many-to-En Translation
In the multilingual setting, BBPE uses fewer parameters than BPE while improving performance. This may be because BBPE has a shorter sequence length, but that's okay because it performs better and is faster anyway ^^.
<img width="1032" alt="image" src="https://user-images.githubusercontent.com/46675408/154609130-f9e77b8a-0190-4638-9ae8-5ce1bd965e3d.png">

- Transfer Learning on Unseen Characters
Since BBPE has all utf-8 bytes and no OOV tokens, the BBPE model is transferable to other languages. On the other hand, character-based vocabularies need to change the vocabularies and learn from scratch when new characters are added. Transfer-learning with the BBPE model on Si(Sinhala)-En data, a character set that is not present in X-En, outperformed the baseline (even with no shared char).
<img width="509" alt="image" src="https://user-images.githubusercontent.com/46675408/154609805-753cb57f-6daf-4136-b43d-48780eff720d.png">