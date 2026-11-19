# 工作记录：AI agent team 的 ETC 模型与 customer 设定

> **记录日期**：2026-11-19。**覆盖时间**：2026-11-14 至 11-19 的讨论。
>
> **性质**：近期工作的记录，不是定稿。由 Claude 根据与 Mike 的讨论整理。文中标为"已证"的结论，证明都还没有经过 Mike 核对；标为"数值"的结论只在 baseline 参数下算过。
>
> **读法**：第 0 节是总结。第 1、2 节讲和 WITS 版本以及 repo 里之前讨论的区别。第 3、4 节讲为什么做成 ETC 版本、为什么它更契合 AI agent。第 5 节是 11-16 和 advisor 讨论之后的 customer 设定。第 6 至 9 节是 reviewer 问题、证明状态、下一步和来源。

---

## 0. 总结

WITS 版本研究的是：planner 把广告预算分给几个会学习的 bidding agent，学习会让最优分配更偏还是更均。这一轮我们把同一个问题搬到 AI agent team 上：

- Orchestrator 把 token 预算分给几个 agent team。
- 每个 team 有一批 task，做完交给系统之外的 customer 验收。模型里这个角色叫 **evaluator**。
- Team 不知道这个 customer 的标准有多高。它可以先交一小批 pilot task 拿早期反馈，判断标准，再决定剩下的 token 怎么分。
- 问题不变：team 会这样学习，会让 orchestrator 的分配更偏还是更均。

Bidding 不再是论文的主体，而是同一个骨架的另一个实例。

这一轮最重要的三个变化：

1. **微观模型重写了。** Bidding 里赢了才付钱；token 不论成败都要花。信息的价值不再来自 pacing，而来自 easy task 和 hard task 之间怎么分 token（triage）。
2. **ETC 从"假设的协议"变成"大部分可以由信息结构推出的结构"。** 还剩一处要明说的假设：早期反馈只有一轮。
3. **Evaluator 解释为 customer。** 反馈是一份 report，team 把它读成一个 satisfaction score；c 是 agent 读反馈花的 token，不是 evaluator 的成本。

时间线：

| 日期 | 做了什么 |
|---|---|
| 11-10 前后 | Repo 已有的工作：`bandit_check/`（ETC 换成 bandit 是否稳健）、`theory/`（bandit formulation、large-horizon limit）、文献综述 |
| 11-14 | 白板提案：把模型迁到 agent 设定。发现按原设定信息没有价值 |
| 11-15 | 改用 triage 模型；写出数学结构和证明；研究 learning premium 的形状（一个定理、一个反例）；grader 改称 evaluator；更正 planner 结论的表述；写给 advisor 的 note |
| 11-16 | Advisor 对评估成本 c 的质疑；report 方案；customer 与 satisfaction score；信息价值递减；ETC 和"看结果再停"的比较；和 few-shot learning 的区别 |
| 11-19 | 本记录 |

---

## 1. 起点：WITS 版本和 repo 里之前的讨论

### 1.1 WITS 版本（bidding）

- **对象**：一个 advertiser 的两个 bidding agent，planner 把总预算 T 分给它们。
- **单个 agent**：K 期，每期一次拍卖。市场的竞争程度 θ∈{θ_L, θ_H} 未知。出价 b 时赢的概率是 b/(b+θ)，赢了才付钱。
- **协议**：前 τ 期用 b^I=√(θ_Lθ_H) 探测（两个状态下胜率差最大的出价），之后按 posterior 用一个固定的 paced bid 把预算花完，不再更新。预算约束的形式是"当前 belief 下的期望花费等于剩余预算"。
- **价值**：V(B) 是对 τ 取最优之后的期望曝光，W(B) 是不学习的基准，learning premium 是 R=V−W。τ 取整数使 V 有折点，所以论文用 averaged（smoothed）模型 V̄ 得到可导的边际价值。
- **单 agent 结论**：学习只在一个有界的预算窗口内值得做（baseline 下入口在 B=56）。窗口内 V̄′/W′ 先高于 1、后低于 1。
- **分配定理**：在不学习时的最优分配 a^E 处比较两个 agent 的 V̄′/W′，决定学习使分配更偏还是更均。
- **标题结论**：junior agent 学不起时更偏；两个都学得起时更均（baseline 下在 T=184 到 185 之间切换）。

### 1.2 Repo 里之前的讨论（11-10 前后）

