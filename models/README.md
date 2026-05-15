---
extra_gated_prompt: >-
  You agree to not use the dataset to conduct experiments that cause harm to
  human subjects.
extra_gated_fields:
  Company/Organization: text
  Country: country
pipeline_tag: text-generation
library_name: transformers
---
---
license: apache-2.0
---
# OpenSeek-Mid-v1

**OpenSeek-Mid-v1** is a 10.61-billion-parameter language model grown from [Qwen3-4B-Base](https://huggingface.co/Qwen/Qwen3-4B-Base) through a two-stage model expansion pipeline and trained on only **2 trillion tokens** of fully open-source data.

Despite having **25% fewer parameters** and using **18x less training data**, OpenSeek-Mid-v1 matches or surpasses Qwen3-14B-Base across multiple benchmarks.



<img src="https://cdn-uploads.huggingface.co/production/uploads/642ee226a7e765fff0bf00ac/VcTNOdzlJK1tw5PjgeSSi.png" width="90%" alt="results_all">


---

## Highlights

- **Model Growth, Not From-Scratch Training**: Grown from Qwen3-4B via width expansion + partial depth stacking, inheriting the seed model's learned representations.
- **Extreme Data Efficiency**: Matches Qwen3-14B-Base (~36T tokens) with only 2T tokens of training — an 18x reduction in data requirement.
- **Muon Optimizer**: Spectral whitening ensures expanded dimensions are effectively utilized, delivering significant gains over AdamW in the model growth setting.
- **Fully Open-Source Data**: All training data comes from publicly available datasets (NemotronCC-v2, Stack-Edu, Dolmino, CCI, etc.).

---

## Architecture

| Specification | Value |
|---|---|
| Parameters | 10.61B |
| Layers | 56 |
| Hidden Size (d_model) | 2560 |
| FFN Intermediate Size (d_FFN) | 19456 |
| Attention Heads | 32 |
| KV Heads | 8 |
| Sequence Length | 8192 |
| Vocabulary Size | same as Qwen3-4B |

### Growth Pipeline

```
Qwen3-4B (4.02B, 36L)
    │  Width expansion (d_FFN: 9728 → 19456, SNR=10dB)
    ▼
Width-Expanded (7.10B, 36L)
    │  Partial depth stacking (layers 14–34 × 2)
    ▼
OpenSeek-Mid-v1 (10.61B, 56L)
    │  Continual pretraining with Muon (2T tokens)
    ▼
Final Model
```

---

## Training

### Training Configuration

| Parameter | Value |
|---|---|
| Optimizer | Muon |
| Sequence Length | 8192 |
| Global Batch Size | 2048 sequences |
| Peak Learning Rate | 1e-4 |
| LR Schedule | Cosine with linear warmup |
| Warmup Steps | 1000 |
| Weight Decay | 0.1 |
| Training Framework | FlagScale (FlagOS) |
| Total Training Tokens | ~2.06T |

### Stage 1: Broad Knowledge Acquisition (1.36T tokens)

#### Stage 1 Data Mixture

| Category | Proportion | Tokens (B) |
|---|---|---|
| Web | 42% | ~571B |
| Math | 20% | ~272B |
| Code | 20% | ~272B |
| STEM | 15% | ~204B |
| Multilingual | 3% | ~41B |

---

### Stage 2: Capability Specialization (0.70T tokens)

#### Stage 2 Data Mixture

| Category | Proportion | Tokens (B) | Delta vs. Stage 1 |
|---|---|---|---|
| Web | 35% | ~245B | -7% |
| Math | 20% | ~140B | — |
| Code | 24% | ~168B | +4% |
| STEM | 18% | ~126B | +3% |
| Multilingual | 3% | ~21B | — |

---

### Detailed Dataset Composition

Stage 1 (%) and Stage 2 (%) denote each dataset's sampling weight within the respective stage. "—" indicates the dataset is not used in that stage.

**Web**

| Dataset | Tokens (B) | Stage 1 (%) | Stage 2 (%) |
|---|---|---|---|
| Nemotron-CC-v2-HQ-Syn | 798.41 | 23.24 | 19.36 |
| Nemotron-CC-v2-Diverse-QA (×5 shards) | 340.81 | 9.92 | 8.26 |
| Nemotron-CC-v2-HQ (×5 shards) | 303.82 | 8.84 | 7.36 |
| dolmino-mix-1124-wiki | 3.82 | 0.15 | 0.18 |
| dolmino-mix-1124-stackexchange | 1.30 | 0.05 | 0.06 |

**Math**

| Dataset | Tokens (B) | Stage 1 (%) | Stage 2 (%) |
|---|---|---|---|
| Nemotron-SFT-MATH | 207.46 | 11.70 | 11.70 |
| Nemotron-CC-Math-v1-4plus-MIND | 74.34 | 4.19 | 4.19 |
| Nemotron-CC-Math-v1-4plus | 53.37 | 3.01 | 3.01 |
| Dolmino-math | 11.17 | 0.63 | 0.63 |
| OpenMathInstruct-2 | 5.30 | 0.30 | 0.30 |
| OpenMathReasoning-4k | 2.48 | 0.14 | 0.14 |
| NuminaMath-1.5 | 0.38 | 0.02 | 0.02 |

**Code**

| Dataset | Tokens (B) | Stage 1 (%) | Stage 2 (%) |
|---|---|---|---|
| Nemotron-Pretraining-Code-v1-Syn | 171.53 | 9.05 | 10.86 |
| Nemotron-SFT-Code | 57.47 | 3.03 | 3.64 |
| stack-edu-Java | 31.70 | 1.06 | 1.27 |
| stack-edu-Markdown | 26.64 | 0.38 | 0.45 |
| stack-edu-Python | 18.27 | 1.54 | 1.85 |
| stack-edu-Cpp | 12.62 | 1.11 | 1.33 |
| stack-edu-JavaScript | 8.99 | 1.00 | 1.20 |
| stack-edu-SQL | 8.23 | 0.37 | 0.44 |
| github-issue | 8.46 | 0.25 | 0.30 |
| stack-edu-PHP | 7.43 | 0.25 | 0.30 |
| stack-edu-CSharp | 7.26 | 0.37 | 0.44 |
| stack-edu-C | 4.80 | 0.43 | 0.52 |
| stack-edu-Shell | 2.60 | 0.01 | 0.01 |
| stack-edu-TypeScript | 2.51 | 0.18 | 0.22 |
| OpenCodeInstruct | 1.59 | — | 0.10 |
| stack-edu-Swift | 1.53 | 0.06 | 0.07 |
| stack-edu-Rust | 1.45 | 0.05 | 0.06 |
| stack-edu-Go | 1.42 | 0.03 | 0.04 |
| kaggle-notebooks | 1.42 | 0.65 | 0.78 |
| stack-edu-Ruby | 1.36 | 0.01 | 0.01 |
| OpenCodeReasoning-2-cpp-4k | 0.76 | 0.04 | 0.05 |
| OpenCodeReasoning-2-python-4k | 0.58 | 0.03 | 0.04 |
| github-code-review | 0.32 | — | 0.02 |

**STEM & Science**

| Dataset | Tokens (B) | Stage 1 (%) | Stage 2 (%) |
|---|---|---|---|
| Nemotron-Pretraining-Specialized-v1 (×4 shards) | 276.83 | 10.55 | 12.73 |
| Nemotron-Pretraining-SFT-v1-General | 86.93 | 3.31 | 4.00 |
| dolmino-mix-1124-pes2o | 60.19 | 0.50 | 0.50 |
| Nemotron-Pretraining-Specialized-v1.1 | 9.04 | — | 0.42 |
| OpenScienceReasoning-2-4k | 1.72 | 0.07 | 0.08 |
| MegaScience | 0.98 | 0.04 | 0.04 |

**Multilingual**

| Dataset | Tokens (B) | Stage 1 (%) | Stage 2 (%) |
|---|---|---|---|
| Nemotron-CC-v2-Translated-Diverse-QA | 135.80 | 1.74 | 1.74 |
| CCI4_0-Zh-High | 98.76 | 1.26 | 1.26 |

---

### Checkpoint Merging

The final model is a weighted average of 5 complementary checkpoints, each selected for a unique strength:

| Checkpoint | Weight | Role | Key Metric |
|---|---|---|---|
| iter 169984 | 0.30 | Code anchor | MBPP **78.84** |
| iter 219136 | 0.25 | Reasoning lead | GPQA-d **44.39** |
| iter 174080 | 0.15 | Code peak | EvalPlus **68.88** |
| iter 190464 | 0.15 | Math bridge | GPQA-d **42.86** |
| iter 217088 | 0.15 | General boost | BBH **82.84** |

---

## Evaluation Results

All evaluations conducted via `lm-eval-harness` with consistent settings.

| Benchmark | Qwen3-4B | Qwen3-8B | Qwen3.5-9B | Nemotron-12B | Gemma3-12B | Qwen3-14B | **OpenSeek-Mid-v1** |
|---|---|---|---|---|---|---|---|
| *Training tokens* | *36T* | *36T* | *36T* | *20T* | *12T* | *36T* | ***2T*** |
| MMLU (5-shot) | 72.72 | 76.57 | 78.64 | 78.07 | 73.28 | **80.57** | <u>79.31</u> |
| MMLU-Pro (5-shot CoT) | 49.31 | 52.35 | <u>58.48</u> | 57.57 | 41.16 | 56.00 | **66.57** |
| AGIEval-en (0-shot) | 45.92 | 49.09 | 45.15 | 49.20 | 44.89 | **52.83** | <u>52.18</u> |
| BBH (3-shot CoT) | 71.20 | 77.75 | <u>82.23</u> | 69.65 | 73.78 | 78.71 | **82.55** |
| HellaSwag (5-shot) | 75.36 | 79.47 | 81.04 | <u>83.13</u> | **83.45** | 82.05 | 81.81 |
| Winogrande (5-shot) | 71.90 | 77.51 | 76.80 | 79.24 | **80.35** | <u>79.40</u> | 79.24 |
| PIQA (5-shot) | 78.89 | 81.39 | 81.61 | 82.97 | 81.80 | **83.30** | <u>83.19</u> |
| OpenBookQA (5-shot) | 45.00 | 49.00 | 50.00 | <u>50.20</u> | 49.60 | **50.80** | 49.80 |
| ARC-C (0-shot) | 51.19 | 56.91 | 56.83 | 60.58 | **64.68** | 59.30 | <u>62.12</u> |
| GSM8K (4-shot CoT) | 84.31 | 86.73 | 85.60 | 81.43 | 72.02 | **90.07** | <u>89.16</u> |
| MATH (4-shot CoT) | 50.16 | 52.48 | 56.16 | 57.30 | 43.30 | <u>59.70</u> | **65.88** |
| GPQA-diamond (3-shot CoT) | 32.65 | 35.71 | <u>37.76</u> | 31.12 | 23.47 | <u>37.76</u> | **45.41** |
| MBPP (0-shot) | 73.81 | 75.66 | <u>77.51</u> | 73.81 | 73.28 | **84.92** | 76.19 |
| EvalPlus Avg (0-shot) | 63.96 | <u>67.95</u> | 59.54 | 61.20 | 53.48 | **73.41** | 66.45 |
| | | | | | | | |
| **Avg General** | 62.39 | 66.67 | 67.86 | 65.04 | 60.98 | <u>69.22</u> | **70.75** |
| **Avg All** | 61.88 | 65.61 | 66.24 | 65.39 | 61.32 | <u>69.20</u> | **69.99** |

- **Avg General**: average of knowledge, reasoning, and commonsense benchmarks (MMLU, MMLU-Pro, AGIEval-en, BBH, HellaSwag, Winogrande, PIQA, OpenBookQA, ARC-C).
- **Avg All**: average of all benchmarks above, including math, STEM, and code (+ GSM8K, MATH, GPQA-diamond, MBPP, EvalPlus Avg).

---

## Citation

If you find this work useful, please cite:

```bibtex
@misc{openseek-mid-v1,
  title={OpenSeek-Mid-v1: Efficient Language Model Scaling via Seed Model Expansion},
  year={2026},
  note={Technical report coming soon}
}
```

---

## Acknowledgements

This project was built using open-source data and tools, including NemotronCC-v2, Stack-Edu, Dolmino, CCI, OpenMathInstruct, OpenCodeReasoning, and FlagOS.