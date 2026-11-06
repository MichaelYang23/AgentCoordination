# Multiple learners / multi-agent bandits ("teams of bandits") and how they differ from a planner splitting a budget across independent learning units

Scope note for the report writer. The paper being positioned is Yang, Zhu & Mookerjee, "Orchestrating Agent Teams: Budget Allocation in Real-Time Bidding" (WITS 2026 submission). Its setting: (a) a planner (the advertiser), (b) a fixed total budget T split ex ante across n independent "agent teams" (campaigns), (c) teams with different per-impression values v1 > v2, (d) a comparison of the learning value V(B) with a no-learning benchmark W(B), and (e) independent markets, one per team, each with its own unknown competition state θ. Each team runs explore-then-commit (ETC): a probing agent bids for τ periods, with τ fixed by the planner up front, then an exploitation agent bids a budget-paced constant bid from the Bayesian posterior.

Every entry below gives the citation, the model, the main result, its relation to the paper, and an overlap rating (High/Medium/Low). Citations were checked this session against Crossref DOIs, arXiv records and abstracts, PMLR volume indexes, the NeurIPS proceedings indexes, or publisher and RePEc pages. Content I am recalling rather than re-reading is marked "(recalled)". Anything I could not verify is marked "unverified" and repeated in the Gaps subsection of its section.

## Q1. Cooperative / distributed multi-agent bandits: what has been done, and how does it differ?

### Takeaway
Cooperative multi-agent bandits study many peers, usually on a communication graph or gossip network, all playing the same bandit instance. They share samples or estimates to reduce group or individual regret. The questions are about information pooling and communication, such as consensus, gossip, communication rounds and graph centrality. No paper in this strand has a planner, a shared spending budget, value-weighted agents or a learning-vs-no-learning allocation comparison. The paper's teams face independent markets, so they have nothing to share, and this machinery would only matter in an extension where the teams' competition states are correlated.