| 位置 | 内容 | 和这一轮的关系 |
|---|---|---|
| `bandit_check/` | 把 ETC team 换成边做边学的 agent，分配方向是否还成立。论文强调的两个区间内方向一致率 92%；尾部（T=3000 的再集中）不稳健；学习窗口的下边主要来自预算的记账方式，B<45.5 时连免费的完美信息都降低价值 | 第 6 节已经指出：token 不论成败都付费，最简单的映射下信息没有价值，微观模型必须重写。这一轮做的就是这件事 |
| `theory/bandit_formulation` | 把 K 期 bidding 问题写成一个优化问题，三个嵌套的 policy class：不学习、decomposition、full bandit | ETC 作为一个 policy class 的定位 |
| `theory/large_horizon_limit` | Proposition 1 至 5：K 大时 per-period premium 的极限与学习如何安排无关；decomposition 的学习成本是 log K 阶；n 个 team 的结论 | Bidding 模型的结果。Agent 模型里对应的大 team 结论见第 7 节 |
| `reports/` 文献综述 | 论文的六个特征、最接近的文献、ETC 与 bandit 之争的论据 | Positioning 沿用 |

### 1.3 当时留下的三个问题

1. 论文的最终目标是对 AI agent 有贡献，bidding 只是提供结构的实例。Advisor 的意见是按"Orchestrating Agent Teams"重写叙事，并且不再用 junior/senior 的叫法。
2. `bandit_check` 第 6 节的判断：在 orchestrator 层面 token 是好的 proxy，但单个 agent 的微观模型要重写。
3. Reviewer 的"为什么不用 bandit"。

---

## 2. 这一轮改了什么

### 2.1 对照表

| | WITS 版本（bidding） | 现在（agent team） |
|---|---|---|
| 分配者和资源 | Planner，广告预算 | Orchestrator，token |
| 学习的单位 | Bidding agent | Agent team，当作一个决策者 |
| 一期做什么 | 一次拍卖 | 一个 task，分 easy 和 hard，难度 d 做之前就看得见 |
| 未知量 θ | 市场的竞争程度 | Customer（evaluator）的标准 |
| 动作 | 出价 b | 给一个 task 的 token b |
| 成功概率 | b/(b+θ) | b/(b+θd) |
| 资源怎么花 | 赢了才付，期望花费依赖 θ | 投了就花掉，与 θ 无关 |
| 预算约束 | 在当前 belief 下取期望 | 在每条路径上都成立 |
| 反馈 | 每次拍卖后免费看到输赢 | 默认全部交付后才有，早期反馈要花 c |
| 信息为什么值钱 | Paced bid 依赖 belief | Easy 和 hard 之间怎么分 token 依赖 belief |
| 为什么先学后做 | 协议是假设的 | 大部分由信息结构推出（第 3 节） |
| 学习的成本 | 探测出价被压在 b^I | Pilot task 的 effort 被定在 b^I，加上读反馈的 c |
| 边际价值 | 需要 smoothed 模型 | 精确：V′ 等于期望 shadow price |
| 免费信息的价值 | 可以为负 | 恒非负 |
| 两个单位的称呼 | Senior，junior | Team 1，team 2 |
| Planner 结论的表述 | 一个学则更偏，两个都学则更均 | 一个方向判据，加上随 T 变化的三段 |

三个量分属三方：b 是 team 的选择，d 是 task 的属性，θ 是 customer 的属性。θd 是通过率达到 50% 所需的 token。

### 2.2 每一处为什么改

**成本结构。** Token 不论结果好坏都要花。直接照搬 bidding 的后果是：如果 task 都一样，最优永远是均分，与 belief 无关，信息一文不值。11-14 的数值：B=100 时不学习得 38.89 个通过，一开始就知道 θ 仍然是 38.89。Bidding 里信息值钱全靠"赢了才付"让花费依赖 θ，这一层在迁移时丢了。

**可观测的异质难度（triage）。** 让信息重新有用的办法是让 task 有 easy 和 hard 之分。标准宽松时值得在 hard task 上投入，标准严格时应该把 token 集中在还过得了的 easy task 上。Baseline 下 B=100、100 个 task 的期望通过数：

| | 不知道标准 | 知道标准 |
|---|---|---|
| 看不到难度 | 39.6 | 39.6 |
| 看得到难度 | 39.8 | 43.6 |

难度和标准是互补的：只有其中一个几乎没用，两个都有才多出约 4 个通过。这也回答了"难度看得见，为什么不让 agent 先扫一遍"：扫一遍只得到难度，得不到标准。

