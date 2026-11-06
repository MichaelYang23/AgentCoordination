# Foundations: bandits, Bayesian optimal learning, explore-then-commit (ETC) and optimal stopping of experimentation — when is separating learning from exploitation near-optimal?

Notes for positioning "Orchestrating Agent Teams: Budget Allocation in Real-Time Bidding" (Yang, Zhu, Mookerjee; WITS 2026). WITS model recap, used in the "Relation" lines: each team faces a first-price RTB market with an unknown binary competition state θ ∈ {θL, θH} (prior π0), win probability q_θ(b) = b/(b+θ), and pays b only on a win. A probing agent bids b^I = √(θL·θH) for τ periods (τ fixed ex ante by the planner). It then hands the win count w (a sufficient statistic) to an exploitation agent, which bids a constant budget-paced bid. The planner splits the total budget T between teams worth v1 > v2 and compares the result with a no-learning benchmark W.

Conventions. "Overlap" rates how close a paper's model or result is to the WITS paper (High/Medium/Low). Bibliographic details were checked against the paper itself or against a reference list or landing page fetched in this session. Anything I could not confirm is marked "unverified". "Inference" means my own reasoning, not a claim made by the cited paper.

---

## Q1. Classic foundations: Gittins index, Whittle restless bandits, Bayesian optimal learning, knowledge gradient, value of information — and why Gittins does not apply here

### Takeaway
The Gittins index solves an infinite-horizon, discounted problem with independent arms and frozen passive arms. It is documented to lose optimality under any of four conditions: a fixed exploration budget followed by a terminal choice, a finite undiscounted horizon, switching costs, or exploration that is disentangled from exploitation. The WITS setting has a finite undiscounted horizon and an exploration budget followed by exploitation, plus a budget-coupled continuous control and a planner-level resource split. So a reviewer's "bandit" alternative cannot be an index policy. It must be either the Bayes-optimal dynamic program, which is tractable here because θ is binary, or a heuristic such as TS, UCB or IDS. Two strands of the value-of-information literature give the WITS planner results a theoretical home: the nonconcavity of the value of information (Radner–Stiglitz; Chade–Schlee; Frazier–Powell) and Whittle's Lagrangian decoupling of many units. The one-armed Bayesian bandit has an optimal policy that is a stopping rule, i.e. explore-then-commit to the safe arm. That structurally supports ETC, but with a data-dependent stopping time.

