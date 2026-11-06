# Marketing / IS / OM literature on test-and-roll vs bandits, allocating experimentation resources, ad budget allocation and bidding with learning, and dynamic pricing with learning — positioning notes for "Orchestrating Agent Teams: Budget Allocation in Real-Time Bidding" (Yang, Zhu, Mookerjee; WITS 2026)

Reading guide: each paper entry gives the full citation, model, main results, and "Relation" with an overlap rating (High / Medium / Low) relative to the focal paper. The focal paper has a planner splitting budget T across teams with values v1 > v2. Each team runs first-price RTB with unknown binary competition θ ∈ {θL, θH} and win probability q_θ(b) = b/(b+θ). Each team uses a fixed-length probing phase τ, then a Bayesian, budget-paced constant bid. "Verified" means the claim was checked against the paper text, the abstract, or an indexing record in this session. Anything not checked that way is marked **unverified**. Entries are grouped by key question. Q8 gives the shortlist of closest works.

## Q1. Test & roll (explore-then-commit, ETC) vs bandits: direct evidence, extensions, later work (through 2026)

### Takeaway
The marketing evidence (Feit & Berman 2019) shows that a test & roll with an optimally sized test reaches regret of the same order as Thompson sampling, O(√N). The absolute gap is small in realistic marketing priors: about 0.2–1.7% of perfect-information profit for test & roll, versus 0.03–0.6% for Thompson sampling. The gap grows with more arms and with intermediate prior dispersion. Theory says ETC is never exactly optimal. It loses a factor of 2 in asymptotic regret, and a fixed-length test loses a further factor of 4 against a sequential-stopping ETC when the two hypotheses are known (Garivier et al. 2016). But a handful of batches recovers near-optimal minimax regret (Perchet et al. 2016). The closest budget-limited precedent of "spend a fraction of the budget exploring, then exploit" is the ε-first policy (Tran-Thanh et al. 2010).