**θ 必须是 customer 的标准。** 如果 θ 是 task 的技术难度，team 从自己的工作里就能免费学到。把 θ 放在验收方，它才只能通过反馈看到。

**反馈要付费。** Bidding 里每次拍卖后都免费看到输赢。Agent team 的验收在系统之外，慢而且贵，所以反馈默认在全部交付之后才到，早期反馈要花 c。

**Planner 结论的表述。** "只有一个学则更偏，两个都学则更均"不对，两个都学时仍然可能更偏。能证的是方向判据：

F′(a^E) = v₁W′(a^E)·[H(a^E) − H(T−a^E)] = v₁R′(a^E) − v₂R′(T−a^E)，其中 H=V′/W′。

Baseline（v₁/v₂=2）下在 a^E 处的两项：

| T | a^E | T−a^E | v₁R′(a^E) | v₂R′(T−a^E) | 学习使分配 | 位置 |
|---|---|---|---|---|---|---|
| 100 | 76.1 | 23.9 | +0.0428 | 0 | 更偏 | Team 2 学不起 |
| 150 | 114.6 | 35.4 | +0.0035 | +0.0629 | 更均 | 都在上升段 |
| 300 | 207.9 | 92.1 | −0.0196 | +0.0113 | 更均 | Team 1 过峰，team 2 未过峰 |
| 500 | 331.8 | 168.2 | −0.0147 | −0.0085 | 更均 | 都在下降段 |
| 700 | 456.6 | 243.4 | −0.0063 | −0.0106 | 更偏 | 都在下降段 |

随 T 增大依次是更偏（约 40 到 110）、更均（约 112 到 560）、更偏（610 以上）。T=500 和 T=700 都在下降段而方向相反，所以"两个都学"或者"都过了峰"本身不决定方向。这和 bidding slides 里 T=150、250、3000 三张图的格局一致。

**理论上的变化。**

- 斜率公式是精确的，不再需要 smoothed 模型。
- 新的核心对象是"知道标准的价值"N(π;B)：免费被告知标准能多通过几个 task。已证它对预算严格单峰（第 7 节）。
- Exact premium 对所有参数单峰这件事不成立，有反例（τ 取整数造成）。所以用两个阈值 B̂ ≤ B̌ 来表述：R 在 B̂ 之前不减，在 B̌ 之后不增。

---

## 3. 为什么做成 ETC 版本

**ETC（explore-then-commit）** 指：先用一段时间只学习，然后按学到的东西定一个计划执行到底，不再更新。

### 3.1 WITS 版本已经是 ETC，但它是假设的

WITS 的协议（前 τ 期探测，之后固定出价）就是 ETC，只是没有这么叫。问题在于 bidding 里每次拍卖后都免费看到输赢，agent 完全可以一直学下去。"学完就不再更新"是我们加的假设，所以 reviewer 会问为什么不用 bandit。`bandit_check` 当时的回答是稳健性（主要区间内方向一致）加文献（两个已知假设时 ETC 只损失常数）。

用 ETC 重读 bidding 还得到三个发现，记在 Project 的 `agent_teams_notes.md` 第 2 节：

- Exact 模型里 K 每翻倍 τ\* 正好加 3，对应 Chernoff information 而不是 KL；smoothed 模型在 K 方向的斜率差了约 3.7 倍。
- 学习窗口的上边是 ETC 现象（探测出价被压在 b^I），下边不是。
- Bidding 里信息可能有害，和 `bandit_check` 的结论一致。

### 3.2 在 agent team 里，ETC 的三个组成部分各是什么地位

| ETC 的组成部分 | 在 bidding 里 | 在 agent team 里 |
|---|---|---|
| 学习排在最前面 | 假设 | 推出来的。早期反馈的代价不随时间变，而它对之后所有 task 都有用，所以越早越好（Project 里 `agent_theory.tex` 的 Proposition 3） |
| 学完之后不再更新 | 假设，反馈其实一直有 | 推出来的。早期反馈之外没有别的反馈，没有东西可以更新 |
| 学几个事先定好 | 假设 | 仍然是假设。在"早期反馈只有一轮"时它是最优的；否则看结果再停更好 |

所以在 agent team 里要辩护的只剩第三行。

### 3.3 ETC 不是最优，差多少

ETC 事先定好"交 8 个 pilot"，不管前几个结果如何。更好的做法是每看到一个结果再决定要不要继续。B=100 时的两条路径（F 是没通过，P 是通过）：

