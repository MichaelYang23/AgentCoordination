# Agent team 模型的数值核对

> 对象：[`theory/agent_teams/`](../theory/agent_teams/) 里的三份笔记，以及 [`worklog/`](../worklog/) 里 2026-11-15 和 2026-11-19 的两份记录。
>
> 这里的脚本只算表和做核对，不是任何证明的一部分。除了 `premium_shape_checks.py` 里的随机抽样，所有数字都只在 baseline 参数下算过。

---

## 模型和 baseline

一个 team 有 K 个 task，分 easy（难度 d_e）和 hard（难度 d_h），难度做之前就看得见。Evaluator 的标准 θ∈{θ_L, θ_H} 未知。在一个难度为 d 的 task 上花 b 个 token，通过率是 b/(b+θd)。Team 有 B 个 token，可以先做 τ 个 learning task（easy task，effort 固定在 d_e·b^I，每个再花 c 拿早期评估），更新对 θ 的判断，再把剩下的 token 分给剩下的 task。V(B) 是会学习时的期望通过数，W(B) 是不学习时的，learning premium 是 R=V−W。

Baseline：θ_L=½，θ_H=8，π₀=½，b^I=2，K=100，easy 和 hard 各 50 个，d_e=¼，d_h=4，c=0.2。一个 learning task 用 s=0.7 个 token，在 lenient 和 strict 下的通过率是 0.8 和 0.2。两个 team 时 v₁/v₂=2。

## 脚本

"秒"是 2026-11-19 在一台两核机器上的运行时间。

**模型和 `agent_theory.tex`**

| 脚本 | 算什么 | 对应 | 秒 |
|---|---|---|---|
| `agent_model.py` | Exact 模型的求解器：commit problem 的 value 和 shadow price，V(τ;B) 及其对 B 的斜率。直接运行时在 B∈[100,160] 上细网格扫描 premium | 下面多数脚本的依赖；premium 的峰在 120.2 | 12 |
| `verify_theory.py` | 标准已知时的闭式；斜率公式对比中心差分；V−W=A−C 的分解；单个 team 的表（τ\*、R、H、知道标准的价值）；token 有价格时的需求 | `agent_theory.tex` 第 12 节，Table 3 和 Table 6 | 54 |
| `story.py` | B=100 的例子；单个 team 在步长 2 的网格上的曲线；两个 team 的分配表 | `agent_coordination_note.tex` Table 3；`agent_theory.tex` Table 4 | 10 |
| `complements.py` | 看不看得到难度、知不知道标准的 2×2 表 | `agent_coordination_note.tex` Table 1 | 1 |
| `refine.py` | Learning window：下界、下界附近免费信息的价值、入口和出口、保守上界 | `agent_theory.tex` Proposition 2 | 3 |
| `regimes.py` | 方向恒等式在 a^E 处的两项 v₁R′(a^E) 和 v₂R′(T−a^E) | `agent_theory.tex` Table 5 | 1 |
| `prior_compare.py` | Two-point prior 对比 lognormal prior，K 从 100 到 3200 | `agent_theory.tex` 第 12 节末尾 | 3 |

**`agent_premium_shape.tex`**

| 脚本 | 算什么 | 对应 | 秒 |
|---|---|---|---|
| `premium_shape_checks.py` | N 的 loss 表示；iso-loss 曲线的曲率（3000 次随机抽样）；N_B 只变号一次（400 次随机抽样）；sandwich 的常数；上升段；两个峰的例子；两个符号恒等式（需要 sympy）。自包含 | 全文；笔记第 8 节列出了这些核对 | 20 |
| `scallop.py` | 对评估费 c 从 0.20 到 0.80 扫描，各个 branch 的峰 | Example 1 | 5 |
| `scallop2.py` | c 从 0.200 到 0.230 的细扫描：τ=7 和 τ=6 两个 branch 的峰和交点。交点落在两个峰之间时 premium 有两个局部极大 | Example 1 | 1 |

**11-16 的讨论（`worklog/2026-11-19_agent_teams_etc_customer.md`）**

| 脚本 | 算什么 | 对应 | 秒 |
|---|---|---|---|
| `advisor_c.py` | B=100 时第 k 次评估新增的信息价值；"一份 report 就揭示标准"的变体 | 第 5.3、5.6 节 | 1 |
| `diminishing.py` | 一条路径上 belief、计划和"还剩多少可学的价值"怎么变 | 第 5.3 节 | 1 |
| `report_update.py` | 四档 report：各档的概率、likelihood ratio、posterior；Bhattacharyya coefficient；premium | 第 5.4、5.6 节 | 3 |
| `satisfaction_score.py` | 连续的 satisfaction score：分数到 posterior、平均分、premium。Premium 用 Monte Carlo，种子固定，误差约 ±0.005 | 第 5.4 至 5.6 节 | 16 |
| `adaptive_stop.py` | 事先定好数量的 ETC 对比"看结果再停" | 第 3.3 节的表 | 4 |
| `adaptive_stop_states.py` | B=100 时每个状态（做了几个 pilot、通过几个）下停和继续的价值 | 第 3.3 节的两条路径 | 1 |

**从 bidding 迁移（11-14；`worklog/2026-11-15_agent_teams_notes.md`）**

| 脚本 | 算什么 | 对应 | 秒 |
|---|---|---|---|
| `homogeneous_and_cap.py` | Task 都一样时信息没有价值（38.89）；有 easy 和 hard 时的 premium；cap / give-up 方案 | 第 3 节 | 3 |
| `etc_decomp.py` | Bidding 模型：premium 拆成免费信息的价值、win displacement、spend drain；免费完美信息开始有价值的预算（45.58） | 第 2 节 | 5 |
| `loglaw.py` | Bidding 模型：K 翻倍时 τ\* 怎么涨，exact 模型对比 averaged 模型 | 第 2 节 | 3 |

## 运行

```bash
pip install numpy scipy sympy      # sympy 只有 premium_shape_checks.py 的最后一步用到
cd agent_check
python verify_theory.py            # 或其他任何一个脚本；输出打印到屏幕
```

每个脚本都从本目录运行，不读写别的文件。

## 结果

[`results/`](results/) 里是 2026-11-19 每个脚本的完整输出，文件名和脚本同名。文档和工作记录里的数字都能在这些输出里找到。输出里的"curve time"和方括号里的秒数是当时的运行时间，换机器会变。

## 说明

- **两套求解器。** `agent_model.py` 用 shadow price 求根；`story.py`、`refine.py`、`verify_theory.py`、`prior_compare.py` 和 `homogeneous_and_cap.py` 写得更早，各自带一个一维有界最小化的求解器。两者的结果一致，例如 B=100 时 premium 都是 2.7065。
- **和 Project 里名字的对应。** 四个脚本放进 repo 时改了名：`sp_check.py` 改为 `agent_model.py`，`sentiment_score.py` 改为 `satisfaction_score.py`（模型里这个量叫 satisfaction score），`adaptive_stop2.py` 改为 `adaptive_stop_states.py`，`ai_agent2.py` 改为 `homogeneous_and_cap.py`。`complements.py` 是 11-19 新写的。其余脚本名字不变。
- **没有放进来的。** 探索用的草稿脚本没有放进来。`agent_model_section.tex`（论文体的 model section）比 `agent_theory.tex` 早一版，其中学习窗口下界的式子还是旧的，同步之前也没有放进来。
