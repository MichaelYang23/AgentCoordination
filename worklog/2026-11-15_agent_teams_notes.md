# 从 bidding 到 agent teams：讨论记录与整体设计

更新于 2026-11-15（下午加入第 7a 节；晚上改称 evaluator 并更正 planner 结论的表述）。这份 notes 记录 11 月 14–15 日的讨论：我们怎样把 bidding 论文的结构迁移到 AI agent teams，做了哪些设计决定，哪些已经证明，哪些只是数值，以及 reviewer 可能的质疑。

## 0. 一句话与文件索引

**一句话**：Orchestrator 把 token 分给几个 agent team；每个 team 不知道自己的 evaluator 有多严，先花一点 token 买几次即时评估摸清标准，再决定剩下的 token 怎么用。问题是：team 会这样学习，会让 orchestrator 的分配更偏还是更均。

| 文件 | 内容 | 状态 |
|---|---|---|
| `claude/agent_theory.tex` | Agent 模型的完整数学结构、推导和证明状态（master record，14 页） | 待 Mike 核对 |
| `claude/agent_premium_shape.tex` | Premium 形状的证明与反例（10 页） | 待 Mike 核对 |
| `claude/agent_model_section.tex` | 论文体的 model section（8 页） | 比 theory 早一版，核对后再同步 |
| `claude/agent_teams_notes.md` | 本文件 | — |
| `claude/proof.md` | Bidding 模型的 master proof record | 未改动 |

## 1. 起点：bidding 论文

- **设定**：一个 bidding agent 面对未知的市场状态 θ∈{θ_L, θ_H}，前 τ 期用 b^I=√(θ_Lθ_H) 探测，之后按 posterior 用一个 paced bid 把预算花完。
- **单 agent 结果**：学习只在一个有界的预算窗口内值得做；窗口内学习 agent 对边际预算的估值与非学习 agent 之比 H=V′/W′ 先高于 1、后低于 1。
- **Planner 结果**：方向由 v₁R′(a^E) 和 v₂R′(T−a^E) 谁大决定（R 是 learning premium，a^E 是不学时的分配）。随总预算上升出现三段：只有值钱的 agent 学得起时更偏；中间一段更均；两者都远在 premium 下降段时又更偏。“两个都学”本身不决定方向。
- **目标**：这个机制不依赖拍卖。我们希望它对 AI agents 有贡献，bidding 是一个提供结构的实例。

## 2. 用 ETC 重读 bidding

Bidding 的 protocol 作为 policy class 就是 Bayesian explore-then-commit：探索长度事前定、探索动作不依赖 belief、commit 后不再更新。

| | ETC（两臂，已知 gap） | Bidding |
|---|---|---|
| Horizon | n | K |
| 探索长度 | 每臂 m，事前定 | τ，upfront 定 |
| 探索动作 | round-robin | b^I |
| Commit | 经验最优臂 | b*(π_τ(w), ρ_w) |
| 探索成本 | mΔ，恒定 | 随 B 变且会变号 |
| ETC 里没有 | — | budget、V(B)、H、planner |

**三项分解**（exact model，baseline 参数）。R=V−W 拆成：信息免费时的价值 A、win displacement D1、spend drain D2。

| B | τ | R | A | D1 | D2 |
|---|---|---|---|---|---|
| 30 | 2（强行） | −0.89 | −0.41 | +0.29 | −0.78 |
| 56 | 2 | +0.003 | +0.15 | +0.14 | −0.28 |
| 100 | 8 | +1.10 | +1.30 | −0.10 | −0.10 |
| 224 | 8 | +1.88 | +2.25 | −0.98 | +0.61 |
| 2000 | 1 | +0.07 | +0.34 | −0.37 | +0.09 |
| 3000 | 1（强行） | −0.11 | +0.22 | −0.40 | +0.07 |

**从中得到的三个发现**：

