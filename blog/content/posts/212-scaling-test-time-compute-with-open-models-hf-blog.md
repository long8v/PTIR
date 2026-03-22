---
title: "Scaling Test-time Compute with Open Models (hf blog)"
date: 2024-12-23
tags: ['2024Q4', 'test-time-scaling', 'reasoning']
paper: "https://huggingface.co/spaces/HuggingFaceH4/blogpost-scaling-test-time-compute"
issue: 212
issueUrl: "https://github.com/long8v/PTIR/issues/212"
summary: "Reasoning side of the survey. Get recommended - organize and test methods"
---
<img width="700" alt="image" src="https://github.com/user-attachments/assets/e002f812-65ad-444e-b175-748b262501ac" />

[paper](https://huggingface.co/spaces/HuggingFaceH4/blogpost-scaling-test-time-compute)

## TL;DR
- **I read this because.. :** reasoning side survey. recommended by
- **task :** let's try test-time scaling
- **architecture :** Llama 3.2 1B instruct / Llama 3.2 3B instruct / Llama 3.1 70B 
- **baseline :** (infer) zero-shot CoT (PRM) Math-Shepherd
- **data :** (PRM) `RLHFlow/Llama3.1-8B-PRM-Deepseek-Data` 
- **evaluation :** Math-500 accuracy
- **result :** 
- **contribution :** Organizing and testing methods

## Details
### Strategies for test-time compute scaling
- self-refinement
refine their own outputs or “thoughts” by identifying and correcting errors in subsequent iterations
Must have built-in refinement capabilities
- Search Against a Verifier
Generation models with multiple answers and a separate verifier to choose between multiple answers
It could be a hard-coded verifier, but we assume it's a learned verifier (https://github.com/long8v/PTIR/issues/209)
If you have a verifier, it can be used in a BoN or tree search

<img width="727" alt="image" src="https://github.com/user-attachments/assets/69900b28-9390-4c49-b3d3-df43c31339bd" />

Possible methods
- Best-of-N: Generate multiple responses per problem and assign scores to each candidate answer, typically using a reward model. Then select the answer with the highest reward (or a weighted variant discussed later). This approach emphasizes answer quality over frequency.
- Beam search: A systematic search method that explores the solution space, often combined with a [process reward model (PRM)](https://huggingface.co/papers/2211.14275) to optimise both the sampling and evaluation of intermediate steps in problem-solving. Unlike conventional reward models that produce a single score on the final answer, PRMs provide a sequence of scores, one for each step of the reasoning process. This ability to provide fine-grained feedback makes PRMs a natural fit for search methods with LLMs.
- Diverse verifier tree search (DVTS): An extension of beam search we developed that splits the initial beams into independent subtrees, which are then expanded greedily using a PRM. This method improves solution diversity and overall performance, particularly with larger test-time compute budgets.

### Experimental setup

<img width="791" alt="image" src="https://github.com/user-attachments/assets/62a87b7e-83a1-4b4e-90ba-d6ffa04e0127" />

### Result
- majority voting / Self-consistency
<img width="726" alt="image" src="https://github.com/user-attachments/assets/e4ad2284-c7ff-454a-88f0-6c37813c7dde" />


- Best-of-N
The vanilla Best-of-N is when the RM selects the highest scoring child as the correct answer, and the Weighted Best-of-N is when the RM's score is weighted to select the correct answer.
It's common to use rm score as the ORM, but we'll use PRM for comparison.

<img width="735" alt="image" src="https://github.com/user-attachments/assets/a9f76e62-9227-4bba-bfaf-af464c44dc18" />

In this case, PRM gives a score per step, so the question is which score to use, and as in the [deep mind paper](https://huggingface.co/papers/2211.14275), Last is the best.

<img width="728" alt="image" src="https://github.com/user-attachments/assets/2551fe8b-2ac3-437e-9c46-141fe3fb9164" />

The weighted BoN was the best of the bunch. However, it still doesn't beat 8B zs-cot.

- Beam search with process reward models
1) Search for beams, keeping the number of beams N at each step.
2) Divide the step based on the stopping criterion defined as `\n` or `\n\n`, etc.
3) Scoring each step through PRM to select N out of M
4) Continue with 3
5) Proceed until EOS or MAX SEARCH is reached

