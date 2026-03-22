---
title: "The Llama 3 Herd of Models "
date: 2024-11-15
tags: ['LLM', 'meta', '2024Q3']
paper: "https://scontent-nrt1-1.xx.fbcdn.net/v/t39.2365-6/463020162_522238820565582_8192401983671993921_n.pdf?_nc_cat=108&ccb=1-7&_nc_sid=3c67a6&_nc_ohc=6V_W4zoVlq0Q7kNvgHWuJ7j&_nc_zt=14&_nc_ht=scontent-nrt1-1.xx&_nc_gid=AyU86C3DYuf-4PmOosJFbYv&oh=00_AYDGekjv4Wb1d1PVWmRzuYLeVW9wLE9u4YJKFjCuah0Dew&oe=673CC719"
issue: 205
issueUrl: "https://github.com/long8v/PTIR/issues/205"
summary: "4D parallelism and more - an open source model for good performance. Optimization + exploration in many areas"
---
<img width="666" alt="image" src="https://github.com/user-attachments/assets/dc6c8b45-f694-4815-acc7-693c9333259b">

[paper](https://scontent-nrt1-1.xx.fbcdn.net/v/t39.2365-6/463020162_522238820565582_8192401983671993921_n.pdf?_nc_cat=108&ccb=1-7&_nc_sid=3c67a6&_nc_ohc=6V_W4zoVlq0Q7kNvgHWuJ7j&_nc_zt=14&_nc_ht=scontent-nrt1-1.xx&_nc_gid=AyU86C3DYuf-4PmOosJFbYv&oh=00_AYDGekjv4Wb1d1PVWmRzuYLeVW9wLE9u4YJKFjCuah0Dew&oe=673CC719), [page](https://ai.meta.com/research/publications/the-llama-3-herd-of-models/)

## TL;DR
- **I read this because.. :** 4D parallelism, etc. is often mentioned, so I thought I'd give it a try.
- **task :** foundation model
- Idea:** More data. More optimization. More modalities
- architecture :** Same as Llama2. The difference between using GQA and increasing vocab and increasing RoPE frequency is said to be the degree of increase. 8B, 70B, 405B three. // cross attention layer for vision
- **objective :** ce loss / DPO loss 
- **baseline :** llama2, claude, chatgpt, mistral, mixtral, gemini, gemma
- **data :** pretraining data, SFT data(via rejection sampling), RM data(human annotation), 
- **evaluation :** ..
- **result :** 
- **contribution :** A good performing open source model. Optimization + exploration in many areas
- **etc. :** It was fun to write down all the little details.

## Details
There's a lot of content, so organize by interest
### pretraining
- model arch
<img width="658" alt="image" src="https://github.com/user-attachments/assets/1bed1297-d839-4ab1-8125-2fc2fdb2d4ab">

- training recipe
It is said that starting with a low bs and gradually increasing the bs is good for performance stability (bs 4M tokens with 4096 length -> 8M sequences of 8192 length -> 16M ...
Increased the proportion of non-english and math data in the middle of the study.

- annealing data
Improved performance by showing more high-quality mathematical data at the end of the pretraining phase (24% and 6.4% improvement in GSM8K and MATH val, respectively)
You can also use it in reverse to do small data annealing and decide that it's not good data if it doesn't perform well.

- parallelism for model scaling
{TP, CP, PP, DP} -- TP has more frequent communication, so it's more likely to be used for
MFUs were reported to be between 38% and 43%.
<img width="658" alt="image" src="https://github.com/user-attachments/assets/83d30f6b-3b6b-426f-9a82-36d536a1b6e3">

The configuration looks like this TP: PP ratio is 1:2 and DP is just the rest!
PP improvements are also mentioned, such as applying an interleaved schedule to reduce bubbles, and letting one GPU handle the embedding of the first layer and the output prediction part at the end. Also, they used asynch point-to-point communication in PP.

I don't understand that BS is limited by the number of GPUs, but I solved it like below.

<img width="656" alt="image" src="https://github.com/user-attachments/assets/1466670a-5a53-4f67-8afc-dddf37659bea">

- numerical stability 
We cared about FP32 for reduce-scatter, FP32 for accum, etc.

- collective communication
He wrote a package called NCCLX, which is an improved version of NCCL. The main function is to tune data chunking / data transfer and to prioritize small control messages more.

### Post Training
- Reward Model
Learned to prefer data in the order edited > chosen > rejected. concatenated to process in one row and saw no performance degradation.

- SFT
RFT data + synthetic data + small amount of human-curated data
RFT data (represented by rejection sampling) K samples from the most recent model with human annotated prompts, rejected and used for training.
-> Says that most of the data was generated this way and went through multiple filters.

The synthetic data was mostly code-related, but the interesting thing was that they gave code snippets to diversify the prompts and said, 'Use this as inspiration to create prompts' + pretraining data to create QA forms.

- DPO 
Adopt DPO because it is more efficient than PPO at large-scale. At this point, we added the following changes
1) formatting token -- Improved the part that suddenly ends the answer or repeats at the end. It is said to improve the part where there is a conflict in loss when both win / reject have the same token.
2) regularization of NLL loss: 0.2 coeff was found to increase stability.