- **F F F**：P(strict) 已经是 0.985。此时停下的价值是 24.29，继续是 24.23，应该停。ETC 还要再做 5 个。
- **F P F P F P F P**：8 个之后 P(strict) 仍然是 0.50。继续的价值是 42.06，停下是 39.20。ETC 却必须在这里停。

同样的 pilot、同样的 0/1 结果，只改停止规则（数值）：

| B | 30 | 60 | 100 | 150 | 250 | 400 |
|---|---|---|---|---|---|---|
| ETC：premium (τ\*) | 0.25 (3) | 1.91 (7) | 2.71 (8) | 2.68 (6) | 1.73 (5) | 0.63 (3) |
| 看结果再停：premium | 0.32 | 2.19 | 3.13 | 3.18 | 2.15 | 0.86 |
| 看结果再停：平均 pilot 数 | 2.9 | 4.8 | 5.7 | 5.4 | 4.8 | 3.8 |

差距占 premium 的约 14% 到 37%，不超过总产出的约 1%。Premium 先升后降的形状不变。

### 3.4 为什么仍然用 ETC

- **现实对应**：一轮 pilot。Team 交一批 pilot，customer 一起看完一起回。每多一轮往返都要等 customer，所以数量必须事先定。在这个假设下 ETC 是最优的，不是限制。
- **可解析**：通过数 w 是充分统计量，V 是有限个光滑分支的上包络，斜率有精确公式。Orchestrator 的问题需要一个形状可以刻画的 V(B)。
- **结论稳健**：换成看结果再停，premium 的形状不变（上表）。
- **文献**：两个已知假设的情形下，固定长度的 ETC 相对完全序贯的策略只损失常数，不损失速率。细节见 `reports/多学习者预算分配文献综述.md`。

Pilot 用固定的 effort b^I 仍然是一个简化。

---

## 4. 为什么这个版本更契合 AI agent

在 bidding 里，ETC 的每一处都要辩护。在 agent team 里，模型的每个要素都对应一个可以指出来的现实特征：

| 模型的要素 | AI agent team 里对应什么 | 依据 |
|---|---|---|
| 预算事先给定，而且是硬约束 | Token 的 envelope：effort level、max_tokens、task budget。Lead agent 事先决定每个 subagent 的工作量，运行中不能干预 | Claude API 文档；Anthropic 的 multi-agent research system；企业按 team 和 task 设 token 上限 |
| 资源投了就花掉 | Token 不论结果好坏都计费 | |
| 标准在系统之外，team 不知道 | 验收由 code owner、client、合规方决定。通过自己的测试不等于被接受 | METR：296 个通过自动测试的 agent PR，maintainer 表示其中约一半不会合并 |
| 反馈贵而且慢 | 已部署的 agent 约四分之三主要靠人工评估 | Measuring Agents in Production |
| 先 pilot 再全量 | Airbnb 迁移约 3,500 个测试文件：先在小样本上调方法，再扫全量，最难的几个百分点留给人工 | Airbnb 工程博客 |
| 学的是标准，不是能力 | 部署后的 model 权重固定，任务期间不 fine-tune | |
| 难度事先可见 | Lead agent 按查询的复杂度事先分工作量 | Anthropic |

相对 bidding，这带来三个好处：

1. **Commit 不用辩护。** 反馈贵而且慢，pilot 之后没有新的信息，按当前判断执行到底是唯一能做的事。
2. **记账问题消失。** Bidding 里学习窗口的下边主要来自"按当前 belief 花完预算"的记账方式，免费信息甚至可能有害。Token 是确定性支出，预算在每条路径上都成立，信息项恒非负。下边的来源也变干净了：预算很小时，无论标准如何都只做 easy task，分配与 belief 无关，所以没有什么可学。
3. **边际价值是精确的。** 不需要 smoothed 模型。

仍然不贴合的地方，写论文时要主动承认：

- **返工。** Code review 里改了再交是常态，模型假设每个 task 只交付一次。
- **信息只改变分配。** 模型里知道标准只改变每个 task 分到多少 token；现实里它也改变活怎么干。
- **内部检查是免费的。** Team 自己的测试每个 task 都跑，它算在 b 里，不是模型里的 evaluator。Lead example 必须是有人或下游来验收的情形。
- **重复合作。** 同一个 customer 再来时标准已经知道了。模型描述的是新 customer 或新类型的 task。
- **没有单个公开案例具备全部要素。** Intro 用 composite，并且明说。