### Cited Findings
- **Gittins, J. C. (1979). "Bandit processes and dynamic allocation indices." Journal of the Royal Statistical Society, Series B, 41(2):148–177.** Companion paper: Gittins & Jones (1979), "A dynamic allocation index for the discounted multiarmed bandit problem," Biometrika 66(3):561–565. Page-range conflict: the Tehrani et al. and Zhou et al. reference lists give pp. 148–177, while Lizzeri et al.'s list gives 148–164. — [Lizzeri et al. refs](https://arxiv.org/abs/2404.19116); [Tehrani et al. refs](https://arxiv.org/abs/1206.5345); [Zhou et al. refs](https://arxiv.org/abs/2607.29375)
  - Model/result: the Bayesian multi-armed bandit (MAB) is an MDP over posterior states. Gittins showed the optimal policy has an index structure, with complexity linear in the number of arms rather than exponential. — [Tehrani, Zhai & Zhao 2012, §I.A](https://arxiv.org/abs/1206.5345)
  - Limits documented in the literature:
    - Budget then terminal choice: "The Gittins index (Whittle, 1983; Gittins et al., 2011) is optimal for discounted cumulative reward, but not for a fixed exploration budget followed by a single terminal choice." — [Guha 2026](https://arxiv.org/abs/2610.24156)
    - Finite undiscounted horizon: playing the arm with the largest finite-horizon index "is not Bayesian optimal anymore" for k-armed bandits, although it performs well in practice. — [Lattimore & Szepesvári book, §35.6 note 7](https://tor-lattimore.com/downloads/book/book.pdf)
    - Bayesian regret: "Gutin and Farias (2016) show that the Gittins analysis does not succeed in minimizing Bayesian regret over all sufficiently large horizons, and propose 'optimistic' Gittins indices." — [Bastani, Bayati & Khosravi](https://arxiv.org/abs/1704.09011)
    - Disentangled exploration: when exploration is separated from exploitation, the optimal policy "cannot be identified by an index à la Gittins." — [Lizzeri, Shmaya & Yariv 2024](https://arxiv.org/abs/2404.19116)
    - Switching costs: Banks & Sundaram (1994), "Switching costs and the Gittins index," Econometrica 62(3):687–694 (title and venue verified via [Simchi-Levi & Xu refs](https://arxiv.org/abs/1905.10825)). The usual summary is that switching costs break index optimality; I did not re-read the paper.
  - Relation (Overlap: Low): each WITS team solves a finite-horizon, undiscounted, budget-coupled control problem with a continuous action (the bid), and the planner couples the teams through one shared budget. None of the Gittins assumptions hold.
- **Gittins, Glazebrook & Weber (2011). *Multi-armed Bandit Allocation Indices*, 2nd ed. Wiley. DOI 10.1002/9780470980033.** The standard reference on index theory. — [Guha 2026 refs](https://arxiv.org/abs/2610.24156); [IDS refs](https://arxiv.org/abs/1403.5556). (Overlap: Low)
- **Niño-Mora (2011). "Computing a classic index for finite-horizon bandits." INFORMS J. Computing 23(2):254–267; Farias & Gutin (2022). "Optimistic Gittins indices." Operations Research 70(6):3432–3456.** Finite-horizon and undiscounted index variants. — [Zhou, Li & Wang 2026 refs](https://arxiv.org/abs/2607.29375). (Overlap: Low)
- **Whittle, P. (1988). "Restless bandits: activity allocation in a changing world." Journal of Applied Probability 25(A):287–298. DOI 10.2307/3214163.** — [Scilit record / search summary](https://www.scilit.net/publications/375e4ecb992249122330f47487d32bc0)
  - Model: n projects, m active at a time, and passive projects keep evolving.
  - Results: a Lagrange multiplier on the activity constraint defines an index, which reduces to the Gittins index when idle projects are static. Whittle conjectures that operating the m projects with the largest current index is nearly optimal when m and n are large in constant ratio. The index applies only to "indexable" models. — [search summary of the abstract](https://www.scilit.net/publications/375e4ecb992249122330f47487d32bc0)
  - Relation (Overlap: Medium): this is the canonical template for "many units coordinated by a planner under a shared resource." A Lagrangian price on the total budget decouples the teams, and the WITS split is a static (ex-ante) version of it.
- **Powell, W. B. & Ryzhov, I. O. (2012). *Optimal Learning*. John Wiley & Sons (Wiley Series in Probability and Statistics, vol. 841).** — [IDS paper reference list](https://arxiv.org/abs/1403.5556). This is the umbrella textbook on Bayesian optimal learning and knowledge-gradient (KG) methods that a reviewer would expect to see cited. I did not read its content in this session (see Gaps). (Overlap: Medium)
- **Frazier, P. I., Powell, W. B. & Dayanik, S. (2008). "A knowledge-gradient policy for sequential information collection." SIAM J. Control and Optimization 47(5):2410–2439.** — [Guha 2026 refs](https://arxiv.org/abs/2610.24156); [Princeton PDF](https://optimallearning.princeton.edu/Papers/Frazier%20Powell%20-%20Knowledge%20gradient%20policy.pdf)
  - Model: sequential Bayesian ranking and selection with independent normal populations, a common known variance, a finite sampling horizon and a terminal utility. — [Princeton listing / abstract](https://collaborate.princeton.edu/en/publications/a-knowledge-gradient-policy-for-sequential-information-collection/)
  - Results:
    - KG myopically maximizes the expected one-period increment in the value of information. It is optimal when a single period remains and in the limit of an infinite horizon.
    - In some special cases it is optimal for any fixed horizon. In the other cases its suboptimality is bounded.
    - The policy was introduced by Gupta & Miescke (1996).
    — [abstract summary](https://collaborate.princeton.edu/en/publications/a-knowledge-gradient-policy-for-sequential-information-collection/)
  - Caveat: "there are no general guarantees for KG, and even in some simple settings, it may not converge to optimality. In fact, it may select a suboptimal action in every period." — [Russo & Van Roy, IDS](https://arxiv.org/abs/1403.5556)
  - Relation (Overlap: Medium): the WITS probing phase is a measurement budget followed by a terminal decision (the exploitation bid), which makes it a ranking-and-selection-type problem. KG supplies a myopic value-of-information rule for continuing or stopping the probe.
- **Frazier, P. I. & Powell, W. B. (2010). "Paradoxes in learning and the marginal value of information." Decision Analysis 7(4):378–403. DOI 10.1287/deca.1100.0190.** — [EconPapers](https://econpapers.repec.org/RePEc:inm:ordeca:v:7:y:2010:i:4:p:378-403); [Princeton listing](https://collaborate.princeton.edu/en/publications/paradoxes-in-learning-and-the-marginal-value-of-information/)
  - Results: the value of information is nonconcave. "When there are many identical alternatives, it is often better to ignore some completely and focus on a smaller number." The value of information is "eventually concave", i.e. concave once each alternative has been measured enough. The paper proposes a new fully sequential strategy that handles the nonconcavity. — [abstract summary](https://collaborate.princeton.edu/en/publications/paradoxes-in-learning-and-the-marginal-value-of-information/)
  - Relation (Overlap: High for the planner-level results): WITS finds that learning creates value only within a budget window, that V'/W' jumps at entry, and that the split skews toward the senior team when the junior team cannot afford to learn. These are the same nonconcavity and "concentrate learning on fewer units" phenomena.
- **Radner, R. & Stiglitz, J. (1984). "A nonconcavity in the value of information"** (book chapter; publisher and pages unverified), and **Chade, H. & Schlee, E. (2002). "Another look at the Radner–Stiglitz nonconcavity in the value of information." Journal of Economic Theory 107(2):421–452.** — [EconPapers](https://econpapers.repec.org/RePEc:eee:jetheo:v:107:y:2002:i:2:p:421-452)
  - Results: Radner and Stiglitz showed that the marginal value of a small amount of information is zero, so the value of information has increasing returns over some range. Chade and Schlee give general sufficient conditions for this nonconcavity and discuss its robustness and why global concavity is hard to obtain. — [abstract summary](https://econpapers.repec.org/RePEc:eee:jetheo:v:107:y:2002:i:2:p:421-452)
  - Relation (Overlap: High, conceptual): a micro-foundation for the "jump at entry" and the bounded window in which learning pays off.
- **Lindley, D. V. (1956). "On a measure of the information provided by an experiment." Annals of Mathematical Statistics 27:986–1005. DOI 10.1214/aoms/1177728069.** The expected-information-gain criterion behind information-maximizing designs. — [Cheng & Huan refs](https://arxiv.org/abs/2509.21734). (Overlap: Low)
- **Robbins (1952). "Some aspects of the sequential design of experiments." Bull. AMS 58(5):527–535; Thompson (1933). Biometrika 25(3/4):285–294; Lai & Robbins (1985). "Asymptotically efficient adaptive allocation rules." Adv. Appl. Math. 6(1):4–22.** — [Gao et al. refs](https://arxiv.org/abs/1904.01763)
  - Lai–Robbins lower bound: lim inf R_t / log t ≥ Σ_a (μ[1] − μa) / KL(νa, ν[1]). — [Kaufmann, Cappé & Garivier 2016](https://arxiv.org/abs/1407.4443)
  - Robbins (1952) proposed "certainty equivalence with forcing", which spreads forced exploration over time, whereas ETC puts it all at the start. The book's verdict on spreading it out: "advantageous if the horizon is not known, but disadvantageous otherwise." — [Lattimore & Szepesvári §6.3](https://tor-lattimore.com/downloads/book/book.pdf)
  - (Overlap: Medium)
- **Bellman (1956). "A problem in the sequential design of experiments." Sankhyā 16(3/4)** — [Tehrani et al. refs](https://arxiv.org/abs/1206.5345); **Berry & Fristedt (1985). *Bandit Problems: Sequential Allocation of Experiments*. Chapman & Hall** — [Perchet et al. refs](https://arxiv.org/abs/1505.00369). (Overlap: Low–Medium)
- **Lattimore & Szepesvári (2020), Ch. 35 "Bayesian Bandits"** (§35.2 Optimal stopping; §35.3 One-armed Bayesian bandits; §35.4 Gittins index). — [book](https://tor-lattimore.com/downloads/book/book.pdf)
  - One-armed (retirement) problem with horizon n: "the Bayesian optimal policy is to retire in the first round t when g_{n−t+1}(S_t) ≤ μ2", where g is the undiscounted finite-horizon Gittins index. — [§35.6 note 7](https://tor-lattimore.com/downloads/book/book.pdf)
  - Exact Bayes-optimal dynamic programming can be feasible: with n = 50 and k = 5 (Bernoulli rewards, Beta prior) it has about 10^11 states, "not so large that the table cannot be stored on disk." — [§35.6 note 9](https://tor-lattimore.com/downloads/book/book.pdf)
  - Relation (Overlap: High): with a known "safe" option (the no-learning benchmark W), the Bayes-optimal finite-horizon policy is a stopping rule. That is exactly the ETC structure, except that the stopping time is data-dependent rather than fixed.

### Inferences
- Gittins does not apply to WITS for five reasons:
  1. The horizon is finite and there is no discounting.
  2. The budget is a stock consumed only on wins, so the state must include remaining budget.
  3. The control (the bid) is continuous.
  4. The planner couples teams through a single resource split rather than choosing one arm per period.
  5. The value of exploration is realized as future exploitation inside the same team ("future utilization").
- The relevant "bandit" benchmarks are therefore (a) the Bayes-optimal dynamic program over (posterior or log-likelihood ratio, remaining budget, time), which is low-dimensional because θ is binary, and (b) heuristics such as TS, UCB, IDS or greedy.
- Whittle and Lagrangian view: for an interior split, the planner's first-order condition equates marginal values, v1·V'(a) = v2·V'(T − a). Nonconcavity of V, which the Radner–Stiglitz and Frazier–Powell results lead one to expect when learning has a fixed entry cost, explains skewed or corner splits and the "jump at entry".
- The one-armed Bayesian bandit result is the cleanest theoretical support for "learn, then commit to the better of learned-policy versus safe-policy". It also shows that the optimal commitment time is a stopping time, not a constant.

### Gaps
- The contents of Powell & Ryzhov (2012) and DeGroot (1970), the publisher and pages of the Radner–Stiglitz (1984) chapter, the content of Banks & Sundaram (1994) and the citation for Gupta & Miescke (1996) were not verified in this session.
- I did not check Whittle's conditions for bandit superprocesses (arms with internal continuous controls), which would be the formal route for the continuous-bid issue.

---

## Q2. ETC theory: how suboptimal is explore-then-commit, and when is phased exploration rate-optimal or near-optimal?

### Takeaway
GLK (2016) prove that a single explore-then-commit phase costs a constant factor asymptotically: 2× against fully sequential policies in general, and in the known-gap or two-hypothesis case, 2× for SPRT-stopped ETC and 8× for fixed-length ETC. The rate stays logarithmic, so ETC is still rate-optimal when the gap is known. Three results show that separation itself is not the problem:
- Jin et al. (2021): a second short explore/commit pair (DETC) is exactly asymptotically optimal and needs only O(1) rounds.
- Rusmevichientong & Tsitsiklis (2010): phased exploration is rate-optimal whenever the best response is smooth in the parameter.
- Feit & Berman (2019): a profit-maximizing Bayesian "test & roll" is about as good as Thompson sampling.

The strongest counter-evidence comes from inventory-constrained revenue management. There, learning-while-doing (Wang, Deng & Ye) improves on the best-known regret rates of the separated learn-then-earn policies of Besbes & Zeevi (2009), with a matching lower bound, though for multi-parameter or nonparametric demand.

### Cited Findings
- **Garivier, A., Kaufmann, E. & Lattimore, T. (2016). "On explore-then-commit strategies." Advances in Neural Information Processing Systems 29 (NIPS 2016), pp. 784–792. arXiv:1605.08988.** Author order: the arXiv PDF lists Garivier, Kaufmann, Lattimore; the L&S bibliography lists Garivier, Lattimore, Kaufmann. — [arXiv](https://arxiv.org/abs/1605.08988); [L&S bibliography](https://tor-lattimore.com/downloads/book/book.pdf)
  - Model: a two-armed Gaussian bandit N(μi, 1) with known horizon T and regret as the objective. Three strategy classes:
    - fixed-design: explore each arm n times, n deterministic;
    - ETC: alternate the arms until a data-dependent stopping time τ, then commit;
    - fully sequential.
    — [arXiv](https://arxiv.org/abs/1605.08988)
  - Main result: regret ≈ C·log T/Δ, with tight upper and lower bounds in every cell.

    | | Fully sequential | ETC (stopping time) | Fixed-design |
    |---|---|---|---|
    | Gap Δ known | 1/2 | 1 | 4 |
    | Gap Δ unknown | 2 | 4 | n/a |

    — [arXiv §2](https://arxiv.org/abs/1605.08988)
  - Algorithms and bounds:
    - Known gap: SPRT-ETC achieves log T/Δ (Thm 2) and no ETC strategy does better (Thm 3). Δ-UCB achieves log T/(2Δ) (Thm 7), which matches the general lower bound (Thm 6).
    - Unknown gap: BAI-ETC achieves 4 log T/Δ (Thm 5), which is optimal within ETC (Thm 4).
    - Fixed-design optimum: n = ⌈(2/Δ²)·W(T²Δ⁴/(32π))⌉, with regret about 4 log T/Δ and always ≤ 2.04√T + Δ (Thm 1).
    — [arXiv](https://arxiv.org/abs/1605.08988)
  - Quotes: "strategies based on distinct phases of exploration and exploitation are necessarily suboptimal"; the obligation to commit "leads to regret asymptotically twice as large on average." The paper is explicitly motivated by A/B testing a website layout and then committing, and it cites Wald (1945) for the gains from sequential testing. — [arXiv §1](https://arxiv.org/abs/1605.08988)
  - Caveats (§6):
    - No non-trivial lower bound is possible for ETC with arbitrary non-uniform sampling, since UCB with an infinite stopping time is formally an ETC.
    - Uniform sampling is the optimal exploration rule in the two-armed Gaussian case.
    - For an ETC that explores with Track-and-Stop, the authors conjecture a worst-case factor of 2. When μ2 = … = μK, the relative gap to Lai–Robbins shrinks as K grows.
    — [arXiv](https://arxiv.org/abs/1605.08988)
  - Relation (Overlap: High): binary θ with known values is the "known gap" case. WITS fixes τ up front, which is the fixed-design class: asymptotically 4× the regret constant of SPRT-stopped ETC and 8× the fully sequential optimum. The reviewer's question is essentially the question this paper answers.
- **Lattimore, T. & Szepesvári, C. (2020). *Bandit Algorithms*. Cambridge University Press** (free online edition). — [PDF](https://tor-lattimore.com/downloads/book/book.pdf)
  - Theorem 6.1 (1-subgaussian rewards, m explorations per arm): R_n ≤ m·Σ Δi + (n − mk)·Σ Δi·exp(−mΔi²/4).
  - For k = 2, choosing m = max{1, ⌈(4/Δ²)·log(nΔ²/4)⌉} gives R_n ≤ min{nΔ, Δ + (4/Δ)(1 + max{0, log(nΔ²/4)})} (eq. 6.6), and hence R_n ≤ Δ + C√n. — [§6.1](https://tor-lattimore.com/downloads/book/book.pdf)
  - The catch is that the optimal m depends on the gap:
    - if m may depend only on n, then R_n = O(n^{2/3}) (Ex. 6.5a);
    - a data-dependent commitment time recovers C log n/Δ (Ex. 6.5b);
    - for every m there is an instance with R_n(ETC) ≥ c·min{n, n^{2/3}·k^{1/3}} (Ex. 15.6).
    — [§6.4, §15.5](https://tor-lattimore.com/downloads/book/book.pdf)
  - Experiment 7.1: "If ETC is tuned with the optimal choice of commitment time for each choice of Δ, then it outperforms the parameter-free UCB, though only by a relatively small margin. If, however, the commitment time must be chosen without the knowledge of Δ, then ETC will usually not outperform UCB." A later UCB variant beats even the optimally tuned ETC. — [§7.1](https://tor-lattimore.com/downloads/book/book.pdf)
  - Notes and bibliographic remarks:
    - ETC's per-step expected regret is monotonically decreasing.
    - Other names: "forced sampling", "explore-first", "explore-then-exploit", epoch-greedy (Langford & Zhang 2008), and phased exploration with greedy exploitation (PEGE).
    - Anscombe (1963) studied exploration and commitment for medical trials and "largely solves the problem in the Gaussian case."
    — [§6.2–6.3](https://tor-lattimore.com/downloads/book/book.pdf)
  - Relation (Overlap: High): the textbook reference reviewers will use. The key nuance for WITS is that θL and θH are known, so the gap is known, and in that case tuned ETC is rate-optimal and empirically competitive with UCB.
- **Jin, T., Xu, P., Xiao, X. & Gu, Q. (2021). "Double explore-then-commit: asymptotic optimality and beyond." COLT 2021, PMLR 134:2584–2633. arXiv:2002.09174.** — [arXiv](https://arxiv.org/abs/2002.09174); venue from the [Zhou et al. 2026 refs](https://arxiv.org/abs/2607.29375)
  - Model: K-armed bandit with 1-subgaussian rewards. DETC runs four stages:
    1. explore both arms;
    2. commit to the leader until it has T1 pulls;
    3. re-explore the arm that was not chosen until a test separates the two;
    4. commit for the rest of the horizon.
    — [arXiv §3](https://arxiv.org/abs/2002.09174)
  - Results:
    - Known gap: asymptotic regret rate 1/(2Δ), which is optimal, plus O(log(TΔ²)/Δ) and O(√T) bounds.
    - Unknown gap: 2/Δ, which is Lai–Robbins optimal. For K arms: Σ 2/Δi.
    - There is an anytime variant.
    - Batched DETC uses O(1) expected rounds while staying asymptotically optimal.
    - "DETC is the first non-fully-sequential algorithm that achieves such asymptotic optimality." "It is not necessary to use the outcome at each time step as in fully sequential algorithms such as UCB." Batched DETC improves the fixed-design ETC rate (4/Δ) "by a factor of 8."
    — [arXiv](https://arxiv.org/abs/2002.09174)
  - Relation (Overlap: High): GLK's suboptimality applies to a *single* explore/commit pair, and one extra short audit phase restores asymptotic optimality. This suggests a natural, still-modular extension of WITS: probe → exploit → brief re-probe check → exploit.
- **Rusmevichientong, P. & Tsitsiklis, J. N. (2010). "Linearly parameterized bandits." Mathematics of Operations Research 35(2):395–411. arXiv:0812.3465.** — [arXiv](https://arxiv.org/abs/0812.3465); venue from the [IDS refs](https://arxiv.org/abs/1403.5556)
  - Model: arms u in U_r ⊂ R^r with expected reward u'Z, where Z ∈ R^r is unknown (r ≥ 2). Objectives are regret and Bayes risk. — [arXiv](https://arxiv.org/abs/0812.3465)
  - Results:
    - On the unit sphere, regret and Bayes risk are Θ(r√T); the lower bound is 0.006·r√T (Thm 2.1).
    - PEGE ("phased exploration and greedy exploitation") runs cycles; cycle c has r exploration periods on a fixed basis followed by c greedy periods. It achieves O(r√T) when the arm set is strongly convex, i.e. has a smooth best-arm response (SBAR) (Thm 3.1).
    - For general compact arm sets, "the separation of exploration and exploitation may not be effective". An active-exploration policy (UE) achieves O(r√T·log^{3/2} T).
    - With finitely many arms, regret is O(log T).
    - For r = 1, the greedy policy has O(log T) Bayes risk (citing Mersereau et al. 2009).
    — [arXiv](https://arxiv.org/abs/0812.3465)
  - Mechanism: under SBAR, the instantaneous regret of a greedy decision is O(‖Z − Ẑ‖²) instead of O(‖Z − Ẑ‖), "and this enables us to separate exploration from exploitation." The authors call this "the first result that establishes the connection between a geometrical property (strong convexity) of the underlying set of arms and the effectiveness of separating exploration from exploitation." — [arXiv §1.4, §4](https://arxiv.org/abs/0812.3465)
  - Relation (Overlap: High, conceptual): the WITS exploitation bid is a smooth interior function of the posterior and the action is continuous. Acting on a slightly wrong estimate therefore costs only second order, which is exactly the regime where phased exploration is rate-optimal. Note that PEGE is cyclic (repeated phases), not a one-shot ETC.
- **Feit, E. M. & Berman, R. (2019). "Test & Roll: Profit-maximizing A/B tests." Marketing Science 38(6):1038–1058. arXiv:1811.00457.** — [arXiv](https://arxiv.org/abs/1811.00457); [EconPapers](https://econpapers.repec.org/RePEc:inm:ormksc:v:38:y:2019:i:6:p:1038-1058)
  - Model: a Bayesian A/B test on a finite population of size N. Test n1 and n2 users, roll the winner out to everyone else, and choose the sample sizes to trade the opportunity cost of testing against the loss from deploying the wrong treatment. — [abstract](https://arxiv.org/abs/1811.00457)
  - Results:
    - Profit-maximizing sample sizes are substantially smaller than hypothesis-testing sample sizes.
    - "A test & roll with the profit-maximizing sample size achieves nearly the same level of regret as the popular Thompson sampling solution"; both are O(√N).
    - The authors say it gives "a transparent decision point and reduced operational complexity without significant loss of profit."
    — [abstract via search](https://arxiv.org/abs/1811.00457)
  - Relation (Overlap: High): the marketing/advertising analogue of WITS' ex-ante τ chosen by a planner, with direct support that ex-ante ETC loses little against Thompson sampling.
- **Besbes, O. & Zeevi, A. (2009). "Dynamic pricing without knowing the demand function: risk bounds and near-optimal algorithms." Operations Research 57(6):1407–1420.** — [Wang, Deng & Ye refs](https://arxiv.org/abs/1101.4681); [Tehrani et al. refs](https://arxiv.org/abs/1206.5345)
  - Wang et al. characterize these as algorithms "with separated learning and doing phases, in which a grid of prices are tested and then the optimal one is used for pricing." Their best-known relative regret was O*(n^{-1/4}) nonparametric and O*(n^{-1/3}) parametric. Experimentation happens only in the learning phase "except the parametric case with a single parameter." — [Wang, Deng & Ye](https://arxiv.org/abs/1101.4681)
  - (Overlap: High as the operations-management "learn-then-earn under finite inventory" benchmark; I did not read the primary paper.)
- **Wang, Z., Deng, S. & Ye, Y. (2014). "Close the gaps: a learning-while-doing algorithm for single-product revenue management problems."** arXiv:1101.4681 (arXiv title: "...for a Class of Single-Product Revenue Management Problems"). The journal version, Operations Research 62(2):318–331, is unverified in this session. — [arXiv](https://arxiv.org/abs/1101.4681)
  - Model: one product, limited inventory x, a finite selling season T, Poisson demand with unknown rate λ(p) (nonparametric), posted prices; regret is relative to the full-information optimum as the market size n grows. — [arXiv](https://arxiv.org/abs/1101.4681)
  - Results:
    - A shrinking-price-interval "learning-while-doing" algorithm achieves relative regret O*(n^{-1/2}). This matches a lower bound built on an "uninformative" price at which all demand curves cross.
    - It improves on Besbes–Zeevi's n^{-1/4} and n^{-1/3} rates.
    - Quotes: "firms would be better off to perform dynamic learning and action concurrently rather than sequentially"; "we should not separate price experimentation from exploitation."
    — [arXiv §1, §6](https://arxiv.org/abs/1101.4681)
  - Also: once the optimal deterministic price is known, posting it for the whole season is already asymptotically optimal, with O(n^{-1/2}) regret (Lemma 1, from Gallego & van Ryzin 1994). — [arXiv §4.1](https://arxiv.org/abs/1101.4681)
  - Relation (Overlap: High): the strongest "against separation" result in a budget- or inventory-constrained setting. Finite inventory and a finite season are the operations-management analogue of a finite ad budget and horizon. Nuance: the gain comes from learning a continuum, multi-parameter demand curve, whereas WITS has a known two-point parametric family.

### Inferences
- In GLK's taxonomy WITS is the known-gap case (fully specified two hypotheses). There, tuned fixed-design ETC is rate-optimal (log T) and loses only constants, 4 versus 1 versus 1/2. ETC is therefore constant-suboptimal asymptotically, not rate-suboptimal. Inside the paper's finite budget window, transients and constants matter more than asymptotic rates (L&S Experiment 7.1).
- Two upgrades would answer the reviewer cheaply and keep the agent architecture:
  - make τ a stopping time on the win count or log-likelihood ratio (SPRT-ETC), which is still a hand-off of a one-dimensional sufficient statistic;
  - add a short audit or re-probe phase (DETC).
- The concurrency gains in Wang–Deng–Ye come from repeatedly shrinking uncertainty over a continuum of demand curves. With two known hypotheses, all uncertainty sits in one log-likelihood ratio and bounded regret is possible (Q6), so the expected benefit of concurrency is smaller, though not zero.
- The Wang–Deng–Ye / Gallego–van Ryzin lemma supports WITS' constant budget-paced exploitation bid: once the state is known, a static fluid-optimal action is asymptotically optimal.

### Gaps
- Garivier, Ménard & Stoltz (2019), "Explore first, exploit next: the true shape of regret in bandit problems," Mathematics of Operations Research 44(2):377–399: venue verified through the [L&S bibliography](https://tor-lattimore.com/downloads/book/book.pdf), content not read.
- Bubeck, Perchet & Rigollet (2013), "Bounded regret in stochastic multi-armed bandits," COLT 2013, pp. 122–134: verified in the [GLK refs](https://arxiv.org/abs/1605.08988), content not read in this session.
- The exact Anscombe (1963) citation, the Besbes–Zeevi primary text and the Wang–Deng–Ye journal details are unverified.
- GLK's constants are derived for Gaussian rewards; I found no analysis of ETC for Bernoulli wins in first-price auctions with budget pacing and a binary competition state.

---

## Q3. Limited adaptivity: batched bandits, switching constraints and costs, limited price changes — evidence that a few phases lose little

### Takeaway
Rate theory consistently shows that a handful of phases is enough:
- about log₂ log T batches or K·log log T switches give minimax √T regret;
- O(log T) batches give problem-dependent log T regret;
- O(1) rounds suffice for exact asymptotic optimality with DETC;
- with a known finite set of demand models, m price changes give log^(m) T regret.

Exactly two phases is the worst non-trivial case only when the gap is unknown (T^{2/3}), or in unstructured bandits where one switch cannot even reach sublinear regret. WITS avoids both because its hypotheses are known and every bid is informative about a single scalar θ.

### Cited Findings
- **Perchet, V., Rigollet, P., Chassang, S. & Snowberg, E. (2016). "Batched bandit problems." Annals of Statistics 44(2):660–681. DOI 10.1214/15-AOS1381. arXiv:1505.00369.** — [arXiv](https://arxiv.org/abs/1505.00369)
  - Model: two-armed subgaussian bandit, horizon T, M batches on a grid. Decisions within a batch use only data from earlier batches. The motivation is clinical trials, and the authors note internet advertising also forces batching. — [arXiv §1–2](https://arxiv.org/abs/1505.00369)
  - Results:
    - The generic ETC policy tests after each batch, commits if one arm dominates, and "goes for broke" in the final batch.
    - Geometric grid: R ≲ (T/log T)^{1/M}·log(TΔ²)/Δ, which is the optimal adaptive rate when M = Θ(log T).
    - Minimax grid: sup R ≲ T^{1/(2−2^{1−M})} up to log factors. M = 2 gives T^{2/3}, M = 3 gives T^{4/7}, M = 4 gives T^{8/15} and M = 5 gives T^{16/31}. √T needs only ⌊log₂ log T⌋ batches.
    - Matching lower bounds: sup R ≳ T^{1/(2−2^{1−M})} and sup ΔR ≳ T^{1/M}.
    - O(log log T) switches suffice for √T.
    - In simulations the minimax grid with 5 batches can beat UCB2, which uses about 50 batches.
    — [arXiv §4–6](https://arxiv.org/abs/1505.00369)
  - History: Somerville (1954) and Maurice (1957) showed two-batch ETC has regret of order T^{2/3}. Colton (1963, 1965) took a Bayesian view; "Typically, this work claims the size of the first batch should be of order √T." — [arXiv §2.4](https://arxiv.org/abs/1505.00369)
  - Relation (Overlap: High): WITS is an M = 2 policy. Proposition 1 bounds regret by 9Δ·t_m(Δ,T) plus a failure term. If the first grid point can be placed at the detection time τ(Δ) ≤ (256/Δ²)·log(TΔ²/128), which is possible when Δ is known, two batches already deliver the log T rate (inference).
- **Gao, Z., Han, Y., Ren, Z. & Zhou, Z. (2019). "Batched multi-armed bandits problem." NeurIPS 2019 (pp. 503–513 per the Simchi-Levi & Xu refs). arXiv:1904.01763.** — [arXiv](https://arxiv.org/abs/1904.01763)
  - Results (policy: BaSE, batched successive elimination):
    - Minimax regret: polylog · √K · T^{1/(2−2^{1−M})}.
    - Problem-dependent regret: polylog · K·T^{1/M}/min Δ.
    - M = O(log log T) batches suffice for minimax-optimal regret and M = O(log T) for problem-dependent-optimal regret.
    - The lower bounds for static grids match. For adaptive grids they lose only an M^{-2} factor, so "its performance is essentially no better than that of the best static grid."
    - Necessary: Ω(log log T) batches for minimax and Ω(log T/log log T) for problem-dependent optimality.
    - Empirically, about M = 4 batches approach the fully sequential UCB1.
    — [arXiv](https://arxiv.org/abs/1904.01763)
  - (Overlap: Medium)
- **Esfandiari, Karbasi, Mehrabian & Mirrokni (2019). "Batched multi-armed bandits with optimal regret." arXiv:1910.04959; Agarwal, Agarwal, Assadi & Khanna (2017). "Learning with limited rounds of adaptivity: coin tossing, multi-armed bandits, and ranking from pairwise comparisons." COLT 2017, pp. 39–75** (pure exploration in rounds). — [Gao et al. refs](https://arxiv.org/abs/1904.01763). (Overlap: Low)
- **Simchi-Levi, D. & Xu, Y. (2023). "Phase transitions in bandits with switching constraints." Management Science 69(12):7182–7201. DOI 10.1287/mnsc.2023.4755. arXiv:1905.10825.** Conference version: "Phase transitions and cyclic phenomena in bandits with switching constraints," NeurIPS 2019, pp. 7521–7530. — [arXiv](https://arxiv.org/abs/1905.10825); journal details from the [Guha 2026 refs](https://arxiv.org/abs/2610.24156)
  - Model: K-armed stochastic bandit with a total switching budget S, under unit or general switching costs. — [arXiv](https://arxiv.org/abs/1905.10825)
  - Results:
    - For fixed K, R*_S(T) = Θ̃(T^{1/(2−2^{−⌊(S−1)/(K−1)⌋})}).
    - Phases: S in [0, K) gives T; [K, 2K−1) gives T^{2/3}; [2K−1, 3K−2) gives T^{4/7}; [3K−2, 4K−3) gives T^{8/15}; and so on.
    - Θ(K log log T) switches are necessary and sufficient for Õ(√KT), and Ω(K) switches are necessary for sublinear regret.
    - The switching-constrained problem is a strict relaxation of batched bandits, and the batched lower bounds of Perchet et al. and Gao et al. are corollaries.
    - "Phase transitions are more relevant to practice when S belongs to the first 4 or 5 phases."
    — [arXiv §3](https://arxiv.org/abs/1905.10825)
  - Relation (Overlap: Medium): in *unstructured* bandits a single switch gives linear regret (S < K). The WITS one-switch protocol works only because of structure: one scalar θ, known hypotheses, and a dedicated probing action.
- **Cesa-Bianchi, N., Dekel, O. & Shamir, O. (2013). "Online learning with switching costs and other adaptive adversaries." NeurIPS 26, pp. 1160–1168. arXiv:1302.4387.** — [arXiv](https://arxiv.org/abs/1302.4387)
  - Results: with an adversary and bandit feedback, switching costs make regret Θ̃(T^{2/3}), versus Θ(√T) with full information. With stochastic i.i.d. losses, O(√T·log log log T) regret is achievable with O(log log T) switches, using stages of length T^{1−2^{−s}}. — [arXiv](https://arxiv.org/abs/1302.4387)
  - Related: Dekel, Ding, Koren & Peres (2014), "Bandits with switching costs: T^{2/3} regret," STOC 2014, pp. 459–467. — [Simchi-Levi & Xu refs](https://arxiv.org/abs/1905.10825). (Overlap: Low)
- **Cheung, W. C., Simchi-Levi, D. & Wang, H. (2017). "Technical Note—Dynamic pricing and demand learning with limited price experimentation." Operations Research 65(6):1722–1731. DOI 10.1287/opre.2017.1629.** — [EconPapers](https://econpapers.repec.org/RePEc:inm:oropre:v:65:y:2017:i:6:p:1722-1731); [MIT DSpace](https://dspace.mit.edu/handle/1721.1/119156)
  - Model: the demand function is unknown but belongs to a known finite set, and the seller may change price at most m times over T periods. Regret is worst-case, against a clairvoyant who knows demand.
  - Result: a policy with regret O(log^(m) T), the m-fold iterated logarithm. It was implemented at Groupon with significant impact on revenue and bookings. — [abstract summary](https://dspace.mit.edu/handle/1721.1/119156)
  - Relation (Overlap: High): matches the WITS structure (finite hypothesis set, very few action changes). In finite-hypothesis problems a handful of switches captures almost all the value of full adaptivity. I only read the abstract.
- **Farias, V. F. & Madan, R. (2011). "The irrevocable multiarmed bandit problem." Operations Research 59(2):383–399. DOI 10.1287/opre.1100.0891** (arXiv 0806.4133, "Irrevocable multi-armed bandit policies"). — [INFORMS](https://pubsonline.informs.org/doi/abs/10.1287/opre.1100.0891); [EconPapers](https://econpapers.repec.org/RePEc:inm:oropre:v:59:y:2011:i:2:p:383-399)
  - Model: several arms played at once, and an arm that has been discarded can never be pulled again.
  - Results: standard heuristics adapted to this constraint perform poorly. A new "packing heuristic" performs well even against unrestricted heuristics. The "price of irrevocability" is uniformly bounded for a broad class of problems, and the method is computationally cheaper than Gittins-based methods. — [abstract summary](https://pubsonline.informs.org/doi/abs/10.1287/opre.1100.0891)
  - Relation (Overlap: Medium): commitment without recall costs little in multi-play Bayesian bandits, which is conceptually close to a planner running several committing teams.
- **Classical few-stage Bayesian designs:** Colton (1963), "A model for selecting one of two medical treatments," JASA 58(302):388–400; Hardwick & Stout (2002), "Optimal few-stage designs," J. Stat. Plann. Inference 104:121–145; Cheng (1996), "Multistage bandit problems," J. Stat. Plann. Inference 53:153–170. — [Perchet et al. refs](https://arxiv.org/abs/1505.00369). (Overlap: Medium; the classic Bayesian "test-then-treat" lineage that WITS belongs to.)

### Inferences
- Limited-adaptivity theory says few phases lose little in rate, but two phases are the worst non-trivial case when the gap is unknown. WITS escapes the T^{2/3} trap because its hypotheses are known, which makes it a "known-Δ" problem where a single well-placed commitment point gives log T.
- DETC and Cheung et al. both suggest that allowing one or two more bid changes (a re-pacing or audit step) would capture most of the remaining gap to fully sequential policies.
- The probing-agent → exploitation-agent hand-off is a limited-adaptivity architecture. For LLM sub-agent teams, where communication or update rounds are costly, these results justify designs with few hand-offs.

### Gaps
- I found no batched or limited-adaptivity result for budgets where spending happens only on wins.
- Cheung et al.'s exact assumptions and constants were not read; only the abstract was available.

---

## Q4. Pure exploration with a budget, then exploitation: best-arm identification, simple regret, and budgeted learning for future utilization

### Takeaway
When information gathered now is used later, allocation should follow pure-exploration logic rather than regret-minimization logic:
- the smaller an allocation's cumulative regret, the larger its simple regret (Bubeck, Munos & Stoltz);
- for fully specified alternatives, sequential stopping saves about 4× in samples, but with unknown means a well-designed fixed budget is about as good (Kaufmann, Cappé & Garivier).

Budgeted learning for future utilization (Madani et al.; Guha & Munagala; Guha 2026) is the closest formalization of a planner allocating a learning budget across many independent Bayesian units and then exploiting, with LP and Lagrangian approximation guarantees of 1/3, 4/27, 0.43 and (1 − 1/e). Unlike WITS, these models ignore payoffs earned during exploration and end with a single selection among units.

### Cited Findings
- **Bubeck, S., Munos, R. & Stoltz, G. (2009/2011). "Pure exploration in multi-armed bandits problems." ALT 2009, LNCS 5809, pp. 23–37.** Journal version: "Pure exploration in finitely-armed and continuous-armed bandits," Theoretical Computer Science 412(19):1832–1852 (2011). arXiv:0802.2655. — [arXiv](https://arxiv.org/abs/0802.2655); venues from the [Guha refs](https://arxiv.org/abs/2610.24156) and [Lizzeri refs](https://arxiv.org/abs/2404.19116)
  - Model: K arms, an allocation strategy plus a recommendation J_n, judged by simple regret r_n = μ* − μ_{J_n}.
    - "The exploration phase and the evaluation phase are separated."
    - The criterion is meant for situations "when the cost of pulling an arm is expressed in terms of resources rather than rewards."
    - Example: "for cosmetic products, there exists a test phase separated from the commercialization phase."
    — [arXiv §1](https://arxiv.org/abs/0802.2655)
  - Results:
    - Theorem 1: if E R_n ≤ C·ε(n) on all Bernoulli instances, then E r_n ≥ (Δ/2)·e^{−D·ε(n)}, for K ≥ 3 Bernoulli arms with distinct parameters, up to a reordering of the arms. In words, "the smaller the cumulative regret, the larger the simple regret."
    - Allocation with UCB therefore gives only polynomially decaying simple regret. Uniform allocation gives exponential decay for large n, but for moderate n, UCB(α) with a most-played-arm recommendation can do better.
    - The distribution-free rate for simple regret is 1/√n.
    — [arXiv §3–4](https://arxiv.org/abs/0802.2655)
  - Relation (Overlap: High): the formal reason a probing agent should not be run as a regret-minimizing bandit. When the probe exists to inform future exploitation, a regret-optimal allocation collects too little information.
- **Audibert, J.-Y., Bubeck, S. & Munos, R. (2010). "Best arm identification in multi-armed bandits." COLT 2010, pp. 41–53.** — [Guha refs](https://arxiv.org/abs/2610.24156)
  - Fixed-budget best-arm identification. The lower bound is p_t ≥ exp(−t/(C_α·H2(ν))), with H2 = max_i i/(μ[1] − μ[i])², for Bernoulli arms with means in [α, 1−α]. Their UCB-E algorithm requires knowing the complexity H. — [as summarized in Kaufmann et al. 2016](https://arxiv.org/abs/1407.4443)
  - (Overlap: Medium)
- **Kaufmann, E., Cappé, O. & Garivier, A. (2016). "On the complexity of best-arm identification in multi-armed bandit models." Journal of Machine Learning Research, published 1/2016, pp. 1–42.** The arXiv header prints "16 (2016)" while the standard listing is volume 17. arXiv:1407.4443. — [arXiv](https://arxiv.org/abs/1407.4443)
  - Results:
    - Defines complexities κC (fixed confidence) and κB (fixed budget).
    - Two-armed Gaussian with known variances: κC = κB = 2(σ1+σ2)²/(μ1−μ2)². For a fixed budget, the static allocation n1/(n1+n2) = σ1/(σ1+σ2) is optimal.
    - Two-armed Bernoulli: κC > κB. Uniform sampling is near-optimal in two-armed cases.
    - Fully specified alternatives (means known up to permutation): an SPRT needs E[τ] ≃ 2σ²/(μ1−μ2)²·log(1/δ), while the batch likelihood-ratio test needs a sample size of order 8σ²/(μ1−μ2)²·log(1/δ). "We will show below that this conclusion is not valid anymore when the values of μ1 and μ2 are not assumed to be known."
    — [arXiv §1, §4–5](https://arxiv.org/abs/1407.4443)
  - Relation (Overlap: High): θL and θH are known in WITS, so the alternatives are fully specified and stopping the probe sequentially is worth up to about 4× in samples. If the competition levels themselves were uncertain, a well-chosen fixed probing budget would be asymptotically as efficient as a sequential one.
- **Garivier, A. & Kaufmann, E. (2016). "Optimal best arm identification with fixed confidence." COLT 2016, PMLR 49:998–1027** (arXiv:1602.04589 from the assignment, not re-checked). — [L&S bibliography](https://tor-lattimore.com/downloads/book/book.pdf)
  - Track-and-Stop is asymptotically optimal for one-parameter exponential families, via a characteristic time T*(μ) and optimal weights w*(μ). — [description in GLK §6](https://arxiv.org/abs/1605.08988)
  - (Overlap: Medium)
- **Madani, O., Lizotte, D. J. & Greiner, R. (2004a). "Active model selection." UAI 2004, pp. 357–365; (2004b). "The budgeted multi-armed bandit problem." COLT 2004 (open problems), LNCS 3120, pp. 643–645, DOI 10.1007/978-3-540-27819-1_46.** Also Lizotte, Madani & Greiner (2003), "Budgeted learning of naive-Bayes classifiers," UAI 2003, pp. 378–385. — [Guha refs](https://arxiv.org/abs/2610.24156)
  - Madani et al. show the budgeted problem is NP-hard when plays of different arms have different costs, and leave the unit-cost case open. — [Guha 2026](https://arxiv.org/abs/2610.24156)
  - (Overlap: Medium)
- **Guha, S. & Munagala, K. (2007). "Approximation algorithms for budgeted learning problems." STOC 2007, pp. 104–113. DOI 10.1145/1250790.1250807.** Related work by the same authors: (2008) "Sequential design of experiments via linear programming," arXiv:0805.2630; (2009) "Multi-armed bandits with metric switching costs," ICALP 2009, LNCS 5556, pp. 496–507; (2013) "Approximation algorithms for Bayesian multi-armed bandit problems," arXiv:1306.3525. — [Guha 2026 refs](https://arxiv.org/abs/2610.24156)
  - Results:
    - These gave the first constant-factor approximations, through LP relaxations. The consolidated 2013 treatment (§7) gets a 1/3 approximation by balancing a Lagrangian bound.
    - Ma (2018), Mathematics of Operations Research 43(3):789–812, gives an LP-based 4/27 approximation for a more general Markovian model.
    - Goel, Khanna & Null (2009), "The ratio index for budgeted learning, with applications," SODA 2009, pp. 18–27, proposed a ratio index; "Its arXiv version was withdrawn in 2016 after the authors reported a bug."
    — [Guha 2026](https://arxiv.org/abs/2610.24156)
  - Relation (Overlap: High for an n-team extension): these papers study a planner allocating a learning budget across many independent Bayesian units before exploitation, and their LP/Lagrangian decompositions are the established approximation toolkit for it.
- **Guha, S. (2026). "Budgeted Bayesian Bandits for Future Utilization." arXiv:2610.24156v1 [cs.LG], 16 Oct 2026.** — [arXiv](https://arxiv.org/abs/2610.24156)
  - Model: n independent rested Bayesian arms with known priors and a hard exploration budget T; "exploration has a hard budget and precedes exploitation." The objective is V_T(π) = E[max_i E[θi | F_T]], and "rewards obtained during exploration do not contribute to this objective." — [arXiv §1](https://arxiv.org/abs/2610.24156)
  - Results:
    - The analyses of Guha–Munagala's 1/3 algorithm and Ma's 4/27 algorithm are tight, even when their relaxations are asymptotically exact.
    - A new efficient algorithm achieves (1 − e^{−2})/2 ≈ 0.43.
    - For bounded exchangeable observations in a "non-vanishing regime", a guarantee approaching 1 − 1/e ≈ 0.63, which is asymptotically tight against natural LP relaxations (integrality gap 1/(1 − 1/e)).
    - "Certificates for stopping sequential model evaluation", with variants for switching, setup and movement budgets.
    — [arXiv abstract, §5](https://arxiv.org/abs/2610.24156)
  - Relation (Overlap: High–Medium): the closest recent formalization of "explore with a budget, then exploit" across many units. It differs from WITS in three ways:
    - payoffs earned during probing are ignored;
    - it ends with a single terminal selection among units, whereas each WITS team exploits its own posterior;
    - there is no per-unit budget split.
- **Weitzman, M. L. (1979). "Optimal search for the best alternative." Econometrica 47(3):641–654.** — [Guha refs](https://arxiv.org/abs/2610.24156)
  - Pandora's box: "When one inspection resolves an alternative and inspections are priced, Pandora's box optimizes expected selected value minus inspection costs." — [Guha 2026](https://arxiv.org/abs/2610.24156)
  - (Overlap: Medium; analogous to a planner deciding which teams get to "inspect", i.e. learn.)
- **Chick, S. E. & Gans, N. (2009). "Economic analysis of simulation selection problems." Management Science 55(3):421–437.** — [Gao et al. refs](https://arxiv.org/abs/1904.01763). Content not read. (Overlap: Medium by title: the economics of selection under sampling costs.)

### Inferences
- In WITS the probe also earns payoff (wins at b^I), so the probing objective mixes simple regret (information for exploitation) with cumulative regret (payoff during the probe). The Bubeck–Munos–Stoltz trade-off implies the probing action should be chosen for information, while τ trades probing opportunity cost against exploitation gain, which is exactly the test & roll logic.
- Budgeted-learning approximation results give an immediate theoretical home for n-team and multi-sub-agent token budgeting. The template is a planner LP over per-unit local policies with a Lagrange price on the shared budget, which comes with constant-factor guarantees.

### Gaps
- I found no paper that combines all three WITS features: a per-unit budget split, payoff during exploration, and unit-specific exploitation with no terminal selection. The combination appears to be new to WITS.
- Ma (2018) and the Successive Rejects details in Audibert et al. were not read directly.

---

## Q5. Optimal stopping and sequential testing / design of experiments: when should the learning phase end?

### Takeaway
The WITS probe is a test between two simple hypotheses (θL vs θH). Classical theory is unambiguous on two points:
- the SPRT minimizes expected sample size for given error rates (Wald–Wolfowitz), and sequential tests use about 4× fewer samples than fixed-sample tests (Wald; Kaufmann et al.; GLK);
- Bayes-optimal stopping of a two-action problem with sampling costs is a backward-induction stopping rule (Arrow–Blackwell–Girshick), and Chernoff's sequential design couples choosing the most informative experiment with sequential stopping.

So the paper's information-maximizing probe is well founded, while the fixed τ is a choice made for tractability. That cost should be acknowledged, or the design made sequential while keeping the same one-dimensional hand-off.

### Cited Findings
- **Wald, A. (1945). "Sequential tests of statistical hypotheses." Annals of Mathematical Statistics 16(2):117–186. DOI 10.1214/aoms/1177731118.** — [Guha refs](https://arxiv.org/abs/2610.24156); [GLK refs](https://arxiv.org/abs/1605.08988)
  - Worked comparison for two simple hypotheses (paired differences N(±Δ, 2)): a batch test needs n ~ (4/Δ²)·log(1/δ) to keep both errors below δ, whereas an SPRT does the same with E[N] ~ log(1/δ)/Δ². — [GLK §3](https://arxiv.org/abs/1605.08988)
- **Wald, A. & Wolfowitz, J. (1948). "Optimum character of the sequential probability ratio test." Annals of Mathematical Statistics 19(3):326–339. DOI 10.1214/aoms/1177730197.** — [Project Euclid](https://www.projecteuclid.org/euclid.aoms/1177730197)
  - Result: among all tests whose error probabilities do not exceed those of a given SPRT, the SPRT has the smallest expected number of observations under both hypotheses. — [Encyclopedia of Mathematics](https://encyclopediaofmath.org/wiki/Sequential_probability_ratio_test)
  - Caveat: the optimality holds under restrictive conditions, mainly that sampling proceeds one observation at a time. — [search summary citing Morgan & Cressie 1997](https://www.projecteuclid.org/euclid.aoms/1177730197)
  - Relation (Overlap: High): the WITS probe is a two-simple-hypothesis test, and fixing τ ex ante is the batch test, so the classical sequential gain applies.
- **Arrow, K. J., Blackwell, D. & Girshick, M. A. (1949). "Bayes and minimax solutions of sequential decision problems." Econometrica 17(3/4):213–244. DOI 10.2307/1905525.** Usually cited in this author order; the search summary of the Econometric Society page listed Blackwell first, so the order there is unverified. — [Econometric Society page](https://econometricsociety.org/publications/econometrica/1949/07/01/bayes-and-minimax-solutions-sequential-decision-problems)
  - Model: sequential choice among several actions; at each stage one can stop and act or continue sampling, with costs for wrong actions and for sampling.
  - Results: a general characterization of the Bayes solution, built from truncated procedures and the best sequential procedure, with explicit solutions for two actions, random sampling and linear costs. — [abstract / table-of-contents summary](https://econometricsociety.org/publications/econometrica/1949/07/01/bayes-and-minimax-solutions-sequential-decision-problems)
  - Relation (Overlap: High, conceptual): the Bayes-optimal way to stop a two-action learning phase with linear sampling cost, and the principled alternative to a fixed τ.
- **Chernoff, H. (1959). "Sequential design of experiments." Annals of Mathematical Statistics 30(3):755–770** (pages unverified). **DOI 10.1214/aoms/1177706205.** — [listing](https://www.bohrium.com/paper-details/sequential-design-of-experiments/811949635357638660-19453)
  - Sequential hypothesis testing where the experimenter also chooses which experiment to run. Chernoff's "procedure A" is asymptotically optimal for finitely many states as the cost per observation c → 0, with risk of order −c·log c, and its stopping rules rely on large-deviation methods. Standard descriptions, not re-read here, say procedure A selects the experiment that maximizes Kullback–Leibler discrimination between the current estimate and its nearest alternative. — [Albert 1961 follow-up](https://projecteuclid.org/journals/annals-of-mathematical-statistics/volume-32/issue-3/The-Sequential-Design-of-Experiments-for-Infinitely-Many-States-of/10.1214/aoms/1177704973.full); [NASA report](https://ntrs.nasa.gov/api/citations/19690013602/downloads/19690013602.pdf)
  - Relation (Overlap: High): WITS' "information-maximizing bid" is a Chernoff-style choice of experiment. Chernoff, however, makes the experiment depend on the current estimate and stops sequentially.
- **Cheng, C. & Huan, X. (2025; v3 dated 13 Jun 2026). "Optimal stopping for sequential Bayesian experimental design." arXiv:2509.21734 [stat.ME].** — [arXiv](https://arxiv.org/abs/2509.21734)
  - Model: sequential Bayesian experimental design (BED) is usually a fixed-horizon policy problem. Here design and stopping are treated as coupled decisions in a finite-horizon problem. — [arXiv abstract](https://arxiv.org/abs/2509.21734)
  - Results:
    - Theorem 3.1: for any fixed design policy, the optimal stopping rule terminates when the immediate terminal reward is no smaller than the expected continuation value.
    - Common threshold rules (posterior variance, information gain, remaining budget) are "myopic".
    - A policy-gradient method learns continuous design policies with value-based stopping. A curriculum that moves from forced continuation to adaptive stopping avoids early-stopping local optima.
    - The largest gains appear where there is strong sequential dependence.
    — [arXiv](https://arxiv.org/abs/2509.21734)
  - Relation (Overlap: Medium–High): a modern computational recipe for replacing a fixed τ with value-based stopping while keeping a design policy for the probing bid.
- **Other stopping rules for ranking and selection and Bayesian optimization:**
  - Frazier, P. & Powell, W. B. (2008), "The knowledge-gradient stopping rule for ranking and selection," Winter Simulation Conference 2008, pp. 305–312, DOI 10.1109/WSC.2008.4736082, which designs sampling and stopping jointly "with a myopic measurement-cost objective";
  - Eckman & Henderson (2022), "Posterior-based stopping rules for Bayesian ranking-and-selection procedures," INFORMS J. Computing 34(3):1711–1728;
  - Xie, Cai, Terenin, Frazier & Scully (2026), "Cost-aware stopping for Bayesian optimization," ICML 2026, arXiv:2507.12453.

  — [Guha 2026 refs and related work](https://arxiv.org/abs/2610.24156). (Overlap: Medium)
- **Peskir & Shiryaev (2006). *Optimal Stopping and Free-Boundary Problems*. Springer; Shiryaev (2008). *Optimal Stopping Rules*. Springer** — [Cheng & Huan refs](https://arxiv.org/abs/2509.21734). L&S: "The classic text on optimal stopping is by Robbins et al. [1971]." — [L&S §35.7](https://tor-lattimore.com/downloads/book/book.pdf). (Overlap: Low)
- **Lai, T. L., Robbins, H. & Siegmund, D. (1983). "Sequential design of comparative clinical trials."** In *Recent Advances in Statistics* (Chernoff Festschrift), Academic Press, pp. 51–68. GLK note that "a similar strategy [to BAI-ETC] was proposed and analysed by Lai et al. [1983], but in the continuous time framework and with asymptotic analysis only." — [GLK](https://arxiv.org/abs/1605.08988). (Overlap: Medium)
- **Che, Y.-K. & Mierendorff, K. (2019). "Optimal dynamic allocation of attention." American Economic Review 109(8):2993–3029**, an "environment à la Wald". — [Lizzeri et al. refs and literature review](https://arxiv.org/abs/2404.19116). Content not re-read. (Overlap: Low–Medium)

### Inferences
- With binary θ, the posterior is a monotone function of the log-likelihood ratio, and after n probes at a fixed b^I that ratio is affine in the win count w. An SPRT is therefore "stop when w leaves [a_n, b_n]". The probing agent can run it and hand off (w, n) exactly as now, so the modular architecture survives.
- Technical remark for the authors (my own algebra, not from a cited source):
  - b^I = √(θL·θH) maximizes the win-probability gap q_θL(b) − q_θH(b) = b(θH − θL)/((b + θL)(b + θH)).
  - Chernoff-style designs, including the "exploration price" of Tehrani et al. (Q6), instead maximize a divergence between Bernoulli(q_θL(b)) and Bernoulli(q_θH(b)), which is generally maximized at a different bid.
  - With a budget, the relevant measure is information per unit of expected *spend* (b·q_θ(b)), not per period. Reviewers may probe this.
- A Wald or ABG Bayes stopping rule makes τ, and therefore probing spend, random. That complicates the planner's ex-ante split and gives a legitimate modeling reason to keep τ deterministic. The paper should still acknowledge the efficiency cost, which for simple hypotheses is up to about 4× in learning samples (Wald; Kaufmann et al.) and translates into the 4 versus 1 regret constants of GLK.

### Gaps
- DeGroot (1970), *Optimal Statistical Decisions* (McGraw-Hill), and Wald (1947), *Sequential Analysis* (Wiley), were not verified in this session. Lizzeri et al.'s list does contain Wald (1947), "Foundations of a general theory of sequential decision functions," Econometrica, pp. 279–313.
- Chernoff (1959)'s page range is unverified.
- Not verified: Bradt, Johnson & Karlin (1956) on the finite-horizon one-armed bandit as a stopping problem (the L&S book covers the structure), and the economics papers on the optimal length or intensity of experimentation (Moscarini & Smith 2001; Fudenberg, Strack & Strzalecki 2018).

---

## Q6. When does greedy/myopic learning suffice, and when does it fail?

### Takeaway
Greedy or myopic learning fails through "confounding" (uninformative) actions or decoys, and succeeds when every relevant action separates the hypotheses:
- in binary-prior pricing, the documented failure of the myopic Bayesian policy is getting stuck at an uninformative price, and policies that stay discriminative have bounded regret;
- with finitely many demand models and informative optimal prices, a likelihood-ratio policy has bounded regret;
- in finite structured bandits, greedy succeeds if and only if the instance is self-identifiable.

In WITS' model the two win curves never cross at a positive bid, so a myopic Bayesian bidder would learn while exploiting. This is the most serious argument a reviewer can make against a separate probing phase. Two other lines of work justify spending on a dedicated, never-exploitation-optimal probing bid: UCB and TS can be arbitrarily suboptimal when the informative action is not a candidate optimum (IDS; "End of Optimism"). ETC's advantage in WITS is therefore learning speed per budget and modularity, not identifiability.

### Cited Findings
- **Harrison, J. M., Keskin, N. B. & Zeevi, A. (2012). "Bayesian dynamic pricing policies: Learning and earning under a binary prior distribution." Management Science 58(3):570–586. DOI 10.1287/mnsc.1110.1426.** — [INFORMS](https://pubsonline.informs.org/doi/fpi/10.1287/mnsc.1110.1426); [EconPapers](https://econpapers.repec.org/RePEc:inm:ormnsc:v:58:y:2012:i:3:p:570-586)
  - Model: a seller offers prices one at a time and observes success or failure. One of two known demand models applies, and the analysis focuses on the myopic Bayesian policy (MBP). — [abstract via search](https://econpapers.repec.org/RePEc:inm:ormnsc:v:58:y:2012:i:3:p:570-586)
  - Results:
    - "Because learning is passive under the MBP ... it can lead to incomplete learning and poor profit performance."
    - The belief converges almost surely, but not necessarily to 0 or 1. The MBP can get stuck at an "uninformative price", where both demand models coincide.
    - δ-discriminative policies (|ρ0(p_t) − ρ1(p_t)| > δ for every t) drive the belief to 0 or 1 exponentially fast.
    - A constrained MBP (CMBP) has an expected gap to the clairvoyant that is bounded by a constant, under one additional assumption.
    — [abstract](https://pubsonline.informs.org/doi/fpi/10.1287/mnsc.1110.1426); [Tehrani et al. §III summary](https://arxiv.org/abs/1206.5345)
  - Relation (Overlap: High, a structural twin of WITS): binary unknown state, binary outcomes and a posterior-based myopic action. In WITS' q_θ(b) = b/(b + θ), q_θL(b) > q_θH(b) for every b > 0, so no positive bid is uninformative, and any bid bounded away from 0 is δ-discriminative (inference). A myopic Bayesian bidder would therefore learn without dedicated probing. This is the strongest counter-argument to ETC.
- **Tehrani, P., Zhai, Y. & Zhao, Q. (2012). "Dynamic pricing under finite space demand uncertainty: a multi-armed bandit with dependent arms." arXiv:1206.5345 (v4, 27 Oct 2012).** — [arXiv](https://arxiv.org/abs/1206.5345)
  - Model: N known candidate demand curves, binary sale outcomes, no prior (non-Bayesian). The arms are the optimal prices of each candidate model, which makes the arms dependent. — [arXiv](https://arxiv.org/abs/1206.5345)
  - Results:
    - The LRT policy plays the optimal price of the currently most likely model. It achieves bounded regret provided no candidate optimal price is uninformative (ρ1(p*_k) ≠ ρ0(p*_k)), "in sharp contrast with the logarithmic growing regret in multi-armed bandit with independent arms."
    - XLRT adds an exploration price that maximizes the Chernoff distance between the two most likely models, used only while the log-likelihood ratio is close to 0. It improves regret.
    - In HKZ's own examples, LRT outperforms CMBP.
    — [arXiv](https://arxiv.org/abs/1206.5345)
  - Relation (Overlap: High): very nearly the WITS learning problem, and it points to an adaptive hybrid design with bounded regret: exploit by default and probe at the most informative bid only while uncertain.
- **Broder, J. & Rusmevichientong, P. (2012). "Dynamic pricing under a general parametric choice model." Operations Research 60(4):965–980. DOI 10.1287/opre.1120.1057.** — [EconPapers](https://econpapers.repec.org/RePEc:inm:oropre:v:60:y:2012:i:4:p:965-980)
  - Results: in general, any policy has regret Ω(√T), and the paper presents an MLE-based pricing policy; standard summaries say it attains O(√T). Under a "well-separated" condition, regret is Θ(log T) and a pure greedy MLE policy achieves O(log T). Every price is informative under that condition (Fisher information bounded away from 0). — [secondary: RL-for-economics survey](https://arxiv.org/pdf/2603.08956); [markdown-pricing paper](https://arxiv.org/pdf/2312.15286). The primary text was not accessed.
  - (Overlap: High)
- **Keskin, N. B. & Zeevi, A. (2014). "Dynamic pricing with an unknown demand model: Asymptotically optimal semi-myopic policies." Operations Research 62(5):1142–1167. DOI 10.1287/opre.2014.1294.** — [EconPapers](https://econpapers.repec.org/RePEc:inm:oropre:v:62:y:2014:i:5:p:1142-1167)
  - Results: linear demand with unknown parameters.
    - Regret is of order √T when nothing is known, and of order log T when expected demand at an incumbent price is known.
    - Greedy iterated least squares (ILS) suffers incomplete learning, but certain "semi-myopic" variants attain the minimum asymptotic loss rate.
    — [abstract summary](https://econpapers.repec.org/RePEc:inm:oropre:v:62:y:2014:i:5:p:1142-1167)
  - Follow-up: Keskin & Zeevi (2018), "On incomplete learning and certainty-equivalence control," Operations Research 66(4), on when certainty-equivalence policies avoid incomplete learning without forced exploration. — [SUFE listing](https://academicnewsletter.sufe.edu.cn/info/402675); venue taken from a secondary listing.
  - (Overlap: Medium–High)
- **den Boer, A. V. & Zwart, B. (2014). "Simultaneously learning and optimizing using controlled variance pricing." Management Science 60(3):770–783. DOI 10.1287/mnsc.2013.1788.** — [EconPapers](https://econpapers.repec.org/RePEc:inm:ormnsc:v:60:y:2014:i:3:p:770-783)
  - Results: controlled variance pricing (CVP) is certainty-equivalent pricing with a "taboo interval" around the average of past prices. The interval shrinks as data accumulate, which guarantees enough price dispersion. CVP is strongly consistent and has regret upper bounds. — [abstract fragments](https://pubsonline.informs.org/doi/fpi/10.1287/mnsc.2013.1788)
  - Without such a device, greedy or certainty-equivalent pricing can converge to a suboptimal price with positive probability. — [Bastani et al. lit review](https://arxiv.org/abs/1704.09011); [Zhou et al. 2026](https://arxiv.org/abs/2607.29375)
  - (Overlap: Medium)
- **Mersereau, A. J., Rusmevichientong, P. & Tsitsiklis, J. N. (2009). "A structured multiarmed bandit problem and the greedy policy." IEEE Transactions on Automatic Control 54(12):2787–2802.** — [Zhou et al. refs](https://arxiv.org/abs/2607.29375)
  - With one unknown scalar, arm rewards linear in it and a known prior, "the cumulative Bayes risk ... under a greedy policy admits an O(log T) upper bound, independent of the number of arms." — [description in Rusmevichientong & Tsitsiklis 2010](https://arxiv.org/abs/0812.3465)
  - (Overlap: High: a single scalar unknown, as with θ.)
- **Slivkins, A., Xu, Y. & Zuo, S. (2025). "Greedy algorithm for structured bandits: A sharp characterization of asymptotic success / failure." arXiv:2503.04010 (v3, 6 Nov 2025).** — [arXiv](https://arxiv.org/abs/2503.04010)
  - Model: bandits with a known finite reward structure, extended to contextual bandits and to decision-making with structured observations (DMSO, arbitrary feedback).
  - Results:
    - Greedy has sublinear (logarithmic) regret if and only if the instance is *self-identifiable*: fixing the mean of any suboptimal arm identifies it as suboptimal.
    - Otherwise a "decoy" exists: an alternative model whose optimal arm is suboptimal for the truth and coincides with the truth on that arm. Greedy then stays on the decoy forever with positive probability, giving linear regret.
    - Under self-identifiability, any "information-aware" algorithm succeeds, so "Greedy succeeds only if the problem is intrinsically 'easy'."
    - Greedy fails for almost all linear, Lipschitz and polynomial bandit instances.
    — [arXiv](https://arxiv.org/abs/2503.04010)
  - Relation (Overlap: High): a clean test for the reviewer's question. In WITS the model class is {θL, θH}, each model's optimal bid is positive, and the two models never coincide on a positive bid. The instance is therefore self-identifiable and myopic learning succeeds asymptotically (inference). The case for ETC must rest on finite-budget speed and design, not on exploration being necessary.
- **Bastani, H., Bayati, M. & Khosravi, K. (2021). "Mostly exploration-free algorithms for contextual bandits." Management Science, DOI 10.1287/mnsc.2020.3605.** Volume and pages 67(3):1329–1349 are the standard citation but were not confirmed here. Zhou et al.'s reference list gives a conflicting "Bastani & Bayati (2020), MS 66(4):1511–1531". I trust the INFORMS DOI record, which lists three authors. — [arXiv](https://arxiv.org/abs/1704.09011); [INFORMS](https://pubsonline.informs.org/doi/fpi/10.1287/mnsc.2020.3605)
  - Results:
    - Greedy is rate-optimal, O(log T), for two-armed linear and GLM contextual bandits under "covariate diversity", and is rate-optimal with positive probability otherwise.
    - Greedy-First tests whether greedy is learning, using a minimum-eigenvalue condition λ0·t/4, and switches to an exploration-based OLS bandit if not. It is rate-optimal without extra assumptions and stays greedy with high probability under covariate diversity.
    - Bietti et al. (2018) found greedy outperforming a wide range of bandit algorithms on more than 400 of 524 datasets.
    — [arXiv](https://arxiv.org/abs/1704.09011)
  - (Overlap: Medium: WITS has no contexts, but "Greedy-First" is an alternative to ETC: exploit, monitor learning, and explore only if it stalls.)
- **Kannan, S., Morgenstern, J., Roth, A., Waggoner, B. & Wu, Z. S. (2018). "A smoothed analysis of the greedy algorithm for the linear contextual bandit problem."** NeurIPS 2018 per the standard citation (venue unverified). Adversarially chosen contexts perturbed by noise make greedy rate-optimal "even for small perturbations." — [description in Bastani et al.](https://arxiv.org/abs/1704.09011). (Overlap: Low)
- **Zhou, K., Li, M. L. & Wang, K. (2026). "The greedy advantage in finite-horizon bandits." arXiv:2607.29375 (31 Jul 2026).** — [arXiv](https://arxiv.org/abs/2607.29375)
  - Results:
    - Regularized greedy selects the arm with the largest (S_i + α)/(N_i + β).
    - Finite-horizon regret splits into a linear absorption term, which shrinks exponentially in the regularization strength, and a transient abandonment term.
    - Calibrated versions match or beat TS, optimistic Gittins indices (OGI) and IDS.
    - In their benchmarks, generic ETC and DETC do much worse. Example (K = 2, T/K = 600, uniformly random means), mean regret: ETC 25.2, DETC 25.0, TS 6.04, IDS 4.75, horizon-aware regularized greedy 4.11, oracle 3.93.
    — [arXiv Table 1](https://arxiv.org/abs/2607.29375)
  - (Overlap: Medium: empirical evidence that untuned ETC is weak in generic finite-horizon Bernoulli bandits, though without known two-hypothesis structure.)
- **Russo, D. & Van Roy, B. (2014/2018). "Learning to optimize via information-directed sampling."** NeurIPS 27 (2014), pp. 1583–1591. The journal version (Operations Research 66(1):230–252, 2018) is the standard citation, unverified here. arXiv:1403.5556. — [arXiv](https://arxiv.org/abs/1403.5556)
  - IDS samples to minimize (expected one-period regret)² divided by the information gained about the optimal action.
  - Example 2 ("a revealing action"): action 0 is known never to be optimal, so TS and UCB never select it and their regret grows linearly in K. IDS plays it once, identifies the optimal action, and its regret is independent of K.
  - "UCB and TS restrict attention to sampling actions that have some chance of being optimal."
  - Example 1 ("a known standard"): deterministic stationary policies can lock onto an uninformative action, and for any of them some prior gives linear regret.
  - Earlier finite-parameter theory: Agrawal et al. (1989) give an attainable asymptotic regret lower bound.
  — [arXiv §2, §4](https://arxiv.org/abs/1403.5556)
  - Relation (Overlap: High): justifies a dedicated probing bid b^I that may never be the exploitation-optimal bid, and rebuts "just run UCB or TS."
- **Lattimore, T. & Szepesvári, C. (2017). "The end of optimism? An asymptotic analysis of finite-armed linear bandits." arXiv:1610.04491** (AISTATS 2017 per the standard citation; venue unverified). — [arXiv](https://arxiv.org/abs/1610.04491)
  - Results:
    - An asymptotic lower bound c(A, θ) comes from an optimal-allocation problem.
    - The optimal algorithm has three phases: a warm-up on a barycentric spanner; a "success phase" that plays the optimal allocation T_n(Δ̂), including informative suboptimal arms; and a recovery phase running UCB if an anomaly is detected.
    - "No algorithm based on optimism or Thompson sampling will ever achieve the optimal rate, and indeed, can be arbitrarily far from optimal, even in very simple cases."
    — [arXiv](https://arxiv.org/abs/1610.04491)
  - Relation (Overlap: High): the asymptotically optimal policy is itself built in phases around an information-optimal design, mirroring WITS' information-maximizing probe.
- **Agrawal, R., Teneketzis, D. & Anantharam, V. (1989). "Asymptotically efficient adaptive allocation schemes for controlled i.i.d. processes: finite parameter space." IEEE TAC 34:258–267; Graves, T. L. & Lai, T. L. (1997). SIAM J. Control Optim. 35(3):715–743.** — [End-of-Optimism refs](https://arxiv.org/abs/1610.04491); [IDS refs and lit review](https://arxiv.org/abs/1403.5556)
  - With a finite parameter space they give an asymptotic regret lower bound for any admissible policy and show it is attainable. — [IDS §2](https://arxiv.org/abs/1403.5556)
  - (Overlap: High: binary θ is the simplest finite parameter space.)
- **Economics of incomplete learning:** Rothschild (1974), "A two-armed bandit theory of market pricing," JET 9(2):185–202; McLennan (1984), "Price dispersion and incomplete learning in the long run," JEDC 7(3):331–347; Easley & Kiefer (1988), "Controlling a stochastic process with unknown parameters," Econometrica 56(5):1045–1064; Aghion, Bolton, Harris & Jullien (1991), "Optimal learning by experimentation," RES 58(4):621–654. — [Tehrani et al. refs](https://arxiv.org/abs/1206.5345)
  - Rothschild showed that a seller following the optimal policy need not end up with complete information or settle at the optimal price. McLennan, in a binary demand model, showed incomplete learning can occur even with a continuum of prices. — [Tehrani §I.A](https://arxiv.org/abs/1206.5345)
  - (Overlap: Medium)
- **Fan, L. & Glynn, P. W. (2025). "The fragility of optimized bandit algorithms." Operations Research 73(6):3173–3198. arXiv:2109.13595.** — [arXiv](https://arxiv.org/abs/2109.13595); venue from the [Zhou et al. refs](https://arxiv.org/abs/2607.29375)
  - Results:
    - Algorithms optimized for expected regret have regret distributions with very heavy, truncated-Cauchy tails.
    - There is a sharp trade-off between the amount of UCB exploration and how heavy the tail is.
    - They are fragile under slight misspecification, and UCB can be modified for robustness.
    — [abstract summary](https://arxiv.org/abs/2109.13595)
  - Related titles (content not read): Simchi-Levi, Zheng & Zhu (2025), "A simple and optimal policy design with safety against heavy-tailed risk for stochastic bandits," MS 71(7):6298–6318; Simchi-Levi & Wang (2025), "Multi-armed bandit experimental design: online decision-making and adaptive inference," MS 71(6):4828–4846. — [Zhou et al. refs](https://arxiv.org/abs/2607.29375)
  - Relation (Overlap: Medium): a counterweight to "fully sequential is better". Optimized sequential policies carry tail and misspecification risk, and simple phased designs may be more robust (inference).

### Inferences
- WITS is "easy" in the sense of Slivkins et al. and well-separated in the sense of Broder–Rusmevichientong and HKZ. Asymptotically, greedy learning suffices and bounded regret is achievable (Tehrani et al.'s LRT).
- ETC can still be defended on three grounds:
  1. Finite-budget learning speed. The informativeness of the exploitation bid, |q_θL(b) − q_θH(b)| = b(θH − θL)/((b + θL)(b + θH)), can be far below its value at b^I. This happens when budget-paced bids are low (small budgets) or very high (large budgets, where both win probabilities approach 1).
  2. Simplicity and modularity (a probing agent and an exploitation agent with a sufficient-statistic hand-off).
  3. A tractable V(B), which the planner-level allocation results require.
- The paper would be strengthened by benchmarking against (a) a myopic Bayesian bidder (MBP, learning passively from exploitation bids), (b) an LRT/XLRT-style hybrid that probes at b^I only while uncertain, and (c) the Bayes-optimal dynamic program, which is low-dimensional with binary θ.

### Gaps
- The HKZ full text (exact assumptions for CMBP) and the Broder–Rusmevichientong primary text were not read; secondary sources were used.
- Venues for Kannan et al., the IDS journal version and "End of Optimism" are unverified.
- Bayati, Hamidi, Johari & Khosravi (2020), "Unreasonable effectiveness of greedy algorithms in multi-armed bandit with many arms" (NeurIPS 2020), and Jedor, Louëdec & Perchet (2021), "Be greedy in multi-armed bandits" (arXiv:2101.01086), were seen only in the [Zhou et al. refs](https://arxiv.org/abs/2607.29375); their content was not read.

---

## Q7. Disentangling exploration from exploitation (Lizzeri, Shmaya & Yariv 2024) and separate information channels

### Takeaway
Lizzeri, Shmaya & Yariv give the economic-theory case for separating an information channel from the payoff channel:
- any disentanglement restores complete learning;
- the optimal exploration rule is not an index;
- disentanglement is most valuable at intermediate parameter values.

The WITS probing agent separates exploration *in time* rather than *in parallel*, and its probes also earn payoff, so the fit is partial but useful. Strategic-experimentation models (Bolton–Harris; Keller–Rady–Cripps) are the multi-agent counterpart. They have a *common* state, whereas WITS teams have independent states coordinated by a planner.

### Cited Findings
- **Lizzeri, A., Shmaya, E. & Yariv, L. (2024). "Disentangling exploration from exploitation." arXiv:2404.19116 [econ.TH] (29 Apr 2024).** — [arXiv](https://arxiv.org/abs/2404.19116)
  - Model:
    - Two projects, each good or bad with independent priors.
    - Each period the agent chooses which project to exploit (discounted payoff) and splits a unit of attention, i.e. exploration, between the projects.
    - News is conclusive and arrives at Poisson rates that may differ by project and by type.
    - In a constrained version a predetermined share of exploration is tied to the exploited project: 0 means fully disentangled, and 1 means fully entangled, which nests Keller–Rady–Cripps (2005) and Keller–Rady (2010).
    — [arXiv §1](https://arxiv.org/abs/2404.19116)
  - Results:
    - With any positive disentanglement, the agent asymptotically exploits the realized best project (complete learning), which can fail under full entanglement.
    - With one safe project, the optimal policy is a threshold rule whose threshold depends only on the larger of the good-news and bad-news rates (Prop. 1).
    - Under full disentanglement the agent exploits the myopically optimal project, but the optimal *exploration* "does not adhere to an index policy akin to Gittins'" (Corollary 2, "No Exploration Index").
    - With balanced news, the choice is by project-specific information values (Prop. 2), and "the inferior project may hold greater information value."
    - In good-news settings exploration is persistent: absent news, the agent switches the explored project at most once (Prop. 3).
    - "Valuable information is actionable"; "Disentanglement is particularly valuable for intermediate parameter values."
    — [arXiv](https://arxiv.org/abs/2404.19116)
  - Relation (Overlap: Medium): formal economic case for separating the information channel (the WITS probing agent) from the payoff channel (the exploitation agent). The value of disentanglement peaking at intermediate parameters parallels WITS' bounded learning window.
- **Strategic experimentation:** Bolton & Harris (1999), "Strategic experimentation," Econometrica 67(2):349–374; Keller, Rady & Cripps (2005), "Strategic experimentation with exponential bandits," Econometrica 73(1):39–68; Keller & Rady (2010), "Strategic experimentation with Poisson bandits," Theoretical Economics 5(2):275–311. — [Lizzeri et al. refs](https://arxiv.org/abs/2404.19116)
  - Lizzeri et al.'s fully entangled case with one safe project and good-news-only arrivals "aligns with" Keller–Rady–Cripps. — [arXiv §1](https://arxiv.org/abs/2404.19116)
  - Contents otherwise not re-read. (Overlap: Low–Medium: multi-agent experimentation on a common state.)
- **Cross-references:** Bubeck, Munos & Stoltz (2011), with test and commercialization phases separated; Guha (2026), where exploration precedes exploitation ("future utilization"); Weitzman (1979), Pandora's box. — [Bubeck et al.](https://arxiv.org/abs/0802.2655); [Guha 2026](https://arxiv.org/abs/2610.24156)

### Inferences
- In agent-team terms the probing agent is an information channel. Lizzeri et al. suggest its value peaks at intermediate parameter values and that its allocation cannot be decided by a per-unit index, which fits the planner-level nonconcavity findings (Q1).
- WITS teams have independent competition states, so there is no cross-team learning externality; this is cleaner than strategic experimentation. If teams faced a common competition state (the same exchange), Bolton–Harris and Keller–Rady–Cripps free-riding logic, and the value of pooling probes across teams, would enter. That is a natural extension for coordinating multiple agents.

### Gaps
- Whether Lizzeri et al. has been published beyond arXiv is unknown.
- I found no paper on a dedicated probing agent in auction bidding.

---

## Q8. Budget-constrained bandits (bandits with knapsacks) — brief, only where they bear on ETC

### Takeaway
Bandits with knapsacks (BwK) is the learn-while-doing-under-budget benchmark a reviewer might propose. Its objective values outcomes *during* learning, so it differs from "observe, then terminal choice" formulations. Each WITS team is effectively a single-resource BwK instance with a continuous bid and a binary unknown. The operations-management evidence that separating learning harms performance under inventory constraints (Wang–Deng–Ye vs Besbes–Zeevi, Q2) is the most direct budget-side argument against ETC. Other researchers cover BwK in depth.

### Cited Findings
- **Badanidiyuru, A., Kleinberg, R. & Slivkins, A. (2013). "Bandits with knapsacks." FOCS 2013. DOI 10.1109/FOCS.2013.30. arXiv:1305.2545** (the journal version, JACM 2018, is unverified). — [Guha 2026 refs](https://arxiv.org/abs/2610.24156)
  - "Bandits with knapsacks add resource budgets to online reward maximization ... LP bounds and primal-dual resource prices." "These objectives value outcomes during learning, whereas here observations precede a terminal choice." Agrawal & Devanur (2014) extend the model to concave rewards and convex constraints. — [Guha 2026 related work](https://arxiv.org/abs/2610.24156)
  - Relation (Overlap: Medium): the per-team problem is a budgeted bandit, and the exploitation agent's constant budget-paced bid is the fluid (LP) policy once θ is known.
- **Li & Cheung (2024), "Best arm identification with resource constraints"** (pure exploration where each pull consumes resources, distinguishing deterministic from stochastic consumption). — [Guha 2026 related work](https://arxiv.org/abs/2610.24156). The year is from Guha's text; the venue is not confirmed. (Overlap: Medium)
- **Fluid optimality of a static action once demand is known:** "if one knows p^D, then simply applying this price can achieve asymptotically optimal performance," with O(n^{-1/2}) regret (Lemma 1, from Gallego & van Ryzin 1994, Management Science 40(8):999–1029). — [Wang, Deng & Ye](https://arxiv.org/abs/1101.4681). (Overlap: Medium; supports WITS' constant budget-paced exploitation bid.)

### Inferences
- In BwK terms the planner's ex-ante budget split is a "static knapsack allocation across sub-problems", and each team's ETC is "learn the dual price, then pace". The relevant BwK question for reviewers is whether learning-while-pacing beats probe-then-pace at the budget scales studied. The Q2 and Q6 evidence says the gap is a constant factor when hypotheses are known.

### Gaps
- I did not verify BwK-specific explore-first or ETC results (others cover BwK).

---

## Q9. Bottom line: the 3–5 results most useful for "why ETC instead of a bandit?", and the results a reviewer could use against ETC

### Takeaway
The defensible position is: "With two known competition states, ETC is rate-optimal and loses only constant factors. Those factors can be removed by a data-dependent τ or a second short probe, without giving up the modular two-agent design or the closed-form value function the planner needs." The authors should also concede, and preferably quantify, that in this model every bid is informative, so a myopic Bayesian bidder learns while exploiting.

### Cited Findings
**Most useful results for defending ETC**
1. **ETC is rate-optimal and near-optimal when the hypotheses are known.**
   - With a known gap, a fixed-design ETC with a tuned exploration length has O(log T/Δ) regret, the right rate. The asymptotic constants are 4 (fixed design), 1 (SPRT stopping) and 1/2 (fully sequential), so the loss is a constant factor, not a rate. — [Garivier, Kaufmann & Lattimore 2016](https://arxiv.org/abs/1605.08988); [Lattimore & Szepesvári eq. 6.6](https://tor-lattimore.com/downloads/book/book.pdf)
   - Tuned ETC "outperforms the parameter-free UCB, though only by a relatively small margin". — [L&S Experiment 7.1](https://tor-lattimore.com/downloads/book/book.pdf)
   - Double ETC (two explore/commit pairs) is *exactly* asymptotically optimal and needs O(1) rounds, which shows that phased structure per se is not what makes ETC suboptimal. — [Jin et al. 2021](https://arxiv.org/abs/2002.09174)
2. **Few phases lose little (limited adaptivity).**
   - √T regret needs only about log₂ log T batches or about K·log log T switches. — [Perchet et al. 2016](https://arxiv.org/abs/1505.00369); [Gao et al. 2019](https://arxiv.org/abs/1904.01763); [Simchi-Levi & Xu 2023](https://arxiv.org/abs/1905.10825)
   - With a known finite set of demand models, m price changes already give log^(m) T regret. — [Cheung, Simchi-Levi & Wang 2017](https://dspace.mit.edu/handle/1721.1/119156)
   - Phased exploration is rate-optimal whenever the best response is smooth (strongly convex action sets). — [Rusmevichientong & Tsitsiklis 2010](https://arxiv.org/abs/0812.3465)
3. **Profit-maximizing test & roll ≈ Thompson sampling in marketing.** A Bayesian A/B test with an ex-ante profit-maximizing sample size achieves nearly the regret of Thompson sampling (both O(√N)), with a transparent decision point and lower operational complexity. — [Feit & Berman 2019](https://arxiv.org/abs/1811.00457)
4. **Dedicated informative probing beats optimism and Thompson sampling in structured problems.**
   - UCB and TS sample only actions that might be optimal, so they never play a "revealing action" and can be arbitrarily suboptimal. — [Russo & Van Roy IDS](https://arxiv.org/abs/1403.5556); [Lattimore & Szepesvári 2017](https://arxiv.org/abs/1610.04491)
   - The asymptotically optimal structured policy is itself built in phases around an information-optimal design. — [Lattimore & Szepesvári 2017](https://arxiv.org/abs/1610.04491)
   - Chernoff-style experiment selection and an "exploration price" maximizing the Chernoff distance are classical ancestors of b^I. — [Chernoff 1959 via Albert 1961](https://projecteuclid.org/journals/annals-of-mathematical-statistics/volume-32/issue-3/The-Sequential-Design-of-Experiments-for-Infinitely-Many-States-of/10.1214/aoms/1177704973.full); [Tehrani et al. 2012](https://arxiv.org/abs/1206.5345)
5. **Pure exploration followed by exploitation is the right abstraction when probing is a resource and value comes later.**
   - Regret-minimizing allocation is information-poor ("the smaller the cumulative regret, the larger the simple regret"). — [Bubeck, Munos & Stoltz](https://arxiv.org/abs/0802.2655)
   - Budgeted learning for future utilization has LP and Lagrangian approximation algorithms for many units. — [Guha & Munagala 2007 / Guha 2026](https://arxiv.org/abs/2610.24156)
   - With a safe option, the Bayes-optimal finite-horizon one-armed policy is a stopping rule, i.e. explore-then-commit. — [L&S §35.6 note 7](https://tor-lattimore.com/downloads/book/book.pdf)
   - The planner-level nonconcavity ("jump at entry", focusing learning on fewer units) is a known value-of-information phenomenon. — [Frazier & Powell 2010](https://collaborate.princeton.edu/en/publications/paradoxes-in-learning-and-the-marginal-value-of-information/); [Chade & Schlee 2002](https://econpapers.repec.org/RePEc:eee:jetheo:v:107:y:2002:i:2:p:421-452)

**Results a reviewer could use against ETC**
- **"ETC is necessarily suboptimal."** Phase-separated strategies have asymptotically twice the regret of fully sequential ones. With a known gap, fixed-length exploration (WITS' τ chosen up front) is 8× worse than the optimum and 4× worse than SPRT-stopped ETC. — [Garivier, Kaufmann & Lattimore 2016](https://arxiv.org/abs/1605.08988)
- **"A fixed sample size is the least efficient test."** For simple hypotheses the SPRT minimizes expected sample size, and batch tests need about 4× more samples. — [Wald & Wolfowitz 1948](https://www.projecteuclid.org/euclid.aoms/1177730197); [Kaufmann, Cappé & Garivier 2016](https://arxiv.org/abs/1407.4443)
- **"Learning-while-doing beats learn-then-earn under budget/inventory constraints."** Concurrent learning achieves O*(n^{-1/2}) relative regret, with a matching lower bound, against the best-known O*(n^{-1/3}) (parametric) and O*(n^{-1/4}) (nonparametric) bounds for separated phases, and "firms would be better off to perform dynamic learning and action concurrently rather than sequentially." The authors' rebuttal: that setting has unknown multi-parameter or nonparametric demand, not two known hypotheses. — [Wang, Deng & Ye 2014](https://arxiv.org/abs/1101.4681)
- **"In your model greedy learning is enough."** The documented failure of myopic Bayesian learning is getting stuck at uninformative actions, and discriminative policies give bounded regret. Likelihood-ratio policies give bounded regret with finitely many models. Greedy succeeds if and only if the instance is self-identifiable. In WITS, q_θL(b) ≠ q_θH(b) for every positive bid, so a myopic Bayesian bidder learns while exploiting (inference). — [Harrison, Keskin & Zeevi 2012](https://pubsonline.informs.org/doi/fpi/10.1287/mnsc.1110.1426); [Tehrani et al. 2012](https://arxiv.org/abs/1206.5345); [Slivkins, Xu & Zuo 2025](https://arxiv.org/abs/2503.04010); [Broder & Rusmevichientong 2012 (secondary)](https://arxiv.org/pdf/2603.08956)
- **"Untuned ETC performs poorly in finite horizons, and two-batch policies are T^{2/3} when the gap is unknown."** — [Zhou, Li & Wang 2026 benchmarks](https://arxiv.org/abs/2607.29375); [Perchet et al. 2016](https://arxiv.org/abs/1505.00369); [L&S Ex. 15.6](https://tor-lattimore.com/downloads/book/book.pdf)
- **"Why not solve the Bayes-optimal adaptive policy?"** Exact Bayesian dynamic programming is feasible for small problems. — [L&S §35.6 note 9](https://tor-lattimore.com/downloads/book/book.pdf)

### Inferences
- Suggested positioning: describe WITS as a *planner-level* contribution (budget split across teams under nonconcave learning value) that uses ETC as a tractable team-level protocol. Cite GLK, Jin et al., Perchet et al. and Feit–Berman to show this choice loses only constants in the known-hypothesis regime.
- Show robustness of the allocation insights by replacing fixed τ with (a) an SPRT on w, (b) DETC, and (c) a myopic Bayesian bidder or LRT hybrid, and check whether the "skew when the junior cannot afford to learn, balance once both learn" pattern survives.
- Justify b^I through information-directed and Chernoff design. Consider whether information per unit of expected spend, rather than the win-probability gap, should define the probing bid.
- For the AI-agent extension (token budgets across sub-agents), cite budgeted learning (Guha–Munagala; Guha 2026) and Whittle-type Lagrangian decoupling as the scalable n-unit theory, and limited-adaptivity results to justify infrequent hand-offs.

### Gaps
- I found no published paper that combines (i) several independent learners, each running ETC under its own budget, (ii) an ex-ante planner split with valuation weights, and (iii) RTB first-price win-curve learning. The closest neighbors are budgeted learning (single terminal selection, no exploration payoff), BwK (a single learner), the Whittle relaxation (no learning-phase structure) and test & roll (a single test).
- These notes cover theory foundations only. Multi-campaign and RTB budget allocation with learning, and LLM-agent budget coordination, are assigned to other researchers.