- Model averaging -- this is called averaging over multiple data and hyperparameters.
- Said to have done this... six other times.

## Visual Experiments
- Using ViT-H/14.
- Using cross-attention. In this case, to use the finegrained ability, we wrote the hidden of the {4, 9, 16, 24, 31}th layer as final layer feature
- Pretrain image-text pairs at scale 6B with anyres with a maximum of 4 grids at 336 x 336
- Later, similar to the language model, SFT + RM + DPO + very high quality data was used to train DPO.
- Benchmark performance
<img width="672" alt="image" src="https://github.com/user-attachments/assets/46227f98-dbd5-42e4-a8da-c01161db3e68">


---- 
Summary
The Llama 3 Herd of Models
With the unveiling of the Llama 3 405B model came the highly anticipated technical report. It's very interesting, with much more information than the Llama 2 report.
1. pre-training
It describes web data preprocessing in some detail. We used our own Main Content Extractor. I'm wondering if it means Global Deduplication when it says that they performed duplication on the entire data. In addition, CCNet-style Line Deduplication was used to remove additional boilerplate. Also used C4/Gopher style heuristic filters and filtering for outliers in the text distribution (probably LM based).
Quality filtering with fastText using Wikipedia as reference, DistilRobert classifier based on Llama 2 predictions.
DeepSeek-style web page extraction specialized for math and code domains.
Classify domains in web data using classifiers and determine data mix through scaling law estimation. 50% general knowledge, 25% math and reasoning related, 17% code, 8% multilingual.
Applying annealing at the end of training with high-quality data. Conversely, annealing can also be used to validate the quality of the dataset.
Applying masking to block attention between documents. Mentioned as useful for learning additional Long Context. Also applied Polyak Averaging.
Estimating the scaling law for downstream assignments by estimating the scaling law for the likelihood of the downstream assignment and then estimating the scaling law as a function of the likelihood and the score for the assignment.
Relaxed the batch size constraints of Pipeline Parallel and used all-gather-based Context Parallel instead of Ring.
2. post-training
The flow that starts with Reward Modeling and performs SFT and DPO with the data generated by Rejection Sampling. In other words, the model-generated data is the mainstay in the SFT stage without using PPO.
We used strong quality control on post-training data. We manually filtered the data, applied model-based quality filtering and difficulty-based scaling, and semantic duplication.
In the post-training phase, we worked on building specialized data for each domain.
2.1 Code
We started by building a code-specific model. We also leveraged repo-level data. Used feedback from compiler feedback and model-generated unit tests to improve and learn from the data.
Translate between different programming languages, describe, create, document, and debug code, have the model generate responses to challenges such as translation between different programming languages, and then translate back to the original code and filter using the quality of the output.
2.2 Multilingual
Train specialized models for multiple languages. Using NLP datasets and human-written prompts, applying Rejection Sampling and then rule-based quality filtering. Intentionally trying to exclude machine translation.
2.3 Math
Build prompts using pre-training data and humans. Generate CoT responses with the model, then validate against the model. Filtering using the Process Reward Model and, for difficult questions, generating responses using MCTS and the Process Reward Model.
2.4 Reasoning
Learn to solve reasoning problems using text and code. Correcting errors by using code execution feedback and modeling incorrectly generated results.
2.5 Long Context
The traditional approach of chunking a long document, then creating QAs for each chunk and merging them together, and then summarizing the chunks. For Python code, you can also do dependency sorting, clear the most referenced files, and then have it generate code from those files.
2.6 Using the tools
You've learned to use tools for web search, the Python interpreter, and Wolfram Alpha. This is the human-created data approach. However, synthetic data is used to build basic tooling skills before starting.
2.7 Factuality
Import documents from pre-training to generate questions and then sample responses. Evaluate the document and responses for accuracy and quality of information based on Llama 3. Generate a Refusal for consistently incorrect answers.
2.8 Steerability
Have annotators create system prompts, then let them proceed with the conversation and make annotations.
2.9 Safety
Build adversarial prompts with annotators and apply automatic red teaming.
3. vision, audio
For vision, Cross Attention to the image encoder, and for audio, the encoder output directly to the model input in Projection.
Impressions
Web data processing adopts methods that are now considered canonical at a high level. DeepSeek-style code and math domain data discovery proved to be an important tool. Additionally, systematic methods such as using scaling laws to determine data mix are interesting.
Proving that building a reliable and efficient learning infrastructure requires getting your hands dirty with communications and parallelism from the ground up.
Post-training is more heavily weighted towards Preference Data. SFT also consists mostly of training on rejection sampled data with Reward Model. In effect, training on online samples makes DPO alone without PPO a good enough choice.
Code execution/compiler feedback and Process Reward Model/MCTS become important components for code and math.
Each of the techniques mentioned in post-training could be an entire paper on its own, and post-training is a synthesis of all of them. In fact, this is also true for pre-training and building learning infrastructure: frontier models are currently being built by synthesizing a variety of cutting-edge techniques into a single model. This is something that is often overshadowed by explicit computational power like GPU numbers, but it suggests that effectively focusing these efforts is a very important factor.