---

## 5. Customer 设定（11-16 和 advisor 讨论之后）

### 5.1 Advisor 的质疑

- 如果评估成本 c 对所有 task 是恒定的，就应该每个 task 结束后都评估。只有成本递增才会出现 ETC。
- 建议：evaluator 返回一份 report 而不是 0/1。一个"0"可能 99% 是对的，只差一两个参数。
- Mike 的新理解：c 不是 evaluator 的成本，而是做事的 agent 理解反馈并据此更新的成本。Evaluator 是外生的。

### 5.2 质疑里对的和不对的

反馈有两种用途：

| | 了解标准 θ | 修这个 task |
|---|---|---|
| 信息对谁有用 | 之后所有 task | 只对当前 task |
| 边际价值 | 递减 | 不递减 |
| c 恒定时的最优 | 开头评几个就停 | 每个都评，或者都不评 |
| 我们的模型 | 有 | 没有 |

- **不对的地方**：在我们的模型里，c 恒定也不会每个都评。ETC 只需要"边际收益递减"或"边际成本递增"之一，我们有前者。
- **对的地方**：Advisor 心里的 verifier 是"检查这个 task，错了就改"，那种用途的价值不递减。模型里没有返工这件事，需要明说。另外，如果 evaluator 是外生的而且只回一个 0/1，读一个 bit 几乎不花 token，c 就没有来源。

### 5.3 "关于共同 θ 的信息价值递减"是什么意思

所有 task 面对同一个 customer，θ 只有一个。每次评估都在回答同一个问题："这个 customer 严不严？"前几次已经回答了大半。

一条路径：B=100，customer 其实是 strict，8 个 pilot 的结果是 F F P F F F F P。这里为了说明，忽略 pilot 本身花掉的 token。

| 第几次 | 结果 | P(strict) | 计划：每个 easy / hard task 的 token | 还剩多少可学的价值 |
|---|---|---|---|---|
| 0 | | 0.50 | 1.16 / 0.84 | 3.78 |
| 1 | F | 0.80 | 1.87 / 0.13 | 2.95 |
| 2 | F | 0.94 | 2.00 / 0 | 0.89 |
| 3 | P | 0.80 | 1.87 / 0.13 | 2.95 |
| 4 | F | 0.94 | 2.00 / 0 | 0.89 |
| 5 | F | 0.985 | 2.00 / 0 | 0.23 |
| 6 | F | 0.996 | 2.00 / 0 | 0.06 |
| 7 | F | 0.999 | 2.00 / 0 | 0.015 |
| 8 | P | 0.996 | 2.00 / 0 | 0.06 |

最后一列是：如果此刻有人直接告诉 team 真实标准，期望能多通过几个 task。它是之后所有评估加起来的收益上限。第 8 次之后，把剩下 92 个 task 全部评估也最多再多通过 0.06 个，而一次评估的代价约为 0.1 个。

对所有可能的结果取平均，第 k 次评估新增的价值：

| k | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|
| 新增价值 | 1.37 | 0.71 | 0.45 | 0.34 | 0.22 | 0.18 | 0.12 | 0.10 | 0.07 |

知道标准的全部价值是 3.78，前 8 次已经拿到 3.48，约 92%。

打个比方：我们的模型像尝一锅汤，尝一两勺就知道咸不咸。Advisor 想的像 100 锅不同的汤，每锅都得尝。

### 5.4 Customer、report 和 satisfaction score

- **Customer。** Evaluator 是一个 customer：在系统之外，有自己的预期水平 θ（lenient 或 strict）。满意度取决于表现对比预期，这是营销和 IS 里的 expectation-disconfirmation 理论（Oliver 1980）。
- **Report 和分数。** Customer 的反馈是一份 report。Team 读完后把它概括成一个 **satisfaction score** s∈[−1, 1]，s ≥ 0 即接受。
- **c 的含义。** c 是 agent 把 report 读进 context 并据此更新所花的 token。

分数和现有模型的连接不需要新参数。通过率 b/(b+θd) 可以写成：

- 作品质量 = (b/d)·U，U 是和 θ 无关的运气，P(U>t)=1/(1+t)。
- 通过当且仅当质量 ≥ θ。
- Margin M = 质量/θ，也就是离 customer 的线有多远。分数是它的单调变换：s=(M−1)/(M+1)。
- 0/1 只说 M 是否 ≥ 1，是把分数压成两档。

