---
description: 机器人感知与状态估计中常用概念的中英文对照和阅读入口。
icon: spell-check
---

# 术语表

这里提供查阅入口。完整解释与推理保留在对应章节中。

| 术语 | 中文与含义 | 阅读入口 |
| --- | --- | --- |
| Perception | 感知：从传感器数据提取与任务相关的信息 | [机器人系统](../slam/foundations/robot-systems.md) |
| Localization | 定位：估计机器人相对于参考系的位置与姿态 | [定位漂移](../slam/foundations/odometry-and-drift.md) |
| Mapping | 建图：估计环境的空间结构或其他表示 | [机器人系统](../slam/foundations/robot-systems.md) |
| Odometry | 里程计：累计估计相邻时刻之间的运动 | [里程计与漂移](../slam/foundations/odometry-and-drift.md) |
| State | 状态：在所选模型中描述系统，并支撑预测的变量 | [状态与时间](../slam/foundations/state-and-time.md) |
| Observation | 观测：由传感器或处理过程得到的状态相关证据 | [观测与 Belief](../slam/foundations/observation-and-belief.md) |
| Belief | 对状态的概率描述，例如分布、参数化分布或样本 | [用分布表达位置](../slam/foundations/belief-over-pose.md) |
| Prior | 先验：使用当前证据更新之前的概率描述 | [贝叶斯直觉](../slam/foundations/bayesian-thinking.md) |
| Likelihood | 似然：给定状态时，对当前观测出现的可能性进行建模 | [贝叶斯例题](bayes-worked-example.md) |
| Posterior | 后验：结合先验与当前证据之后的概率描述 | [贝叶斯例题](bayes-worked-example.md) |
| Prediction | 预测：根据系统模型与已有估计，推到下一时刻 | [预测与校正](../slam/foundations/prediction-and-correction.md) |
| Correction | 校正：使用新观测更新预测得到的估计 | [预测与校正](../slam/foundations/prediction-and-correction.md) |
| Uncertainty | 不确定性：对可能取值范围或分布的描述，不等同于已知误差 | [Kalman Gain 直觉](../slam/foundations/kalman-gain-intuition.md) |
| Kalman Gain | 卡尔曼增益：在相应模型与噪声假设下决定观测残差怎样修正状态 | [Kalman Gain 直觉](../slam/foundations/kalman-gain-intuition.md) |
| Markov assumption | Markov 假设：给定当前状态后，转移不再直接依赖更早历史 | [状态与时间](../slam/foundations/state-and-time.md) |
| SLAM | 同时定位与建图：联合估计轨迹与环境表示 | [相关章节](../slam/mapping/slam-formulation.md) |
| EKF-SLAM | 用联合 Gaussian 与协方差表示机器人和地标的状态相关性 | [相关章节](../slam/mapping/ekf-slam.md) |
| Gauge Freedom | 相对观测不改变的全局坐标／尺度自由度 | [相关章节](../slam/mapping/gauge-freedom.md) |
| Keyframe | 关键帧：保留有效约束并控制计算规模的状态选择 | [相关章节](../slam/mapping/keyframes-local-mapping.md) |
| Bundle Adjustment | 光束法平差：联合优化相机与三维地标的重投影残差 | [相关章节](../slam/mapping/bundle-adjustment.md) |
| Schur Complement | Schur 补：消去部分增量，将其影响保留在缩减系统中 | [相关章节](../slam/mapping/bundle-adjustment.md) |
| Factor Graph | 因子图：用变量与局部因子表示函数或概率分解 | [相关章节](../slam/mapping/factor-graphs.md) |
| Marginalization | 边缘化：消去变量并将历史信息压缩到保留变量 | [相关章节](../slam/mapping/factor-graphs.md) |
| Pose Graph | 位姿图：以位姿为节点、以位姿约束为主要边的图 | [相关章节](../slam/mapping/pose-graph.md) |
| Loop Closure | 回环：验证历史重访并加入跨时间几何约束 | [相关章节](../slam/mapping/loop-closure.md) |
| IMU Preintegration | IMU 预积分：把关键状态之间高频惯性观测压成相对运动约束 | [相关章节](../slam/mapping/visual-lidar-inertial.md) |

## 两组容易混淆的关系

**状态与 Belief**：状态是待估计的对象；Belief 描述我们对该对象的认识。均值、协方差属于估计表示，不一定是物理状态本身。

**似然与后验**：给定状态时观测可能怎样出现，与获得观测后状态可能是什么，是两个不同的条件概率方向。见[完整计算例题](bayes-worked-example.md)。
