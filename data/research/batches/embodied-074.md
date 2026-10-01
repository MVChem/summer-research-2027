# 检索批次 embodied-074

[返回完整排序](../ranked_candidates.md) · [本批完整 JSON](embodied-074.json) · [评分与字段](../README.md)

本批 **2 位**。首次发现时间保持不变；资料修正通过独立提交保留历史。分数是研究筛选优先级，不是接收概率。

<a id="laszlo-a-jeni"></a>

## László A. Jeni · Carnegie Mellon University

- 稳定键：`laszlo-a-jeni`；[导师主页](https://www.ri.cmu.edu/ri-faculty/laszlo-attila-jeni/)
- 任职：Associate Research Professor
- 方向：Geometrically supervised vision-language-action models；4D scene and human representations；Multimodal embodied perception；Robot world-dynamics learning
- 匹配理由：Current direct VLA-policy collaboration provides a strong embodied-method link beyond the group’s broader human sensing and graphics work. A tightly scoped geometry/representation or VLA evaluation project is plausible research alignment, without implying an open visitor slot.
- 真机证据（public-hardware-evidence）：Full Pri4R March 10, 2026 v2 §V-E and AppendixS.I deploy OpenVLA-OFT/π0.5 variants on an actual OMY-F3M 6-DoF arm, using a gripper and three RealSense views. Learned actions execute at 10Hz on obstacle crossing, bin placement, farthest-object selection and moving-target grasping. Privileged3D-track prediction is a training-only auxiliary objective, not extra inference sensing. CMU authors include current CUBE PhD Ananya Bal and former visitor Jungbin Cho, but the LG/CMU/multi-university paper does not establish CUBE hardware ownership or visitor access; physical20.
- 短访证据（unknown）：Full lab roster lists visitors/interns and local MS students. Jungbin Cho’s first-person timeline confirms a CMU visit August 2025–February 2026, after bachelor’s graduation and before a later PhD; it is not proof of an external-master’s eight-week visit. No current dedicated short-visit invitation was found. RISS mentoring concerns an undergraduate program, not external graduate visitors.
- 首次发现：2026-10-01T07:05:23Z；最后核查：2026-10-01T07:07:22Z
- 当前总分：72/100；评分依据：
  - fit 37/40：Direct current VLA world-dynamics training with broader3D/human sensing methods.
  - physical 20/25：Actual learned arm execution in a multi-institution collaboration; local hardware ownership unresolved.
  - shortVisit 0/20：Roster/historical visitor evidence only, no current suitable outside-master invitation.
  - freshness 15/15：FullMarch 2026 deployed-VLA paper and current home-department advising record.
- 未确认事项：Current RI directory says Associate Research Professor; Mechanical Engineering/Carnegie Bosch pages retain Assistant Research Professor. Use the home-department rank, retain the discrepancy, and do not conflate research rank with tenure-track status.；Summer 2027, eight-week dates, funding, remote work and CUBE apparatus access remain unknown; visitor evidence0.；Pri4R evaluates task-specific fine-tuning and a small four-task real setup; LIBERO/RoboCasa gains are simulation. Neither those gains nor selected100% cells mean universal physical success.；Current project page labels arXiv 2026; one author reports CoRL 2026 acceptance. Do not describe a newer physical experiment merely from the later venue announcement. Code/models remained coming soon on the inspected project page.；Reuse CMU Student Intern and Collaborating Visitor notes. The June 2026 form explicitly includes master’s students and personal funds at$3,253/month; host/OIE approval, degree link, dates and 2027 figures still require confirmation. RISS excludes master’s students.；Public robot research does not confirm current equipment access, a summer 2027 offer or host availability.；Timestamp scope: First precisely retained primary encounter in the 2026 CMU/Fujitsu physical-AI center announcement; full candidate screen followed.；[Institutional visitor rules](../eligibility_notes.md#cmu-student-intern)
- 来源：
  - [www.ri.cmu.edu / source 1](https://www.ri.cmu.edu/ri-faculty/laszlo-attila-jeni/)：Full current home-department Associate Research Professor, email, lab leadership and current PhD/MS advising.（核查 2026-10-01T07:07:22Z；读取方式 direct-primary-page）
  - [www.meche.engineering.cmu.edu / source 2](https://www.meche.engineering.cmu.edu/directory/bios/jeni-laszlo.html)：Full courtesy Mechanical Engineering profile retains Assistant Research Professor; rank discrepancy recorded.（核查 2026-10-01T07:07:22Z；读取方式 direct-primary-page）
  - [laszlojeni.com / source 3](https://laszlojeni.com/lab.html)：Full group roster and visitor/intern categories; not a current invitation or external-master eligibility proof.（核查 2026-10-01T07:07:22Z；读取方式 direct-primary-page）
  - [arxiv.org / source 4](https://arxiv.org/html/2603.01549v2)：FullMarch10, 2026 Pri4R revision, realOMY-F3M deployment and appendix setup/training; mixed international collaboration.（核查 2026-10-01T07:07:22Z；读取方式 direct-primary-page）
  - [jiiiisoo.github.io / source 5](https://jiiiisoo.github.io/Pri4R/)：Full author project confirms Jeni/CMU authorship and distinguishes real rollout sections from simulation; releases coming soon.（核查 2026-10-01T07:07:22Z；读取方式 direct-primary-page）
  - [whwjdqls.github.io / source 6](https://whwjdqls.github.io/)：Full coauthor timeline documents 2025–26 CMU visitor under Jeni and later 2026 Penn PhD; no master’s status or8-week duration inferred.（核查 2026-10-01T07:07:22Z；读取方式 direct-primary-page）
  - [riss.ri.cmu.edu / source 7](https://riss.ri.cmu.edu/mentors/)：FullRISS mentor listing does not establish participation every year or graduate-student eligibility.（核查 2026-10-01T07:07:22Z；读取方式 direct-primary-page）

<a id="ramesh-karri"></a>

## Ramesh Karri · New York University

- 稳定键：`ramesh-karri`；[导师主页](https://engineering.nyu.edu/faculty/ramesh-karri)
- 任职：Professor of ECE; Department Chair
- 方向：3D vision-language-action models；Language-conditioned robotic grasping；Object-interaction reasoning；Trustworthy AI and cyber-physical systems
- 匹配理由：An adjacent VLA collaborator with multiple recent manipulation/perception papers, within a primarily trustworthy-hardware and cybersecurity portfolio. Best treated as a collaborative research backup whose specific robotics supervision arrangement needs confirmation, rather than assuming leadership of CRRL.
- 真机证据（public-hardware-evidence）：Full 3D-CAVLA March 30, 2026 v2 §IV-D deploys learned policies on a real Franka arm using50 teleoperated demonstrations for each of10 tabletop tasks. Five train/test splits use seven training tasks and three held-out tasks, with 10 trials/task. TableV reports90% seen,60% similar and 38% unseen versus30.2% unseen baseline. The paper calls execution open-loop beyond RGB-D observations; CoT/ROI preparation occurs once before rollout. All authors areNYU-affiliated, but CRRL’s roster identifies Khorrami as PI; Karri’s separate hardware ownership/access is unverified. Physical20.
- 短访证据（unknown）：No current explicit external-master’s summer/short-visitor invitation was located in the inspected official faculty record and relevant lab pages. CRRL’s MS/UG route is expressly for current NYU students and directed to Khorrami, so it cannot be borrowed as a Karri external-visitor offer. Degree advising or department-chair status does not imply a vacancy.
- 首次发现：2026-10-01T07:06:08Z；最后核查：2026-10-01T07:09:08Z
- 当前总分：70/100；评分依据：
  - fit 35/40：Repeated direct VLA/grasping collaboration, but hardware security is the main declared faculty portfolio.
  - physical 20/25：Full actual learnedFranka execution through CRRL collaboration; separate Karri ownership/access unknown.
  - shortVisit 0/20：No current lab-specific external-master’s short visit verified.
  - freshness 15/15：March 2026 revised deployment paper andCVPR 2026 VLM project.
- 未确认事项：Main appointment is current Brooklyn Tandon professor/chair. His primary declared portfolio is hardware security/cybersecurity; verify that a robotics project can actually be supervised through him.；No Summer 2027 hosting, eight-week dates, funding, remote role or robotics equipment access established. Visitor evidence0.；3D-CAVLA originated May 2025 and was revisedMarch 2026.38% unseen is an absolute success rate; the paper’s25% gain is relative to30.2%, not25 percentage points. LIBERO98.1% is simulation.；BOP-ASK CVPR 2026 provides current object-interaction VLM data/methods, not an additional physical robot-policy trial. Do not infer apparatus ownership from coauthorship or news.；Reuse NYU external Research Affiliate policy: qualifying full-time faculty sponsorship, HR/safety review and educational-benefit conditions; visa category and fully personal funding remain specific unresolved questions. The policy’s three-month approval period is not a minimum visit duration.；Public robot research does not confirm current equipment access, a summer 2027 offer or host availability.；Timestamp scope: Earliest precisely retained primary encounter in Pri4R’s3D-CAVLA reference; dedicated Karri faculty screen began07:07:47Z. Earlier incidental un-timed coauthor exposure is not reconstructed.；[Institutional visitor rules](../eligibility_notes.md#nyu)
- 来源：
  - [engineering.nyu.edu / source 1](https://engineering.nyu.edu/faculty/ramesh-karri)：Full current NYU Tandon Professor/ECE Chair, professional email and hardware-security research focus.（核查 2026-10-01T07:09:08Z；读取方式 direct-primary-page）
  - [engineering.nyu.edu / source 2](https://engineering.nyu.edu/sites/default/files/2024-07/cv-ramesh-karri.pdf)：Full 2-page 2024 NSF biosketch confirms Brooklyn organization and professor title; not a current visitor offer.（核查 2026-10-01T07:09:08Z；读取方式 direct-primary-page）
  - [arxiv.org / source 3](https://arxiv.org/html/2505.05800v2)：FullMarch30, 2026 3D-CAVLA revision including§IV-D actual learnedFranka execution, exact protocols and limitations.（核查 2026-10-01T07:09:08Z；读取方式 direct-primary-page）
  - [3d-cavla.github.io / source 4](https://3d-cavla.github.io/)：Full author project corroborates NYU collaboration and real tabletop validation.（核查 2026-10-01T07:09:08Z；读取方式 direct-primary-page）
  - [bop-ask.github.io / source 5](https://bop-ask.github.io/)：FullCVPR 2026 object-interaction VLM project, Karri author; benchmark data rather than a new physical deployment.（核查 2026-10-01T07:09:08Z；读取方式 direct-primary-page）
  - [crrl-control-robotics-research-lab.github.io / source 6](https://crrl-control-robotics-research-lab.github.io/people.html)：FullCRRL roster identifies Khorrami as PI, Krishnamurthy as research staff and Bhat as student; no independent Karri apparatus claim.（核查 2026-10-01T07:09:08Z；读取方式 direct-primary-page）
  - [crrl-control-robotics-research-lab.github.io / source 7](https://crrl-control-robotics-research-lab.github.io/joining.html)：Fullcurrent intake MS/UG limited to current NYU students and directed to Khorrami; no borrowed visitor invitation.（核查 2026-10-01T07:09:08Z；读取方式 direct-primary-page）
  - [vineet2104.github.io / source 8](https://vineet2104.github.io/)：Full lead-author currentNYU PhD page confirms VLA/robotics research and 2026 papers; does not explicitly establish Karri co-advising.（核查 2026-10-01T07:09:08Z；读取方式 direct-primary-page）

