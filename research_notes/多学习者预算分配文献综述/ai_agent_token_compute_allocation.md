# Token/compute allocation across LLM agents and explore–exploit behaviour of LLM agents (2023–2026): notes for extending "Orchestrating Agent Teams: Budget Allocation in Real-Time Bidding" (Yang, Zhu & Mookerjee, WITS 2026) to AI-agent coordination

Conventions used below (read first):
- "The paper" means the WITS 2026 submission. A planner splits a fixed budget T across teams with values v1 > v2. Each team runs learn-then-exploit: a probing agent learns, then hands a summary statistic to an exploitation agent. Learning creates value only inside a bounded budget window. Learning shifts the split toward the junior team once both teams can afford to learn, and makes it more concentrated when only the senior team can.
- Each paper entry gives: the citation; what is allocated and across what; whether exploration or learning is modelled; the main results, including the shape of returns; and an Overlap rating (High/Medium/Low) for the planned extension. Lines starting "Relation (inference)" are my own analysis and are not sourced facts.
- I checked every arXiv ID, title, author list and date against the arXiv API (export.arxiv.org) or the paper's PDF text. Venues are given only where arXiv's comment or journal-ref field (or the PDF header) states them. Otherwise I write "venue not verified".
- Most 2026 items are arXiv preprints, not peer-reviewed. Numbers marked "(alphaXiv summary)" come from alphaXiv's AI-generated full-text report of the paper, not from the abstract. Treat them as slightly less certain.
- Web pages (Anthropic blog, Anthropic pricing, Intercom pricing) were accessed on 2026-11-06.
- Name collision: Jeremy Hadfield (an author of the Anthropic multi-agent blog post) is not Gillian K. Hadfield (co-author of "An Economy of AI Agents").

## Q1. Test-time compute allocation within a model: across queries, difficulty levels and reasoning steps (Snell, Damani, OSCA, s1, TALE and successors)

### Takeaway
A mature literature allocates inference compute (samples, thinking tokens, revisions) across prompts according to estimated difficulty. Typical gains are 2–4× efficiency, or up to 50% less compute at equal quality. Returns are strongly difficulty-dependent and often non-monotone: they saturate, follow an inverted U, or reverse. But almost all of this work allocates across independent queries with equal value, using one model, with no explicit "learn first, then exploit" phase. It is the "within-team production function" layer of the paper, not the planner layer.

