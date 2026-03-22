---
title: "[15] Quantifying Memorization Across Neural Language Models"
date: 2022-03-24
tags: ['NLP', '2022Q1', 'privacy', 'LM']
paper: "https://arxiv.org/pdf/2202.07646.pdf"
issue: 15
issueUrl: "https://github.com/long8v/PTIR/issues/15"
---
![image](https://user-images.githubusercontent.com/46675408/160091748-b52f560c-9421-468e-9ac0-3e62893efa05.png)
[paper](https://arxiv.org/pdf/2202.07646.pdf)
**problem :**
As a model grows, it memorizes training data. We quantitatively evaluate how this phenomenon increases with 1) model size, 2) number of data iterations, and 3) length of the given context.

**conclusion :** 
![image](https://user-images.githubusercontent.com/46675408/159837370-b5c2dd4e-d3e3-4a2d-b240-149f93695c81.png)

1. Model scale: Within a model family, larger models memorize 2-5× more data than smaller models. 
2. Data duplication: Examples repeated more often are more likely to be extractable.
3. Context: It is orders of magnitude easier to extract sequences when given a longer surrounding context. -> In a good way, this means that it is harder to make an adversarial attack. Practitioners building language generation APIs could (until stronger attacks are developed) significantly reduce extraction risk by restricting the maximum prompt length available to users.

**details :**
- In the previous paper, the rate of memorizing training data was 0.00000015% of the training data, but in this paper, we found that at least 1% of the training data was memorized.
- There are roughly three ways to define memorization
1) One leading general memorization definition is differential privacy (Dwork et al., 2006), which is formulated around the idea that removing any user’s data from the training set should not change the trained model significantly.
2) counterfactual memorization (Feldman and Zhang, 2020; Zhang et al., 2021)
3) **Given k context tokens, if the string s that emerges through greedy decoding is in the training data** <- Definition adopted in this paper
if a model’s training dataset contains the sequence “My phone number is 555-6789”, and given the length k = 4 prefix “My phone number is”, the most likely output is “555-6789”, then we call this sequence extractable (with 4 words of context). 
- Since it's practically impossible to use the entire sequence as a query, we picked 50,000 queries, where we picked 1000 queries for each length of the repeated sequence for sequences of lengths 50, 100, ... 500.
- The model is GPT-Neo (125M, 1.3B, 2.7B, 6B) and the dataset is the Pile dataset (825GB, book, web, open source code). The model and dataset are among the largest publicly available. In this case, the model size - memorization relationship is log-linear.
- beam search (b=100) increased the extracted memory very slightly (average 2%, maximum 5.6%). 45% of the time, beam search and greedy gave the same result.
- We also ran experiments with T5 and C4. We defined memorization as perfect recovery of the masked LM. The overall trend was the same as GPT-Neo. However, model size - memorization was non-linear, with sequences repeated 140 times or less being significantly more likely to be memorized (than more repeated sequences), but this was due to the fact that these sequences had more spaces, making them easier to memorize (...)
- I also trained on C4 with repetitions removed for sequences longer than 50 tokens, and the probability of memorization decreased by 1/3.

**next papers :**
- training data extraction attacks (adversarial attack in LM)
- GitHub Copilot: Parrot or crow?
- Membership inference attacks against machine learning models.
- Understanding unintended memorization in federated learning.
- Calibrating noise to sensitivity in private data analysis

**thinkings :**
- There seems to be some model that prevents extraction in a similar way to GANs.
- Isn't privacy usually associated with numbers....
- I think augmentation might be the way to go, but let's think about a more fundamental solution.
- It says memorization != overfitting https://bair.berkeley.edu/blog/2019/08/13/memorization/
- Is this something we can't tackle by changing the way we decode?
- Or more memorization as you use teacher force?
 