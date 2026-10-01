# 检索批次 control-051

[返回完整排序](../ranked_candidates.md) · [本批完整 JSON](control-051.json) · [评分与字段](../README.md)

本批 **1 位**。首次发现时间保持不变；资料修正通过独立提交保留历史。分数是研究筛选优先级，不是接收概率。

<a id="bowen-weng"></a>

## Bowen Weng · Iowa State University

- 稳定键：`bowen-weng`；[导师主页](https://www.cs.iastate.edu/people/bowen-weng)
- 任职：Assistant Professor
- 方向：Safety evaluation of learned robots；Sim-to-real performance certification；Humanoid systems；Autonomous-system testing
- 匹配理由：Strong match for statistical assurance and evaluation of learned physical robot policies, with current local humanoid experiments. Policy certification is the main computational contribution; it should not be described as learning a new end-to-end controller.
- 真机证据（public-hardware-evidence）：August 2026 Betting for Sim-to-Real Performance Certificates reports live Unitree G1 command-tracking tests using GR00T WholeBodyControl. Its mobile-manipulator and quadruped cases replay existing test outcomes rather than rerun hardware. The separate August 2026 football study uses a G1 and Dex3-1 hand, RL-based GR00T lower-body control, optimized upper-body trajectories and lookup-table MPC follow-through. Online MPC was too slow; the actual throwing method is hybrid rather than an end-to-end learned throwing policy. Official Spring 2026 reporting confirms Weng’s local graduate research team, two humanoids and a quadruped.
- 短访证据（unknown）：Current official faculty page verifies the position and public email. No external short-visitor invitation was found in the reviewed primary sources. The presence of graduate researchers does not establish an available summer placement.
- 首次发现：2026-10-01T02:42:28Z；最后核查：2026-10-01T02:53:44Z
- 当前总分：78/100；评分依据：
  - fit 38/40：Direct learned-policy assurance, simulator-to-real statistical methods and hybrid humanoid control.
  - physical 25/25：Current Iowa State G1 experiments with named local graduate researchers and official laboratory hardware confirmation.
  - shortVisit 0/20：No verified current external visitor invitation or compatible short program.
  - freshness 15/15：Two August 2026 primary studies and Spring 2026 university laboratory reporting.
- 未确认事项：Eight-week availability, external master’s eligibility, appointment, funding, access and institutional approval all require confirmation. Do not equate ordinary degree supervision or public code availability with visiting-student acceptance.；Public robot research does not confirm current equipment access, a summer 2027 offer or host availability.
- 来源：
  - [www.cs.iastate.edu / source 1](https://www.cs.iastate.edu/people/bowen-weng)：Current Assistant Professor of Computer Science; public email. Publications widget errors, so research claims use separate primary sources.（核查 2026-10-01T02:53:44Z；读取方式 Direct official or author-primary page via web.run）
  - [iowastater.iastate.edu / source 2](https://iowastater.iastate.edu/spring-2026/article/iowa-state-graduate-students-get-hands-research-experience-humanoid-robots)：Official Spring 2026 laboratory and graduate-researcher feature establishes current local robots and supervision.（核查 2026-10-01T02:53:44Z；读取方式 Direct official or author-primary page via web.run）
  - [arxiv.org / source 3](https://arxiv.org/html/2608.21572v1)：August 21, 2026 primary paper: actual G1 runtime evaluation, simulator-guided statistical certificates; other hardware cases use replayed datasets.（核查 2026-10-01T02:53:44Z；读取方式 Direct official or author-primary page via web.run）
  - [arxiv.org / source 4](https://arxiv.org/html/2608.16642v1)：August 17, 2026 primary paper: actual G1 football throws, GR00T leg controller and offline lookup-table MPC; online MPC infeasible at the required rate.（核查 2026-10-01T02:53:44Z；读取方式 Direct official or author-primary page via web.run）
  - [github.com / source 5](https://github.com/NVlabs/GR00T-WholeBodyControl)：Official NVIDIA implementation specifies decoupled WBC uses RL for the lower body and inverse kinematics for upper body. Used only to characterize the controller incorporated by Weng’s studies.（核查 2026-10-01T02:53:44Z；读取方式 Direct official or author-primary page via web.run）