### Cited Findings
- **Feit, E. M., & Berman, R. (2019). "Test & Roll: Profit-Maximizing A/B Tests." *Marketing Science* 38(6):1038–1058. DOI 10.1287/mksc.2019.1194; arXiv 1811.00457.** — [arXiv](https://arxiv.org/abs/1811.00457); [RePEc](https://econpapers.repec.org/RePEc:inm:ormksc:v:38:y:2019:i:6:p:1038-1058); [INFORMS DOI record](https://pubsonline.informs.org/doi/suppl/10.1287/mksc.2019.1194)
  - *Model:* Finite population N. A test stage gives n1 and n2 customers each treatment. The roll stage deploys the posterior-better treatment to the remaining N−n1−n2. Normal responses with normal priors. The objective is total expected profit, with the explicit trade-off between test opportunity cost and the risk of a wrong roll. The authors describe it as "a constrained version of a multi-armed bandit, where there are only two allocation decisions instead of many." — [arXiv](https://arxiv.org/abs/1811.00457)
  - *Main results:* Closed-form profit-maximizing n*. It is "substantially smaller than typically recommended for a hypothesis test." It grows sub-linearly in the response s.d. and is proportional to √N. Asymmetric priors rationalize small holdout groups. Regret is O(√N) for test & roll versus Ω(N) for the hypothesis-test sample size. "The proposed test design achieves nearly the same expected regret as the flexible, yet harder-to-implement multi-armed bandit." — [arXiv](https://arxiv.org/abs/1811.00457)
  - *Head-to-head numbers vs Thompson sampling (TS), regret relative to perfect information:*
    - Website test (N=100,000): n*=2,284 per arm. Test & roll regret is 0.22% vs TS 0.03%. TS yields 136 more conversions (69,672 vs 69,536). The hypothesis test needs 18,468 per arm. — [arXiv](https://arxiv.org/abs/1811.00457)
    - Display ads, with priors built from Lewis & Rao (2015) (N=1,000,000): n*=11,391 per arm. Test & roll regret is 0.89% vs TS 0.29%. The wrong-roll rate is 6.9%. A standard hypothesis test would need 4,782,433 per arm. — [arXiv](https://arxiv.org/abs/1811.00457)
    - Catalog holdout with asymmetric priors: n1*=588 control and n2*=1,884 treated. Test & roll regret is 1.68% vs TS 0.57%. — [arXiv](https://arxiv.org/abs/1811.00457)
  - *When TS wins more:* "The difference between algorithms is more pronounced when there are a greater number of treatment arms." Simulations use K up to 8. The gap is also larger at moderate expected differences σ. Relative regret of test & roll peaks at intermediate σ (Corollary A.5). "A test that is too large is preferable to one that is too small by the same amount." — [arXiv](https://arxiv.org/abs/1811.00457)
  - *Why practitioners choose test & roll:* it gives "a transparent decision point and reduced operational complexity without significant loss of profit." The dynamic approach is hard to run "when the response is not immediately observable (e.g., sales) or when the treatments are sent out in batches." Schwartz et al. (2017) and Misra et al. (2019) "use a test & roll as a benchmark, but they do not optimize the sample size." — [arXiv](https://arxiv.org/abs/1811.00457)
  - *Relation:* The most direct published answer to "why ETC instead of a bandit." The focal paper's probing length τ is the analogue of n*. The total team budget plays the role of N. **Overlap: High** on the ETC-vs-bandit question. Low on cross-campaign budget allocation, since the paper has a single test and no planner.
- **Garivier, A., Kaufmann, E., & Lattimore, T. (2016). "On Explore-Then-Commit Strategies." NIPS 2016 (30th Conference on Neural Information Processing Systems). arXiv 1605.08988.** — [arXiv](https://arxiv.org/abs/1605.08988)
  - *Model:* Two-armed Gaussian bandit with horizon T. Motivated explicitly by website A/B testing followed by deployment. Compares fixed-design ETC, data-dependent-stopping ETC, and fully sequential policies. — [arXiv](https://arxiv.org/abs/1605.08988)
  - *Results:* "Strategies based on an exploration phase (up to a stopping time) followed by exploitation are necessarily suboptimal." The asymptotic regret constants (× log T/Δ) are:
    - Known gap: fixed-design ETC 4; SPRT-based ETC 1; fully sequential Δ-UCB 1/2.
    - Unknown gap: best ETC 4; UCB 2.
    - So ETC loses a factor of 2 versus fully sequential policies. Fixed-design ETC with known gap loses a factor of 4 versus SPRT-ETC and 8 versus the best sequential policy. — [arXiv](https://arxiv.org/abs/1605.08988)
  - *Fixed design is still minimax-order optimal:* "In all cases, R ≤ 2.04√T + Δ." In simulations, best-arm-identification ETC "performs very well" at short horizons. — [arXiv](https://arxiv.org/abs/1605.08988)
  - *Relation:* The canonical citation a reviewer would raise against ETC. Because θ is binary (two simple hypotheses), the "known-gap" case applies. The focal paper's fixed-τ probing is the fixed-design ETC, which is asymptotically 4× worse than an SPRT stopping rule. **Overlap: High** (it answers the reviewer question directly).
- **Perchet, V., Rigollet, P., Chassang, S., & Snowberg, E. (2016). "Batched Bandit Problems." *Annals of Statistics* 44(2):660–681. DOI 10.1214/15-AOS1381; arXiv 1505.00369.** — [arXiv](https://arxiv.org/abs/1505.00369)
  - *Model:* The policy can update only at M batch boundaries. Motivated by clinical trials and by marketing and internet advertising, where "technical constraints often force data to be considered in batches." Cites Bertsimas & Mersereau (2007) and Schwartz et al. (2013 WP). — [arXiv](https://arxiv.org/abs/1505.00369)
  - *Results:* The generic M-batch ETC policy has minimax regret T^{2/3} for M=2, i.e. a classic explore-then-commit. It is T^{4/7}(log T)^{1/7} for M=3, and reaches √T with about log₂ log T batches. Matching lower bounds hold for any M-batch policy. Near-optimal policies switch arms only O(log log T) times. — [arXiv](https://arxiv.org/abs/1505.00369)
  - *Relation:* Supports the focal design. A two-phase protocol is a 2-batch policy, and adding one or two more re-planning points recovers most of the gap. **Overlap: High** (theoretical defense of ETC with few switches).
- **Kawato, K., & Sakaguchi, S. (2026). "Prior-Free Sample Size Design for Test-and-Roll Experiments." arXiv 2605.02414 (econ.EM, May 2026).** — [arXiv](https://arxiv.org/abs/2605.02414)
  - *Model:* Finite-population test-and-roll with Bernoulli or Gaussian outcomes. Uses the empirical success rule. Regret is decomposed into exploration cost (m/2)|τ| and exploitation risk (N−m)|τ|·e(m). — [arXiv](https://arxiv.org/abs/2605.02414)
  - *Results:* Absolute minimax regret recommends "implausibly small" tests, e.g. m/N=2.3% at N=10,000. The proposed Worst-case Marginal Benefit rule gives the "rule of thirds" m* ≈ N/3. The paper positions itself against bandits because "outcomes are delayed, implementation is costly, or frequent reassignment raises ethical concerns." — [arXiv](https://arxiv.org/abs/2605.02414)
  - *Relation:* The newest (2026) test-and-roll extension. It shows that the choice of criterion (Bayesian, minimax, or marginal-minimax) moves the optimal τ from about √N to about N/3. **Overlap: Medium.**
- **Tran-Thanh, L., Chapman, A., Munoz de Cote, E., Rogers, A., & Jennings, N. R. (2010). "Epsilon–First Policies for Budget–Limited Multi-Armed Bandits." *Proceedings of AAAI-10* 24(1):1211–1216. DOI 10.1609/aaai.v24i1.7758.** — [AAAI](https://ojs.aaai.org/index.php/AAAI/article/view/7758)
  - *Model:* Arm pulls cost money under a fixed budget. The ε-first policy spends a fraction ε of the budget learning arm rewards and the rest exploiting the estimates. — [AAAI](https://ojs.aaai.org/index.php/AAAI/article/view/7758)
  - *Results:* The authors bound the loss and report up to 50% improvement over traditional bandit algorithms. Later work (Tran-Thanh et al. 2012, AAAI, "Knapsack based optimal policies for budget-limited multi-armed bandits") notes that ε-first performance depends on the chosen ε. — [AAAI](https://ojs.aaai.org/index.php/AAAI/article/view/7758); [Avadhanula et al. reference list](https://arxiv.org/abs/2103.10246)
  - *Relation:* The exact algorithmic precedent of "a budget share for probing, then commit." **Overlap: High** (algorithmic). It has no planner across teams and no auction structure.
- **Bertsimas, D., & Mersereau, A. J. (2007). "A Learning Approach for Interactive Marketing to a Customer Segment." *Operations Research* 55(6):1120–1135. DOI 10.1287/opre.1070.0427.** — [RePEc](https://econpapers.repec.org/RePEc:inm:oropre:v:55:y:2007:i:6:p:1120-1135)
  - *Model:* A Bayesian bandit in which marketing messages are sent to batches of customers, and decisions may vary within a batch. — [RePEc](https://econpapers.repec.org/RePEc:inm:oropre:v:55:y:2007:i:6:p:1120-1135)
  - *Results:* A Lagrangian-decomposition ADP and an asymptotic-index heuristic "clearly outperform approaches that ignore the effects of information gain." — [RePEc](https://econpapers.repec.org/RePEc:inm:oropre:v:55:y:2007:i:6:p:1120-1135)
  - *Relation:* An early OR/marketing statement that batched decisions make the exploration problem closer to staged designs. **Overlap: Medium.**
- **Field evidence that adaptive designs beat fixed A/B tests in advertising** (details in Q2):
  - Comparison Lift at JD.com: the adaptive design produced about 27% more clicks during testing than a fixed-sample A/B design. — [arXiv](https://arxiv.org/abs/2009.07899)
  - Misra et al. (2019): +43% profit in the test month versus balanced experiments, in calibrated simulation. — [INFORMS](https://pubsonline.informs.org/doi/fpi/10.1287/mksc.2018.1129)
  - Schwartz et al. (2017): about 8% higher acquisition rate than the control policy. — [Penn repository](https://repository.upenn.edu/handle/20.500.14332/48003)
  - These numbers compare against balanced or fixed designs, not against an optimally sized test & roll. Feit & Berman note that neither Schwartz et al. nor Misra et al. optimized the test & roll sample size. — [arXiv](https://arxiv.org/abs/1811.00457)

### Inferences
- The two literatures do not contradict each other.
  - Garivier et al. compare asymptotic, frequentist regret constants (factor 2).
  - Feit & Berman compare Bayesian prior-averaged regret at finite N with data-calibrated priors. Both designs are O(√N), and the realized absolute gap is a fraction of a percent of profit.
  - Perchet et al. show that the frequentist minimax rate of a pure 2-stage design is T^{2/3}, not √T. The authors should be clear about which criterion they invoke.
- For the reviewer question, the strongest defense combines four points:
  1. Feit & Berman's empirical near-equivalence and their operational rationale (transparency, delayed or batched feedback).
  2. Perchet et al.'s result that a few re-plans recover near-optimality.
  3. Platform-imposed learning phases (Q4), which make the probing length an institutional constraint.
  4. The planner's ex ante budget split, which needs a forecastable per-team value function V(a). ETC yields that in closed form; an adaptive bandit generally does not.
- A reviewer may still ask why τ is fixed rather than set by a sequential (SPRT-type) stopping rule. With binary θ this is exactly Garivier et al.'s known-gap case, where fixed design is 4× worse asymptotically than an SPRT-ETC. The authors should either discuss this or show that the gap is small at the budget scales they study.
- Feit & Berman find that the bandit advantage grows with the number of arms. The n-team extension does not add arms within a team, so the two-hypothesis setting is the most favorable case for ETC.

### Gaps
- No published "multi-arm test & roll" paper was found. Feit & Berman's own K>2 results are numerical (Figure 5). The 2021–2026 discovery searches returned extensions on sample-size criteria (Kawato & Sakaguchi 2026) and on experimentation programs (Q3), but no K-arm closed form.
- No paper was found that compares ETC and bandits when the resource being consumed is the *bidding budget itself*, i.e. probing costs money only on wins. All test & roll papers measure exploration cost as opportunity cost per unit.

## Q2. Bandits vs A/B tests in marketing and IS practice (adaptive experimentation on digital platforms)

### Takeaway
Marketing Science has a sustained line of bandit-experiment papers: Hauser et al. 2009, Schwartz et al. 2017, Misra et al. 2019, Aramayo et al. 2023, and Waisman et al. 2025, the last inside RTB auctions. Industry systems (Google's Thompson-sampling content experiments, JD.com's Comparison Lift) argue that, online, opportunity cost dominates experimentation cost. That is the argument reviewers will use for "why not a bandit." No ISR or MISQ paper comparing bandits with ETC for ad budgets was found.

### Cited Findings
- **Scott, S. L. (2010). "A modern Bayesian look at the multi-armed bandit." *Applied Stochastic Models in Business and Industry* 26(6):639–658. DOI 10.1002/asmb.874.** — [RePEc](https://econpapers.repec.org/RePEc:wly:apsmbi:v:26:y:2010:i:6:p:639-658)
  - *Model:* Randomized probability matching (Thompson sampling). Arms are chosen with probability equal to the posterior probability that each is best. — [RePEc](https://econpapers.repec.org/RePEc:wly:apsmbi:v:26:y:2010:i:6:p:639-658)
  - *Results:* Simple to implement and broadly applicable. Modern Bayesian computation widens the reward models it can handle. Published with a discussion (Agarwal) and a rejoinder. — [RePEc](https://econpapers.repec.org/RePEc:wly:apsmbi:v:26:y:2010:i:6:p:639-658)
  - *Relation:* The standard practitioner citation for "use TS instead of A/B." **Overlap: Medium.**
- **Scott, S. L. (2015). "Multi-armed bandit experiments in the online service economy." *Applied Stochastic Models in Business and Industry* 31(1):37–45 (rejoinder pp. 48–49). DOI 10.1002/asmb.2104.** — [Google Research](https://research.google/pubs/pub42550/); [RePEc](https://econpapers.repec.org/RePEc:wly:apsmbi:v:31:y:2015:i:1:p:37-45)
  - *Results:* In online services the cost of experimentation "is dominated by opportunity cost rather than the cost of obtaining experimental units," which calls for bandit experiments. Thompson sampling is singled out. — [Google Research](https://research.google/pubs/pub42550/)
  - *Relation:* A key argument against ETC. In the focal paper's RTB setting, probing does cost money (the bid is paid on a win), which partly answers Scott's framing. **Overlap: Medium.**
- **Schwartz, E. M., Bradlow, E. T., & Fader, P. S. (2017). "Customer Acquisition via Display Advertising Using Multi-Armed Bandit Experiments." *Marketing Science* 36(4):500–522. DOI 10.1287/mksc.2016.1023.** — [RePEc](https://econpapers.repec.org/RePEc:inm:ormksc:v:36:y:2017:i:4:p:500-522); [Penn repository](https://repository.upenn.edu/handle/20.500.14332/48003)
  - *Model:* Hierarchical, attribute-based Thompson sampling for ad allocation across websites and creatives, with **batched decisions** over millions of impressions. — [Penn repository](https://repository.upenn.edu/handle/20.500.14332/48003)
  - *Results:* A live field experiment with more than 750 million impressions for a large retail bank. About 8% improvement in customer acquisition rate over two months relative to a control policy. This figure is from the working-paper abstract as reported by a search summary; the published abstract wording is **unverified**. Optimizing CTR instead of conversions would cut acquisitions by about 10% (counterfactual). — [Penn repository](https://repository.upenn.edu/handle/20.500.14332/48003)
  - *Relation:* The closest marketing paper using bandits to allocate display-ad spend. It is batched, like the focal paper's phases, but has no budget split across campaigns and no auction bidding. **Overlap: Medium-High.**
- **Misra, K., Schwartz, E. M., & Abernethy, J. (2019). "Dynamic Online Pricing with Incomplete Information Using Multiarmed Bandit Experiments." *Marketing Science* 38(2):226–252. DOI 10.1287/mksc.2018.1129.** — [INFORMS](https://pubsonline.informs.org/doi/fpi/10.1287/mksc.2018.1129); [RePEc](https://econpapers.repec.org/RePEc:inm:ormksc:v:38:y:2019:i:2:p:226-252)
  - *Model:* A bandit pricing policy built on economic demand theory (partial identification); weakly downward-sloping demand. — [INFORMS](https://pubsonline.informs.org/doi/fpi/10.1287/mksc.2018.1129)
  - *Results:* Asymptotically optimal. In a calibrated simulation based on a pricing field experiment it raises profit by 43% during the testing month and 4% annually. Balanced price experiments "can create high opportunity costs." — [INFORMS](https://pubsonline.informs.org/doi/fpi/10.1287/mksc.2018.1129)
  - *Relation:* Marketing evidence against balanced A/B designs, though not against an optimized test & roll. **Overlap: Medium.**
- **Hauser, J. R., Urban, G. L., Liberali, G., & Braun, M. (2009). "Website Morphing." *Marketing Science* 28(2):202–223.** DOI not confirmed in this session (**unverified**). — [RePEc](https://econpapers.repec.org/RePEc:inm:ormksc:v:28:y:2009:i:2:p:202-223); [MIT DSpace](https://dspace.mit.edu/handle/1721.1/52436)
  - *Model:* A POMDP balancing learning against short-term sales, solved in real time with expected Gittins indices. Tested on a BT Group website with 835 priming respondents. — [RePEc](https://econpapers.repec.org/RePEc:inm:ormksc:v:28:y:2009:i:2:p:202-223)
  - *Results:* With perfect information on cognitive styles, the optimal morph assignment would raise purchase intentions by 21%. This is a benchmark, not a measured lift. The rejoinder clarifies that the expected Gittins index is close to optimal, not exactly optimal. — [RePEc](https://econpapers.repec.org/RePEc:inm:ormksc:v:28:y:2009:i:2:p:202-223); [Rejoinder](https://stuff.mit.edu/~hauser/Papers/Morphing_Rejoinder_2009.pdf)
  - *Relation:* Seminal marketing bandit work. **Overlap: Low-Medium.**
- **Aramayo, N., Schiappacasse, M., & Goic, M. (2023). "A Multiarmed Bandit Approach for House Ads Recommendations." *Marketing Science* 42(2):271–292. DOI 10.1287/mksc.2022.1378.** — [RePEc](https://econpapers.repec.org/RePEc:inm:ormksc:v:42:y:2023:i:2:p:271-292)
  - *Results:* A bandit with time-varying effectiveness and neural-network personalization for a large retailer's house ads. In controlled experiments it beat managers' decisions and other bandit policies, with a "significant increment" in click-through and add-to-cart rates. — [RePEc](https://econpapers.repec.org/RePEc:inm:ormksc:v:42:y:2023:i:2:p:271-292)
  - *Relation:* **Overlap: Low.**
- **Waisman, C., Nair, H. S., & Carrion, C. (2025). "Online Causal Inference for Advertising in Real-Time Bidding Auctions." *Marketing Science* 44(1):176–195. DOI 10.1287/mksc.2022.0406; arXiv 1908.08600 (the arXiv version also lists Nan Xu).** — [RePEc](https://econpapers.repec.org/RePEc:inm:ormksc:v:44:y:2025:i:1:p:176-195); [arXiv](https://arxiv.org/abs/1908.08600)
  - *Model:* Uses the structure of first- and second-price auctions to show that ad effects are identified by the advertiser's optimal bids. An adapted Thompson sampling algorithm learns the optimal bids "while minimizing the costs of experimentation." — [RePEc](https://econpapers.repec.org/RePEc:inm:ormksc:v:44:y:2025:i:1:p:176-195)
  - *Results:* An order-optimal regret bound. On RTB data it outperforms common ad-effect estimation methods. — [RePEc](https://econpapers.repec.org/RePEc:inm:ormksc:v:44:y:2025:i:1:p:176-195)
  - *Relation:* The closest Marketing Science paper combining RTB bidding with learning by bandit. A natural reviewer citation for "TS in RTB is feasible." **Overlap: Medium-High.**
- **Geng, T., Lin, X., Nair, H. S., Hao, J., Xiang, B., & Fan, S. (2021). "Comparison Lift: Bandit-based Experimentation System for Online Advertising." *Proceedings of AAAI-21* 35(17):15117–15126. DOI 10.1609/aaai.v35i17.17775; arXiv 2009.07899.** — [AAAI](https://ojs.aaai.org/index.php/AAAI/article/view/17775); [arXiv](https://arxiv.org/abs/2009.07899)
  - *Results:* An experimentation-as-a-service tool at JD.com for testing audiences and creatives. More than 1,500 experiments since May 2019. CTR rose 46% on average for participating campaigns, and the adaptive design gave about 27% more clicks during testing than a fixed-sample A/B design. Both are the authors' estimates. — [arXiv](https://arxiv.org/abs/2009.07899)
  - *Relation:* Industry evidence for bandits over fixed tests in advertising. **Overlap: Medium.**
- **Ye, Z., Zhang, D. J., Zhang, H., Zhang, R., Chen, X., & Xu, Z. (2023). "Cold Start to Improve Market Thickness on Online Advertising Platforms: Data-Driven Algorithms and Field Experiments." *Management Science* 69(7):3838–3860. DOI 10.1287/mnsc.2022.4550.** — [RePEc](https://econpapers.repec.org/RePEc:inm:ormnsc:v:69:y:2023:i:7:p:3838-3860); [INFORMS](https://pubsonline.informs.org/doi/fpi/10.1287/mnsc.2022.4550)
  - *Model:* A platform-side cold-start (learning) phase for new ads. "Shadow bidding with learning" (SBL) algorithms built on duality and bandits, with a regret bound. — [INFORMS](https://pubsonline.informs.org/doi/fpi/10.1287/mnsc.2022.4550)
  - *Results:* A two-sided randomized field experiment on a large video-sharing platform. The partner is not named in the sources; the query's "Alibaba" was **not** supported. Cold-start success rose 61.62%, short-term revenue fell 0.717%, market thickness rose 3.13%, and long-term ad revenue rose at least 5.35%. — [INFORMS](https://pubsonline.informs.org/doi/fpi/10.1287/mnsc.2022.4550)
  - *Relation:* Management Science evidence that ad-platform learning phases are a designed, budget-like allocation of exposure. Good support for the focal paper's "learning phase" framing. **Overlap: Medium-High.**

### Inferences
- Reviewers from marketing (Feit, Schwartz, Nair, Hauser lineages) will expect the authors to cite Feit & Berman for ETC and Schwartz et al., Waisman et al. and Comparison Lift for bandits in ads.
- A defensible position: bandits are preferable when feedback is immediate and arms are many. The focal setting has two hypotheses, a planner who must commit budgets ex ante, and platform-fixed learning windows, all of which favor ETC.
- Scott's argument that "opportunity cost dominates" is weaker in RTB, where a probe consumes the real budget on wins. Probing is therefore a direct cash cost, as in Tran-Thanh et al.'s budget-limited bandits.

### Gaps
- Targeted searches found no ISR or MISQ paper (2017–2026) on bandits vs A/B tests or ETC for ad budgets. One search explicitly returned none, and the closest hits were conference or arXiv papers. This should be confirmed with the AIS eLibrary / ISR site search (not done here).
- The published-version wording of Schwartz et al.'s 8% figure is unverified; INFORMS and CORE pages blocked fetching.

## Q3. Allocating experimentation resources across many experiments; returns to experiment size (convex vs concave production of information)

### Takeaway
The economics and marketing literature already formalizes "split a fixed experimental resource across many learning problems" (Azevedo et al. 2020; Azevedo, Mao, Montiel Olea & Velez 2023; Sudijono et al. 2024). The production function (value of information as a function of sample size) is convex near zero and concave later, with f′(0)=0 for thin-tailed priors. This yields "go big," concentrating everything on one idea, when resources are scarce, and "go lean," spreading equally, when resources are abundant or tails are fat. This is the same qualitative mechanism as the focal paper's "learning pays only in a budget window" and "skewed then balanced split."

### Cited Findings
- **Azevedo, E. M., Deng, A., Montiel Olea, J. L., Rao, J., & Weyl, E. G. (2020). "A/B Testing with Fat Tails." *Journal of Political Economy* 128(12):4614–4672. DOI 10.1086/710607.** — [IDEAS](https://ideas.repec.org/a/ucp/jpolec/doi10.1086-710607.html); [2019 working-paper PDF](https://www.gwern.net/doc/statistics/decision/2019-azevedo.pdf)
  - *Model:* A firm with I ideas and N users. It allocates users to experiments, then implements ideas with positive posterior mean. The firm maximizes the sum of per-idea "production functions" f(n), the expected gain from testing an idea on n users. — [WP PDF](https://www.gwern.net/doc/statistics/decision/2019-azevedo.pdf)
  - *Theorem 2:* For small n, the marginal product is roughly proportional to n^{(α−3)/2}, where α is the tail coefficient of the prior. With α > 3 (thin tails) the marginal product at n=0 is zero, giving "increasing returns to scale." With α < 3 it is infinite. — [WP PDF](https://www.gwern.net/doc/statistics/decision/2019-azevedo.pdf)
  - *Corollary 1:*
    - Thick tails: "go lean" and test all ideas.
    - Thin tails with small N: the firm "should allocate all experimental resources to one idea," i.e. "go big."
    - Remark 1: with large enough N, go lean.
    - Intuition: with thin tails "a small bit of information is unlikely to change the optimal action … nearly useless," which reproduces Radner & Stiglitz (1984). — [WP PDF](https://www.gwern.net/doc/statistics/decision/2019-azevedo.pdf)
  - *Bing evidence (working-paper version):* The tail coefficient is "considerably smaller than 3." The top 2% of ideas account for 74.8% of historical gains. Testing 20% more ideas with the same users would raise productivity by 17.05%. The average experiment has about 20 million users. The published-version numbers may differ slightly (**unverified**). — [WP PDF](https://www.gwern.net/doc/statistics/decision/2019-azevedo.pdf); [IDEAS](https://ideas.repec.org/a/ucp/jpolec/doi10.1086-710607.html)
  - *Relation:* The closest formal antecedent of the focal paper's allocation logic: a fixed resource, separate learners, and a non-concave value of information. It lacks value heterogeneity across learners and auctions. **Overlap: High.**
- **Azevedo, E. M., Mao, D., Montiel Olea, J. L., & Velez, A. (2023). "The A/B Testing Problem with Gaussian Priors." *Journal of Economic Theory* 210:105646. DOI 10.1016/j.jet.2023.105646.** — [IDEAS](https://ideas.repec.org/a/eee/jetheo/v210y2023ics002205312300042x.html); [WP PDF (Mar 2020)](https://eduardomazevedo.github.io/papers/azevedo-et-al-ab-gaussian.pdf)
  - *Model:* A risk-neutral firm chooses a sample size and an implementation rule, with a Gaussian prior and linear costs. — [WP PDF](https://eduardomazevedo.github.io/papers/azevedo-et-al-ab-gaussian.pdf)
  - *Results:* Closed-form value of experimentation and optimal sample size; minimax-regret sample size; least-favorable prior.
    - Proposition 2: f(n) "is bounded, increasing, convex in an interval [0, n̂], and concave in [n̂, ∞)," with closed-form n̂.
    - When the prior mean M ≠ 0, f′(0)=0, so a small experiment has essentially zero marginal value.
    - The convexity region is small when M ≈ 0. The paper connects explicitly to Radner & Stiglitz (1984) and Chade & Schlee (2002). — [WP PDF](https://eduardomazevedo.github.io/papers/azevedo-et-al-ab-gaussian.pdf)
  - *Relation:* Gives the precise S-shape behind a lower budget threshold for learning. **Overlap: High** (mechanism).
- **Sudijono, T., Ejdemyr, S., Lal, A., & Tingley, M. (2024). "Optimizing Returns from Experimentation Programs." arXiv 2412.05508 (Stanford / Netflix).** — [arXiv](https://arxiv.org/abs/2412.05508)
  - *Model:* The A/B Testing Problem of Azevedo et al. (2020), solved by dynamic programming for any prior. Shipping decisions use tuned p-value thresholds. Extensions cover "managing multiple experimentation programs with shared resources." — [arXiv](https://arxiv.org/abs/2412.05508)
  - *Theorem 1 (metaproduction function):* Let x* maximize f(x)/x. The optimum allocates equally across a subset of tests and zero to the rest:
    - one test if x* ≥ N;
    - N/x* tests if x* ∈ [N/I, N];
    - all I tests if x* ≤ N/I. — [arXiv](https://arxiv.org/abs/2412.05508)
  - *Netflix numbers:* The return-maximizing p-value threshold is "closer to 0.5 than to 0.05." The firm should run "several orders of magnitude more tests" with smaller allocations. p<0.05 is optimal only if implementation costs are about 9× |μ|. — [arXiv](https://arxiv.org/abs/2412.05508)
  - *Relation:* Theorem 1 is the clean statement of "concentrate when scarce, spread when abundant" for S-shaped learners. The focal paper's two-team result is a value-weighted, auction-based instance of it. **Overlap: High.**
- **Schmit, S., Shah, V., & Johari, R. (2019). "Optimal Testing in the Experiment-rich Regime." AISTATS 2019, PMLR 89:626–633; arXiv 1805.11754.** — [PMLR](https://proceedings.mlr.press/v89/schmit19a.html)
  - *Results:* Many hypotheses and costly observations. The paper derives the optimal policy for allocating observations across experiments. "Paradox of power": high-power classical tests sample inefficiently, and efficient discovery comes with low classical power. — [PMLR](https://proceedings.mlr.press/v89/schmit19a.html)
  - *Relation:* **Overlap: Medium.**
- **Basu, P., & Berman, R. (2024/2025). "Ranking by Lifts: A Cost-Benefit Approach to Large-Scale A/B Tests." arXiv 2407.01036 (v3 Aug 2025).** — [arXiv](https://arxiv.org/abs/2407.01036)
  - *Results:* Maximizes expected profit subject to a cost-weighted FDR constraint. An empirical-Bayes greedy-knapsack ranking by expected lift-to-cost ratio, using the local FDR. Applied to 2,766 Optimizely tests. Builds on "experimentation programs" (Sudijono et al.). Also cites Berman & Van den Bulte (2022), "False Discovery in A/B Testing," *Management Science* 68(9):6762–6782. — [arXiv](https://arxiv.org/abs/2407.01036)
  - *Relation:* **Overlap: Low-Medium.**
- **Bastani, H., Simchi-Levi, D., & Zhu, R. (2022). "Meta Dynamic Pricing: Transfer Learning Across Experiments." *Management Science* 68(3):1865–1881. DOI 10.1287/mnsc.2021.4071; arXiv 1902.10918.** — [RePEc](https://econpapers.repec.org/RePEc:inm:ormnsc:v:68:y:2022:i:3:p:1865-1881); [MIT DSpace](https://dspace.mit.edu/handle/1721.1/148654)
  - *Results:* A sequence of Thompson-sampling pricing experiments for related products whose demand parameters share an unknown prior. The prior is learned online, and regret grows sublinearly in the number of products. — [RePEc](https://econpapers.repec.org/RePEc:inm:ormnsc:v:68:y:2022:i:3:p:1865-1881)
  - *Relation:* Learning across many experiments; it could support sharing the prior π0 across teams. **Overlap: Medium-Low.**
- **Sandoval, R. J., Arbour, D., Feller, A., & Jordan, M. I. (2026). "Always-On Experimentation." arXiv 2609.38695 (Sep 30, 2026).** — [arXiv](https://arxiv.org/abs/2609.38695)
  - *Results:* Treatments are generated, often by GenAI, and added to or removed from a running experiment. Uses anytime-valid testing-by-betting with online FDR control. It is about inference, not allocation. — [arXiv](https://arxiv.org/abs/2609.38695)
  - *Relation:* **Overlap: Low.** Possibly useful for the "agentic" framing.
- **Classic value-of-information nonconcavity**, as cited by AMOV and ADMORW:
  - Radner, R., & Stiglitz, J. (1984), "A nonconcavity in the value of information," in *Bayesian Models in Economic Theory*.
  - Chade, H., & Schlee, E. (2002), "Another look at the Radner–Stiglitz nonconcavity in the value of information," *Journal of Economic Theory*.
  - Moscarini & Smith (2002) and Keppo et al. (2008) are also cited.
  - Reference details are taken from those reference lists; pages are **unverified**. — [AMOV WP](https://eduardomazevedo.github.io/papers/azevedo-et-al-ab-gaussian.pdf); [ADMORW WP](https://www.gwern.net/doc/statistics/decision/2019-azevedo.pdf)

### Inferences
- **Mapping to the focal results.** Define each team's value of learning as Δ(a) = V(a) − W(a). AMOV's f′(0)=0 plus convexity on [0, n̂] implies a minimum efficient learning scale, which is the lower edge of the "budget window."
  - The upper edge is consistent with Feit & Berman's relative regret peaking at an intermediate σ, and with production functions bounded by the value of perfect information.
  - With two S-shaped Δ's and weights v1 > v2, Sudijono's Theorem 1 and Azevedo's Corollary 1 predict the following. When T is too small for the junior team to cross its convex region, budget goes disproportionately to the senior team (skewed). Once both teams are on concave segments, the split becomes more balanced. This is the focal paper's comparative static.
- Reviewers who know this literature (MS/JPE-trained reviewers in marketing or economics of experimentation) may say the allocation insight "follows from nonconcave value of information." The defensible novelty is:
  1. the learning target is a market (competition) state, not idea quality;
  2. the experimentation cost is the auction spend itself, so probing and exploitation draw on the same budget;
  3. value heterogeneity v1 > v2 across learners;
  4. the RTB first-price structure with q_θ(b) = b/(b+θ).
- Feit & Berman's √N scaling of n*, against Kawato & Sakaguchi's N/3, suggests the authors should report how the optimal τ scales with a team's budget.

### Gaps
- No paper was found where the units being allocated are dollars spent in auctions, and where each learner's experiment both consumes and earns from the same budget. Azevedo-type models allocate users (traffic) as the experimental resource, and payoffs accrue after implementation.
- The published JPE numbers were not re-checked against the 2019 working paper.

## Q4. Ad-platform learning phases and the economics of measuring advertising returns

### Takeaway
Measuring advertising effects is intrinsically noisy and needs enormous samples (Lewis & Rao 2015; Gordon et al. 2019). Platforms institutionalize short, fixed learning windows:
- Google: the "Learning" status "never lasts more than 7 days."
- TikTok: volatility declines after "about 25 campaign results or 7 days."
- Meta: about 50 optimization events in 7 days, reported by secondary sources only.

This supports modeling τ as a fixed, ex ante "learning phase." No academic study of how learning-phase thresholds interact with budget allocation across campaigns was found.

### Cited Findings
- **Lewis, R. A., & Rao, J. M. (2015). "The Unfavorable Economics of Measuring the Returns to Advertising." *Quarterly Journal of Economics* 130(4):1941–1973.** — [IDEAS](https://ideas.repec.org/a/oup/qjecon/v130y2015i4p1941-1973.html); [PDF mirror](https://Www.Gwern.net/doc/economics/advertising/2015-lewis.pdf)
  - *Results:* 25 large field experiments with US retailers and brokerages, about $2.8 million in spend. The median ROI confidence interval is more than 100 percentage points wide. A coefficient of variation of about 10 in individual sales is common, so informative experiments "can easily require more than 10 million person-weeks." Selection bias cripples observational methods. — [IDEAS](https://ideas.repec.org/a/oup/qjecon/v130y2015i4p1941-1973.html)
  - *Relation:* Motivates why learning is costly and only worthwhile at scale. Feit & Berman build their display-ad priors from these experiments (Q1). **Overlap: Medium.**
- **Gordon, B. R., Zettelmeyer, F., Bhargava, N., & Chapsky, D. (2019). "A Comparison of Approaches to Advertising Measurement: Evidence from Big Field Experiments at Facebook." *Marketing Science* 38(2):193–225.** — [RePEc](https://econpapers.repec.org/RePEc:inm:ormksc:v:38:y:2019:i:2:p:193-225); [Kellogg PDF](https://www.kellogg.northwestern.edu/faculty/gordon_b/files/fb_comparison.pdf)
  - *Results:* 15 US advertising RCTs at Facebook, with 500 million user-experiment observations and 1.6 billion impressions. Observational methods "often fail" to reproduce the experimental lift, even with rich covariates. — [RePEc](https://econpapers.repec.org/RePEc:inm:ormksc:v:38:y:2019:i:2:p:193-225)
  - *Relation:* Supports explicit experimentation by a probing agent over passive inference. **Overlap: Low-Medium.**
- **Google Ads Help, "Duration of the learning period for campaigns and what affects it" (answer 13020501), fetched Nov 2026.** — [Google support](https://support.google.com/google-ads/answer/13020501)
  - The "Learning" status "never lasts more than 7 days." "Smart Bidding performance typically converges to your new goal within 1 to 2 conversion cycles." Duration depends on conversion volume and conversion-cycle length. Learning is triggered by new or reactivated strategies, composition changes and goal changes.
  - Budget and target changes "never remove your historical data or trigger 'Learning' status." Google advises evaluating over "2 conversion cycles or a 2 week window (whichever is longer)" and notes "low daily budgets" can slow ramp-up. — [Google support](https://support.google.com/google-ads/answer/13020501)
  - Secondary sources quote older guidance (about 7–14 days; 15 or 50 conversions per 30 days). These are not official and conflict with the current page.
- **TikTok Ads Help, learning phase article (aid=11234).** — [TikTok help](https://ads.tiktok.com/help/article?aid=11234)
  - Learning phase: "a period during which our ad system identifies the best users for a specific campaign target." Volatility typically declines "after about 25 campaign results or 7 days." Advertisers should avoid edits that retrigger learning, pausing, and "unreasonable budget setting." — [TikTok help](https://ads.tiktok.com/help/article?aid=11234)
  - According to a search summary (the blog itself was not fetched), the TikTok business blog suggests budgets that allow about 50 conversions in 7 days, roughly 50× the target CPA. — [TikTok blog](https://www.tiktok.com/business/blog/tiktok-fundamentals-unlock-full-potential-tiktok-advertising)
- **Meta Business Help Center, "About the learning phase" (help/112167992830700).** The official page did not render for the fetch tool, so its text is **unverified**. — [Meta help](https://www.facebook.com/business/help/112167992830700)
  - Secondary sources consistently report about 50 optimization events per ad set within 7 days to exit learning. Otherwise the status becomes "Learning Limited," and significant edits restart the clock. Thresholds of about 20% budget-change and lower event counts appear but are inconsistent across sources. — [Lebesgue blog](https://lebesgue.io/blog/facebook-ads-learning-phase/); [9clouds](https://9clouds.com/blog/learning-limited-status-impacts-facebook-ads/)
- **Ye et al. (2023, *Management Science*)**: a platform-designed cold-start phase with measurable revenue trade-offs (−0.717% short-term revenue vs +61.62% cold-start success). See Q2. — [INFORMS](https://pubsonline.informs.org/doi/fpi/10.1287/mnsc.2022.4550)

### Inferences
- Platform learning phases are event-count or time-based windows set by the platform. They tie the length of learning to conversions per dollar, and hence to budget. A small campaign may never finish learning ("Learning Limited"). This is an institutional counterpart to the focal paper's result that a junior team "cannot afford to learn."
- The authors could cite these windows as the empirical reason τ is fixed ex ante rather than adaptively stopped (cf. Garivier et al. in Q1). The citation should be explicit that Meta's figures come from practitioner sources.

### Gaps
- No peer-reviewed study was found that estimates the performance effect of platform learning phases or of "Learning Limited" status, or that links learning-phase thresholds to budget allocation across ad sets or campaigns.
- Meta's Advantage+ campaign budget (CBO) documentation, which allocates budget across ad sets that are each learning, was not retrievable. That claim is **unverified** and would need direct confirmation.

## Q5. Ad budget allocation across campaigns/channels and bidding with learning (RTB, pacing, first-price learning, surveys)

### Takeaway
The closest ad-tech analogue of the focal planner is Deng, Golrezaei, Jaillet, Liang & Mirrokni (2023). An advertiser allocates budget across channel autobidders treated as black boxes. Per-channel budgets alone attain the global optimum, and these budgets can be learned under bandit feedback. Combinatorial or knapsack bandits handle budget across sub-campaigns or platforms (Nuara et al. 2018/2022; Avadhanula et al. 2021). Pacing and first-price learning results (Balseiro & Gur 2019; Wang et al. 2023; Han, Zhou & Weissman) cover the single-team problem. The focal paper's win function q_θ(b) = b/(b+θ) is exactly the ORTB winning function of Zhang, Yuan & Wang (2014), with θ playing the role of ORTB's market parameter l.

### Cited Findings
**(a) RTB bidding functional form and censored learning**
- **Zhang, W., Yuan, S., & Wang, J. (2014). "Optimal Real-Time Bidding for Display Advertising." *Proceedings of KDD '14*, pp. 1077–1086. DOI 10.1145/2623330.2623633.** — [dblp](https://dblp.uni-trier.de/rec/bibtex/conf/kdd/ZhangYW14); [UCL Discovery](https://discovery.ucl.ac.uk/1496878/)
  - *Model and result (as presented in Wang, Zhang & Yuan's monograph):* Budget-constrained KPI maximization solved by a Lagrangian and calculus of variations. Under first-price cost c(b) = b and market-price density p_z(z) = l/(l+z)², the winning function is **w(b) = b/(b+l)**. The optimal ("ORTB") bid is b(r) = √(u(r)·l/λ + l²) − l, which is non-linear in CTR.
  - "One can tune the parameter l to alter the winning probability so as to fit different market environments." — [Monograph arXiv 1610.03013](https://arxiv.org/abs/1610.03013)
  - *Relation:* The focal q_θ(b) = b/(b+θ) with pay-b-on-win is precisely ORTB's first-price model with l = θ. The focal paper effectively makes ORTB's market parameter unknown (binary) and learns it online. This should be cited explicitly. **Overlap: High** (model primitive).
- **Wang, J., Zhang, W., & Yuan, S. (2017). "Display Advertising with Real-Time Bidding (RTB) and Behavioural Targeting." arXiv 1610.03013.** The venue is believed to be *Foundations and Trends in Information Retrieval* (**unverified**). — [arXiv](https://arxiv.org/abs/1610.03013)
  - *Content:* Win and loss data in RTB are right-censored. Bid landscapes are learned with log-normal trees, censored regression, and Kaplan–Meier survival models (Amin et al. 2012; Zhang et al. 2016 KDD). Also covers multi-campaign statistical arbitrage, where a meta-bidder samples among M campaigns under one budget (Zhang & Wang 2015 KDD), and budget pacing. — [arXiv](https://arxiv.org/abs/1610.03013)
  - *Relation:* The probing agent's win-count-only learning is the censored-feedback case. Multi-campaign arbitrage is an early "one budget, many campaigns" RTB model. **Overlap: Medium.**

**(b) Budget split across campaigns, channels or platforms with learning**
- **Deng, Y., Golrezaei, N., Jaillet, P., Liang, J. C. N., & Mirrokni, V. (2023). "Multi-channel Autobidding with Budget and ROI Constraints." ICML 2023 (PMLR); arXiv 2302.01523.** — [arXiv](https://arxiv.org/abs/2302.01523); [Survey summary](https://arxiv.org/abs/2408.07685)
  - *Model:* An advertiser buys on multiple channels (e.g., Google Ads, Meta). Each channel's autobidder procures "through automated blackbox algorithms." The advertiser's only levers are a per-channel budget and a per-channel target ROI. — [arXiv](https://arxiv.org/abs/2302.01523)
  - *Results:*
    - Optimizing only per-channel ROIs can be "arbitrarily worse" than the global optimum.
    - Optimizing only per-channel budgets achieves the global optimum (Theorem 3.3).
    - Under bandit feedback (observe only each channel's total conversion and spend), the SGD-UCB algorithm learns per-channel budgets with O(T^{-1/3}) accuracy. — [arXiv](https://arxiv.org/abs/2302.01523)
  - *Relation:* The closest ad-tech analogue of "a planner allocating budget across autonomous agent teams." Differences: Deng et al. learn the split across repeated periods and channels are black boxes. The focal planner commits ex ante, teams learn internally via ETC, and value heterogeneity drives skew. **Overlap: High.** It is very likely to be cited by OM/MS reviewers.
- **Avadhanula, V., Colini-Baldeschi, R., Leonardi, S., Sankararaman, K. A., & Schrijvers, O. (2021). "Stochastic Bandits for Multi-platform Budget Optimization in Online Advertising." WWW '21 (venue per search summary; proceedings pages **unverified**); arXiv 2103.10246.** — [arXiv](https://arxiv.org/abs/2103.10246)
  - *Model:* Spend one campaign budget B over T rounds across m platforms with unknown values. Second-price auctions. Bandits with knapsacks over bid m-tuples. — [arXiv](https://arxiv.org/abs/2103.10246)
  - *Results:*
    - Discrete bids: regret O(OPT·√(mn/B) + √(mn·OPT)).
    - Continuous bids: Õ(m^{1/3}·min{B^{2/3}, (mT)^{2/3}}).
    - Near-matching lower bounds.
    - On Facebook data it beats UCB and LuekerLearn baselines, and spends the budget uniformly rather than exhausting it early.
    - The algorithm starts with an explicit initial exploration phase, bidding each b_i on all platforms. — [arXiv](https://arxiv.org/abs/2103.10246)
  - *Relation:* **Overlap: Medium-High.**
- **Nuara, A., Trovò, F., Gatti, N., & Restelli, M. (2018). "A Combinatorial-Bandit Algorithm for the Online Joint Bid/Budget Optimization of Pay-per-Click Advertising Campaigns." *Proceedings of AAAI-18*, pp. 2379–2386. DOI 10.1609/aaai.v32i1.11888.** — [AAAI PDF](https://cdn.aaai.org/ojs/11888/11888-13-15416-1-2-20201228.pdf); [mlanthology](https://mlanthology.org/aaai/2018/nuara2018aaai-combinatorial)
  - *Model and results:* Bids and daily budgets jointly across sub-campaigns. Gaussian processes estimate the click and cost curves, Bayesian bandits handle exploration, and dynamic programming solves a multiple-choice knapsack each day (the AdComB algorithm). — [mlanthology](https://mlanthology.org/aaai/2018/nuara2018aaai-combinatorial)
  - Journal extension: **Nuara, A., Trovò, F., Gatti, N., & Restelli, M. (2022). "Online joint bid/daily budget optimization of Internet advertising campaigns." *Artificial Intelligence* 305:103663; arXiv 2003.01452.** Avadhanula et al. describe it as an O(√T)-regret combinatorial semi-bandit that "does static budget optimization in each single round." — [arXiv](https://arxiv.org/abs/2003.01452); [Avadhanula et al.](https://arxiv.org/abs/2103.10246)
  - *Relation:* Budget split across learning sub-campaigns, solved by a planner each day. **Overlap: Medium-High.**
- **Han, B., & Arndt, C. (2021). "Budget Allocation as a Multi-Agent System of Contextual & Continuous Bandits." KDD 2021, pp. 2937–2945.** Bibliography verified. Content is known only secondhand: a contextual-bandit system using augmented data from a global model to share information across ad lines, as described by Ge et al. 2024 (**content unverified**). — [dblp](https://dblp.dagstuhl.de/rec/conf/kdd/HanA21.html)
  - *Relation:* A "multi-agent" framing of budget allocation. Worth checking for the agent-teams narrative. **Overlap: Medium** (provisional).
- **Ge, L., Xu, Y., Chu, J., Cramer, D., Li, F., Paulson, K., & Song, R. (2024). "Multi-Task Combinatorial Bandits for Budget Allocation." arXiv 2409.00561 (Amazon).** Venue **unverified**. — [arXiv](https://arxiv.org/abs/2409.00561)
  - Budget allocation across ad lines as a multi-task combinatorial bandit. **Overlap: Medium** (title/abstract-level).
- **Susan, F., Golrezaei, N., & Schrijvers, O. (2023). "Multi-platform budget management in ad markets with non-IC auctions." arXiv 2306.07352** (cited in the Aggarwal et al. survey; not read). — [Survey](https://arxiv.org/abs/2408.07685)
- 2025–2026 arXiv items found by discovery (title/abstract-level only; **Overlap: Low-Medium**):
  - "Adaptive Budget Optimization for Multichannel Advertising Using Combinatorial Bandits" (Sony/EPFL, 2502.02920) — [alphaXiv](https://www.alphaxiv.org/abs/2502.02920)
  - "DARA: Few-shot Budget Allocation in Online Advertising via In-Context Decision Making with RL-Finetuned LLMs" (2601.14711), relevant to the LLM-agent framing — [arXiv](https://arxiv.org/abs/2601.14711)
  - "HiBid: A Cross-Channel Constrained Bidding System with Budget Allocation by Hierarchical Offline Deep Reinforcement Learning" (2312.17503) — [alphaXiv](https://www.alphaxiv.org/abs/2312.17503)
  - "AdCoEvo: A Co-Evolving Multi-Agent Advertising Delivery System" (2610.19454) — [alphaXiv](https://www.alphaxiv.org/abs/2610.19454)

**(c) Budget pacing, equilibrium, coordination of pacing modules**
- **Balseiro, S. R., Besbes, O., & Weintraub, G. Y. (2015). "Repeated Auctions with Budgets in Ad Exchanges: Approximations and Design." *Management Science* 61(4):864–884.** — [RePEc](https://econpapers.repec.org/RePEc:inm:ormnsc:v:61:y:2015:i:4:p:864-884)
  - *Results:* Fluid mean-field equilibrium (FMFE). Each auction involves only a small fraction of a large advertiser population, so a bidder faces a stationary competition distribution. FMFE approximates rational behavior well. Ignoring budgets in reserve-price setting can cost the publisher significant profit. Optimal bids take the form b = v/(1+α_B), as described in the survey. — [RePEc](https://econpapers.repec.org/RePEc:inm:ormnsc:v:61:y:2015:i:4:p:864-884); [Survey](https://arxiv.org/abs/2408.07685)
  - *Relation:* Justifies treating competition θ as an exogenous, stationary state. **Overlap: Medium-Low.**
- **Balseiro, S. R., & Gur, Y. (2019). "Learning in Repeated Auctions with Budgets: Regret Minimization and Equilibrium." *Management Science* 65(9):3952–3968. DOI 10.1287/mnsc.2018.3174.** — [RePEc](https://econpapers.repec.org/RePEc:inm:ormnsc:v:65:y:2019:i:9:p:3952-3968)
  - *Results:* Adaptive pacing via dual gradient descent: bid v/(1+α), with α updated by the spend gap B/m − p. Regret is O(√m) in stochastic settings, with an asymptotically optimal competitive ratio under adversarial bids. Approximate Nash equilibrium when all bidders pace, with convergence under monotonicity. — [RePEc](https://econpapers.repec.org/RePEc:inm:ormnsc:v:65:y:2019:i:9:p:3952-3968); [Survey](https://arxiv.org/abs/2408.07685)
  - *Relation:* The exploitation agent's "constant budget-paced bid" is the static analogue. Reviewers may ask why not adaptive pacing, which learns implicitly. **Overlap: Medium.**
- Further references, all cited in the Aggarwal et al. survey reference list (not read in full). — [Survey](https://arxiv.org/abs/2408.07685)
  - Balseiro, Kim, Mahdian & Mirrokni (2021), "Budget-Management Strategies in Repeated Auctions," *Operations Research* 69(3):859–876.
  - Balseiro, Lu & Mirrokni (2023), "The Best of Many Worlds: Dual Mirror Descent for Online Allocation Problems," *Operations Research* 71(1):101–119.
  - Conitzer, Kroer, Sodomka & Stier-Moses (2022), "Multiplicative Pacing Equilibria in Auction Markets," *Operations Research* 70(2):963–989.
  - Gaitonde, Li, Light, Lucier & Slivkins (2023), "Budget Pacing in Repeated Auctions: Regret and Efficiency without Convergence," ITCS 2023 (arXiv 2205.08674).
  - Lucier, Pattathil, Slivkins & Zhang (2024), "Autobidders with Budget and ROI Constraints: Efficiency, Regret, and Pacing Dynamics," COLT 2024 (arXiv 2301.13306).
  - These are mostly multi-agent welfare and dynamics papers. **Overlap: Low.**
  - Conitzer et al.'s first-price-specific *Management Science* paper ("Pacing equilibrium in first price auction markets," 2022) was **not verified** in this session.
- **Balseiro, S. R., Bhawalkar, K., Feng, Z., Lu, H., Mirrokni, V., Sivan, B., & Wang, D. (2023). "Joint feedback loop for spend and return-on-spend constraints." arXiv 2302.08530.** As summarized in the survey: a fully decoupled sequential pacing design "could lead to poor performance and constraints violations," while a minimally coupled design that runs services independently "can achieve similar performance to the optimal, fully-coupled algorithm." — [Survey](https://arxiv.org/abs/2408.07685)
  - *Relation:* Evidence on modular, separate agents vs integrated control. It is relevant to the focal paper's division of labor between the probing and exploitation agents. **Overlap: Medium-Low.**

**(d) Learning to bid in first-price auctions (with and without budgets)**
- **Han, Y., Zhou, Z., & Weissman, T. "Optimal No-regret Learning in Repeated First-price Auctions." arXiv 2003.09795 (2020); listed as *Operations Research* (2024) in the survey (volume/pages **unverified**).** — [arXiv](https://arxiv.org/abs/2003.09795); [Survey](https://arxiv.org/abs/2408.07685)
  - *Results (as summarized by Wang et al. 2023):* One-sided feedback (winning bid revealed). Exploits graph-feedback and partial-order structure to achieve Õ(√T) regret, with an Ω(√T) lower bound even under full information. Wang et al. also note Balseiro et al. (2019): binary win/loss feedback gives Θ̃(T^{2/3}). — [Wang et al. 2023](https://arxiv.org/abs/2304.13477)
  - *Relation:* Binary win/loss feedback is exactly the focal probing signal. The T^{2/3} benchmark shows how hard learning from win counts alone is. **Overlap: Medium.**
- **Wang, Q., Yang, Z., Deng, X., & Kong, Y. (2023). "Learning to Bid in Repeated First-Price Auctions with Budgets." ICML 2023, PMLR pp. 36494–36513; arXiv 2304.13477.** — [arXiv](https://arxiv.org/abs/2304.13477)
  - *Model:* i.i.d. values and competing bids. Budget ρT. Full or one-sided feedback.
  - *Results:*
    - A dual-based algorithm with Õ(√T) regret in both feedback models; the one-sided case needs a density assumption.
    - Uses value shading v/(1+λ) and online gradient descent on λ.
    - Example 4.1: with U(0,1) values and competing bids, the budget constraint does not bind if ρ ≥ 1/12. "A seemingly 'tight' constraint is necessary for budget management to be of even the least use." — [arXiv](https://arxiv.org/abs/2304.13477)
  - *Relation:* The single-team, adaptive alternative to ETC. Example 4.1 parallels the focal "bounded budget window": with loose budgets, budget-aware learning adds nothing. **Overlap: Medium.**
- Also cited in the survey and in Wang et al.:
  - Ai et al. (2022), "No-regret learning in repeated first-price auctions with budget constraints," arXiv 2205.14572.
  - Badanidiyuru et al. on contextual first-price auctions (cited by Wang et al. as 2021; the WWW 2023 venue is **unverified**).
  - — [Survey](https://arxiv.org/abs/2408.07685); [Wang et al.](https://arxiv.org/abs/2304.13477)
- 2025–2026 budget-constrained first-price learning (abstract-level; **Overlap: Medium-Low**):
  - "Plan-Driven Adaptive Bidding for First-Price Auctions with Budget Constraints under Nonstationarity" (HKUST, 2505.02796)
  - "Online Bidding for Contextual First-Price Auctions with Budgets under One-Sided Information Feedback" (2603.07207)
  - "Adaptive Bidding Policies for First-Price Auctions with Budget Constraints under Non-stationarity" (2604.03103)
  - "Learning to Bid with Unknown Private Values in Budget-Constrained First-Price Auctions" (2605.09448)
  - "Optimally Pacing Budget Spending and Learning" (Princeton/Google, 2610.11074)
  - — [alphaXiv 2505.02796](https://www.alphaxiv.org/abs/2505.02796); [2603.07207](https://www.alphaxiv.org/abs/2603.07207); [2604.03103](https://www.alphaxiv.org/abs/2604.03103); [2605.09448](https://www.alphaxiv.org/abs/2605.09448); [2610.11074](https://www.alphaxiv.org/abs/2610.11074)

**(e) Budget-limited bandits in sponsored search and RTB** (all as described in Avadhanula et al. 2021) — [arXiv](https://arxiv.org/abs/2103.10246)
- Amin et al. (2012) formulate budget-constrained bidding as an MDP with censored observations and a product-limit estimator. Full title **unverified** here; commonly cited as UAI 2012.
- Tran-Thanh et al. (2014, UAI) prove O(√(CB)) regret for "online bid optimisation in budget-limited sponsored search auctions."
- Flajolet & Jaillet (2017) use probabilistic bisection with UCB for O(√T) regret when B = Θ(T). Exact title **unverified**.
- *Relation:* Single-campaign budget-constrained learning. **Overlap: Medium.**

**(f) Surveys and the authors' own prior work**
- **Choi, H., Mela, C. F., Balseiro, S. R., & Leary, A. (2020). "Online Display Advertising Markets: A Literature Review and Future Directions." *Information Systems Research* 31(2):556–575. DOI 10.1287/isre.2019.0902.** Organizes the display-ad literature by ecosystem agents, drawing on IS, marketing, economics, OM and CS. — [RePEc](https://econpapers.repec.org/RePEc:inm:orisre:v:31:y:2020:i:2:p:556-575)
  - *Relation:* The natural ISR anchor for WITS/ISR positioning. **Overlap: Low-Medium.**
- **Aggarwal, G., Badanidiyuru, A., Balseiro, S. R., Bhawalkar, K., Deng, Y., Feng, Z., Goel, G., Liaw, C., Lu, H., Mahdian, M., Mao, J., Mehta, A., Mirrokni, V., Paes Leme, R., Perlroth, A., Piliouras, G., Schneider, J., Schvartzman, A., Sivan, B., Spendlove, K., Teng, Y., Wang, D., Zhang, H., Zhao, M., Zhu, W., & Zuo, S. (2024). "Auto-bidding and Auctions in Online Advertising: A Survey." arXiv 2408.07685 (Google).** — [arXiv](https://arxiv.org/abs/2408.07685)
  - Covers bidding algorithms (pacing, first-price learning), equilibria and PoA, auction design, and "multi-channel" bidding.
  - Includes a principal–agent model in which an advertiser's "decision department (the principal)" sets goals for an "execution department (the agent) with slightly misaligned goals." This is useful for the agent-teams framing.
  - *Relation:* **Overlap: Low-Medium.**
- **Mookerjee, R., Kumar, S., & Mookerjee, V. S. (2017). "Optimizing Performance-Based Internet Advertisement Campaigns." *Operations Research* 65(1):38–54. DOI 10.1287/opre.2016.1553.** (One RePEc URL labels the year 2018.) — [IDEAS](https://ideas.repec.org/a/inm/oropre/v65y2017i1p38-54.html); [INFORMS](https://pubsonline.informs.org/doi/fpi/10.1287/opre.2016.1553)
  - Chitika case. Predicts click probability and uses a threshold to decide whether to show the ad, maximizing revenue under a CTR constraint. A static solution is optimal with known parameters. A rolling-horizon re-solve does better when parameters are estimated. Deployed in real time. — [IDEAS](https://ideas.repec.org/a/inm/oropre/v65y2017i1p38-54.html)
  - *Relation:* The co-author's prior OR paper. Reviewers who know the group will expect it cited, and the "static vs re-solve with estimates" theme parallels "no-learning vs learning." **Overlap: Medium.**
  - No prior Zhu–Mookerjee RTB paper was found in searches.

### Inferences
- **Citation hook:** state that the model "adopts the ORTB winning function w(b) = b/(b+l) of Zhang, Yuan & Wang (2014) under first-price payment, and treats the market parameter l = θ as unknown." This connects the paper to a well-cited RTB model and makes the novelty precise: learning l.
- **Expected reviewer comparisons to Deng et al. (2023):**
  - Their key result is that per-channel budgets suffice for global optimality. The focal paper similarly uses budgets as the planner's only lever.
  - Their learning happens at the planner level across periods. The focal learning happens within teams via ETC.
  - Their result has no "learning-threshold" skew because it lacks value heterogeneity and a fixed learning cost.
- Reviewers may suggest that each exploitation agent use Balseiro–Gur-style adaptive pacing, which learns about competition implicitly through spend feedback. A response could note that the planner's ex ante allocation needs V(a) in closed form.

### Gaps
- No paper was found that combines (i) ex ante budget allocation by a planner across multiple learners, (ii) heterogeneous impression values across learners, and (iii) within-learner explore-then-commit in first-price auctions with unknown competition. Each verified paper covers at most two of the three.
- Han & Arndt (2021) and Ge et al. (2024) were not read in full; their exact algorithms and results are unverified.

## Q6. Dynamic pricing with learning: learning-and-earning, explore-then-exploit, finite/binary hypotheses, multi-product with shared resources

### Takeaway
The OM pricing literature contains the closest structural cousins of the focal model:
- Besbes & Zeevi (2009): explicit ETC policies (a learning phase of length τ, then a fixed price) under an inventory constraint. Near-optimal in rate, but not rate-optimal.
- Harrison, Keskin & Zeevi (2012): a **binary prior** over two demand curves. Myopic Bayesian pricing can suffer incomplete learning at an "uninformative price," so forced experimentation is needed.
- Cheung, Simchi-Levi & Wang (2017): with a finite set of demand hypotheses and at most m price changes, regret is of order log^{(m)} T (m-fold iterated log). A strong argument that very few switches suffice when hypotheses are finite and separated.

### Cited Findings
- **Besbes, O., & Zeevi, A. (2009). "Dynamic Pricing Without Knowing the Demand Function: Risk Bounds and Near-Optimal Algorithms." *Operations Research* 57(6):1407–1420. DOI 10.1287/opre.1080.0640.** — [RePEc](https://econpapers.repec.org/RePEc:inm:oropre:v:57:y:2009:i:6:p:1407-1420); [WP PDF](https://faculty.wharton.upenn.edu/wp-content/uploads/2008/06/Dp_wo_demand_risk_ob_az_posted.pdf)
  - *Model:* Single product with initial inventory x over horizon T. Unknown demand function, either parametric or nonparametric. Asymptotic regime n → ∞. — [WP PDF](https://faculty.wharton.upenn.edu/wp-content/uploads/2008/06/Dp_wo_demand_risk_ob_az_posted.pdf)
  - *Algorithm:* "divided into two main stages. A 'learning' phase (exploration) of length τ is first used, in which κ prices are tested. Then a 'pricing' phase (exploitation) fixes a 'good' price." — [WP PDF](https://faculty.wharton.upenn.edu/wp-content/uploads/2008/06/Dp_wo_demand_risk_ob_az_posted.pdf)
  - *Rates (relative regret):*
    - Nonparametric: O((log n)^{1/2} n^{−1/4}) with τ_n ≍ n^{−1/4}.
    - Parametric: O((log n)^{1/2} n^{−1/3}) with τ_n ≍ n^{−1/3}.
    - Lower bound: C′/n^{1/2}.
    - With a single unknown parameter, a multi-step policy reaches the lower bound up to logs.
    - The paper interprets regret as "the economic value of prior knowledge on the demand function." — [WP PDF](https://faculty.wharton.upenn.edu/wp-content/uploads/2008/06/Dp_wo_demand_risk_ob_az_posted.pdf)
  - *Relation:* An ETC with a hard resource constraint, where the learning-phase length is a design variable optimized ex ante: the focal paper's τ. **Overlap: High.**
- **Harrison, J. M., Keskin, N. B., & Zeevi, A. (2012). "Bayesian Dynamic Pricing Policies: Learning and Earning Under a Binary Prior Distribution." *Management Science* 58(3):570–586. DOI 10.1287/mnsc.1110.1426.** — [RePEc](https://econpapers.repec.org/RePEc:inm:ormnsc:v:58:y:2012:i:3:p:570-586); [INFORMS](https://pubsonline.informs.org/doi/fpi/10.1287/mnsc.1110.1426)
  - *Model:* Sale/no-sale outcomes. The prior puts mass on two known demand curves, extendable to any finite prior. — [INFORMS](https://pubsonline.informs.org/doi/fpi/10.1287/mnsc.1110.1426)
  - *Results:*
    - Under the myopic Bayesian policy (MBP) "learning is passive," which can cause incomplete learning: prices converge to the uninformative price or to the optimal price, each with positive probability.
    - A constrained MBP keeps the expected gap to a clairvoyant bounded by a constant (under one added assumption).
    - Because firms cannot detect incomplete learning, myopic policies "need to be modified with some kind of forced price experimentation." — [INFORMS](https://pubsonline.informs.org/doi/fpi/10.1287/mnsc.1110.1426)
  - *Relation:* The closest OM model to binary θ with Bayesian learning. It supports deliberate probing over purely myopic, learn-while-doing behavior. Its uninformative-point mechanism is absent in the focal model; see the inference below. **Overlap: High.**
- **Keskin, N. B., & Zeevi, A. (2014). "Dynamic Pricing with an Unknown Demand Model: Asymptotically Optimal Semi-Myopic Policies." *Operations Research* 62(5):1142–1167. DOI 10.1287/opre.2014.1294.** — [RePEc](https://econpapers.repec.org/RePEc:inm:oropre:v:62:y:2014:i:5:p:1142-1167)
  - *Results:* Modifies greedy iterated least squares into "semi-myopic" policies that are asymptotically optimal. The smallest achievable regret is of order √T with unknown linear-demand parameters, and of order log T when expected demand at an incumbent price is known. One search snippet dropped the radical; a second snippet confirmed "order √T" for the first case. The log-T case is from the abstract as summarized and is not checked in the full text. — [RePEc](https://econpapers.repec.org/RePEc:inm:oropre:v:62:y:2014:i:5:p:1142-1167)
  - *Relation:* **Overlap: Medium.**
- **Broder, J., & Rusmevichientong, P. (2012). "Dynamic Pricing Under a General Parametric Choice Model." *Operations Research* 60(4):965–980. DOI 10.1287/opre.1120.1057.** — [RePEc](https://econpapers.repec.org/RePEc:inm:oropre:v:60:y:2012:i:4:p:965-980)
  - *Results:* Worst-case regret Θ(√T), with a maximum-likelihood-based policy achieving O(√T). Under a "well-separated" condition the optimal regret is Θ(log T). The √T lower bound comes from an "uninformative price" where all candidate demand curves intersect. The "MLE-cycle" policy name was not confirmed. — [RePEc](https://econpapers.repec.org/RePEc:inm:oropre:v:60:y:2012:i:4:p:965-980)
  - *Relation:* **Overlap: Medium.**
- **Cheung, W. C., Simchi-Levi, D., & Wang, H. (2017). "Technical Note—Dynamic Pricing and Demand Learning with Limited Price Experimentation." *Operations Research* 65(6):1722–1731. DOI 10.1287/opre.2017.1629.** — [MIT DSpace](https://dspace.mit.edu/handle/1721.1/119156); [RePEc](https://econpapers.repec.org/RePEc:inm:oropre:v:65:y:2017:i:6:p:1722-1731)
  - *Model:* The demand function belongs to a known **finite set**, and the seller may change price at most m times.
  - *Results:* Worst-case regret of order log^{(m)} T, i.e. m iterations of the logarithm. The exact notation was rendered ambiguously in the snippet, so check the PDF. Implemented at Groupon with significant revenue and bookings effects. — [MIT DSpace](https://dspace.mit.edu/handle/1721.1/119156)
  - *Relation:* With finite hypotheses (the focal θ is binary), very few switches suffice. This is a strong defense of a one-switch probe-then-commit protocol. **Overlap: High.**
- **Ferreira, K. J., Simchi-Levi, D., & Wang, H. (2018). "Online Network Revenue Management Using Thompson Sampling." *Operations Research* 66(6):1586–1602. DOI 10.1287/opre.2018.1755.** — [MIT DSpace](https://dspace.mit.edu/handle/1721.1/125757)
  - *Results:* Multiple products share limited inventories, with unknown demand parameters. Thompson sampling is combined with an LP to respect inventory constraints. Comes with guarantees and numerical gains, and extends to bandits with resource constraints. The paper compares itself with Besbes & Zeevi (2012, "Blind network revenue management," *Operations Research*; details **unverified**). — [MIT DSpace](https://dspace.mit.edu/handle/1721.1/125757)
  - *Relation:* The multi-product analogue: one shared resource across several learning sub-problems. It is a single integrated learner, not separate teams. **Overlap: Medium.**
- **Bastani, Simchi-Levi & Zhu (2022, *Management Science*)**: learning a shared prior across pricing experiments (see Q3). **Overlap: Medium-Low.** — [RePEc](https://econpapers.repec.org/RePEc:inm:ormnsc:v:68:y:2022:i:3:p:1865-1881)
- den Boer, A. V. (2015), "Dynamic pricing and learning: Historical origins, current research, and new directions," *Surveys in Operations Research and Management Science* 20(1):1–18. Bibliographic details are from memory and **unverified** in this session; it is the standard survey.

### Inferences
- **No uninformative bid in the focal model (my derivation, not from a source).** With q_θ(b) = b/(b+θ), for any b > 0 we have q_L(b) − q_H(b) = b(θH−θL)/[(b+θL)(b+θH)] > 0. The two win curves never cross, so there is no "uninformative bid" of the HKZ or Broder–Rusmevichientong type.
  - A myopic Bayesian (learn-while-doing) bidder therefore learns passively at any positive bid. This weakens the HKZ-style argument for forced probing.
  - A reviewer could argue that a greedy Bayesian bidder learns "for free." The authors need another rationale: informativeness per dollar, platform learning phases, or planner-level forecastability.
- **Most informative bid (my derivation).** The separation q_L(b) − q_H(b) is maximized at b* = √(θL·θH). Expected spend per period, b·q_θ(b), rises in b. So the "informative bid" generally differs from the budget-paced exploitation bid. This gives a concrete reason for a separate probing agent with its own bid. It is worth formalizing, e.g. via KL divergence per dollar.
- **Mapping to the pricing literature.** The focal planner's budget plays the role of Besbes & Zeevi's inventory x. Cheung et al.'s finite-hypothesis, limited-switch result is the right OM citation to argue that one switch (ETC) is near-optimal for binary θ. Garivier et al.'s factor-2 loss is the right citation for the residual inefficiency.

### Gaps
- No pricing paper was found in which separate learners (product teams) receive budget or inventory from a planner ex ante and each run ETC internally, with heterogeneous product values. Ferreira et al. and Besbes & Zeevi (2012) use a single coordinated learner.
- The exact regret statements of Cheung et al. (2017) and the details of Besbes & Zeevi (2012) were not checked in the full text.

## Q7. Targeted searches: "budget allocation across multiple learning campaigns", "portfolio of experiments", "allocating traffic across concurrent A/B tests", "learning phase budget"

### Takeaway
These phrases mostly surface:
- the experimentation-program literature: Azevedo et al. 2020; Sudijono et al. 2024; Schmit et al. 2019; Basu & Berman 2024/25;
- ad-tech budget-allocation bandits: Deng et al. 2023; Avadhanula et al. 2021; Nuara et al. 2018/2022; Han & Arndt 2021; Ge et al. 2024;
- platform cold-start design: Ye et al. 2023.

None formalizes a planner allocating budgets to independent learners whose learning has a fixed probing cost and a learning threshold.

### Cited Findings
- **"Portfolio of experiments" / experimentation programs.**
  - Sudijono et al. (2024) explicitly treat experimentation as a portfolio problem with a "metaproduction function," including multiple programs that share resources. — [arXiv](https://arxiv.org/abs/2412.05508)
  - Basu & Berman rank a portfolio of 2,766 A/B tests by expected lift per cost under FDR control. — [arXiv](https://arxiv.org/abs/2407.01036)
  - Azevedo et al. (2020) allocate users across ideas. — [IDEAS](https://ideas.repec.org/a/ucp/jpolec/doi10.1086-710607.html)
- **"Allocating traffic across concurrent A/B tests."**
  - Sudijono et al. note that "a unit may only be assigned to one test at a time, making the allocation pool a limited resource." — [arXiv](https://arxiv.org/abs/2412.05508)
  - Schmit et al. (2019) derive optimal sampling across many experiments. — [PMLR](https://proceedings.mlr.press/v89/schmit19a.html)
- **"Budget allocation across multiple learning campaigns."**
  - Deng et al. (2023): per-channel budgets learned under bandit feedback. — [arXiv](https://arxiv.org/abs/2302.01523)
  - Avadhanula et al. (2021): multi-platform bandits with knapsacks. — [arXiv](https://arxiv.org/abs/2103.10246)
  - Nuara et al. (2018/2022): joint bid and budget across sub-campaigns. — [mlanthology](https://mlanthology.org/aaai/2018/nuara2018aaai-combinatorial)
  - Ge et al. (2024): multi-task combinatorial bandits across ad lines. — [arXiv](https://arxiv.org/abs/2409.00561)
  - A targeted search for ISR/MISQ papers on bandit-based ad budget allocation (2021–2024) returned none. — [Search result: Ge et al. arXiv](https://arxiv.org/abs/2409.00561)
- **"Learning phase budget."**
  - Platform documentation (Google ≤ 7 days; TikTok about 25 results or 7 days; Meta about 50 events in 7 days, secondary) ties learning to event volume and hence budget. — [Google](https://support.google.com/google-ads/answer/13020501); [TikTok](https://ads.tiktok.com/help/article?aid=11234); [Lebesgue (secondary for Meta)](https://lebesgue.io/blog/facebook-ads-learning-phase/)
  - Ye et al. (2023, *Management Science*) is the peer-reviewed paper on designing a platform's cold-start allocation. — [INFORMS](https://pubsonline.informs.org/doi/fpi/10.1287/mnsc.2022.4550)

### Inferences
- The focal paper sits in an identifiable white space: experimentation-program allocation (economics/marketing) crossed with multi-channel autobidding budget allocation (OM/CS) crossed with ETC learning of competition (RTB).
- The cleanest positioning sentence would cite three anchors:
  1. Azevedo et al. (2020) / Sudijono et al. (2024) for "allocating a fixed learning resource across learners";
  2. Deng et al. (2023) for "allocating budgets to autonomous bidding agents";
  3. Feit & Berman (2019) for "ETC as a near-bandit-optimal, operationally simple protocol."
- The contribution would be the interaction: budget is both the learning resource and the exploitation resource, and values are heterogeneous.

### Gaps
- No academic paper studies optimal budgets with respect to platform learning-phase thresholds, e.g. "fund an ad set enough to exit learning." This is a gap the focal paper could claim, with care.
- IS-journal coverage (ISR/MISQ/JMIS) could not be exhaustively searched with the available tools.

## Q8. Closest 3–5 works and which ones WITS / ISR / Management Science reviewers would cite against or in support

### Takeaway
The closest works are, in order:
1. the Azevedo et al. (2020) / Azevedo–Mao–Montiel Olea–Velez (2023) / Sudijono et al. (2024) cluster, on the allocation mechanism;
2. Feit & Berman (2019), on ETC vs bandit;
3. Deng et al. (2023), on a planner splitting budget across bidding agents;
4. Harrison–Keskin–Zeevi (2012), Besbes–Zeevi (2009) and Cheung–Simchi-Levi–Wang (2017), on binary/finite-hypothesis learning-and-earning with limited switches;
5. Garivier–Kaufmann–Lattimore (2016) and Perchet et al. (2016), on ETC theory.

Expect Garivier et al. to be cited against ETC. Feit & Berman, Perchet et al. and Cheung et al. support it. Azevedo/Sudijono will be cited as prior art for the skewed-then-balanced allocation logic.

### Cited Findings
- **1. Azevedo et al. (2020, JPE) + Azevedo, Mao, Montiel Olea & Velez (2023, JET) + Sudijono et al. (2024, arXiv): Overlap High.**
  - They show S-shaped value of information, "go big" (all resources to one idea) when scarce and thin-tailed, and "go lean" when abundant. Sudijono's Theorem 1 states the equal-split-over-a-subset optimum. — [WP PDF](https://www.gwern.net/doc/statistics/decision/2019-azevedo.pdf); [AMOV WP](https://eduardomazevedo.github.io/papers/azevedo-et-al-ab-gaussian.pdf); [arXiv](https://arxiv.org/abs/2412.05508)
  - *Reviewer use:* likely **against novelty** of the allocation comparative statics: "this follows from non-concave value of information." Also usable **in support** as theoretical grounding. Most likely from Management Science or Marketing Science-trained reviewers.
- **2. Feit & Berman (2019, Marketing Science): Overlap High.**
  - Optimal test & roll is close to Thompson sampling (e.g., 0.22% vs 0.03%, 0.89% vs 0.29%, 1.68% vs 0.57% regret relative to perfect information). Both are O(√N). The gap grows with more arms. — [arXiv](https://arxiv.org/abs/1811.00457)
  - *Reviewer use:* **in support**. It is the standard answer to "why not a bandit," and WITS/ISR and marketing reviewers will expect it.
- **3. Deng, Golrezaei, Jaillet, Liang & Mirrokni (2023, ICML): Overlap High.**
  - Per-channel budgets to black-box autobidders achieve the global optimum, and the budgets are learnable with bandit feedback. — [arXiv](https://arxiv.org/abs/2302.01523)
  - *Reviewer use:* as the **closest competing formulation** of "planner allocates budget to bidding agents." OM/MS reviewers will ask for differentiation: ex ante vs repeated, value heterogeneity, internal ETC learning.
- **4. Harrison, Keskin & Zeevi (2012, MS); Besbes & Zeevi (2009, OR); Cheung, Simchi-Levi & Wang (2017, OR): Overlap High.**
  - Binary-prior Bayesian pricing with incomplete learning under myopic policies; ETC with a resource constraint; finite hypotheses with limited switches giving log^{(m)} T regret. — [INFORMS](https://pubsonline.informs.org/doi/fpi/10.1287/mnsc.1110.1426); [WP PDF](https://faculty.wharton.upenn.edu/wp-content/uploads/2008/06/Dp_wo_demand_risk_ob_az_posted.pdf); [MIT DSpace](https://dspace.mit.edu/handle/1721.1/119156)
  - *Reviewer use:* OR/MS (OM-department) reviewers will cite these in **mixed** fashion. HKZ and Cheung et al. support deliberate probing and few switches. Besbes & Zeevi show two-phase policies are near-optimal but not rate-optimal.
- **5. Garivier, Kaufmann & Lattimore (2016, NeurIPS) and Perchet, Rigollet, Chassang & Snowberg (2016, AoS): Overlap High** for the reviewer question.
  - ETC loses a factor of 2 asymptotically, and fixed design loses a factor of 4 versus SPRT-ETC when hypotheses are known. A few batches recover near-optimal minimax regret. — [arXiv](https://arxiv.org/abs/1605.08988); [arXiv](https://arxiv.org/abs/1505.00369)
  - *Reviewer use:* Garivier et al. **against** (likely from CS/OR-leaning reviewers). Perchet et al. **in support**.
- **Honorable mentions to cite defensively:**
  - Tran-Thanh et al. (2010, AAAI): ε-first, budget-limited bandits, the exact algorithmic precedent. — [AAAI](https://ojs.aaai.org/index.php/AAAI/article/view/7758)
  - Zhang, Yuan & Wang (2014, KDD): ORTB winning function b/(b+l), the model primitive. — [Monograph](https://arxiv.org/abs/1610.03013)
  - Ye et al. (2023, MS): platform cold-start / learning phase. — [INFORMS](https://pubsonline.informs.org/doi/fpi/10.1287/mnsc.2022.4550)
  - Waisman, Nair & Carrion (2025, MkSc): bandits inside RTB. — [RePEc](https://econpapers.repec.org/RePEc:inm:ormksc:v:44:y:2025:i:1:p:176-195)
  - Schwartz, Bradlow & Fader (2017, MkSc): batched bandits for display ads. — [RePEc](https://econpapers.repec.org/RePEc:inm:ormksc:v:36:y:2017:i:4:p:500-522)
  - Balseiro & Gur (2019, MS): adaptive pacing. — [RePEc](https://econpapers.repec.org/RePEc:inm:ormnsc:v:65:y:2019:i:9:p:3952-3968)
  - Choi, Mela, Balseiro & Leary (2020, ISR): the IS-venue survey anchor. — [RePEc](https://econpapers.repec.org/RePEc:inm:orisre:v:31:y:2020:i:2:p:556-575)
  - Mookerjee, Kumar & Mookerjee (2017, OR): the co-author's own learning-vs-static ad campaign paper. — [IDEAS](https://ideas.repec.org/a/inm/oropre/v65y2017i1p38-54.html)

### Inferences
- **Venue-specific expectations.**
  - WITS/ICIS/ISR reviewers are most likely to look for Choi et al. (2020 ISR), Feit & Berman (2019), Schwartz et al. (2017), Ye et al. (2023), and possibly Mookerjee et al. (2017).
  - Management Science reviewers are most likely to look for Azevedo et al. (2020), Harrison–Keskin–Zeevi (2012), Balseiro & Gur (2019), Balseiro–Besbes–Weintraub (2015), Ye et al. (2023) and Deng et al. (2023).
  - OR reviewers are most likely to look for Besbes & Zeevi (2009), Cheung et al. (2017) and Garivier/Perchet.
- **Suggested rebuttal structure for "why not a bandit?"**
  1. ETC is near-optimal in Bayesian expected profit at realistic scales (Feit & Berman). With binary θ and one switch, limited-experimentation theory gives very low regret (Cheung et al.). Few batches suffice (Perchet et al.).
  2. Platforms impose fixed learning windows (Google, TikTok, Meta documentation; Ye et al.).
  3. The planner needs an ex ante, closed-form team value function V(a) to allocate budgets. That is tractable under ETC but not under adaptive bandits.
  4. In RTB, probing consumes real budget. The informative bid (√(θLθH) by my derivation) generally differs from the paced bid, which justifies separate probing and exploitation agents.
  5. Acknowledge Garivier et al.'s factor-2 asymptotic loss. Optionally simulate a TS or adaptive-pacing team under the same budget accounting; the coordinator's tasks #2–3 appear to do this already.

### Gaps
- The search did not establish whether any 2025–2026 working paper (SSRN/arXiv) already studies "budget allocation across agentic AI bidding teams." The DARA (2601.14711) and AdCoEvo (2610.19454) LLM-agent ad papers were seen only at title level and should be checked by the agent-systems researcher.
- Reviewer predictions are judgment calls based on the citation patterns above, not on any data about the actual reviewers.
