# Budget allocation ACROSS learning units: a planner splits a limited resource (samples, money, compute, rounds, traffic, tokens) across learners whose value depends on how much they receive. Literature notes for positioning "Orchestrating Agent Teams: Budget Allocation in Real-Time Bidding" (Yang, Zhu & Mookerjee, WITS 2026)

Conventions used in every entry:
- **Attributes** answers the coordinator's four questions: (A) is the allocation **adaptive/online** or **committed ex ante**; (N) are units' value functions **non-concave in the resource because of learning**; (H) do units have **heterogeneous values/weights**; (W) is there a **comparison of the allocation with vs. without learning** (the paper's key comparative static, V vs. the no-learning benchmark W).
- **Overlap** (High/Medium/Low) is our assessment of how close the work is to the paper's planner problem: max v1·V(a) + v2·V(T−a), where V is non-concave because each team runs probe-then-exploit learning.
- "Relation" lines are our own analysis, not claims made by the cited authors. Claims checked only against an abstract, an index page or a reference list are flagged as such. Anything we could not verify is marked **unverified**.
- How we verified: DOIs and pages via the Crossref API; arXiv IDs, abstracts and journal-ref/comments via the arXiv API; conference venues by finding the exact title on the official proceedings index pages (PMLR v35/v51/v70/v139/v202, NeurIPS 2017/2019/2020, IJCAI 2015/2016, AAAI OJS) or OpenReview. We read full text for Boutilier & Lu (2016) and for the working-paper version of Azevedo et al. (2020).

---

## Q1. Bandits with knapsacks (BwK) and budgeted MAB: one learner with a knapsack vs. a planner splitting a budget across learners

### Takeaway
BwK and budgeted-MAB papers study ONE learner whose own arm pulls use up a shared budget. The "split" across arms is decided round by round and pools all information. The benchmark is a concave LP (the best fixed mixture of arms). None of these papers commits budgets ex ante to separate learners, models value functions made non-concave by learning, or compares allocations with vs. without learning. The useful links to the paper are the within-team design (ε-first = explore-then-commit under a budget) and the knapsack/LP view of the planner's split.

### Cited Findings
- **Badanidiyuru, A., Kleinberg, R., & Slivkins, A. (2013). "Bandits with Knapsacks." Proc. 54th IEEE FOCS, pp. 207–216; journal version J. ACM 65(3), 2018, pp. 1–55. arXiv:1305.2545.** — [FOCS DOI](https://doi.org/10.1109/FOCS.2013.30); [JACM DOI](https://doi.org/10.1145/3164539); [arXiv](https://arxiv.org/abs/1305.2545)
  - Model: one learner in a stochastic MAB with "one or more supply (or budget) limits, in addition to the customary limitation on the time horizon". The authors say it "combines aspects of stochastic integer programming with online learning." — [arXiv abstract](https://arxiv.org/abs/1305.2545)
  - Main result: "the optimal policy for a given latent distribution may significantly outperform the policy that plays the optimal fixed arm". Two algorithms, one based on "balanced exploration" and one primal-dual with multiplicative updates; the abstract says their regret is optimal (the exact qualifier was truncated in our retrieval). — [arXiv abstract](https://arxiv.org/abs/1305.2545)
  - Attributes: A = adaptive (per round); N = no (the benchmark is a fixed distribution over arms, i.e., an LP); H = arms differ in rewards/costs, but there are no separate "units"; W = no.
  - Relation (assessment), Overlap **Medium–Low**: the canonical "one learner with a knapsack". In the paper, the budget is instead committed to separate learners that cannot pool information or reallocate mid-stream.
- **Badanidiyuru, A., Langford, J., & Slivkins, A. (2014). "Resourceful Contextual Bandits." COLT 2014 (PMLR v35). arXiv:1402.6779.** — [arXiv](https://arxiv.org/abs/1402.6779); [PMLR v35 index](https://proceedings.mlr.press/v35/)
  - Contextual extension of BwK. The arXiv comment says "full version of a paper in COLT 2014". We did not retrieve the abstract; content is described from the title only. — [arXiv listing](https://arxiv.org/abs/1402.6779)
  - Attributes: A adaptive; N no; H no; W no. Overlap **Low**.
- **Agrawal, S., & Devanur, N. R. (2014). "Bandits with concave rewards and convex knapsacks." Proc. 15th ACM Conference on Economics and Computation (EC '14), pp. 989–1006. arXiv:1402.5758. Journal version: "Bandits with Global Convex Constraints and Objective," Operations Research 67(5):1486–1502 (2019).** — [EC DOI](https://doi.org/10.1145/2600057.2602844); [arXiv](https://arxiv.org/abs/1402.5758); [OR DOI](https://doi.org/10.1287/opre.2019.1840)
  - Model/result: allows "arbitrary concave rewards and convex constraints on the decisions across time". The model subsumes MAB and BwK. A UCB-family extension is polynomial-time with near-optimal regret and matches the BwK bounds. — [arXiv abstract](https://arxiv.org/abs/1402.5758)
  - Attributes: A adaptive; N no (concavity is assumed); H no; W no.
  - Relation, Overlap **Low–Medium**: the concavity assumption is exactly what the paper's learning-induced non-concavity breaks.
- **Immorlica, N., Sankararaman, K. A., Schapire, R., & Slivkins, A. (2019). "Adversarial Bandits with Knapsacks." Proc. 60th IEEE FOCS, pp. 202–219; J. ACM 69(6), 2022, pp. 1–47. arXiv:1811.11881.** — [FOCS DOI](https://doi.org/10.1109/FOCS.2019.00022); [JACM DOI](https://doi.org/10.1145/3557045); [arXiv](https://arxiv.org/abs/1811.11881)
  - Result: with adversarial outcomes "regret minimization is no longer feasible", so the objective becomes the competitive ratio. Their algorithm achieves competitive ratio O(log T). — [arXiv abstract](https://arxiv.org/abs/1811.11881)
  - Attributes: A adaptive; N no; H no; W no. Overlap **Low**.
- **Tran-Thanh, L., Chapman, A., Munoz de Cote, E., Rogers, A., & Jennings, N. R. (2010). "Epsilon-First Policies for Budget-Limited Multi-Armed Bandits." Proc. AAAI-10, 24(1):1211–1216.** — [DOI](https://doi.org/10.1609/aaai.v24i1.7758); [AAAI OJS](https://ojs.aaai.org/index.php/AAAI/article/view/7758)
  - Model: pulls are costly and limited by a fixed budget "incommensurable with the rewards". Hence "an optimal exploitation policy is not to pull the optimal arm repeatedly, but to pull the combination of arms that maximises the agent's total reward within the budget". The proposed ε-first algorithm uses "the first epsilon of the budget … solely to learn" the arms, then exploits. — [AAAI abstract](https://ojs.aaai.org/index.php/AAAI/article/view/7758)
  - The regret rate is **unverified** here; we did not read the full text.
  - Attributes: A = an ex-ante split of ONE budget between exploration and exploitation, i.e., explore-then-commit; N not analyzed; H no; W no.
  - Relation, Overlap **Medium (within-team)**: this is the closest single-learner analogue of each team's protocol (a probing share of the budget, then budget-paced exploitation). It has no planner and no multiple teams.
- **Tran-Thanh, L., Chapman, A., Rogers, A., & Jennings, N. R. (2012). "Knapsack Based Optimal Policies for Budget-Limited Multi-Armed Bandits." Proc. AAAI-12, 26(1):1134–1140. arXiv:1204.1909.** — [DOI](https://doi.org/10.1609/aaai.v26i1.8279); [arXiv](https://arxiv.org/abs/1204.1909)
  - Result: proposes KUBE and fractional KUBE. Both have logarithmic regret upper bounds, shown to be asymptotically optimal; KUBE performs up to 40% better in experiments. — [AAAI abstract](https://ojs.aaai.org/index.php/AAAI/article/view/8279)
  - Attributes: A adaptive; N no; H no; W no. Overlap **Low**.
- **Xia, Y., Li, H., Qin, T., Yu, N., & Liu, T.-Y. (2015). "Thompson Sampling for Budgeted Multi-armed Bandits." IJCAI 2015. arXiv:1505.00146.** — [arXiv](https://arxiv.org/abs/1505.00146); [IJCAI 2015 index](https://www.ijcai.org/proceedings/2015)
  - Result: each round, sample reward and cost posteriors, pick the arm with the largest ratio. Distribution-dependent regret O(ln B), extended to general distributions. — [arXiv abstract](https://arxiv.org/abs/1505.00146)
  - Attributes: A adaptive; N no; H no; W no. Overlap **Low**.
- **Recent (2026): Braverman, M., Liu, J., Mao, J., Schneider, J., & Xue, E. "Optimally Pacing Budget Spending and Learning." arXiv:2610.11074.** — [arXiv](https://arxiv.org/abs/2610.11074)
  - Result: budget-constrained online learning against classes of budget-pacing experts; regret O(D√log F + √(T log F)), matching lower bounds. — [arXiv abstract](https://arxiv.org/abs/2610.11074)
  - Attributes: A adaptive, single learner; N/H/W no. Overlap **Low** (relevant to the exploitation agent's pacing, not to the cross-team split).

### Inferences
- **One learner with a knapsack vs. a planner splitting a budget across learners** (synthesis grounded in the BwK abstract and the paper's model):
  1. *Who decides and when.* In BwK, the learner reallocates every round on the basis of all past observations. In the paper, the planner commits (B_i, τ_i) ex ante and gets no feedback from teams.
  2. *Information pooling.* In BwK, every observation updates a single posterior. Under a planner's split, each team learns its own θ separately, so the cost of learning is paid once per team, like a duplicated fixed cost. This produces V's entry jump.
  3. *Benchmark curvature.* BwK benchmarks against the best fixed mixture of arms (an LP). The optimal value of an LP is concave in its right-hand-side budget (standard LP duality; our inference), so the BwK benchmark never shows the paper's non-concavity.
  4. *Object allocated.* In BwK the budget is spent on individual pulls. In the paper it buys an entire learning-plus-exploitation process whose value function V(B) is the object being allocated. This makes the planner's problem a resource allocation over value functions (Q2), not a bandit.
- Tran-Thanh et al.'s ε-first rule and the paper's probing agent share the same logic: commit a fraction of one budget to exploration up front. The paper's novelty is to nest that rule inside an across-team split. The planner then chooses each team's τ jointly with its budget.

### Gaps
- We did not retrieve abstracts for Badanidiyuru–Langford–Slivkins (2014) or Xia et al.'s 2016 multiple-play paper ("Budgeted multi-armed bandits with multiple plays", IJCAI 2016, **unverified**), and we did not read regret constants from full texts.
- We found no BwK paper in which the "arms" are themselves learning agents with internal state that need a minimum allocation before they produce value.

---

## Q2. Weakly coupled stochastic DPs, Lagrangian decomposition, restless bandits and budgeted MDPs (including allocating budget across MDPs in advertising)

### Takeaway
This is the methodological home of the planner's problem: independent sub-problems linked only by a shared resource, decomposed through a price on that resource (Lagrangian) or through additive approximations (ALP). The closest architecture is Boutilier & Lu (2016, Google), who allocate an ad budget across many independent MDPs. However, they prove the per-unit value is **concave** in budget, which makes greedy marginal allocation optimal, and their sub-processes do not learn. Learning versions (restless-bandit regret, WCDQN, budgeted RL) learn the dynamics online but do not study how learning bends the value-of-budget curve.

### Cited Findings
- **Gittins, J. C. (1979). "Bandit Processes and Dynamic Allocation Indices." Journal of the Royal Statistical Society, Series B 41(2):148–164.** — [DOI](https://doi.org/10.1111/j.2517-6161.1979.tb01068.x)
  - Content from standard knowledge (full text not read): an index policy for sequentially allocating effort among independent Bayesian projects (bandit processes). The index includes the value of learning.
  - Attributes: A adaptive; N not the object of study; H yes (projects differ); W no.
  - Relation, Overlap **Medium (conceptual)**: one resource (time) allocated across independent learning projects. Allocation is sequential, not an ex-ante split.
- **Whittle, P. (1988). "Restless bandits: activity allocation in a changing world." Journal of Applied Probability 25(A):287–298.** — [DOI](https://doi.org/10.2307/3214163)
  - Content from standard knowledge (not re-read): relaxes the per-period "m of N arms active" constraint to a time-average via a Lagrange multiplier, which yields the Whittle index.
  - Attributes: A adaptive; N no; H yes; W no. Overlap **Low–Medium**.
- **Hawkins, J. T. (2003). "A Langrangian decomposition approach to weakly coupled dynamic optimization problems and its applications." PhD thesis, MIT Sloan / Operations Research Center (advisor D. Bertsimas).** Note: "Langrangian" is the catalogued spelling; it is a typo.
  - Content: a Lagrangian approach to decoupling weakly coupled dynamic optimization problems (finite and infinite horizon), with applications to multi-armed bandits, restless bandits and queueing; 192 pp. — [MIT DSpace](https://dspace.mit.edu/handle/1721.1/29599)
  - Attributes: A adaptive (dynamic); N no; H yes; W no. Overlap **Medium (method)**.
- **Adelman, D., & Mersereau, A. J. (2008). "Relaxations of Weakly Coupled Stochastic Dynamic Programs." Operations Research 56(3):712–727.** — [DOI](https://doi.org/10.1287/opre.1070.0445)
  - Abstract: sub-problems are "independent of each other except for a collection of coupling constraints on the action space". The paper fits additively separable value-function approximations by Lagrangian relaxation and by the LP approach to ADP, proves comparisons between the relaxations and the optimal value, gives a column-generation algorithm, and reports experiments on bandit-like problems. — [Crossref abstract via DOI](https://doi.org/10.1287/opre.1070.0445)
  - Attributes: A adaptive; N no; H yes; W no. Overlap **Medium (method)**.
- **Boutilier, C., & Lu, T. (2016). "Budget Allocation using Weakly Coupled, Constrained Markov Decision Processes." Proc. 32nd Conference on Uncertainty in Artificial Intelligence (UAI 2016).** Page numbers conflict: a Google Research listing gives pp. 52–61; a PMLR listing gives R14:682–691. — [UAI PDF](https://www.auai.org/uai2016/proceedings/papers/246.pdf); [Google Research](https://research.google/pubs/pub45291/); [PMLR listing](https://proceedings.mlr.press/r14/boutilier16a.html)
  - Model: "budget … allocation in sequential decision problems involving a large number of concurrently running sub-processes, whose only interaction is through their consumption of budget". They introduce budgeted MDPs (BMDPs), "an MDP model in which policies/values are a function of available budget". — [UAI PDF](https://www.auai.org/uai2016/proceedings/papers/246.pdf)
  - Concavity result: "optimal value functions are concave, non-decreasing in budget, and piecewise-linear in the finite horizon case". The concavity comes from allowing randomized policies: "The optimal VF for such 'single-stage randomized' policies is given by the convex hull of the useful budgets". Deterministic policies give a piecewise-constant, non-concave value function. — [UAI PDF](https://www.auai.org/uai2016/proceedings/papers/246.pdf)
  - Allocation: the cross-unit problem "can be cast as a multiple-choice knapsack problem, which admits an efficient, optimal greedy algorithm". Allocation is an offline decomposition plus an optional online "dynamic budget reallocation" (DBRA) that reallocates remaining budget each stage. — [UAI PDF](https://www.auai.org/uai2016/proceedings/papers/246.pdf)
  - Empirics: online-advertising domain (a synthetic ad MDP and a 452K-state advertiser MDP whose parameters were learned offline by MLE from data). "Sweet spot" curves of expected value vs. global budget show "diminishing return with increasing budget". The greedy allocation averages 1.47 ms. — [UAI PDF](https://www.auai.org/uai2016/proceedings/papers/246.pdf)
  - Motivation: prior work (Archak et al.) "assume[s] a fixed, predetermined budget for each user … does not determine a suitable budget, nor … allow for making budget tradeoffs across different users". — [UAI PDF](https://www.auai.org/uai2016/proceedings/papers/246.pdf)
  - Attributes: A = ex ante (offline greedy) plus optional online reallocation; N = **no** (concave by theorem; no within-unit learning); H = yes (users in different states/types); W = no.
  - Relation, Overlap **High (architecture), opposite mechanism**: this is the paper's planner problem with known, concave sub-problems.
- **Ad-budget MDP references cited by Boutilier & Lu** (verified only from their reference list):
  - Archak, N., Mirrokni, V., & Muthukrishnan, S. (2012). "Budget optimization for online campaigns with positive carryover effects." WINE-12, pp. 86–99. — [Boutilier & Lu reference list](https://www.auai.org/uai2016/proceedings/papers/246.pdf)
  - Amin, K., Kearns, M., Key, P., & Schwaighofer, A. (2012). "Budget optimization for sponsored search: Censored learning in MDPs." UAI-12, pp. 543–553. — [Boutilier & Lu reference list](https://www.auai.org/uai2016/proceedings/papers/246.pdf)
  - Content of both not read. Overlap **Medium–Low** (single advertiser).
- **Brown, D. B., & Smith, J. E. (2020). "Index Policies and Performance Bounds for Dynamic Selection Problems." Management Science 66(7):3029–3050.** — [DOI](https://doi.org/10.1287/mnsc.2019.3342)
  - Abstract: a decision maker "repeatedly selects a set of items from a larger collection". The example is "the dynamic assortment problem with demand learning". Policies and bounds come from "a Lagrangian relaxation of the DP that relaxes the constraint limiting the number of items that may be selected". The abstract then states performance guarantees under mild conditions; it was truncated in our retrieval, and we read the claim as asymptotic optimality. — [Crossref abstract via DOI](https://doi.org/10.1287/mnsc.2019.3342)
  - Attributes: A adaptive; N not studied (sub-problems do include Bayesian learning); H yes; W no.
  - Relation, Overlap **Medium**: a planner rationing slots across learning sub-problems, decomposed by a price.
- **Brown, D. B., & Zhang, J. (2022). "Dynamic Programs with Shared Resources and Signals: Dynamic Fluid Policies and Asymptotic Optimality." Operations Research 70(5):3015–3033.** — [DOI](https://doi.org/10.1287/opre.2021.2181)
  - Abstract: "repeatedly allocating a limited resource across subsystems". Examples are adaptive clinical trials (allocating patients to treatments "in an effort to learn about the efficacy of treatments") and R&D capital budgeting with randomly evolving budgets. The method is dynamic fluid policies, shown asymptotically optimal (per the title). — [Crossref abstract via DOI](https://doi.org/10.1287/opre.2021.2181)
  - Attributes: A adaptive; N not studied; H yes; W no.
  - Relation, Overlap **Medium**: resource split across learning subsystems, but dynamic and asymptotic (many units).
- **Brown, D. B., & Zhang, J. (2023). "Technical Note—On the Strength of Relaxations of Weakly Coupled Stochastic Dynamic Programs." Operations Research 71(6):2374–2389.** — [DOI](https://doi.org/10.1287/opre.2022.2287)
  - Abstract: compares approximate linear programs (additive across subsystems) with Lagrangian relaxations. Both are upper bounds; the ALP bound "is a better bound but also, more difficult to compute". The paper gives a detailed theoretical comparison under fairly broad conditions; the precise conclusion was truncated in our retrieval and is **unverified**. — [Crossref abstract via DOI](https://doi.org/10.1287/opre.2022.2287)
  - Lists online advertising among its applications. Overlap **Medium–Low (method)**.
- **Brown, D. B., & Zhang, J. (2025). "Fluid Policies, Reoptimization, and Performance Guarantees in Dynamic Resource Allocation." Operations Research 73(2):1029–1045.** — [DOI](https://doi.org/10.1287/opre.2022.0601)
  - Bibliographic data verified; content not read. Overlap **Low–Medium**.
- **Learning versions of restless/weakly coupled models:**
  - **Ortner, R., Ryabko, D., Auer, P., & Munos, R. (2012). "Regret Bounds for Restless Markov Bandits." ALT 2012, LNCS 7568, pp. 214–228. arXiv:1209.2693.** Regret for restless bandits with unknown dynamics. — [arXiv](https://arxiv.org/abs/1209.2693)
  - **Wang, S., Huang, L., & Lui, J. C. S. (2020). "Restless-UCB, an Efficient and Low-complexity Algorithm for Online Restless Bandits." NeurIPS 2020. arXiv:2011.02664.** A learning policy "that follows the explore-then-commit framework", with regret Õ((N+M³)T^{2/3}). — [arXiv abstract](https://arxiv.org/abs/2011.02664); [NeurIPS 2020 index](https://papers.nips.cc/paper_files/paper/2020)
  - **Avrachenkov, K. E., & Borkar, V. S. (2022). "Whittle index based Q-learning for restless bandits with average reward." Automatica 139:110186.** Content from the title only. — [DOI](https://doi.org/10.1016/j.automatica.2022.110186)
  - **El Shar, I., & Jiang, D. R. (2023). "Weakly Coupled Deep Q-Networks." NeurIPS 2023. arXiv:2310.18803.** Trains DQN "subagents", one per subproblem, combined into an upper bound that guides the main agent; the tabular version, WCQL, converges almost surely. — [arXiv abstract](https://arxiv.org/abs/2310.18803)
  - **Carrara, N., Leurent, E., Laroche, R., Urvoy, T., Maillard, O.-A., & Pietquin, O. (2019). "Budgeted Reinforcement Learning in Continuous State Space." NeurIPS 2019. arXiv:1903.01004.** Extends BMDPs to continuous states and unknown dynamics via a "Budgeted Bellman Optimality operator". Here "budget" is a cost/risk threshold, not money. — [arXiv abstract](https://arxiv.org/abs/1903.01004); [NeurIPS 2019 index](https://papers.nips.cc/paper_files/paper/2019)
  - Attributes for all: A adaptive; N no; H yes/varies; W no. Overlap **Low–Medium**. Restless-UCB is notable because it uses explore-then-commit, as the paper's teams do.

### Inferences
- The paper's planner problem is a **one-shot weakly coupled problem**: a single linking budget constraint at t = 0, followed by independent sub-problems. Lagrangian decomposition prices the budget at λ, and each team solves max v_i V(B_i) − λB_i.
- With non-concave V, the Lagrangian dual only "sees" the concave envelope of V (standard duality theory; our inference). For two teams the duality gap can be large, so price/marginal-equalization rules can fail. This is exactly where the paper's corner-like solutions (the junior team is not funded to learn) come from.
- Boutilier & Lu's concavity is manufactured by **randomization**: the convex hull of deterministic budget-value points. This suggests a robustness point for the paper. If the planner could randomize over budget levels (lotteries), the relevant objective would be the concave envelope of V, and the "entry jump" would be smoothed away. The paper's non-concavity matters precisely because budgets are deterministic, one-shot commitments.
- None of these works asks how learning inside a sub-process changes the curvature of the sub-process's value in the resource. That is the paper's contribution relative to this literature.

### Gaps
- We did not read full texts of Hawkins (2003), Brown & Smith (2020) or Brown & Zhang (2022/2023/2025), so we cannot say whether any of them discusses non-concave sub-problem values or duality gaps explicitly.
- We found no Google/industry paper beyond Boutilier & Lu that splits an ad budget across learning sub-processes.

---

## Q3. Allocating a sampling budget across multiple bandit or selection problems (multi-bandit BAI, active learning in MAB, ranking & selection / OCBA, knowledge gradient)

### Takeaway
A mature literature splits a sample budget across alternatives or across separate bandit problems. Most of it is adaptive and pure-exploration (error probability or estimation error). The single most important finding for positioning is Frazier & Powell (2010). They show that **the marginal value of information is not concave**, and therefore that with many identical alternatives "it is often better to ignore some completely and focus on a smaller number than … to spread the measurement budget equally". Value is only "eventually concave". This is the paper's "non-concave V leads to a skewed split" logic, in a pure-learning setting with symmetric units.

### Cited Findings
- **Gabillon, V., Ghavamzadeh, M., Lazaric, A., & Bubeck, S. (2011). "Multi-Bandit Best Arm Identification." Advances in Neural Information Processing Systems 24 (NIPS 2011), pp. 2222–2230.** — [NeurIPS PDF](https://proceedings.nips.cc/paper_files/paper/2011/file/c4851e8e264415c4094e4e85b0baa7cc-Paper.pdf); [HAL](https://hal.archives-ouvertes.fr/hal-00632523)
  - Model/result (from the proceedings and HAL description): best-arm identification in several bandit problems simultaneously under one sampling budget. GapE focuses samples on arms whose means are close to the best arm's mean in the same bandit; GapE-V also uses variances. Error-probability bounds are given, plus adaptive versions that estimate the unknown complexity online. — [NeurIPS PDF](https://proceedings.nips.cc/paper_files/paper/2011/file/c4851e8e264415c4094e4e85b0baa7cc-Paper.pdf); [HAL](https://hal.archives-ouvertes.fr/hal-00632523)
  - Attributes: A adaptive; N no (the objective is error probability); H no (bandits weighted equally); W no.
  - Relation, Overlap **Medium–High (structure)**: a single sample budget split across several independent learning problems is very close to "budget across teams of bandits". There is no exploitation spend, no ex-ante commitment and no value weights.
- **Bubeck, S., Wang, T., & Viswanathan, N. "Multiple Identifications in Multi-Armed Bandits." arXiv:1205.3181 (2012).** The ICML 2013 venue is **unverified**.
  - Successive accepts and rejects; "this idea … applies to the multi-bandit best arm identification problem". — [arXiv abstract](https://arxiv.org/abs/1205.3181)
  - Overlap **Medium–Low**.
- **Antos, A., Grover, V., & Szepesvári, C. (2008). "Active Learning in Multi-armed Bandits." ALT 2008, LNCS, pp. 287–302. Journal version: "Active learning in heteroscedastic noise." Theoretical Computer Science 411(29–30):2712–2728 (2010).** — [ALT DOI](https://doi.org/10.1007/978-3-540-87987-9_25); [TCS DOI](https://doi.org/10.1016/j.tcs.2010.04.007)
  - Attributes: A adaptive; N no; H no; W no. Overlap **Medium–Low**.
- **Carpentier, A., Lazaric, A., Ghavamzadeh, M., Munos, R., & Auer, P. (2011). "Upper-Confidence-Bound Algorithms for Active Learning in Multi-Armed Bandits." ALT 2011. Extended arXiv version 2015 adds A. Antos as an author (arXiv:1507.04523).** — [arXiv](https://arxiv.org/abs/1507.04523)
  - Problem: "estimating uniformly well the mean values of several distributions given a finite budget of samples". With known variances, the optimal allocation is "proportional to their variance"; with unknown variances, adaptive UCB-on-variance allocation, with finite-sample excess-error bounds. — [arXiv abstract](https://arxiv.org/abs/1507.04523)
  - Attributes: A adaptive; N no (estimation loss is convex and decreasing in samples, so the allocation is interior and balanced); H through variances; W no.
  - Relation, Overlap **Medium–Low**: a useful contrast. With convex losses the planner balances, whereas the paper's non-concave value produces corner-like skew.
- **Chen, C.-H., Lin, J., Yücesan, E., & Chick, S. E. (2000). "Simulation Budget Allocation for Further Enhancing the Efficiency of Ordinal Optimization." Discrete Event Dynamic Systems 10(3):251–270.** This is OCBA. — [DOI](https://doi.org/10.1023/A:1008349927281)
  - Content from standard knowledge (not re-read): allocate simulation replications across designs to maximize an approximation of the probability of correct selection.
  - Attributes: A sequential/asymptotic rule; N no; H no; W no. Overlap **Low–Medium** (one selection decision, not separately valued units).
- **Glynn, P., & Juneja, S. (2004). "A Large Deviations Perspective on Ordinal Optimization." Proc. 2004 Winter Simulation Conference, pp. 565–573.** — [DOI](https://doi.org/10.1109/WSC.2004.1371364)
  - Content from standard knowledge: a static allocation that is optimal in large-deviations rate.
  - Overlap **Low–Medium**.
- **Frazier, P. I., Powell, W. B., & Dayanik, S. (2008). "A Knowledge-Gradient Policy for Sequential Information Collection." SIAM Journal on Control and Optimization 47(5):2410–2439.** — [DOI](https://doi.org/10.1137/070693424)
  - Content from standard knowledge: a one-step-lookahead value-of-information sampling rule for ranking and selection.
  - Overlap **Low–Medium**.
- **Frazier, P. I., & Powell, W. B. (2010). "Paradoxes in Learning and the Marginal Value of Information." Decision Analysis 7(4):378–403.** — [DOI](https://doi.org/10.1287/deca.1100.0190); [EconPapers](https://econpapers.repec.org/RePEc:inm:ordeca:v:7:y:2010:i:4:p:378-403)
  - Abstract: in Bayesian R&S ("allocate an information collection budget as efficiently as possible to choose the best among several alternatives"), "the marginal value of information is not concave, leading to algorithmic difficulties and apparent paradoxes". — [Crossref abstract via DOI](https://doi.org/10.1287/deca.1100.0190)
  - Key paradox: "when there are many identical alternatives, it is often better to ignore some completely and focus on a smaller number than it is to spread the measurement budget equally across all the alternatives". — [Crossref abstract via DOI](https://doi.org/10.1287/deca.1100.0190)
  - The value of information is "eventually concave", i.e., "concave when the number of measurements of each alternative is large enough". The paper proposes a new fully sequential strategy that handles the non-concavity. That strategy is commonly referred to as KG(*); the name is our recollection and **unverified** from the abstract. — [Crossref abstract via DOI](https://doi.org/10.1287/deca.1100.0190)
  - Attributes: A can be sequential, but the paradox is about static allocations; N = **yes** (value of information); H = no (identical alternatives in the paradox); W = no.
  - Relation, Overlap **High (mechanism)**: non-concave value of information leads to concentrating on fewer units, and "eventually concave" implies abundance leads to spreading. It lacks the paper's exploitation spend, heterogeneous values (v1 > v2) and no-learning benchmark W.
- **Chick, S. E., & Inoue, K. (2001). "New Two-Stage and Sequential Procedures for Selecting the Best Simulated System." Operations Research 49(5):732–743.** — [DOI](https://doi.org/10.1287/opre.49.5.732.10615)
- **Chick, S. E., Branke, J., & Schmidt, C. (2010). "Sequential Sampling to Myopically Maximize the Expected Value of Information." INFORMS Journal on Computing 22(1):71–80.** — [DOI](https://doi.org/10.1287/ijoc.1090.0327)
- **Chick, S. E., & Frazier, P. (2012). "Sequential Sampling with Economics of Selection Procedures." Management Science 58(3):550–569.** — [DOI](https://doi.org/10.1287/mnsc.1110.1425)
- **Ryzhov, I. O., Powell, W. B., & Frazier, P. I. (2012). "The Knowledge Gradient Algorithm for a General Class of Online Learning Problems." Operations Research 60(1):180–195.** — [DOI](https://doi.org/10.1287/opre.1110.0999)
  - For these four we verified bibliographic data only; content is inferred from titles. All are value-of-information-based sampling allocation. Overlap **Low–Medium**.

### Inferences
- The R&S/value-of-information community already knows that non-concave value of information pushes toward concentrating samples, and that the value becomes concave once enough samples are taken. The paper's V(B) (a jump at entry, then a decline in V'/W') is the analogue of this "eventually concave" value of information, with two additions:
  - the budget also buys exploitation (impressions), not just information;
  - the teams are asymmetric (v1 > v2).
- In the active-learning-in-MAB problem, losses are convex, so the planner spreads samples in proportion to variance. The paper's non-concave V gives the opposite (skewed) recommendation at low budgets. The two literatures bracket the paper.

### Gaps
- We did not read the full text of Frazier & Powell (2010) to check whether they analyze heterogeneous alternatives or a "with vs. without learning" benchmark. The abstract mentions only identical alternatives in the paradox.

---

## Q4. Master algorithms that allocate rounds across base learners, and rising/rotting/improving bandits (learners that improve with investment)

### Takeaway
Corralling and model-selection papers are the closest ML formalization of "a master allocating a resource (rounds) across learners whose performance depends on how much they get". CORRAL's stated main challenge is precisely not to "starve a base algorithm that might perform uncompetitively initially but would eventually outperform others if given enough feedback". That is the online-learning face of the paper's entry-jump non-concavity. Improving/rising bandits formalize "learning-by-doing" units: the per-pull reward grows with cumulative pulls, so cumulative value is convex in investment and benchmarks commit to a single arm.

### Cited Findings
- **Agarwal, A., Luo, H., Neyshabur, B., & Schapire, R. E. (2017). "Corralling a Band of Bandit Algorithms." COLT 2017 (PMLR v65). arXiv:1612.06246.** — [arXiv](https://arxiv.org/abs/1612.06246)
  - Abstract: build "a master algorithm that performs almost as well as the best base algorithm if it were to be run on its own". "The main challenge is that when run with a master, base algorithms unavoidably receive much less feedback and it is thus critical that the master not starve a base algorithm that might perform uncompetitively initially but would eventually outperform others if given enough feedback." Solved by OMD with a special mirror map (log-barrier) and a learning-rate schedule. — [arXiv abstract](https://arxiv.org/abs/1612.06246)
  - Attributes: A adaptive; N = implicitly yes (starvation is a minimum-feedback threshold), though not modeled as a value function; H no (common reward scale, best-of objective); W no.
  - Relation, Overlap **Medium**: same "learners need enough resource before they pay off" tension. The objective is winner-take-all regret, not a weighted sum of team values, and there is no ex-ante split.
- **Foster, D. J., Krishnamurthy, A., & Luo, H. (2019). "Model selection for contextual bandits." NeurIPS 2019. arXiv:1906.00531.** — [arXiv](https://arxiv.org/abs/1906.00531); [NeurIPS 2019 index](https://papers.nips.cc/paper_files/paper/2019)
  - Result: model selection over nested linear policy classes with Õ(T^{2/3} d_{m*}^{1/3}) regret without knowing d_{m*}. — [arXiv abstract](https://arxiv.org/abs/1906.00531)
  - Overlap **Low–Medium**.
- **Pacchiano, A., Phan, M., Abbasi-Yadkori, Y., Rao, A., Zimmert, J., Lattimore, T., & Szepesvári, C. (2020). "Model Selection in Contextual Stochastic Bandit Problems." NeurIPS 2020. arXiv:2003.01704.** — [arXiv](https://arxiv.org/abs/2003.01704); [NeurIPS 2020 index](https://papers.nips.cc/paper_files/paper/2020)
  - Result: a meta-algorithm over base algorithms with a "smoothing transformation", giving O(√T) model-selection guarantees, plus a lower bound showing Ω(√T) is unavoidable even if one base has O(log T) regret. — [arXiv abstract](https://arxiv.org/abs/2003.01704)
  - Overlap **Medium–Low**.
- **Pacchiano, A., Dann, C., Gentile, C., & Bartlett, P. (2020). "Regret Bound Balancing and Elimination for Model Selection in Bandits and RL." arXiv:2012.13045** (preprint; we found no venue).
  - Rule: "In each round, our approach plays a base algorithm to keep the candidate regret bounds of all remaining base algorithms balanced, and eliminates algorithms that violate their candidate bound." — [arXiv abstract](https://arxiv.org/abs/2012.13045)
  - Attributes: A adaptive; N no; H no; W no.
  - Relation, Overlap **Medium**: an explicit balancing rule for allocating rounds across learners.
- **Cutkosky, A., Dann, C., Das, A., Gentile, C., Pacchiano, A., & Purohit, M. (2021). "Dynamic Balancing for Model Selection in Bandits and RL." ICML 2021 (PMLR v139).** — [PMLR](https://proceedings.mlr.press/v139/cutkosky21a.html)
  - Title and authors verified on the PMLR index; content not read. Overlap **Medium–Low**.
- **Heidari, H., Kearns, M., & Roth, A. (2016). "Tight Policy Regret Bounds for Improving and Decaying Bandits." Proc. IJCAI-16.** The third author follows the standard citation; our first-page extract showed only the first two names. — [IJCAI PDF](https://www.ijcai.org/proceedings/2016/0224.pdf)
  - Abstract: the reward of each arm "changes monotonically every time the decision maker pulls that arm". Motivation: "settings in which we must give a series of homogeneous tasks to a finite set of arms (workers) whose performance may improve (due to learning) or decay (due to loss of interest) with repeated trials". Regret is measured against "the optimal policy that knows the reward functions" (policy regret). — [IJCAI PDF](https://www.ijcai.org/proceedings/2016/0224.pdf)
  - Attributes: A adaptive; N = yes, in the sense that cumulative reward is convex in pulls when per-pull reward increases (our inference); H yes; W no.
  - Relation, Overlap **Medium–High (learning-by-doing units)**: this is the formal "allocate work across workers who learn" problem. The learning is skill growth, not Bayesian learning about a market state.
- **Levine, N., Crammer, K., & Mannor, S. (2017). "Rotting Bandits." NeurIPS 2017. arXiv:1702.07274.** — [arXiv](https://arxiv.org/abs/1702.07274); [NeurIPS 2017 index](https://papers.nips.cc/paper_files/paper/2017)
  - "each arm's expected reward decays as a function of the number of times it has been pulled" (motivated by online advertising, recommendation, crowdsourcing). — [arXiv abstract](https://arxiv.org/abs/1702.07274)
  - The opposite curvature, which favors spreading. Follow-up: Seznec, Locatelli, Carpentier, Lazaric & Valko, "Rotting bandits are not harder than stochastic ones," AISTATS 2019 (arXiv:1811.11043). — [arXiv](https://arxiv.org/abs/1811.11043)
  - Overlap **Low–Medium (contrast)**.
- **Metelli, A. M., Trovò, F., Pirola, M., & Restelli, M. (2022). "Stochastic Rising Bandits." ICML 2022. arXiv:2212.03798.** — [arXiv](https://arxiv.org/abs/2212.03798)
  - Rested and restless arms with "monotonically non-decreasing" expected payoff; R-ed-UCB / R-less-UCB with regret down to Õ(T^{2/3}) in some cases; application to online model selection. — [arXiv abstract](https://arxiv.org/abs/2212.03798)
  - Overlap **Medium**.
- **Mussi, M., Montenegro, A., Trovò, F., Restelli, M., & Metelli, A. M. (2024). "Best Arm Identification for Stochastic Rising Bandits." ICML 2024. arXiv:2302.07510.** — [arXiv](https://arxiv.org/abs/2302.07510)
  - Options "are learning entities whose performance improves (in expectation) over time (e.g., online best model selection)". Fixed-budget BAI via R-UCBE and R-SR; guarantees "with a sufficiently large budget". — [arXiv abstract](https://arxiv.org/abs/2302.07510)
  - Attributes: A adaptive; N yes (rising); H yes; W no.
  - Relation, Overlap **Medium–High (learners improving with investment under a fixed budget)**. Related: Fiandri, Metelli & Trovò (2025), "Thompson Sampling-like Algorithms for Stochastic Rising Bandits," arXiv:2505.12092. — [arXiv](https://arxiv.org/abs/2505.12092)
- **Blum, A., & Ravichandran, K. (2024). "Nearly-tight Approximation Guarantees for the Improving Multi-Armed Bandits Problem." arXiv:2404.01198.** — [arXiv](https://arxiv.org/abs/2404.01198)
  - Each arm's reward is "a concave and increasing function of the number of times that arm has been pulled". Any randomized online algorithm suffers an Ω(√k) approximation factor; they give an O(√k) algorithm when the optimal arm's maximum reward is known, and O(√k log k) without it. — [arXiv abstract](https://arxiv.org/abs/2404.01198)
  - Overlap **Medium–High**.
- **Blum, A., Garicano, M., Ravichandran, K., & Sharma, D. (2025). "Algorithm Design and Stronger Guarantees for the Improving Multi-Armed Bandits Problem." arXiv:2511.10619.** — [arXiv](https://arxiv.org/abs/2511.10619)
  - Motivation: "a formal model for allocating effort under uncertainty, motivated by scenarios such as investing research effort into new technologies, performing clinical trials, and hyperparameter selection from learning curves". Known lower bounds are Ω(k) (deterministic) and Ω(√k) (randomized) "relative to the optimal arm". Proposes parameterized algorithm families learned from offline data. — [arXiv abstract](https://arxiv.org/abs/2511.10619)
  - Overlap **Medium–High**.
- **Patil, V., Nair, V., Ghalme, G., & Khan, A. (2022). "Mitigating Disparity while Maximizing Reward: Tight Anytime Guarantee for Improving Bandits." arXiv:2208.09254** (venue **unverified**). — [arXiv](https://arxiv.org/abs/2208.09254)
  - Tension between "maximizing the cumulative reward" and "ensuring that arms with better long-term rewards get sufficient opportunities even if they initially have low rewards". In the horizon-unaware setting, the authors show that "the two objectives are aligned". — [arXiv abstract](https://arxiv.org/abs/2208.09254)
  - Relation, Overlap **Medium**: the "junior team needs enough investment to show its value" issue, framed as fairness.
- **Lattimore, T., Crammer, K., & Szepesvári, C. (2014). "Optimal Resource Allocation with Semi-Bandit Feedback." arXiv:1406.3840** (commonly cited as UAI 2014; venue **unverified**). — [arXiv](https://arxiv.org/abs/1406.3840)
  - A manager "should distribute available resources among the jobs". Each job's completion probability "increases linearly until it equals one". Job difficulty is unknown; regret bounds are given, and learning is faster as the problem becomes "resource-laden". — [arXiv abstract](https://arxiv.org/abs/1406.3840)
  - Attributes: A adaptive; N no (the response min(1, ·) is concave); H yes (difficulties); W no.
  - Relation, Overlap **Medium**: a planner allocating across units with unknown response, but with concave response.

### Inferences
- If per-pull reward rises with experience, cumulative value is a sum of increasing terms and so convex in pulls. The optimal offline policy then concentrates on one arm; the improving-bandit benchmark is literally "the optimal arm". This is the learning-by-doing route to concentration. The paper's route is different: a fixed learning cost (τ probes) plus a bounded value of information. Both produce non-concavity at small budgets.
- CORRAL's starvation problem is the online, adaptive version of the paper's ex-ante result that a junior team with too little budget cannot learn. The paper can be framed as the "static, value-weighted" counterpart of corralling.

### Gaps
- None of these papers compares allocations "with vs. without learning", or weights learners by different per-unit values (v1 ≠ v2).
- We did not verify Heidari et al.'s exact claim about the optimal offline policy for improving arms.

---

## Q5. Hyperparameter and training-budget allocation across configurations or tasks that learn

### Takeaway
AutoML allocates a compute budget across learning runs whose value rises with the resource received (learning curves). Hyperband explicitly hedges the breadth-vs-depth (concentration) trade-off. These methods are adaptive, use winner-take-all objectives over interchangeable configurations, and do not model value-weighted units or with/without-learning comparisons.

### Cited Findings
- **Jamieson, K., & Talwalkar, A. (2016). "Non-stochastic Best Arm Identification and Hyperparameter Optimization." AISTATS 2016 (PMLR v51). arXiv:1502.07943.** — [arXiv](https://arxiv.org/abs/1502.07943); [PMLR v51 index](https://proceedings.mlr.press/v51/)
  - Casts hyperparameter optimization as non-stochastic best-arm identification (successive halving). "By allocating more resources to promising hyperparameter settings, we typically achieve comparable test accuracies an order [of magnitude faster]". — [arXiv abstract](https://arxiv.org/abs/1502.07943)
  - Attributes: A adaptive; N not modeled; H no; W no. Overlap **Medium–Low**.
- **Li, L., Jamieson, K., DeSalvo, G., Rostamizadeh, A., & Talwalkar, A. (2018). "Hyperband: A Novel Bandit-Based Approach to Hyperparameter Optimization." Journal of Machine Learning Research 18 (2018), 1–52. arXiv:1603.06560.** — [arXiv](https://arxiv.org/abs/1603.06560)
  - "a pure-exploration non-stochastic infinite-armed bandit problem where a predefined resource like iterations, data samples, or features is allocated to randomly sampled configurations". Over an order-of-magnitude speedup vs. BO competitors. — [arXiv abstract and journal-ref](https://arxiv.org/abs/1603.06560)
  - Our recollection (**unverified** in this session) is that the paper frames the core issue as the "n versus B/n" trade-off (many configurations with little resource each vs. few with much) and hedges it with several successive-halving brackets. An earlier ICLR 2017 version is **unverified**.
  - Attributes: A adaptive; N implicit; H no; W no.
  - Relation, Overlap **Medium**: the breadth-vs-depth question is the paper's skew-vs-balance question, without value weights or a no-learning benchmark.
- **Swersky, K., Snoek, J., & Adams, R. P. (2014). "Freeze-Thaw Bayesian Optimization." arXiv:1406.3896.** — [arXiv](https://arxiv.org/abs/1406.3896)
  - Uses partial training information "to decide whether to pause training and start a new model, or resume the training of a previously-considered model", with a learning-curve kernel and an information-theoretic decision rule. — [arXiv abstract](https://arxiv.org/abs/1406.3896)
  - Overlap **Medium**.
- **Domhan, T., Springenberg, J. T., & Hutter, F. (2015). "Speeding Up Automatic Hyperparameter Optimization of Deep Neural Networks by Extrapolation of Learning Curves." IJCAI 2015.** — [IJCAI 2015 index](https://www.ijcai.org/proceedings/2015)
  - Title verified on the IJCAI 2015 index. Content from standard knowledge: extrapolates learning curves to stop unpromising runs early.
  - Overlap **Low–Medium**.
- **Li, Y., Jiang, J., Gao, J., Shao, Y., Zhang, C., & Cui, B. (2020). "Efficient Automatic CASH via Rising Bandits." Proc. AAAI 34(04):4763–4771. arXiv:2012.04371.** — [arXiv](https://arxiv.org/abs/2012.04371)
  - Alternates per-algorithm HPO (BO) with algorithm selection, modeled by "Rising Bandits, a CASH-oriented Multi-Armed Bandits (MAB) variant". The abstract was truncated in our retrieval. — [arXiv abstract](https://arxiv.org/abs/2012.04371)
  - Attributes: A adaptive; N yes (rising); H yes; W no. Overlap **Medium**.
- **Jaderberg, M., et al. (2017). "Population Based Training of Neural Networks." arXiv:1711.09846.** — [arXiv](https://arxiv.org/abs/1711.09846)
  - "effectively utilises a fixed computational budget to jointly optimise a population of models and their hyperparameters". — [arXiv abstract](https://arxiv.org/abs/1711.09846)
  - Attributes: A adaptive; N no; H no; W no. Overlap **Medium–Low**.
- **Graves, A., Bellemare, M. G., Menick, J., Munos, R., & Kavukcuoglu, K. (2017). "Automated Curriculum Learning for Neural Networks." ICML 2017 (PMLR v70). arXiv:1704.03003.** — [arXiv](https://arxiv.org/abs/1704.03003); [PMLR v70 index](https://proceedings.mlr.press/v70/)
  - A learning-progress signal is "provided as a reward signal to a nonstationary multi-armed bandit algorithm, which then determines a stochastic syllabus". In some cases the method halves the time to reach satisfactory performance. — [arXiv abstract](https://arxiv.org/abs/1704.03003)
  - Attributes: A adaptive; N not modeled; H tasks differ; W no.
  - Relation, Overlap **Medium**: a master allocating training resource across tasks by marginal learning progress.
- **Matiisen, T., Oliver, A., Cohen, T., & Schulman, J. (2020). "Teacher–Student Curriculum Learning." IEEE Transactions on Neural Networks and Learning Systems 31(9):3732–3740.** — [DOI](https://doi.org/10.1109/TNNLS.2019.2934906)
  - Content not read. Overlap **Low–Medium**.
- **Bateni, M., Esfandiari, H., HosseinGhorban, S., Mirrokni, A., & Shahdaei, R. (2025). "Budget Allocation for Unknown Value Functions in a Lipschitz Space." arXiv:2510.10605.** — [arXiv](https://arxiv.org/abs/2510.10605)
  - "optimally allocating a bounded budget to explore the space of intermediate models" (feature selection, structure search, tuning), formalized over unknown-value functions in a Lipschitz space. — [arXiv abstract](https://arxiv.org/abs/2510.10605)
  - Overlap **Low–Medium**.
- **Data-budget splits across subgroups or data sources:**
  - **Rolf, E., Worledge, T., Recht, B., & Jordan, M. I. (2021). "Representation Matters: Assessing the Importance of Subgroup Allocations in Training Data." ICML 2021. arXiv:2103.03399.** Casts "data collection as part of the learning process" and studies how dataset composition (allocation across subgroups) drives subgroup and population objectives. — [arXiv abstract](https://arxiv.org/abs/2103.03399)
  - **Hashimoto, T. (2021). "Model Performance Scaling with Multiple Data Sources." ICML 2021.** Title verified on the PMLR v139 index; content not read. — [PMLR v139 index](https://proceedings.mlr.press/v139/)
  - Overlap **Medium–Low**: these use smooth (typically power-law, concave) learning curves, so allocations are interior.

### Inferences
- AutoML's breadth-vs-depth question (Hyperband) is the closest practical twin of the paper's "skewed vs. balanced" question. Successive halving's answer (start broad, then concentrate) is adaptive. The paper studies the committed, ex-ante version with value-weighted, non-interchangeable units, where adaptivity is unavailable.
- Smooth power-law learning curves (Rolf; Hashimoto) give concave value and interior splits. The paper's entry jump is a sharp departure from that convention.

### Gaps
- We did not verify Hyperband's "n vs. B/n" wording or the conference version, nor Domhan et al.'s and Hashimoto's content.

---

## Q6. R&D and project funding with learning, staged investment, portfolios of experiments, and the non-concave value of information

### Takeaway
Economics and OM have long studied funding several uncertain projects or approaches when funding generates information. Azevedo et al. (2020, JPE) is the single closest analogue to the paper's comparative static.
- A firm allocates a fixed pool of experimental users across ideas to maximize the **sum of per-idea "production functions"** (value of information).
- The allocation is **concentrated** ("go big": all resources to one idea when data is scarce) if the production function is convex near zero (thin-tailed priors, the Radner–Stiglitz case).
- It is **spread** ("go lean") if the production function is concave (fat tails), or when resources are abundant.
- It is a pure-learning model with symmetric ideas and no no-learning benchmark.

### Cited Findings
- **Azevedo, E. M., Deng, A., Montiel Olea, J. L., Rao, J., & Weyl, E. G. (2020). "A/B Testing with Fat Tails." Journal of Political Economy 128(12):4614–4672.** RePEc shows a garbled page range (4614–4000); the end page 4672 comes from another listing. — [DOI](https://doi.org/10.1086/710607); [IDEAS](https://ideas.repec.org/a/ucp/jpolec/doi10.1086-710607.html); [2019 working-paper PDF used for quotes](https://www.gwern.net/doc/statistics/decision/2019-azevedo.pdf)
  - JPE abstract: "if the tails of the unobserved distribution of innovation quality are not too fat, the standard approach of using a few high-powered 'big' experiments is optimal. However, if the distribution is very fat tailed, a 'lean' strategy of trying more ideas, each with possibly smaller sample sizes, is preferred." — [IDEAS](https://ideas.repec.org/a/ucp/jpolec/doi10.1086-710607.html)
  - Model (WP): "The firm's problem is how to assign its total budget of available users to the different ideas, and to then select which ideas to implement." The firm "should allocate users to maximize the sum of production functions of all ideas" (Proposition 2, production function decomposition). — [WP PDF](https://www.gwern.net/doc/statistics/decision/2019-azevedo.pdf)
  - Theorem 2 (small n), with prior tails ~ power law of coefficient α: marginal product f′(n) ∝ n^{(α−3)/2}. If α > 3, the marginal product at n = 0 is zero, giving increasing returns (convex near 0); if α < 3, it is infinite (concave). Theorem 1 (large n): marginal product decreases as 1/n². — [WP PDF](https://www.gwern.net/doc/statistics/decision/2019-azevedo.pdf)
  - Corollary 1, identical priors and more than one idea:
    - α < 3: "it is optimal to run experiments on all ideas (… 'go lean')".
    - α > 3 and N sufficiently small: "the firm should allocate all experimental resources to one idea (… 'go big')".
    - Remark 1: if N is large enough, it is optimal to experiment on all ideas.
    - [WP PDF](https://www.gwern.net/doc/statistics/decision/2019-azevedo.pdf)
  - Intuition (WP): with thin tails "a small bit of information is unlikely to change the optimal action … This makes the value of information convex for small sample sizes". The authors tie this to Radner & Stiglitz (1984) and show it reverses under fat tails. — [WP PDF](https://www.gwern.net/doc/statistics/decision/2019-azevedo.pdf)
  - Bing EXP evidence (WP): tail coefficient "considerably smaller than 3". "The top 2% of ideas are responsible for 74.8% of the historical gains". Experimenting on 20% more ideas with the same users would raise productivity by 17.05%. Extensions include fixed costs of experimentation. — [WP PDF](https://www.gwern.net/doc/statistics/decision/2019-azevedo.pdf)
  - Attributes: A = ex ante (a static allocation of users); N = **yes** (value of information convex near 0 with thin tails); H = no in Corollary 1 (identical priors; heterogeneity allowed in general); W = no explicit no-learning benchmark (f(0) = 0 is the no-experiment value).
  - Relation, Overlap **High**: same planner structure (Σ value(B_i) s.t. ΣB_i ≤ T) and same comparative static (non-concavity leads to concentration; abundance leads to spreading). It differs in that the budget buys only information, units are symmetric, and the source of the non-concavity is the tails of the prior rather than a fixed probing cost.
- **Value-of-information non-concavity lineage** (the mechanism behind V's entry jump):
  - **Radner, R., & Stiglitz, J. (1984). "A Nonconcavity in the Value of Information."** In Boyer, M. & Kihlstrom, R. (eds.), *Bayesian Models in Economic Theory*, North-Holland. Chapter details **unverified**; its existence and result are as cited in Azevedo et al. — [Azevedo WP](https://www.gwern.net/doc/statistics/decision/2019-azevedo.pdf)
  - **Chade, H., & Schlee, E. (2002). "Another Look at the Radner–Stiglitz Nonconcavity in the Value of Information." Journal of Economic Theory 107(2):421–452.** — [DOI](https://doi.org/10.1006/jeth.2001.2960). Per Azevedo et al., Chade & Schlee show "even when information is measured by n, the convexity result depends on substantial assumptions. Nevertheless, they show that convexity does hold with some generality." — [Azevedo WP](https://www.gwern.net/doc/statistics/decision/2019-azevedo.pdf)
  - **Moscarini, G., & Smith, L. (2002). "The Law of Large Demand for Information." Econometrica 70(6):2351–2366.** — [DOI](https://doi.org/10.1111/1468-0262.00378). Listed by Azevedo et al. among works on the value of information, which "is often convex close to zero". — [Azevedo WP](https://www.gwern.net/doc/statistics/decision/2019-azevedo.pdf)
  - **De Lara, M., & Gilotte, L. (2007). "A tight sufficient condition for Radner–Stiglitz nonconcavity in the value of information." Journal of Economic Theory 137(1):696–708.** — [DOI](https://doi.org/10.1016/j.jet.2007.01.014)
  - Overlap **Medium–High (mechanism)**. None of these is an allocation-across-units paper.
- **Roberts, K., & Weitzman, M. L. (1981). "Funding Criteria for Research, Development, and Exploration Projects." Econometrica 49(5):1261–1288.** — [DOI](https://doi.org/10.2307/1912754); [IDEAS](https://ideas.repec.org/a/ecm/emetrp/v49y1981i5p1261-88.html); [Econometric Society page](https://www.econometricsociety.org/publications/econometrica/1981/09/01/funding-criteria-research-development-and-exploration-projects); [MIT working paper](https://dspace.mit.edu/handle/1721.1/35160)
  - Abstract-level: the sequential nature of R&D/exploration "requires optimal funding criteria to take account of the fact that subsequent funding decisions will be made throughout the future". They model a "Sequential Development Project (SDP)", and "in an important special case, an explicit formula is derived". — [Econometric Society page](https://www.econometricsociety.org/publications/econometrica/1981/09/01/funding-criteria-research-development-and-exploration-projects)
  - The often-cited reading (index/reservation-value funding criteria, and the option value of learning justifying funding of projects with low expected value) is **unverified** from the full text.
  - Attributes: A sequential; N not framed this way; H projects differ; W implicitly (option value of learning).
  - Overlap **Medium**.
- **Weitzman, M. L. (1979). "Optimal Search for the Best Alternative." Econometrica 47(3):641–654** (end page from memory). — [DOI](https://doi.org/10.2307/1910412)
  - Content from standard knowledge: "Pandora's rule", which opens boxes in order of reservation value and stops when the best sampled reward exceeds all remaining reservation values.
  - Attributes: A sequential; N no; H yes; W no. Overlap **Low–Medium**.
- **Nelson, R. R. (1961). "Uncertainty, Learning, and the Economics of Parallel Research and Development Efforts." Review of Economics and Statistics 43(4):351–[364].** — [DOI](https://doi.org/10.2307/1927475)
  - Content not read; the title indicates parallel R&D approaches under uncertainty with learning.
  - Overlap **Medium (conceptual)**.
- **Granot, D., & Zuckerman, D. (1991). "Optimal Sequencing and Resource Allocation in Research and Development Projects." Management Science 37(2):140–156.** — [DOI](https://doi.org/10.1287/mnsc.37.2.140)
  - Content not read. Overlap **Low–Medium**.
- **Loch, C. H., Terwiesch, C., & Thomke, S. (2001). "Parallel and Sequential Testing of Design Alternatives." Management Science 47(5):663–678.** — [DOI](https://doi.org/10.1287/mnsc.47.5.663.10480)
  - Abstract: parallel testing is faster "but does not take advantage of the potential for learning between tests". The optimal mix comes from a dynamic program, as a function of testing cost, prior knowledge and lead time; with imperfect testing, "the attractiveness of parallel strategies decreases". — [Crossref abstract via DOI](https://doi.org/10.1287/mnsc.47.5.663.10480)
  - Overlap **Medium–Low**.
- **Ding, M., & Eliashberg, J. (2002). "Structuring the New Product Development Pipeline." Management Science 48(3):343–363.** — [DOI](https://doi.org/10.1287/mnsc.48.3.343.7727)
  - Abstract: "multiple approaches may be simultaneously funded at the various NPD stages … The managerial challenge is to construct ex ante an appropriate NPD pipeline by choosing the right number of approaches to be funded at each stage". The optimum is driven by cost, survival probability and expected profitability; applied to pharma. — [Crossref abstract via DOI](https://doi.org/10.1287/mnsc.48.3.343.7727)
  - Attributes: A ex ante; N not framed; H no; W no.
  - Overlap **Medium**: ex-ante funding breadth, but the approaches are substitutes for one product.
- **Staged investment and experimentation in entrepreneurship:**
  - Bergemann, D., & Hege, U. (1998). "Venture capital financing, moral hazard, and learning." Journal of Banking & Finance 22(6–8):703–735. — [DOI](https://doi.org/10.1016/S0378-4266(98)00017-X)
  - Kerr, W. R., Nanda, R., & Rhodes-Kropf, M. (2014). "Entrepreneurship as Experimentation." Journal of Economic Perspectives 28(3):25–48. — [DOI](https://doi.org/10.1257/jep.28.3.25)
  - Content of both not read. A commonly cited RAND Journal of Economics (2005) paper by Bergemann & Hege, "The Financing of Innovation: Learning and Stopping", is **unverified**: Crossref did not return it. Overlap **Low**.
- **Feit, E. M., & Berman, R. (2019). "Test & Roll: Profit-Maximizing A/B Tests." Marketing Science 38(6):1038–1058.** — [DOI](https://doi.org/10.1287/mksc.2019.1194)
  - Described by Azevedo et al. as a model "for how long to test new advertisements and how long to run them". — [Azevedo WP](https://www.gwern.net/doc/statistics/decision/2019-azevedo.pdf)
  - Attributes: an ex-ante test length within ONE unit; N/H/W not applicable.
  - Relation, Overlap **Medium (within-team τ choice)**: the marketing analogue of choosing the probing length τ up front.

### Inferences
- The paper can be positioned as **"Azevedo et al. with exploitation spending, asymmetric unit values and an explicit no-learning benchmark"**:
  - In Azevedo et al. the only use of the resource is information.
  - In the paper, the budget both buys information (probing) and is the object being optimized in exploitation (impressions at v_i). The value-of-information non-concavity therefore interacts with v1 > v2.
  - That interaction is what produces the paper's two-regime result: more skew when the junior cannot afford to learn, more balance once both learn.
- In Radner–Stiglitz terms, the paper's "fixed-cost-like jump at entry" is a value of information that is convex near zero. The paper's micro-foundation is a fixed probing length needed before any posterior shift can change the bid; Azevedo et al.'s is prior tails.

### Gaps
- We did not read Roberts & Weitzman (1981), Nelson (1961), Granot & Zuckerman (1991) or the VC/staging papers in full; their main results are given only at abstract or title level.
- We could not verify Bergemann & Hege (2005) or the chapter details of Radner & Stiglitz (1984).

---

## Q7. Direct searches: budget across learning agents, campaigns, platforms, sub-agents, prompts and skills ("budget allocation to bandit learners", "learning-by-doing across units", "planner allocates exploration budget across sub-problems")

### Takeaway
Two applied clusters are closest in setting.
1. **Advertising**: one advertiser splits a budget across campaigns, sub-campaigns, platforms or channels using bandit learning. Examples are Nuara et al. (GP + MCKP), Han & Arndt (a "multi-agent system of contextual & continuous bandits"), Avadhanula et al. (BwK across platforms) and Deng et al. (per-channel budgets to delegated autobidders suffice for the global optimum).
2. **LLM compute** (2024–2026): rollouts and test-time attempts are allocated across prompts, and compute across agent teams. Two 2026 preprints derive the paper's qualitative logic for LLMs. Bae: the value of one more attempt peaks at intermediate difficulty, so the optimal static allocation is inverted-U and starves hopeless inputs. Wan et al.: S-shaped per-query utility with emergence thresholds, a global shadow price and "rational abandonment".

None of these lets the units be autonomous Bayesian explore-then-commit learners whose budget funds both probing and exploitation, and none compares splits with vs. without learning.

### Cited Findings
**Advertising: budget across campaigns, platforms and channels with learning**
- **Nuara, A., Trovò, F., Gatti, N., & Restelli, M. (2018). "A Combinatorial-Bandit Algorithm for the Online Joint Bid/Budget Optimization of Pay-per-Click Advertising Campaigns." Proc. AAAI-18, 32(1). Extended: "Online joint bid/daily budget optimization of Internet advertising campaigns," Artificial Intelligence 305:103663 (2022).** — [AAAI DOI](https://doi.org/10.1609/aaai.v32i1.11888); [AAAI OJS](https://ojs.aaai.org/index.php/AAAI/article/view/11888); [AIJ DOI](https://doi.org/10.1016/j.artint.2022.103663)
  - Abstract: a campaign has sub-campaigns "each with a different ad—and a cumulative daily budget". The method is a combinatorial bandit using "Gaussian Processes to estimate stochastic functions, Bayesian bandit techniques to address the exploration/exploitation problem, and a dynamic programming technique to solve a variation of the Multiple-Choice Knapsack problem". — [AAAI OJS](https://ojs.aaai.org/index.php/AAAI/article/view/11888)
  - Attributes: A adaptive (daily re-split); N not modeled (learning is centralized in the planner); H yes (sub-campaign value curves differ); W no.
  - Relation, Overlap **Medium–High (setting)**.
- **Han, B., & Arndt, C. (2021). "Budget Allocation as a Multi-Agent System of Contextual & Continuous Bandits." Proc. 27th ACM SIGKDD (KDD '21), pp. 2937–2945.** — [DOI](https://doi.org/10.1145/3447548.3467124) (abstract retrieved via Semantic Scholar)
  - Abstract: the Contextual Budgeting System (CBS) is "a budget allocation framework using a multi-agent system of contextual & continuous Multi-Armed Bandits". It "decomposes the problem into a convex optimization problem whose objective is drawn using Thompson Sampling" and uses transfer learning for cold-start campaigns. Deployed on all of Lyft's new-driver-acquisition spend, with a "(22 ± 10)% improvement in the mean Cost Per user Acquisition". — [DOI](https://doi.org/10.1145/3447548.3467124)
  - Attributes: A adaptive; N no (a convex program); H yes; W no.
  - Relation, Overlap **Medium–High (closest name to "teams of bandits")**: here "agents" are per-campaign bandit models combined by a convex allocator. The cold-start issue echoes the junior team's learning need.
- **Avadhanula, V., Colini-Baldeschi, R., Leonardi, S., Sankararaman, K. A., & Schrijvers, O. (2021). "Stochastic bandits for multi-platform budget optimization in online advertising." Proc. Web Conference 2021 (WWW '21), pp. 2805–2817. arXiv:2103.10246.** — [DOI](https://doi.org/10.1145/3442381.3450074); [arXiv](https://arxiv.org/abs/2103.10246)
  - Spend one campaign budget across m platforms "without knowing the value", modeled as stochastic BwK over bid m-tuples. Discrete-bid regret O(OPT√(mn/B) + √(mn·OPT)), with matching-type lower bounds. — [arXiv abstract](https://arxiv.org/abs/2103.10246)
  - Attributes: A adaptive; N no; H yes (platforms); W no. Overlap **Medium**.
- **Deng, Y., Golrezaei, N., Jaillet, P., Liang, J. C. N., & Mirrokni, V. (2023). "Multi-channel Autobidding with Budget and ROI Constraints." ICML 2023 (PMLR v202). arXiv:2302.01523.** — [arXiv](https://arxiv.org/abs/2302.01523); [PMLR v202 index](https://proceedings.mlr.press/v202/)
  - The advertiser "authorizes a channel to procure impressions on her behalf" and controls only per-channel budgets and target ROIs. Optimizing only per-channel ROIs "can be arbitrarily worse" than the global optimum, whereas the advertiser "can achieve the global optimal conversion when she only optimizes over per-channel budgets". The authors give a bandit-feedback learning algorithm. — [arXiv abstract](https://arxiv.org/abs/2302.01523)
  - Attributes: A adaptive (online learning of budgets); N no (channel agents optimize given the budget); H yes; W no.
  - Relation, Overlap **High (structure: a planner allocating budgets to delegated bidding agents)**, but the channel agents do not learn, so there is no learning-induced non-concavity.
- **Ge, L., Xu, Y., Chu, J., Cramer, D., Li, F., Paulson, K., & Song, R. (2024). "Multi-Task Combinatorial Bandits for Budget Allocation." arXiv:2409.00561.** — [arXiv](https://arxiv.org/abs/2409.00561)
  - Online budget allocation "across various ad lines in each campaign" with a Bayesian hierarchical model and Thompson sampling. — [arXiv abstract](https://arxiv.org/abs/2409.00561)
  - Overlap **Medium**.
- **Gangopadhyay, B., Wang, Z., Chiappa, A. S., & Takamatsu, S. (2025). "Adaptive Budget Optimization for Multichannel Advertising Using Combinatorial Bandits." arXiv:2502.02920.** — [arXiv](https://arxiv.org/abs/2502.02920)
  - A combinatorial bandit with a "saturating mean function" and change-point detection. — [arXiv abstract](https://arxiv.org/abs/2502.02920)
  - Concave/saturating response is assumed. Overlap **Medium–Low**.
- **Song, M., et al. (2026). "DARA: Few-shot Budget Allocation in Online Advertising via In-Context Decision Making with RL-Finetuned LLMs." WWW 2026. arXiv:2601.14711.** — [arXiv](https://arxiv.org/abs/2601.14711)
  - Single-advertiser LLM bidding planner. Overlap **Low**.

**LLM compute: rollouts, test-time attempts, tokens and agent teams**
- **Snell, C., Lee, J., Xu, K., & Kumar, A. "Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters." arXiv:2408.03314 (2024). ICLR 2025 Oral, under the title "…than Scaling Parameters for Reasoning".** — [arXiv](https://arxiv.org/abs/2408.03314); [OpenReview](https://openreview.net/forum?id=4FWAwZtd2n)
  - Asks how much a fixed test-time compute budget can improve performance on a prompt. — [arXiv abstract](https://arxiv.org/abs/2408.03314)
  - Quantitative claims (e.g., efficiency gains of a prompt-adaptive "compute-optimal" strategy) are **unverified** here; the abstract was truncated in our retrieval.
  - Overlap **Low–Medium**.
- **Damani, M., Shenfeld, I., Peng, A., Bobu, A., & Andreas, J. "Learning How Hard to Think: Input-Adaptive Allocation of LM Computation." arXiv:2410.04707 (2024); ICLR 2025 (poster).** — [arXiv](https://arxiv.org/abs/2410.04707); [OpenReview](https://openreview.net/forum?id=6qUUgw9bAZ)
  - "predicts the distribution of rewards given an input and computation budget, then allocates additional computation to inputs for which it is predicted to be most useful". — [arXiv abstract](https://arxiv.org/abs/2410.04707)
  - Attributes: A adaptive per input; N not modeled; H yes; W no. Overlap **Medium–Low**.
- **Li, Z., Chen, C., Yang, T., Ding, T., Sun, R., Zhang, G., Huang, W., & Luo, Z.-Q. (2025). "Knapsack RL: Unlocking Exploration of LLMs via Optimizing Budget Allocation." arXiv:2509.25849.** — [arXiv](https://arxiv.org/abs/2509.25849)
  - Under uniform rollout budgets, "easy tasks consistently succeed while difficult tasks consistently fail, both producing zero gradients" in GRPO. Each task's exploration is treated as an "item" with a distinct "value" and "cost" in a knapsack. The result raises the effective ratio of non-zero policy gradients by 20–40%, reallocates budget "from tasks where learning is saturated to those where it is most impactful", and allows e.g. 93 rollouts on hard problems. — [arXiv abstract](https://arxiv.org/abs/2509.25849)
  - Attributes: A per-iteration knapsack; N = effectively yes (learning value exists only in a difficulty window); H yes; W no.
  - Relation, Overlap **Medium–High (mechanism, AI setting)**.
- **Zong, Y., Wang, Y., Hu, X., Jiang, J., & Shen, Z.-J. M. (2026). "CERO: Where and When to Allocate Rollouts for RL Post-Training." arXiv:2610.09679.** — [arXiv](https://arxiv.org/abs/2610.09679)
  - Coordinates "a finite rollout budget over the entire training horizon" using "a concave surrogate utility of cumulative prompt exposure" and an online primal-dual scheduler with "a shared budget price". — [arXiv abstract](https://arxiv.org/abs/2610.09679)
  - Attributes: A adaptive; N no (concave by construction); H yes; W no.
  - Overlap **Medium**: a contrast showing how LLM work often concavifies the problem.
- **Bae, J. (2026). "Give Up to Get More: Priors, Not Policies, Govern Test-Time Compute Allocation." arXiv:2611.06372.** — [arXiv](https://arxiv.org/abs/2611.06372)
  - "Because the value of one more attempt peaks at intermediate difficulty, the optimal static allocation is inverted-U and gives little to inputs that are hopeless at the current budget." Difficulty-proportional rules capture at most 13% of oracle gain on hard workloads. In a survey of 221 allocation papers, at least 13 give the hardest inputs the most attempts. With a verifier and a prior, Thompson sampling raises the solved share on the hardest workload from 14% to 27%; "information, not the policy, drives the gain". — [arXiv abstract](https://arxiv.org/abs/2611.06372)
  - Attributes: A both static and adaptive; N = yes (per-input success curves); H yes; W = partial (with vs. without prior information).
  - Relation, Overlap **High (AI-extension analogue)**.
- **Wan, X., Zhu, S., Cai, J., Chen, G., Huang, X., Zhou, W., & Sun, M. (2026). "The Shadow Price of Reasoning: Economic Perspective on Optimal Budget Allocation for LLMs." arXiv:2606.03092.** — [arXiv](https://arxiv.org/abs/2606.03092)
  - Models "per-query reasoning utility with a shifted-surge function" and derives "an optimal allocation policy based on a global shadow price that equilibrates marginal utility under resource scarcity". CLEAR "performs rational abandonment and reallocates resources from insolvent queries to solvable queries near their emergence thresholds", with up to 3× global accuracy vs. uniform allocation in scarce regimes. — [arXiv abstract](https://arxiv.org/abs/2606.03092)
  - Attributes: A ex-ante/global; N = yes (S-shaped utility); H yes; W no.
  - Relation, Overlap **High (AI-extension analogue)**.
- **Samway, K., D'souza, D., Darwiche Domingues, O., Fadaee, M., Yi-Chern, T., & Dziri, N. (2026). "Scaling Inference-Time Compute with Teams of Coding Agents." arXiv:2610.17471.** — [arXiv](https://arxiv.org/abs/2610.17471)
  - "We therefore formulate team design as a compute allocation problem". Teams beat solo agents but cost 3–7× as much; "planning is the most valuable use of workers"; a heterogeneous 17-agent team comes within 1.4 points of a homogeneous 5-agent team at 70% lower cost. — [arXiv abstract](https://arxiv.org/abs/2610.17471)
  - Empirical. Overlap **Medium (AI agent teams)**.
- **Liu, X., Li, H., Li, S., Fang, H., Xu, F., Shi, F., & Evans, J. (2026). "Markets, Not Planners: Decentralized Orchestration of LLM Agents with Private Information." arXiv:2608.23867** (working paper). — [arXiv](https://arxiv.org/abs/2608.23867)
  - Centralized planners "require private information (e.g., agents' execution costs)" and are manipulable: "a single inserted preference nearly doubles a favored agent's task share under a centralized LLM allocator". The alternative is AgentLance, a VCG-style repeated labor market with hierarchical subcontracting. — [arXiv abstract](https://arxiv.org/abs/2608.23867)
  - Overlap **Low–Medium**: a planner-vs-market alternative for the authors' AI extension.

**Robots and MARL: practice or exploration budgets across skills or agents**
- **Vats, S., Harithas, S., Akbulut, M. T., Raghunathan, A., & Konidaris, G. (2026). "Deliberate Practice: Learning Robot Skills under a Budget." arXiv:2608.13415.** — [arXiv](https://arxiv.org/abs/2608.13415)
  - Computes "a provably budget-optimal allocation—practicing skills that maximize expected cumulative reward while being learnable within the budget". It estimates time-to-mastery and the reward that skills unlock, and solves a bilinear program. — [arXiv abstract](https://arxiv.org/abs/2608.13415)
  - Attributes: A ex-ante plan; N = yes (a skill is worth practicing only if masterable within budget, a threshold); H yes; W no.
  - Relation, Overlap **Medium–High (mechanism)**.
- **Oh, D., Yoon, M., & Kim, H. J. (2026). "Quality-Aware Exploration Budget Allocation for Cooperative Multi-Agent Reinforcement Learning." arXiv:2605.01865** (submitted to Neurocomputing). — [arXiv](https://arxiv.org/abs/2605.01865)
  - A per-agent Reward Signal Quality metric "concentrates the exploration budget on agents with reliable signals". — [arXiv abstract](https://arxiv.org/abs/2605.01865)
  - Overlap **Medium–Low**.

### Inferences
- The advertising papers show that the paper's setting (an advertiser splitting a budget across campaign-level bidding units) is practically important and that learning-based allocators already exist. In all of them, though, learning sits at the planner (who learns response curves), not inside units that must "pay to learn". The response curves are also typically concave or saturating. The paper's distinctive move is to put the learning inside each team and show this makes the per-team value non-concave.
- Deng et al.'s result (per-channel budgets alone attain the global optimum when channel agents are optimal) suggests a natural question for the paper: does budget-only delegation remain sufficient when channel agents must learn? The paper's planner also chooses τ (the probing length), which hints that budget alone may not suffice. This is our conjecture, not a cited result.
- The 2026 LLM papers (Bae; Wan et al.; Knapsack RL; Deliberate Practice) independently rediscover "value only within a window / abandonment of units that cannot reach the threshold". This makes the paper's planned AI-agent extension timely. The paper can claim a micro-founded (Bayesian learn-then-exploit) source of the threshold and an explicit no-learning benchmark, which these works lack.

### Gaps
- We found no paper that allocates budgets across RTB campaigns where each campaign learns an unknown competition state through probing.
- We could not read the full texts of Han & Arndt (ACM DL returned 403) or Nuara et al. to check their curvature assumptions.
- 2026 arXiv items are preprints and not peer-reviewed. Their claims are as stated in the abstracts.
- The phrase "teams of bandits" was not found as an established term. The closest is Han & Arndt's "multi-agent system of contextual & continuous bandits".

---

## Q8. The 3–5 closest works and what is and isn't already done (does anyone show that learning makes the optimal split more or less concentrated?)

### Takeaway
The pieces of the paper's story exist separately:
- non-concave value of information leads to concentrated allocations, and abundance leads to spreading (Azevedo et al. 2020; Frazier & Powell 2010);
- a planner splits a budget across independent sub-processes in advertising, with concave values and greedy MCKP (Boutilier & Lu 2016);
- budgets are delegated to channel bidding agents (Deng et al. 2023);
- LLM compute allocation starves "hopeless" units (Bae 2026; Wan et al. 2026).

**We found no work that (i) gives each unit an internal explore-then-commit learner whose budget funds both learning and exploitation, (ii) weights units by different values (v1 > v2), and (iii) compares the optimal split with learning vs. a no-learning benchmark.** In particular, the two-regime result is not documented in what we found: learning makes the split more skewed when the junior cannot afford to learn and more balanced once both learn.

### Cited Findings
- **Closest #1: Azevedo et al. (2020, JPE), "A/B Testing with Fat Tails."** Overlap **High**. — [DOI](https://doi.org/10.1086/710607); [WP](https://www.gwern.net/doc/statistics/decision/2019-azevedo.pdf)
  - Already done: a static budget split across units maximizing the sum of per-unit value-of-information "production functions". With a convex-near-zero production function and scarce data, "allocate all experimental resources to one idea"; with abundant data, experiment on all ideas. — [WP](https://www.gwern.net/doc/statistics/decision/2019-azevedo.pdf)
  - Not done: exploitation spending, asymmetric unit values, a no-learning benchmark W, or the planner's choice of exploration length.
- **Closest #2: Frazier & Powell (2010, Decision Analysis), "Paradoxes in Learning and the Marginal Value of Information."** Overlap **High (mechanism)**. — [DOI](https://doi.org/10.1287/deca.1100.0190)
  - Already done: non-concave marginal value of information, so it is "often better to ignore some completely and focus on a smaller number" than to spread equally; value is "eventually concave". — [DOI](https://doi.org/10.1287/deca.1100.0190)
  - Not done: units valued differently, exploitation, or an RTB/market learning model.
- **Closest #3: Boutilier & Lu (2016, UAI), "Budget Allocation using Weakly Coupled, Constrained MDPs."** Overlap **High (architecture)**. — [UAI PDF](https://www.auai.org/uai2016/proceedings/papers/246.pdf)
  - Already done: a planner allocates a global ad budget across many independent sub-processes using per-unit value-of-budget curves (MCKP, greedy, plus online reallocation).
  - Not done: learning within units. Their V is provably concave (via randomized policies), the opposite of the paper.
- **Closest #4: Deng et al. (2023, ICML), "Multi-channel Autobidding with Budget and ROI Constraints"** (together with Han & Arndt 2021 KDD and Nuara et al. 2018 AAAI). Overlap **High/Medium–High (setting)**. — [arXiv](https://arxiv.org/abs/2302.01523); [KDD DOI](https://doi.org/10.1145/3447548.3467124); [AAAI](https://ojs.aaai.org/index.php/AAAI/article/view/11888)
  - Already done: an advertiser splits budget across delegated bidding agents or campaigns, with online learning of the split.
  - Not done: the units' own learning, non-concavity, or a with/without-learning comparison.
- **Closest #5 (AI-extension analogues): Bae (2026), "Give Up to Get More", and Wan et al. (2026), "The Shadow Price of Reasoning".** Overlap **High for the planned token-budget extension**. — [Bae](https://arxiv.org/abs/2611.06372); [Wan et al.](https://arxiv.org/abs/2606.03092)
  - Already done: per-unit value of compute peaks at intermediate difficulty or is S-shaped. The optimal static allocation is inverted-U, with abandonment of hopeless units and a global shadow price.
  - Not done: units that are learning agents, a Bayesian learn-then-exploit micro-foundation, or a no-learning benchmark.
- **Honorable mentions:**
  - Vats et al. (2026), Deliberate Practice: practice only skills "learnable within the budget". — [arXiv](https://arxiv.org/abs/2608.13415)
  - Agarwal et al. (2017), CORRAL: do not "starve" learners that would eventually outperform. — [arXiv](https://arxiv.org/abs/1612.06246)
  - Gabillon et al. (2011): one sample budget split across several bandits. — [NeurIPS](https://proceedings.nips.cc/paper_files/paper/2011/file/c4851e8e264415c4094e4e85b0baa7cc-Paper.pdf)
  - Li et al. (2018), Hyperband: breadth vs. depth. — [arXiv](https://arxiv.org/abs/1603.06560)
  - Heidari et al. (2016) and the improving/rising-bandits line: workers improve by doing. — [IJCAI](https://www.ijcai.org/proceedings/2016/0224.pdf)
  - Tran-Thanh et al. (2010), ε-first: explore-then-commit under a budget, which is the within-team protocol. — [AAAI](https://ojs.aaai.org/index.php/AAAI/article/view/7758)

### Inferences
- **On "more vs. less concentrated":**
  - Prior work establishes mainly the direction "non-concavity, hence concentration (relative to equal or proportional spreading)". This appears in Azevedo et al.'s "go big", Frazier & Powell's paradox, Bae's starvation of hopeless inputs and Wan et al.'s abandonment.
  - It also establishes "abundance, hence spreading": Azevedo's Remark 1 and Frazier & Powell's "eventually concave".
  - What we did not find is a comparison against a no-learning benchmark showing that the possibility of learning can make the split either more skewed or more balanced, depending on whether the junior unit's budget clears its learning threshold. Nor did we find this interacting with asymmetric unit values. This is the paper's most defensible novelty claim.
  - Phrase it as "to our knowledge, not previously documented", given search limits.
- **Suggested positioning sentence** (our wording): "Our planner problem is a one-shot weakly coupled resource allocation (Hawkins 2003; Adelman & Mersereau 2008; Boutilier & Lu 2016) in which, unlike budgeted MDPs whose values are concave in budget, each unit's value is non-concave because it must pay to learn. This is the Radner–Stiglitz/Frazier–Powell non-concavity, which Azevedo et al. (2020) show drives 'big vs. lean' experimentation. We add exploitation spending, asymmetric unit values and a no-learning benchmark, and show learning can either concentrate or balance the optimal split."
- **Natural robustness checks suggested by the literature:**
  - Randomized budgets would concavify V (Boutilier & Lu's convex hull) and remove the entry jump in expectation.
  - Adaptive reallocation after probing (DBRA in Boutilier & Lu; CORRAL; successive halving) would let a planner hedge the junior team's learning threshold.
  - With many teams (n large), Lagrangian/fluid decomposition becomes asymptotically tight (Brown & Smith 2020; Brown & Zhang 2022). Non-concavity might then matter less for aggregate value but still determine which units are funded to learn. This is our inference.

### Gaps
- Our search was limited to roughly 30 tool calls. We did not search the OM/economics literature on production allocation across plants with learning curves (classic learning-by-doing), strategic-experimentation papers (multi-agent experimentation without a planner), or RTB-specific multi-campaign budget papers beyond those listed. A follow-up search there could surface a closer comparative static.
- Several classic items were verified only bibliographically (Gittins; Whittle; Nelson; Granot & Zuckerman; Weitzman; OCBA; KG). Their content statements rest on standard knowledge and are flagged as such above.
- Unverified items to check before citing: Bergemann & Hege (2005, RAND); Radner & Stiglitz (1984) chapter pages; Lattimore et al. (2014) venue (UAI 2014?); Bubeck et al. (2013) venue (ICML 2013?); Patil et al. (2022) venue; Hyperband's ICLR 2017 version and its "n vs. B/n" wording; Snell et al.'s quantitative claims; Brown & Zhang (2023)'s main conclusion (truncated abstract); Boutilier & Lu's page numbers (52–61 vs. PMLR R14:682–691).