- **Horizon law 是 Chernoff 而不是 KL。** Exact model 里 K 每翻倍 τ* 正好加 3（8, 11, 14, 17, 20, 23, 26），对应每次 probe 的 Chernoff information 0.223（预测 3.11）。Averaged model 每翻倍只加 0.85–0.96，对应 KL rate 0.832。Smoothed model 在 K 方向的斜率错了约 3.7 倍。full.tex 里悬着的 τ* log-law 应该用 Chernoff 常数，或者标明是 averaged-model statement。
- **上边是 ETC 现象，下边不是。** 上边：D1 每次 probe 约 −0.4 不随预算缩小，而 A→0。下边：主力是 D2，而且 A 本身为负。
- **Bidding 里信息可能有害。** B<45.6 时，连免费的 perfect information 都降低价值。原因是 pacing constraint 是在 posterior 下施加的：不学习的 agent 用一个 bid，在 easy market 花 160、hard market 花 40，等于拿到一次跨 state 的预算调配；知道 state 之后每个 state 都得花 B。论文现在把下边只归因于 spending cost，漏了这一点。

## 3. 迁移：白板提案、发现的问题、三条路

**白板提案（11 月 14 日）**：一个 agent system 做一系列同分布的 task；① 所有 task 都要完成，② agent 可以追加 effort 提高质量，③ 最后由 evaluator 判 pass/fail，P(pass)=b/(b+θ)，θ 有 high/low 的 prior。Learning phase 里 evaluator 对 τ 个 task 立刻评估（每次成本 c），exploitation 结束后再统一评估。

**这个提案好的地方**：评估要付费，所以 commit 是信息结构推出来的，不是硬加的假设；而且可以证明付费评估在最优策略里一定排在最前面，这直接回答了 "vs full bandit"。

**发现的问题**：按原设定，学到 θ 之后没有任何动作可以改。Token 是确定性支出，预算是 hard 的，task 同分布，所以最优永远是均分，与 belief 无关。数值上：B=100 时不学习得 38.89，τ=8、c=1 得 36.96，evaluator 免费也只有 38.44，一开始就知道 θ 仍是 38.89。Bidding 里信息值钱全靠 pay-if-win 让花费依赖 θ，这一层在迁移时丢了。

**三条让信息 actionable 的路**：

| 路 | 让动作依赖 θ 的东西 | 代价 |
|---|---|---|
| A. Triage（采用） | Task 有可观测的异质难度 d，P=b/(b+θd) | 需要异质性 |
| B. Cap / give-up | 所需 token 重尾，撞 cap 即失败，实际消耗 min(X,b) | 撞没撞 cap 是免费信号；expected-spend 语义下信息又可能有害 |
| C. Planner 二次分配 | Probe 后 planner 按 posterior 重分 | Planner 变成 learner，和我们相对 Schwartz–Bradlow–Fader 的定位相反 |

## 4. 现在的模型

| 要素 | 含义 | Team 知道吗 |
|---|---|---|
| K 个 task | n_e 个 easy（难度 d_e）、n_h 个 hard（难度 d_h） | 知道 |
| d | "用 token 计量的难度"：达到同样通过率需要的 token 与 θ·d 成正比 | 知道，做之前可观测 |
| θ | Evaluator 的严格程度 | 不知道，prior π₀ |
| b | 分给一个 task 的追加 effort，以 token 计 | 自己决定 |
| B | Token 预算，hard | 给定 |
| c | 一次即时评估的费用 | 给定 |

- **g(query) 的含义**：白板上的 token cost = g(query) 在模型里就是 d。它不是 query 长度（长度只是可能的 proxy），也不是实际消耗的 token（那是 b）。
- **θ 必须是 evaluator 的标准**：它不被评估就看不到；同时保证 token 消耗不泄露 θ。如果 θ 是 task 的技术难度，team 从自己的工作里就能免费学到。
- **Protocol**：先做 τ 个 easy task，每个投 d_e·b^I 并立刻评估；按 posterior 分配剩下的 B−τ(d_e b^I+c)；之后不再评估。

**两条 assumption**（写法见 `agent_theory.tex` 第 2 节）：