这是一种自然的写法，不是唯一的，所以分数的分布是一个建模选择。

**Bayes update 仍然是一个数的更新**：posterior odds = prior odds × likelihood ratio。Baseline 下一个 pilot task 的 likelihood ratio 有闭式 ((5−3s)/(5+3s))²。从 prior 0.5 出发：

| 分数 s | −0.8 | −0.4 | −0.05 | 0 | +0.4 | +0.8 |
|---|---|---|---|---|---|---|
| P(strict) | 0.89 | 0.73 | 0.53 | 0.50 | 0.27 | 0.11 |

0/1 模型只有两个值：没通过是 0.80，通过是 0.20。Advisor 的例子正好落在这里：一个"差一点"的没通过（s=−0.05）几乎不说明 customer 严不严，而 0/1 模型把它和"差很远"的没通过混在一起，都更新到 0.80。

如果把分数分成四档，更新就是查一张表：

| Report 归档 | Lenient 下概率 | Strict 下概率 | Likelihood ratio | Posterior P(strict) |
|---|---|---|---|---|
| 差很远（M<0.25） | 0.059 | 0.500 | 8.5 | 0.895 |
| 差一点（0.25≤M<1） | 0.141 | 0.300 | 2.1 | 0.680 |
| 刚好过（1≤M<4） | 0.300 | 0.141 | 0.47 | 0.320 |
| 远超（M≥4） | 0.500 | 0.059 | 0.12 | 0.105 |

模型的其余部分不变：commit problem、V、W、premium 和 orchestrator 的问题都只通过 posterior 依赖 learning 的结果。

### 5.5 三条约定

1. **分数是 signal，不是 payoff。** 目标函数仍然是被接受的 task 数。如果改成最大化分数之和，response function 就变了（pilot effort 下平均分是 ±0.43，而 2p−1 是 ±0.6），commit problem 和已有的代数都要重做。
2. **分数是相对 customer 自己标准的，不是绝对完成度。** 低分可能是做得差，也可能是 customer 严，team 分不清，这正是要学的东西。如果分数只反映绝对质量，它对 θ 没有信息。
3. **模型里叫 satisfaction score，不叫 sentiment。** Sentiment 只是一种测量方式，而且问题不少：语气不等于质量；"99% 对"的 report 逐句平均是正面的，结果却是没通过；通用的 sentiment 工具在软件工程文本上不可靠（Jongeling et al. 2017）。更干净的测量是 customer 直接给的 rating，或者 agent 按 rubric 给 report 打分。

### 5.6 更细的反馈值多少

每次评估的 token 成本保持 s=0.7 不变，只改一次评估带回多少信息（数值；括号里是 τ\*）：

| B | 30 | 60 | 100 | 150 | 250 | 400 |
|---|---|---|---|---|---|---|
| 0/1 | 0.25 (3) | 1.91 (7) | 2.71 (8) | 2.68 (6) | 1.73 (5) | 0.63 (3) |
| 四档 | 0.28 (2) | 2.01 (6) | 2.86 (6) | 2.88 (6) | 1.93 (4) | 0.77 (3) |
| 连续分数 | 0.29 (3) | 2.04 (6) | 2.91 (6) | 2.93 (6) | 2.00 (4) | 0.81 (3) |
| 一份 report 就揭示标准 | 0.57 | 2.56 | 3.69 | 3.98 | 3.28 | 1.83 |
| 免费知道标准（N） | 0.64 | 2.63 | 3.78 | 4.11 | 3.48 | 2.08 |

连续分数一行是 Monte Carlo，误差约 ±0.005。

- "离线有多远"这种反馈只比 0/1 多一点信息。衡量区分度的 Bhattacharyya coefficient 从 0.80 降到 0.755（四档）和 0.739（连续）。
- 大的提升只有在 report 直接描述标准本身时才有。那时 τ 只取 0 或 1，学习区间约为 22 到 1127，τ 在相邻取值之间换档造成的反例不再出现。这时 premium 是 N 减去一个随预算变化的成本项，它本身是否单峰还要再证一步。

目前的倾向：正文保留 0/1（统计量就是 w，最简单），把 report 写成"归入 J 档之一、各档概率已知"的一般形式，J=2 是 baseline。

### 5.7 现在需要写明的假设

给 advisor 的 note 里已有五条：exogenous evaluator、observable difficulty、committed effort、diminishing returns、costly early evaluation。这一轮讨论之后要补上或改写的：