### Cited Findings
- **Snell, Lee, Xu & Kumar (2024). "Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters." arXiv:2408.03314 (v1 6 Aug 2024; UC Berkeley / Google DeepMind; venue not verified).**
  - Allocates: a test-time generation budget (number of samples, revisions or beams; FLOPs-matched against pretraining) per prompt. The strategy is chosen per model-specific difficulty bin: five quantiles of pass@1, estimated from 2048 samples. — [arXiv:2408.03314](https://arxiv.org/abs/2408.03314)
  - Main result: a "compute-optimal" per-prompt strategy beats best-of-N while using up to 4× less test-time compute, for both revisions and PRM search. In a FLOPs-matched comparison, on problems where the small model has "somewhat non-trivial success rates", test-time compute can outperform a 14× larger model. — [arXiv:2408.03314](https://arxiv.org/abs/2408.03314)
  - Shape of returns:
    - Beam search beats best-of-N at low budgets, but "as the budget is scaled up, these improvements greatly diminish", often falling below best-of-N.
    - On easy questions, beam search degrades as the budget grows (over-optimization of the PRM).
    - On the hardest bin, "no method makes much meaningful progress".
    - At a given budget there is an ideal ratio of sequential to parallel compute. Easy questions do best with purely sequential compute; harder questions need a balance.
    - The authors frame parallel sampling as "more of a global search process" and sequential revision as "local refinement". — [arXiv:2408.03314](https://arxiv.org/abs/2408.03314)
  - Test-time and pretraining compute are "not 1-to-1 exchangeable". On the hardest questions, or with high inference load (R = D_inference/D_pretrain ≫ 1), extra pretraining is more effective. — [arXiv:2408.03314](https://arxiv.org/abs/2408.03314)
  - Exploration modelled: only implicitly (parallel sampling = exploring approaches). There is no environment learning.
  - Relation (inference) — Overlap: Medium. This is the canonical "allocate by difficulty" result plus an explore (parallel) vs refine (sequential) split inside one query. It supports the paper's claim that the value of extra budget depends on a window: compute helps only where the base success rate is non-trivial and the question is not trivially easy. It does not allocate across teams with different values.
- **Damani, Shenfeld, Peng, Bobu & Andreas (2024). "Learning How Hard to Think: Input-Adaptive Allocation of LM Computation." arXiv:2410.04707 (v1 7 Oct 2024; venue not verified).**
  - Allocates: decoding computation across inputs. The method predicts the distribution of rewards given an input and a computation budget, then "allocates additional computation to inputs for which it is predicted to be most useful". It is instantiated two ways: adaptive best-of-k (the number of samples sent to a reranker), and routing between an expensive-accurate and a cheap decoding procedure. — [arXiv:2410.04707](https://arxiv.org/abs/2410.04707)
  - Results: "reduce computation by up to 50% at no cost to response quality, or improve quality by up to 10% at a fixed computational budget" on programming, math and dialog. — [arXiv:2410.04707](https://arxiv.org/abs/2410.04707)
  - Exploration modelled: no; the predictor is learned offline.
  - Relation (inference) — Overlap: Medium. Formally this is a planner splitting a fixed budget across units by predicted marginal value, so it is close to the paper's planner. But the units are equal-value queries, and no unit has an internal learning phase.
- **Zhang, Zhou, Wang, Wang & Li (2024). "Scaling LLM Inference with Optimized Sample Compute Allocation" (OSCA). arXiv:2410.22480 (v1 29 Oct 2024; venue not verified).**
  - Allocates: the sample budget across inference configurations (model, temperature, language, etc.) and the number of samples per configuration, as a learned mixed allocation. — [arXiv:2410.22480](https://arxiv.org/abs/2410.22480)
  - Results: accuracy better than the best single configuration "with 128x less compute on code generation and 25x less compute on 4 reasoning tasks". On SWE-Bench (agentic), better accuracy with 3× less compute than the default configuration. — [arXiv:2410.22480](https://arxiv.org/abs/2410.22480)
  - Relation (inference) — Overlap: Low–Medium. This is portfolio allocation across heterogeneous "workers" (configurations). There is no test-time learning phase and no value heterogeneity.
- **Muennighoff, Yang, Shi, Li, Fei-Fei, Hajishirzi, Zettlemoyer, Liang, Candès & Hashimoto (2025). "s1: Simple test-time scaling." arXiv:2501.19393 (v1 31 Jan 2025; venue not verified).**
  - Allocates: thinking tokens per query via "budget forcing". The method either forces the end-of-thinking delimiter, or suppresses it and appends "Wait". — [arXiv:2501.19393](https://arxiv.org/abs/2501.19393)
  - Results: s1-32B (SFT on 1,000 examples) "exceeds o1-preview on competition math questions by up to 27% (MATH and AIME24)". Budget forcing extrapolates AIME24 "from 50% to 57%". — [arXiv:2501.19393](https://arxiv.org/abs/2501.19393)
  - Shape of returns:
    - The AIME24 gain "does eventually flatten out at six times" suppression.
    - "Suppressing the end-of-thinking token delimiter too often can lead the model into repetitive loops."
    - Further scaling is limited by the context window.
    - Rejection-sampling to length caps shows an inverse scaling trend (longer samples are more often wrong).
    - Prompt-only token-budget control fails because "our model cannot reliably count tokens". — [arXiv:2501.19393](https://arxiv.org/abs/2501.19393)
  - Relation (inference) — Overlap: Low. A single-agent budget knob, but clear evidence of saturation, i.e. an upper bound on the useful budget window.
- **Han, Wang, Fang, Zhao, Ma & Chen (2024). "Token-Budget-Aware LLM Reasoning" (TALE). arXiv:2412.18547 (v1 24 Dec 2024; venue not verified).**
  - Allocates: a per-problem token budget, dynamically adjusted to "the reasoning complexity of each problem" and placed in the prompt. The authors find that LLM reasoning "is unnecessarily lengthy" and can be compressed, but "the choice of token budget plays a crucial role". Token cost falls with only a slight performance reduction. — [arXiv:2412.18547](https://arxiv.org/abs/2412.18547)
  - Economic check by Erol et al. (Cost-of-Pass, ICLR 2026): TALE-EP gives frontier cost-of-pass reductions on several tasks, e.g. 66.6% on GSM8K and 50% on GPQA-Diamond. Majority voting (k=3, 4) gives 0% on every dataset tested. — [arXiv:2504.13359](https://arxiv.org/abs/2504.13359)
  - Relation (inference) — Overlap: Low.
- **Aggarwal & Welleck (2025). "L1: Controlling How Long A Reasoning Model Thinks With Reinforcement Learning." arXiv:2503.04697 (COLM 2025 per arXiv comment).** Length-Controlled Policy Optimization yields "smoothly trading off computational cost and accuracy". It "outperforms the state-of-the-art S1 method for length control", and a 1.5B L1 "surpasses GPT-4o at equal reasoning lengths". — [arXiv:2503.04697](https://arxiv.org/abs/2503.04697). Relation (inference) — Overlap: Low (it makes a sub-agent's token budget contractible).
- **Zuo & Zhu (2025). "Strategic Scaling of Test-Time Compute: A Bandit Learning Approach." arXiv:2506.12721 (to appear at ICLR 2026 per arXiv comment).**
  - Allocates: compute across queries, formulated as a bandit problem. The algorithms "estimate query difficulty on the fly and allocate compute accordingly". Among challenging queries they "learn to prioritize solvable instances, effectively reducing excessive computing on unsolvable queries". They provably beat uniform allocation in compute efficiency. — [arXiv:2506.12721](https://arxiv.org/abs/2506.12721)
  - Exploration modelled: yes, at the allocator level (online learning of difficulty).
  - Relation (inference) — Overlap: Medium. The allocator itself learns (explore/exploit across queries), whereas the paper's planner is ex ante and learning happens inside teams. "Do not fund unsolvable queries" is a lower-bound window condition.
- **Nguyen, Gupta & Le (2026). "Uncertainty-Aware Budget Allocation for Adaptive Test-Time Reasoning" (UAB). arXiv:2605.26849 (v1 26 May 2026).**
  - Two-phase protocol. In Phase 1, every question gets a small fixed number of generations; vote entropy gives a difficulty signal, and these generations also count toward the final vote. In Phase 2, the remaining budget is allocated by a marginal-greedy algorithm that "optimally solves a concave coverage-maximization surrogate".
  - Results: +2.3% average accuracy over uniform allocation, up to +5.5% on individual benchmarks, with "the largest gains in low-resource settings". — [arXiv:2605.26849](https://arxiv.org/abs/2605.26849)
  - Relation (inference) — Overlap: Medium. Structurally "probe, then allocate", with a fixed probing length. It relies on a concave surrogate, which is exactly the assumption the paper's learning window breaks.
- **Fan, Cheng, Li, Liang, Zhou & Feizi (2026). "Thinking Hard, Not Smart: Reasoning Models Fail to Ration Test-Time Compute Across Questions." arXiv:2608.07968 (v1 8 Aug 2026).**
  - Exam-style setting: a model must "distribute one shared token budget across questions with different difficulty and point values".
  - Models "fail to allocate a shared budget strategically". They "behave largely as greedy sequential solvers", "front-load effort on early questions, and remain insensitive to value", and these tendencies get worse as the number of questions grows. Planning prompts "spread compute more evenly but do not produce value- or difficulty-aware prioritization". — [arXiv:2608.07968](https://arxiv.org/abs/2608.07968)
  - Relation (inference) — Overlap: Medium. This is direct evidence that an LLM acting as its own planner does not solve the paper's value-weighted (v1 > v2) split. That motivates an explicit, model-based planner.
- **Wang, Jain, Zhang, Ray, Kumar & Athiwaratkun (2024). "Reasoning in Token Economies: Budget-Aware Evaluation of LLM Reasoning Strategies." arXiv:2406.06461 (venue not verified).** Complex strategies often do not beat simpler baselines "purely due to algorithmic ingenuity, but rather due to the larger computational resources allocated". CoT self-consistency with comparable compute "frequently outperforms" them. "Multi-agent debate or Reflexion can become worse if more compute budget is utilized." — [arXiv:2406.06461](https://arxiv.org/abs/2406.06461). Relation (inference) — Overlap: Low–Medium (matched-budget methodology; non-monotone returns for interactive strategies).
- **De Sabbata, Sumers, AlKhamissi, Bosselut & Griffiths (2024). "Rational Metareasoning for Large Language Models." arXiv:2410.05563.** The reward includes the Value of Computation, "penalizing unnecessary reasoning", and is trained with Expert Iteration. Result: "20-37% fewer tokens generated across three models while maintaining task performance". — [arXiv:2410.05563](https://arxiv.org/abs/2410.05563). Relation (inference) — Overlap: Low–Medium (VOC is the cognitive-science analogue of the value of learning).
- **Brown, Juravsky, Ehrlich, Clark, Le, Ré & Mirhoseini (2024). "Large Language Monkeys: Scaling Inference Compute with Repeated Sampling." arXiv:2407.21787.**
  - Coverage scales with the number of samples "over four orders of magnitude", often log-linearly ("exponentiated power law").
  - SWE-bench Lite rises "from 15.9% with one sample to 56% with 250 samples".
  - Without automatic verifiers, majority voting and reward models "plateau beyond several hundred samples". — [arXiv:2407.21787](https://arxiv.org/abs/2407.21787)
  - Relation (inference) — Overlap: Low–Medium (returns to paid attempts; coverage vs selection).
- **Wu, Sun, Li, Welleck & Yang (2024). "Inference Scaling Laws: An Empirical Analysis of Compute-Optimal Inference for Problem-Solving with Language Models." arXiv:2408.00724.** "Smaller models combined with advanced inference algorithms offer Pareto-optimal trade-offs". Llemma-7B with tree search "consistently outperforms the Llemma-34B model". — [arXiv:2408.00724](https://arxiv.org/abs/2408.00724). Relation (inference) — Overlap: Low (relevant to junior vs senior team substitution).
- **Chen, Davis, Hanin, Bailis, Stoica, Zaharia & Zou (2024). "Are More LLM Calls All You Need? Towards Scaling Laws of Compound Inference Systems." arXiv:2403.02419.** Vote and Filter-Vote performance "can first increase but then decrease as a function of the number of LM calls". The cause is a mix of "easy" queries (more calls help) and "hard" queries (more calls hurt). The optimal number of calls can be computed from a small number of samples. — [arXiv:2403.02419](https://arxiv.org/abs/2403.02419). Relation (inference) — Overlap: Medium (an explicit interior optimum: a bounded useful budget per unit).
- **Wu, Wang, Ye, Du, Jegelka & Wang (2025). "When More is Less: Understanding Chain-of-Thought Length in LLMs." arXiv:2502.07266.** Accuracy "typically follows an inverted U-shaped curve with CoT length". The optimal length "increases with task difficulty but decreases with model capability". — [arXiv:2502.07266](https://arxiv.org/abs/2502.07266). Relation (inference) — Overlap: Medium. A bounded window, and the window location depends on capability (a "senior" model needs fewer tokens).
- **Gema et al. (2025). "Inverse Scaling in Test-Time Compute." arXiv:2507.14417 (TMLR 12/2025 per journal-ref).** They construct tasks "where extending the reasoning length of Large Reasoning Models (LRMs) deteriorates performance" and identify five failure modes, e.g. "Claude models become increasingly distracted by irrelevant information". — [arXiv:2507.14417](https://arxiv.org/abs/2507.14417)
- **Chen et al. (2024). "Do NOT Think That Much for 2+3=? On the Overthinking of o1-Like LLMs." arXiv:2412.21187.** "Overthinking", in which "excessive computational resources are allocated for simple problems with minimal benefit". — [arXiv:2412.21187](https://arxiv.org/abs/2412.21187)
- **Bilal, Mohsin, Umer, Mohsin, Bilal & Hougen (2026). "Adaptive Replay Refinement: Allocating Test-Time Compute Between Revision and Resampling." arXiv:2610.28294.** ARR decides "Should I keep improving this solution, or ... try a completely new solution?". It detects when revision reaches a fixed point and reallocates the freed compute to a new independent sample. It matches majority voting on 3/5 math benchmarks at equal compute while cutting serial passes by up to 2.4×. — [arXiv:2610.28294](https://arxiv.org/abs/2610.28294). Relation (inference) — Overlap: Low–Medium (a stopping rule for exploit/refine vs explore/resample).
- **Alomrani et al. (2025). "Reasoning on a Budget: A Survey of Adaptive and Controllable Test-Time Compute in LLMs." arXiv:2507.02076.** A taxonomy separating "L1-controllability" (fixed compute budgets) from "L2-adaptiveness" (methods that scale inference with difficulty or confidence). — [arXiv:2507.02076](https://arxiv.org/abs/2507.02076)

### Inferences
- In this literature the "planner" allocates across queries, and its objective is total accuracy with equal weights. Damani et al. and Zuo & Zhu are the closest formally (allocation by predicted marginal value), but none weights units by heterogeneous output values v_i or embeds a probing phase inside each unit.
- Concavity is assumed in the allocation algorithms (UAB's concave surrogate, Damani's marginal allocation), yet the empirical curves are often non-concave or non-monotone: Chen et al.'s rise then fall, Wu et al.'s inverted U, Gema et al.'s inverse scaling, and s1's flattening. This tension is exactly where the paper's "learning window" adds value.
- Snell et al.'s "non-trivial success rate" condition and Zuo & Zhu's "skip unsolvable queries" are lower bounds of a useful-budget window. s1 flattening, the inverted U and overthinking are upper bounds.

### Gaps
- No work here models a within-query learning phase whose length is chosen together with the cross-query split.
- Venues for Snell, Damani, OSCA, s1 and TALE were not verified; only arXiv metadata was checked.

## Q2. Budget-aware LLM agents: the 2025–2026 literature (all seven specified arXiv IDs verified and read)

### Takeaway
In 2026 a cluster of papers made agents budget-aware over tokens, tool calls, steps and time. Most operate within a single agent, deciding how to spend across turns, and use reward shaping or learned shadow prices. Three of them give strong evidence on the shape of returns:
- Elo-per-token: concave in log tokens, with a measurable "inflection point" beyond which splitting the budget into fresh sessions wins.
- Think-more-or-read-more: sigmoidal, threshold-and-saturation ability curves, where communication or reading pays only when the gain exceeds the reasoning room it consumes.
- SPLIT: success saturates at verifier precision.

None models a planner splitting a budget across several learning agents with different values.

### Cited Findings
- **Lamb, Golinski, Gualdoni, Williamson & Kirchhof (2026). "Rewards for Budget-Aware Multi-Turn Agents That Adapt to Arbitrary Test-Time Constraints." arXiv:2610.28409 (v1 20 Oct 2026, cs.LG; Apple / University of Oxford).**
  - Allocates: one episode-level budget across the turns of a multi-turn agent. Budgets cover "tokens, API calls, and environment steps" (AppWorld) and turns (BabyAI). The policy is told its total and remaining budget each turn. Eleven reward objectives are compared on Qwen3.5 4B/9B, with one policy per environment and resource type, trained across budget values. — [arXiv:2610.28409](https://arxiv.org/abs/2610.28409)
  - Results:
    - Rewards that penalize overspending "substantially improve within-budget success and natural compliance over untrained models and over training on task success alone". Agents adapt "their resource use to stated budgets and task difficulty", and this generalizes to unseen budgets and zero-shot to a new benchmark.
    - A sigmoid overspend penalty most often achieves the highest within-budget success; a fixed negative reward gives the strongest compliance; "Dual" has the smallest average gap to the best method.
    - "Simply prompting an agent with an inference budget is not enough to make it adhere to that budget or succeed within it."
    - At step budget B = 36, the untrained 9B and 4B models reach only 37% and 19% budget utility. — [arXiv:2610.28409](https://arxiv.org/abs/2610.28409)
  - Exploration modelled: no explicit learning phase.
  - Relation (inference) — Overlap: Low–Medium. This is the within-team layer. It shows sub-agents can be trained to honour an allocated budget, which a planner's ex-ante split needs in order to be implementable. The authors note allocation "is usually left to external machinery ... planners, harnesses, or routers".
- **Yan, Zhang, Tan, Chen & Wang (2026). "PORA: Learning When More Reasoning Pays Off for LLM Agents." arXiv:2610.27119 (v1 19 Oct 2026, cs.AI).**
  - Allocates: the per-step choice between a short and a long reasoning allowance under a finite episode budget that "must support future steps" (later "evidence acquisition and verification").
  - Method: in training, two executions start from the same state, one with a short allowance (PRESERVE) and one with a long allowance (SPEND), and their final quality and total processing are compared. At inference, a controller "weighs this estimate against learned prices on remaining-budget pressure". — [arXiv:2610.27119](https://arxiv.org/abs/2610.27119)
  - Results: on BFCL memory, +17.4–32.9 pp over the strongest existing method. It matches or exceeds always-long reasoning on code and math with "50.6% fewer actor tokens and 31.2% fewer model requests". — [arXiv:2610.27119](https://arxiv.org/abs/2610.27119)
  - PORA's text also cites other per-step agent allocators: ARES (Yang et al., 2026), TAB ("learns turn-level budgets ... under a global token constraint", Jali et al., 2026) and Re-FORC (Zabounidis et al., 2026). — [arXiv:2610.27119](https://arxiv.org/abs/2610.27119) (these three are unverified by me)
  - Relation (inference) — Overlap: Medium. The learned positive "price" on remaining budget is the dynamic analogue of the planner's Lagrange multiplier. The trade-off between "think long now" and "keep budget for later evidence acquisition" is the within-team learn-vs-exploit timing problem.
- **Liu, Mang, Peng, Chai, Li, Pimpalgaonkar, Zettlemoyer, Dimakis & Cheung (2026). "When Agents Slow Down: Understanding LLM Agents' Test-Time Strategies via Elo-per-token Analysis." arXiv:2609.15309 (v1 14 Sep 2026; UC Berkeley, Princeton, UW, Bespoke Labs).**
  - Allocates: tokens. It studies "sessions of up to 100M tokens" and splits a fixed total between depth (one long session) and breadth (several independent sessions).
  - Agents: Kimi Code/K2.7, Codex/GPT-5.5, Claude Code/Opus 4.8 and Gemini CLI/Gemini 3.5 Flash, on 14 tasks from FrontierCS, ALE-Bench, MLS-Bench and FlashInfer-Bench. — [arXiv:2609.15309](https://arxiv.org/abs/2609.15309); details [alphaXiv summary](https://www.alphaxiv.org/abs/2609.15309)
  - Reference model: for independent sampling, "Elo grows linearly with log compute", with exactly 400 Elo per tenfold compute (alphaXiv summary). — [arXiv:2609.15309](https://arxiv.org/abs/2609.15309)
  - Shape of returns: agents "can initially convert tokens into Elo faster than independent sampling, but their marginal gains diminish and eventually fall below the reference". The later portions are concave in log compute. The strongest human contestants instead "improve superlinearly over contest time" ("continual learning"). Specialized harnesses (AdaEvolve, GEPA, test-time training) do not remove the diminishing returns (alphaXiv summary). — [arXiv:2609.15309](https://arxiv.org/abs/2609.15309)
  - Allocation rule: per-session budget = "scaling inflection point" (the point where marginal Elo equals the reference). Splitting 100M tokens this way on FrontierCS Polyomino gains "+264 Elo over one long session and +355 over ten short sessions". Per the alphaXiv summary, the inflection is ≈38M tokens, giving 3 sessions with 2,245 vs 1,981 vs 1,890 Joint-Elo. Predicting task-level inflection points without profiling remains unresolved. — [arXiv:2609.15309](https://arxiv.org/abs/2609.15309); [alphaXiv summary](https://www.alphaxiv.org/abs/2609.15309)
  - Exploration modelled: implicitly. Agents "explore alternatives, and decide when to stop", and a "sticky-basin" explanation is offered as a hypothesis.
  - Relation (inference) — Overlap: High for returns-shape evidence, Medium for allocation. This is an empirical analogue of a learning window: in-context adaptive learning beats fresh attempts only up to an inflection budget. It is a natural calibration target for a learning-window parameter. Unlike the paper, the split is across identical sessions of one task with no value heterogeneity.
- **Nguyen, Gupta & Le (2026). "Think More or Read More? A Token-Budget Theory of Reasoning with Shared Context." arXiv:2610.23246 (v1 16 Oct 2026, cs.CL; Deakin University).**
  - Allocates: one token window W per agent between reading and thinking. Reading is the question plus peers' messages (H tokens) plus overhead c, and thinking room is g = W − H − c. The theory chooses the debate group size n.
  - Votes are aggregated with a Condorcet jury model that allows correlated errors. The "synergy index" S(n) = δ√n_eff peaks at an interior n*, e.g. "n* = 4.9" on Qwen2.5-7B/GSM8K. — [arXiv:2610.23246](https://arxiv.org/abs/2610.23246)
  - Shape of returns (key evidence): "The cap sweeps are sigmoidal, near zero below the length a solution needs, rising sharply around it, then saturating. Held-out error selects the sigmoid family over the concave power law prior work adopts." The adopted Hill form is β_eff(g) = p_max·g^κ/(g^κ + g0^κ), where g0 can be read as a median solution length. A group that "reads past" the minimum thinking room "leaves too few tokens for reasoning and its accuracy collapses". — [arXiv:2610.23246](https://arxiv.org/abs/2610.23246)
  - Results:
    - At the predicted size there is only a 1.4% accuracy gap from a per-cell oracle, using 26–79 calibration questions.
    - "Self-consistency matches or beats deployed debate at 93% of 980 matched window-and-group-size settings"; debate is significantly ahead at only 0.5%.
    - "Communication pays only when the gain in the accuracy ceiling exceeds the reasoning room spent on reading, with this condition tightening as the window shrinks." — [arXiv:2610.23246](https://arxiv.org/abs/2610.23246)
  - Pricing ablation: with output-to-input price ratio r ∈ {1, 2, 2.5, 4}, "the interior optimum persists under realistic pricing, with cheaper input shifting n* upward at matched budget". On Qwen2.5-7B/MMLU-Pro the optimum stays pinned at n = 1 (a "g-floor effect"). — [arXiv:2610.23246](https://arxiv.org/abs/2610.23246)
  - Exploration modelled: reading peers is a costly form of learning from others, drawn from the same budget as thinking.
  - Relation (inference) — Overlap: High on mechanism. This is the closest formal statement that learning (reading) consumes the shared budget, pays only above a threshold, and has S-shaped returns. Those are the ingredients of the paper's bounded learning window. Differences from the paper: agents are symmetric with no value heterogeneity, and the setting is debate or self-consistency, not explore-then-exploit with a posterior.
- **Sun, Li, Hong, Fu & Xiao (2026). "One Policy, Any Budget: Internalizing Budget-Aware Search via Reinforcement Learning" (AnySearch). arXiv:2609.00813 (v1 1 Sep 2026; Fudan, Southeast, SJTU).**
  - Allocates: the number of external search calls (budget B) within a single search agent choosing among reason, search and answer actions.
  - Training: GRPO in two phases. Phase I uses an explicit budget-state scaffold. In Phase II the scaffold is removed and budgets are sampled adaptively. — [arXiv:2609.00813](https://arxiv.org/abs/2609.00813)
  - Results (alphaXiv summary):
    - Qwen2.5-7B average EM 0.431 vs StepSearch 0.403.
    - Accuracy increases "monotonically" with budget, including unseen budgets up to B = 8 (trained up to 5).
    - Retrieved documents are 51–68% of total token consumption.
    - The authors list modelling budget as a discrete count of searches, rather than a multi-dimensional cost, as a limitation. — [alphaXiv summary](https://www.alphaxiv.org/abs/2609.00813)
  - Relation (inference) — Overlap: Low–Medium. The exploration (search) budget of a single prober; it shows budget-proportional search strategies can be internalized by the agent.
- **Iyengar (2026). "Sample, Mix, or Verify? Allocating Test-Time Compute under Imperfect Verifiers" (SPLIT). arXiv:2610.23255 (v1 16 Oct 2026, cs.LG; Microsoft Research India).**
  - Allocates: a fixed budget across generators (models), sample counts, and verifier calls or thresholds. It uses an exact formula, P(success) = P(a correct candidate exists) × P(it is selected | it exists), with correlated verifier errors and shared blind spots. The formula is fitted "from a small labelled pilot" by empirical Bayes. — [arXiv:2610.23255](https://arxiv.org/abs/2610.23255)
  - Results:
    - Lands within 0.02–0.8 pp of the best allocation in hindsight, across 7 benchmarks, 26 models, 175 agent systems and 6 verifier kinds.
    - "Every fixed rule we test loses at least 2.5 points in some setting."
    - It stays near-optimal "under compute, price and latency costs".
    - "Verified success saturates at the verifier's precision however many samples are drawn". On MATH, majority voting stays near 43% while coverage reaches 98% (Llama-3-8B-Instruct). — [arXiv:2610.23255](https://arxiv.org/abs/2610.23255)
  - Relation (inference) — Overlap: Medium. The pilot is an explicit learning phase before allocation. The selection bottleneck (the exploiter cannot recognize the right answer) caps returns, which parallels exploitation being limited by the quality of the summary statistic.
- **Ning, Li & Kong (2026). "Agentic RAG Evaluation: Budget Allocation Across Questions, Trajectories, and Reads." arXiv:2610.05034 (v1 4 Oct 2026, cs.IR; CMU).**
  - Allocates: an evaluation budget of about 34.14–34.39M model tokens across questions Q, search trajectories T and repeated reads R. The nested variance model is V ≈ σ²_Q/Q + σ²_T/(QT) + σ²_R/(QTR). — [arXiv:2610.05034](https://arxiv.org/abs/2610.05034)
  - Results:
    - At equal model tokens, broader question coverage "lowers standard error by 33% versus five reads and 12.6% versus three trajectories", but needs 2.55× more search requests.
    - "Under recorded model fees, more questions beat more trajectories at search prices of $0–1 per 1,000 requests"; the question-vs-read fee ranking is unresolved.
    - Equal-dollar allocations "were not executed". — [arXiv:2610.05034](https://arxiv.org/abs/2610.05034)
  - Relation (inference) — Overlap: Low as a topic, but a clean demonstration that allocations equal in tokens are not equal in dollars once tool fees enter (see Q9).
- **Liu, Wang, Miao, Hsu, Yan, Chen, Han, Xu et al. (2025). "Budget-Aware Tool Use Enables Effective Agent Scaling" (Budget Tracker / BATS). arXiv:2511.17006 (COLM 2026 per arXiv comment; Google).** "Simply increasing the tool-call budget fails to improve performance, as agents lack 'budget awareness' and quickly hit a performance ceiling." A Budget Tracker plug-in plus BATS, which adapts planning and verification, gives "more favorable scaling curves". It uses "a unified cost metric that jointly accounts for token and tool consumption". — [arXiv:2511.17006](https://arxiv.org/abs/2511.17006). Relation (inference) — Overlap: Medium. Returns to a sub-agent's budget are endogenous to its budget awareness; the unified cost metric is relevant to Q9.
- **Lin, Wang, Liu, Shan, Bai, Zhang, Jin, Chen et al. (2026). "BAGEN: Are LLM Agents Budget-Aware?" arXiv:2606.00198 (v1 29 May 2026).**
  - Budget awareness is defined as "progressive interval estimation" of the remaining budget.
  - Findings: "strong agents do not necessarily have strong budget-awareness, with correlation r=0.35". Frontier models are "consistently over-optimistic, continue spending on tasks that are unlikely to succeed". "Early stop saves 28-64% tokens on failed trajectories". Interval coverage caps at 47% even after SFT+RL. — [arXiv:2606.00198](https://arxiv.org/abs/2606.00198)
  - Relation (inference) — Overlap: Medium for the cost structure: all-pay waste on failing runs, and sub-agents cannot self-estimate their needed budget.
- **Ma, Li, Chen, Li, Li, Guo, Lin & Chen (2026). "Timely Machine: Awareness of Time Makes Test-Time Scaling Agentic." arXiv:2601.16486.** Redefines test-time as wall-clock time because "tool latency decouples inference time from generation length". "Smaller models excel with fast feedback through more interactions, while larger models dominate high-latency settings". "Existing models fail to adapt reasoning to time budgets." — [arXiv:2601.16486](https://arxiv.org/abs/2601.16486). Relation (inference) — Overlap: Low–Medium (time vs tokens as the budget unit).
- **Zhu, Li, Wu, Xing, Ma, Tang, Liu, Yang et al. (2025). "Scaling Test-time Compute for LLM Agents." arXiv:2506.12928.** Scaling test-time compute improves agents; "knowing when to reflect is important"; list-wise verification and merging work best. — [arXiv:2506.12928](https://arxiv.org/abs/2506.12928). Overlap: Low.
- **Kapoor, Stroebl, Kirgis, Nadgir, Siegel, Wei, Xue, Chen et al. (2025). "Holistic Agent Leaderboard: The Missing Infrastructure for AI Agent Evaluation" (HAL). arXiv:2510.11977.** 21,730 rollouts, 9 models, 9 benchmarks, about $40,000 in total. Surprising findings include "higher reasoning effort reducing accuracy in the majority of runs". — [arXiv:2510.11977](https://arxiv.org/abs/2510.11977). Relation (inference) — Overlap: Medium (agent-level evidence that returns to reasoning tokens are not monotone).
- **Zeng, Lu, Cai, Jiang, Wu, Kung, Hu, Wang et al. (2026). "How Do AI Agents Waste Your Money?" arXiv:2611.07238 (v1 4 Nov 2026).** In online pruning, "we remove 41-46% of the model's reasoning while largely preserving task performance". "Waste varies more across tasks and agent settings than across models." — [arXiv:2611.07238](https://arxiv.org/abs/2611.07238). Overlap: Low–Medium (tokens are a noisy proxy for productive effort).

### Inferences
- The 2026 budget-aware agents literature works at the team level: one agent decides how to spend across turns, steps or tools. The learned remaining-budget prices (PORA) and overspend penalties (Lamb et al.) are Lagrangian devices. A planner in the paper's sense would sit one level up.
- Elo-per-token and Think-more-or-read-more give two complementary empirical windows:
  - An upper bound: past the inflection point, continuing to learn in context is worse than fresh attempts.
  - A lower bound: below a minimum thinking room, reading or communication destroys value.
  
  Together they make a "bounded budget window for learning" empirically plausible for LLM agents.
- The finding that sigmoidal fits beat concave power laws (Nguyen et al.) is direct evidence against the concavity assumptions used by allocators (ZEBRA, UAB), and supports modelling non-convex sub-agent production functions.

### Gaps
- None of the seven specified 2026 papers allocates across multiple sub-agents with heterogeneous values.
- None has a probing agent pass a summary statistic to a separate exploitation agent.
- The TAB, ARES and Re-FORC papers cited by PORA were not independently verified.

## Q3. Multi-agent orchestration with budgets: FutureWeaver, Agent Contracts, "On Time, Within Budget", ATOM, ZEBRA, budget conservation, AutoGen, Anthropic's research system, and the team-scaling evidence

### Takeaway
Several 2025–2026 systems have an orchestrator allocating a budget (USD, tokens or agent count) across sub-agents, phases or subtasks:
- FutureWeaver: adaptive, lookahead planning.
- ZEBRA: ex-ante knapsack with concave curves.
- AgentTTS and MCPP: subtask budgets.
- Cohere's coding teams: compute allocation across roles.
- ATOM: agent count set by query difficulty.

Anthropic's production system confirms that token spend is the dominant driver of research-agent performance (80% of BrowseComp variance) and that multi-agent systems use about 15× chat tokens. The controlled-comparison literature (Kim et al.; Tran & Kiela; Jwalapuram et al.) shows that at matched tokens, splitting a budget across agents often hurts unless the task decomposes or the agents bring new information. Exploration is never modelled as a priced, endogenous learning phase per sub-agent.

### Cited Findings
- **Jung, Shi, Chen & Zhang (2025). "FutureWeaver: Planning Test-Time Compute for Multi-Agent Systems with Modularized Collaboration." arXiv:2512.11213 (v1 12 Dec 2025; authors Dongwon Jung, Peng Shi, Muhao Chen, Yi Zhang; venue not verified).**
  - Allocates: test-time compute "in multi-agent systems under fixed budgets". The units are "collaboration modules" (callable functions wrapping multi-agent workflows, "automatically induced via self-play reflection") plus individual agents. A "dual-level planning architecture" combines "short-horizon action selection" with "long-horizon abstract lookahead". — [arXiv:2512.11213](https://arxiv.org/abs/2512.11213)
  - Details (alphaXiv summary):
    - An A*-like score combines short-term gain (self-consistency) with long-term feasibility (the share of speculative module trajectories that fit the remaining budget).
    - Budgets are in USD from AWS Bedrock token prices: $0.2–$0.5 for Claude 3.7 Sonnet/3.5 Haiku and $0.025–$0.3 for Qwen3-32B. Benchmarks are GAIA and BrowseComp-Plus; the metric is Acc@B.
    - It is best across all budgets. Baselines "consistently underutilized the available budget", and simply telling the orchestrator the budget in its prompt is insufficient. — [alphaXiv summary](https://www.alphaxiv.org/abs/2512.11213)
  - Exploration modelled: no explicit learning about an unknown state. Costs are learned offline via self-play, and lookahead is planning, not information acquisition.
  - Relation (inference) — Overlap: High on the problem setting. It is the closest system in which an orchestrator splits a fixed budget across sub-agents. It is adaptive rather than ex ante, has no value-heterogeneous teams, no closed-form insight, and no learning-window structure. Its result that baselines leave budget unspent is consistent with lumpy, threshold-type returns.
- **Hamri & Talgam-Cohen (2026). "ZEBRA: Zero-shot Budgeted Resource Allocation for LLM Orchestration." arXiv:2605.20485 (v1 19 May 2026; Tel Aviv University).**
  - Allocates: a continuous monetary budget across the "composing phases of a multi-agent pipeline", ex ante and zero-shot, "reduced to a continuous nonlinear knapsack problem". An LLM controller estimates per-phase utility curves, and "a water-filling search on the Lagrange multiplier returns the per-phase split". Additive and multiplicative aggregations share one solver. — [arXiv:2605.20485](https://arxiv.org/abs/2605.20485)
  - Assumptions and method (alphaXiv summary):
    - Each phase curve f_i is "non-decreasing, concave, and differentiable", with parametric form f_i(x) = a_i(1 − e^(−b_i x)).
    - The LLM elicits n_basic (tokens to reach about 50% quality) and n_great (about 90%), which are converted to USD.
    - The additive objective "starves phases where the initial marginal return (a_i b_i) falls below the shadow price λ". — [alphaXiv summary](https://www.alphaxiv.org/abs/2605.20485)
  - Results:
    - On a 150-task APPS benchmark at α = 0.5 of unconstrained spend, ZEBRA "recovers 94.4% of unconstrained quality, versus 88.1% for LLM-direct"; on a 3-phase HotpotQA pipeline it is +14.3 pp. — [arXiv:2605.20485](https://arxiv.org/abs/2605.20485)
    - Per the alphaXiv summary: at α = 0.8, 98.1% vs 94.3%. LLM-direct uses an essentially fixed split (about 25% implement, 50% refine), while ZEBRA's refine share rises from 30–45% on easy tasks to 60–66% on medium/hard tasks. A uniform split loses 5.1–5.9 points. Controller overhead is about 33% of budget at α = 0.5. Allocation is one-shot; online re-allocation showed no clear benefit in the tested pipeline. — [alphaXiv summary](https://www.alphaxiv.org/abs/2605.20485)
  - Exploration modelled: no.
  - Relation (inference) — Overlap: High. This is the most direct analogue of the paper's planner: an ex-ante split of a fixed budget across components whose marginal values differ, with corner solutions ("starving") at low budgets. The key contrast is the concavity assumption, which rules out the learning-induced non-convexity at the heart of the paper. With S-shaped curves (Q2, Nguyen et al.), water-filling can mis-allocate.
- **Samway, D'souza, Darwiche Domingues, Fadaee, Tan Yi-Chern & Dziri (2026). "Scaling Inference-Time Compute with Teams of Coding Agents." arXiv:2610.17471 (v1 12 Oct 2026; Cohere).**
  - Allocates: they "formulate team design as a compute allocation problem: starting from a solo agent, where should additional inference compute go". One at a time, they vary the stage at which a lead delegates (planning, implementation or verification), the models in the team, and the number of workers, on ProgramBench. — [arXiv:2610.17471](https://arxiv.org/abs/2610.17471)
  - Results:
    - Teams beat solo agents "but cost three to seven times as much".
    - A heterogeneous 17-agent team comes "within 1.4 points of a strong homogeneous 5-agent team at 70% lower cost".
    - "Planning is the most valuable use of workers": delegating only planning matches full delegation "at half the cost".
    - Cheap planners recover "47.5% of the reward gain of an all-strong team for only 13.9% of its additional cost, whereas cheap implementers lower reward".
    - "Planners keep improving reward as the team grows, whereas implementers and verifiers plateau beyond four workers." — [arXiv:2610.17471](https://arxiv.org/abs/2610.17471)
  - Relation (inference) — Overlap: High as empirical evidence. Planner-workers act like probing/exploration agents and the lead implements, which mirrors learn-then-exploit. Exploration is best given to cheap ("junior") agents and execution to strong ones, and execution roles plateau. There is no formal model and no value heterogeneity across tasks.
- **Anthropic Engineering — Hadfield, Zhang, Lien, Scholz, Fox & Ford (13 June 2025). "How we built our multi-agent research system."** The two claims the coordinator asked about are verified:
  - Architecture and performance: an orchestrator–worker design with Claude Opus 4 as lead agent and Claude Sonnet 4 subagents. It "outperformed single-agent Claude Opus 4 by 90.2% on our internal research eval". — [Anthropic](https://www.anthropic.com/engineering/multi-agent-research-system)
  - Variance claim: "three factors explained 95% of the performance variance" in the BrowseComp evaluation, and "token usage by itself explains 80% of the variance". The other two factors are the number of tool calls and model choice. — [Anthropic](https://www.anthropic.com/engineering/multi-agent-research-system)
  - Token multiples: "agents typically use about 4× more tokens than chat interactions, and multi-agent systems use about 15× more tokens than chats". — [Anthropic](https://www.anthropic.com/engineering/multi-agent-research-system)
  - Quotes on tokens and models: "Multi-agent systems work mainly because they help spend enough tokens to solve the problem", but "upgrading to Claude Sonnet 4 is a larger performance gain than doubling the token budget on Claude Sonnet 3.7". — [Anthropic](https://www.anthropic.com/engineering/multi-agent-research-system)
  - Effort-scaling heuristics in the lead agent's prompt: simple fact-finding uses 1 agent with 3–10 tool calls; direct comparisons use 2–4 subagents with 10–15 calls each; complex research uses more than 10 subagents. Early failures included "spawning 50 subagents for simple queries" and continuing "when they already had sufficient results". — [Anthropic](https://www.anthropic.com/engineering/multi-agent-research-system)
  - Compression and speed: "Subagents facilitate compression by operating in parallel with their own context windows", condensing information for the lead. Parallelization "cut research time by up to 90% for complex queries". — [Anthropic](https://www.anthropic.com/engineering/multi-agent-research-system)
  - Economics: multi-agent systems "require tasks where the value of the task is high enough to pay for the increased performance", and domains needing shared context or many dependencies "are not a good fit". — [Anthropic](https://www.anthropic.com/engineering/multi-agent-research-system)
  - Caveat: the 80% figure comes from Anthropic's analysis of its own BrowseComp runs, not a general law.
  - Relation (inference) — Overlap: High as practice and motivation. This is the production pattern the extension targets: explorer subagents compress findings, which act as the summary statistic, and the lead acts on them. Allocation is heuristic and value-aware only loosely ("value of the task high enough"). The 80% figure supports tokens as a first-order proxy, while the model-upgrade quote warns that model quality is a separate input.
- **Wang, Liu, Dai, Zeng, Zhang, Wu, Luo, Li et al. (2025). "AgentTTS: Large Language Model Agent for Test-time Compute-optimal Scaling Strategy in Complex Tasks." arXiv:2508.00890 (NeurIPS 2025 per arXiv comment).** Studies "test-time compute-optimal scaling in multi-stage complex tasks, aiming to select suitable models and allocate budgets per subtask". It notes the "combinatorial search space" and that "optimal model and budget allocations across subtasks are interdependent". An LLM-agent search over allocations driven by execution feedback outperforms baselines. — [arXiv:2508.00890](https://arxiv.org/abs/2508.00890). Relation (inference) — Overlap: Medium (cross-subtask budget split with interdependence; no learning phase; empirical search rather than theory).
- **Wang, Liu, Feng, Yuan, Li, Shi, Zhang, Tan, Zhang, Pan, Hu & Li (2026). "On Time, Within Budget: Constraint-Driven Online Resource Allocation for Agentic Workflows." arXiv:2605.06110 (v1 7 May 2026; BIT and Xiaohongshu).**
  - Goal: maximize "the probability that the entire workflow completes successfully under explicit budget and deadline constraints".
  - Inputs: "estimates of success rates and generation lengths for each subtask–model pair".
  - Method: the executor "dynamically allocates models and parallel samples across simultaneously executable subtasks". This is formulated as a "finite-horizon stochastic online allocation problem" and solved by Monte Carlo Portfolio Planning (MCPP), which "replans after observed outcomes". It is evaluated on CodeFlow and ProofFlow. — [arXiv:2605.06110](https://arxiv.org/abs/2605.06110)
  - Relation (inference) — Overlap: Medium. Online, probability-of-success allocation across subtasks with hard constraints. Learning is limited to replanning on realized outcomes, with no deliberate probing phase.
- **Zhao, Liu, Zhang, Ma, Lin, Wang, Cheng, Liu & Xu (2026). "ATOM: Instantiating Budget-Controllable Multi-Agent Collaboration via Nucleus-Electron Hierarchy." arXiv:2605.26178 (v1 25 May 2026; Zhejiang University, Xidian).**
  - Method: an offline-learned "nucleus" backbone plus query-conditioned "electron" agents, with "a complexity-aware budgeting strategy" that "estimat[es] query difficulty to strictly regulate electron instantiation". Token efficiency improves "by up to 30%". — [arXiv:2605.26178](https://arxiv.org/abs/2605.26178)
  - Per the alphaXiv summary:
    - Budget K(q) = ⌊K_max·C̄(q)⌋ electrons, where C̄(q) is a predicted complexity.
    - Pearson r = 0.737 between predicted complexity and token use.
    - A zero-budget (nucleus-only) ablation loses 6.61% on HumanEval; a fixed budget nearly doubles MMLU prompt tokens.
    - The authors name the problem the "average-complexity trap". — [alphaXiv summary](https://www.alphaxiv.org/abs/2605.26178)
  - Relation (inference) — Overlap: Low–Medium (agent count chosen by difficulty; no learning phase; no value weights).
- **Ye & Tan (2026). "Agent Contracts: A Formal Framework for Resource-Bounded Autonomous AI Systems." arXiv:2601.08815 (cs.MA; v1 13 Jan 2026, v3 25 Mar 2026). Zhu & Wang's reference list says it was accepted as an oral at COINE 2026, co-located with AAMAS 2026.**
  - Contracts unify "input/output specifications, multi-dimensional resource constraints, temporal boundaries, and success criteria". "Conservation laws" ensure "delegated budgets respect parent constraints".
  - Results: "90% token reduction with 525x lower variance in iterative workflows, zero conservation violations in multi-agent delegation". — [arXiv:2601.08815](https://arxiv.org/abs/2601.08815); venue per [arXiv:2610.00349](https://arxiv.org/abs/2610.00349)
  - Relation (inference) — Overlap: Low–Medium. This is the governance layer that makes an ex-ante split enforceable (Σ child budgets ≤ parent budget). It does not optimize the split.
- **Zhu & Wang (2026). "Fault-Tolerant Budget Conservation in Distributed Multi-Agent Delegation." arXiv:2610.00349 (v1 29 Sep 2026, cs.AI; Accentrust / Georgia Tech / UIUC).**
  - Budgets are "quantized resource vectors represented by exclusive escrow credits" moving through a delegation DAG. "Uncertain effects remain charged until authenticated settlement".
  - Key point: "Allocation safety is not execution safety." Their example: a timeout refund followed by a late completion lets three effects consume a two-effect authorization. Properties are checked with TLA+.
  - The paper cites a catalog of "63 production budget overruns" (Khan 2026). — [arXiv:2610.00349](https://arxiv.org/abs/2610.00349)
  - Relation (inference) — Overlap: Low. Enforcement, but it shows that in agent systems costs are committed before outcomes are known (all-pay under uncertainty).
- **Wu, Bansal, Zhang, Wu, Li, Zhu, Jiang, Zhang et al. (2023). "AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation." arXiv:2308.08155.** An open-source framework of "conversable" agents with programmable interaction patterns. The abstract describes no budget-allocation mechanism. — [arXiv:2308.08155](https://arxiv.org/abs/2308.08155). Relation (inference) — Overlap: Low (infrastructure where a planner could be implemented).
- **Kim, Gu, Park, Park, Schmidgall, Heydari, Yan, Zhang et al. (2025). "Towards a Science of Scaling Agent Systems." arXiv:2512.08296 (v1 9 Dec 2025, v3 Apr 2026; Google Research, Google DeepMind, MIT).**
  - Design: 260 configurations, 6 agentic benchmarks, 5 architectures and 3 LLM families. All configurations were "matched for total reasoning-token budget (mean 4,800 tokens per trial)" and tool access. — [arXiv:2512.08296](https://arxiv.org/abs/2512.08296)
  - Capability ceiling: "tasks where single-agent performance already exceeds 45% accuracy experience negative returns from additional agents". This is the most robust finding.
  - Tool-coordination trade-off: β = −0.096, because "multi-agent systems fragment the per-agent token budget".
  - Error amplification: 17.2× for independent architectures vs 4.4× for centralized ones.
  - Range of effects: from +80.8% (Finance-Agent, centralized) to −70.0% (PlanCraft, independent). — [arXiv:2512.08296](https://arxiv.org/abs/2512.08296)
  - Shape: turns scale as T = 2.72·(n+0.5)^1.724. "Under fixed computational budgets, per-agent reasoning capacity becomes prohibitively thin beyond 3–4 agents." Message density saturates logarithmically, S = 0.73 + 0.28 ln(c), plateauing near 0.39 messages per turn. Decentralized coordination helps "parallel exploration of high-entropy search spaces (dynamic web navigation: +9.2%)". — [arXiv:2512.08296](https://arxiv.org/abs/2512.08296)
  - Relation (inference) — Overlap: Medium. Clean evidence of a fragmentation cost when a fixed token budget is split across agents. Once per-agent budget falls below what reasoning needs, splitting hurts, which is the multi-agent version of "cannot afford to learn".
- **Tran & Kiela (2026). "Single-Agent LLMs Outperform Multi-Agent Systems on Multi-Hop Reasoning Under Equal Thinking Token Budgets." arXiv:2604.02460 (v1 2 Apr 2026).** A Data Processing Inequality argument: "under a fixed reasoning-token budget and with perfect context utilization, single-agent systems are more information-efficient". Multi-agent systems "become competitive when a single agent's effective context utilization is degraded, or when more compute is expended". Single-agent systems "consistently match or outperform" multi-agent ones under matched budgets. The authors also flag "artifacts in API-based budget control (particularly in Gemini 2.5)". — [arXiv:2604.02460](https://arxiv.org/abs/2604.02460). Relation (inference) — Overlap: Medium. Splitting a budget across sub-agents pays only if they add information, e.g. by exploring separate contexts, which is the paper's "learning must create value" condition.
- **Anchan & Sen (2026). "Attention Tax, Handoff Tax: A Stylised Model of When Multi-Agent LLM Systems Help." arXiv:2610.06069 (v1 5 Oct 2026, cs.MA).**
  - Model: step failure probability ε(c, b) depends on context load c and thinking budget b. Decomposition gives each agent a fresh context at "handoff loss h". Redundancy uses N parallel calls with shared failures. — [arXiv:2610.06069](https://arxiv.org/abs/2610.06069)
  - Results:
    - Decomposition wins past a crossover depth, which exists iff "the curve's asymptotic rise above a fresh agent's operating point exceeds one handoff's cost".
    - Parallel sampling at equal budget eventually wins iff its "shared-failure floor lies below the error floor of one agent thinking longer".
    - On a ledger task the predicted crossover is at depth 10. Decomposition wins at depths 20/50/100, within 9 pp of the predicted rate. — [arXiv:2610.06069](https://arxiv.org/abs/2610.06069)
  - Relation (inference) — Overlap: Medium. A stylized reliability model with threshold crossovers. Its "handoff tax" is the cost of passing a compressed summary between agents, the analogue of the paper's summary-statistic handoff.
- **Ao, Gao & Simchi-Levi (2026). "On the Reliability Limits of LLM-Based Multi-Agent Planning." arXiv:2603.26993 (v2 "substantially revised").**
  - Specialists report to a coordinator through "finite reports", and the coordinator "can revisit source records" at a reading cost.
  - Results: "two report forms suffice for a broad class of allocation requirements". "Identical specialists can optimally report different facts." "Maximizing immediate completion can impose an unbounded recovery cost penalty." — [arXiv:2603.26993](https://arxiv.org/abs/2603.26993)
  - Anchan & Sen describe Ao et al. as proving that without new exogenous signals any delegated network is dominated by a centralized Bayes decision maker with the same information. That is the citing paper's characterization; the v2 abstract does not state it. — [arXiv:2610.06069](https://arxiv.org/abs/2610.06069)
  - Relation (inference) — Overlap: Medium (an operations-research theory of report or summary-statistic design in delegation).
- **Park, Kontonis, Garg, Krishnamurthy & Papailiopoulos (2026). "Scaling Discovery through Test-Time Communication." arXiv:2609.21032.** A team of k communicating agents "matches the success rate of 4k independent agents" on ARC-AGI-3, and the advantage grows with k. But "independent agents may outperform communication when compute is limited or when a clear measure of progress is absent". — [arXiv:2609.21032](https://arxiv.org/abs/2609.21032). Relation (inference) — Overlap: Medium. Learning spillovers across agents pay only above a compute threshold, the lower edge of a learning window. This is relevant if the extension relaxes independence between teams.
- **Yang, Qu, Wen, Shi, Wen, Zhang, Wierman & Gu (2026). "Understanding Agent Scaling in LLM-Based Multi-Agent Systems via Diversity." arXiv:2602.03794.** Homogeneous scaling "exhibits strong diminishing returns". Performance "is bounded by the intrinsic task uncertainty, not by agent count". "2 diverse agents can match or exceed the performance of 16 homogeneous agents." — [arXiv:2602.03794](https://arxiv.org/abs/2602.03794). Overlap: Low–Medium.
- **Jwalapuram, Lin, Li, Jiao, Wang, Ming, Ke, Qin et al. (2026). "The Illusion of Multi-Agent Advantage." arXiv:2606.13003.** "Automatic MAS consistently underperform CoT-SC despite being up to 10x more expensive"; expert-designed multi-agent systems do better on a diagnostic decomposition dataset. — [arXiv:2606.13003](https://arxiv.org/abs/2606.13003). Overlap: Low–Medium.
- **Xu, Koesdwiady, Bei, Han, Huang, Wang, Chen, Wang et al. (2026). "Rethinking the Value of Multi-Agent Workflow: A Strong Single Agent Baseline" (OneFlow). arXiv:2601.12307.** "A single agent can reach the performance of homogeneous workflows with an efficiency advantage from KV cache reuse." Heterogeneous workflows cannot be simulated this way "due to the lack of KV cache sharing across different LLMs". — [arXiv:2601.12307](https://arxiv.org/abs/2601.12307). Overlap: Low–Medium (cache economics favour fewer contexts).
- **Bertalanic & Fortuna (2026). "An Exact Generate - Transform Decomposition of Small-LLM Team Scaling Across Orchestration Architectures." arXiv:2609.36104.** From 3 to 30 calls, accuracy rises "by up to 17 points" on GSM8K/GSMHard but "by at most four on ARC, GPQA, and MMLU". "At equal call budgets token cost still varies 2.1x." — [arXiv:2609.36104](https://arxiv.org/abs/2609.36104). Overlap: Low–Medium.
- **Wunderlich, Kaesberg, Wahle, Ruas & Gipp (2026). "Multi-Agent Reasoning Improves Compute Efficiency: Pareto-Optimal Test-Time Scaling." arXiv:2605.01566 (ACL 2026 SRW per arXiv comment).** At equal compute, debate and mixture-of-agents beat self-consistency by 1.3 and 2.7 points. "Self-consistency saturates earlier, multi-agent gains persist". The gain is up to +7.1 points over chain-of-thought at 20× the CoT budget. — [arXiv:2605.01566](https://arxiv.org/abs/2605.01566). Overlap: Low–Medium.
- **Qian, Xie, Wang, Liu, Zhu, Xia, Dang, Du et al. (2024). "Scaling Large Language Model-based Multi-Agent Collaboration" (MacNet). arXiv:2406.07155 (ICLR 2025 per arXiv comment).** A "collaborative scaling law": "the overall performance follows a logistic growth pattern as agents scale". — [arXiv:2406.07155](https://arxiv.org/abs/2406.07155). Overlap: Low (S-shaped returns in agent count).
- **Li, Zhang, Yu, Fu & Ye (2024). "More Agents Is All You Need." arXiv:2402.05120 (TMLR per arXiv comment).** Sampling-and-voting performance "scales with the number of agents", and "the degree of enhancement is correlated to the task difficulty". — [arXiv:2402.05120](https://arxiv.org/abs/2402.05120). Overlap: Low.
- **Smit, Duckworth, Grinsztajn, Barrett & Pretorius (2023). "Should we be going MAD? A Look at Multi-Agent Debate Strategies for LLMs." arXiv:2311.17371 (venue not verified).** Multi-agent debate does "not reliably outperform other proposed prompting strategies, such as self-consistency". — [arXiv:2311.17371](https://arxiv.org/abs/2311.17371)
- **Cemri, Pan, Yang, Agrawal, Chopra, Tiwari, Keutzer, Parameswaran et al. (2025). "Why Do Multi-Agent LLM Systems Fail?" arXiv:2503.13657.** Multi-agent performance gains "are often minimal". The MAST taxonomy has 14 failure modes from 1600+ traces across 7 frameworks (kappa 0.88). — [arXiv:2503.13657](https://arxiv.org/abs/2503.13657)
- **Ding, Wang, Ruan, Lu, Ge, Fang & Lin (2026). "MS-Eval: Benchmarking Sub-Agent Delegation and Orchestration in MCP-Intensive Working Scenarios." arXiv:2610.22869.** Main-agent delegation with sub-agent execution "generally raises cost with contingent payoff"; "unnecessary or redundant delegation turns the same cost into pure overhead". — [arXiv:2610.22869](https://arxiv.org/abs/2610.22869)
- **Tang, Liang, Jiang & Dong (2025). "On the Importance of Task Complexity in Evaluating LLM-Based Multi-Agent Systems." arXiv:2510.04311.** The multi-agent benefit "increases with both task depth and width", and more so with depth. — [arXiv:2510.04311](https://arxiv.org/abs/2510.04311)
- **Meyerson, Paolo, Dailey, Shahrzad, Francon, Hayes, Qiu, Hodjat & Miikkulainen (2025). "Solving a Million-Step LLM Task with Zero Errors" (MAKER). arXiv:2511.09030.** Over one million LLM steps with zero errors via "extreme decomposition" into microagents plus per-step voting. — [arXiv:2511.09030](https://arxiv.org/abs/2511.09030)
- **Su & Wu (2026). "When Do Multi-Agent Systems Outperform? Analysing the Learning Efficiency of Agentic Systems." arXiv:2602.08272.** In PAC sample-complexity terms, "MARL improves sample complexity when tasks naturally decompose into independent subtasks, whereas dependent subtasks diminish MARL's comparative advantage". — [arXiv:2602.08272](https://arxiv.org/abs/2602.08272). Relation (inference) — Overlap: Medium (a formal learning-efficiency argument for splitting learning across agents when subtasks are independent, like the paper's independent teams).
- **Xie, Hua, He, Karne, Agrawal, Pagonas, Wu, Kaffes et al. (2026). "Which Model for Which Role? Cost-Efficient Pareto Recommendation for LLM Agentic Workflows" (CC-Gittins). arXiv:2610.26676 (preliminary version at the NeurIPS 2026 RAAAI workshop per arXiv comment).** A cost-aware Gittins search over role-to-model assignments recovers "a substantial fraction of the true Pareto frontier at roughly 10% of the exhaustive-evaluation cost". — [arXiv:2610.26676](https://arxiv.org/abs/2610.26676). Overlap: Low–Medium (explore/exploit at system-design time).
- **Zhou, Leonardis & Feng (2026). "Agora: Enhancing LLM Agent Reasoning Via Auction-Based Task Allocation." arXiv:2607.09600 (EMNLP 2026 Findings per arXiv comment).** A "confidence-calibrated auction" allocates reasoning steps, "tradeable items", to expert models and tools. — [arXiv:2607.09600](https://arxiv.org/abs/2607.09600). Overlap: Low–Medium (market mechanism).
- **Luo, Huang, Li, Luo, Deng, Wang, Xu, Hu et al. (2026). "Where Should the Evaluation Budget Go in LLM-Driven Agent Scaffold Evolution?" arXiv:2610.37276.** Splits an evaluation budget between search-time feedback and final selection. "Sparse feedback can sustain productive evolution, while additional targeted evaluation improves final selection", after a short fully evaluated warm-up. It uses about half the evaluation cells. — [arXiv:2610.37276](https://arxiv.org/abs/2610.37276). Overlap: Low–Medium (an explicit explore-vs-confirm budget split).
- **Wu, Jing, Yi, Hao, Yang, Chang, Wei, Yang et al. (2026). "TMAS: Scaling Test-Time Compute via Multi-Agent Synergy." arXiv:2605.10344.** An experience bank and a guideline bank help "balance exploration and exploitation" across parallel trajectories. — [arXiv:2605.10344](https://arxiv.org/abs/2605.10344). Overlap: Low.

### Inferences
- Rough mapping from the paper to AI agents:

  | Paper | AI-agent counterpart |
  |---|---|
  | Planner | Lead/orchestrator agent, or an external allocator (ZEBRA, FutureWeaver) |
  | Team i | A sub-agent pipeline, e.g. explorer subagent(s) plus an executor |
  | Value v_i | Business value of the sub-task (Anthropic's "value of the task high enough") |
  | Learning duration | Exploration tokens: reading, search, tests |
  | Summary statistic | Compressed findings (Anthropic) or reports (Ao et al.); the "handoff tax" (Anchan & Sen) is its information loss |

- The controlled evidence suggests a regime split. With small per-agent budgets, splitting across agents destroys value:
  - fragmentation beyond 3–4 agents (Kim et al.);
  - single-agent ≥ multi-agent at matched tokens (Tran & Kiela);
  - communication helps only with enough compute (Park et al.).

  With larger budgets, decomposed or parallel teams pay off (Park et al.; Wunderlich et al.; Cohere). This matches the paper's prediction that splitting toward the junior team happens only once both teams can afford to learn. I am inferring that from the pattern; no paper tests it directly.
- Water-filling (ZEBRA) already produces "starving" of low-marginal-value phases at tight budgets. That is the concave-world analogue of the paper's concentration result. The paper's extra content is that learning makes the allocation regime switch non-smoothly with the budget.

### Gaps
- No orchestration paper parameterizes sub-agent exploration length as a choice variable, or derives comparative statics of the cross-agent split with respect to the value of learning.
- FutureWeaver's numerical details come from the alphaXiv summary, not from my own reading of its tables.

## Q4. LLM routing and model selection framed as bandits, including budget-constrained routing (2023–2026)

### Takeaway
Routing work treats choosing a model per query (sometimes also the number of samples or the output-token grant) as a cascade, an MDP/POMDP, or a contextual bandit with cost or knapsack constraints. The 2026 wave adds dollar-denominated pacing, shadow prices for multiple budgets, non-stationarity, and pathwise budgets in which the cost is revealed only after a call. This is the closest operations-research analogue to the paper's planner, but the arms are models, not learning teams, and learning happens in the router across many queries rather than inside each unit.

### Cited Findings
- **Chen, Zaharia & Zou (2023). "FrugalGPT: How to Use Large Language Models While Reducing Cost and Improving Performance." arXiv:2305.05176 (venue not verified).** An LLM cascade that "can match the performance of the best individual LLM (e.g. GPT-4) with up to 98% cost reduction or improve the accuracy over GPT-4 by 4% with the same cost". It notes that API prices "can differ by two orders of magnitude". — [arXiv:2305.05176](https://arxiv.org/abs/2305.05176)
- **Ong, Almahairi, Wu, Chiang, Wu, Gonzalez, Kadous & Stoica (2024). "RouteLLM: Learning to Route LLMs with Preference Data." arXiv:2406.18665 (venue not verified).** Routes between a strong and a weak model using preference data, reducing cost "by over 2 times in certain cases" without loss. — [arXiv:2406.18665](https://arxiv.org/abs/2406.18665)
- **Ding, Mallick, Wang, Sim, Mukherjee, Ruhle, Lakshmanan & Awadallah (2024). "Hybrid LLM: Cost-Efficient and Quality-Aware Query Routing." arXiv:2404.14618 (ICLR 2024 per arXiv comment).** "Up to 40% fewer calls to the large model, with no drop in response quality". — [arXiv:2404.14618](https://arxiv.org/abs/2404.14618)
- **Aggarwal, Madaan, Anand, Potharaju, Mishra, Zhou, Gupta, Rajagopal et al. (2023). "AutoMix: Automatically Mixing Language Models." arXiv:2310.12963 (NeurIPS 2024 per arXiv comment).** A few-shot self-verification step plus "a POMDP based router" that escalates to larger models. — [arXiv:2310.12963](https://arxiv.org/abs/2310.12963)
- **Ding, Mallick, Zhang, Wang, Madrigal, Hipolito Garcia, Xia, Lakshmanan et al. (2025). "BEST-Route: Adaptive LLM Routing with Test-Time Optimal Compute." arXiv:2506.22716 (ICML 2025 per arXiv comment).** "Chooses a model and the number of responses to sample from it based on query difficulty", reducing costs "by up to 60% with less than 1% performance drop". — [arXiv:2506.22716](https://arxiv.org/abs/2506.22716)
- **Dai, Li, Liu, Yu & Lui (2024). "Cost-Effective Online Multi-LLM Selection with Versatile Reward Models" (C2MAB-V). arXiv:2405.16587.** A "Cost-effective Combinatorial Multi-armed Bandit" for selecting several LLMs per task. — [arXiv:2405.16587](https://arxiv.org/abs/2405.16587)
- **Wang, Liu, Cheng, Zhao, Chen, Yu, Fu & Chen (2025). "MixLLM: Dynamic Routing in Mixed Large Language Models." arXiv:2502.18482 (NAACL 2025 per arXiv comment).** A "contextual-bandit-based routing system" trading off quality, cost and latency, with continual learning and a changing set of candidate models. — [arXiv:2502.18482](https://arxiv.org/abs/2502.18482)
- **Li (2025). "LLM Bandit: Cost-Efficient LLM Generation via Preference-Conditioned Dynamic Routing." arXiv:2502.02743.** Formulates LLM selection "as a multi-armed bandit problem" with user preferences set at inference time, generalizing to unseen LLMs. — [arXiv:2502.02743](https://arxiv.org/abs/2502.02743)
- **Panda, Magazine, Devaguptapu, Takemori & Sharma (2025). "Adaptive LLM Routing under Budget Constraints" (PILOT). arXiv:2508.21141 (EMNLP 2025 Findings per arXiv comment).** Routing as "a contextual bandit problem". PILOT is "a novel extension of LinUCB" that uses offline preference priors, with "an online cost policy modeled as a multi-choice knapsack problem". — [arXiv:2508.21141](https://arxiv.org/abs/2508.21141)
- **Taberner-Miller (2026). "ParetoBandit: Budget-Paced Adaptive Routing for Non-Stationary LLM Serving." arXiv:2604.00136.** Cost-aware contextual bandits with "an online primal–dual budget pacer" that enforces a dollar-denominated ceiling across portfolios "spanning a ~530× cost range". It adapts to price and quality drift. — [arXiv:2604.00136](https://arxiv.org/abs/2604.00136)
- **Qin, Yu, Zhang & Zhang (2026). "Pathwise-Budgeted LLM Routing: Online Allocation with K-Bit Tail-Cost Learning" (ADP-HT). arXiv:2611.05835 (v1 4 Nov 2026).**
  - Setting: firms "must decide which model to call and whether to retry a failed task. Because a call's charge is revealed only after completion, one long response can exhaust the remaining budget and leave later tasks unserved." The objective is "the number of tasks solved before service stops".
  - Result: at the tightest budgets ADP-HT "solves more than twice as many MATH500 and GPQA tasks as the best implemented baseline". — [arXiv:2611.05835](https://arxiv.org/abs/2611.05835)
  - Relation (inference) — Overlap: Medium. It models all-pay retries and stochastic per-call charges explicitly (see Q9).
- **Lee & Wong (2026). "Drift-Aware LLM Routing with Sparse Contexts and Shared Budgets." arXiv:2609.00662.** Non-stationary sparse contextual routing "with multiple knapsack constraints" over compute, latency, memory and money. It uses pessimistic reward and optimistic cost estimates and updates "resource shadow prices online". — [arXiv:2609.00662](https://arxiv.org/abs/2609.00662)
- **Wei, Pal, Mukherjee, Dernoncourt, Rossi, Kveton & Eldardiry (2026). "Online Learning with LLM Experts from Limited Feedback." arXiv:2609.05820.** A bandit with K experts and d features. Regret is Õ(dT/√m) with full information and Õ(dT√(K/m)) with bandit feedback, where m ≪ T is "a budget on feedback". — [arXiv:2609.05820](https://arxiv.org/abs/2609.05820)
- **Zhang, Huang, Zhang & Yang (2026). "Rethinking Quality in Large Language Model Routing: Security-Conditioned Model-and-Budget Selection" (SCRouter). arXiv:2610.18566.** Routers choose "which model to call and how many output tokens to grant it". SCRouter estimates "the probability that the response finishes within budget". — [arXiv:2610.18566](https://arxiv.org/abs/2610.18566)
- Further 2026 bandit-routing papers whose titles and dates I verified only through alphaXiv listings (abstracts not read):
  - WISERouter (arXiv:2607.23765)
  - "Cost-Aware Best-LLM Identification using Dueling Feedback" (arXiv:2609.30360)
  - "Online LLM Selection via Constrained Bandits with Time-Varying Demand" (arXiv:2606.17489)
  - "Cost-Aware Multi-Objective Bandits: Theory and Application to Budgeted LLM Configuration Evaluation" (arXiv:2608.04333)
  - "Chance-Constrained Personalized LLM Routing with Online Preference Learning" (arXiv:2610.22695)
  - "Correlation-Aware Contextual Bandits with Surrogate Rewards for LLM Routing" (arXiv:2607.09015)
  
  — [alphaXiv listing](https://www.alphaxiv.org/abs/2508.21141)
- Allocation across queries as a bandit is covered under Q1 (Zuo & Zhu, ICLR 2026). — [arXiv:2506.12721](https://arxiv.org/abs/2506.12721)

### Inferences
- Routing gives the paper a ready OR vocabulary: knapsack and shadow prices (PILOT, Drift-Aware), primal–dual pacing (ParetoBandit), and pathwise budget exhaustion (ADP-HT). It also sets the contrast. In routing, the router learns arm qualities across a stream of queries (between-unit exploration). In the paper, each team explores within its own unit and the planner commits ex ante.
- BEST-Route and SCRouter allocate both the model and the amount of compute, which parallels the paper's joint choice of budget and learning duration. They do not model a learning phase inside the call.

### Gaps
- I found no routing paper whose arms are learning agents with an internal explore-then-exploit protocol, or whose rewards are weighted by heterogeneous task values in a fixed-budget, one-shot split.
- Venues for FrugalGPT and RouteLLM are not verified.

## Q5. Explore–exploit behaviour of LLM agents (bandits, in-context RL, explore-then-act agents)

### Takeaway
Off-the-shelf LLMs explore poorly. They are greedy, frequency-biased and "think too fast". Krishnamurthy et al. (NeurIPS 2024) found robust exploration only for GPT-4 with chain-of-thought and an externally summarized history presented as sufficient statistics. Remedies include algorithmic scaffolds (EVOLvE, LLM-implemented posterior sampling), RL fine-tuning (which can increase greediness), in-context summarization, and explicit "Explore-then-Act" designs with a separate interaction budget for information gathering. Two recurring findings map onto the paper's protocol: a separate exploration phase helps, and summaries or sufficient statistics are what make LLM exploitation work.

### Cited Findings
- **Krishnamurthy, Harris, Foster, Zhang & Slivkins (2024). "Can large language models explore in-context?" arXiv:2403.15371 (NeurIPS 2024 per arXiv comment).** GPT-3.5, GPT-4 and Llama2 were tested on multi-armed bandits described in-context. "Only one configuration resulted in satisfactory exploratory behavior: GPT-4 with chain-of-thought reasoning and an externally summarized interaction history, presented as sufficient statistics." The authors conclude "non-trivial algorithmic interventions, such as fine-tuning or dataset curation, may be required". — [arXiv:2403.15371](https://arxiv.org/abs/2403.15371). Relation (inference) — Overlap: Medium. Strong support for the paper's design choice that the prober hands a summary statistic to the exploiter: without it, LLM decision-makers do not explore or exploit reliably.
- **Harris & Slivkins (2025). "Should You Use Your Large Language Model to Explore or Exploit?" arXiv:2502.00225 (UAI 2026 per arXiv comment).** Uses LLMs "to explore and exploit in silos". "Reasoning models show the most promise for solving exploitation tasks, although they are still too expensive or too slow". Tool use and in-context summarization help on medium-difficulty tasks, "however even then, all LLMs we study perform worse than a simple linear regression". "LLMs do help at exploring large action spaces with inherent semantics, by suggesting suitable candidates to explore." — [arXiv:2502.00225](https://arxiv.org/abs/2502.00225). Relation (inference) — Overlap: Medium. This is the closest empirical treatment of separate explore and exploit roles. It suggests LLMs work better as proposers (probing) and that a statistical posterior update may beat an LLM exploiter.
- **Nie, Su, Chang, Lee, Chi, Le & Chen (2024). "EVOLvE: Evaluating and Optimizing LLMs For In-Context Exploration." arXiv:2410.06238 (ICML 2025 per arXiv comment).** A bandit benchmark suite. "Algorithm-guided support during inference" and algorithm distillation let "smaller models" achieve "superior exploration performance", surpassing larger models. — [arXiv:2410.06238](https://arxiv.org/abs/2410.06238). Overlap: Low–Medium.
- **Monea, Bosselut, Brantley & Artzi (2024). "LLMs Are In-Context Bandit Reinforcement Learners." arXiv:2410.05362 (COLM 2025 per arXiv comment).** Contextual-bandit in-context RL from external reward, with models from 500M to 70B parameters. "LLMs effectively demonstrate such learning", once instability is addressed. — [arXiv:2410.05362](https://arxiv.org/abs/2410.05362). Overlap: Low.
- **Schmied, Bornschein, Grau-Moya, Wulfmeier & Pascanu (2025). "LLMs are Greedy Agents: Effects of RL Fine-tuning on Decision-Making Abilities." arXiv:2504.16078.** Identifies three failure modes: "greediness, frequency bias, and the knowing-doing gap". "RL fine-tuning enhances the decision-making abilities of LLMs by increasing exploration and narrowing the knowing-doing gap." — [arXiv:2504.16078](https://arxiv.org/abs/2504.16078). Overlap: Low–Medium.
- **Chen, Chen, Huang, Xie & Dhingra (2025). "When Greedy Wins: Emergent Exploitation Bias in Meta-Bandit LLM Training." arXiv:2509.24923.** SFT/RL agents reach UCB or Thompson-sampling level performance, but "gains often stem from more sophisticated but greedier exploitation". They are "more prone to early catastrophic failure ... prematurely abandoning exploration". — [arXiv:2509.24923](https://arxiv.org/abs/2509.24923). Overlap: Low.
- **Arumugam & Griffiths (2025). "Toward Efficient Exploration by Large Language Model Agents." arXiv:2504.20997 (ICLR 2026 per arXiv comment).** Uses LLMs "to explicitly implement an existing RL algorithm (Posterior Sampling for Reinforcement Learning)", which proves "considerably more effective in natural language tasks that demand prudent exploration". — [arXiv:2504.20997](https://arxiv.org/abs/2504.20997). Relation (inference) — Overlap: Low–Medium (a posterior-based exploiter in natural language, like the paper's posterior-acting exploitation agent).
- **Pan, Xie & Wilson (2025). "Large Language Models Think Too Fast To Explore Effectively." arXiv:2501.18009.** In Little Alchemy 2, "most LLMs underperform compared to humans, except for the o1 model". Sparse-autoencoder analysis suggests LLMs "think too fast and make premature decisions". — [arXiv:2501.18009](https://arxiv.org/abs/2501.18009). Overlap: Low.
- **Park, Liu, Ozdaglar & Zhang (2024). "Do LLM Agents Have Regret? A Case Study in Online Learning and Games." arXiv:2403.16843 (ICLR 2025 per arXiv comment).** Studies no-regret behaviour of LLMs in online learning and repeated games. — [arXiv:2403.16843](https://arxiv.org/abs/2403.16843). Overlap: Low.
- **Austin, Suleman & Cheung (2026). "Semantic Bandits: In-Context Exploration-Exploitation is Biased by Semantic Priors." arXiv:2608.16707.** "Semantically informative action labels reduce exploration in favour of exploitation". — [arXiv:2608.16707](https://arxiv.org/abs/2608.16707). Overlap: Low.
- **Tajwar, Jiang, Thankaraj, Rahman, Kolter, Schneider & Salakhutdinov (2025). "Training a Generally Curious Agent" (Paprika). arXiv:2502.17543 (ICML 2025 per arXiv comment).** Fine-tuning on synthetic interaction data teaches models "to explore and adapt their behavior on a new task based on environment feedback in-context". It uses a curriculum that favours tasks "with high learning potential". — [arXiv:2502.17543](https://arxiv.org/abs/2502.17543). Overlap: Low.
- **Ye, Shi, Liu, Wang, Cai, Shi, Gu, Cai et al. (2026). "Look Before You Leap: Autonomous Exploration for LLM Agents." arXiv:2605.16143.** Agents fail through "premature exploitation: a tendency to act on prior knowledge before acquiring sufficient environment-specific information". The proposed "Explore-then-Act paradigm ... decouples information-gathering from task execution: agents first utilize an interaction budget to acquire grounded environmental knowledge, then leverage it for task resolution". Standard task-oriented RL yields "narrow and repetitive behaviors". — [arXiv:2605.16143](https://arxiv.org/abs/2605.16143). Relation (inference) — Overlap: Medium. This is the paper's team-level protocol (probe, then exploit) implemented for LLM agents, but with no planner splitting budgets across teams.
- **Guan, Huang, Liu, Liang, Lei, Ng, Chua & Cohn (2026). "Clearing the Fog: Towards Installing and Refining Proactive Exploration Capabilities in LLM Agents." arXiv:2608.14339.** Proactive exploration, defined as "the ability to explore an environment to acquire information that improves future decision-making", is trained with exploration-rich data and contrastive RL. — [arXiv:2608.14339](https://arxiv.org/abs/2608.14339). Overlap: Low–Medium.
- **Karim & Keon (2026). "Explore or Confirm? LLM Agents Misallocate Measurements Under Noise." arXiv:2610.25111.** With a fixed experiment budget, five LLM agents "misallocate in both directions". Three "over-confirm, spending most of the budget re-testing", and on the generated landscape "every model ends with a worse final pick than a basic scripted strategy". Giving a list of untried candidates reduces over-confirmation; a running summary changes outcomes "by at most five percentage points". — [arXiv:2610.25111](https://arxiv.org/abs/2610.25111). Relation (inference) — Overlap: Medium (behavioural evidence that LLM agents mis-set their own learning duration, which argues for planner-set learning budgets).
- **Huang, Cao, Lee, Gomez, Yang, Harris, Do, Mao et al. (2026). "Planning Commitment of LLM under Partial Observability." arXiv:2610.21108.** "Aggressive commitment risks costly failures, while conservative commitment risks excessive LLM calls". Accuracy is similar, but conservative planners have fewer failed attempts at the cost of more API calls. "LLMs treat the provided priors nearly as facts." — [arXiv:2610.21108](https://arxiv.org/abs/2610.21108). Overlap: Low–Medium (an exploration-length vs commitment trade-off).
- **Fang & Wang (2026). "Exploit More, Explore Smarter for Budget-Constrained Agentic Search" (ExTS). arXiv:2608.23848 (Amazon).** Under small evaluation budgets, "standard MCTS allocates budget poorly". ExTS "treats expansion itself as a value-of-information decision", for an average +5.5% relative gain. — [arXiv:2608.23848](https://arxiv.org/abs/2608.23848). Overlap: Low–Medium.
- **Samuel, Ursekar, Kalmath, Shanker, Chatrath & Xue (2026). "Studying Without a Syllabus: Task-Agnostic Environment Preprocessing." arXiv:2609.10824 (Scale AI / UMD).** A "studying system explores an environment under a budget and produces artifacts for a frozen solver". "Larger study budgets do not reliably improve downstream reward", but studied artifacts "reduce the test-time sampling needed", shifting "computation from repeated test-time attempts to a pre-task study phase". — [arXiv:2609.10824](https://arxiv.org/abs/2609.10824). Relation (inference) — Overlap: Medium. A pre-task learning budget with bounded value is a direct analogue of the paper's learning phase and its window.
- **Hartmann, Harvey, Navott, Wang, Melo, Cipcigan, Zhang & Abate (2026). "Amortising Bayesian Experimental Design for Sequential Information Gathering in LLMs" (ASIG). arXiv:2607.03426 (ICML 2026 FoGen workshop, non-archival).** An expected-information-gain reward more than doubles 20 Questions success and cuts inference cost by over 25× relative to BED-LLM. — [arXiv:2607.03426](https://arxiv.org/abs/2607.03426). Overlap: Low.
- **Nguyen-Hien, Teh, Lee & Zhi-Xuan (2026). "Rational Clarification by Assistive Agents via Value-of-Information Reasoning" (REVOIR). arXiv:2609.37588.** Value-of-information reasoning decides when to ask rather than act. It improves preference satisfaction "by 13-15%" while "asking five times fewer questions". — [arXiv:2609.37588](https://arxiv.org/abs/2609.37588). Overlap: Low–Medium.
- **Kim, Li & Lee (2026). "Learning to Ask: Information Acquisition for SLM-LLM Collaboration, under a budget." arXiv:2610.01236.** Reframes small-model/large-model collaboration "as an information acquisition problem, under an API budget". A small model reasons and queries a large-model advisor only when needed, sometimes matching "oracle problem-level routing". — [arXiv:2610.01236](https://arxiv.org/abs/2610.01236). Overlap: Low–Medium (a junior agent buying information from a senior one).
- Listing-only items (title and date verified on alphaXiv, not read):
  - "In-Context Curiosity: Distilling Exploration for Decision-Pretrained Transformers on Bandit Tasks" (arXiv:2510.00347)
  - "Survey: Multi-Armed Bandits Meet Large Language Models" (arXiv:2505.13355)
  - "A Component-Based Survey of Interactions between Large Language Models and Multi-Armed Bandits" (arXiv:2601.12945)
  
  — [alphaXiv](https://www.alphaxiv.org/abs/2410.05362)

### Inferences
- The explore/exploit literature supports splitting the roles, which the paper already does:
  - Harris & Slivkins: explore and exploit "in silos".
  - Krishnamurthy et al.: sufficient-statistic summaries are needed.
  - Ye et al.: Explore-then-Act with its own interaction budget.
  - Karim & Keon; Huang et al.: agents mis-set exploration length on their own.
  
  For the extension, this argues for planner-set or rule-set learning durations and a structured summary-statistic interface rather than free-form context sharing.
- Greedy or premature exploitation biases (Schmied et al.; Chen et al.; Pan et al.) mean an LLM probing agent may under-explore relative to the paper's optimal learning duration. The realized learning curve of an LLM team is then flatter than the Bayesian ideal, which could shift the window.

### Gaps
- No explore/exploit paper places several LLM learners under a common budget allocated by a planner.
- In-context RL and decision-pretrained-transformer lines (e.g. DPT) were not verified in this pass.

## Q6. Economics and organization of AI agents: principal–agent and contract views, and cost models (pay-per-token; input vs output vs cached pricing)

### Takeaway
Economics papers frame AI agents as market and organizational actors (Hadfield & Koh; Rothschild et al.; Tomasev et al.). They treat token budgets as products sold through menus and committed-spend contracts (Bergemann, Bonatti & Smolin). They identify moral hazard in pay-per-token pricing and propose pay-for-performance contracts (Saig, Einav & Talgam-Cohen; Velasco et al.). Cost-of-Pass formalizes expected cost per success as per-attempt cost divided by success probability. Real API pricing is all-pay and type-specific: output costs 5× input for the tiers checked, cache hits cost 0.1× input, tools carry per-call fees. Outcome-based pricing appears only at the application layer (e.g. Intercom Fin at $0.99 per outcome).

### Cited Findings
- **Hadfield & Koh (2025). "An Economy of AI Agents." arXiv:2509.01063 (econ.GN; v1 1 Sep 2025; Gillian K. Hadfield and Andrew Koh).** "This chapter surveys recent developments and highlights open questions for economists around how AI agents might interact with humans and with each other, shape markets and organizations, and what institutions might be required for well-functioning markets." — [arXiv:2509.01063](https://arxiv.org/abs/2509.01063). A search-result summary says it was prepared for the NBER Handbook on the Economics of Transformative AI (I did not open the NBER PDF myself). — [NBER PDF](https://www.nber.org/system/files/chapters/c15305/c15305.pdf). Relation (inference) — Overlap: Low (framing and institutions; no allocation model).
- **Rothschild, Mobius, Hofman, Dillon, Goldstein, Immorlica, Jaffe, Lucier et al. (2025). "The Agentic Economy." arXiv:2505.15799.** Assistant agents act for consumers and service agents for businesses. The main economic impact is "reducing communication frictions between consumers and businesses". — [arXiv:2505.15799](https://arxiv.org/abs/2505.15799). Overlap: Low.
- **Tomasev, Franklin, Leibo, Jacobs, Cunningham, Gabriel & Osindero (2025). "Virtual Agent Economies." arXiv:2509.10147.** Proposes the "sandbox economy" framework and considers "auction mechanisms for fair resource allocation" among agents. — [arXiv:2509.10147](https://arxiv.org/abs/2509.10147). Overlap: Low.
- **Bergemann, Bonatti & Smolin (2025). arXiv:2502.07736.** The v1 title was "The Economics of Large Language Models: Token Allocation, Fine-Tuning, and Optimal Pricing"; the current v2 title is "Menu Pricing of Large Language Models".
  - v1: models "variable operational costs of processing input and output tokens". "The optimal pricing structure depends on whether token allocation across tasks is contractible". The optimal mechanism is implemented by "menus of two-part tariffs, with higher markups for more intensive users". — [arXiv:2502.07736v1](https://arxiv.org/abs/2502.07736v1)
  - v2: a provider "sells menus of token budgets"; the optimal mechanism is "committed-spend contracts: buyers pay for a budget that they allocate across token classes priced at marginal cost". The paper says this matches pricing at Anthropic, OpenAI and GitHub. — [arXiv:2502.07736](https://arxiv.org/abs/2502.07736)
  - Relation (inference) — Overlap: Medium. Token allocation across tasks is the buyer's problem, and in the paper's language the buyer is the planner. The paper's ex-ante budget fits the "committed-spend" institution.
- **Saig, Einav & Talgam-Cohen (2024). "Incentivizing Quality Text Generation via Statistical Contracts." arXiv:2406.11118 (NeurIPS 2024 per arXiv comment).** "Current pay-per-token pricing schemes create a misalignment of incentives known in economics as moral hazard." The paper proposes "a pay-for-performance, contract-based framework" with "cost-robust contracts", characterized through composite hypothesis tests. — [arXiv:2406.11118](https://arxiv.org/abs/2406.11118). Relation (inference) — Overlap: Medium on the principal–agent view. Note Talgam-Cohen is also a ZEBRA co-author, so this group links contracts and orchestration budgets.
- **Velasco, Tsirtsis, Okati & Gomez-Rodriguez (2025). "Is Your LLM Overcharging You? Tokenization, Transparency, and Incentives." arXiv:2505.21627 (ICML 2026 oral per arXiv comment).** Under pay-per-token pricing, providers have "a financial incentive ... to strategize and misreport the (number of) tokens", and users "cannot prove, or even know" this. — [arXiv:2505.21627](https://arxiv.org/abs/2505.21627). Overlap: Low–Medium.
- **Erol, El, Suzgun, Yuksekgonul & Zou (2025). "Cost-of-Pass: An Economic Framework for Evaluating Language Models." arXiv:2504.13359 (ICLR 2026 per PDF header).**
  - Definitions: R_m(p) is the probability of a correct answer and C_m(p) the "expected cost of one inference attempt". With independent trials, cost-of-pass is v(m,p) = C_m(p)/R_m(p), and it is infinite when R = 0. The per-attempt cost is c = n_in·c_in + n_out·c_out, the vector form being w^T x.
  - Results: "performance-oriented methods with marginal performance gains rarely justify the costs". Majority voting gives 0% frontier-cost improvement in all tested datasets.
  - Suggested extensions: verification costs, "costs associated with unsuccessful outputs, tool-usage fees, orchestration overhead", and "explicit penalties for failed attempts". — [arXiv:2504.13359](https://arxiv.org/abs/2504.13359)
  - Relation (inference) — Overlap: Medium. It makes the all-pay structure explicit: every attempt is paid whether or not it succeeds.
- **Kapoor, Stroebl, Siegel, Nadgir & Narayanan (2024). "AI Agents That Matter." arXiv:2407.01502.** "A narrow focus on accuracy without attention to other metrics" makes state-of-the-art agents "needlessly complex and costly". The authors propose jointly optimizing cost and accuracy. — [arXiv:2407.01502](https://arxiv.org/abs/2407.01502). Overlap: Low–Medium.
- **Khan (2026). "Token Budgets: An Empirical Catalog of 63 LLM-Agent Budget-Overrun Incidents, with an Affine-Typed Rust Mitigation as a Case Study." arXiv:2606.04056.** "A single retry loop can spend thousands of dollars before an operator notices". The catalog has 63 confirmed incidents from 21 orchestration frameworks (2023–2026). — [arXiv:2606.04056](https://arxiv.org/abs/2606.04056). Overlap: Low (evidence of all-pay overrun risk).
- **Anthropic API pricing (Claude Platform docs, accessed 2026-11-06).**
  - Example rows (input / output per MTok): Claude Opus 4.5–4.8 at $5 / $25; Claude Sonnet 4.5 and 4.6 at $3 / $15; Claude Haiku 4.5 at $1 / $5. Claude Opus 5.5 is listed at $4 / $20.
  - Prompt caching: 5-minute cache write is "1.25x base input price", 1-hour write is 2×, and a cache read (hit) is "0.1x base input price", with exceptions for some models (0.05× on Opus 5.5 and Sonnet 5.5). "Caching pays off after one cache read for the 5-minute duration".
  - Batch API: "a 50 percent discount on both input and output tokens".
  - Web search: "$10 USD per 1,000 searches, plus standard token costs for search-generated content". Search results "are counted as input tokens" in later turns.
  - No price on the page is contingent on outcomes. — [Anthropic pricing](https://platform.claude.com/docs/en/about-claude/pricing)
- **Intercom Fin pricing (accessed 2026-11-06).**
  - "Fin is priced at $0.99 per outcome". An outcome is counted when "a customer confirms their issue is resolved", when "they don't ask for more help after Fin responds", or when "Fin completes a workflow (Procedure), including handoffs". It is charged "only once per conversation".
  - The page does not explicitly say whether unresolved conversations are free. — [Intercom pricing](https://www.intercom.com/pricing)
  - A secondary search summary reports other outcome-priced vendors (Sierra, Zendesk), but those figures are unverified.

### Inferences
- **All-pay at the token layer, pay-on-success only at the application layer.** Model providers bill every token, tool call and cache write regardless of outcome. Outcome pricing (Intercom) shifts risk to the vendor, which must then solve exactly an all-pay allocation problem internally. For the paper this means exploration tokens are sunk. The planner's objective is naturally Σ_i v_i·R_i(b_i) subject to Σ b_i ≤ T, with all b_i spent, and the cost per success is a cost-of-pass ratio.
- **Price asymmetry changes the learning cost.** Exploration such as reading files, search results and test logs is input-heavy and often cacheable (0.1× on hits). Execution, meaning writing code or answers, is output-heavy (5× input). So in dollars, learning is cheaper per token than exploiting. A token budget overstates the relative cost of learning, and a dollar budget with type-specific prices is the right unit. Think-more-or-read-more's price-ratio ablation already finds that cheaper input "buy[s] a larger cost-optimal group".
- **Contract framing.** Committed-spend budgets (Bergemann et al.) plus conservation laws (Agent Contracts) make the paper's ex-ante split institutionally natural. Saig et al.'s moral-hazard view suggests a further extension in which sub-agents, or third-party agent vendors, are paid per success rather than per token.

### Gaps
- OpenAI and Google pricing pages were not fetched here.
- I found no peer-reviewed analysis of outcome-based pricing for LLM agents. Evidence is limited to vendor pages.
- Hadfield & Koh's chapter body was not read beyond the abstract.

## Q7. Does any work study an orchestrator allocating a token/compute budget across multiple sub-agents that each learn/explore before acting, and how learning changes the optimal split?

### Takeaway
I found no paper that does this. Pieces exist separately:
- An orchestrator splits a budget across sub-agents or phases: ZEBRA (ex ante, concave), FutureWeaver (adaptive), AgentTTS, MCPP, Cohere teams, ATOM.
- Sub-agents explore before acting: Look Before You Leap's Explore-then-Act; Anthropic's subagents that compress findings; Studying Without a Syllabus.
- Probe-then-allocate protocols at the allocator level: UAB, SPLIT's pilot, Zuo & Zhu's bandit, the scaffold-evolution warm-up.

But no work makes each sub-agent's learning duration an endogenous, priced choice inside a cross-agent budget split. None derives comparative statics such as the paper's "junior shift once both can afford to learn" or "concentration when only the senior can".

### Cited Findings
- An ex-ante cross-component split exists, but with concave per-phase curves and no learning (ZEBRA): "reduces multi-phase budget allocation to a continuous nonlinear knapsack problem". — [arXiv:2605.20485](https://arxiv.org/abs/2605.20485)
- An adaptive orchestrator over sub-agents and modules under a fixed budget exists, with lookahead planning rather than environment learning (FutureWeaver). — [arXiv:2512.11213](https://arxiv.org/abs/2512.11213)
- Cross-subtask budget and model allocation with interdependence (AgentTTS) — [arXiv:2508.00890](https://arxiv.org/abs/2508.00890). Online allocation across subtasks using success-rate estimates, replanned after outcomes (MCPP) — [arXiv:2605.06110](https://arxiv.org/abs/2605.06110)
- Empirically, delegating exploration-like planning to cheap workers is the most valuable use of team compute, and execution roles plateau beyond four workers (Cohere). — [arXiv:2610.17471](https://arxiv.org/abs/2610.17471)
- Explore-then-act within one agent: "agents first utilize an interaction budget to acquire grounded environmental knowledge, then leverage it for task resolution". — [arXiv:2605.16143](https://arxiv.org/abs/2605.16143)
- A pre-task "study" budget whose value is bounded ("larger study budgets do not reliably improve downstream reward"). — [arXiv:2609.10824](https://arxiv.org/abs/2609.10824)
- Probe-then-allocate at the allocator level:
  - UAB: Phase 1 small fixed sampling, Phase 2 marginal-greedy allocation. — [arXiv:2605.26849](https://arxiv.org/abs/2605.26849)
  - SPLIT: a labelled pilot calibrates the allocation. — [arXiv:2610.23255](https://arxiv.org/abs/2610.23255)
  - Zuo & Zhu: a bandit learns difficulty online. — [arXiv:2506.12721](https://arxiv.org/abs/2506.12721)
  - Scaffold evolution: a short warm-up, then sparse feedback, then final confirmation. — [arXiv:2610.37276](https://arxiv.org/abs/2610.37276)
- Learning from others costs budget and pays only beyond a threshold:
  - Think-more-or-read-more: "communication pays only when the gain in the accuracy ceiling exceeds the reasoning room spent on reading". — [arXiv:2610.23246](https://arxiv.org/abs/2610.23246)
  - Park et al.: communication loses to independent agents "when compute is limited". — [arXiv:2609.21032](https://arxiv.org/abs/2609.21032)
- In practice, the production orchestrator lets subagents explore in parallel and compress findings for the lead, with heuristic effort-scaling rules. — [Anthropic](https://www.anthropic.com/engineering/multi-agent-research-system)
- LLMs used as their own allocators ignore value and difficulty when splitting a shared budget. — [arXiv:2608.07968](https://arxiv.org/abs/2608.07968)

### Inferences
- **The novelty claim is defensible.** The paper's combination of (i) a planner's ex-ante split across heterogeneous-value units, (ii) a within-unit learn-then-exploit protocol with chosen learning duration and a summary-statistic handoff, and (iii) comparative statics showing that learning changes the split has no direct counterpart in the 2023–2026 LLM literature I found.
- **Testable predictions for the AI version** (my reading of the paper mapped onto agents):
  1. At small budgets, an optimal orchestrator should fund exploration only for the highest-value sub-task, and concentrate.
  2. Once the budget clears every sub-agent's exploration threshold, it should shift budget toward the lower-value sub-agent.
  3. Learning has value only within a budget band. The band's lower edge is like the g-floor or communication threshold; its upper edge is like the Elo inflection point or the s1 flattening.
  
  These can be tested with ZEBRA- or FutureWeaver-style orchestrators by sweeping the total budget and comparing against the LLM-direct allocation that Fan et al. show to be value-insensitive.
- Existing allocators would likely mis-allocate in the window regime. Concave water-filling (ZEBRA) or marginal-greedy rules (UAB, Damani) cannot reproduce corner-then-interior regime switches driven by fixed learning costs. This is a concrete reason why the paper's theory matters for AI orchestration.

### Gaps
- I did not search every 2026 paper. Systems papers on agent schedulers and serving (e.g., KV-cache-aware schedulers) were out of scope and could contain allocation heuristics.
- No paper I found measures how the optimal token split between two sub-agents changes as the total budget varies, which is the key empirical test.

## Q8. Shape of returns to tokens: concavity, thresholds, saturation and "learning windows"

### Takeaway
The evidence rejects a simple concave model:
- Coverage and agent progress are typically concave or log-linear in compute: Brown et al.; Elo-per-token; Kim et al.'s log saturation; Wunderlich et al.
- Selection and verification impose ceilings: SPLIT's verifier precision; plateaus in majority voting.
- Single-agent thinking curves are sigmoidal: near zero below a solution length, then saturating (Nguyen et al.).
- Many methods are non-monotone (an interior optimum, an inverted U, or inverse scaling): Chen et al.; Wu et al.; Gema et al.; HAL; s1's rejection sampling.
- Multi-agent returns have thresholds at both ends. A minimum compute is needed before communication or decomposition pays, and a capability or fragmentation ceiling limits gains above it (Kim et al.; Park et al.; Tran & Kiela; Anchan & Sen).

Together this is good empirical support for a bounded "learning window".

### Cited Findings
- **Concave, log-linear or saturating:**
  - Coverage "often log-linear", an "exponentiated power law"; voting and reward models "plateau beyond several hundred samples". — [arXiv:2407.21787](https://arxiv.org/abs/2407.21787)
  - Agents' Elo-per-token is concave in log compute and falls below the 400-Elo-per-decade independent-sampling reference after an inflection point. — [arXiv:2609.15309](https://arxiv.org/abs/2609.15309)
  - Budget forcing "does eventually flatten out at six times". — [arXiv:2501.19393](https://arxiv.org/abs/2501.19393)
  - Verified success "saturates at the verifier's precision". — [arXiv:2610.23255](https://arxiv.org/abs/2610.23255)
  - Message density gives logarithmic saturation, S = 0.73 + 0.28 ln(c). — [arXiv:2512.08296](https://arxiv.org/abs/2512.08296)
  - Implementers and verifiers "plateau beyond four workers". — [arXiv:2610.17471](https://arxiv.org/abs/2610.17471)
  - Without budget awareness, agents "quickly hit a performance ceiling" as the tool-call budget grows. — [arXiv:2511.17006](https://arxiv.org/abs/2511.17006)
  - Self-consistency "saturates earlier" than debate or mixture-of-agents. — [arXiv:2605.01566](https://arxiv.org/abs/2605.01566)
  - Homogeneous agent scaling "exhibits strong diminishing returns". — [arXiv:2602.03794](https://arxiv.org/abs/2602.03794)
- **S-shaped and threshold returns:**
  - Single-agent ability vs thinking cap is "sigmoidal, near zero below the length a solution needs, rising sharply around it, then saturating". A sigmoid (Hill) fit beats the concave power law on held-out error. — [arXiv:2610.23246](https://arxiv.org/abs/2610.23246)
  - Multi-agent collaboration follows "a logistic growth pattern as agents scale". — [arXiv:2406.07155](https://arxiv.org/abs/2406.07155)
  - Test-time compute substitutes for 14× parameters only "on problems where a smaller base model attains somewhat non-trivial success rates"; on the hardest bin "no method makes much meaningful progress". — [arXiv:2408.03314](https://arxiv.org/abs/2408.03314)
  - Communication beats independent agents only with enough compute and a clear progress measure. — [arXiv:2609.21032](https://arxiv.org/abs/2609.21032)
  - Decomposition beats a single agent only past a crossover depth L*. — [arXiv:2610.06069](https://arxiv.org/abs/2610.06069)
  - Multi-agent setups become competitive "when more compute is expended". — [arXiv:2604.02460](https://arxiv.org/abs/2604.02460)
- **Non-monotone and inverse:**
  - Performance with the number of LM calls "can first increase but then decrease". — [arXiv:2403.02419](https://arxiv.org/abs/2403.02419)
  - Accuracy with CoT length follows an "inverted U-shaped curve". — [arXiv:2502.07266](https://arxiv.org/abs/2502.07266)
  - Inverse scaling with reasoning length on constructed tasks. — [arXiv:2507.14417](https://arxiv.org/abs/2507.14417)
  - "Higher reasoning effort reducing accuracy in the majority of runs". — [arXiv:2510.11977](https://arxiv.org/abs/2510.11977)
  - Beam search degrades with budget on easy questions. — [arXiv:2408.03314](https://arxiv.org/abs/2408.03314)
  - Debate and Reflexion "can become worse if more compute budget is utilized". — [arXiv:2406.06461](https://arxiv.org/abs/2406.06461)
  - Gemini-2.0 Flash "exhibits a clear optimum at 7 agents before degradation". — [arXiv:2512.08296](https://arxiv.org/abs/2512.08296)
  - A debate group that reads past the minimum thinking room collapses in accuracy. — [arXiv:2610.23246](https://arxiv.org/abs/2610.23246)
- **Upper capability ceilings for coordination:** tasks with single-agent baselines above about 45% "experience negative returns from additional agents". — [arXiv:2512.08296](https://arxiv.org/abs/2512.08296)
- **Tokens as the dominant input (first-order evidence):** "token usage by itself explains 80% of the variance" on BrowseComp, and three factors explain 95%. — [Anthropic](https://www.anthropic.com/engineering/multi-agent-research-system)
- **Learning-window analogues (closest to the paper's construct):**
  - In-context adaptive learning beats fresh independent attempts only up to a "scaling inflection point" (≈38M tokens for Kimi Code on Polyomino, per the alphaXiv summary). Beyond it, splitting into parallel sessions gains +264 Elo. — [arXiv:2609.15309](https://arxiv.org/abs/2609.15309); [alphaXiv summary](https://www.alphaxiv.org/abs/2609.15309)
  - Learning from others' text (reading) pays only when the ceiling gain exceeds the reasoning room it consumes, a condition that "tighten[s] as the window shrinks". — [arXiv:2610.23246](https://arxiv.org/abs/2610.23246)
  - Pre-task study shifts compute away from test-time attempts, but "larger study budgets do not reliably improve downstream reward". — [arXiv:2609.10824](https://arxiv.org/abs/2609.10824)

### Inferences
- The S-curve plus saturation pattern is exactly what generates a bounded learning window in the paper. A fixed learning cost (lower threshold) and saturating post-learning value (upper bound) give non-concave value in budget. This justifies the paper's non-convex analysis over a knapsack/water-filling approach in the AI extension.
- The window location depends on capability (Wu et al.: the optimal CoT length falls with capability) and on difficulty (Snell et al.). In the paper's language, senior and junior teams have different windows. This suggests modelling team-specific learning thresholds, e.g. g0 in the Hill form, rather than a common one.
- One calibration recipe for the extension: fit Hill-type curves (Nguyen et al.) per sub-agent role, and use Elo-per-token-style inflection points as the upper edge of the learning window.

### Gaps
- No study estimates returns separately for exploration tokens and exploitation tokens of the same agent. That would be the direct test of the paper's two-phase production function.
- Most curves are for math, QA or coding benchmarks. Evidence for long-horizon business tasks is thin.

## Q9. Cost structure: is LLM cost pay-per-attempt (all-pay) rather than pay-on-success, what does that imply, and is "token allocation" a good proxy?

### Takeaway
Yes, the cost is all-pay. Providers bill every input, output and cached token, plus tool calls, whether or not the attempt succeeds. Agents also waste a large share of spend on failing trajectories (28–64% savings from early stopping per BAGEN) or on removable reasoning (41–46% per Zeng et al.). Expected cost per success is the cost-of-pass ratio C/R.

Tokens are a reasonable first-order proxy: they explain 80% of BrowseComp variance in Anthropic's system, and most papers budget in tokens. But they are an imperfect currency:
- Prices differ by token type (output 5× input; cache hit 0.1×; batch 0.5×) and by model (5× between Haiku 4.5 and Opus 4.5–4.8).
- Tools carry separate fees ($10 per 1,000 searches) and latency.
- Model quality can matter more than quantity ("upgrading to Claude Sonnet 4 is a larger performance gain than doubling the token budget").
- Equal-token allocations can differ in dollars (2.55× search requests in Ning et al.; 2.1× token-cost spread at equal call budgets in Bertalanic & Fortuna).
- Token counts can be unobservable or misreported (Velasco et al.).

### Cited Findings
- **All-pay pricing.**
  - Per-token and per-search prices with no outcome contingency. — [Anthropic pricing](https://platform.claude.com/docs/en/about-claude/pricing)
  - "Current pay-per-token pricing schemes create a misalignment of incentives known in economics as moral hazard". — [arXiv:2406.11118](https://arxiv.org/abs/2406.11118)
  - Users "pay a fixed price per token" and "cannot prove, or even know, whether a provider is overcharging them". — [arXiv:2505.21627](https://arxiv.org/abs/2505.21627)
- **Expected cost per success.**
  - Cost-of-pass v(m,p) = C_m(p)/R_m(p) ("the expected number of attempts to obtain the first correct solution is 1/R_m(p)"). The authors propose adding "costs associated with unsuccessful outputs" and "explicit penalties for failed attempts". — [arXiv:2504.13359](https://arxiv.org/abs/2504.13359)
- **Waste on failures.**
  - Frontier models "continue spending on tasks that are unlikely to succeed"; "early stop saves 28-64% tokens on failed trajectories". — [arXiv:2606.00198](https://arxiv.org/abs/2606.00198)
  - "A single retry loop can spend thousands of dollars before an operator notices". — [arXiv:2606.04056](https://arxiv.org/abs/2606.04056)
  - 41–46% of reasoning is removable while largely preserving performance. — [arXiv:2611.07238](https://arxiv.org/abs/2611.07238)
- **Stochastic charges revealed ex post.** "A call's charge is revealed only after completion, one long response can exhaust the remaining budget". The objective becomes "the number of tasks solved before service stops", with retries as decisions. — [arXiv:2611.05835](https://arxiv.org/abs/2611.05835)
- **Costs committed under uncertainty.** "Uncertain effects remain charged until authenticated settlement". — [arXiv:2610.00349](https://arxiv.org/abs/2610.00349)
- **Pay-on-success exists at the application layer.** Intercom Fin charges "$0.99 per outcome". — [Intercom pricing](https://www.intercom.com/pricing)
- **Tokens as proxy, supporting evidence.**
  - Token usage explains 80% of BrowseComp variance; agents use about 4× chat tokens and multi-agent systems about 15×. — [Anthropic](https://www.anthropic.com/engineering/multi-agent-research-system)
  - Elo is roughly linear in log tokens for independent sampling. — [arXiv:2609.15309](https://arxiv.org/abs/2609.15309)
- **Tokens as proxy, caveats.**
  - Model quality beats quantity: upgrading to Sonnet 4 is a larger gain "than doubling the token budget on Claude Sonnet 3.7". — [Anthropic](https://www.anthropic.com/engineering/multi-agent-research-system)
  - Type-specific prices: output 5× input in the tiers checked; cache read 0.1×; cache write 1.25× or 2×; batch −50%; web search $10 per 1,000 plus results billed as input tokens later. — [Anthropic pricing](https://platform.claude.com/docs/en/about-claude/pricing)
  - At matched model tokens, allocation A needs 2.55× more search requests than B, and the fee ranking depends on search price. — [arXiv:2610.05034](https://arxiv.org/abs/2610.05034)
  - Retrieved documents are 51–68% of total tokens in search agents. — [alphaXiv summary](https://www.alphaxiv.org/abs/2609.00813)
  - A unified cost needs "token and tool consumption" jointly. — [arXiv:2511.17006](https://arxiv.org/abs/2511.17006)
  - Wall-clock time is decoupled from tokens by tool latency. — [arXiv:2601.16486](https://arxiv.org/abs/2601.16486)
  - Which fixed allocation rule is optimal "depends on how a sample is priced". — [arXiv:2610.23255](https://arxiv.org/abs/2610.23255)
  - At equal call budgets token cost varies 2.1×. — [arXiv:2609.36104](https://arxiv.org/abs/2609.36104)
  - Cache-inclusive and uncached token accounting differ (the Elo-per-token authors note this confound, per the alphaXiv summary). — [alphaXiv summary](https://www.alphaxiv.org/abs/2609.15309)
  - KV-cache reuse gives single agents an efficiency edge. — [arXiv:2601.12307](https://arxiv.org/abs/2601.12307)
  - "Artifacts in API-based budget control (particularly in Gemini 2.5)". — [arXiv:2604.02460](https://arxiv.org/abs/2604.02460)
  - Cheaper input tokens enlarge the cost-optimal debate group. — [arXiv:2610.23246](https://arxiv.org/abs/2610.23246)

### Inferences
- **Implications of all-pay for the paper's model.** In the RTB setting, as I understand it, spend arises from winning impressions (pay-per-win), so the probing agent's spend is itself tied to outcomes. In LLM agents every exploration token is paid unconditionally, so learning is a pure sunk cost. That raises the lower edge of the learning window. All-pay costs plus stochastic, ex-post charges (ADP-HT) also make overspend risk a first-order concern, which favours the paper's ex-ante caps, enforced via Agent Contracts-style conservation.
- **Recommended budget unit for the extension.** Use a dollar budget with a cost vector, w = (input, cached-input, output, tool-call prices) per model, rather than raw tokens. Alternatively, use tokens with type-specific weights. Exploration, which is mostly reading, should get a lower unit price than exploitation, which is mostly writing. If cross-agent caching is possible, exploration that re-reads shared context is cheaper still. A token-only model would overstate the cost of learning and so understate the optimal learning duration.
- **Model choice as a separate input.** "Senior" vs "junior" in the AI version maps naturally onto model tier (e.g., Opus vs Haiku, about 5× price difference), not only onto task value. The Anthropic and Cohere evidence says cheap models are effective explorers or planners but poor implementers. A two-dimensional allocation (tokens × model tier) is a natural generalization.

### Gaps
- I found no empirical study that randomizes pricing (all-pay vs pay-on-success) for agent tasks.
- OpenAI and Google pricing structures were not verified in this pass, though Nguyen et al. cite all three providers' 2026 pricing pages.

## Q10. Which 3–5 works are closest to the planned extension, and what is the clearest open gap?

### Takeaway
The five closest works:
1. **ZEBRA** (Hamri & Talgam-Cohen 2026): an ex-ante orchestrator split of a dollar budget across pipeline phases with value-differentiated marginal returns, but concave curves.
2. **FutureWeaver** (Jung, Shi, Chen & Zhang 2025): an orchestrator that plans a fixed test-time budget across sub-agents and modules.
3. **Scaling Inference-Time Compute with Teams of Coding Agents** (Samway et al., Cohere, 2026): an empirical allocation of team compute across roles; planning/exploration workers are most valuable and execution roles plateau.
4. **Think More or Read More?** (Nguyen, Gupta & Le 2026): a token-budget theory in which learning from others consumes the same window as thinking, with sigmoidal returns and threshold conditions for when learning pays.
5. **When Agents Slow Down: Elo-per-token** (Liu et al. 2026): concave returns with a measurable inflection point that dictates how a fixed budget should be split across sessions.

Close runners-up: Anthropic's multi-agent research system (practice and the 80%/15× facts), On Time Within Budget (MCPP), AgentTTS, UAB (probe then allocate), and Thinking Hard, Not Smart (LLMs are not value-aware allocators).

Clearest open gap: there is no theory, or test, of how an orchestrator should split a fixed, all-pay token or dollar budget across heterogeneous-value sub-agents when each sub-agent's production function contains an endogenous explore-then-exploit phase. In particular, nobody has shown how the feasibility of learning (a budget window) changes the optimal split in the way the paper derives.

### Cited Findings
- ZEBRA: "None address how to split a budget across the composing phases of a multi-agent pipeline at inference time". It reduces the problem to a "continuous nonlinear knapsack" with water-filling; 94.4% vs 88.1% of unconstrained quality at α = 0.5. — [arXiv:2605.20485](https://arxiv.org/abs/2605.20485)
- FutureWeaver: "existing approaches lack principled mechanisms for allocating compute to enable effective collaboration ... or optimizing compute usage under explicit budget constraints". — [arXiv:2512.11213](https://arxiv.org/abs/2512.11213)
- Cohere teams: "formulate team design as a compute allocation problem"; "planning is the most valuable use of workers"; "implementers and verifiers plateau beyond four workers". — [arXiv:2610.17471](https://arxiv.org/abs/2610.17471)
- Think-more-or-read-more: "every token spent reading is a token that cannot be spent reasoning"; sigmoidal cap sweeps; "communication pays only when the gain in the accuracy ceiling exceeds the reasoning room spent on reading". — [arXiv:2610.23246](https://arxiv.org/abs/2610.23246)
- Elo-per-token: marginal gains "diminish and eventually fall below the reference"; splitting at the inflection point gives +264 and +355 Elo. — [arXiv:2609.15309](https://arxiv.org/abs/2609.15309)
- Runners-up:
  - Anthropic multi-agent system (80% variance; 15× tokens; subagent compression). — [Anthropic](https://www.anthropic.com/engineering/multi-agent-research-system)
  - MCPP. — [arXiv:2605.06110](https://arxiv.org/abs/2605.06110)
  - AgentTTS. — [arXiv:2508.00890](https://arxiv.org/abs/2508.00890)
  - UAB. — [arXiv:2605.26849](https://arxiv.org/abs/2605.26849)
  - Thinking Hard, Not Smart. — [arXiv:2608.07968](https://arxiv.org/abs/2608.07968)
  - Explore-then-Act. — [arXiv:2605.16143](https://arxiv.org/abs/2605.16143)

### Inferences
- **How to position the paper.** It supplies the missing theory layer between budget-aware single agents (Q2) and empirical or algorithmic orchestrators (Q3):
  1. A planner-level split across valued units, like ZEBRA but with learning.
  2. A unit-level learn-then-exploit protocol, like Explore-then-Act or Anthropic subagents, with an endogenous learning duration and a summary-statistic handoff. That handoff is supported by Krishnamurthy et al.'s sufficient-statistics finding and quantified as a "handoff tax" by Anchan & Sen.
  3. Non-concave returns producing a learning window, which Think-more and Elo-per-token observe empirically.
- **Is "token allocation" a good proxy?** Adequate as a first approximation (Anthropic's 80% figure), but the extension should:
  - use dollars or weighted tokens with separate prices for reading/exploration (input, cacheable) and writing/exploitation (output), plus tool-call fees;
  - treat model tier as a second allocation dimension;
  - treat costs as all-pay, with cost-of-pass as the per-success metric.
- **Most valuable empirical companion study.** Sweep the total budget T for a two-subtask orchestration with different task values (e.g., ZEBRA- or FutureWeaver-style). Measure each sub-agent's exploration-token vs execution-token returns, fit Hill-type curves, and test the predicted regime switch: concentration at small T, a shift toward the junior or lower-value sub-agent once both can afford exploration, and no value of exploration outside the window. Compare against LLM-direct allocation, which Fan et al. show to be value-insensitive.

### Gaps
- No existing work tests the paper's two headline comparative statics (the junior shift and the concentration effect) in LLM-agent systems. These are open empirical questions.
- Interaction effects across teams were outside the paper's independence assumption, but Park et al. (2026) show they can be large: communication gives team@k ≈ 4k independent agents. This is a natural second-stage gap.
- Several items above rely on alphaXiv summaries for numerical details: FutureWeaver, ZEBRA, ATOM, AnySearch, and the Elo-per-token inflection figures. Their abstracts and IDs are verified; exact table values should be rechecked before quoting in the final report.