- **Assumption 1（Committed effort）**：effort 以 token 计；投了就花掉，且消耗与 θ 无关。"以 token 计"是 normalization，不需要为"effort 与 token 成正比"辩护。近似之处：同一设置下实际消耗随机且常常用不满，b 应理解为期望消耗。
- **Assumption 2（Diminishing returns）**：通过率对 effort 递增且凹；基准形式 x/(x+θ)。证据：Anthropic 报告准确率随 thinking token 对数增长；Opus 4.5 的 medium 到 high 约两倍 token 换 4.3 个点；token 上限压到 1,024 时准确率从 72% 掉到 44%。反面：最高档位回报接近零、偶尔为负。
- **不需要的东西**：跨 task 的"token 多则成功率高"。模型自己预测它是负的：B=100、evaluator 宽松时，hard task 每个投 1.30、通过率 39%，easy task 每个投 0.70、通过率 85%。

## 5. 结果与证明状态

详见 `agent_theory.tex` 的 Table 1。"General" 指只用两条 assumption；"Skeleton" 指只用 V 是有限多个光滑递增分支的上包络、W 严格凹，bidding 同样适用。

| 结果 | 内容 | 需要 | 状态 |
|---|---|---|---|
| Lemma 1 | Commit phase：同类均分、triage 门槛、shadow price λ、G 对 belief 凸 | General | 已证 |
| Lemma 2 | 标准已知时的闭式：G_θ=M−θS²/(R+θD) | 基准形式 | 已证，8 位核对 |
| Lemma 3 | Learning phase 的 belief | General | 已证 |
| Lemma 4 | V(τ;·) 凹且 C¹，斜率 = 期望 shadow price | General | 已证，8 位核对 |
| Lemma 5 | V 的折点都是凸的 | Skeleton | 已证 |
| Proposition 1 | V−W = A−C，A≥0、C>0；A=0 当且仅当一个分配对所有可能的 posterior 都最优 | General | 已证，已核对 |
| Corollary 1 | Task 相同则永不学习 | General | 已证 |
| Proposition 2 | Learning window 有界；下界在基准形式下是紧的 | General | 已证 |
| Lemma 6 | 入口处 V′≥W′ | Skeleton | 已证 |
| Proposition 3 | 付费评估排在最前 | General | 已证 |
| Proposition 4–5 | 分配方向恒等式 F′(a^E) = v₁R′(a^E) − v₂R′(T−a^E)；pairwise dominance | Skeleton | 已证 |
| Corollary 2 | 只有 team 1 学得起（T/2≤B₁）时更偏 | Skeleton | 已证 |
| Corollary 3 | 两个都学时的方向：H(x) ≤ H(T−x) 时不会更偏 | Skeleton | 条件性 |
| Proposition 6 | Token 有价格时：benchmark 需求低于 premium 峰值的 team 需求上升，高于的下降 | Skeleton | 已证，已核对 |
| Theorem 1（shape 文档） | 知道标准的价值 N(π;B) 对预算严格单峰 | 基准形式 | 已证，已核对 |
| Proposition 1（shape 文档） | N − ½Kρ^τ − τχ ≤ V(τ;B) − W(B) ≤ R ≤ N | General | 已证 |
| Proposition 2（shape 文档） | R 在 [0, B↑] 上不减，B↑ = n_e·min{s, d_e·x̲(π₀)} | General | 已证，已核对 |
| Example 1（shape 文档） | Exact premium 可以有两个局部极大 | 基准形式 | 反例 |
| — | R 在某个显式预算之后不增；H 的形状；分配表 | — | Open / 仅数值 |

**相对 bidding 的三个结构性变化**：

- 斜率公式是精确的：V′=期望 shadow price，不需要 smoothed model。
- 信息项有符号：A≥0 恒成立。
- W′(0) 有限（bidding 里是无穷），所以 benchmark 分配可能是角点。

## 6. 基准数字

参数：θ_L=½，θ_H=8，π₀=½，b^I=2，K=100，easy 和 hard 各 50，d_e=¼，d_h=4，c=0.2。

**B=100 时为什么知道标准值钱**：

