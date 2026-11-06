# Economic theory for budget-funded learning: value-of-information nonconcavity, optimal experimentation, dynamic information acquisition and stopping, informativeness, delegated/organizational experimentation, and allocation of resources across learning units

Notes positioning "Orchestrating Agent Teams: Budget Allocation in Real-Time Bidding" (Yang, Zhu & Mookerjee; WITS 2026). Compiled 2026-11-06.

How things were checked:
- Citations were checked against Crossref/OpenAlex metadata, IDEAS/RePEc, publisher pages or arXiv during this session.
- "Abstract-verified" means the result comes from the paper's abstract or text, which was read.
- "Standard summary" means no abstract could be retrieved, so the result comes from well-established knowledge of the paper. Treat these as lower confidence.
- "Unverified" means the item could not be confirmed.
- Page ranges marked with * have a first page confirmed by Crossref (JSTOR-hosted items). The last page comes from the standard citation and was not separately checked.
- Overlap ratings measure closeness to the paper's problem. **High** means the same mechanism or problem, or a direct anchor. **Medium** means a related mechanism. **Low** means background.

---

## Q1. Nonconcavity in the value of information (Radner–Stiglitz and successors): consequences for demand for information, thresholds and discontinuous adoption

### Takeaway
A large, verified literature shows that the marginal value of a small amount of information is often zero. The value of information is therefore not globally concave, and demand for information is lumpy: it is zero up to a choke point and then jumps. This is the natural theoretical anchor for the paper's abrupt, fixed-cost-like entry into learning. Two further results matter for the planner's split. Wilson's informational economies of scale explain why learning pays only above a budget scale. Azevedo et al. (2020) show that when such nonconcave "production functions of data" are summed under a common resource constraint, the optimal allocation concentrates resources when they are scarce and spreads them when they are abundant. That is the same pattern as "skewed toward the senior team, then balanced".

