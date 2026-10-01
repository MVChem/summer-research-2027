# 检索批次 embodied-084

[返回完整排序](../ranked_candidates.md) · [本批完整 JSON](embodied-084.json) · [评分与字段](../README.md)

本批 **1 位**。首次发现时间保持不变；资料修正通过独立提交保留历史。分数是研究筛选优先级，不是接收概率。

<a id="wojciech-matusik"></a>

## Wojciech Matusik · Massachusetts Institute of Technology

- 稳定键：`wojciech-matusik`；[导师主页](https://people.csail.mit.edu/wojciech/)
- 任职：Cadence Design Systems Professor
- 方向：Neural robot dynamics and force perception；Robot assembly and imitation learning；Differentiable physics；AI for physical design and scientific discovery
- 匹配理由：Strong robot-learning and AI-for-physical-systems option, with current neural actuation, contact-aware control and computational design. A CS project could investigate learned dynamics, force-aware imitation or efficient model transfer. The lab also explicitly considers visiting students, though a suitable eight-week project and funding arrangement need individual approval.
- 真机证据（public-hardware-evidence）：Full July 2026 NeuralActuator §IV-I and AppendixF verify real OpenManipulator-X control: a frozen learned force-estimation model supplies live telemetry-based feedback to Transformer behavior-cloning policies for lift-and-hold and pick-and-place. TableXIII reports40-trial evaluations, with 92.5% and 95% success versus80% and 85% position-only baselines. This is actual learned feedback controlling hardware, beyond recorded-data modeling. The full official 2025 Fabrica project also documents residual-RL dual-arm assembly, but the score does not require treating its shared Panda as solely CDFG-owned.
- 短访证据（inquiry-only · case-by-case；MIT访学生资金需至少51%非个人）：Current full CDFG joining page explicitly considers visiting students and researchers case by case, asking for dates and funding situation. This is separate from PhD admissions, postdocs and MIT-only UROP. It is a generic student-visitor inquiry route, not explicit outside-master acceptance, funding, eight-week availability or a summer 2027 offer. Visitor8.
- 首次发现：2026-10-01T10:42:07Z；最后核查：2026-10-01T10:47:43Z
- 当前总分：87/100；评分依据：
  - fit 39/40：Strong neural models, robot learning, contact-aware control and physical design.
  - physical 25/25：Full 2026 actual causal force-aware learned manipulation; offline platforms explicitly separated.
  - shortVisit 8/20：Explicit generic visitor inquiry, without master/duration guarantee.
  - freshness 15/15：July 2026 complete paper, current group and recruitment pages.
- 未确认事项：Official MIT EECS page verifies current named professorship and wojciech@csail.mit.edu; the faculty/lab pages use wojciech@mit.edu. Both are public professional aliases, not two people.；NeuralActuator’s Franka experiment is an offline benchmark using a future-recorded-state proxy, not real-time Franka control. SO-101 validates modeling/perception; the verified downstream policy is the low-cost four-arm-joint-plus-gripper system. Keep these platform roles separate.；Actuation outputs are simulator-equivalent surrogates, not identified true torques. Force labels are supervised during training. The evaluated loads lie within pretraining range;500g pick-and-place is also in BC demonstrations, so avoid unseen-payload or broad zero-shot generalization claims.；The Fabrica project acknowledges Adelson-lab Panda support. Its real assembly and modern learning agenda corroborate fit, without implying every apparatus is independently owned or available to a visitor.；Reuse mit-visiting-students: overseas enrolled graduate visitors require faculty invitation and formal ISO approval; published range3weeks–12months can encompass eight weeks, but dates must conform to current rules. At least51% of total support must be non-personal; fully self/family-funded participation is not eligible under this route.；Existing MIT note gives 2026–27 support estimate$4350/month including$625 monthly fee, complete documents≥90days ahead, plus separate$1000 processing fee from PI discretionary funds. CSAIL’s older local guide has additional approvals/120-day lead; confirm current local application details.2027 funding, exact dates, project access, mentor capacity and remote options remain unresolved.；Public robot research does not confirm current equipment access, a summer 2027 offer or host availability.；Timestamp scope: Earliest precisely retained candidate-specific primary-name occurrence; earlier incidental coauthor encounters were not precisely timestamped and are not reconstructed.；[Institutional visitor rules](../eligibility_notes.md#mit-visiting-students)
- 来源：
  - [www.eecs.mit.edu / source 1](https://www.eecs.mit.edu/people/wojciech-matusik/)：Full official current professorship and professional email.（核查 2026-10-01T10:47:43Z；读取方式 direct-primary-page）
  - [people.csail.mit.edu / source 2](https://people.csail.mit.edu/wojciech/)：Full present group/department roles, physical-AI agenda and contact.（核查 2026-10-01T10:47:43Z；读取方式 direct-primary-page）
  - [cdfg.mit.edu / source 3](https://cdfg.mit.edu/join/)：Full distinct case-by-case visiting-student/researcher paragraph requests dates and funding situation.（核查 2026-10-01T10:47:43Z；读取方式 direct-primary-page）
  - [cdfg.mit.edu / source 4](https://cdfg.mit.edu/people/)：Full current directed group, distinct from historic alumni.（核查 2026-10-01T10:47:43Z；读取方式 direct-primary-page）
  - [arxiv.org / source 5](https://arxiv.org/html/2607.11734v1)：Full July 2026 NeuralActuator, §IV-I/AppendixF live control and AppendixB offline Franka caveat.（核查 2026-10-01T10:47:43Z；读取方式 direct-primary-full-paper）
  - [frank-zy-dou.github.io / source 6](https://frank-zy-dou.github.io/projects/NeuralActuator/index.html)：Full author project corroborates current MIT work and distinct platform roles.（核查 2026-10-01T10:47:43Z；读取方式 direct-primary-project）
  - [fabrica.csail.mit.edu / source 7](https://fabrica.csail.mit.edu/)：Full 2025 author project: residual-RL physical dual-arm assembly and shared hardware acknowledgment; secondary fit corroboration.（核查 2026-10-01T10:47:43Z；读取方式 direct-primary-project）