| Team 知道什么 | 每个 easy 投 | 每个 hard 投 | 期望 pass |
|---|---|---|---|
| Evaluator 宽松 | 0.70 | 1.30 | 62.1 |
| Evaluator 严格 | 2.00 | 0 | 25.0 |
| 不知道 | 1.16 | 0.84 | 宽松时 60.0，严格时 19.6（平均 39.8） |

知道时平均 43.6；8 次 probe 后得 42.5。

**单个 team**：

| B | 20 | 26 | 30 | 40 | 60 | 100 | 122 | 160 | 250 | 400 | 600 | 720 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| τ* | 0 | 1 | 3 | 5 | 7 | 8 | 7 | 6 | 5 | 3 | 1 | 0 |
| Premium R | 0 | 0.03 | 0.25 | 0.92 | 1.91 | 2.71 | 2.77 | 2.61 | 1.73 | 0.63 | 0.11 | 0 |
| H | 1 | 1.12 | 1.28 | 1.27 | 1.19 | 1.05 | 1.00 | 0.92 | 0.83 | 0.87 | 0.95 | 1 |

学习区间约 25 到 705；入口连续（τ* 从 1 开始）；下界 18.75；premium 峰值在 B̂≈120.2（R=2.774；之前写的 122 是步长 2 的网格读数）。

**两个 team（v₁/v₂=2）**：

| T | 不学时 | 会学时 | Team 1 的变化 | 学习长度 |
|---|---|---|---|---|
| 40 | (26, 14) | (28, 12) | +2 | (1, 0) |
| 60 | (42, 18) | (46, 14) | +4 | (5, 0) |
| 100 | (76, 24) | (78, 22) | +2 | (7, 0) |
| 150 | (114, 36) | (104, 46) | −10 | (8, 5) |
| 300 | (208, 92) | (194, 106) | −14 | (6, 7) |
| 500 | (332, 168) | (324, 176) | −8 | (4, 6) |
| 700 | (456, 244) | (468, 232) | +12 | (2, 5) |

T≈40–110 更偏；T≈112 时 team 2 到达学习门槛，转为更均；T≈560–610 接近零；之后再反转。入口连续，所以分配不跳。

**方向判据在 benchmark 分配处的两项**（和 bidding slides 的三张图对应）：

| T | a^E | T−a^E | v₁R′(a^E) | v₂R′(T−a^E) | 学习使分配 | 位置 |
|---|---|---|---|---|---|---|
| 100 | 76.1 | 23.9 | +0.0428 | 0 | 更偏 | Team 2 学不起 |
| 150 | 114.6 | 35.4 | +0.0035 | +0.0629 | 更均 | 都在上升段 |
| 300 | 207.9 | 92.1 | −0.0196 | +0.0113 | 更均 | Team 1 过峰，team 2 未过峰 |
| 500 | 331.8 | 168.2 | −0.0147 | −0.0085 | 更均 | 都在下降段 |
| 700 | 456.6 | 243.4 | −0.0063 | −0.0106 | 更偏 | 都在下降段 |

后四行两个 team 都学，三行更均、一行更偏。T=500 和 T=700 都在下降段而方向相反：决定方向的是谁的加权 premium 掉得更快，不是在峰的哪一侧。T=300 这种“一个过峰、一个未过峰”的情形可以由 pairwise dominance 直接证出更均（尚未写进 theory 文档）。

**Token 有价格时的需求**：

| Benchmark 需求 | 15 | 24 | 40 | 80 | 110 | 122 | 140 | 200 | 400 |
|---|---|---|---|---|---|---|---|---|---|
| 会学时的需求 | 15 | 31.5 | 58 | 90 | 112.5 | 121.5 | 135 | 177.5 | 350.5 |

## 7. 与 bidding 的关系

Bidding 不是 agent 模型的 special case，反过来也不是。两者是同一个 skeleton 的两个实例。

