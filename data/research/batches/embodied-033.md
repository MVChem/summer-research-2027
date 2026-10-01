# 检索批次 embodied-033

[返回完整排序](../ranked_candidates.md) · [本批完整 JSON](embodied-033.json) · [评分与字段](../README.md)

本批 **1 位**。首次发现时间保持不变；资料修正通过独立提交保留历史。分数是研究筛选优先级，不是接收概率。

<a id="karthik-desingh"></a>

## Karthik Desingh · University of Minnesota, Twin Cities

- 稳定键：`karthik-desingh`；[导师主页](https://karthikdesingh.com/)
- 任职：Assistant Professor
- 方向：World models for VLA deployment；Visual-force manipulation；Imitation learning；Object-centric navigation；Robot perception
- 匹配理由：The current RPM Lab combines directly relevant physical policy learning with learned perception. July 2026 DreamSteer ranks imagined action outcomes to improve a frozen pi0 policy without deployment-time finetuning; a separate 2026 study learns object-relative positioning on Spot.
- 真机证据（public-hardware-evidence）：DreamSteer tests a real Franka Panda with Robotiq gripper and RealSense L515 cameras, with 20 trials per task. It is a Meta collaboration, and its specific hardware ownership is not established. Separately, the current RPM/Minnesota team deploys a learned RGB-only category-level navigation policy on an actual Boston Dynamics Spot; the paper explicitly acknowledges Minnesota experimental facilities. AugInsert (August 2025 revision) also validates visual-force policies on dual UR5e arms.
- 短访证据（unknown）：The inspected vacancies page describes research for already enrolled University of Minnesota master’s and undergraduate students. Its summer-capacity warning refers specifically to summer 2025. No external-master’s short visit or summer 2027 invitation is established, so no visit points are awarded.
- 首次发现：2026-10-01T01:18:38Z；最后核查：2026-10-01T01:21:16Z
- 当前总分：80/100；评分依据：
  - fit 40/40：Direct match to VLA world models, manipulation policy robustness and visual imitation.
  - physical 25/25：Detailed current-group real Spot deployment plus manipulation experiments; Meta collaborative hardware is distinguished from established campus evidence.
  - shortVisit 0/20：No current external short-visit invitation found; local degree-student intake and old capacity statements receive no credit.
  - freshness 15/15：Specific July 2026 VLA study and February 2026 physical-navigation revision.
- 未确认事项：DreamSteer requires approximately 13 seconds per steering decision in the reported implementation; it should not be called real-time seamless control. Its instruction-following metric is contact with or attempted grasp of the correct object, not complete pick-and-place success.；The Spot policy uses RGB during learned execution; AprilTags and built-in localization supply demonstration and evaluation ground truth. Its numeric translation threshold is 0.3 meters, not centimeter-level accuracy.；AugInsert’s robot policy acts in two alignment dimensions; a compliant arm completes insertion after alignment. Its extensive augmentation studies are mainly simulation, with smaller real-robot validation.；The published local-student research terms and historical summer 2025 capacity statement neither prove an external route nor prohibit summer 2027 visitors.；Summer 2027 acceptance, mentor capacity, exact dates, funding, visitor appointment, and applicable university/immigration approvals remain unconfirmed. Self-funding alone does not establish eligibility.；Public robot research does not confirm current equipment access, a summer 2027 offer or host availability.
- 来源：
  - [cse.umn.edu / source 1](https://cse.umn.edu/cs/karthik-desingh)：Current official Assistant Professor and robot perception/manipulation research profile.（核查 2026-10-01T01:21:16Z；读取方式 direct-primary-page）
  - [karthikdesingh.com / source 2](https://karthikdesingh.com/)：Primary current affiliation and public obfuscated email kdesingh(At)umn(dot)edu.（核查 2026-10-01T01:21:16Z；读取方式 direct-primary-page）
  - [rpm-lab.github.io / source 3](https://rpm-lab.github.io/publications/)：Current lab lists DreamSteer, 2026 last-meter navigation, and AugInsert.（核查 2026-10-01T01:21:16Z；读取方式 direct-primary-page）
  - [rpm-lab.github.io / source 4](https://rpm-lab.github.io/vacancies)：Direct intake page restricts listed master’s/undergraduate research to current UMN students; summer-capacity warning is dated 2025.（核查 2026-10-01T01:21:16Z；读取方式 direct-primary-page）
  - [arxiv.org / source 5](https://arxiv.org/html/2607.02865v1)：July 3, 2026 DreamSteer primary paper: real Panda protocol, frozen VLA steering, latency and instruction-following definition.（核查 2026-10-01T01:21:16Z；读取方式 direct-primary-page）
  - [arxiv.org / source 6](https://arxiv.org/html/2512.11173v2)：February 15, 2026 revision: actual Spot policy rollouts, separate RGB inference and AprilTag ground truth, Minnesota facility acknowledgement.（核查 2026-10-01T01:21:16Z；读取方式 direct-primary-page）
  - [rpm-lab-umn.github.io / source 7](https://rpm-lab-umn.github.io/category-level-last-meter-nav/)：Current group author project and physical Spot navigation demonstrations.（核查 2026-10-01T01:21:16Z；读取方式 direct-primary-page）
  - [arxiv.org / source 8](https://arxiv.org/pdf/2410.14968)：August 1, 2025 AugInsert revision: dual UR5e setup and bounded real-world visual-force policy experiments.（核查 2026-10-01T01:21:16Z；读取方式 direct-primary-page）

