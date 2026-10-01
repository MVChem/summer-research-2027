# 检索批次 embodied-035

[返回完整排序](../ranked_candidates.md) · [本批完整 JSON](embodied-035.json) · [评分与字段](../README.md)

本批 **1 位**。首次发现时间保持不变；资料修正通过独立提交保留历史。分数是研究筛选优先级，不是接收概率。

<a id="wenshan-wang"></a>

## Wenshan Wang · Carnegie Mellon University

- 稳定键：`wenshan-wang`；[导师主页](https://www.ri.cmu.edu/ri-faculty/wenshan-wang/)
- 任职：Research faculty / Systems Scientist
- 方向：Vision-language navigation；Learned visual navigation；Foundation-model perception；Self-supervised off-road autonomy；Robot learning
- 匹配理由：IntentNav (June 2026) learns spatially grounded waypoint decisions from human navigation demonstrations and transfers the VLM policy to real robot platforms. Wang also works on semantic scene memory and off-road self-supervised autonomy, giving a strong physical foundation-model systems match.
- 真机证据（public-hardware-evidence）：IntentNav deploys the same learned checkpoint on a wheeled robot, Unitree Go2 and Unitree G1 across ten real scenes and eight object categories. LiDAR, SLAM, camera observations and a laptop VLM feed robot-specific local control. Separately, CMU’s April 2025 TartanDriver report directly identifies Wang and his AirLab team testing a self-supervised, foundation-model-informed autonomy stack on an actual ATV. The current RI profile lists his named current advisees; the campus hardware is shared rather than asserted to be personally owned.
- 短访证据（unknown）：AirLab’s current openings page covers central graduate admissions, current CMU students, and staff/postdocs. It does not establish an external-master’s short research visit. Prior interns and affiliates are not evidence of summer 2027 capacity. Opportunity score is zero.
- 首次发现：2026-10-01T01:23:36Z；最后核查：2026-10-01T01:26:27Z
- 当前总分：78/100；评分依据：
  - fit 38/40：Strong deployed VLM and learned navigation, with less manipulation emphasis.
  - physical 25/25：Current CMU group deployment plus official campus ATV attribution; hardware is shared and not personally owned.
  - shortVisit 0/20：No verified faculty-level external short-visit invitation.
  - freshness 15/15：Explicit June and August 2026 primary research.
- 未确认事项：Official Robotics Institute faculty-category profile and named advisees establish university faculty scope. Exact Systems Scientist rank is preserved; independent visitor-host authority remains unverified.；Systems Scientist is the current official role; do not invent an Assistant Professor title. The external personal website could not be retrieved in this pass, so the official RI profile is the verified homepage/contact source.；IntentNav’s physical examples and latency tests are separate from its large simulation benchmark success rates. No overall physical success percentage is claimed here. Its main text gives an approximate 0.8-second policy query, while the detailed 20-episode appendix reports about 1.28-second VLM inference and 1.40-second full decision cycles; avoid an unqualified fixed latency.；The learned high-level policy remains unchanged across embodiments, while sensing and low-level control are platform-specific. This is not evidence of a newly learned low-level humanoid locomotion controller.；The existing CMU institutional Student Intern supplement may provide an administrative route, subject to host approval and current requirements; it does not add faculty opportunity credit.；Summer 2027 acceptance, mentor capacity, exact dates, funding, visitor appointment, and applicable university/immigration approvals remain unconfirmed. Self-funding alone does not establish eligibility.；Public robot research does not confirm current equipment access, a summer 2027 offer or host availability.
- 来源：
  - [www.ri.cmu.edu / source 1](https://www.ri.cmu.edu/ri-faculty/wenshan-wang/)：Direct official Systems Scientist appointment, AirLab affiliation, named current advisees and public professional email.（核查 2026-10-01T01:26:27Z；读取方式 direct-primary-page）
  - [theairlab.org / source 2](https://theairlab.org/openings/)：Direct current recruitment categories; no explicit external-master’s summer visitor invitation.（核查 2026-10-01T01:26:27Z；读取方式 direct-primary-page）
  - [arxiv.org / source 3](https://arxiv.org/html/2606.08029v1)：June 2026 IntentNav primary paper: real cross-embodiment deployment, distinct simulation outcomes, sensing and appendix latency protocol.（核查 2026-10-01T01:26:27Z；读取方式 direct-primary-page）
  - [arxiv.org / source 4](https://arxiv.org/html/2608.22896v1)：August 2026 SuperMap collaboration provides related spatio-temporal semantic scene memory research.（核查 2026-10-01T01:26:27Z；读取方式 direct-primary-page）
  - [www.ri.cmu.edu / source 5](https://www.ri.cmu.edu/taking-autonomous-driving-off-road/)：April 22, 2025 official report explicitly identifies Wang in the AirLab TartanDriver team and reports autonomous physical ATV trials.（核查 2026-10-01T01:26:27Z；读取方式 direct-primary-page）
  - [arxiv.org / source 6](https://arxiv.org/html/2603.06914v1)：March 2026 SysNav is an additional current physical VLM navigation collaboration, distinct from ownership of every robot.（核查 2026-10-01T01:26:27Z；读取方式 direct-primary-page）