| | Bidding | Agent team |
|---|---|---|
| 动作消耗的资源 | 赢了才付，期望值依赖 θ | 确定，与 θ 无关 |
| 反馈 | 每次拍卖后免费 | 只有付费 c 才有 |
| 预算约束 | 在当前 belief 下取期望 | 每条路径上都成立 |
| 信息为什么有价值 | Paced bid 依赖 belief | 跨难度的 triage 依赖 belief |
| 信息项的符号 | 可以为负 | 非负 |
| 为什么 commit | 假设 | 推出来的 |
| 下边 | Spending 稀缺，影子价格无界 | 分配与 belief 无关 |
| 上边 | V(τ;B)≤K−τδ_I | 同一个 bound |
| 共享（skeleton） | 凸折点、入口处的边际价值、方向恒等式、pairwise dominance、token 需求 | 同左 |

论文里应该说"同一骨架的两个实例"，不要说 special case。一个嵌套两者的统一模型（一般的资源消耗函数 e_θ(b)，反馈免费或付费）还没有写。

## 7a. Premium 的形状：证明了什么（11 月 15 日下午）

详见 `claude/agent_premium_shape.tex`。问题是 R(B)=V(B)−W(B) 是否单峰。结论分三层。

**已证：知道标准的价值单峰（Theorem 1）。** 定义 N(π;B) = πG_H(B) + (1−π)G_L(B) − G(π;B)，即免费被告知标准能多得多少。基准形式下，对所有参数：

- B ≤ B_L 时 N=0；在 [B_L, B̂_N] 严格增；在 [B̂_N, ∞) 严格减并趋于 0。
- 峰值 B̂_N 严格落在 prior 的 triage 预算 B_π 和严格标准的 triage 预算 B_H 之间。
- 等价说法：informed team 的期望 shadow price 与 uninformed team 的 shadow price 之比 H_∞，先等于 1，再大于 1，最后小于 1，只穿过一次。

证明的三个工具：

- **Loss 表示**：N(π;B) = min_y [π·L_H(y;B) + (1−π)·L_L(y;B)]，y 是给 hard task 的 token 总数，L_θ 是在标准 θ 下相对 informed 最优的损失，有显式有理式。
- **两端**：B_π 以下 N=(1−π)L_L(0;B) 递增；B_H 以上用坐标 u（easy 拿 σ_e·B+u）后每个 L_θ 的分子与 B 无关、分母三个因子都随 B 增，所以 N 递减。
- **中段**：在 (B, y) 平面上，宽松标准的 iso-loss 曲线严格凹，严格标准的 iso-loss 曲线严格凸（Lemma 2）。N_B=0 的点上两条曲线相切，沿公切线对 min 求二阶导得 N_BB<0，所以 N_B 的零点都是严格极大，只能有一个。凸性那一半归结为一个多项式恒等式：c³(a²−b²)² − a³(c²−b²)² − ab²(c−b)(a−c)(a+c)² = (a−b)(a−c)[a²(b³−b²c+c³)+ab³c+abc³+b³c²]。

**已证：premium 与 N 的距离（Proposition 1）。** N − ½Kρ^τ − τχ ≤ V(τ;B) − W(B) ≤ R ≤ N，ρ = 2r^{1/4}/(1+√r)，χ = 1 − q̄^I + (s/d_e)·q̄_x(π₀,0)。所以大 team 的 per-task premium 收敛到一个单峰函数。**但常数很粗**：baseline 下 ρ=0.8、χ=3.475，K=100 时下界是空的（界约 76，N 最大 4.1）。这是大 team 的结论。

**反例：exact premium 不是对所有参数都单峰（Example 1）。** 原因是 τ 取整数。τ* 换档处 V 的斜率只能向上跳；如果换档点落在相邻两个 branch 的峰之间，premium 会先降后升。baseline 把评估费改成 c=0.205：

| B | 120.354 | 121.452（换档 7→6） | 121.885 |
|---|---|---|---|
| R | 2.769860 | 2.769686 | 2.769713 |
| H | 1.0000 | 0.9974 → 1.0010 | 1.0000 |

第二次上升只有 0.00003，但它是反例。c=0.200 和 c=0.210 时是单峰。所以“premium 单峰”不能作为模型的定理；有限 team 该瞄准的是两个单侧结论：R 在 [0, B̂] 不减，在 [B̌, ∞) 不增，B̂ ≤ B̌。theory 文档的 Proposition 6（token 需求）本来就是按这两个条件写的，不用改。