An hparm looks like this
- N﻿ beams in compute scalings of 4, 16, 64, 256
- Fixed beam width m = 4
- Sampling with temperature T=0.8﻿
- Up to 40 iterations, i.e. a tree of maximum depth with 40 steps.
<img width="753" alt="image" src="https://github.com/user-attachments/assets/7a0abd94-aa74-4c0d-a0ba-54e8425ed5bb" />

Says he beat 8B and that his absolute math score is okay (CS PhD average is 0.4 (that's really hard...))

- when beam search works well?
<img width="744" alt="image" src="https://github.com/user-attachments/assets/f85f0342-ba33-4aff-a035-9d31c64bc6ee" />

Overall, Majority voting is the worst for computational complexity.
The harder the difficulty, the better beam search does, but for difficulties 1-2 it is worse than BoN or even majority voting

- DVTS: boosting performance with diversity
<img width="693" alt="image" src="https://github.com/user-attachments/assets/cbf046d5-8408-45b1-8bd4-2af8d77d7ad6" />

What's different from a tree is that when expanding M trees, it's different to grow trees independently (e.g. "A world" vs "A happy", when there are two paths alive, if N paths are drawn, A world is more promising, so N paths can be drawn, but it's a technique to expand by dividing N paths independently).

<img width="727" alt="image" src="https://github.com/user-attachments/assets/453f9bc8-c5f8-4a29-a725-14285a26c10c" />

This scales better as the number of answers grows!
<img width="704" alt="image" src="https://github.com/user-attachments/assets/887a1984-a7eb-4e4b-ae05-c5e082b20076" />

When separated by difficulty, DVTS did better when difficulty was low and N was large, and beam search did better when N was small, regardless of difficulty.
Additionally, beam search does better overall on the hardest difficulty level.

- compute optimal scaling
<img width="482" alt="image" src="https://github.com/user-attachments/assets/d1419039-3af6-451d-999f-e0c11ec24c38" />

The idea of being able to choose a strategy for a given compute budget N.
Since it's hard to get this, the deep mind researchers took the strategy of just looking at the difficulty level as a given, picking the best approach for each difficulty level, and then choosing that (??)
When you do this, the Performance

<img width="739" alt="image" src="https://github.com/user-attachments/assets/a10c327c-6a20-4ae3-82e2-cd45c8e9093d" />

- Scaling up to larger models
<img width="736" alt="image" src="https://github.com/user-attachments/assets/ccf2458f-d9c4-48e2-bc7e-a9b8ac924e7d" />

- next steps
1) The Power of Strong Verifiers:
Strong verifiers play a critical role in enhancing performance. However, their current limitations are apparent, as highlighted in benchmarks like ProcessBench. Improving the robustness and generalization of verifiers will be crucial for advancing these methods.

2) The Challenge of Self-Verification:
The ultimate goal—or "holy grail"—is achieving self-verification, where models can validate their own outputs autonomously. This approach appears to be what models like o1 are doing, but remains difficult to implement in practice. Unlike standard supervised fine-tuning (SFT), self-verification demands more nuanced strategies. The recent DeepMind paper on self-verification and Score sheds light on this challenge and offers a pathway for future research.

3) Integrating “Thoughts” into the Process:
Incorporating explicit intermediate steps or “thoughts” during generation could further enhance reasoning and decision-making. By integrating structured reasoning into the search process, we may unlock better performance on complex tasks.

4) Search as a Data Generation Tool:
This method can also serve as a powerful data generation process, creating high-quality training datasets. For example, fine-tuning models like Llama 1B on correct traces produced by search could yield significant gains. This on-policy approach resembles techniques like ReST or V-StaR but with the added benefits of search, offering a promising direction for iterative improvement.

5) A Call for More PRMs:
Open process reward models (PRMs) are relatively rare, limiting their broader application. Developing and sharing more PRMs for different domains is a critical area where the community can contribute significantly.

6) Expanding Beyond Verifiable Domains:
While current methods excel in domains like math and code, where solutions are inherently verifiable, extending these techniques to other areas remains a major challenge. How can we adapt these strategies for less structured or subjective tasks? This is a vital question for future exploration.