1. **每个 task 只交付一次。** 早期反馈只用于后面的 task，不用来改被评估的那个 task。
2. **早期反馈只有一轮。** Pilot 一批交、一起回，所以数量事先定。
3. **Agent 的能力在任务期间不变。** 权重固定是主要理由，但还不够：需要的是从 (b, d, θ) 到通过率的函数对每个 task 都一样，唯一跨 task 传递的是对 θ 的判断。
4. **一个 team 面对同一个 customer。** 已经包含在 exogenous evaluator 里，值得单独强调：task 来自标准各异的不同 customer 时，学到的东西无法迁移。
5. **Costly early evaluation 要改写。** c 是 agent 读反馈的 token 成本，反馈是 report。Note 里现在把成本放在 evaluator 一侧，这句要改。

这些还没有写进 note。

---

## 6. Reviewer 可能的问题和目前的回答

| 问题 | 目前的回答 | 还缺什么 |
|---|---|---|
| c 恒定，为什么不每个 task 都评 | 关于共同 θ 的信息价值递减（5.3）；每个 task 只交付一次 | 返工的 robustness |
| 为什么不是 bandit 或者自适应策略 | Pilot 之后没有新反馈，commit 是推出来的；一轮反馈下固定数量是最优的；看结果再停时形状不变（3.3） | 把 3.3 的表写成正式的 robustness |
| 这不就是 few-shot learning 吗 | "几个例子就够"是前提，不是贡献。Few-shot learning 研究给了 k 个例子 model 能做多好；我们研究该不该买例子、买几个、预算怎么跟着重分。我们的例子要自己花 token 换，有噪声，和干活抢同一笔预算。学习只在一段预算区间内值得、分配方向的三段，这两个结论 few-shot learning 给不出 | 信息在模型里只通过分配起作用，这一点放进 discussion 主动承认 |
| Agent 为什么不知道自己做得对不对 | 它知道是否通过自己的检查，不知道 customer 的标准（METR 的证据） | Lead example 要选准 |
| 难度看得见，为什么不先扫一遍 | 扫一遍得到难度，得不到标准；两者互补（2.2 的表） | |
| 和 model 的 effort level 有什么区别 | Effort level 是工具。我们研究的是它外面的问题：在一个预算下给很多 task 设定它，设定取决于一个未知的标准，以及 orchestrator 怎么在 team 之间分预算 | |
| Agent 是生成到结束为止，事前分配合理吗 | 模型里的预算是事先设的 envelope，不是实际生成的 token 数 | Envelope 内实际消耗是随机的，模型没有刻画 |
| 学习的成本从哪来 | c 是读反馈的 token；pilot task 的 effort 被固定在 b^I | 对正常 effort 完成的 task 评估的版本 |

---

## 7. 证明状态

以下"已证"都指 Project 里的草稿，待 Mike 核对。

| 结论 | 状态 |
|---|---|
| Commit phase：同类 task 均分、triage 门槛、shadow price、G 对 belief 凸 | 已证 |
| V(τ;·) 对预算凹，斜率等于期望 shadow price | 已证 |
| V−W 等于信息项减成本项，信息项非负；task 相同则永不学习 | 已证 |
| 学习窗口有界；下界是紧的（baseline 下 18.75） | 已证 |
| 付费评估排在最前 | 已证 |
| 分配方向恒等式；pairwise dominance | 已证 |
| 只有 team 1 学得起时更偏 | 已证，范围是 T/2 不超过学习门槛（baseline 下 T≤51）；之后到 T≈110 是数值 |
| 知道标准的价值 N(π;B) 对预算严格单峰（baseline 形式，所有参数） | 已证 |
| N − ½Kρ^τ − τχ ≤ V(τ;B)−W(B) ≤ R ≤ N | 已证，但 K=100 时下界是空的，是大 team 的结论 |
| R 在 [0, B↑] 上不减（baseline 下 B↑=30.14） | 已证，只覆盖上升段的开头 |
| Exact premium 对所有参数单峰 | 不成立，有反例（c=0.205 时有两个局部极大） |
| R 在某个显式预算之后不增 | 未解决 |
| 两个 team 都学时的方向（都在上升段、都在下降段） | 只有数值和一个条件性结论 |
| 第 3.3、5.3、5.4、5.6 节的表 | 数值 |
| 哪些证明用到了 0/1 的 binomial 结构，换成分数后是否还成立 | 没有逐条核对 |