**已证：上升段的显式范围（Proposition 2）。** R_τ′ = information effect + resource effect。

- Resource effect 的符号是精确的：非负当且仅当普通 easy task 拿到的 token 不超过 s（Lemma 3）。Baseline 下在 B=43.2 变号。
- Information effect 在 prior 的 triage 预算以下非负（Lemma 4）。
- 合起来：R 在 [0, B↑] 不减，baseline 下 B↑=30.14（入口约 25）。只覆盖上升段的开头。

**没证出来的**：有限 team 的下降段，即一个显式预算，之后 R 不增。缺的是 posterior 不退化、预算在 prior 的 triage 预算之上时 information effect 的符号。Theorem 1 的公切线论证只能给 min 的二阶导一个上界；posterior 不退化时 informed 一侧自己也是 min，方向反了。

**Baseline 对照**：

| B | 26 | 40 | 60 | 100 | 122 | 160 | 250 | 400 | 600 |
|---|---|---|---|---|---|---|---|---|---|
| R | 0.03 | 0.92 | 1.91 | 2.71 | 2.77 | 2.61 | 1.73 | 0.63 | 0.11 |
| N | 0.31 | 1.46 | 2.63 | 3.78 | 4.03 | 4.10 | 3.48 | 2.08 | 1.12 |
| H | 1.12 | 1.27 | 1.19 | 1.05 | 1.00 | 0.92 | 0.83 | 0.87 | 0.95 |
| H_∞ | 1.24 | 1.31 | 1.24 | 1.11 | 1.06 | 0.98 | 0.84 | 0.81 | 0.86 |

B_L=18.75，B_π₀=30.14，B_H=300；N 的峰在 148.97（4.11），R 的峰在 120.2（2.774）。付费学习拿到 N 的一成到七成半，峰更早。

**不要再试的三条路**（都有反例）：λ(π;B) 在大预算下对 π 凹（不成立）；H_∞ 在三段上各自单调（不成立）；“按固定的 as-if 标准行动”的损失对预算 quasi-concave（不成立，会有两个驼峰）。

## 8. 企业案例

没有单个公开案例具备全部要素；intro 用 composite，并明说。

| 案例 | 支撑模型的哪一块 | 不匹配之处 |
|---|---|---|
| Anthropic Research | Lead agent 按查询复杂度事前分工作量（简单 1 个 agent、3–10 次 tool call；复杂超过 10 个 subagent）；subagent 运行中不能被干预；LLM judge 给 pass/fail | 分配靠 heuristic |
| Airbnb 测试迁移（约 3,500 个文件） | 同分布 task、pass/fail、重试提高通过率、最难的约 3% 放弃自动化；先抽 5–10 个文件调 prompt 再扫全量 | Evaluator 是自动测试，几乎免费 |
| Coding agent 的 PR（AIDev，45.6 万个 PR） | 外部 evaluator（maintainer），接受率随任务类型变；有公开数据 | 没有 token 预算 |
| Allianz Project Nemo（七个 agent） | 最终 evaluator 是人；简单案件给 agent | 是流水线 |
| Uber、Accenture 的 token cap；Claude API 的 task budget | 预算是硬约束，已细到 team 和 task | 是人用 agent 的预算 |
| MAP 调研 | 74% 的已部署 agent 主要靠人工评估；反馈延迟是主要限制 | — |

建议的 intro 链条：预算真的会用完 → orchestrator 事前分预算且中途不能干预 → 评估贵而且慢 → 一批同类 task 被外部 evaluator 判 pass/fail。Running example：一个 coding agent fleet 向多个仓库提交一批同类修改，由各自的 maintainer 决定是否合并。

## 9. Reviewer 风险与目前的应对

