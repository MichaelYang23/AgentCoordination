# AgentCoordination

Research code for *Orchestrating Agent Teams: Budget Allocation in Real-Time Bidding*
(Yang, Zhu & Mookerjee).

* [`bandit_check/`](bandit_check/README.md): does the allocation result survive if the
  learn-then-exploit (ETC) agent team is replaced by agents that learn while they exploit
  (bandit-style)? It reproduces the paper's numbers, compares six learning protocols under two
  budget accountings, runs a 37-market × 5-value-ratio sweep, and discusses token budgets as a
  proxy for AI-agent coordination. The report is in Chinese and includes a draft reviewer response in English.
* [`theory/`](theory/large_horizon_limit.pdf): Propositions 1-5 (draft, LaTeX + PDF). The per-period
  learning premium of the learn-then-exploit team converges, as the horizon grows, to a function of the
  primitives that does not depend on how learning is scheduled; its shape (negative-to-zero at small budgets,
  ~Var(θ)/ρ² at large budgets, a kink at entry) is characterised. Verified numerically up to K = 400 with
  `bandit_check/run_large_K.py`.
  Proposition 3: under a common (ex-ante) budget rule, the decomposition (learn, then execute) and the
  full bandit (Bayes-optimal, learns and executes in every auction) converge to the same limit; the full bandit's
  learning cost stays bounded, the decomposition's grows like log K, and their allocations converge.
  Proposition 4: no probe-then-commit design can do better than order log K (lower bound).
  Proposition 5: with n teams, a team gains budget from learning exactly when its marginal-value ratio
  exceeds one common number; learning takes budget from non-learners, balances it among learners and
  favours the marginal (lowest-value) learner. Code: `bandit_check/n_teams.py`.
  Verified for K = 50-400 with `bandit_check/run_dp_largeK.py`.
