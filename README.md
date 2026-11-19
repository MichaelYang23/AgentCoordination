# AgentCoordination

Research code for *Orchestrating Agent Teams: Budget Allocation in Real-Time Bidding*
(Yang, Zhu & Mookerjee).

* [`bandit_check/`](bandit_check/README.md): does the allocation result survive if the
  learn-then-exploit (ETC) agent team is replaced by agents that learn while they exploit
  (bandit-style)? It reproduces the paper's numbers, compares six learning protocols under two
  budget accountings, runs a 37-market × 5-value-ratio sweep, and discusses token budgets as a
  proxy for AI-agent coordination. The report is in Chinese and includes a draft reviewer response in English.
* [`theory/bandit_formulation.pdf`](theory/bandit_formulation.pdf): the K-period bidding problem written as one
  optimization problem: state (the belief, not the win count), the budget constraint in its expected and
  hard forms, the dynamic programs, and the three nested policy classes (no learning, decomposition,
  full bandit).
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
* [`worklog/`](worklog/2026-11-19_agent_teams_etc_customer.md): dated records of recent work (in Chinese).
  The 2026-11-19 entry covers 14-19 November: how the AI-agent-team model differs from the WITS (bidding)
  version and from the earlier discussions in this repository, why the model is built as explore-then-commit
  and why that structure fits AI agents, the customer reading of the evaluator (report, satisfaction score,
  the cost of reading feedback), open reviewer questions and the status of the proofs. The
  [2026-11-15 entry](worklog/2026-11-15_agent_teams_notes.md) is the discussion record of the move from bidding
  to agent teams. Both are records of discussion, not finished drafts.
* [`theory/agent_teams/`](theory/agent_teams/): the agent-team model (drafts, LaTeX + PDF; proofs not yet
  checked by Mike). [`agent_coordination_note`](theory/agent_teams/agent_coordination_note.pdf): background,
  research questions, setting, the single-team problem and the orchestrator's problem, without results.
  [`agent_theory`](theory/agent_teams/agent_theory.pdf): the mathematics of the model and the status of each
  result (commit phase, value and marginal value of a budget, learning window, why paid evaluations come first,
  direction of the allocation across teams, token demand under a price).
  [`agent_premium_shape`](theory/agent_teams/agent_premium_shape.pdf): the value of knowing the evaluator's
  standard is single-peaked in the budget; the exact learning premium is not single-peaked for all parameters
  (an example); it is nondecreasing on an explicit initial range.
* [`agent_check/`](agent_check/README.md): scripts that reproduce the numbers in `theory/agent_teams/` and in
  the worklog, with their outputs in `agent_check/results/`. Numerical checks only, at the baseline parameters.