| # | 质疑 | 目前的应对 | 还缺什么 |
|---|---|---|---|
| 1 | θ 为什么未知？rubric 是公司自己写的 | Evaluator 是外部的（maintainer、客户、合规） | 例子要选准；别把 θ 解释成 team 的能力匹配，否则和 Proposition 3 冲突 |
| 2 | 为什么是事前定死的 hard budget？ | Cap 的证据；Proposition 6（价格版本）已证 | 说明允许事后重分时是另一个问题 |
| 3 | "Bidding 是 special case" 不成立 | 改成 skeleton 的两个实例（第 7 节） | 统一模型未写 |
| 4 | 新意：Test & Roll、paid-observation bandits、input-adaptive compute allocation | 贡献在"学习如何改变跨 learner 的分配" | Proposition 3 的新意要查文献 |
| 5 | 学习的成本从哪来？LLM judge 便宜 | 主要成本是 probe effort 的扭曲；人工评估占主导的证据 | "对正常 effort 完成的 task 评估"的版本 |
| 6 | 函数形式与经验证据 | 两条 assumption 及证据；核心命题不依赖函数形式 | 通过率上限小于 1、斜率不等于 1、d 带噪声的 robustness |
| 7 | Multi-agent 在哪？team 之间独立 | — | 共享 θ 时"谁替大家学"至少要有初步结果 |
| 8 | Agent 模型的主要结果只有数值 | Skeleton 层的命题已证；N 单峰已证 | 三段式里“都在上升段”和“都在下降段”两种情形的方向、跨 configuration 比较 |

## 10. Prior 的 robustness

Two-point prior 指 θ 只有两个可能值，不是 easy/hard（那是 d，可观测）。连续 prior 下 team 要估计 θ 的值，τ* 从 log K 变成 √K 增长。Lognormal prior（log θ 的均值和标准差与 two-point 相同，B=K）：

| K | 100 | 200 | 400 | 800 | 1600 | 3200 |
|---|---|---|---|---|---|---|
| Two-point 的 τ* | 8 | 10 | 12 | 16 | 18 | 20 |
| 连续 prior 的 τ* | 5 | 9 | 13 | 19 | 28 | 42 |
| Two-point 的 premium（占 W） | 6.8% | 7.9% | 8.5% | 8.9% | 9.2% | 9.3% |
| 连续 prior 的 premium（占 W） | 2.9% | 3.8% | 4.5% | 5.0% | 5.4% | 5.7% |

学习在两种 prior 下都值得做；连续 prior 下 premium 小一半左右，"learning 是很短的阶段"在 K 大时不成立。

## 11. 下一步

按优先级：

1. **Mike 核对 `agent_theory.tex` 和 `agent_premium_shape.tex`。** 前者建议顺序：Lemma 1(iii) 的 supergradient 论证、Proposition 1 的 Jensen 等号条件、Proposition 3 的归纳、Proposition 5–6。后者先看 Lemma 2(ii) 的多项式不等式和 Theorem 1 证明里的公切线二阶导。
2. **Premium 的形状。** 已做一轮，见第 7a 节：N 单峰已证，exact premium 有反例，上升段证到 B↑。剩下的是有限 team 的下降段，以及“每个 branch 单峰、峰位随 τ 递减”（baseline 下成立，证出来就能完整描述 exact premium）。另一个选择是把论文的理论核心放在 N 上，付费学习作为它的近似。
3. **跨 configuration 的比较。** 把 T/2>B₁ 的第一 regime 和第二 regime 的全局最优补上，沿用 bidding 里配置价值差的单调性论证。
4. **优化的 learning phase。** 让 probe effort 可选，看上边还在不在。
5. **统一模型。** 写出嵌套 bidding 和 agent 的一般形式。
6. **证据。** 用 AIDev 估计接受率在仓库间和任务类型间的差异，或跑一个真实 agent 加 judge 的小实验。
7. **共享 θ。** 两个 team 面对同一个 evaluator 时谁来学。

## 12. 更正记录

讨论过程中改过的判断，避免以后重复：

