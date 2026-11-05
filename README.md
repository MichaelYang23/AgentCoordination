# AgentCoordination

Research code for *Orchestrating Agent Teams: Budget Allocation in Real-Time Bidding*
(Yang, Zhu & Mookerjee).

* [`bandit_check/`](bandit_check/README.md): does the allocation result survive if the
  learn-then-exploit (ETC) agent team is replaced by agents that learn while they exploit
  (bandit-style)? It reproduces the paper's numbers, compares six learning protocols under two
  budget accountings, runs a 37-market × 5-value-ratio sweep, and discusses token budgets as a
  proxy for AI-agent coordination. The report is in Chinese and includes a draft reviewer response in English.
