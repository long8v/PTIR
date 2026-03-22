---
title: "[16] Counterfactual Memorization in Neural Language Models"
date: 2022-03-25
tags: ['NLP', '2021Q4', 'privacy', 'LM']
paper: "https://arxiv.org/pdf/2112.12938.pdf"
issue: 16
issueUrl: "https://github.com/long8v/PTIR/issues/16"
---
<img width="754" alt="image" src="https://user-images.githubusercontent.com/46675408/160056323-1d6ad0f0-105f-45b3-8e63-a578d6613cb4.png">

[paper](https://arxiv.org/pdf/2112.12938.pdf)
**problem :** Is the problem simply that the model memorized the phrases in the training data? If the phrases are common, that's fine, right? The problem is when the model memorized rare data.
**solution :** Divide the data into subsets and define bad memory as when the model performance changes significantly depending on whether a particular sample is present or absent.
**Counterfactual memorization measures the expected change in a model’s prediction when a particular example is excluded from the training set.** 
<img width="604" alt="image" src="https://user-images.githubusercontent.com/46675408/160054417-e8db1a2a-83f4-4329-ab64-2faf01459b66.png">
For each model, we sample the entire training data and train it independently. For each model, we measure the difference between the accuracy of predicting the next token on the model with a particular sample x (the IN model) and the accuracy of doing the same task on the model without the sample x (the OUT model).

More formally, we say a training example x is counterfactually memorized, when the model predicts x accurately if and only if the model was trained on x. 
1. We define counterfactual memorization in neural LMs which gives us a principled **perspective to
distinguish “rare” (episodic) memorization from “common” (semantic) memorization in neural LMs**
(Section 2).
2. We estimate counterfactual memorization on several standard text datasets, and confirm that rare
memorized examples exist in all of them. We study common patterns across memorized text in all
datasets and the memorization profiles of individual internet domains. (Section 3).
3. We extend the definition of counterfactual memorization to counterfactual influence, and study
the impact of memorized examples on the test-time prediction of the validation set examples and
generated examples (Section 4).

To measure Generation-Time Memorization, we check if the generated sequence is in the training data or compare the perplexity of LM if the training data is difficult to obtain. The difference between this memorization and the Counterfactual memorization we propose is that if there are many near-duplicates in the training data, they will not be measured as memorization because many will remain after removing a subset from our training set.
![image](https://user-images.githubusercontent.com/46675408/160090448-83d21bf7-0999-479c-b2c6-f920b2f1674f.png)
For the training sample with low counterfactual memory, we can see that there are a lot of repeated phrases (texts that are not highlighted in yellow in the last block).

In summary, generation-time memorization measures how likely a trained model would directly copy from the training examples, while counterfactual memorization aims to discover rare information that is memorized.

The model used T5, C4, RealNews, and Wiki. We built the model with a 25% subset of the training data.
<img width="863" alt="image" src="https://user-images.githubusercontent.com/46675408/160056001-c948a599-c42b-4149-be40-be8e6589454f.png">
The results of the experiment are shown above. I tended to memorize more specialty texts (all caps, tables, bullet lists, multilingual texts) than plain lines.

Similar to memorization, you can measure how much a sample has influenced the model, called Counterfactual Influence.
To measure this, you can use the
![image](https://user-images.githubusercontent.com/46675408/160085482-e7d14c13-07a1-44b4-833e-74600cfdfe7c.png)
We can do this The difference with the above formula is that to measure the impact of x on x', we measure it on x' for the subset with x and the subset without x. In other words, the above memorization measures the influence of x on itself.

In general, high memorization was associated with high influence, but not in all cases, and influence was noticeably lower for data with memorization above 0.4. The reason for this is that a high percentage of the data with high memorization was garbage text data (meaningless blah blah blah blah?), which had to be memorized in order to learn, but didn't learn any interesting information, so there was no information to influence.

The larger infl was, the more we saw that sentences in train (the subset with x) tended to be in valid (the subset without x), i.e., there were exactly the same sets in valid, so the influence on train must have been large.
![image](https://user-images.githubusercontent.com/46675408/160087330-e8e25958-c46f-4f85-a37c-6e490ec1e681.png)

In practice, the generation results for a large sample of influence and memorization looked like this
![image](https://user-images.githubusercontent.com/46675408/160091391-fd059123-4dfd-468d-a2b9-4f7f215ddbc3.png)