- "Token 版的上边需要 probe 挤占 productive step" 改为 "有 eval cost 就够"，后来又改回：上边的证明用的是 V(τ;B)≤K−τδ_I，起作用的是被 probe 的 task 只拿到 probe effort，评估费 c 不参与。
- "数据显示 token 多不等于成功率高"曾被写成对模型的质疑。这不准确：模型需要的是同一 task 上调高 effort 的因果效应，跨 task 的相关性模型自己预测为负。
- Learning window 的下界最初写成 n_e d_e·min{θ_L(√(d_h/d_e)−1), b^I+c/d_e}。用 Proposition 1 之后第二项不需要，下界就是 n_e d_e θ_L(√(d_h/d_e)−1)，并且是紧的。`agent_model_section.tex` 里还是旧式子。
- 这组参数下入口是连续的，所以 planner 的分配不跳；bidding baseline 的两次跳变不是一般性质。
- 我曾把 planner 的结论概括成“只有一个学则更偏，两个都学则更均”。这不对：两个都学时仍可能更偏（agent 模型 T≥610，bidding slides 的 T=3000）。要证的是方向判据（已证）和三段式的格局（第一段和“跨峰”情形可证，其余靠数值），和 bidding 里一样。
- 11 月 15 日晚：evaluator 统一改称 evaluator；“评估”改称“评估”。
- “Premium 单峰一旦证出，条件都能去掉”不成立：exact premium 对某些参数有两个局部极大（c=0.205），单峰不可能是定理。能证的是 N 单峰和两个单侧结论。
- “入手点是标准已知时 λ 的闭式”只对了一半：闭式解决了 informed 一侧，uninformed 一侧 W′ 没有闭式，最后靠的是 loss 表示和 iso-loss 曲线的曲率。
- Premium 的峰在 120.2，不是 122。
- Resource effect 在 B=43.2 变号（普通 easy task 拿到 s=0.7 个 token 处）。

## 13. 脚本与来源

脚本（未放进 project，已单独发送）：`premium_shape_checks.py`（第 7a 节的全部核对，自包含）、`story.py`（B=100 的故事、单 team 曲线、planner 表）、`refine.py`（window 的入口出口与上下界）、`verify_theory.py`（闭式、斜率公式、分解、H、token 需求）、`prior_compare.py`（两种 prior）、`etc_decomp.py` 和 `loglaw.py`（bidding 的三项分解与 horizon law）。

来源：

- Anthropic, How we built our multi-agent research system: https://www.anthropic.com/engineering/multi-agent-research-system
- Airbnb, Accelerating Large-Scale Test Migration with LLMs: https://airbnb.tech/?p=366
- AIDev dataset: https://www.alphaxiv.org/abs/2507.15003v1
- A Task-Level Evaluation of AI Agents in Open-Source Projects: https://arxiv.org/html/2602.02345
- Allianz Project Nemo: https://www.allianz.com/en/mediacenter/news/articles/251103-when-the-storm-clears-so-should-the-claim-queue.html
- STL Partners, AI token costs: https://stlpartners.com/articles/ai/ai-token-costs-enterprise-ai-budgets/
- Task budgets, Claude Platform Docs: https://platform.claude.com/docs/en/build-with-claude/task-budgets
- Measuring Agents in Production: https://arxiv.org/html/2512.04123v3
- Feit and Berman, Test & Roll, Marketing Science 2019: https://econpapers.repec.org/RePEc:inm:ormksc:v:38:y:2019:i:6:p:1038-1058
- Damani et al., Learning How Hard to Think: https://arxiv.org/pdf/2410.04707
- Tucker et al., Bandits with Costly Reward Observations: https://mlanthology.org/uai/2023/tucker2023uai-bandits
- Seldin et al., Multiarmed Bandits with Paid Observations: https://proceedings.mlr.press/v32/seldin14.html
- Claude's extended thinking: https://www.anthropic.com/news/visible-extended-thinking
- How Do AI Agents Spend Your Money?: https://arxiv.org/html/2604.22750v3
- Don't Blame the Large Language Model: https://arxiv.org/pdf/2607.03691
- METR, Impact of modelling assumptions on time horizon results: https://metr.org/notes/2026-03-20-impact-of-modelling-assumptions-on-time-horizon-results/
