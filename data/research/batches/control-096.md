# 检索批次 control-096

[返回完整排序](../ranked_candidates.md) · [本批完整 JSON](control-096.json) · [评分与字段](../README.md)

本批 **2 位**。首次发现时间保持不变；资料修正通过独立提交保留历史。分数是研究筛选优先级，不是接收概率。

<a id="tae-myung-huh"></a>

## Tae Myung Huh · University of California, Santa Cruz

- 稳定键：`tae-myung-huh`；[导师主页](https://tml.engineering.ucsc.edu/)
- 任职：Assistant Professor
- 方向：Learned grasp perception and haptic manipulation；Soft robotic sensing；Data-driven tactile sensing
- 匹配理由：Current manipulation PI with verified learned-vision-guided physical picking in an older Berkeley collaboration and current UCSC tactile-sensing research; current local learned-action evidence remains limited.
- 真机证据（Older collaborative learned-perception-to-action; current local hardware verified separately without new learned control）：The complete September 2023 Smart Suction Cup paper uses GQCNN learned grasp-quality proposals from depth data to seed actual UR10 bin picking; subsequent pressure-based haptic corrections are model-based. Nineteen adversarial objects and 1316 autonomous attempts establish execution. Huh is already UCSC-affiliated, but the apparatus belongs to the Berkeley collaboration, so UCSC access is not inferred. July 2026 PinFT independently demonstrates current UCSC Franka Research3 manipulation, but initial arm placement is manual and gripper width/motions are prescribed; polynomial sensor calibration and force monitoring do not establish a learned action policy. The 2025 Strain in Sound gradient-boosting study is sensor/strain estimation, not robot execution.
- 短访证据（unknown）：The lab join page distinguishes PhD, MS and postdoctoral intake; its MS item is a January 2023 lab-setup assistant role, not a current external-master invitation. UCSC has announced an outside-graduate eight-week summer 2027 ISRP, but Huh is not identified in the catalog inspected. Institution feasibility alone earns no lab short-visit points.
- 首次发现：2026-10-01T10:46:38Z；最后核查：2026-10-01T11:00:43Z
- 当前总分：68/100；评分依据：
  - fit 33/40：Substantive learned grasp perception and tactile regression, while principal haptic control remains classical.
  - physical 20/25：Verified older collaborative actual learned-perception-guided manipulation; newer local hardware is not upgraded to current learned control.
  - shortVisit 0/20：No explicit lab external visitor route; university program does not identify this PI.
  - freshness 15/15：Dated July 10, 2026 current-UCSC manipulation-sensor paper, explicitly separated from older learned execution.
- 未确认事项：Previously reviewed UCSC conditions apply. Outside-degree masters can use a degree-linked Student Intern process with home approval, continued enrollment, return to complete the degree and at least32h/week. Published 2027 ISRP timing is compatible, but its partner-university wording, competitive project selection and current catalog uncertainty require checking. Personal funds are permitted subject to documentation; current principal threshold is$2200/month and the program/living fees are additional planning considerations. Lab capacity, visitor hardware access, funding and remote arrangement are unknown.；Public robot research does not confirm current equipment access, a summer 2027 offer or host availability.；Timestamp scope: First precisely preserved source-observation time; earlier incidental lead time and source are unavailable and were not reconstructed.；[Institutional visitor rules](../eligibility_notes.md#uc-santa-cruz)；[Institutional visitor review](../eligibility_notes.md#uc-santa-cruz); sources retain the original policy-observation times.
- 来源：
  - [campusdirectory.ucsc.edu / source 1](https://campusdirectory.ucsc.edu/cd_detail?uid=thuh)：Current official assistant professor, regular-faculty status and public email.（核查 2026-10-01T11:00:35Z；读取方式 Direct primary/official source via web.run）
  - [tml.engineering.ucsc.edu / source 2](https://tml.engineering.ucsc.edu/joinus/)：Full lab recruitment page: degree intake and dated 2023 MS lab-setup task; no external-master short-visit offer.（核查 2026-10-01T10:48:55Z；读取方式 Public primary HTML downloaded and read locally）
  - [tml.engineering.ucsc.edu / source 3](https://tml.engineering.ucsc.edu/publication/)：Current lab publication list, including 2025 sensor-learning paper.（核查 2026-10-01T10:48:55Z；读取方式 Public primary HTML downloaded and read locally）
  - [arxiv.org / source 4](https://arxiv.org/html/2309.07360v1)：Full first 2023 paper verifies GQCNN-seeded real UR10 picking and classical haptic correction; collaboration provenance qualified.（核查 2026-10-01T11:00:35Z；读取方式 Direct primary/official source via web.run）
  - [arxiv.org / source 5](https://arxiv.org/html/2607.10000v1)：Complete July 10, 2026 current-UCSC PinFT paper: actual FR3 gripper sensing, manual positioning and scripted motions rather than learned feedback control.（核查 2026-10-01T11:00:43Z；读取方式 Direct primary/official source via web.run）
  - [arxiv.org / source 6](https://arxiv.org/html/2604.20017v1)：Full 2025 RoboSoft strain-sensing paper repostedApril 2026; gradient boosting is sensor estimation, with mannequin evaluation.（核查 2026-10-01T10:48:55Z；读取方式 Direct primary/official source via web.run）
  - [global.ucsc.edu / source 7](https://global.ucsc.edu/visiting-students/isrp/isrp-how-to-apply/)：Live 2027 eight-week institution program; no mentor-specific offer.（核查 2026-10-01T10:56:03Z；读取方式 Live cloud-browser visible page）
  - [ucsc-isrp.softr.app / source 8](https://ucsc-isrp.softr.app/)：Catalog checked and still shows 2025–26 projects; Huh participation not established.（核查 2026-10-01T10:57:00Z；读取方式 Live cloud-browser visible page）

<a id="shinjiro-sueda"></a>

## Shinjiro Sueda · Texas A&M University

- 稳定键：`shinjiro-sueda`；[导师主页](https://people.engr.tamu.edu/sueda/index.html)
- 任职：Associate Professor
- 方向：Physics-based robotic assembly；Reinforcement learning for contact-rich insertion；Differentiable and learned simulation
- 匹配理由：Current US faculty coauthor of verified RL-controlled physical dual-arm assembly, with a broader physics-based simulation and computational fabrication program.
- 真机证据（2025 collaborator-hardware physical RL; no verified Texas A&M local platform or visitor access）：The complete 2025 Fabrica paper combines assembly sequence/grasp/motion planning with PPO-trained residual part-pose actions passed to task-space impedance control on two real Franka Panda arms. Simulation training is in Isaac Gym; physical operation uses calibrated bases, predefined pickup/assembly regions and custom pickup fixtures. The headline80% is successful assembly steps, not whole-assembly completion. Manual interventions remain, and the core insertion policy relies on joint encoders rather than external force/vision feedback. The acknowledgment places Panda support in MIT’s Adelson lab; Sueda is a Texas A&M coauthor, without verified local TAMU apparatus or direct lead-student supervision. Physical credit is therefore collaborative.
- 短访证据（precedent-only）：Current faculty homepage lists enrolled students and a2018 PhD visitor, which is historical precedent only. No current external-master, eight-week, remote or funded-visitor invitation was verified. The 2026 learned-PDE paper confirms ongoing research activity but is not additional robot execution.
- 首次发现：2026-10-01T10:47:13Z；最后核查：2026-10-01T11:00:43Z
- 当前总分：69/100；评分依据：
  - fit 34/40：Concrete robot-assembly RL contribution within a primarily simulation/graphics program.
  - physical 20/25：Verified real dual-arm execution, but collaborative MIT apparatus with no current TAMU physical-group ownership evidence.
  - shortVisit 0/20：No current external short-visit invitation; historical PhD visitor is not a master offer.
  - freshness 15/15：Explicit June 2026 learned-simulation publication; physical assembly evidence remains 2025.
- 未确认事项：Previously reviewed Texas A&M conditions apply. Current Student Intern policy includes overseas undergraduate/master degree students for 3weeks–12months, degree relevance, at least32h/week and return to complete the degree. The current$2000/month proof threshold can use personal/family funds within12months, plus required insurance and documentation. A host department must sponsor the request, obtain HR/compliance approval and bear its$350 operational fee.2027 costs, host willingness, exact dates, lab access and any stipend remain unconfirmed.；Public robot research does not confirm current equipment access, a summer 2027 offer or host availability.；Timestamp scope: First precisely preserved source-observation time; earlier incidental lead time is unavailable and was not reconstructed.；[Institutional visitor rules](../eligibility_notes.md#texas-am)；[Institutional visitor review](../eligibility_notes.md#texas-am); sources retain the original policy-observation times.
- 来源：
  - [engineering.tamu.edu / source 1](https://engineering.tamu.edu/cse/profiles/sueda-shinjiro.html)：Current official associate-professor role and contact.（核查 2026-10-01T11:00:35Z；读取方式 Direct primary/official source via web.run）
  - [people.engr.tamu.edu / source 2](https://people.engr.tamu.edu/sueda/index.html)：Current group roster,2018 doctoral visitor and explicitly datedJune 2026 learned-multigrid research.（核查 2026-10-01T11:00:43Z；读取方式 Direct primary/official source via web.run）
  - [fabrica.csail.mit.edu / source 3](https://fabrica.csail.mit.edu/)：Primary project and coauthor attribution for CoRL 2025 robotic assembly.（核查 2026-10-01T11:00:43Z；读取方式 Direct primary/official source via web.run）
  - [fabrica.csail.mit.edu / source 4](https://fabrica.csail.mit.edu/static/pdf/paper.pdf)：Full primary paper and appendices verify physical PPO insertion, deployment limitations and MIT apparatus acknowledgment.（核查 2026-10-01T10:51:28Z；读取方式 Public primary PDF downloaded; complete pdftotext read locally）
  - [arxiv.org / source 5](https://arxiv.org/abs/2506.05168)：First 2025 paper record; publication timing does not imply a later new experiment.（核查 2026-10-01T10:51:28Z；读取方式 Direct primary/official source via web.run）