Baseline 下的单个 team（0/1，ETC）：

| B | 20 | 26 | 30 | 40 | 60 | 100 | 122 | 160 | 250 | 400 | 600 | 720 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| τ\* | 0 | 1 | 3 | 5 | 7 | 8 | 7 | 6 | 5 | 3 | 1 | 0 |
| Premium R | 0 | 0.03 | 0.25 | 0.92 | 1.91 | 2.71 | 2.77 | 2.61 | 1.73 | 0.63 | 0.11 | 0 |
| H=V′/W′ | 1 | 1.12 | 1.28 | 1.27 | 1.19 | 1.05 | 1.00 | 0.92 | 0.83 | 0.87 | 0.95 | 1 |

学习区间约为 25 到 705。Premium 的峰在 B≈120.2（R=2.774）；N 的峰在 B≈149（4.11）。

---

## 8. 未决问题和下一步

1. **Mike 核对证明。** 所有"已证"都还没有核对。
2. **把 customer 设定写进给 advisor 的 note。** 第 5.7 节的五处改动。
3. **两个要定的选择。** 正文用 0/1 还是 J 档分数；理论核心放在 N（已证单峰）还是 exact premium（下降段未解决）。
4. **返工。** 目前靠假设排除。需要想清楚是否做一个 robustness，或者把适用范围限定在不能返工的交付上。
5. **信息改变做法本身。** 模型里信息只改变分配，这是 few-shot 那个质疑真正指向的地方。
6. **两个 team 面对同一个 customer。** 谁替大家学。
7. **Bidding 和 agent team 的统一模型。** 现在的说法是同一个骨架的两个实例，嵌套两者的一般形式还没有写。
8. **把推导和脚本放进 repo。** 见第 9 节。

---

## 9. 参数、文件和来源

**Baseline 参数**：θ_L=½，θ_H=8，π₀=½，b^I=2，K=100，easy 和 hard 各 50 个，d_e=¼，d_h=4，c=0.2，所以一个 pilot task 用 s=0.7 个 token，在 lenient 和 strict 下的通过率是 0.8 和 0.2。两个 team 时 v₁/v₂=2。

**详细推导在哪里**。以下文件在 claude.ai 的 Project "Agent Coordination" 里，还不在这个 repo：

| 文件 | 内容 |
|---|---|
| `claude/agent_coordination_note.tex` | 给 advisor 的 note：背景、研究问题、设定、单 team 问题、orchestrator 问题。不含推导结果，也还没有 customer 设定 |
| `claude/agent_theory.tex` | Agent 模型的数学结构、推导和证明状态 |
| `claude/agent_premium_shape.tex` | Premium 的形状：N 单峰的证明、反例、上升段 |
| `claude/agent_teams_notes.md` | 11-14 至 11-15 的讨论记录，包括更正记录 |

**本文数字的来源**。第 3.3、5.3、5.4、5.6 节的表来自 11-16 写的几个脚本（`advisor_c.py`、`report_update.py`、`sentiment_score.py`、`diminishing.py`、`adaptive_stop.py`，都依赖 `sp_check.py` 里的模型求解器）。这些脚本也还不在这个 repo。

**外部来源**：

- METR, Many SWE-bench-Passing PRs Would Not Be Merged into Main: https://metr.org/notes/2026-03-10-many-swe-bench-passing-prs-would-not-be-merged-into-main/
- Measuring Agents in Production: https://arxiv.org/abs/2512.04123
- Anthropic, How we built our multi-agent research system: https://www.anthropic.com/engineering/multi-agent-research-system
- Airbnb, Accelerating Large-Scale Test Migration with LLMs: https://airbnb.tech/?p=366
- Claude Platform Docs, effort 和 task budgets: https://platform.claude.com/docs/en/build-with-claude/effort ， https://platform.claude.com/docs/en/build-with-claude/task-budgets
- Claude Code agent teams: https://code.claude.com/docs/en/agent-teams
- Jongeling, Sarkar, Datta & Serebrenik (2017), On negative results when using sentiment analysis tools for software engineering research, Empirical Software Engineering 22: https://doi.org/10.1007/s10664-016-9493-x
- Oliver (1980), A Cognitive Model of the Antecedents and Consequences of Satisfaction Decisions, Journal of Marketing Research 17(4)
- ETC 与完全序贯策略的比较（Garivier, Kaufmann & Lattimore 2016 等）：见 `reports/多学习者预算分配文献综述.md`
