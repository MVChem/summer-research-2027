# 检索批次 control-091

[返回完整排序](../ranked_candidates.md) · [本批完整 JSON](control-091.json) · [评分与字段](../README.md)

本批 **2 位**。首次发现时间保持不变；资料修正通过独立提交保留历史。分数是研究筛选优先级，不是接收概率。

<a id="luis-antonio-garcia"></a>

## Luis Antonio Garcia · University of Utah

- 稳定键：`luis-antonio-garcia`；[导师主页](https://iotrustlab.com/)
- 任职：Assistant Professor
- 方向：Trustworthy learning-enabled robotics；Neurosymbolic SLAM；Sim-to-real reinforcement learning；Cyber-physical systems safety
- 匹配理由：Visitor-first trustworthy-robotics option with a current short-visit invitation, substantive recent learned perception methods and fully verified earlier physical RL.
- 真机证据（Earlier UCLA collaborative physical RL verified; current Utah learned hardware unknown）：CoRL 2020, published in PMLR 2021, deploys PPO-trained Time-in-State RL on an actual1/18-scale DeepRacer. Camera features are fused with execution latency and sampling interval; the policy controls steering and speed on a7.3m indoor track, measured with OptiTrack. Training is in Gazebo and legged HalfCheetah/Ant results are simulation. Garcia’s affiliation explicitly says USC ISI, work performed at UCLA: this is prior collaborative hardware, not current Utah access. Physical18. The 2024 nFEX paper learns feature-extractor parameters with symbolic selection but evaluates KITTI, EuRoC and HoloSet datasets; the 2025 property-guided drone paper evaluates surrogate simulation. Neither supplies new learned robot execution.
- 短访证据（inquiry-only · 短期scholar询问；硕士类别与八周需确认）：The live IOTrust homepage explicitly lists visiting scholars for short-term visits around shared systems problems and experimental platforms. This is a general scholar invitation, not a guaranteed external-master place or a funded 2027 offer. The detailed opportunities page describes cross-institution collaborators but does not specify a minimum visit or graduate visitor intake. Utah’s institutional master-student pathway must be arranged individually.
- 首次发现：2026-10-01T10:14:16Z；最后核查：2026-10-01T10:17:12Z
- 当前总分：70/100；评分依据：
  - fit 34/40：Substantive robot-learning/perception track with broader current CPS/security emphasis.
  - physical 18/25：Complete older collaborative real-car policy experiment; no current Utah learned platform claimed.
  - shortVisit 8/20：Explicit general short-term scholar invitation, with master-level acceptance unresolved.
  - freshness 10/15：Dated 2025 robotic safety work; current undated invitation is not itself a 2026 event.
- 未确认事项：Reuse Utah notes: the Visiting Graduate Student title explicitly includes master’s candidates and requires academic-unit/Graduate School approval; its honorary appointment is unpaid. The separate Student Intern route permits degree-linked outside study for 3weeks–12months, at least32hours/week, with return to the home degree, DS7002 and review. Personal funds are accepted institutionally; current support minimum$2,400/month and$350 department processing charge require 2027 confirmation. The lab must confirm master-level eligibility, project scope, hardware availability and sponsorship; one-semester generic scholar wording must not automatically replace the separate graduate category.；Public robot research does not confirm current equipment access, a summer 2027 offer or host availability.；[Institutional visitor rules](../eligibility_notes.md#utah)
- 来源：
  - [people.utah.edu / source 1](https://people.utah.edu/basic.hml?eid=224139356)：Current University of Utah faculty appointment and email.（核查 2026-10-01T10:17:12Z；读取方式 Direct official or author-controlled primary source; complete paper methods inspected）
  - [www.cs.utah.edu / source 2](https://www.cs.utah.edu/people/faculty/)：Current Kahlert faculty listing independently verifies the host.（核查 2026-10-01T10:17:12Z；读取方式 Direct official or author-controlled primary source; complete paper methods inspected）
  - [iotrustlab.com / source 3](https://iotrustlab.com/)：Current PI lab and explicit short-term visiting-scholar route.（核查 2026-10-01T10:17:12Z；读取方式 Direct official or author-controlled primary source; complete paper methods inspected）
  - [iotrustlab.com / source 4](https://iotrustlab.com/opportunities/)：Detailed intake instructions; no master-specific promise or 2027 date.（核查 2026-10-01T10:17:12Z；读取方式 Direct official or author-controlled primary source; complete paper methods inspected）
  - [proceedings.mlr.press / source 5](https://proceedings.mlr.press/v155/sandha21a/sandha21a.pdf)：Complete primary methods: actual DeepRacer timing-aware PPO, prior UCLA location explicitly disclosed; legged experiments simulated.（核查 2026-10-01T10:17:12Z；读取方式 Direct official or author-controlled primary source; complete paper methods inspected）
  - [arxiv.org / source 6](https://arxiv.org/html/2407.06889v2)：Complete 2024 nFEX neural/symbolic feature adaptation and dataset-only validation; Utah affiliation.（核查 2026-10-01T10:17:12Z；读取方式 Direct official or author-controlled primary source; complete paper methods inspected）
  - [arxiv.org / source 7](https://arxiv.org/html/2512.02270v1)：CompleteDecember 2025 drone safety-surrogation work is simulated and is not new learned actuation.（核查 2026-10-01T10:17:12Z；读取方式 Direct official or author-controlled primary source; complete paper methods inspected）
  - [sayom.me / source 8](https://sayom.me/)：Current Utah PhD researcher independently identifies Garcia as advisor and the 2025 robotic safety project.（核查 2026-10-01T10:17:12Z；读取方式 Direct official or author-controlled primary source; complete paper methods inspected）

<a id="venkat-n-krovi"></a>

## Venkat N. Krovi · Clemson University

- 稳定键：`venkat-n-krovi`；[导师主页](https://sites.google.com/view/armlab-cuicar/home)
- 任职：Michelin SmartState Chair Professor of Vehicle Automation
- 方向：Multi-robot coordination；Deep reinforcement learning；Wheeled-biped payload transport；Vehicle automation
- 匹配理由：Current directed-group sim-to-real RL coordinates two physical wheel-legged robots for payload transport.
- 真机证据（Current Clemson-advised physical RL coordination verified; bounded indoor experiment）：The author-uploaded ICRA 2025 final paper, postedMay5, 2025, verifies a central PPO policy trained in Isaac Sim then transferred without hardware retraining to two real Diablo robots. OptiTrack provides robot/payload poses; a workstation publishes ego and relative-follower velocity commands through ROS at 50Hz. Indoor payload paths include changed loads and physical speed bumps. Legs primarily accommodate disturbances; internal robot control handles roll, while the learned policy coordinates transport. Active learned height control and longer rough terrain remain future. The physical workspace is limited to5m×2m and motor heating limits repeated tests. Lead author Mehta independently names Krovi his advisor, and the author code repository provides real-deployment implementation. Physical23; no outdoor deployment or whole-body torque policy inferred.
- 短访证据（unknown）：No explicit external-master short-visitor invitation or summer 2027 availability was established. The lab’s old SAE bootcamp is a12-week virtual training course, not an in-person research visit. Faculty role, conference leadership and equipment pages do not create a visitor offer.
- 首次发现：2026-10-01T10:16:14Z；最后核查：2026-10-01T10:17:12Z
- 当前总分：71/100；评分依据：
  - fit 38/40：Direct multi-robot deep-RL sim-to-real coordination, with bounded tasks.
  - physical 23/25：Complete recent physical experiment plus independent current adviser/project linkage; limited indoor scope.
  - shortVisit 0/20：No applicable external-master visitor invitation.
  - freshness 10/15：Explicit 2025 publication and lab activity; no unverified 2026 update used.
- 未确认事项：Reuse Clemson notes: outside-master academic/visa category requires individual review. Short-Term Scholar permits1day–6months with at least a bachelor’s, but visitor appointment details remain unresolved. Student Intern generally/typically undergraduate wording is not an absolute graduate prohibition; home-degree linkage and return are required. Current-linked forms have conflicting old dates; newer Intern form lists$1,800/month with family/friend support, but 2027 amounts, full personal-funding acceptance, fees and security review require confirmation. CU-ICAR is in Greenville; confirm research site, lab access and the exact project rather than assume main-campus hosting.；Public robot research does not confirm current equipment access, a summer 2027 offer or host availability.；[Institutional visitor rules](../eligibility_notes.md#clemson)
- 来源：
  - [www.clemson.edu / source 1](https://www.clemson.edu/cecas/departments/automotive-engineering/people/venkat-krovi.html)：Current official chaired faculty appointment and email.（核查 2026-10-01T10:17:12Z；读取方式 Direct official or author-controlled primary source; complete paper methods inspected）
  - [sites.google.com / source 2](https://sites.google.com/view/armlab-cuicar/home)：Current ARMLab director/Greenville site; historical12-week virtual bootcamp is not visitor intake.（核查 2026-10-01T10:17:12Z；读取方式 Direct official or author-controlled primary source; complete paper methods inspected）
  - [www.researchgate.net / source 3](https://www.researchgate.net/publication/384085603_Deep_Reinforcement_Learning_for_Coordinated_Payload_Transport_in_Biped-Wheeled_Robots)：Full author-uploaded ICRA 2025 final manuscript publicly readable; page also retains a 2024preprint. Complete real hardware methods and limitations inspected, not ResearchGate-generated summary.（核查 2026-10-01T10:17:12Z；读取方式 Direct official or author-controlled primary source; complete paper methods inspected）
  - [github.com / source 4](https://github.com/dhruvkm2402/Deep_Reinforcement_Learning_Multi_Robot_Payload_Transport)：Lead-author primary implementation independently documents simulation and actual Diablo/OptiTrack/ROS deployment.（核查 2026-10-01T10:17:12Z；读取方式 Direct official or author-controlled primary source; complete paper methods inspected）
  - [www.linkedin.com / source 5](https://www.linkedin.com/posts/dhruvkm_icra2025-ai-deeplearning-activity-7329323904643043328-m2xX)：Lead author explicitly identifies Krovi as advisor of this ICRA 2025 project; broad outdoor motivation is not used as deployment evidence.（核查 2026-10-01T10:17:12Z；读取方式 Direct official or author-controlled primary source; complete paper methods inspected）
  - [ieeexplore.ieee.org / source 6](https://ieeexplore.ieee.org/abstract/document/11127939/)：Official publisher listing independently confirms the ICRA paper; full-method basis is the author manuscript.（核查 2026-10-01T10:17:12Z；读取方式 Direct official or author-controlled primary source; complete paper methods inspected）