### Cited Findings
- **[Overlap: Low] Landgren, P., Srivastava, V., & Leonard, N. E. (2016a). "On distributed cooperative decision-making in multiarmed bandits." 2016 European Control Conference (ECC), pp. 243–248. DOI 10.1109/ECC.2016.7810293; arXiv:1512.06888.**
  - Model: N agents cooperatively play the same multi-armed bandit (MAB). The cooperative UCB algorithm interleaves (i) running-consensus estimation of rewards and (ii) UCB-based arm selection.
  - Result: performance analysis that characterizes how the communication-graph structure affects group decision-making.
  - Relation: the canonical "cooperative UCB over networks" reference. It assumes one shared environment and has no budget or planner.
  - [Crossref DOI](https://doi.org/10.1109/ecc.2016.7810293); [arXiv](https://arxiv.org/abs/1512.06888)
- **[Overlap: Low] Landgren, P., Srivastava, V., & Leonard, N. E. (2016b). "Distributed cooperative decision-making in multiarmed bandits: Frequentist and Bayesian algorithms." 2016 IEEE 55th Conference on Decision and Control (CDC), pp. 167–172. DOI 10.1109/CDC.2016.7798264; arXiv:1606.00911.**
  - Companion paper with frequentist and Bayesian cooperative algorithms. The arXiv revision notes a correction to the published version.
  - [Crossref DOI](https://doi.org/10.1109/cdc.2016.7798264); [arXiv](https://arxiv.org/abs/1606.00911)
- **[Overlap: Low] Landgren, P., Srivastava, V., & Leonard, N. E. (2020). "Distributed Cooperative Decision Making in Multi-agent Multi-armed Bandits." arXiv:2003.01312 (journal version unverified).**
  - Model: agents face the same MAB and share estimates over a fixed graph. Two reward models: unconstrained (agents on the same arm get independent rewards) and constrained (collisions give zero reward).
  - Algorithms: coop-UCB2 and coop-UCB2-selective-learning.
  - Result: group performance close to that of a centralized fusion center. It also proposes a "graph explore-exploit index" and a "nodal explore-exploit centrality" index that predict group and agent performance.
  - [arXiv abstract](https://arxiv.org/abs/2003.01312)
- **[Overlap: Low] Kolla, R. K., Jagannathan, K., & Gopalan, A. (2018). "Collaborative Learning of Stochastic Bandits Over a Social Network." IEEE/ACM Transactions on Networking 26(4):1782–1795. DOI 10.1109/TNET.2018.2852361; arXiv:1602.08886. Earlier version: Allerton 2016, pp. 1228–1235.**
  - Model: agents on a social network play a stochastic MAB, and each agent's reward is observed by its neighbours.
  - Result: "non-altruistic and individually consistent" policies can suffer large regret on networks. A dominating-set algorithm exploits network structure, and in a star network the hub serves as an "information sink".
  - Relation: a "leader learns, followers benefit" structure. The leader is not a budget-allocating planner.
  - [Crossref (ToN)](https://doi.org/10.1109/tnet.2018.2852361); [arXiv](https://arxiv.org/abs/1602.08886)
- **[Overlap: Low] Martínez-Rubio, D., Kanade, V., & Rebeschini, P. (2019). "Decentralized Cooperative Stochastic Bandits." NeurIPS 2019. arXiv:1810.04468.**
  - Model: K arms on a network of N agents with identical reward distributions. Each agent pulls an arm and messages its neighbours each round.
  - Algorithm: accelerated-consensus delayed estimates combined with a UCB index (DDUCB).
  - Result: regret is at most the optimal centralized regret plus a term that depends on the spectral gap of the communication matrix.
  - [arXiv abstract](https://arxiv.org/abs/1810.04468); [NeurIPS 2019 proceedings index](https://papers.nips.cc/paper_files/paper/2019)
- **[Overlap: Low] Szörényi, B., Busa-Fekete, R., Hegedűs, I., Ormándi, R., Jelasity, M., & Kégl, B. (2013). "Gossip-based distributed stochastic bandit algorithms." ICML 2013, PMLR 28(3):19–27.**
  - Model (recalled): peers in a P2P network solve a common stochastic bandit and exchange information by gossip.
  - [PMLR v28 index (title, authors, pages verified)](https://proceedings.mlr.press/v28/)
- **[Overlap: Low–Medium] Hillel, E., Karnin, Z., Koren, T., Lempel, R., & Somekh, O. (2013). "Distributed Exploration in Multi-Armed Bandits." NIPS 2013. arXiv:1311.0800.**
  - Model: k players collaborate to identify an ε-optimal arm.
  - Result: with one communication round they learn √k times faster than a single player, and a lower bound shows this is in general best possible. An algorithm reaching the ideal k-fold speed-up needs communication only logarithmic in 1/ε.
  - Relation: closest in spirit to "parallel teams that probe and then pool". It is pure exploration in one shared environment, and the k samplers split exploration work rather than a spending budget.
  - [arXiv abstract](https://arxiv.org/abs/1311.0800); [NeurIPS 2013 index](https://papers.nips.cc/paper_files/paper/2013)
- **[Overlap: Low] Tao, C., Zhang, Q., & Zhou, Y. (2019). "Collaborative Learning with Limited Interaction: Tight Bounds for Distributed Exploration in Multi-armed Bandits." FOCS 2019, pp. 126–146. DOI 10.1109/FOCS.2019.00017; arXiv:1904.03293.**
  - Model: distributed best-arm identification with multiple agents under limited interaction (communication steps).
  - Result: almost tight round–speedup trade-offs, plus new lower-bound techniques for communication steps under time or confidence constraints.
  - [arXiv abstract](https://arxiv.org/abs/1904.03293); [Crossref DOI](https://doi.org/10.1109/focs.2019.00017)
- **[Overlap: Low] Sankararaman, A., Ganesh, A., & Shakkottai, S. (2019). "Social Learning in Multi Agent Multi Armed Bandits." Proc. ACM Meas. Anal. Comput. Syst. / SIGMETRICS 2020 abstract (ACM SIGMETRICS Perf. Eval. Rev. 48(1):29–30, DOI 10.1145/3410048.3410065); arXiv:1910.02100.**
  - Model: n agents solve the same K-armed instance. They gossip only arm IDs, not samples, through a pairwise asynchronous protocol.
  - Result: per-agent regret O(((⌈K/n⌉+log n)/Δ)·log T + log³(n)·loglog(n)/Δ²), with Θ(log T) communications per agent. Regret falls sharply compared with no collaboration.
  - [arXiv abstract](https://arxiv.org/abs/1910.02100); [Crossref](https://doi.org/10.1145/3410048.3410065)
- **[Overlap: Low] Chawla, R., Sankararaman, A., Ganesh, A., & Shakkottai, S. (2020). "The Gossiping Insert-Eliminate Algorithm for Multi-Agent Bandits." AISTATS 2020, PMLR 108. arXiv:2001.05452.**
  - Result: with Ω(log T) gossip communications, every agent's regret is a factor of order N smaller than without collaboration. Communication constraints have only a second-order effect.
  - [arXiv abstract](https://arxiv.org/abs/2001.05452); [PMLR v108 index](https://proceedings.mlr.press/v108/)
- **[Overlap: Low] Chakraborty, M., Chua, K. Y. P., Das, S., & Juba, B. (2017). "Coordinated Versus Decentralized Exploration In Multi-Agent Multi-Armed Bandits." IJCAI 2017, pp. 164–170. DOI 10.24963/ijcai.2017/24.**
  - Model: team agents either pull an arm or broadcast their reward, under limited communication.
  - Result: a value-of-information-based decentralized communication strategy that approaches a centralized benchmark. The paper uses "team" vocabulary but has no budget.
  - [Crossref DOI](https://doi.org/10.24963/ijcai.2017/24); [IJCAI page](https://www.ijcai.org/proceedings/2017/24)
- **[Overlap: Low] Bıyık, E., Lalitha, A., Saha, R., Goldsmith, A., & Sadigh, D. (2022). "Partner-Aware Algorithms in Decentralized Cooperative Bandit Teams." AAAI 2022 (per arXiv comment). arXiv:2110.00751.**
  - Model: a decentralized MAB with coupled team rewards.
  - Result: naive single-agent algorithms fail, while a partner-aware UCB achieves logarithmic regret.
  - Relation: "bandit teams" in name only. There is no planner or budget.
  - [arXiv](https://arxiv.org/abs/2110.00751)
- **[Overlap: Low–Medium] Chawla, R., Vial, D., Shakkottai, S., & Srikant, R. (2023). "Collaborative Multi-Agent Heterogeneous Multi-Armed Bandits." ICML 2023, PMLR 202. arXiv:2305.18784.**
  - Model: N agents, each learning one of M different stochastic bandits, minimize group cumulative regret.
  - Result: decentralized algorithms with per-agent and group regret bounds and near-matching lower bounds.
  - Relation: the cooperative work closest to "independent environments", but the agents still collaborate on overlapping instances and there is no budget.
  - [arXiv abstract](https://arxiv.org/abs/2305.18784); [PMLR v202 index](https://proceedings.mlr.press/v202/)
- **[Overlap: Low] Barnea, I., Lancewicki, T., & Mansour, Y. (2025). "Individual Regret in Cooperative Stochastic Multi-Armed Bandits." NeurIPS 2025 (Advances in NeurIPS 38, pp. 89817–89871), DOI 10.52202/085713-2706.**
  - Recent evidence that the strand is still active on individual-regret guarantees. Content not read beyond the title.
  - [Crossref record](https://doi.org/10.52202/085713-2706)
- **[Overlap: Medium–Low] Afsharrad, A., Oftadeh, P., Moradipari, A., & Lall, S. (2025). "Cooperative Multi-Agent Constrained Stochastic Linear Bandits." 2025 American Control Conference (ACC), pp. 3614–3621. DOI 10.23919/ACC63710.2025.11107780.**
  - Model (as summarized by the search tool from its arXiv version): a network of agents maximizes welfare while keeping total cost below a known threshold.
  - Relation: a shared cost constraint across learning agents, partial (b). There is no planner allocating budgets or values. The match to arXiv:2410.17382 is my inference.
  - [Crossref DOI](https://doi.org/10.23919/acc63710.2025.11107780); [arXiv PDF (as returned by search)](https://arxiv.org/pdf/2410.17382)
- **Surveys.**
  - **Boursier, E., & Perchet, V. (2024). "A survey on multi-player bandits." Journal of Machine Learning Research (arXiv:2211.16275, final version "accepted at JMLR").** It organizes the multiplayer bandit literature, driven mostly by cognitive radio, and notes that current algorithms are "far from applicable" to real networks. [arXiv abstract](https://arxiv.org/abs/2211.16275); [IP Paris record](https://researchportal.ip-paris.fr/en/publications/a-survey-on-multi-player-bandits/)
  - Web and alphaXiv searches for a 2022–2026 survey on cooperative or federated multi-agent bandits returned only the Boursier–Perchet multi-player survey and a decentralized-MARL survey (Jiang, Su & Lu, arXiv:2401.04934, which covers RL rather than bandits). [arXiv 2401.04934](https://www.arxiv.org/abs/2401.04934); [Boursier–Perchet HTML](https://arxiv.org/html/2211.16275v2)

### Inferences
- Checklist for this strand:
  - (a) Planner/coordinator: No. Agents are peers, and the closest analog is a centralized "fusion center" used only as a performance benchmark (Landgren et al. 2020).
  - (b) Shared budget split among learners: No. Each agent has its own horizon. Tao et al. constrain communication rounds, not spending.
  - (c) Different values/weights: No. Agents are symmetric, and Chawla et al. (2023) add heterogeneous instances only.
  - (d) With vs. without learning: No. The comparison is "collaboration vs. no collaboration", which is the value of pooling information, not the value of learning.
  - (e) Environment: shared (the same instance), except Chawla et al. (2023).
- What a reviewer may say is "multiple bandit learners has been done" is a different object. In this strand, learners add value by pooling samples about a common unknown. In the paper, learners add value by adapting to their own unknown θ_i, and the planner's lever is how much budget, and hence probing, each one gets.
- Possible bridge: if the competition states θ_1, θ_2 were correlated, for example a common market-wide factor, then cross-team sharing of probe outcomes would create value. The paper would then inherit cooperative-MAB results and free-riding issues (see Q6).

### Gaps
- Journal version of Landgren et al. (2020, arXiv:2003.01312) not verified.
- Szörényi et al. (2013): model details are recalled; only title, authors, venue and pages were verified.
- The arXiv:2410.17382 ↔ Afsharrad et al. (ACC 2025) correspondence is inferred from the search-tool summary.
- No 2022–2026 survey dedicated to cooperative or federated MAB was found. One may exist outside the indexes searched.

## Q2. Multi-player bandits with collisions: what has been done, and how does it differ?

### Takeaway
Multi-player MAB, motivated by cognitive radio, studies decentralized players who share arms as congestible resources: colliding players get zero reward. The benchmark is the centralized optimal assignment of players to arms, and the work centres on coordinating without communication. Several algorithms have an explore-then-commit structure (Musical Chairs, SIC-MMAB phases). There are heterogeneous player-specific values (Kalathil et al. 2014; Bistritz & Leshem 2018/2021). There is no planner budget and no learning-vs-no-learning comparison, and the environment is shared, the opposite of the paper's independent markets.

### Cited Findings
- **[Overlap: Low] Liu, K., & Zhao, Q. (2010). "Distributed Learning in Multi-Armed Bandit With Multiple Players." IEEE Transactions on Signal Processing 58(11):5667–5681. DOI 10.1109/TSP.2010.2062509; arXiv:0910.2065.**
  - Model: M players compete for N arms, and colliding players get no reward or share it.
  - Result: decentralized system regret can reach the same logarithmic order as the centralized counterpart, using the Time-Division Fair Sharing (TDFS) policy, with a matching lower bound for a class of decentralized policies.
  - [Crossref DOI](https://doi.org/10.1109/tsp.2010.2062509); [arXiv abstract](https://arxiv.org/abs/0910.2065)
- **[Overlap: Low] Anandkumar, A., Michael, N., Tang, A. K., & Swami, A. (2011). "Distributed Algorithms for Learning and Cognitive Medium Access with Logarithmic Regret." IEEE Journal on Selected Areas in Communications 29(4):731–745. DOI 10.1109/JSAC.2011.110406; arXiv:1006.1673.**
  - Model: secondary users with no information exchange.
  - Result: policies with order-optimal throughput (logarithmic regret) under self-play.
  - [OpenAlex/Crossref record](https://doi.org/10.1109/jsac.2011.110406); [arXiv abstract](https://arxiv.org/abs/1006.1673)
- **[Overlap: Low–Medium] Kalathil, D. M., Nayyar, N., & Jain, R. (2014). "Decentralized Learning for Multiplayer Multiarmed Bandits." IEEE Transactions on Information Theory 60(4):2331–2345. DOI 10.1109/TIT.2014.2302471.**
  - Model (recalled): player-specific (heterogeneous) arm means, with the system goal of the max-weight matching of players to arms. Learning is combined with distributed matching.
  - Relation: one of the few multi-learner models with heterogeneous values, but values attach to (player, arm) pairs rather than to a planner's per-unit weights.
  - [Crossref/OpenAlex record](https://doi.org/10.1109/tit.2014.2302471)
- **[Overlap: Low–Medium] Rosenski, J., Shamir, O., & Szlak, L. (2016). "Multi-Player Bandits – a Musical Chairs Approach." ICML 2016, PMLR 48. arXiv:1512.02866.**
  - Result: a communication-free algorithm, Musical Chairs, attains constant regret with high probability. Dynamic Musical Chairs is sublinear when players enter and leave.
  - Relation: structurally an explore-then-commit multi-agent protocol (an explore phase, then a commit/"seat-taking" phase), but the coupling is collisions, not a budget.
  - [arXiv abstract](https://arxiv.org/abs/1512.02866); [PMLR v48 index](https://proceedings.mlr.press/v48/)
- **[Overlap: Low] Boursier, E., & Perchet, V. (2019). "SIC-MMAB: Synchronisation Involves Communication in Multiplayer Multi-Armed Bandits." NeurIPS 2019. arXiv:1809.08151.**
  - Result: a decentralized algorithm matches centralized performance, "contradicting the existing lower bounds", by deliberately enforcing collisions as a communication protocol.
  - [arXiv abstract](https://arxiv.org/abs/1809.08151); [NeurIPS 2019 index](https://papers.nips.cc/paper_files/paper/2019)
- **[Overlap: Low] Wang, P.-A., Proutière, A., Ariu, K., Jedra, Y., & Russo, A. (2020). "Optimal Algorithms for Multiplayer Multi-Armed Bandits." AISTATS 2020, PMLR 108:4120–4129.**
  - Result: DPE1 for the collision setting is simpler than SIC-MMAB with better guarantees. DPE2 for the no-collision graph setting is asymptotically optimal with a finite expected number of transmitted bits.
  - [PMLR page](https://proceedings.mlr.press/v108/wang20m.html); [search summary confirming venue and pages](https://mlanthology.org/aistats/2020/wang2020aistats-optimal)
- **[Overlap: Low–Medium] Bistritz, I., & Leshem, A. (2018). "Distributed Multi-Player Bandits – a Game of Thrones Approach." NeurIPS 2018. Journal version: "Game of Thrones: Fully Distributed Learning for Multiplayer Bandits." Mathematics of Operations Research 46(1):159–178 (2021). DOI 10.1287/moor.2020.1051; arXiv:1810.11162.**
  - Model: each player has different expected rewards per arm, collisions give zero, and there is no communication.
  - Result: near-O(log T) sum of regrets against the optimal assignment.
  - Relation: heterogeneous values with a welfare-maximizing (planner-like) benchmark, but no planner and no budget.
  - [arXiv abstract](https://arxiv.org/abs/1810.11162); [Crossref (MOR)](https://doi.org/10.1287/moor.2020.1051); [NeurIPS 2018 index](https://papers.nips.cc/paper_files/paper/2018)
- **[Overlap: Low] Besson, L., & Kaufmann, E. (2018). "Multi-Player Bandits Revisited." ALT 2018. arXiv:1711.02317.**
  - Result: a taxonomy of feedback/sensing levels, an improved decentralized lower bound, and the RandTopM and MCTopM algorithms.
  - [arXiv abstract](https://arxiv.org/abs/1711.02317)
- **[Overlap: Low] Wang, X., Xie, H., & Lui, J. C. S. (2022). "Multi-Player Multi-Armed Bandits with Finite Shareable Resources Arms: Learning Algorithms & Applications." IJCAI 2022, pp. 3537–3543. DOI 10.24963/ijcai.2022/491; arXiv:2204.13502.**
  - Model: arms with finite shareable capacity. Reward is the per-load reward times min(#players, capacity).
  - Relation: arms as shared resources, a capacity analog of a budget, but no planner.
  - [Crossref DOI](https://doi.org/10.24963/ijcai.2022/491); [arXiv](https://arxiv.org/abs/2204.13502)
- **Survey: Boursier & Perchet (2024, JMLR)**, see Q1. [arXiv](https://arxiv.org/abs/2211.16275)

### Inferences
- Checklist for this strand:
  - (a) Planner: No. The centralized assignment is only the benchmark.
  - (b) Shared budget: No monetary budget. Arms are shared congestible resources.
  - (c) Different values: Yes, in the heterogeneous variants (Kalathil et al.; Bistritz & Leshem), as player–arm-specific means.
  - (d) With vs. without learning: No.
  - (e) Environment: shared, with strong interference (collisions).
- The paper should say explicitly that its teams never collide. Each team bids in its own market, so the multi-player coordination problem, and the communication-through-collision tricks, are absent. The only coupling is the planner's budget constraint, a weak coupling through a resource rather than through the environment.
- Musical Chairs and SIC-MMAB show that ETC-type protocols are standard for multiple learners. The novelty claim cannot rest on "multiple ETC learners" per se.

### Gaps
- Kalathil et al. (2014): model details are recalled; only the bibliographic data were verified.
- Several 2025–2026 multi-player preprints surfaced in alphaXiv searches but were not read: arXiv:2510.06683 ("Distributed Algorithms for Multi-Agent Multi-Armed Bandits with Collision"), arXiv:2610.18514 (heterogeneous asynchronous multi-player bandits) and arXiv:2602.16965 ("Multi-Agent Lipschitz Bandits"). They are recent, but nothing in their abstracts suggests a planner or budget.

## Q3. Federated / communication-constrained bandits: what has been done, and how does it differ?

### Takeaway
Federated bandits add a central server that aggregates clients' statistics under communication constraints. Clients may face heterogeneous local instances of a global model, and personalization weights mix local and global objectives. The server is an information aggregator, not a resource allocator. No paper here splits a spending budget across clients or compares allocations with and without learning. The closest element is Réda, Vakili & Kaufmann (2022): a central controller, weighted "mixed rewards" across agents, and data-dependent sampling across agents for pure exploration.

### Cited Findings
- **[Overlap: Low–Medium] Shi, C., & Shen, C. (2021). "Federated Multi-Armed Bandits." AAAI 2021. arXiv:2101.12204.**
  - Model, approximate version: heterogeneous local models are random realizations of an unknown global model, which adds client-sampling uncertainty. The exact version makes the global model the exact average of the local models.
  - Result: Fed2-UCB ("double UCB") gets O(log T) regret while accounting for communication cost, and gradually admitting new clients is critical. In the exact model, order-optimal regret holds regardless of the number of clients, given a careful choice of update period.
  - [arXiv abstract](https://arxiv.org/abs/2101.12204)
- **[Overlap: Low–Medium] Shi, C., Shen, C., & Yang, J. (2021). "Federated Multi-armed Bandits with Personalization." AISTATS 2021, PMLR 130. arXiv:2102.13101.**
  - Model (recalled): each client's objective mixes its local reward with the global reward through a personalization weight.
  - Relation: client-specific weights loosely resemble (c), but the weights apply to objectives rather than budget priorities.
  - [arXiv](https://arxiv.org/abs/2102.13101); [PMLR v130 index](https://proceedings.mlr.press/v130/)
- **[Overlap: Low] Wang, Y., Hu, J., Chen, X., & Wang, L. "Distributed Bandit Learning: Near-Optimal Regret with Efficient Communication." arXiv:1904.06309 (venue unverified; believed ICLR 2020).**
  - Model: M agents coordinated by a central server minimize total regret.
  - Result: near-optimal regret with O(M log(MK)) communication for MAB, independent of T. For d-dimensional linear bandits, communication is Õ(Md).
  - [arXiv abstract](https://arxiv.org/abs/1904.06309)
- **[Overlap: Medium–Low] Réda, C., Vakili, S., & Kaufmann, E. (2022). "Near-Optimal Collaborative Learning in Bandits." NeurIPS 2022 (Advances in NeurIPS 35, pp. 14183–14195), DOI 10.52202/068431-1031; arXiv:2206.00121.**
  - Model: agents communicate through a central controller, and each agent's optimal arm maximizes a weighted sum of all agents' rewards (the "mixed reward"). The setting recovers federated learning with personalization.
  - Result: lower bounds for pure exploration and regret, and a near-optimal phased-elimination algorithm with a data-dependent sampling scheme.
  - Relation: the federated paper closest to "a controller allocating sampling across weighted agents", but it allocates samples, not money, and has no learning-vs-no-learning allocation.
  - [arXiv abstract](https://arxiv.org/abs/2206.00121); [Crossref](https://doi.org/10.52202/068431-1031)
- **[Overlap: Low] Huang, R., Wu, W., Yang, J., & Shen, C. (2021). "Federated Linear Contextual Bandits." NeurIPS 2021. arXiv:2110.14177.** [arXiv](https://arxiv.org/abs/2110.14177); [NeurIPS 2021 index](https://papers.nips.cc/paper_files/paper/2021)
- **[Overlap: Low] Dubey, A., & Pentland, A. (2020). "Differentially-Private Federated Linear Bandits." NeurIPS 2020.** [NeurIPS 2020 index](https://papers.nips.cc/paper_files/paper/2020)
- **[Overlap: Low–Medium] "Pay to Learn, Share to Earn: Incentivized Federated Multi-Player Bandits." arXiv:2610.06062 (Oct 2026; IISc; authors not retrieved).**
  - Model: players interact with a common bandit environment and share information through a central server, with incentives or payments.
  - Relation: recent work adding economics (payments) to federated bandits. There is still a common environment.
  - [alphaXiv listing](https://www.alphaxiv.org/abs/2610.06062)

### Inferences
- Checklist for this strand:
  - (a) Coordinator: Yes, a central server, but it aggregates information and schedules communication. It does not allocate resources.
  - (b) Shared budget: only a communication budget (bits or rounds), never a spending budget.
  - (c) Different weights: partial (personalization or mixed-reward weights).
  - (d) With vs. without learning: No.
  - (e) Environment: a common global model with heterogeneous local instances, partly independent.
- Federated bandits are the strand a reviewer most naturally maps to "planner + many learners". The answer is that the federated server never decides how much each client may spend or explore. Its lever is communication. The paper's planner has the opposite lever (budget and τ) and no information pooling.

### Gaps
- Venue of Wang, Hu, Chen & Wang (arXiv:1904.06309) not verified.
- The personalization-weight detail of Shi, Shen & Yang (2021) is recalled.
- Authors of arXiv:2610.06062 were not retrieved.

## Q4. Competing bandits, matching markets, and competition among learning firms: what has been done, and how does it differ?

### Takeaway
This strand puts multiple learners into a shared market where they compete for arms or users. In matching markets, players learn preferences while arms have preferences over players. ETC is a standard tool (Liu, Mania & Jordan 2020; Pagare & Ghosh 2024). The economic message of Aridor et al. (2025) is that competition between learning firms pushes them toward greedy, no-exploration algorithms. That message is the closest "with vs. without exploration" comparison in multi-learner work, but it concerns algorithm choice under rivalry, not a planner's budget split.

### Cited Findings
- **[Overlap: Low–Medium] Liu, L. T., Mania, H., & Jordan, M. I. (2020). "Competing Bandits in Matching Markets." AISTATS 2020, PMLR 108. arXiv:1906.05363.**
  - Model: one side (players) learns its preferences from stochastic rewards, and arms have preferences over players. Both centralized (platform) and decentralized approaches are studied.
  - Result: "surprising exploration-exploitation trade-offs" compared with single-player MAB.
  - (Recalled) The paper analyses a centralized explore-then-commit (ETC) algorithm and a centralized UCB. ETC attains player-optimal stable regret given gap knowledge, while UCB guarantees only player-pessimal stable regret.
  - Relation: an ETC multi-learner model with a central platform. The platform computes matchings and does not allocate budgets.
  - [arXiv abstract](https://arxiv.org/abs/1906.05363); [PMLR v108 index](https://proceedings.mlr.press/v108/)
- **[Overlap: Low] Liu, L. T., Ruan, F., Mania, H., & Jordan, M. I. "Bandit Learning in Decentralized Matching Markets." arXiv:2012.07348 (JMLR 2021, venue unverified).**
  - Result: O(log T) stable regret when arms' preferences are shared, and O(log² T) with no preference assumptions. Incentive compatibility holds when arm preferences are shared.
  - [arXiv abstract](https://arxiv.org/abs/2012.07348)
- **[Overlap: Low] Sankararaman, A., Basu, S., & Sankararaman, K. A. (2021). "Dominate or Delete: Decentralized Competing Bandits in Serial Dictatorship." AISTATS 2021, PMLR 130. arXiv:2006.15166.**
  - Model: demand-side agents have unknown, heterogeneous valuations, and arms have a known uniform preference.
  - Algorithm: UCB with Decentralized Dominant-arm Deletion (UCB-D3).
  - [arXiv abstract](https://arxiv.org/abs/2006.15166); [PMLR v130 index](https://proceedings.mlr.press/v130/)
- **[Overlap: Low–Medium] Pagare, T., & Ghosh, A. (2024). "Explore-then-Commit Algorithms for Decentralized Two-Sided Matching Markets." ISIT 2024 (per arXiv comment). arXiv:2408.08690.**
  - Model: a decentralized two-sided market where arms do not know their preferences and there are no structural assumptions.
  - Result: epoch-based CA-ETC (collision-avoidance explore-then-commit) needs no communication and yields player-optimal expected regret bounds that depend on epoch parameters. A blackboard-communication baseline gets logarithmic regret.
  - Relation: the multi-learner ETC paper the coordinator flagged. The multi-agent ETC design problem is epoch-length tuning under competition, whereas the paper's is ex-ante probe length under a budget.
  - [arXiv abstract](https://arxiv.org/abs/2408.08690)
- **[Overlap: Medium] Aridor, G., Mansour, Y., Slivkins, A., & Wu, Z. S. (2025). "Competing Bandits: The Perils of Exploration Under Competition." ACM Transactions on Economics and Computation 13(1):1–47. DOI 10.1145/3711831; arXiv:2007.10144, which merges and extends arXiv:1702.08533 and arXiv:1902.05590.**
  - Model: a duopoly in which two firms face the same MAB. Users arrive and choose a firm, and each firm learns only from its own users.
  - Result: "stark competition induces firms to commit to a 'greedy' bandit algorithm that leads to low welfare". Weakening competition, through "free" users, less rational users or a first-mover advantage, incentivizes better exploration and raises welfare. The paper relates this to "competition vs. innovation".
  - Relation: an economics-of-exploration result that a planner allocating budget to teams could cite. Protected budget, like "free users", is what makes exploration worthwhile. In the paper, too, exploration is worthwhile only when a team's budget is large enough. The mechanism differs: rivalry for users there, a budget threshold here.
  - [Crossref (TEAC)](https://doi.org/10.1145/3711831); [arXiv abstract](https://arxiv.org/abs/2007.10144)
- **[Overlap: Low–Medium] Antecedents:**
  - Aridor, G., Liu, K., Slivkins, A., & Wu, Z. S. (2019). "The Perils of Exploration under Competition: A Computational Modeling Approach." EC 2019, pp. 171–172. DOI 10.1145/3328526.3329635. [Crossref](https://doi.org/10.1145/3328526.3329635)
  - Mansour, Y., Slivkins, A., & Wu, Z. S. "Competing Bandits: Learning under Competition." arXiv:1702.08533 (ITCS 2018, venue unverified). [arXiv](https://arxiv.org/abs/1702.08533)
- **[Overlap: Low] Ghosh, A., Sankararaman, A., Ramchandran, K., Javidi, T., & Mazumdar, A. (2024). "Competing Bandits in Non-Stationary Matching Markets." IEEE Transactions on Information Theory 70(4):2831–2850. DOI 10.1109/TIT.2024.3352228.** [Crossref](https://doi.org/10.1109/tit.2024.3352228)

### Inferences
- Checklist for this strand:
  - (a) Planner: a matching platform in the centralized versions, which computes matchings and never allocates budgets. No planner in Aridor et al. (firms compete).
  - (b) Shared budget: No. Shared capacity, one arm per player, plays that role.
  - (c) Different values: Yes, heterogeneous preferences.
  - (d) With vs. without learning: only Aridor et al., as greedy vs. exploring algorithm adoption under competition.
  - (e) Environment: shared market with competition.
- If the two agent teams were in the same RTB market, competing with each other or with other learners, this strand would become directly relevant. The paper's "independent markets" assumption is what separates it. The authors should state it as a modelling choice and could mention competition between teams as an extension.

### Gaps
- The ETC detail of Liu, Mania & Jordan (2020) is recalled from the paper, not the abstract.
- JMLR details of Liu, Ruan, Mania & Jordan (2021) and the ITCS 2018 venue of Mansour, Slivkins & Wu are unverified.

## Q5. Multiple learning bidders in auctions: what has been done, and how does it differ?

### Takeaway
A large literature studies several learning bidders interacting in the same repeated auctions: algorithmic collusion, regret-minimizing agents, budget pacing and its equilibrium, and liquid-welfare guarantees. A recent sub-strand studies principals who configure their own learning agents ex ante, choosing reported values or budgets (Kolumbus & Nisan 2022a,b; Feng, Lucier & Slivkins 2024). That is conceptually close to the paper's planner committing budgets and probe lengths. The closest single paper is Deng, Golrezaei, Jaillet, Liang & Mirrokni (2023): an advertiser splits budget (and ROI targets) across channels whose autobidders act for her, and learns the per-channel budgets under bandit feedback. None of these combines value-weighted teams, ETC learning inside each unit, and a with-vs-without-learning allocation comparison.

### Cited Findings
- **[Overlap: Medium] Kolumbus, Y., & Nisan, N. (2022a). "Auctions Between Regret-Minimizing Agents." Proceedings of the ACM Web Conference 2022 (WWW '22). arXiv:2110.11855.**
  - Model: software agents implemented as regret-minimizing algorithms bid in repeated first-price, second-price and generalized auctions on behalf of users.
  - Result: in second-price auctions, players have incentives to misreport their true valuations to their own learning agents. In first-price auctions, truthful reporting to agents is a dominant strategy.
  - Relation: a principal–learning-agent delegation layer, as in the paper. The principals compete, rather than one planner allocating across its own agents.
  - [arXiv abstract](https://arxiv.org/abs/2110.11855)
- **[Overlap: Medium] Kolumbus, Y., & Nisan, N. (2022b). "How and Why to Manipulate Your Own Agent: On the Incentives of Users of Learning Agents." NeurIPS 2022. arXiv:2112.07640.**
  - Model: the agents' learning dynamics induce a "meta-game" between users.
  - Result: users generally have incentives to misreport their parameters to their own agents, which can produce outcomes very different from standard analysis.
  - Relation: the planner's ex-ante choice of (budget, τ) is a "meta-game" decision over learning agents' parameters, but with a single decision-maker.
  - [arXiv abstract](https://arxiv.org/abs/2112.07640); [NeurIPS 2022 index](https://papers.nips.cc/paper_files/paper/2022)
- **[Overlap: Medium–Low] Banchio, M., & Skrzypacz, A. (2022). "Artificial Intelligence and Auction Design." EC 2022, pp. 30–31 (extended abstract), DOI 10.1145/3490486.3538244; arXiv:2202.05947.**
  - Model: Q-learning bidders in repeated auctions.
  - Result: first-price auctions with no extra feedback lead to tacit-collusive outcomes (bids below values) and second-price auctions do not, because of the incentive to outbid by one increment. Revealing the minimum winning bid increases competitiveness.
  - Relation: the RTB context is first-price, as in the paper. Interaction among learners is the key mechanism there and is absent in the paper.
  - [arXiv abstract](https://arxiv.org/abs/2202.05947); [Crossref (EC'22)](https://doi.org/10.1145/3490486.3538244)
- **[Overlap: Low–Medium] Calvano, E., Calzolari, G., Denicolò, V., & Pastorello, S. (2020). "Artificial Intelligence, Algorithmic Pricing, and Collusion." American Economic Review 110(10):3267–3297. DOI 10.1257/aer.20190623.**
  - Result: Q-learning pricing algorithms "consistently learn to charge supracompetitive prices, without communicating with one another". Collusion is sustained by a finite punishment phase followed by a gradual return to cooperation, and is robust to asymmetries, the number of players and uncertainty.
  - [Crossref record with abstract](https://doi.org/10.1257/aer.20190623)
- **[Overlap: Medium] Balseiro, S. R., & Gur, Y. (2019). "Learning in Repeated Auctions with Budgets: Regret Minimization and Equilibrium." Management Science 65(9):3952–3968. DOI 10.1287/mnsc.2018.3174.**
  - Model: budget-constrained advertisers in sequential auctions who know neither their value distribution nor competitors' budgets, values or strategies.
  - Result: adaptive pacing strategies, which adjust bids to realized spending, are asymptotically optimal against i.i.d. and arbitrary competing bids, with matching bounds. In a display-advertising regime they form an approximate Nash equilibrium in dynamic strategies.
  - Relation: the canonical reference for "budget-paced bidding by learning agents" and for many budgeted learners in one market. Each bidder owns its budget, and nobody splits a budget across units.
  - [Crossref](https://doi.org/10.1287/mnsc.2018.3174); [Stanford GSB page (abstract)](https://www.gsb.stanford.edu/faculty-research/publications/learning-repeated-auctions-budgets-regret-minimization-equilibrium)
- **[Overlap: Low–Medium] Fikioris, G., & Tardos, É. (2023). "Liquid Welfare Guarantees for No-Regret Learning in Sequential Budgeted Auctions." EC 2023; also Mathematics of Operations Research (per arXiv comment). arXiv:2210.07502.**
  - Result: in first-price auctions with budget-limited learning buyers, a γ + 1/2 + O(1/γ) price of anarchy (PoA) for liquid welfare, about 2.41 at γ = 1 with a lower bound of 2. Sequential second-price auctions can be arbitrarily bad.
  - [arXiv abstract](https://arxiv.org/abs/2210.07502)
- **[Overlap: Low–Medium] Gaitonde, J., Li, Y., Light, B., Lucier, B., & Slivkins, A. (2023). "Budget Pacing in Repeated Auctions: Regret and Efficiency without Convergence." ITCS 2023 (preliminary version; per arXiv comment). arXiv:2205.08674.**
  - Result: when all agents use gradient-based pacing, liquid welfare is at least half of optimal without convergence of the dynamics, for any core auction (first-price, second-price, GSP). Individual dynamic-regret bounds also hold.
  - [arXiv abstract](https://arxiv.org/abs/2205.08674)
- **[Overlap: Medium–High] Feng, Y., Lucier, B., & Slivkins, A. (2024). "Strategic Budget Selection in a Competitive Autobidding World." STOC 2024, pp. 213–224. DOI 10.1145/3618260.3649688; arXiv:2307.07374.**
  - Model: advertisers strategically choose the constraints, such as budgets, given to the platform's autobidders, and those constraints define an inner budget-pacing game in a first-price auction.
  - Result: at any pure Nash equilibrium of the constraint-choosing metagame, liquid welfare is at least half of optimal (tight), with a 4-approximation for mixed and Bayes–Nash equilibria. Without the power to declare budgets (value-per-click or ROI only), the factor can be linear in the number of advertisers.
  - Relation: the clearest precedent for "budget as the principal's ex-ante lever over a learning agent". It differs in having many competing principals with one agent each, welfare and PoA as the focus, and no value-weighted split across one's own teams and no learning-vs-no-learning comparison.
  - [arXiv abstract](https://arxiv.org/abs/2307.07374); [Crossref](https://doi.org/10.1145/3618260.3649688)
- **[Overlap: High] Deng, Y., Golrezaei, N., Jaillet, P., Liang, J. C. N., & Mirrokni, V. (2023). "Multi-channel Autobidding with Budget and ROI Constraints." ICML 2023, PMLR 202. arXiv:2302.01523.**
  - Model: an advertiser maximizes total conversions under aggregate budget and ROI constraints across channels. She cannot bid directly; each channel's autobidder buys on her behalf, and her levers are per-channel budgets and per-channel target ROIs.
  - Result: ROI-only optimization can be "arbitrarily worse" than the global optimum, while optimizing only per-channel budgets achieves the global optimum. An efficient learning algorithm under bandit feedback produces per-channel budgets whose conversions approximate the global optimum.
  - Relation: the closest published analog of "an advertiser-planner splitting a budget across delegated bidding units". Differences:
    - The learning is done by the planner, across rounds, over budget splits.
    - The channel autobidders are not modelled as explore-then-commit learners of an unknown competition state.
    - There is no learning-vs-no-learning value window and no result on the skew of the split.
  - [arXiv abstract](https://arxiv.org/abs/2302.01523); [PMLR v202 index](https://proceedings.mlr.press/v202/)
- **[Overlap: Low] Feng, Z., Podimata, C., & Syrgkanis, V. (2018). "Learning to Bid Without Knowing your Value." EC 2018 (per arXiv comment). arXiv:1711.01333.** A single-learner bidding reference. [arXiv](https://arxiv.org/abs/1711.01333)

### Inferences
- Checklist for this strand:
  - (a) Planner: Mostly No. The partial exceptions are Deng et al. 2023, an advertiser over channels, and the principals configuring their own agents in Kolumbus–Nisan and Feng–Lucier–Slivkins.
  - (b) Shared budget split: Deng et al. only (per-channel budgets). Elsewhere each bidder has its own budget.
  - (c) Different values: Yes, across bidders, and across channels in Deng et al.
  - (d) With vs. without learning: No. Benchmarks are competitive or collusive outcomes, PoA, or the budget vs. ROI lever.
  - (e) Environment: shared auctions with strategic interaction, except Deng et al., where channels are separate markets.
- For a WITS/IS audience, Balseiro & Gur (2019) and Deng et al. (2023) are the references the paper is most likely to be compared with. The paper should position its exploitation agent (a constant budget-paced bid from the posterior) against adaptive pacing. It should position its planner against multi-channel budget optimization. Its distinct contribution is that the value of a unit's budget includes the option value of learning that unit's market, which makes V(B) non-concave and produces the entry jump in V'(B)/W'(B). Deng et al. and Balseiro–Gur do not model this.

### Gaps
- The full regret statement for Deng et al.'s bandit-feedback algorithm was not read.
- No paper was found that studies one advertiser running several learning campaigns in separate first-price markets and optimizing the ex-ante split, beyond the planner-learns formulations in Q7.

## Q6. Economics: strategic experimentation, incentivized exploration, social learning, team experimentation

### Takeaway
Economics has three relevant multi-learner traditions:
1. Strategic experimentation (Bolton–Harris 1999; Keller–Rady–Cripps 2005): players learn about a common or correlated state, information is a public good, and equilibria have free-riding and too little experimentation compared with a planner's benchmark.
2. Incentivized exploration (Kremer–Mansour–Perry 2014; Frazier et al. 2014; Mansour–Slivkins–Syrgkanis 2020): a planner or principal uses disclosure or payments, sometimes under a payment budget, to make myopic agents explore one common bandit.
3. Principal–team experimentation and contests: Bonatti–Hörner 2011; Halac–Kartik–Liu 2016, and 2017 (a designer allocating a prize budget); Moroni 2022.

The closest economics analog of "split a fixed experimentation budget across independent units" is Azevedo et al. (2020, JPE) on allocating scarce A/B-testing traffic across innovations. The value-of-information non-concavity literature (Radner–Stiglitz; Chade–Schlee 2002) is the natural theoretical anchor for the paper's entry jump and skewed allocation.

### Cited Findings
- **[Overlap: Medium] Bolton, P., & Harris, C. (1999). "Strategic Experimentation." Econometrica 67(2):349–374. DOI 10.1111/1468-0262.00022.**
  - Model: the two-armed bandit is extended to many players facing the same problem, who learn from each other's experiments.
  - Result: information is a public good, which creates a free-rider effect. An "encouragement effect" also appears: expected future experimentation by others encourages more experimentation now. Stationary Markov equilibria are characterized in terms of these two effects.
  - Relation: the classic "team of bandit learners" in economics. There is a common state, no budget and no planner, and the planner solution appears only as the efficiency benchmark.
  - [Crossref DOI](https://doi.org/10.1111/1468-0262.00022); [Econometric Society page](https://econometricsociety.org/publications/econometrica/1999/03/01/strategic-experimentation)
- **[Overlap: Medium–Low] Keller, G., Rady, S., & Cripps, M. (2005). "Strategic Experimentation with Exponential Bandits." Econometrica 73(1):39–68. DOI 10.1111/j.1468-0262.2005.00564.x.**
  - Result:
    - Free-riding gives inefficiently low experimentation in any stationary Markov equilibrium.
    - There is a unique symmetric Markovian equilibrium, in mixed strategies, and no equilibrium in simple cut-off strategies.
    - Asymmetric equilibria with role switching share the burden and dominate the symmetric one in aggregate payoff where both arms are used.
  - [Crossref DOI](https://doi.org/10.1111/j.1468-0262.2005.00564.x); [RePEc/IDEAS abstract](https://ideas.repec.org/a/ecm/emetrp/v73y2005i1p39-68.html)
  - Follow-up: Keller, G., & Rady, S., "Strategic Experimentation with Poisson Bandits". Only the SSRN 2009 version is verified (DOI 10.2139/ssrn.1375355); the Theoretical Economics 2010 details are unverified. [SSRN DOI](https://doi.org/10.2139/ssrn.1375355)
- **[Overlap: Medium–Low] Bonatti, A., & Hörner, J. (2011). "Collaborating." American Economic Review 101(2):632–663. DOI 10.1257/aer.101.2.632.**
  - Model: "moral hazard in teams over time". Agents work collectively on a project of uncertain duration and outcome with unobserved efforts.
  - Result: free-riding reduces effort and causes procrastination. Delay increases with the number of agents, and deadlines help.
  - Relation: "teams" of learners with a common project, the opposite of independent units.
  - [Crossref record with abstract](https://doi.org/10.1257/aer.101.2.632)
- **[Overlap: Medium] Halac, M., Kartik, N., & Liu, Q. (2017). "Contests for Experimentation." Journal of Political Economy 125(5):1523–1569. DOI 10.1086/693040.**
  - Model: contests for innovation in which agents learn about the innovation's feasibility and about opponents' outcomes. The designer chooses a prize-sharing scheme and a disclosure policy.
  - Per the authors' slides, the designer maximizes experimentation subject to limited liability and an ex-post budget constraint. In the working-paper abstract, public winner-take-all dominates other prize-sharing schemes, and more generally a mixture contest is optimal.
  - Relation: a designer allocating a fixed reward budget across several learning agents, the closest "planner + shared budget + multiple learners" in economics. The agents are strategic and experiment on one common project, and the budget is a prize rather than operating funds.
  - [Crossref](https://doi.org/10.1086/693040); [RePEc](https://econpapers.repec.org/RePEc:ucp:jpolec:doi:10.1086/693040); [authors' slides](https://www.columbia.edu/~nk2339/Slides/HKL-contests-slides.pdf)
- **[Overlap: Low–Medium] Halac, M., Kartik, N., & Liu, Q. (2016). "Optimal Contracts for Experimentation." Review of Economic Studies 83(3):1040–1091. DOI 10.1093/restud/rdw013.** A principal contracting with a single experimenting agent. [Crossref](https://doi.org/10.1093/restud/rdw013)
- **[Overlap: Medium–Low] Moroni, S. (2022). "Experimentation in Organizations." Theoretical Economics 17(3):1403–1450. DOI 10.3982/TE3069.**
  - Model: a principal motivates a team of agents on a risky two-milestone project of unknown feasibility. Agents' beliefs fall while they fail.
  - Result: the principal must pay rents to prevent delay and free-riding, and prefers rewarding through future contract terms or task assignments rather than cash.
  - Working-paper versions report inefficiently early stopping and asymmetric experimentation assignments to identical agents. That is a principal deliberately allocating experimentation asymmetrically, an echo of the paper's skew.
  - [Crossref](https://doi.org/10.3982/te3069); [IDEAS](https://ideas.repec.org/a/the/publsh/3069.html)
- **[Overlap: Medium–Low] Kremer, I., Mansour, Y., & Perry, M. (2014). "Implementing the 'Wisdom of the Crowd'." Journal of Political Economy 122(5):988–1012. DOI 10.1086/676597.**
  - Model: a planner discloses information to sequentially arriving agents who choose among actions with unknown payoffs.
  - Result: the optimal disclosure policy for social welfare. Per a Microsoft Research talk abstract, welfare converges to the unconstrained optimum as agents grow.
  - [Crossref](https://doi.org/10.1086/676597); [RePEc](https://econpapers.repec.org/RePEc:ucp:jpolec:doi:10.1086/676597); [Microsoft Research page](https://www.microsoft.com/en-us/research/?p=189948)
- **[Overlap: Medium] Frazier, P., Kempe, D., Kleinberg, J., & Kleinberg, R. (2014). "Incentivizing Exploration." EC 2014, pp. 5–22. DOI 10.1145/2600057.2602897.**
  - Model: a principal maximizes time-discounted reward from a Bayesian MAB, but the arms are pulled by selfish myopic agents, who must be paid to explore.
  - Result: the paper characterizes which (payment, reward) pairs are achievable as fractions of OPT, the reward from pulling directly, using "time-expanded" policies. It received the EC 2014 Best Paper award.
  - Relation: a planner with a payment budget buying exploration from learners is (a)+(b). But it is one common bandit and the payments buy exploration rather than funding units.
  - [Crossref](https://doi.org/10.1145/2600057.2602897); [Cornell news](https://news.cornell.edu/node/283818)
- **[Overlap: Medium–Low] Mansour, Y., Slivkins, A., & Syrgkanis, V. (2020). "Bayesian Incentive-Compatible Bandit Exploration." Operations Research 68(4):1132–1161. DOI 10.1287/opre.2019.1949 (EC 2015 extended abstract); arXiv:1502.04147.**
  - Result: a social planner's recommendation policy is modelled as a bandit algorithm under Bayesian incentive-compatibility constraints. The algorithm is BIC and asymptotically regret-optimal, and a black-box reduction turns any bandit algorithm into a BIC one at constant multiplicative regret cost.
  - [Crossref record with abstract](https://doi.org/10.1287/opre.2019.1949)
- **[Overlap: Low–Medium] Mansour, Y., Slivkins, A., Syrgkanis, V., & Wu, Z. S. (2022). "Bayesian Exploration: Incentivizing Exploration in Bayesian Games." Operations Research 70(2):1105–1127. DOI 10.1287/opre.2021.2205 (EC 2016).** Many interacting agents per round. [Crossref](https://doi.org/10.1287/opre.2021.2205)
- **[Overlap: Low–Medium] Wang, S., & Huang, L. (2018). "Multi-armed Bandits with Compensation." NeurIPS 2018. arXiv:1811.01715.**
  - Model: a controller pays short-term players to explore.
  - Result: a compensation lower bound Θ(Σ_i Δ_i log T / KL_i), and algorithms with O(log T) regret and O(log T) compensation.
  - [arXiv abstract](https://arxiv.org/abs/1811.01715)
- **Social learning with bandits.**
  - **[Overlap: Low] Rosenberg, D., Solan, E., & Vieille, N. (2007). "Social Learning in One-Arm Bandit Problems." Econometrica 75(6):1591–1611. DOI 10.1111/j.1468-0262.2007.00807.x.** (Recalled) players face one-arm bandits with irreversible stopping and observe each other's actions. [Crossref](https://doi.org/10.1111/j.1468-0262.2007.00807.x)
  - **[Overlap: Low] Bala, V., & Goyal, S. (1998). "Learning from Neighbours." Review of Economic Studies 65(3):595–621. DOI 10.1111/1467-937X.00059.** (Recalled) agents learn from neighbours' experiences in a network. [Crossref](https://doi.org/10.1111/1467-937x.00059)
  - **[Overlap: Low–Medium] Banihashem, K., Hajiaghayi, M., Shin, S., & Slivkins, A. (2023). "Bandit Social Learning under Myopic Behavior." NeurIPS 2023; arXiv:2302.07425 (extended version titled "Bandit Social Learning: Exploration under Myopic Behavior").** Agents collectively follow a bandit protocol but act myopically, and the paper derives "stark learning failures" for greedy or biased behaviour with matching positive results. This is a with- vs. without-exploration comparison in a multi-agent setting. [arXiv abstract](https://arxiv.org/abs/2302.07425); [NeurIPS 2023 index](https://papers.nips.cc/paper_files/paper/2023)
- **[Overlap: Medium–High conceptual] Azevedo, E. M., Deng, A., Montiel Olea, J. L., Rao, J., & Weyl, E. G. (2020). "A/B Testing with Fat Tails." Journal of Political Economy 128(12):4614– (end page not returned by Crossref). DOI 10.1086/710607.**
  - Question: "how to optimally use scarce experimental resources to screen innovations", that is, allocating a fixed experimentation budget (traffic) across independent candidate ideas.
  - Result: if the tails of the prior of true effects are not too thick, a few high-powered experiments are optimal. With very fat tails, a "lean" strategy of many small experiments is optimal. Bing EXP data show extremely fat tails.
  - Relation: the cleanest economics precedent for a planner splitting a fixed learning budget across independent units, with the optimal split hinging on the shape of the value of experimentation. It differs from the paper: it is one-shot screening without a downstream exploitation budget, the units are ideas rather than value-weighted spending teams, and there is no RTB structure.
  - [Crossref](https://doi.org/10.1086/710607); [IDEAS](https://ideas.repec.org/a/ucp/jpolec/doi10.1086-710607.html)
- **[Overlap: Medium (theory anchor)] Value-of-information non-concavity.**
  - **Chade, H., & Schlee, E. (2002). "Another Look at the Radner–Stiglitz Nonconcavity in the Value of Information." Journal of Economic Theory 107(2):421–452. DOI 10.1006/jeth.2001.2960.** (Recalled) it gives general conditions under which the marginal value of information is zero at zero information, so the value of information is not concave. [Crossref](https://doi.org/10.1006/jeth.2001.2960)
  - **Moscarini, G., & Smith, L. (2002). "The Law of Large Demand for Information." Econometrica 70(6):2351–2366. DOI 10.1111/1468-0262.00378.** [Crossref](https://doi.org/10.1111/1468-0262.00378)
  - The original Radner & Stiglitz (1984) chapter is cited in Chade–Schlee's title. Its bibliographic details were not independently verified.
- **[Overlap: Low–Medium] Allocation across divisions or teams without learning, as background for the skew result.**
  - **Stein, J. C. (1997). "Internal Capital Markets and the Competition for Corporate Resources." Journal of Finance 52(1):111–133. DOI 10.1111/j.1540-6261.1997.tb03810.x.** (Recalled) headquarters engages in "winner-picking" across divisions. [Crossref](https://doi.org/10.1111/j.1540-6261.1997.tb03810.x)
  - **Marschak, J., & Radner, R. (1972). *Economic Theory of Teams*. Yale University Press.** The classic theory of decentralized team members with a common objective. Verified via contemporaneous book reviews. [Book review record (J. Business 1973)](https://doi.org/10.1086/295563)
  - **Bergemann, D., & Hege, U. (1998). "Venture Capital Financing, Moral Hazard, and Learning." Journal of Banking & Finance 22(6–8):703–735. DOI 10.1016/S0378-4266(98)00017-X.** (Recalled) staged financing of a project of unknown quality, where the investor's money buys learning. [Crossref](https://doi.org/10.1016/s0378-4266(98)00017-x)

### Inferences
- Checklist:
  - Strategic experimentation: (a) No (planner only as benchmark); (b) No; (c) symmetric players; (d) equilibrium vs. efficient experimentation, not with vs. without learning; (e) common state.
  - Incentivized exploration: (a) Yes; (b) a payment budget (Frazier et al.; Wang–Huang); (c) homogeneous myopic agents; (d) greedy vs. incentivized exploration; (e) one common bandit.
  - Contests and organizations: (a) Yes; (b) a prize budget (Halac–Kartik–Liu 2017); (c) mostly symmetric agents, though Moroni assigns asymmetric experimentation to identical agents; (e) a common project.
  - A/B testing: (a) Yes; (b) Yes (traffic); (c) ideas differ only through the prior; (d) implicit, since the value of testing vs. not testing drives the allocation; (e) independent units.
- The paper's main allocation result, that the split is skewed toward the senior team when the junior cannot afford to learn and more balanced once both learn, is in economic terms a corner/threshold effect from a non-concave unit value function. The Radner–Stiglitz/Chade–Schlee non-concavity and Azevedo et al.'s "few big vs. many small experiments" are the closest theoretical relatives. Citing them would pre-empt a reviewer who argues that "learning adds a fixed cost, hence a threshold; this is known".
- The economics team-experimentation literature (Bolton–Harris, Keller–Rady–Cripps, Bonatti–Hörner, Moroni) treats teams as strategic agents sharing a common state. The paper's teams are non-strategic, have independent states and are coordinated only through money. Saying this explicitly separates the paper from "teams" in economics.

### Gaps
- The exact achievable-region condition in Frazier et al. (2014) was not re-verified.
- The published JPE abstract wording of Halac–Kartik–Liu (2017) was not seen, only the slides and the working-paper summary.
- Keller–Rady (Theoretical Economics 2010) and the Radner–Stiglitz (1984) chapter details are unverified.
- Model descriptions marked "(recalled)" for Rosenberg–Solan–Vieille, Bala–Goyal, Stein, Bergemann–Hege and Chade–Schlee were not re-read this session.

## Q7. Coordinated teams under a common resource: what exists?

### Takeaway
The targeted searches covered multi-agent bandits with a shared budget, a central planner allocating budget to bandit learners, meta-bandits with budgets, multi-task budget allocation and hierarchical coordinators. They found several lines that share some of the paper's ingredients:
- **Centralized budget allocation across campaigns or tasks learned by bandits:** Nuara et al. 2018/2022; Ge et al. 2024; Zuo & Joe-Wong 2021; Bachoc et al. 2025/2026.
- **Budgeted pure exploration across several independent bandits:** Gabillon et al. 2011.
- **Budgeted Bayesian learning with explore-before-exploit structure:** Guha & Munagala 2007; Guha 2026b.
- **Meta-bandits with budgets:** Guha 2026a, arXiv:2610.38955.
- **Managing a portfolio of self-learning algorithms under a training budget:** Latypov et al. 2025/2026; CORRAL.
- **A central coordinator over several bandits coupled by a global constraint:** Zibaie et al. 2025.
- **Shared cost budgets in multi-agent RL:** Cao et al. 2026.
- **LLM-agent orchestration and budget work, mostly empirical or systems:** 2026 preprints.

None has a planner who commits budgets (and probe lengths) ex ante to autonomous explore-then-commit units in independent markets, weights them by different values, and compares the allocation with a no-learning benchmark.

### Cited Findings
- **[Overlap: High (structure)] Gabillon, V., Ghavamzadeh, M., Lazaric, A., & Bubeck, S. (2011). "Multi-Bandit Best Arm Identification." NIPS 2011, pp. 2222–2230.**
  - Model: identify the best arm in each of several independent bandit problems under one fixed total sampling budget.
  - Algorithms: Gap-based Exploration (GapE) and GapE-V, which concentrate sampling on arms close to their bandit's best arm, with error-probability bounds.
  - Relation: a single allocator splitting one budget across independent learning problems, which is (a)+(b)+(e). Differences: pure exploration with no exploitation payoff funded from the same budget, no value weights, adaptive allocation rather than ex-ante commitment, and no no-learning benchmark.
  - [NeurIPS PDF](https://proceedings.nips.cc/paper_files/paper/2011/file/c4851e8e264415c4094e4e85b0baa7cc-Paper.pdf); [search summary](https://mlanthology.org/neurips/2011/gabillon2011neurips-multibandit)
- **[Overlap: High (structure)] Guha, S. (2026b). "Budgeted Bayesian Bandits for Future Utilization." arXiv:2610.24156 (16 Oct 2026).**
  - Model: exploration has a hard budget and must happen before exploitation, which is the "budgeted learning" problem.
  - Result: the Lagrangian-duality 1/3-approximation of Guha–Munagala and the 4/27-approximation of Ma are both tight. A new efficient algorithm reaches 0.43, and with bounded exchangeable observations an algorithm approaches 1 − 1/e (≈ 0.63), asymptotically tight against natural LP relaxations. It also gives stopping certificates for sequential model evaluation.
  - Relation: the algorithmic literature closest to the paper's "probe τ, then commit" structure with a budget over independent Bayesian units. Here the planner explores arms and then exploits one; in the paper, every unit exploits its own market with its own budget, and the planner weights the units by value.
  - [arXiv abstract page](https://arxiv.org/abs/2610.24156)
- **[Overlap: Medium–High] Guha, S., & Munagala, K. (2007). "Approximation Algorithms for Budgeted Learning Problems." STOC 2007, pp. 104–113. DOI 10.1145/1250790.1250807.** The foundational budgeted-learning paper: an exploration budget over independent priors, then commit. [Crossref](https://doi.org/10.1145/1250790.1250807)
- **[Overlap: Medium–High] Guha, S. (2026a). "Planned Restlessness: Delayed Meta Bandits with Budgets." arXiv:2610.38955 (28 Oct 2026; cs.LG, cross-listed cs.DS). This is the arXiv ID the coordinator flagged, verified.**
  - Model: episodic finite-horizon Bayesian bandits ("meta-bandits") with recurring unknown priors, known feedback delays, per-episode caps and total budgets.
  - Method: a planning LP values an experiment by its current reward, resource consumption and continuation value. Dual prices separate the problem into arm-local programs, a Lagrangian decomposition of weakly coupled units, and certify policies such as hierarchical Thompson sampling.
  - Result: with stationary priors, bounded lags and nonbinding budgets, posterior sampling pays O(√N) over N episodes for not knowing the priors. For a single undelayed episode with per-arm caps T/X, the LP-relative factor is 1 + (2πX)^(−1/2) + O(1/X), with a matching lower bound on the leading term.
  - Relation: the most recent formal treatment of budgets plus learning across independent units through dual prices. That is exactly the decomposition the paper's planner problem admits, max v1·V(a) + v2·V(T−a), which is separable in the units. The paper is about how non-concavity of V from learning shapes the split. Guha's is about approximation guarantees for a single learner's plan.
  - [arXiv abstract page](https://arxiv.org/abs/2610.38955); full text read via alphaXiv, including the introduction and related work
- **[Overlap: Medium] Adelman, D., & Mersereau, A. J. (2008). "Relaxations of Weakly Coupled Stochastic Dynamic Programs." Operations Research 56(3):712–727. DOI 10.1287/opre.1070.0445.**
  - The standard framework for independent subproblems linked by shared resource constraints, using Lagrangian and LP relaxations. Guha (2026a) describes this as "Lagrangian relaxation separates weakly coupled dynamic programs by pricing their shared resources".
  - Relation: the paper's planner problem is a static weakly coupled program, and citing this frames the "teams of bandits" structure formally.
  - [Crossref](https://doi.org/10.1287/opre.1070.0445); [Guha 2026a related work](https://arxiv.org/abs/2610.38955)
- **[Overlap: Medium] Gittins, J. C. (1979). "Bandit Processes and Dynamic Allocation Indices." Journal of the Royal Statistical Society Series B 41(2):148–164. DOI 10.1111/j.2517-6161.1979.tb01068.x.**
  - The classic optimal allocation of effort across independent learning projects by index (recalled).
  - Relation: a reviewer may cite it as "allocation across independent bandit units is the Gittins problem". The difference is sequential one-at-a-time effort versus an ex-ante budget split with concurrent units.
  - [Crossref](https://doi.org/10.1111/j.2517-6161.1979.tb01068.x)
- **[Overlap: High (application)] Nuara, A., Trovò, F., Gatti, N., & Restelli, M. (2018). "A Combinatorial-Bandit Algorithm for the Online Joint Bid/Budget Optimization of Pay-per-Click Advertising Campaigns." AAAI 2018, 32(1). DOI 10.1609/aaai.v32i1.11888. Journal version: Nuara et al. (2022). "Online Joint Bid/Daily Budget Optimization of Internet Advertising Campaigns." Artificial Intelligence 305:103663. DOI 10.1016/j.artint.2022.103663; arXiv:2003.01452.**
  - Model: an advertiser allocates a daily budget over "several, even thousands" of campaigns and sets bids. Clicks as a function of bid and budget are learned per campaign with Gaussian processes.
  - Method: a combinatorial semi-bandit that solves a multiple-choice knapsack each day.
  - Result: O(√T) high-probability regret, plus a real deployment spending about €1,000 per day for over a year.
  - Relation: planner + budget split across campaigns + learning, so (a)+(b)+(c) in application. The learning sits with the central planner, re-allocation is daily rather than ex ante, the campaigns are not autonomous learners, and there is no learning-vs-no-learning window.
  - [arXiv abstract](https://arxiv.org/abs/2003.01452); [Crossref AAAI](https://doi.org/10.1609/aaai.v32i1.11888); [Crossref AIJ](https://doi.org/10.1016/j.artint.2022.103663)
- **[Overlap: Medium–High (application)] Ge, L., Xu, Y., Chu, J., Cramer, D., Li, F., Paulson, K., & Song, R. (2024). "Multi-Task Combinatorial Bandits for Budget Allocation." arXiv:2409.00561.**
  - Model: budget allocation across ad lines within campaigns, for advertisers running hundreds of campaigns. A Bayesian hierarchical model shares information across campaigns, ad lines and budget sizes, with Thompson sampling.
  - Result: offline and online tests are reported to show robustness and higher cumulative returns.
  - [arXiv abstract](https://arxiv.org/abs/2409.00561)
- **[Overlap: Medium] Zuo, J., & Joe-Wong, C. (2021). "Combinatorial Multi-armed Bandits for Resource Allocation." 55th CISS, pp. 1–4. DOI 10.1109/CISS50987.2021.9400228; arXiv:2105.04373.**
  - Model: a decision maker repeatedly allocates budgets across resources/users and learns each user's value of resources from feedback.
  - [arXiv abstract](https://arxiv.org/abs/2105.04373); [Crossref](https://doi.org/10.1109/ciss50987.2021.9400228)
- **[Overlap: Medium–High] Bachoc, F., Cesa-Bianchi, N., Cesari, T., & Colomboni, R. "Online Budget Allocation with Censored Semi-Bandit Feedback." arXiv:2508.05844 (v1 Aug 2025; v3 Nov 2026; "Accepted at NeurIPS 2026").**
  - Model: each round, allocate a budget over K tasks. Task k succeeds with an unknown nondecreasing probability of its allocation, and its reward is observed only on success. Applications include splitting bids across simultaneous auctions.
  - Result: polylogarithmic instance-dependent regret under diminishing returns, Õ(K√T) worst-case regret for general nondecreasing curves, and a matching Ω(K√T) lower bound even with full feedback.
  - Relation: a learner splitting a budget across independent tasks, close to (b)+(e). Its finding that only diminishing returns allow polylogarithmic regret links to the paper's non-concave V. The paper's planner faces non-concavity from learning itself, and the units learn internally.
  - [arXiv abstract](https://arxiv.org/abs/2508.05844)
- **[Overlap: High (spirit)] Latypov, I., Suvorikova, A., Kroshnin, A., Gasnikov, A., & Dorn, Y. "Managing Self-Learning Experts under Per-Round Budget Constraints." arXiv:2510.22654 (v3, 28 Sep 2026).**
  - Model: a manager of a pool of K self-learning experts, which are bandit or RL algorithms and parametric models, selects one expert to act and at most M ≤ K to train each round, a per-round learning budget. The motivating example is "managing a portfolio of bandit or RL algorithms".
  - Result: M-LCB trains by lower confidence bounds and deploys by upper confidence bounds. Regret is Õ(√(KT/M) + (K/M)^(1−α)·T^α) when experts have Õ(T^α) regret, with a matching minimax lower bound.
  - Relation: literally "a planner managing a team of learners under a budget". Differences:
    - the budget is training slots per round, allocated adaptively;
    - the experts compete for one deployment in a shared environment;
    - there are no value weights or market structure;
    - there is no learning-vs-no-learning allocation comparison.
  - [arXiv / alphaXiv full text](https://arxiv.org/abs/2510.22654)
- **[Overlap: Medium] Agarwal, A., Luo, H., Neyshabur, B., & Schapire, R. E. (2017). "Corralling a Band of Bandit Algorithms." COLT 2017, PMLR 65. arXiv:1612.06246.**
  - Model: a master algorithm combines base bandit algorithms and must not "starve" a base learner that would eventually win. Method: online mirror descent with a special mirror map.
  - Relation: "bandits over bandits" (model selection) for one task, as opposed to allocation across separate tasks.
  - [arXiv abstract](https://arxiv.org/abs/1612.06246); [PMLR v65 index](https://proceedings.mlr.press/v65/)
- **[Overlap: Medium–Low] Badanidiyuru, A., Kleinberg, R., & Slivkins, A. (2018). "Bandits with Knapsacks." Journal of the ACM 65(3):1–55. DOI 10.1145/3164539 (FOCS 2013); arXiv:1305.2545.**
  - Model: a single learner under budget and supply limits.
  - Result: the optimal dynamic policy may "significantly outperform" the best fixed arm. Two algorithms, balanced exploration and primal-dual with multiplicative updates, achieve regret optimal up to polylogarithmic factors.
  - Relation: the default "budgeted bandits" citation a reviewer will raise. It has one learner, not a planner over learners.
  - [arXiv abstract](https://arxiv.org/abs/1305.2545); [Crossref](https://doi.org/10.1145/3164539)
- **[Overlap: Low–Medium] Zhou, D. P., & Tomlin, C. J. (2018). "Budget-Constrained Multi-Armed Bandits with Multiple Plays." AAAI 2018.** A single player picks several arms per round under a budget. Authors as given by the search summary. [AAAI OJS](https://ojs.aaai.org/index.php/AAAI/article/view/11629)
- **[Overlap: Medium] Zibaie, A., Hutchinson, S., Pedarsani, R., & Alizadeh, M. (2025). "The Safety-Privacy Tradeoff in Linear Bandits." ISIT 2025 (per arXiv comment). arXiv:2504.16371.**
  - Model: "a collection of linear stochastic bandit problems, each modeling the random response of different agents", coupled by a global safety constraint. "A central coordinator must choose actions to play on each bandit", and agents share data under local differential privacy.
  - Relation: a coordinator over several independent bandits coupled by an aggregate constraint, (a)+(e) with a coupling constraint. The constraint is safety, not money, and there are no value weights and no learning-vs-no-learning comparison.
  - [arXiv abstract](https://arxiv.org/abs/2504.16371)
- **[Overlap: Medium] Cao, X., Li, J., Fu, Z., & Bayen, A. M. (2026). "Who Bears the Burden? Learning Responsibility for Shared Constraints in Multi-Agent Reinforcement Learning." arXiv:2610.07491.**
  - Model: multiple agents share a cost budget. A common Lagrange multiplier enforces the aggregate budget but does not allocate responsibility. LiRA learns each agent's share of the multiplier by optimizing social welfare.
  - Result: in convex games, varying the shares traces a family of normalized generalized Nash equilibria.
  - Relation: a shared budget among heterogeneous learning agents, (b)+(c). It is a decentralized game and does not split the budget ex ante across independent units.
  - [arXiv abstract](https://arxiv.org/abs/2610.07491)
- **[Overlap: Medium] Chen, X., Lin, Q., & Zhou, D. "Statistical Decision Making for Optimal Budget Allocation in Crowd Labeling." SSRN 2014, DOI 10.2139/ssrn.2408163 (journal venue, believed JMLR 2015, unverified).**
  - (Recalled) a fixed labeling budget is allocated sequentially across many items with unknown binary true labels, as a Bayesian MDP, using an optimistic knowledge-gradient policy.
  - Relation: a structural analog, with a budget across many independent units, a binary latent state and Bayesian posteriors. The objective there is accuracy, not exploitation value.
  - [SSRN DOI](https://doi.org/10.2139/ssrn.2408163)
- **[Overlap: Low–Medium] Multi-task / hierarchical / meta-bandits, which share information through priors and have no budget:**
  - Hong, J., Kveton, B., Zaheer, M., & Ghavamzadeh, M. (2022). "Hierarchical Bayesian Bandits." AISTATS 2022, PMLR 151. [PMLR v151 index](https://proceedings.mlr.press/v151/)
  - Basu, S., Kveton, B., Zaheer, M., & Szepesvári, C. (2021). "No Regrets for Learning the Prior in Bandits." NeurIPS 2021. [NeurIPS 2021 index](https://papers.nips.cc/paper_files/paper/2021)
  - Kveton, B., et al. (2021). "Meta-Thompson Sampling." ICML 2021, PMLR 139:5884–5893. Cited from Guha 2026a's reference list (secondary). [Guha 2026a](https://arxiv.org/abs/2610.38955)
- **[Overlap: Low–Medium] LLM-agent orchestration and budgets (2026), relevant to the authors' planned extension:**
  - Antony Oliver, M. C., Jiang, L., Anampiu, A. B., Almahmoud, E., Quinzan, F., & Bhatt, U. (2026). "Learning to Orchestrate Agents under Uncertainty." arXiv:2605.27073. Orchestration is a bandit over heterogeneous agents, regularized by optimal-transport distance to a reference output distribution, with O(√T) regret. No budget formulation. [arXiv](https://arxiv.org/abs/2605.27073)
  - Samway, K., D'souza, D., Darwiche Domingues, O., Fadaee, M., Yi-Chern, T., & Dziri, N. (2026). "Scaling Inference-Time Compute with Teams of Coding Agents." arXiv:2610.17471. Treats team design as compute allocation. Teams beat solo agents at 3–7× cost, planning is "the most valuable use of workers", and a well-allocated heterogeneous 17-agent team comes within 1.4 points of a strong 5-agent team at 70% lower cost. Empirical, with no learning-theoretic planner. [arXiv](https://arxiv.org/abs/2610.17471)
  - Zhu, G., & Wang, C. (2026). "Fault-Tolerant Budget Conservation in Distributed Multi-Agent Delegation." arXiv:2610.00349. Budget flows parent→child through a delegation DAG with escrow and reservation, with proofs of conservation. It is systems/formal methods with no learning. [arXiv](https://arxiv.org/abs/2610.00349)
- **"Teams of bandits" as a phrase:** the web search found no paper using the term. The closest are "bandit teams" (Bıyık et al. 2022), "teams of agents" (Chakraborty et al. 2017) and budgeted multiple-play bandits. [Web search results](https://ojs.aaai.org/index.php/AAAI/article/view/11629)

### Inferences
- Checklist for this strand:
  - (a) Planner: Yes in most, but the planner is itself the learner (Nuara, Ge, Zuo, Bachoc, Gabillon, Guha) or a manager of learners for one task (Latypov, CORRAL).
  - (b) Shared budget: Yes.
  - (c) Values: unit-specific response curves (Nuara, Bachoc). Explicit value weights v_i on independent learning units do not appear.
  - (d) With vs. without learning: No. Benchmarks are regret against the oracle allocation or LP relaxations.
  - (e) Environment: mostly independent units or tasks, the closest match to the paper.
- The paper's distinctive design is delegated learning plus ex-ante commitment: units learn internally through ETC, and the planner fixes (B_i, τ_i) at time 0 without observing intermediate outcomes. In the closest bandit-allocation papers the planner learns centrally and re-allocates over time. The paper should frame this as a feature with a practical motivation (campaign budgets and test windows are set up front; LLM sub-agents receive token budgets when spawned). It should also note the natural extension: a planner who re-allocates after observing probe outcomes, which connects to Nuara et al., Bachoc et al. and Gabillon et al.

### Gaps
- Not checked: whether Guha 2026a or 2026b has been extended to multiple concurrently exploiting units with value weights. Both are 3–4 weeks old, with no venue.
- Authors of arXiv:2510.16221 ("Heterogeneous Multi-Agent Task-Assignment with Uncertain Execution Times and Preferences", Purdue/MSU), in which a central planner assigns recurring tasks to team members via combinatorial bandits, were not retrieved. [arXiv](https://arxiv.org/html/2510.16221v1)
- No paper was found with the exact phrase "multi-agent bandits with a shared budget" or a "central planner allocating budget to multiple bandit learners". This absence is itself the positioning claim, but search coverage is limited to the arXiv, alphaXiv and web indexes used.

## Q8. The 3–5 closest works; what is and is not already done; what a reviewer is most likely to cite

### Takeaway
The paper's combination is (a) planner + (b) ex-ante split of one budget + (c) value-weighted units + (d) an explicit learning-vs-no-learning comparison of value and allocation + (e) independent markets, with ETC learning delegated inside each unit. No verified work contains it. The closest works each have three of the five elements at most. The claims "multiple learners", "ETC with multiple agents", "budget allocation across campaigns with bandits", "budgeted exploration across independent units" and "principals setting budgets for learning agents" are all already taken. The defensible novelty is the value-of-learning window and the way learning reshapes the optimal split.

### Cited Findings
- **Closest works (ranked):**
  1. **Deng, Golrezaei, Jaillet, Liang & Mirrokni (ICML 2023), "Multi-channel Autobidding with Budget and ROI Constraints".** An advertiser splits budget across channel autobidders and learns the per-channel budgets; budget-only levers suffice for the global optimum. Has (a), (b), (c) and independent channels. Lacks (d), the units are not modelled as ETC learners, and the planner learns over time rather than committing ex ante. [arXiv](https://arxiv.org/abs/2302.01523)
  2. **Nuara, Trovò, Gatti & Restelli (AAAI 2018; AIJ 2022).** A daily budget split across many campaigns with GP-bandit learning and an O(√T) regret bound. Has (a), (b), (c) via campaign-specific response curves, and (e). Lacks (d); the learning is central and sequential. Ge et al. (2024) and Bachoc et al. (NeurIPS 2026) are close variants. [arXiv](https://arxiv.org/abs/2003.01452); [arXiv Ge et al.](https://arxiv.org/abs/2409.00561); [arXiv Bachoc et al.](https://arxiv.org/abs/2508.05844)
  3. **Budgeted exploration across independent learning problems:** Gabillon et al. (NIPS 2011, multi-bandit BAI under one sampling budget); Guha & Munagala (STOC 2007) and Guha (arXiv:2610.24156, 2026), budgeted learning that explores and then exploits; and Guha (arXiv:2610.38955, 2026), meta-bandits with budgets and dual-price decomposition. Has (a), (b) and (e), with ETC structure. Lacks value-weighted concurrent exploitation and (d). [Gabillon et al.](https://proceedings.nips.cc/paper_files/paper/2011/file/c4851e8e264415c4094e4e85b0baa7cc-Paper.pdf); [Guha 2026b](https://arxiv.org/abs/2610.24156); [Guha 2026a](https://arxiv.org/abs/2610.38955)
  4. **Latypov, Suvorikova, Kroshnin, Gasnikov & Dorn (arXiv:2510.22654).** A manager of a portfolio of self-learning bandit/RL algorithms under a per-round training budget, with matching minimax rates. Has (a), (b) and multiple learners. Lacks (c) and (d), and the environment is shared. [arXiv](https://arxiv.org/abs/2510.22654)
  5. **Principals choosing budgets or parameters for learning agents:** Feng, Lucier & Slivkins (STOC 2024) and Kolumbus & Nisan (WWW 2022; NeurIPS 2022). An ex-ante choice of a learning agent's budget or parameters inside a meta-game. Lacks a single planner over multiple own units, (c) as value weights across own units, and (d). [arXiv FLS](https://arxiv.org/abs/2307.07374); [arXiv KN-a](https://arxiv.org/abs/2110.11855); [arXiv KN-b](https://arxiv.org/abs/2112.07640)
  - Economics analogs to cite alongside: Azevedo et al. (JPE 2020), a fixed experimentation budget across independent ideas whose optimal split depends on the shape of the value of experimentation, and Halac, Kartik & Liu (JPE 2017), a designer allocating a prize budget across learning agents. [Crossref Azevedo](https://doi.org/10.1086/710607); [Crossref HKL](https://doi.org/10.1086/693040)
- **Already done (cannot be claimed as new):**
  - Multiple learners sharing one environment, cooperating (Q1) or competing (Q2, Q4, Q5).
  - ETC protocols in multi-agent settings: Musical Chairs; Liu–Mania–Jordan; Pagare–Ghosh. [arXiv](https://arxiv.org/abs/1512.02866); [arXiv](https://arxiv.org/abs/2408.08690)
  - Budget-paced learning bidders and their equilibria (Balseiro–Gur; Gaitonde et al.; Fikioris–Tardos). [Crossref](https://doi.org/10.1287/mnsc.2018.3174)
  - Central budget allocation across campaigns via bandits (Nuara et al.; Ge et al.; Bachoc et al.; Deng et al.).
  - Budgeted exploration across independent arms or bandits (Gabillon; Guha–Munagala; Guha 2026a,b).
  - Principals configuring learning agents' budgets (Feng–Lucier–Slivkins).
  - Competition reducing exploration (Aridor et al. 2025). [Crossref](https://doi.org/10.1145/3711831)
- **Not found (positioning claims supported by these searches):**
  1. A planner that commits budgets and probe lengths ex ante to autonomous ETC learning units in independent markets.
  2. A characterization of the budget window in which a unit's learning creates value relative to a no-learning benchmark W, including the jump of V'(B)/W'(B) at entry and its subsequent decline.
  3. A comparison of the value-weighted optimal split with and without learning, showing more skew toward the high-value unit when the low-value unit cannot afford to learn, and more balance once both learn.
  4. The first-price RTB instantiation with q_θ(b) = b/(b+θ) and payment only on wins.
  - The nearest theoretical relatives for points 2–3 are the value-of-information non-concavity results (Chade–Schlee 2002, building on Radner–Stiglitz) and the lean-vs-big experimentation result of Azevedo et al. (2020). [Crossref](https://doi.org/10.1006/jeth.2001.2960); [Crossref](https://doi.org/10.1086/710607)

### Inferences
- Strand-level summary of (a)–(e), which is my synthesis of the checklists in Q1–Q7:

| Strand | (a) Planner/coordinator | (b) Shared budget split | (c) Different values/weights | (d) With vs. without learning | (e) Environment |
|---|---|---|---|---|---|
| Cooperative MAB (Q1) | No (peers; fusion-center benchmark) | No (communication limits only) | Rare (heterogeneous instances) | No (collaboration vs. none) | Shared |
| Multi-player/collisions (Q2) | No (centralized assignment benchmark) | No (arms as shared capacity) | Some (player–arm means) | No | Shared, interfering |
| Federated (Q3) | Server = aggregator | Communication budget only | Personalization/mixing weights | No | Global model + local heterogeneity |
| Competing/matching (Q4) | Platform matches, no budgets | No | Yes (preferences) | Aridor et al.: greedy vs. exploring | Shared, competitive |
| Auctions (Q5) | Mostly no; Deng et al. (advertiser over channels); principals config agents | Deng et al. yes; else own budgets | Yes | No | Shared auctions (Deng et al.: separate channels) |
| Economics (Q6) | Incentivized exploration, contests, A/B testing: yes; strategic experimentation: no | Payments/prizes/traffic | Mostly symmetric | Equilibrium vs. efficient; Azevedo implicit | Common state (except A/B testing) |
| Coordinated/budget (Q7) | Yes, but the planner itself learns | Yes | Response curves, not value weights | No | Mostly independent |
| **This paper** | **Yes (non-learning planner)** | **Yes, ex ante** | **Yes (v1 > v2)** | **Yes (V vs. W; window; skew)** | **Independent markets** |

- **Reviewers' most likely citations, by objection:**
  1. "This is just budgeted bandits": Bandits with Knapsacks (Badanidiyuru, Kleinberg & Slivkins, JACM 2018), and possibly Gittins (1979) for allocating across independent units.
  2. "Pacing/autobidding already covers this": Balseiro & Gur (MS 2019); Deng et al. (ICML 2023) on multi-channel budgets; possibly Feng, Lucier & Slivkins (STOC 2024).
  3. "Multi-agent bandits have been studied": Landgren et al. (2016) or Martínez-Rubio et al. (2019) for cooperative MAB, and the Boursier & Perchet survey (JMLR 2024) for multi-player bandits.
  4. "Teams that learn" in economics: Bolton & Harris (1999); Keller, Rady & Cripps (2005).
  5. "Campaign budget allocation with bandits": Nuara et al. (AAAI 2018).
  6. For the AI-agent extension: CORRAL (COLT 2017) and model-selection/meta-learner management (Latypov et al.).
- **Suggested one-sentence positioning, built from the verified literature:**

  > Unlike multi-agent bandits, where learners share one environment and pool information or compete, and unlike centralized budget-allocation bandits, where the planner itself learns and re-allocates, we study a non-learning planner who commits budgets ex ante to autonomous explore-then-commit units in independent markets. We show that the option value of learning makes unit value non-concave in budget, creating a bounded learning window and a learning-induced shift in the value-weighted split.

### Gaps
- The searches did not cover the marketing literature on S-shaped advertising response, where non-concave response also produces concentrated budget allocations, or explore-then-commit theory for a single learner. Adjacent researchers may cover these; I did not verify any citation there.
- I did not find, and so cannot rule out, IS/marketing papers (for example in Management Science, ISR or Marketing Science) on multi-campaign budget allocation under learning by autonomous campaign agents. This strand was outside my search scope.
- Content of the most recent 2026 preprints (Guha 2026a,b; Latypov et al. v3; Bachoc et al.) is preprint-stage, and claims should be cited as such.