### Cited Findings
- **Radner, R. & Stiglitz, J. E. (1984). "A Nonconcavity in the Value of Information." In M. Boyer & R. E. Kihlstrom (eds.), *Bayesian Models in Economic Theory* (Studies in Bayesian Econometrics 5), Elsevier/North-Holland, Amsterdam, pp. 33–52.**
  - No DOI. The page range comes from bibliographic records found by web search; the chapter itself was not opened.
  - Model: a single Bayesian decision maker. The information structure is indexed by an "amount of information", with null information at zero. Finite states and finite signal realizations are assumed.
  - Result: under regularity conditions, the marginal value of a small amount of information is zero. Since free information is weakly valuable, information that is not useless must show increasing marginal returns over some range, so its value cannot be globally concave.
  - Relation (Overlap: **High**, anchor): this is the canonical theoretical anchor for the paper's finding that learning creates no value for small budgets and then "switches on" abruptly.
  - Caveat: Azevedo et al. (2020, fn. 17) note that in Radner–Stiglitz's leading example (p. 40) the quantity of information is measured by the signal–state correlation, which is roughly √n. The convexity therefore partly depends on the units of measurement.
  - Sources: [Chade–Schlee abstract describing R–S](https://asu.elsevierpure.com/en/publications/another-look-at-the-radner-stiglitz-nonconcavity-in-the-value-of-); [Azevedo et al. WP discussion of R–S](https://www.gwern.net/doc/statistics/decision/2019-azevedo.pdf); [De Lara–Gilotte record](https://ideas.repec.org/p/hal/journl/hal-00716396.html)
- **Chade, H. & Schlee, E. (2002). "Another Look at the Radner–Stiglitz Nonconcavity in the Value of Information." *Journal of Economic Theory* 107(2): 421–452.** DOI [10.1006/jeth.2001.2960](https://doi.org/10.1006/jeth.2001.2960).
  - Abstract-verified. R–S assume finitely many states and signal realizations, "assumptions which preclude most analyses of optimal information acquisition".
  - Chade and Schlee give sufficient conditions for the nonconcavity in a general framework, illustrate them with examples, and discuss the result's robustness and "the difficulties involved in getting the value of information to be globally concave".
  - Relation (Overlap: **High**, anchor): cite this to argue that the paper's threshold is generic rather than an artifact of the binary-state, binomial-signal model.
  - Source: [ASU Pure abstract](https://asu.elsevierpure.com/en/publications/another-look-at-the-radner-stiglitz-nonconcavity-in-the-value-of-)
- **De Lara, M. & Gilotte, L. (2007). "A Tight Sufficient Condition for Radner–Stiglitz Nonconcavity in the Value of Information." *Journal of Economic Theory* 137(1): 696–708.** DOI [10.1016/j.jet.2007.01.014](https://doi.org/10.1016/j.jet.2007.01.014).
  - Abstract-verified. The paper defines an "infinitesimal information distance variation" (IIDV). IIDV = 0 is sufficient for zero marginal value of information at the null, whatever the decision maker's preferences.
  - The condition is tight: if IIDV > 0, there is a payoff function under which the marginal value at the null is positive.
  - Relation (Overlap: **Medium**): gives a checkable condition on the paper's experiment family. The family would need a continuous embedding, for example probing intensity or probing probability, because τ is discrete.
  - Source: [IDEAS/HAL record](https://ideas.repec.org/p/hal/journl/hal-00716396.html)
- **Keppo, J., Moscarini, G. & Smith, L. (2008). "The Demand for Information: More Heat than Light." *Journal of Economic Theory* 138(1): 21–50.** DOI [10.1016/j.jet.2007.03.003](https://doi.org/10.1016/j.jet.2007.03.003).
  - Content from the IDEAS record summary; the exact abstract wording was not retrieved.
  - The paper gives a general theory of the value of Bayesian information and its static demand, using a Brownian-motion signal. With two states the problem reduces to the heat equation.
  - The marginal value of information is initially zero and the value is non-concave.
  - Demand is "lumpy": as the price rises, demand suddenly chokes off to zero. The marginal value vanishes exponentially fast, which yields logarithmic demand.
  - Relation (Overlap: **High**, anchor): the cleanest anchor for "abrupt entry". As the stakes (here, the budget) rise, the optimal amount of probing jumps from zero to a strictly positive level rather than rising continuously from zero.
  - Source: [IDEAS record](https://ideas.repec.org/a/eee/jetheo/v138y2008i1p21-50.html)
- **Moscarini, G. & Smith, L. (2002). "The Law of Large Demand for Information." *Econometrica* 70(6): 2351–2366.** DOI [10.1111/1468-0262.00378](https://doi.org/10.1111/1468-0262.00378).
  - Abstract-verified (SSRN version). Building on large deviation theory, the paper gives a generically complete asymptotic order on samples of i.i.d. signals in finite-state, finite-action models.
  - The marginal value of an additional signal is "eventually exponentially falling in quantity, and higher for lower quality signals".
  - At low prices, information demand is "asymptotically a constant times the log price, and falling in the signal quality for a given price".
  - Relation (Overlap: **High**, anchor for the large-τ regime): beyond the entry point, the value of probing is eventually concave in the number of probes. When the per-probe cost is fixed and the stakes scale with the budget, the optimal probing length should grow only logarithmically in the stakes (see Inferences).
  - Source: [SSRN abstract](https://doi.org/10.2139/ssrn.300080)
- **Azrieli, Y. (2014). "Comment on 'The Law of Large Demand for Information'." *Econometrica* 82(1): 415–423.** DOI [10.3982/ecta11127](https://doi.org/10.3982/ecta11127).
  - The citation was verified; Crossref metadata omit the author, who is given here from the standard citation. The content was not read.
  - Relation (Overlap: Low): cite alongside Moscarini–Smith (2002) if asymptotic demand formulas are used.
- **Kihlstrom, R. (1974a). "A Bayesian Model of Demand for Information about Product Quality." *International Economic Review* 15(1): 99–118\*.** DOI [10.2307/2526092](https://doi.org/10.2307/2526092).
  - Abstract-verified (opening text). Consumers buy information "because it helps [them] to make better purchases": a derived demand that standard consumer theory does not handle.
  - Companion paper: **Kihlstrom, R. (1974b). "A General Theory of Demand for Information about Product Quality." *Journal of Economic Theory* 8(4): 413–439.** DOI [10.1016/0022-0531(74)90019-2](https://doi.org/10.1016/0022-0531(74)90019-2).
  - Relation (Overlap: **Low–Medium**): an early root of the derived demand for information that R–S and later work analyze.
- **Wilson, R. (1975). "Informational Economies of Scale." *Bell Journal of Economics* 6(1): 184–195\*.** DOI [10.2307/3003221](https://doi.org/10.2307/3003221).
  - Abstract-verified. When technological information can be bought at a resource cost, the firm faces economies of scale "even though the technology of physical production has no economies of scale".
  - "Better information justifies a higher scale of operations and vice versa." Combined, the two effects "lead to an unbounded optimal scale of operations".
  - Relation (Overlap: **High**, anchor for a threshold in budget space): information applied to a larger budget is worth more, while probing cost is largely independent of the budget. Learning therefore pays only above a budget scale.
  - Contrast: the paper's window is bounded above. Wilson's scale effect alone has no upper bound.
- **Azevedo, E. M., Deng, A., Montiel Olea, J. L., Rao, J. & Weyl, E. G. (2020). "A/B Testing with Fat Tails." *Journal of Political Economy* 128(12): 4614–4672.** DOI [10.1086/710607](https://doi.org/10.1086/710607). Abstract-verified; theorem statements from the 2019 working paper.
  - Model: a firm allocates N experimental users across many ideas. Each idea's quality has a prior with power-law tail index α, and the firm implements an idea if its posterior mean is positive.
  - Proposition 2 ("Production Function Decomposition"): the firm's payoff equals Σ E[Δᵢ]⁺ + Σ fᵢ(nᵢ). The problem therefore reduces to maximizing a sum of per-idea production functions of data subject to Σ nᵢ ≤ N.
  - Theorem 2 (small n): the marginal product of data f′(n) is proportional to n^((α−3)/2).
    - Thin tails (α > 3): marginal product is zero at n = 0 and increasing, giving increasing returns. The authors say this convexity "has been formalized in a classic paper by Radner and Stiglitz (1984)".
    - Fat tails (α < 3): marginal product is infinite at n = 0 and decreasing.
  - Corollary 1: with thin tails and small N, "the firm should allocate all experimental resources to one idea" ("go big"). With fat tails, test all ideas ("go lean").
  - Remark 1: because returns eventually decrease, abundant resources should be spread across many ideas.
  - Theorem 1: for large n, the marginal product decreases as 1/n².
  - Empirically, Bing's EXP platform shows α < 3.
  - Relation (Overlap: **High**, closest formal analog): this is the planner's problem max Σ vᵢV(Bᵢ) with nonconcave V. The paper's "skew toward the senior team when the junior cannot afford to learn, balance once both learn" is the two-unit, budget-funded counterpart of "go big when resources are scarce, spread when abundant".
  - Differences from the paper:
    - The scarce resource is data, not money that also funds exploitation.
    - There is no market or auction feedback and no pacing rule.
    - The nonconcavity comes from thin prior tails rather than from the cost structure of probing.
  - Sources: [JPE abstract](https://doi.org/10.1086/710607); [2019 WP text](https://www.gwern.net/doc/statistics/decision/2019-azevedo.pdf)
- **Hilton, R. W. (1981). "The Determinants of Information Value: Synthesizing Some General Results." *Management Science* 27(1): 57–64.** DOI [10.1287/mnsc.27.1.57](https://doi.org/10.1287/mnsc.27.1.57).
  - Abstract-verified. Some attributes of an information system have a consistent directional effect on information value, but "attributes of the decision setting and decision maker do not".
  - Relation (Overlap: **Medium**): supports the claim that value of information need not rise monotonically with stakes such as the budget. This fits a bounded learning window. Note the venue is Management Science.

### Inferences
- **Abrupt entry is a choke-off in information demand, expressed in budget space.** Suppose the value of τ probes is convex near τ = 0 (R–S, Keppo et al.) and probing cost is roughly linear in τ (about τ·b^I·E[q_θ(b^I)]). Then the optimal τ\*(B) jumps from 0 to a positive value at some B\*: no small τ is ever optimal. This is exactly a fixed-cost-like entry.
- **The paper should name its own source of nonconcavity rather than cite R–S alone.** The R–S convexity depends on units (Azevedo fn. 17) and on regularity conditions (Chade–Schlee; De Lara–Gilotte). In the paper the plausible sources are:
  - (i) a few win/loss observations barely move the posterior and hence the paced bid;
  - (ii) the cost of probing does not scale with B, while the benefit does (Wilson's scale effect).
- **The upper end of the window is a decision-insensitivity effect, not a scale effect.** At large budgets the paced bid pushes win probabilities toward 1 in both states. The optimal action becomes insensitive to θ and the value of information falls. Wilson-type scale effects alone cannot produce this ceiling; Hilton (1981) shows that such non-monotonicity is to be expected.
- **Testable comparative static from Moscarini–Smith (2002).** Above entry, if per-probe cost is fixed and stakes are roughly proportional to B, τ\* should grow roughly like log(B) until the window's upper end bites.
- **Where the planner's nonconcavity comes from.** Each team's value is V(B) = max{V_learn(B), W(B)}. At the entry point V_learn crosses W from below, so V has a convex kink: the derivative ratio V′/W′ jumps there, as the paper reports. With such a kink the first-order condition v₁V′(a) = v₂V′(T−a) is not sufficient. The optimum avoids leaving a team just around the threshold and instead concentrates the budget, which is Azevedo et al.'s "go big" logic.

### Gaps
- The Radner–Stiglitz chapter text was not accessible. The exact regularity conditions and the page range (from bibliographic records) were not checked against the chapter itself.
- Chade–Schlee's specific sufficient conditions beyond the abstract were not read.
- Azrieli (2014) content was not read.
- The exact abstract wording of Keppo et al. (2008) was not retrieved.

---

## Q2. Optimal experimentation (learning while doing; bandits; experimentation intensity)

### Takeaway
In the classical experimentation literature, information is a by-product of payoff-generating actions:
- Rothschild (1974) and McLennan (1984) show that learning may rationally stop short (incomplete learning).
- Easley–Kiefer (1988) and Aghion–Bolton–Harris–Jullien (1991) show that whether learning is complete depends on local properties of the payoff function.
- Moscarini–Smith (2001) show that optimal experimentation intensity rises with the value at stake.

The multi-armed bandit (Gittins; Bergemann–Välimäki) is the canonical model of allocating a resource across learning projects. The index decomposition breaks with switching costs (Banks–Sundaram) and changes form under capacity constraints (Whittle). These results position the paper's learn-then-exploit (dedicated probing) design. They also suggest that part of the "fixed cost of learning" comes from separating probing from exploitation.

### Cited Findings
- **Rothschild, M. (1974). "A Two-Armed Bandit Theory of Market Pricing." *Journal of Economic Theory* 9(2): 185–202.** DOI [10.1016/0022-0531(74)90066-0](https://doi.org/10.1016/0022-0531(74)90066-0).
  - Standard summary; no abstract was retrievable. A monopolist learns demand by experimenting with prices (a two-armed bandit). With positive probability it settles forever on the inferior price (incomplete learning), and identical sellers can end up with dispersed prices.
  - Relation (Overlap: **Medium**): the founding economic model of pricing experimentation. An RTB bidder learning competition θ through its own bids is a direct descendant. Under learning-while-doing, information comes from exploitation bids themselves, so there is no dedicated probing cost.
- **McLennan, A. (1984). "Price Dispersion and Incomplete Learning in the Long Run." *Journal of Economic Dynamics and Control* 7(3): 331–347.** DOI [10.1016/0165-1889(84)90023-x](https://doi.org/10.1016/0165-1889(84)90023-x).
  - Standard summary: incomplete learning persists with a continuum of prices.
  - Relation (Overlap: Low–Medium).
- **Prescott, E. C. (1972). "The Multi-Period Control Problem Under Uncertainty." *Econometrica* 40(6): 1043–1058\*.** DOI [10.2307/1913854](https://doi.org/10.2307/1913854).
  - Standard summary: control of a process with unknown parameters, where current actions affect future information (active learning versus certainty-equivalent control).
  - Relation (Overlap: **Medium**): the paper's exploitation rule, "pace to the remaining budget given current beliefs", is a certainty-equivalent (passive-learning) rule. This literature is the reference point for asking what a fully optimal, actively learning policy would do.
- **Grossman, S. J., Kihlstrom, R. E. & Mirman, L. J. (1977). "A Bayesian Approach to the Production of Information and Learning by Doing." *Review of Economic Studies* 44(3): 533–547\*.** DOI [10.2307/2296906](https://doi.org/10.2307/2296906).
  - Standard summary: actions produce information as a joint product.
  - Relation (Overlap: Low–Medium).
- **Easley, D. & Kiefer, N. M. (1988). "Controlling a Stochastic Process with Unknown Parameters." *Econometrica* 56(5): 1045–1064\*.** DOI [10.2307/1911358](https://doi.org/10.2307/1911358).
  - Abstract-verified. Beliefs converge to a limit, which "may or may not be concentrated at the true parameter value". In some cases complete learning is optimal; in others the optimal strategy does not imply complete learning.
  - Relation (Overlap: **Medium**): benchmark for comparing explore-then-commit with learn-while-doing agents.
- **Kiefer, N. M. & Nyarko, Y. (1989). "Optimal Control of an Unknown Linear Process with Learning." *International Economic Review* 30(3): 571–586\*.** DOI [10.2307/2526776](https://doi.org/10.2307/2526776).
  - Abstract-verified. Active learning strategies weigh the information value of actions against current reward; convergence of beliefs and actions is established.
  - Relation (Overlap: Low–Medium).
- **Aghion, P., Bolton, P., Harris, C. & Jullien, B. (1991). "Optimal Learning by Experimentation." *Review of Economic Studies* 58(4): 621–654\*.** DOI [10.2307/2297825](https://doi.org/10.2307/2297825).
  - Abstract-verified. "Local properties of the payoff function (such as smoothness) are crucial in determining whether the agent eventually attains the true maximum payoff or not."
  - Relation (Overlap: **Medium**): RTB payoffs are smooth in the bid (q_θ(b) = b/(b+θ)). This is the regime where incomplete learning by a learn-while-doing bidder is plausible.
- **Keller, G. & Rady, S. (1999). "Optimal Experimentation in a Changing Environment." *Review of Economic Studies* 66(3): 475–507.** DOI [10.1111/1467-937x.00095](https://doi.org/10.1111/1467-937x.00095).
  - Abstract-verified. A monopolist faces a demand curve that switches randomly. There are two regimes, with the optimal policy depending discontinuously on the parameters:
    - "extreme experimentation and good tracking";
    - "moderate experimentation and poor tracking", in which the agent can become "trapped".
  - Relation (Overlap: **Medium–Low**): if RTB competition switches over time (for example by daypart), a one-shot probing phase goes stale. This is a robustness caveat for learn-then-exploit.
- **Bergemann, D. & Välimäki, J. (1996). "Learning and Strategic Pricing." *Econometrica* 64(5): 1125–1149\*.** DOI [10.2307/2171959](https://doi.org/10.2307/2171959).
  - Abstract-verified. With exogenous prices the buyer's problem is a multi-armed bandit. With price competition, all Markov perfect equilibria are efficient and prices below marginal cost sustain experimentation.
  - Relation (Overlap: Low–Medium): the price of experimentation is set in a market, as in RTB, where the "price" of a probe is the bid paid on a win.
- **Bergemann, D. & Välimäki, J. (2008). "Bandit Problems." In *The New Palgrave Dictionary of Economics* (2nd ed.), pp. 1–7.** DOI [10.1057/978-1-349-95121-5_2386-1](https://doi.org/10.1057/978-1-349-95121-5_2386-1).
  - Abstract-verified. The multi-armed bandit is "a statistical decision model of an agent trying to optimize his decisions while improving his information at the same time", modelling the exploration–exploitation trade-off.
  - Relation (Overlap: **Medium**): the survey entry to cite for the bandit framing.
  - Note: the full Cowles discussion-paper version could not be downloaded in this session.
- **Moscarini, G. & Smith, L. (2001). "The Optimal Level of Experimentation." *Econometrica* 69(6): 1629–1644.** DOI [10.1111/1468-0262.00259](https://doi.org/10.1111/1468-0262.00259).
  - Abstract-verified. An impatient decision maker runs variable-size experiments at an increasing, strictly convex cost before an irreversible action, modelled as control of the variance of a diffusion with uncertain mean.
  - Results:
    - (a) "the optimal experimentation level rises in the Bellman value";
    - (b) experimentation costs drift up;
    - (c) a more impatient decision maker may experiment more.
  - Intuition: the decision maker acts like a competitive firm "producing information at an increasing marginal cost and selling it to himself".
  - Relation (Overlap: **High**, anchor for experimentation intensity): in RTB, a probe's informativeness per period rises with the bid up to b^I, while its spend b²/(b+θ) is convex in b. That is the M–S structure. The result suggests that probing intensity and length should rise with the stakes (budget, value v) and be belief-contingent, not fixed at b^I.
- **Gittins, J. C. (1979). "Bandit Processes and Dynamic Allocation Indices." *Journal of the Royal Statistical Society, Series B* 41(2): 148–164.** DOI [10.1111/j.2517-6161.1979.tb01068.x](https://doi.org/10.1111/j.2517-6161.1979.tb01068.x).
  - Abstract-verified. A unified account of dynamic allocation indices, reducing previously intractable problems to computing indices. Applications include scheduling and sequential clinical trials.
  - Relation (Overlap: **High** as the canonical "allocate a resource across learning projects" model): the planner allocates one unit of effort per period across independent projects, and the index decouples them.
  - Difference: the paper's split is a one-shot, ex ante division of money, and that money also funds exploitation.
- **Banks, J. S. & Sundaram, R. K. (1994). "Switching Costs and the Gittins Index." *Econometrica* 62(3): 687–694\*.** DOI [10.2307/2951664](https://doi.org/10.2307/2951664).
  - The abstract excerpt confirms the paper's framing: the Gittins–Jones (1974) theorem reduces optimal strategies to per-arm indices that depend only on that arm.
  - The main result (standard summary): with switching costs, no index characterization of optimal strategies exists in general.
  - Relation (Overlap: **Medium**): decomposition fails when the allocation problem has nonconvexities or frictions, which is the paper's situation.
- **Weber, R. (1992). "On the Gittins Index for Multiarmed Bandits." *Annals of Applied Probability* 2(4): 1024–1033.** DOI [10.1214/aoap/1177005588](https://doi.org/10.1214/aoap/1177005588).
  - Abstract-verified. A new intuitive proof of index optimality, and "the optimal value function is a submodular set function of the available projects".
  - Relation (Overlap: Medium): diminishing returns to adding projects in the bandit benchmark. The paper's nonconcavity is the opposite of this property.
- **Whittle, P. (1988). "Restless Bandits: Activity Allocation in a Changing World." *Journal of Applied Probability* 25(A): 287–298.** DOI [10.2307/3214163](https://doi.org/10.2307/3214163).
  - Abstract-verified. Choose which projects to operate "under a constraint upon the expected number of projects in operation". The Lagrange multiplier on this relaxed, expected constraint defines an index, and with exactly m projects the index policy is conjectured to be nearly optimal.
  - Relation (Overlap: **Medium–High**): this is the standard device of relaxing a hard (pathwise) capacity or budget constraint into an expected one. It is directly relevant to the paper's comparison of a belief-targeting uninformed agent with a state-targeting informed agent (see Q5).
- **Bergemann, D. & Välimäki, J. (2001). "Stationary Multi-Choice Bandit Problems." *Journal of Economic Dynamics and Control* 25(10): 1585–1594.** DOI [10.1016/s0165-1889(99)00064-0](https://doi.org/10.1016/s0165-1889(99)00064-0).
  - The abstract was not retrieved. From the title, the paper concerns bandits in which several arms can be chosen at once.
  - Relation (Overlap: Low–Medium; content unverified).
- **Bolton, P. & Harris, C. (1999). "Strategic Experimentation." *Econometrica* 67(2): 349–374.** DOI [10.1111/1468-0262.00022](https://doi.org/10.1111/1468-0262.00022).
  - Abstract-verified. With N agents facing the same bandit, information is a public good. There is a free-rider effect, and also an "encouragement effect": future experimentation by others encourages current experimentation.
  - Relation (Overlap: **Medium**): if the two campaigns face the same competition state, probing by one team informs the other, so learning has economies of scope.
- **Keller, G., Rady, S. & Cripps, M. (2005). "Strategic Experimentation with Exponential Bandits." *Econometrica* 73(1): 39–68.** DOI [10.1111/j.1468-0262.2005.00564.x](https://doi.org/10.1111/j.1468-0262.2005.00564.x).
  - Abstract-verified. Free riding makes experimentation inefficiently low. In asymmetric equilibria, "greater efficiency [is] achieved when the players share the burden of experimentation more equitably".
  - Relation (Overlap: **Medium**): a counterpoint to skewed allocations when learning is a shared public good.
- **Hörner, J. & Skrzypacz, A. (2017). "Learning, Experimentation, and Information Design." In *Advances in Economics and Econometrics: Eleventh World Congress*, Cambridge University Press, pp. 63–98.** DOI [10.1017/9781108227162.002](https://doi.org/10.1017/9781108227162.002).
  - The citation was verified; the content was not read in this session.
  - Relation (Overlap: Medium): a recent survey useful for the related-work section.

### Inferences
- **Part of the paper's "fixed cost of learning" comes from the architecture.** In the optimal-experimentation tradition (Rothschild; Easley–Kiefer; ABHJ; Moscarini–Smith 2001), information arrives as a by-product of exploitation. In RTB every exploitation bid's win or loss is informative about θ, because q_θ(b) depends on θ at any b. A learn-while-doing agent therefore gets some information "free", whereas a dedicated probe at b^I ≠ exploitation bid pays an explicit cost. The paper should say clearly that the threshold is (partly) a property of the learn-then-exploit protocol, and that integrated (bandit-like) agents may show smaller or no thresholds.
- **The pacing rule is certainty-equivalent.** "Targeting remaining budget given current beliefs" is passive learning. Prescott, Easley–Kiefer and Kiefer–Nyarko are the natural benchmark for what active learning would add.
- **Probing intensity should respond to stakes.** By Moscarini–Smith (2001), a natural extension makes the probing bid and length increase with the stakes. The current protocol is a restricted special case with fixed b^I and τ chosen up front.
- **Correlated competition states change the allocation problem.** If θ is common across campaigns, the planner's problem gains learning economies of scope (Bolton–Harris). The optimal design may assign all probing to one team, which would make allocations even more skewed. The paper's independence assumption should be stated as a scope condition.

### Gaps
- The full Bergemann–Välimäki Cowles DP was unavailable, so Rothschild, McLennan, Prescott and Grossman–Kihlstrom–Mirman are described from standard knowledge.
- No paper was found that studies explore-then-commit with a budget-funded probing phase as such in economics. This terminology is from CS and OR; other tracks cover it.

---

## Q3. Dynamic information acquisition and optimal stopping in economics

### Takeaway
Several results imply that the paper's protocol is a restricted special case. Wald-type results show that sequential stopping dominates fixed-sample probing. Chernoff (1959) adds adaptive choice of experiments. Modern economic models of attention and dynamic acquisition (Che–Mierendorff 2019; Zhong 2022; Liang–Mu–Syrgkanis 2022) show that optimal learning often uses "biased", Poisson-like confirmatory sources rather than balanced ones. The protocol chooses a fixed probe length τ up front at a fixed balanced bid, so these results supply natural robustness checks and extensions. Pandora's-box and Gittins-type indices are the sequential counterpart of the planner's simultaneous split.

### Cited Findings
- **Wald, A. (1945). "Sequential Tests of Statistical Hypotheses." *Annals of Mathematical Statistics* 16(2): 117–186.** DOI [10.1214/aoms/1177731118](https://doi.org/10.1214/aoms/1177731118).
  - Introduces the sequential probability ratio test (SPRT); content per standard summary.
  - Wald's 1947 book *Sequential Analysis* (Wiley) is the standard companion citation but was not verified here.
  - Relation (Overlap: Medium).
- **Wald, A. & Wolfowitz, J. (1948). "Optimum Character of the Sequential Probability Ratio Test." *Annals of Mathematical Statistics* 19(3): 326–339.** DOI [10.1214/aoms/1177730197](https://doi.org/10.1214/aoms/1177730197).
  - Abstract-verified. "Of all tests with the same power the sequential probability ratio test requires on the average fewest observations."
  - Relation (Overlap: **High**, anchor for a methodological caveat): a fixed-τ probe is dominated in expected probing cost by a win-count likelihood-ratio stopping rule. Sequential probing would lower expected probing spend and likely lower the entry threshold B\*.
- **Arrow, K. J., Blackwell, D. & Girshick, M. A. (1949). "Bayes and Minimax Solutions of Sequential Decision Problems." *Econometrica* 17(3/4): 213–244\*.** DOI [10.2307/1905525](https://doi.org/10.2307/1905525).
  - Standard summary: Bayesian optimal stopping with a cost per observation, the economic version of Wald's problem.
  - Relation (Overlap: Medium).
- **Chernoff, H. (1959). "Sequential Design of Experiments." *Annals of Mathematical Statistics* 30(3): 755–770.** DOI [10.1214/aoms/1177706205](https://doi.org/10.1214/aoms/1177706205).
  - Standard summary: chooses which experiment to perform as a function of current beliefs, in addition to when to stop.
  - Relation (Overlap: **Medium**): the probing bid could adapt over time instead of being fixed at b^I.
- **Fudenberg, D., Strack, P. & Strzalecki, T. (2018). "Speed, Accuracy, and the Optimal Timing of Choices." *American Economic Review* 108(12): 3651–3684.** DOI [10.1257/aer.20150742](https://doi.org/10.1257/aer.20150742).
  - Abstract-verified. An optimal sequential-sampling model with uncertain utilities and a constant cost per unit time. Choices are "more likely to be correct when the agent chooses to decide quickly", which matches data better than the classical drift-diffusion model.
  - Relation (Overlap: Low–Medium): the optimal stopping time should depend on the history.
- **Che, Y.-K. & Mierendorff, K. (2019). "Optimal Dynamic Allocation of Attention." *American Economic Review* 109(8): 2993–3029.** DOI [10.1257/aer.20171000](https://doi.org/10.1257/aer.20171000).
  - Abstract-verified. A decision maker allocates limited attention over news sources biased toward alternative actions. Learning is biased toward the current belief when the belief is extreme and against it when it is moderate (echo-chamber and anti-echo-chamber effects).
  - Relation (Overlap: **Medium**): see Inferences. Extreme bids act like biased Poisson news sources about θ.
- **Zhong, W. (2022). "Optimal Dynamic Information Acquisition." *Econometrica* 90(4): 1537–1582.** DOI [10.3982/ecta17787](https://doi.org/10.3982/ecta17787).
  - From the Econometric Society abstract, paraphrased. Any dynamic signal process is allowed, with a flow cost increasing in informativeness. The optimal policy is a Poisson signal that confirms the prior belief and is precise enough to trigger immediate action. Absent arrival, the decision maker seeks more precise but less frequent signals.
  - Relation (Overlap: **Medium**): suggests that with flexible probing, balanced probes such as b^I need not be optimal.
  - Source: [Econometric Society page](https://www.econometricsociety.org/publications/econometrica/2022/07/01/optimal-dynamic-information-acquisition)
- **Liang, A., Mu, X. & Syrgkanis, V. (2022). "Dynamically Aggregating Diverse Information." *Econometrica* 90(1): 47–80.** DOI [10.3982/ecta18324](https://doi.org/10.3982/ecta18324).
  - Abstract-verified. An agent samples Brownian sources, each informative about a different component of a Gaussian state. The agent chooses which sources to sample and how to allocate attention until an endogenous stopping time. Under conditions on the prior, the optimal strategy is characterized exactly.
  - Relation (Overlap: **Medium–Low**): allocation of sampling across sources within one learner, whereas the paper allocates a budget across learners.
  - Note: an earlier conference (EC) version exists; its year was not verified.
- **Liang, A. & Mu, X. (2020). "Complementary Information and Learning Traps." *Quarterly Journal of Economics* 135(1): 389–448.** DOI [10.1093/qje/qjz033](https://doi.org/10.1093/qje/qjz033).
  - Abstract-verified (SSRN). Short-lived agents choose among correlated sources. The outcome is either efficient aggregation or "learning traps", depending on informational complementarities.
  - Relation (Overlap: Low).
- **Steiner, J., Stewart, C. & Matějka, F. (2017). "Rational Inattention Dynamics: Inertia and Delay in Decision-Making." *Econometrica* 85(2): 521–553.** DOI [10.3982/ecta13636](https://doi.org/10.3982/ecta13636).
  - Abstract-verified. The solution resembles dynamic logit but is biased toward an optimal default rule, with applications to sunk costs, inertia, and accuracy versus delay.
  - Relation (Overlap: Low).
- **Hébert, B. & Woodford, M. (2023). "Rational Inattention when Decisions Take Time." *Journal of Economic Theory* 208: 105612.** DOI [10.1016/j.jet.2023.105612](https://doi.org/10.1016/j.jet.2023.105612).
  - The citation was verified; the content was not read.
  - Relation (Overlap: Low).
- **Pomatto, L., Strack, P. & Tamuz, O. (2023). "The Cost of Information: The Case of Constant Marginal Costs." *American Economic Review* 113(5): 1360–1393.** DOI [10.1257/aer.20190185](https://doi.org/10.1257/aer.20190185).
  - Abstract-verified. Axioms state that the cost of two independent signals is the sum of their costs, and that a signal generated with probability ½ costs half. Together with Blackwell monotonicity and continuity, they pin down the cost "up to a vector of parameters" that measure how hard states are to distinguish. The resulting cost is a weighted sum of KL divergences; this comes from the paper's main theorem, not from the abstract.
  - Relation (Overlap: **Low–Medium**): the paper's probing cost is additive across independent probes, consistent with the additivity axiom. However, it is money, determined by the bid, not a KL-based cost.
- **Weitzman, M. L. (1979). "Optimal Search for the Best Alternative." *Econometrica* 47(3): 641–654\*.** DOI [10.2307/1910412](https://doi.org/10.2307/1910412).
  - Standard summary (Pandora's rule): each box has a reservation value. Inspect boxes in descending order of reservation value and stop when the best realized reward exceeds the reservation values of all unopened boxes.
  - Relation (Overlap: **Medium**): the sequential counterpart of allocating learning across units. The paper's simultaneous ex ante split is a parallel design.
- **Ke, T. T. & Villas-Boas, J. M. (2019). "Optimal Learning before Choice." *Journal of Economic Theory* 180: 383–437.** DOI [10.1016/j.jet.2019.01.005](https://doi.org/10.1016/j.jet.2019.01.005).
  - Abstract-verified. A decision maker allocates learning effort over two uncertain alternatives with an outside option and stops optimally. An alternative is considered "if and only if [its] expected payoff ... is above a threshold". In some regions it is optimal to learn about the worse, less uncertain alternative first.
  - Relation (Overlap: **Medium**): threshold-based inclusion of an alternative in learning, analogous to "the junior team learns only above a budget threshold".
- **Ke, T. T., Shen, Z.-J. M. & Villas-Boas, J. M. (2016). "Search for Information on Multiple Products." *Management Science* 62(12): 3576–3603.** DOI [10.1287/mnsc.2015.2316](https://doi.org/10.1287/mnsc.2015.2316).
  - Abstract-verified. Continuous search over multiple products yields an optimal consideration set and a purchase threshold. A product is considered only if its expected utility is high enough.
  - Relation (Overlap: Medium; Management Science venue).

### Inferences
- **Extreme bids behave like biased Poisson sources (in the sense of Che–Mierendorff and Zhong).** This follows directly from q_θ(b) = b/(b+θ):
  - At very low bids, wins are rare. Their likelihood ratio P(win|θL)/P(win|θH) = (b+θH)/(b+θL) tends to θH/θL, the maximum, so wins are "breakthrough" news confirming θL.
  - At very high bids, losses are rare, and P(lose|θH)/P(lose|θL) tends to θH/θL, so losses are breakthrough news confirming θH.
  - b^I = √(θLθH) is the "balanced" source.
  - Zhong (2022) and Che–Mierendorff (2019) suggest that an optimal dynamic prober may prefer belief-confirming extreme probes over b^I. Cost structures differ, so treat this as a hypothesis to test, not a result.
- **Robustness checks suggested by Wald–Wolfowitz.** Two variants would show how much of the entry threshold comes from fixed-sample design:
  - a sequential stopping rule for the probing phase (SPRT on win counts);
  - adaptive probe bids (Chernoff 1959).

### Gaps
- No economics paper was found on optimal stopping of probing when the probe's cost is the same budget that later funds exploitation (budget-funded stopping). The closest are Bergemann–Hege (2005) and Roberts–Weitzman (1981), in Q6.

---

## Q4. Informativeness (Blackwell; valid measures of information) and the choice of the probing bid b^I = √(θLθH)

### Takeaway
Two-state experiments are dichotomies, where Blackwell's comparisons reduce to error trade-offs. Probing bids along the curve (q_θL(b), q_θH(b)) are not Blackwell-ordered, so "the informative bid" must be justified by a named decision problem (Frankel–Kamenica) or by a large-sample criterion (Chernoff; Mu–Pomatto–Strack–Tamuz). A symmetry of the win-probability model makes b^I the maximizer of every symmetric criterion. The two directional KL divergences are maximized elsewhere, and information per dollar is maximized by low bids.

### Cited Findings
- **Blackwell, D. (1953). "Equivalent Comparisons of Experiments." *Annals of Mathematical Statistics* 24(2): 265–272.** DOI [10.1214/aoms/1177729032](https://doi.org/10.1214/aoms/1177729032).
  - Abstract-verified. Proves the equivalence of comparison methods for general experiments and introduces weaker k-decision-problem comparisons. "For dichotomies, all methods are equivalent, and can be described in terms of errors of the first and second kinds."
  - Relation (Overlap: **High**, anchor): the binary-θ probing problem is a dichotomy, so comparing bids reduces to comparing error (ROC) trade-offs.
  - The 1951 Berkeley Symposium paper, "Comparison of Experiments", is the usual companion citation but was not verified here.
- **Lehmann, E. L. (1988). "Comparing Location Experiments." *Annals of Statistics* 16(2): 521–533.** DOI [10.1214/aos/1176350818](https://doi.org/10.1214/aos/1176350818).
  - Abstract-verified. Blackwell dominance "for all decision problems is too strong". The paper restricts comparison to monotone decision problems (Karlin–Rubin) for one-parameter problems with monotone likelihood ratio.
  - Relation (Overlap: Medium): the exploitation decision (bid given posterior) is monotone, so Lehmann-type orders are the relevant weakening.
- **Athey, S. & Levin, J. (2018). "The Value of Information in Monotone Decision Problems." *Research in Economics* 72(1): 101–116.** DOI [10.1016/j.rie.2017.01.001](https://doi.org/10.1016/j.rie.2017.01.001).
  - Abstract-verified. In monotone decision problems, information preferences are characterized via stochastic-dominance orders on posterior distributions. The paper identifies when one decision maker has a higher marginal value of information than another, and so acquires more.
  - Relation (Overlap: **Medium**): a tool for proving comparative statics such as "a higher-value team (v₁ > v₂) learns more".
- **Persico, N. (2000). "Information Acquisition in Auctions." *Econometrica* 68(1): 135–148.** DOI [10.1111/1468-0262.00096](https://doi.org/10.1111/1468-0262.00096).
  - Abstract-verified. The value of information is higher in more "risk-sensitive" decision problems, and "a first price auction induces more information acquisition than a second price auction".
  - Relation (Overlap: **Medium**): RTB in the paper is first-price, so bidders' information incentives are stronger there. This is useful context for why first-price RTB makes learning about competition valuable.
- **Frankel, A. & Kamenica, E. (2019). "Quantifying Information and Uncertainty." *American Economic Review* 109(10): 3650–3680.** DOI [10.1257/aer.20181897](https://doi.org/10.1257/aer.20181897).
  - Abstract-verified. A measure of information is "valid" if it corresponds to the value of news in some decision problem. All valid measures are characterized; information and uncertainty measures from the same decision problem are coupled; and valid measures are the only payment schemes that never give incentives to delay revealing information.
  - Relation (Overlap: **High**, anchor): to justify b^I, name the decision problem whose valid information measure b^I maximizes.
- **Chernoff, H. (1952). "A Measure of Asymptotic Efficiency for Tests of a Hypothesis Based on the Sum of Observations." *Annals of Mathematical Statistics* 23(4): 493–507.** DOI [10.1214/aoms/1177729330](https://doi.org/10.1214/aoms/1177729330).
  - Abstract-verified. Each test has an efficiency index ρ, and the ratio log ρ₁/log ρ₂ gives the relative large-sample efficiency of two tests.
  - Relation (Overlap: **Medium–High**): the right informativeness yardstick when τ is long.
- **Mu, X., Pomatto, L., Strack, P. & Tamuz, O. (2021). "From Blackwell Dominance in Large Samples to Rényi Divergences and Back Again." *Econometrica* 89(1): 475–506.** DOI [10.3982/ecta17548](https://doi.org/10.3982/ecta17548).
  - Abstract-verified. With a binary state, one experiment is "generically ... more informative than another in large samples if and only if it has higher Rényi divergences".
  - Relation (Overlap: **High**): directly applicable to comparing τ repeated probes at bid b against b′.

### Inferences
These come from the author's own numerical check (model q_θ(b) = b/(b+θ); not from the literature):
- **b^I maximizes every symmetric criterion.** b^I maximizes q_θL(b) − q_θH(b), since the first-order condition gives b = √(θLθH). The map b ↦ θLθH/b sends the experiment (q_θL, q_θH) to (1 − q_θH, 1 − q_θL), which is the same experiment with states swapped and win/lose relabelled. Every divergence or decision value that is symmetric under swapping states is therefore symmetric in log b around log √(θLθH). If it is unimodal, it is maximized exactly at b^I. This covers total variation, Hellinger and Chernoff information, for one probe and for τ i.i.d. probes.
- **Numerical confirmation, θL = 1, θH = 4.** Total variation and Hellinger are maximized at b ≈ 2.00, and Chernoff information at about 2 (grid resolution 0.12).
- **The KL divergences are asymmetric.** KL(L‖H) is maximized at b ≈ 1.57 and KL(H‖L) at b ≈ 2.53; the product is 1.57 × 2.53 ≈ 4 = θLθH, as the symmetry predicts. With (θL, θH) = (1, 10), the maximizers are 2.10 and 4.77 versus b^I = 3.16.
  - So b^I is optimal for state-symmetric decision problems: prior ½ and symmetric losses from misclassification.
  - With asymmetric priors or asymmetric exploitation stakes, which are likely given budget pacing, a tilted probing bid does better.
- **No Blackwell dominance along the bid curve.** A binary experiment E′ is a garbling of E iff its (P(win|H), P(win|L)) point lies in the parallelogram spanned by E. No tested bid b′ ∈ {0.05, …, 30} was Blackwell-dominated by b^I in any of the three (θL, θH) cases. Because the KL (Rényi order-1) maximizers differ from b^I, b^I is also not large-sample dominant in the sense of Mu et al. (2021).
- **Information per dollar favours low bids.** Spend per period is b²/(b+θ), while total variation and Chernoff information are roughly linear in b at low bids. Informativeness per dollar of probing spend therefore rises as b → 0 (the argmax was at the grid minimum).
  - If time (periods) is the scarce probing resource, b^I is right.
  - If money is the binding resource, cheaper and longer probing buys information more efficiently. This is the "time versus money" trade-off of Moscarini–Smith (2001).

### Gaps
- No economics paper was found on choosing an auction bid to maximize learning about competition, the informative-bid problem as such. It appears to be new to this paper, apart from the CS literature on bandit bidding, which other tracks cover.

---

## Q5. When can information hurt? Value of information under constraints, the Hirshleifer effect, and expected versus per-state budget constraints

### Takeaway
For a single Bayesian optimizer whose feasible set does not depend on information, free information can never lower ex ante value (Blackwell 1953; Good 1967). Any "free information hurts" result therefore needs one of three channels:
- (a) information changes the effective constraint, for example by destroying pooling or insurance across states (Hirshleifer 1971; Schlee 2001);
- (b) strategic or commitment effects (Kessler 1998; Carrillo–Mariotti 2000);
- (c) a restricted policy class that cannot ignore information.

The paper's result, that under belief-targeting pacing free information lowers value at small budgets, is a channel (a)/(c) result. It should be framed that way to pre-empt "Blackwell says information cannot hurt" objections. No paper was found that states the exact budget-pacing result.

### Cited Findings
- **Good, I. J. (1967). "On the Principle of Total Evidence." *British Journal for the Philosophy of Science* 17(4): 319–321.** DOI [10.1093/bjps/17.4.319](https://doi.org/10.1093/bjps/17.4.319).
  - Standard summary: an expected-utility maximizer weakly gains, in expectation, from free evidence ("Good's theorem").
  - Relation (Overlap: **High**, baseline anchor).
- **Blackwell (1953)**, cited in Q4: more informative experiments are weakly preferred by every decision maker. This is the baseline any "information hurts" claim must get around.
- **Hirshleifer, J. (1971). "The Private and Social Value of Information and the Reward to Inventive Activity." *American Economic Review* 61(4): 561–574.**
  - Bibliographic data verified on IDEAS; no abstract is available there.
  - Standard summary: public information revealed before risk-sharing can lower welfare by destroying insurance opportunities (the "Hirshleifer effect"), and the private value of information can differ from its social value.
  - Relation (Overlap: **High**, closest economic analog of "cross-subsidization across states"): an uninformed agent's budget is effectively pooled across states. Information un-pools it and forces state-by-state budget balance.
  - Source: [IDEAS](https://ideas.repec.org/a/aea/aecrev/v61y1971i4p561-74.html)
- **Schlee, E. E. (2001). "The Value of Information in Efficient Risk-Sharing Arrangements." *American Economic Review* 91(3): 509–524.** DOI [10.1257/aer.91.3.509](https://doi.org/10.1257/aer.91.3.509).
  - Abstract-verified. With competitive risk-sharing and a representative agent, "better information makes everyone worse off". The "representative" agent is normatively unrepresentative: indifferent, while each individual dislikes information.
  - Relation (Overlap: **Medium–High**): the modern formal statement of the Hirshleifer effect, useful as a theoretical anchor for "information destroys cross-state pooling".
- **Kessler, A. S. (1998). "The Value of Ignorance." *RAND Journal of Economics* 29(2): 339–354\*.** DOI [10.2307/2555892](https://doi.org/10.2307/2555892).
  - Abstract-verified. In adverse-selection contracting, the possibility of staying ignorant has "a strictly positive strategic value". There may be no equilibrium with perfect information "even if additional information is costless".
  - Relation (Overlap: Medium): a strategic channel, not the paper's channel.
- **Carrillo, J. D. & Mariotti, T. (2000). "Strategic Ignorance as a Self-Disciplining Device." *Review of Economic Studies* 67(3): 529–544.** DOI [10.1111/1467-937x.00142](https://doi.org/10.1111/1467-937x.00142).
  - Abstract-verified. Agents with time-inconsistent preferences may stop costless learning, and such "strategic ignorance" equilibria "strictly Pareto dominate the complete learning equilibrium".
  - Relation (Overlap: **Medium**): the closest single-agent analog to "an orchestrator may prefer not to pass probing results to an exploitation agent whose rule cannot commit".
- **Galanis, S. (2015). "The Value of Information under Unawareness." *Journal of Economic Theory* 157: 384–396.** DOI [10.1016/j.jet.2015.01.015](https://doi.org/10.1016/j.jet.2015.01.015).
  - Per the search summary: in a single-agent model with unawareness, the value of information can be negative, unlike the standard partitional model.
  - Relation (Overlap: Low).
  - Source: [City Research Online](https://openaccess.city.ac.uk/id/eprint/21336)
- **Bassan, B., Gossner, O., Scarsini, M. & Zamir, S. (2003). "Positive Value of Information in Games." *International Journal of Game Theory* 32(1): 17–31.** DOI [10.1007/s001820300142](https://doi.org/10.1007/s001820300142).
  - The abstract was not read. Per its title, the paper studies conditions under which information has positive value in games, where the single-agent Blackwell result can fail.
  - Relation (Overlap: Low).
- **Gomes, R., Gottlieb, D. & Maestri, L. (2016). "Experimentation and Project Selection: Screening and Learning." *Games and Economic Behavior* 96: 145–169.** DOI [10.1016/j.geb.2016.02.001](https://doi.org/10.1016/j.geb.2016.02.001).
  - From the Semantic Scholar TLDR: necessary and sufficient conditions for private information about returns from exploration to have zero value to the firm. When they fail, "private information about exploration may even decrease the firm's payoff".
  - Relation (Overlap: **Medium**): an organizational setting in which information about experimentation can hurt the principal.
- **Pohlschmidt, T. & Zhu, S. (2026). "Ex Ante and Scenario-Conditional Value of Information in Dynamic Portfolio Choice." arXiv:2610.14821.**
  - From the paper text. "If additional information can be ignored, a richer information structure cannot lower the optimized value function." Yet the induced strategy "need not improve ... in every fixed-drift scenario".
  - Over short horizons, the scenario-conditional value of learning is negative "when belief error is small relative to posterior uncertainty".
  - Relation (Overlap: **Medium–High**): gives exactly the distinction the paper needs between ex ante value (non-negative) and state-conditional value (can be negative).
  - Source: [arXiv](https://arxiv.org/abs/2610.14821)
- **Babichenko, Y., Talgam-Cohen, I. & Zabarnyi, K. (2021). "Bayesian Persuasion under Ex Ante and Ex Post Constraints." *Proceedings of the AAAI Conference on Artificial Intelligence* 35(6): 5127–5134.** DOI [10.1609/aaai.v35i6.16648](https://doi.org/10.1609/aaai.v35i6.16648).
  - The abstract was not read. Per its title, it contrasts constraints imposed in expectation with constraints imposed per realization in information design.
  - Relation (Overlap: Low–Medium): the formal language for "budget in expectation versus per state".
- **Whittle (1988)**, cited in Q2: relaxing a hard capacity constraint to an expected one raises value and yields Lagrangian indices. This is the OR counterpart of comparing an uninformed agent whose spend target holds only on average across states with an informed agent whose target binds state by state.
- **Unverified: Crémer, J. & Khalil, F. (1992), "Gathering Information before Signing a Contract", *American Economic Review* (volume/pages not verified).** It is the standard reference on information acquisition before contracting; Crossref lookup failed in this session.

### Inferences
- **How to frame the paper's result.** Under Blackwell/Good, free information cannot lower ex ante value if the exploitation agent could optimize given the posterior, including choosing to ignore it. The paper's negative value of free information at small budgets must therefore come from:
  - (i) the pacing rule, a fixed belief-to-bid map that cannot "ignore" information; and/or
  - (ii) the uninformed agent's spend target holding only in expectation across states (pooling), while the informed agent's target binds state by state. This is the cross-subsidy, a single-agent Hirshleifer/Whittle-type effect.
- **Robustness check worth reporting.** Let the informed exploitation agent choose its bid optimally given the posterior and remaining budget, or default to the prior bid. Its value then weakly exceeds the uninformed value. The gap between this and the paper's pacing agent measures the "rule cost of information".
- **Separate ex ante from state-conditional negativity** (Pohlschmidt–Zhu 2026). If the negative value appears only in one state (for example θH), it is expected. If it appears ex ante, averaged over π₀, it is a policy-class effect and should be labelled as such.
- **Design implication for agent orchestration.** At small budgets an orchestrator may rationally withhold probing results from a rule-based exploitation agent, or not probe at all. This is a non-strategic analog of strategic ignorance (Carrillo–Mariotti) and the value of ignorance (Kessler).

### Gaps
- No economics paper was found that proves "free information lowers the value of a budget-paced (expected-spend-targeting) bidder", or that compares the value of information under expected and per-state budget constraints for a single decision maker.
- The RTB/OR pacing literature, for example Balseiro & Gur (2019, *Management Science* 65(9): 3952–3968, DOI [10.1287/mnsc.2018.3174](https://doi.org/10.1287/mnsc.2018.3174)), uses expected-budget (fluid) relaxations. Other tracks cover it.
- Crémer–Khalil (1992) was not verified.

---

## Q6. Delegated and organizational experimentation, capital budgeting, parallel versus sequential R&D, research portfolios, and allocation of a common budget across learning units

### Takeaway
Economics has studied every ingredient separately:
- team decisions with shared objectives (Marschak–Radner);
- delegated and contracted experimentation with misaligned agents (Guo; Halac–Kartik–Liu; McClellan);
- financing a learning project (Bergemann–Hege; Roberts–Weitzman);
- headquarters splitting scarce capital across divisions (Stein; Harris–Raviv; Malenko);
- parallel versus sequential R&D and research portfolios (Nelson; Dasgupta–Maskin; Loch–Terwiesch–Thomke);
- decentralized experimentation across units (Callander–Harstad; Kollman–Miller–Page);
- allocating a fixed experimentation budget across experiments (Azevedo et al.; Kasy–Sautmann; recent 2025–26 work).

No work found combines all of these in the paper's way. In the paper, the planner splits a fixed monetary budget across aligned units. Each unit's learning is funded out of its own allocation, which creates a learning threshold, and the optimal split moves from skewed to balanced as the total budget grows.

### Cited Findings
**(a) Team theory: aligned objectives, dispersed information**
- **Marschak, J. (1955). "Elements for a Theory of Teams." *Management Science* 1(2): 127–137.** DOI [10.1287/mnsc.1.2.127](https://doi.org/10.1287/mnsc.1.2.127).
  - Abstract-verified. Studies "a particularly simple form of organization which we call a team".
  - Relation (Overlap: **Medium**; Management Science venue): the agent teams share the advertiser's objective, so team theory, not agency theory, is the right frame.
- **Radner, R. (1962). "Team Decision Problems." *Annals of Mathematical Statistics* 33(3): 857–881.** DOI [10.1214/aoms/1177704455](https://doi.org/10.1214/aoms/1177704455).
  - Standard summary: optimal decentralized decision rules for team members with different information.
  - Relation (Overlap: Medium).
- **Marschak, J. & Radner, R. (1972). *Economic Theory of Teams*. New Haven: Yale University Press (Cowles Foundation Monograph 22).**
  - Verified via the Cowles page and library catalogues.
  - Relation (Overlap: **Medium**): the probing-to-exploitation hand-off of win counts is a team information structure.
  - Source: [Cowles page](https://cowles.yale.edu/research/cfm-22-economic-theory-teams)

**(b) Delegated and contracted experimentation and information acquisition**
- **Manso, G. (2011). "Motivating Innovation." *Journal of Finance* 66(5): 1823–1860.** DOI [10.1111/j.1540-6261.2011.01688.x](https://doi.org/10.1111/j.1540-6261.2011.01688.x).
  - Abstract-verified. Optimal innovation-motivating incentives show "tolerance (or even reward) for early failure and reward for long-term success".
  - Relation (Overlap: Low–Medium): agency, whereas the paper's agents are aligned.
- **Guo, Y. (2016). "Dynamic Delegation of Experimentation." *American Economic Review* 106(8): 1969–2008.** DOI [10.1257/aer.20141215](https://doi.org/10.1257/aer.20141215).
  - Abstract-verified. A principal delegates a Poisson one-armed bandit to a better-informed, experimentation-biased agent. The optimal mechanism is a time-consistent cutoff rule in belief space: pessimistic types over-experiment and the most optimistic under-experiment.
  - Relation (Overlap: **Medium**): the canonical delegated-experimentation result; the cutoff structure parallels stopping rules for probing.
- **Halac, M., Kartik, N. & Liu, Q. (2016). "Optimal Contracts for Experimentation." *Review of Economic Studies* 83(3): 1040–1091.** DOI [10.1093/restud/rdw013](https://doi.org/10.1093/restud/rdw013).
  - Abstract-verified. Adverse selection on ability, dynamic moral hazard and private learning together preclude efficiency.
  - Relation (Overlap: Low–Medium).
- **Halac, M., Kartik, N. & Liu, Q. (2017). "Contests for Experimentation." *Journal of Political Economy* 125(5): 1523–1569.** DOI [10.1086/693040](https://doi.org/10.1086/693040).
  - Abstract-verified. A designer chooses prize-sharing and disclosure to maximize innovation by several learning agents. "Public winner-takes-all" dominates other public contests, but jointly changing sharing and disclosure can raise innovation; "hidden equal-sharing" is optimal under simple conditions.
  - Relation (Overlap: **Medium**): a principal dividing a fixed reward across learning agents, with concentrated versus shared allocations, as in the skew/balance question but through incentives.
- **Hörner, J. & Samuelson, L. (2013). "Incentives for Experimenting Agents." *RAND Journal of Economics* 44(4): 632–663.** DOI [10.1111/1756-2171.12039](https://doi.org/10.1111/1756-2171.12039).
  - The citation was verified; the abstract was not read. It concerns dynamic incentives for agents experimenting on the principal's behalf.
  - Relation (Overlap: Low–Medium).
- **Gerardi, D. & Maestri, L. (2012). "A Principal–Agent Model of Sequential Testing." *Theoretical Economics* 7(3): 425–463.** DOI [10.3982/te914](https://doi.org/10.3982/te914).
  - Abstract-verified. Optimal incentives for an agent acquiring costly sequential information for the principal; payments for correctly announcing the good state rise over time.
  - Relation (Overlap: Medium): delegated probing.
- **Chade, H. & Kovrijnykh, N. (2016). "Delegated Information Acquisition with Moral Hazard." *Journal of Economic Theory* 162: 55–92.** DOI [10.1016/j.jet.2015.12.003](https://doi.org/10.1016/j.jet.2015.12.003).
  - From the TLDR: a principal hires an agent to evaluate options. At intermediate priors, positive effort cannot be sustained.
  - Relation (Overlap: Low–Medium).
- **Henry, E. & Ottaviani, M. (2019). "Research and the Approval Process: The Organization of Persuasion." *American Economic Review* 109(3): 911–955.** DOI [10.1257/aer.20171919](https://doi.org/10.1257/aer.20171919).
  - Abstract-verified. Sequential costly research by an informer to persuade an evaluator. The welfare benchmark is "Wald's classic solution"; giving authority to the informer is optimal when information is costly enough.
  - Relation (Overlap: Medium).
- **McClellan, A. (2022). "Experimentation and Approval Mechanisms." *Econometrica* 90(5): 2215–2247.** DOI [10.3982/ecta17021](https://doi.org/10.3982/ecta17021).
  - Abstract-verified. With delegated experimentation, the optimal approval rule is history-dependent and its threshold moves downward over time. Private information can make fast-track options optimal.
  - Relation (Overlap: Medium).
- **Moroni, S. (2022). "Experimentation in Organizations." *Theoretical Economics* 17(3): 1403–1450.** DOI [10.3982/te3069](https://doi.org/10.3982/te3069).
  - Abstract-verified. A principal incentivizes a team on a two-milestone project. To reduce rents, the principal stops too early "and gives identical agents asymmetric experimentation assignments".
  - Relation (Overlap: **Medium–High**): optimal asymmetric treatment of identical learning units, parallel to the paper's skewed splits but driven by incentives.
- **Bonatti, A. & Hörner, J. (2011). "Collaborating." *American Economic Review* 101(2): 632–663.** DOI [10.1257/aer.101.2.632](https://doi.org/10.1257/aer.101.2.632).
  - Abstract-verified. Moral hazard in teams on an uncertain project leads to free riding and procrastination; deadlines help.
  - Relation (Overlap: Low–Medium).

**(c) Financing learning (budget-funded learning)**
- **Bergemann, D. & Hege, U. (1998). "Venture Capital Financing, Moral Hazard, and Learning." *Journal of Banking & Finance* 22(6–8): 703–735.** DOI [10.1016/s0378-4266(98)00017-x](https://doi.org/10.1016/s0378-4266(98)00017-x).
  - Abstract-verified. Information about project value arrives by developing the project, and fund allocation is subject to moral hazard. The optimal contract is a time-varying share; agency costs can cause inefficient early stopping.
  - Relation (Overlap: **Medium–High**).
- **Bergemann, D. & Hege, U. (2005). "The Financing of Innovation: Learning and Stopping." *RAND Journal of Economics* 36(4): 719–752.**
  - Abstract-verified on IDEAS. Financing a research project with uncertain completion time and success. In both relationship and arm's-length financing, "equilibrium funding stops altogether too early". The release rate tightens over time under relationship financing and loosens under arm's-length financing.
  - Relation (Overlap: **High** as the canonical "budget funds the learning process" model): a single project, with no competing units.
  - Source: [IDEAS](https://ideas.repec.org/a/rje/randje/v36y20054p719-752.html)
- **Roberts, K. & Weitzman, M. L. (1981). "Funding Criteria for Research, Development, and Exploration Projects." *Econometrica* 49(5): 1261–1288\*.** DOI [10.2307/1912754](https://doi.org/10.2307/1912754).
  - Abstract-verified. The sequential nature of R&D means funding criteria must account for future funding decisions, with "a continual possibility of reviewing a project's status, based on the latest information". An explicit formula is given in an important special case, relevant to "the general theory of information gathering processes".
  - Relation (Overlap: **High** as an anchor for staged funding of learning): contrast with the paper's up-front τ.

**(d) Internal capital markets and capital budgeting: headquarters splitting a scarce budget**
- **Stein, J. C. (1997). "Internal Capital Markets and the Competition for Corporate Resources." *Journal of Finance* 52(1): 111–133.** DOI [10.1111/j.1540-6261.1997.tb03810.x](https://doi.org/10.1111/j.1540-6261.1997.tb03810.x).
  - Abstract-verified. Headquarters allocates scarce resources to competing projects. "Winner-picking", actively shifting funds between projects, creates value even without relaxing firm-wide constraints, and works best "when headquarters oversees a small and focused set of projects".
  - Relation (Overlap: **High**, closest economics analog of the planner's split): it has no learning thresholds.
- **Stein, J. C. (2002). "Information Production and Capital Allocation: Decentralized versus Hierarchical Firms." *Journal of Finance* 57(5): 1891–1921.** DOI [10.1111/0022-1082.00483](https://doi.org/10.1111/0022-1082.00483).
  - Abstract-verified. Decentralization is attractive when information is "soft"; hierarchies do better when information can be "hardened" and passed along.
  - Relation (Overlap: **Medium**): the win count passed from prober to exploiter is hard information. This supports a hierarchical, orchestrated design.
- **Gertner, R. H., Scharfstein, D. S. & Stein, J. C. (1994). "Internal versus External Capital Markets." *Quarterly Journal of Economics* 109(4): 1211–1230.** DOI [10.2307/2118361](https://doi.org/10.2307/2118361).
  - Abstract-verified (NBER version, DOI [10.3386/w4776](https://doi.org/10.3386/w4776)). Owner-provided internal capital means more monitoring and weaker managerial incentives, and makes it easier to redeploy assets from poorly performing projects.
  - Relation (Overlap: Medium).
- **Scharfstein, D. S. & Stein, J. C. (2000). "The Dark Side of Internal Capital Markets: Divisional Rent-Seeking and Inefficient Investment." *Journal of Finance* 55(6): 2537–2564.** DOI [10.1111/0022-1082.00299](https://doi.org/10.1111/0022-1082.00299).
  - Abstract-verified. Rent-seeking leads to "'socialism' in internal capital allocation, whereby weaker divisions get subsidized by stronger ones".
  - Relation (Overlap: **Medium**): a contrast. Agency pushes allocations toward excessive balance, whereas the paper's efficient planner skews toward the senior team when the junior cannot afford to learn.
- **Harris, M. & Raviv, A. (1996). "The Capital Budgeting Process: Incentives and Information." *Journal of Finance* 51(4): 1139–1174\*.** DOI [10.2307/2329390](https://doi.org/10.2307/2329390).
  - Abstract-verified. Budgeting processes respond to decentralized information and incentive problems, producing "underinvestment when capital productivity is high and overinvestment when it is low".
  - Relation (Overlap: Medium).
- **Harris, M. & Raviv, A. (1998). "Capital Budgeting and Delegation." *Journal of Financial Economics* 50(3): 259–289.**
  - Bibliographic data verified on IDEAS; the abstract is unavailable there and the content was not read.
  - Relation (Overlap: Medium).
  - Source: [IDEAS](https://ideas.repec.org/a/eee/jfinec/v50y1998i3p259-289.html)
- **Malenko, A. (2019). "Optimal Dynamic Capital Budgeting." *Review of Economic Studies* 86(4): 1747–1778.** DOI [10.1093/restud/rdy043](https://doi.org/10.1093/restud/rdy043).
  - Abstract-verified (SSRN version, DOI [10.2139/ssrn.1710884](https://doi.org/10.2139/ssrn.1710884)). Headquarters "allocate a spending account to the manager and replenish it over time", with a threshold: projects below it are financed from the account, and projects above it are fully financed by headquarters after an audit.
  - Relation (Overlap: **Medium–High**): dynamic budget allocation to a unit, with threshold structure.

**(e) Parallel versus sequential R&D and research portfolios**
- **Nelson, R. R. (1961). "Uncertainty, Learning, and the Economics of Parallel Research and Development Efforts." *Review of Economics and Statistics* 43(4): 351–364\*.** DOI [10.2307/1927475](https://doi.org/10.2307/1927475).
  - Standard summary: run several approaches in parallel until learning allows choosing the best; the optimal number of parallel efforts depends on costs and the speed of learning.
  - Relation (Overlap: **Medium**).
- **Abernathy, W. J. & Rosenbloom, R. S. (1969). "Parallel Strategies in Development Projects." *Management Science* 15(10): B486–B505.** DOI [10.1287/mnsc.15.10.b486](https://doi.org/10.1287/mnsc.15.10.b486).
  - Abstract-verified. Parallel approaches "provide better information for a decision, maintain options, or hedge". The paper addresses when to continue them, using field and simulation evidence.
  - Relation (Overlap: Medium; Management Science venue).
- **Loch, C. H., Terwiesch, C. & Thomke, S. (2001). "Parallel and Sequential Testing of Design Alternatives." *Management Science* 47(5): 663–678.** DOI [10.1287/mnsc.47.5.663.10480](https://doi.org/10.1287/mnsc.47.5.663.10480).
  - Abstract-verified. Parallel testing is faster but forgoes learning between tests. The optimal mix depends on testing cost, prior knowledge and lead time; with imperfect (noisy) tests, "the attractiveness of parallel strategies decreases".
  - Relation (Overlap: **Medium–High**): learning from one unit's test before funding another is an alternative the paper's simultaneous split rules out.
- **Dasgupta, P. & Maskin, E. (1987). "The Simple Economics of Research Portfolios." *Economic Journal* 97(387): 581–595.** DOI [10.2307/2232925](https://doi.org/10.2307/2232925).
  - The abstract was unavailable; standard summary: the choice of how correlated (diverse) research projects are, and how market outcomes compare with the social optimum.
  - Relation (Overlap: Low–Medium).
- **Bhattacharya, S. & Mookherjee, D. (1986). "Portfolio Choice in Research and Development." *RAND Journal of Economics* 17(4): 594–605\*.** DOI [10.2307/2555484](https://doi.org/10.2307/2555484).
  - Abstract-verified. Neither society nor firms prefer correlation per se; the gap between social and private risk depends on skewness and risk aversion.
  - Relation (Overlap: Low).
- **Francetich, A. (2016). "Managing Multiple Research Projects." SSRN WP.** DOI [10.2139/ssrn.2828419](https://doi.org/10.2139/ssrn.2828419).
  - From the TLDR: there is a rationale for simultaneous research "even on costly, conflicting projects ... even if it is known that only one of the projects is fruitful ex-post".
  - Publication status beyond SSRN was not verified.
  - Relation (Overlap: **Medium–High**): one decision maker allocating effort across multiple learning projects.

**(f) Decentralized and federal policy experimentation across units**
- **Callander, S. (2011). "Searching for Good Policies." *American Political Science Review* 105(4): 643–662.** DOI [10.1017/s0003055411000426](https://doi.org/10.1017/s0003055411000426).
  - Abstract-verified. Trial-and-error policy search in complex environments, where policymaking can get stuck at arbitrarily bad outcomes.
  - Relation (Overlap: Low–Medium).
- **Garfagnini, U. & Strulovici, B. (2016). "Social Experimentation with Interdependent and Expanding Technologies." *Review of Economic Studies* 83(4): 1579–1613.** DOI [10.1093/restud/rdw008](https://doi.org/10.1093/restud/rdw008).
  - Abstract-verified. Radical experimentation is informative and expands the set of affordable technologies; experimentation eventually stagnates.
  - Relation (Overlap: Low–Medium).
- **Callander, S. & Harstad, B. (2015). "Experimentation in Federal Systems." *Quarterly Journal of Economics* 130(2): 951–1002.** DOI [10.1093/qje/qjv008](https://doi.org/10.1093/qje/qjv008).
  - Abstract-verified. In the first best, districts converge in their policy choice to maximize informational spillovers. With decentralization they diverge to discourage free riding. "Progressive concentration of power", harmonizing after experimentation, can raise experimentation.
  - Relation (Overlap: **Medium**): a central planner coordinating experimentation across units.
- **Kollman, K., Miller, J. H. & Page, S. E. (2000). "Decentralization and the Search for Policy Solutions." *Journal of Law, Economics, and Organization* 16(1): 102–128.** DOI [10.1093/jleo/16.1.102](https://doi.org/10.1093/jleo/16.1.102).
  - Crossref metadata list only the first author; the co-authors are from the standard citation.
  - Abstract-verified. Federated organizations can search in parallel and combine findings. The benefits "first increase and then decrease as the problem of finding good policies increases in difficulty".
  - Relation (Overlap: **Medium**): the inverted-U value of parallel learning resembles the paper's bounded window.
- **Strulovici, B. (2010). "Learning While Voting: Determinants of Collective Experimentation." *Econometrica* 78(3): 933–971.** DOI [10.3982/ecta8011](https://doi.org/10.3982/ecta8011).
  - The citation was verified; the content was not read.
  - Relation (Overlap: Low).

**(g) Allocating a fixed experimentation budget across experiments (closest modern work)**
- **Azevedo et al. (2020, JPE)**, detailed in Q1: production-function decomposition, with "go big" versus "go lean" depending on tails and resource scarcity. Overlap: **High**.
- **Li, H., Namkoong, H. & Scheinfeld, I. (2026). "When Representative Samples Produce Worse Outcomes: Scale-up Decisions and Testing in Small-Budget RCTs." arXiv:2606.13531.**
  - From the text. When significance tests gate further study, the optimal pilot composition "depends critically on its budget size".
  - In the large-budget limit, the optimal pilot converges to a representative sample. "In the small-budget regime, the pilot designer maximizes expected impact by sampling only from a single homogeneous sub-population."
  - The proof "applies more generally when an RCT and significance test are used to decide whether to receive any non-adaptive downstream payoff".
  - Relation (Overlap: **High**): concentration at small budgets and spreading at large budgets is the same qualitative pattern as the paper's skewed-then-balanced split.
  - Source: [arXiv](https://arxiv.org/abs/2606.13531)
- **Yang, F., Ham, D. W. & Jasin, S. (2026). "Minimizing Type 2 Errors in an Experiment-Rich Regime via Optimal Resource Allocation." arXiv:2603.17031.**
  - Abstract-verified. Allocates a fixed pool of users across M concurrent A/B tests to minimize the worst-case Type 2 error. Allocations that minimize mean squared error "can be highly inefficient for detection".
  - A naive plug-in of pilot standard deviations loses power, so the authors propose correction factors.
  - Relation (Overlap: **Medium**): a budget split across learning units, but in a pure inference objective.
  - Source: [arXiv](https://arxiv.org/abs/2603.17031)
- **Soumalias, E., Mudd, R. & Zaidi, A. (2026). "Incentive Alignment in Online Experimentation." arXiv:2610.05922 (Meta).**
  - Read in full. An experimenter allocates B units across N interventions and is rewarded on significance-filtered effects. Theorem 1: for any threshold and budget, the platform's value at the experimenter-optimal allocation can be ≤ 0 while the platform optimum is arbitrarily large.
  - Sample splitting aligns incentives at a cost of at most a fraction γ of value. A shrinkage penalty keeps the full budget and makes negative-effect tests unprofitable.
  - Relation (Overlap: **Medium**): decentralized budget allocation across experiments, with incentives.
  - Its reference list points to centralized portfolio work, which was not opened in this session: Schmit, Shah & Johari (2019), "Optimal Testing in the Experiment-Rich Regime", AISTATS, PMLR 89: 626–633; and Sudijono, Ejdemyr, Lal & Tingley (2025), "Optimizing Returns from Experimentation Programs", EC '25, DOI [10.1145/3736252.3742638](https://doi.org/10.1145/3736252.3742638).
  - Source: [arXiv](https://arxiv.org/abs/2610.05922)
- **Kasy, M. & Sautmann, A. (2021). "Adaptive Treatment Assignment in Experiments for Policy Choice." *Econometrica* 89(1): 113–132.** DOI [10.3982/ecta17527](https://doi.org/10.3982/ecta17527).
  - Abstract-verified. "Exploration sampling" assigns each wave's units with probabilities that are an increasing concave function of the posterior probability that each treatment is optimal. The paper proves asymptotic optimality for policy choice.
  - Relation (Overlap: **Medium**): allocating a sampling budget across arms.
- **Feit, E. M. & Berman, R. (2019). "Test & Roll: Profit-Maximizing A/B Tests." *Marketing Science* 38(6): 1038–1058.** DOI [10.1287/mksc.2019.1194](https://doi.org/10.1287/mksc.2019.1194).
  - The abstract was not retrieved. Per its title, it sizes A/B tests to maximize test-plus-rollout profit.
  - Relation (Overlap: Medium; a cross-reference for the marketing track).
- **Schwartz, E. M., Bradlow, E. T. & Fader, P. S. (2017). "Customer Acquisition via Display Advertising Using Multi-Armed Bandit Experiments." *Marketing Science* 36(4): 500–522.** DOI [10.1287/mksc.2016.1023](https://doi.org/10.1287/mksc.2016.1023).
  - From the TLDR: bandit experiments for display advertising, and optimizing click-through rather than conversion would cut acquisition by about 10%.
  - Relation (Overlap: Medium; a cross-reference).
- **Lewis, R. A. & Rao, J. M. (2015). "The Unfavorable Economics of Measuring the Returns to Advertising." *Quarterly Journal of Economics* 130(4): 1941–1973.** DOI [10.1093/qje/qjv023](https://doi.org/10.1093/qje/qjv023).
  - Abstract-verified. Across 25 large field experiments ($2.8M in spend), the median confidence interval on ROI is more than 100 percentage points wide. Informative experiments "can easily require more than 10 million person-weeks".
  - Relation (Overlap: **Medium**): empirical support that learning in advertising carries a large, fixed-cost-like price.
- **Snippet-level only** (the abstract snippet was seen; the paper was not read):
  - "Resource Allocation with Midterm Review" (arXiv:2610.15786, 2026): a principal funds an agent's project over two periods, with a midterm public signal. [alphaXiv](https://www.alphaxiv.org/abs/2610.15786)
  - "Optimally Pacing Budget Spending and Learning" (arXiv:2610.11074, 2026; Princeton/Google): regret bounds for budget-constrained online learning against budget-pacing experts. [alphaXiv](https://www.alphaxiv.org/abs/2610.11074)
  - Both are Low–Medium cross-references.

### Inferences
- **How to frame the setting.** The paper is best described as a team problem: an aligned planner and aligned agents (Marschak–Radner), not delegated experimentation. The organizational analogs are Stein's (1997) winner-picking headquarters and Bergemann–Hege's budget-funded learning.
- **The novelty is the dual role of the budget.** The same allocation funds both learning (probing spend) and exploitation, so a unit's capacity to learn depends on what it is given. In Azevedo et al. the resource is pure data. In Gittins/Whittle it is attention per period. In Stein and Malenko units do not learn at all.
- **Two forces can make the optimal split skewed:**
  - nonconcavity, as in the paper, Azevedo et al. and Li–Namkoong–Scheinfeld;
  - incentives (Moroni; Halac–Kartik–Liu 2017).

  By contrast, agency can make allocations too balanced (Scharfstein–Stein's "socialism"), and experimentation burden-sharing can raise efficiency (Keller–Rady–Cripps). Citing these contrasts positions the paper's result as an efficiency (technology) effect, not an incentive effect.
- **A missing design option.** Learning from one unit before funding the other, a sequential design (Loch et al.; Roberts–Weitzman; Weitzman), would be a natural extension. It would likely lower the entry threshold relative to the simultaneous ex ante split.

### Gaps
- No economics paper was found in which a planner splits a fixed monetary budget across independent learning units whose learning is self-financed from their allocations, with a learning threshold and a split that is skewed for small totals and balanced for large ones. The closest formal analogs are Azevedo et al. (2020) and Li–Namkoong–Scheinfeld (2026), and both allocate samples, not money.
- The content of Harris–Raviv (1998), Hörner–Samuelson (2013), Feit–Berman (2019) and Bergemann–Välimäki (2001) was not read.
- Francetich's publication venue was not verified.

---

## Q7. Synthesis: which results are the best theoretical anchors, and which works are closest to "a principal allocating a budget across several learning units"?

### Takeaway
Five anchor families cover the paper's main results:
- the learning threshold: Radner–Stiglitz, Chade–Schlee, Keppo–Moscarini–Smith;
- the threshold expressed in budget scale: Wilson, plus Moscarini–Smith for τ\* growth;
- the skewed-then-balanced split: Azevedo et al., plus Li–Namkoong–Scheinfeld;
- "free information hurts under pacing": Blackwell/Good as the baseline, Hirshleifer/Schlee and Pohlschmidt–Zhu as the analogs;
- experimentation intensity and stopping: Moscarini–Smith 2001, Wald–Wolfowitz, and the informativeness criteria for b^I.

The closest works on "allocating a budget across learning units" are Azevedo et al. (2020), Li–Namkoong–Scheinfeld (2026), the Gittins/Whittle bandit-allocation family, Stein (1997) with Malenko (2019), and Bergemann–Hege (2005) with Roberts–Weitzman (1981). None of them combines a money budget that funds both learning and exploitation, independent units in auction markets, and a pacing rule.

### Cited Findings
**(1) Anchors the paper can use**
- **A1. Fixed cost of learning and abrupt entry.**
  - The zero marginal value of small information makes the value of information nonconcave ([Chade–Schlee 2002](https://asu.elsevierpure.com/en/publications/another-look-at-the-radner-stiglitz-nonconcavity-in-the-value-of-); [De Lara–Gilotte 2007](https://ideas.repec.org/p/hal/journl/hal-00716396.html)).
  - Demand for information is lumpy and "suddenly chokes off" ([Keppo–Moscarini–Smith 2008](https://ideas.repec.org/a/eee/jetheo/v138y2008i1p21-50.html)).
  - Use: justify that τ\*(B) jumps from 0 to a positive value at the entry point. State that the unit-dependence of R–S (Azevedo et al. fn. 17, [WP](https://www.gwern.net/doc/statistics/decision/2019-azevedo.pdf)) is resolved here by the cost structure of probing.
- **A2. Scale economies of information and the growth of τ\*.**
  - "Better information justifies a higher scale of operations and vice versa" ([Wilson 1975](https://doi.org/10.2307/3003221)).
  - Large-sample information demand is about a constant × log price ([Moscarini–Smith 2002](https://doi.org/10.2139/ssrn.300080)).
  - Use: learning pays only above a budget scale, and τ\* should grow roughly like log B inside the window.
- **A3. Nonconcave production functions summed under a common constraint.**
  - Payoff = Σ production functions of data (Proposition 2). Thin tails give convexity near zero, and with scarce resources "allocate all experimental resources to one idea"; with abundance, spread ([Azevedo et al. WP](https://www.gwern.net/doc/statistics/decision/2019-azevedo.pdf)).
  - With small budgets, sample a single sub-population; with large budgets, a representative sample ([Li–Namkoong–Scheinfeld 2026](https://arxiv.org/abs/2606.13531)).
  - Use: the direct theoretical precedent for "more skewed when the junior cannot afford to learn, more balanced once both learn".
- **A4. When free information can hurt.**
  - Baseline: free information never hurts an unconstrained Bayesian ([Blackwell 1953](https://doi.org/10.1214/aoms/1177729032); [Good 1967](https://doi.org/10.1093/bjps/17.4.319)).
  - Analogs: information destroys pooling or insurance ([Hirshleifer 1971](https://ideas.repec.org/a/aea/aecrev/v61y1971i4p561-74.html); [Schlee 2001](https://doi.org/10.1257/aer.91.3.509)); ex ante value is non-negative while scenario-conditional value can be negative ([Pohlschmidt–Zhu 2026](https://arxiv.org/abs/2610.14821)); relaxing a hard constraint to an expected one ([Whittle 1988](https://doi.org/10.2307/3214163)).
  - Use: frame the paper's result as a pacing-rule and cross-state-pooling effect.
- **A5. Experimentation intensity, stopping and informativeness.**
  - "The optimal experimentation level rises in the Bellman value" ([Moscarini–Smith 2001](https://doi.org/10.1111/1468-0262.00259)).
  - The SPRT minimizes expected sample size for given error rates ([Wald–Wolfowitz 1948](https://doi.org/10.1214/aoms/1177730197)).
  - Valid information measures correspond to decision problems ([Frankel–Kamenica 2019](https://doi.org/10.1257/aer.20181897)); large-sample dominance is governed by Rényi divergences ([Mu et al. 2021](https://doi.org/10.3982/ecta17548)).
  - Use: comparative statics on τ, a caveat on fixed τ, and a principled justification of b^I.

**(2) Works closest to "allocating a budget across learning units", and what they do and don't cover**
- **C1. [Azevedo et al. (2020, JPE)](https://doi.org/10.1086/710607).**
  - Covers: a fixed experimental resource split across many learning units; an additive decomposition; nonconcave versus concave unit value functions; concentration versus spreading.
  - Does not cover: money that funds both learning and exploitation; heterogeneous unit stakes v_i (unit values are not v-weighted shares of one market); market or auction feedback; a pacing rule; dedicated probing; "free information hurts".
- **C2. [Li–Namkoong–Scheinfeld (2026)](https://arxiv.org/abs/2606.13531).**
  - Covers: an explicit budget-size dependence of the optimal allocation of a sampling budget across sub-populations, concentrated when small and representative when large.
  - Does not cover: units that act on what they learn under their own budgets; a planner valuing several units' downstream payoffs.
- **C3. The bandit allocation family: [Gittins (1979)](https://doi.org/10.1111/j.2517-6161.1979.tb01068.x), [Whittle (1988)](https://doi.org/10.2307/3214163), [Weber (1992)](https://doi.org/10.1214/aoap/1177005588), [Banks–Sundaram (1994)](https://doi.org/10.2307/2951664) and [Bergemann–Välimäki (2008)](https://doi.org/10.1057/978-1-349-95121-5_2386-1).**
  - Covers: dynamic allocation of one resource across independent learning projects, index decomposition, expected-constraint relaxation, and the failure of indices with frictions.
  - Does not cover: a one-shot ex ante split; budgets consumed by exploitation; nonconcavity-induced corner allocations.
- **C4. [Stein (1997)](https://doi.org/10.1111/j.1540-6261.1997.tb03810.x), with [Malenko (2019)](https://doi.org/10.1093/restud/rdy043) and [Harris–Raviv (1996)](https://doi.org/10.2307/2329390).**
  - Covers: headquarters dividing scarce capital across divisions (winner-picking); spending accounts with thresholds; information-driven reallocation.
  - Does not cover: units' own learning costs or learning thresholds. These papers focus on agency rather than an aligned team.
- **C5. [Bergemann–Hege (2005)](https://ideas.repec.org/a/rje/randje/v36y20054p719-752.html), with [Roberts–Weitzman (1981)](https://doi.org/10.2307/1912754).**
  - Covers: a budget that funds the learning process itself; when to stop funding; staged funding with continual review.
  - Does not cover: several units competing for a fixed total; the cross-unit split.
- **Runners-up:**
  - [Moroni (2022)](https://doi.org/10.3982/te3069): asymmetric assignments for identical learning agents.
  - [Halac–Kartik–Liu (2017)](https://doi.org/10.1086/693040): a fixed prize split across learning agents.
  - [Callander–Harstad (2015)](https://doi.org/10.1093/qje/qjv008) and [Kollman–Miller–Page (2000)](https://doi.org/10.1093/jleo/16.1.102): central coordination of unit experimentation.
  - [Francetich (2016)](https://doi.org/10.2139/ssrn.2828419): managing multiple research projects.
  - [Kasy–Sautmann (2021)](https://doi.org/10.3982/ecta17527), [Yang–Ham–Jasin (2026)](https://arxiv.org/abs/2603.17031) and [Soumalias–Mudd–Zaidi (2026)](https://arxiv.org/abs/2610.05922): splitting sample or traffic budgets across experiments.

### Inferences
- **Suggested positioning sentence.** "We bring the Radner–Stiglitz nonconcavity (Radner and Stiglitz 1984; Chade and Schlee 2002; Keppo, Moscarini and Smith 2008) into a resource-allocation problem in which, unlike the A/B-testing allocation problem of Azevedo et al. (2020) and the bandit allocation problem of Gittins (1979), the same budget finances both learning and exploitation. As in Stein's (1997) winner-picking, the planner reallocates toward the high-value unit, but here because the junior unit cannot afford to cross its learning threshold."
- **Most valuable robustness and extension checks**, each motivated by an anchor above:
  - (i) sequential probe stopping (Wald–Wolfowitz);
  - (ii) an exploitation agent that optimizes given its posterior, which pins down Blackwell non-negativity and isolates the pacing-rule cost of information;
  - (iii) a probing bid tilted for asymmetric stakes, using KL or Frankel–Kamenica criteria;
  - (iv) correlated θ across teams (Bolton–Harris economies of scope);
  - (v) a learn-while-doing comparator, to show how much of the threshold comes from the explore-then-commit architecture.

### Gaps
- No single prior paper studies the full combination: a monetary budget split across aligned, self-financing learning units in auction markets with pacing. This supports a novelty claim, with the caveat that CS/OR work on budgeted bandits and pacing (other tracks) must be checked.
- Exact proposition numbering in the published JPE version of Azevedo et al. (2020) may differ from the 2019 working paper used here.
