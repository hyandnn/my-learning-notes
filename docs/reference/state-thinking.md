---
description: 状态思维：如何拆解机器人估计问题的课程笔记。
---

# 状态思维：如何拆解机器人估计问题

> 这篇笔记的目标不是总结某一个算法，而是建立一种机器人问题分析方法：看到一个任务时，先问它的 **State / Observation / Prediction Model / Correction** 分别是什么。

---

## 1. 什么样的信息才能称为 State？

**State（状态）不是“所有重要信息”，而是所选模型中用于描述系统并预测演化的一组变量。**

更准确地说：

> **State = 在给定模型和输入下支持未来演化预测的变量集合。**

它有几个关键特征：

1. **与未来预测直接相关**  
   State 不是为了描述当前画面，而是为了支持下一时刻的预测。

2. **是任务相关的隐藏变量**  
   不同任务的 State 不同。SLAM 的 State 是位姿和地图；目标跟踪的 State 是目标位置、速度和存在概率；Ground Detection 的 State 可以是地面几何模型。

3. **应与模型和任务相匹配**  
   State 不应该包含所有可观测数据，而应该只保留决定未来演化所必需的信息。  
   例如，预测目标下一帧位置时，目标颜色通常不是必要 State；但位置和速度通常是必要的。

4. **通常带有不确定性**  
   机器人维护的不是一个确定 State，而是关于 State 的 Belief，例如均值 + 协方差、粒子集合、概率分布或优化图。

可以总结为：

```text
State = Predictive + Task-relevant；Belief 描述状态的不确定性
```

---

## 2. 为什么 Observation 往往不能直接作为 State？

**Observation（观测）是传感器对真实世界的测量结果，而 State 是机器人想要估计的隐藏变量。**

二者的区别在于：

```text
Reality → Sensor → Observation → Inference → Belief over State
```

Observation 通常不适合作为 State，原因包括：

1. **Observation 是原始或半原始数据，信息冗余且驳杂**  
   图像、点云、深度图、Mask 中包含大量与当前任务无关的信息。

2. **Observation 不一定具有预测能力**  
   一张图像可以告诉我们当前看到了什么，但它不一定能直接预测下一帧系统如何演化。

3. **Observation 可能不是稳定表示**  
   图像会受到光照、曝光、材质、遮挡影响；点云会受到噪声、反射率、深度质量影响；Mask 可能受到模型误检和漏检影响。

4. **Observation 通常需要 Observation Model 解释**  
   Observation Model 的作用是说明：

```text
如果真实 State 是 x，那么我应该观测到什么 z？
```

数学上常写作：

```text
p(z | x)
```

例如，在地面平面估计中，真实 State 可以是平面参数，而 Observation 是点云点。Observation Model 描述这些点应该如何落在平面附近。

---

## 3. 统一框架：State / Observation / Prediction Model / Correction

一个典型的贝叶斯状态估计问题可以写成：

```text
上一时刻 Belief
        ↓
Prediction Model
        ↓
当前先验 Belief
        ↓
Observation
        ↓
Correction / Update
        ↓
当前后验 Belief
```

其中：

| 概念 | 含义 |
|---|---|
| State | 待估计的隐藏变量 |
| Belief | 对 State 的概率性估计 |
| Prediction Model | 描述 State 如何随时间演化 |
| Observation | 传感器或算法产生的新证据 |
| Observation Model | 描述 State 如何生成 Observation |
| Correction | 用 Observation 修正先验 Belief |

---

## 4. 四类任务拆解

---

## 4.1 Ground Detection：地面几何状态估计

### State

Ground Detection 的 State 不应简单理解为 Ground Mask，而更适合理解为：

> **能够生成地面观测的潜在几何状态。**

在简单单平面假设下，State 可以是：

```text
x = [n_x, n_y, n_z, d]
```

其中地面平面满足：

```text
n_x X + n_y Y + n_z Z + d = 0
```

也可以写成：

```text
n^T P + d = 0
```

其中 `n` 是平面法向量，`d` 是平面偏移。

如果考虑时序变化，也可以扩展为：

```text
x = [n_x, n_y, n_z, d, dot_n_x, dot_n_y, dot_n_z, dot_d]
```

但在实际工程中，不一定需要显式加入导数项。更常见的是使用“平面缓变”或“相机运动补偿”作为预测模型。

### Prediction Model

Ground Detection 的预测模型可以来自：

1. **地面局部连续假设**  
   相邻帧中地面几何不会突然变化。

2. **相机/机器人运动补偿**  
   如果已知机器人位姿变化，可以将上一帧地面平面变换到当前相机坐标系下。

3. **地面模型缓变假设**  
   平面法向和高度在短时间内只发生小幅变化。

因此预测过程可以理解为：

```text
上一帧地面 Belief + 相机运动 / 平面连续性假设
→ 当前帧地面先验 Belief
```

### Observation

Observation 不是“真实地面”，而是当前帧能够约束地面 State 的测量信息，例如：

- 候选地面 3D 点；
- 深度图或双目视差；
- 点云局部法向；
- RANSAC 拟合出的临时平面；
- 语义分割中的 ground probability；
- 左右一致性、深度置信度、残差分布等质量指标。

### Observation Model

如果 State 是平面参数，Observation 是点云点 `P_i`，那么常见观测模型是点到平面残差：

```text
r_i = n^T P_i + d
```

理想地面点应满足：

```text
r_i ≈ 0
```

如果残差大，则可能是噪声、障碍物、非地面点，或者当前平面模型不准。

### Correction

Correction 的本质不是“直接更新平面”，而是：

> **用当前观测修正机器人对地面几何状态的 Belief。**

常见做法包括：

- 鲁棒最小二乘拟合平面；
- RANSAC 剔除离群点；
- 根据残差、点数、左右一致性调整观测权重；
- 当观测质量差时，降低更新幅度，更多保留历史先验；
- 当观测质量好时，更多相信当前观测。

最终输出可以包括：

- 后验平面参数；
- 地面 Mask；
- 地面置信度；
- 当前帧是否可信的质量评估。

---

## 4.2 SLAM：机器人位姿与地图的联合状态估计

### State

SLAM 的 State 通常不是单一当前位姿，而是：

> **机器人轨迹与环境地图的联合隐藏状态。**

可以写成：

```text
x = {T_wb_1, T_wb_2, ..., T_wb_t, m}
```

其中：

- `T_wb_t`：第 t 时刻机器人或相机在世界坐标系下的位姿；
- `m`：地图，可以是特征点、点云、栅格地图、平面、语义地图等。

对于视觉惯性 SLAM，还可能包含：

- IMU bias；
- 速度；
- 相机-IMU 外参；
- 单目尺度；
- 相机内参等。

### Prediction Model

SLAM 中的 Prediction Model 可以来自：

1. **轮速计 / 里程计运动模型**  
   根据轮速或控制输入预测位姿变化。

2. **IMU 预积分模型**  
   根据加速度和角速度预测姿态、速度、位置变化。

3. **匀速或匀加速假设**  
   在缺少其他输入时，用短时运动连续性预测下一帧位姿。

4. **静态地图假设**  
   地图中的大部分结构在短时间内保持不变。

### Observation

SLAM 的 Observation 可以是：

- 图像特征点；
- 光流；
- 语义观测；
- 深度图；
- LiDAR 点云；
- IMU 原始测量；
- 回环检测结果；
- GPS / UWB / AprilTag 等外部定位观测。

### Observation Model

不同 SLAM 系统有不同观测模型，例如：

1. **视觉重投影误差**

```text
r = z_image - projection(T, P_world)
```

2. **LiDAR 点到点 / 点到线 / 点到面误差**

```text
r = distance(transformed point, map feature)
```

3. **IMU 预积分残差**

```text
r = measured inertial motion - predicted inertial motion
```

### Correction

SLAM 的 Correction 通常分为：

1. **前端修正**  
   通过帧间匹配、scan matching、PnP、ICP 等方法修正当前位姿。

2. **后端优化**  
   通过 BA、pose graph optimization、factor graph optimization 同时修正历史轨迹和地图。

3. **回环修正**  
   当机器人识别出曾经到过的位置时，用回环约束修正累计漂移。

SLAM 的核心不是“当前定位”，而是：

> **在不确定观测下，同时维护机器人在哪里，以及世界长什么样。**

---

## 4.3 多目标跟踪：目标运动状态估计

### State

多目标跟踪中的 State 是每个目标的隐藏运动状态，而不是检测框本身。

对于 2D MOT，单个目标的 State 可以是：

```text
x = [u, v, w, h, dot_u, dot_v, dot_w, dot_h]
```

其中：

- `u, v`：目标框中心；
- `w, h`：目标框宽高；
- `dot_u, dot_v, dot_w, dot_h`：对应变化速度。

对于 3D MOT，State 可以是：

```text
x = [X, Y, Z, yaw, l, w, h, dot_X, dot_Y, dot_Z, dot_yaw]
```

还可以包含：

- 目标存在概率；
- 类别概率；
- 外观特征；
- 遮挡状态。

### Prediction Model

常见预测模型包括：

1. **Constant Velocity Model**  
   假设目标短时间内速度近似不变。

2. **Constant Acceleration Model**  
   适用于加速度变化明显的目标。

3. **相机运动补偿**  
   如果相机自身在运动，需要先扣除 ego-motion。

4. **外观短期一致性假设**  
   同一目标在短时间内外观不会突变。

### Observation

Observation 通常来自检测器或传感器：

- 2D bounding box；
- 3D bounding box；
- 类别置信度；
- ReID embedding；
- 点云聚类结果；
- 深度估计结果。

### Observation Model

Observation Model 描述目标 State 如何生成检测结果，例如：

```text
z = Hx + noise
```

在简单 2D 跟踪中，检测器只观测到位置和尺寸，不直接观测速度。因此：

```text
Observation = [u, v, w, h]
State = [u, v, w, h, dot_u, dot_v, dot_w, dot_h]
```

速度是隐藏状态，需要通过时序推断得到。

### Correction

多目标跟踪的 Correction 包括两层：

1. **数据关联**  
   判断当前检测属于哪个历史轨迹。常见方法包括 IoU matching、匈牙利匹配、ReID 匹配等。

2. **状态更新**  
   用匹配到的检测结果修正目标状态 Belief。  
   如果没有匹配观测，则降低目标存在置信度；如果新检测无法匹配已有轨迹，则初始化新目标。

多目标跟踪的难点不只是滤波，而是：

> **在观测有漏检、误检和遮挡时，维护多个目标身份与运动状态的 Belief。**

---

## 4.4 时序人体姿态估计：人体关节状态估计

### State

人体姿态估计的 State 不是图像中的热图，而是人体骨架的隐藏几何状态。

对于单人 2D 姿态，State 可以是：

```text
x = [p_1, p_2, ..., p_K, dot_p_1, dot_p_2, ..., dot_p_K]
```

其中：

```text
p_i = [u_i, v_i]
```

表示第 i 个关节的图像坐标。

对于 3D 姿态，State 可以是：

```text
p_i = [X_i, Y_i, Z_i]
```

还可以包含：

- 根节点位姿；
- 骨骼长度；
- 关节角；
- 关节角速度；
- 遮挡状态；
- 多人身份 ID。

### Prediction Model

人体姿态的预测模型来自人体运动先验：

1. **关节运动连续性**  
   相邻帧关节位置不会无物理原因地跳变。

2. **骨骼长度约束**  
   同一个人的骨骼长度在短时间内近似固定。

3. **关节角范围约束**  
   人体关节运动受到生理结构限制。

4. **根节点运动模型**  
   人体整体运动可以近似为匀速或平滑变化。

### Observation

Observation 通常来自视觉模型或传感器：

- 2D joint heatmap；
- 关节坐标回归结果；
- 关节置信度；
- 深度图中的人体点；
- IMU 动捕数据；
- 多视角 triangulation 结果。

### Observation Model

Observation Model 描述隐藏骨架状态如何生成观测。例如：

```text
真实关节位置 → 图像投影 → heatmap peak
```

低置信度、遮挡、运动模糊会增加观测不确定性。

### Correction

Correction 包括：

- 用当前帧关键点观测修正预测关节位置；
- 对低置信度关节降低更新权重；
- 用骨骼长度和关节角约束修正不合理姿态；
- 在遮挡时更多依赖历史 Belief 和运动预测；
- 多人场景中还需要进行人体身份关联。

时序人体姿态估计的核心是：

> **在视觉观测不稳定时，利用人体运动连续性和骨骼结构先验维护稳定的人体姿态 Belief。**

---

## 5. 横向对比表

| 任务               | State                    | Prediction Model     | Observation                          | Correction                      |
| ---------------- | ------------------------ | -------------------- | ------------------------------------ | ------------------------------- |
| Ground Detection | 地面平面参数、法向、偏移、地面几何 Belief | 平面缓变、相机运动补偿、地面连续性    | 点云、深度、视差、候选地面点、语义 ground probability | 点到平面残差、鲁棒拟合、置信度加权更新             |
| SLAM             | 机器人轨迹 + 地图 + IMU bias 等  | 里程计、IMU、匀速假设、静态地图假设  | 图像特征、LiDAR 点云、IMU、回环观测               | 前端匹配、BA、pose graph、factor graph |
| 多目标跟踪            | 目标位置、速度、尺寸、存在概率、身份       | 匀速/匀加速、相机运动补偿、外观短期一致 | 检测框、类别分数、ReID、3D box                 | 数据关联 + Kalman/粒子滤波 + track 管理   |
| 时序人体姿态估计         | 关节位置、速度、骨骼长度、根节点位姿       | 运动连续性、骨骼约束、关节角约束     | heatmap、关键点、深度、IMU                   | 关键点更新、骨骼约束优化、遮挡处理               |

---

## 6. 核心统一逻辑

这四类任务虽然表面差异很大，但本质上都可以写成同一个循环：

```text
历史 Belief
    ↓
Prediction Model
    ↓
当前先验 Belief
    ↓
Observation
    ↓
Correction
    ↓
当前后验 Belief
```

它们的区别主要来自三点：

1. **State 不同**  
   Ground Detection 的 State 是地面几何；SLAM 的 State 是位姿和地图；目标跟踪的 State 是目标运动；人体姿态估计的 State 是人体骨架。

2. **Prediction Model 不同**  
   地面依赖平面连续性；SLAM 依赖机器人运动模型；目标跟踪依赖目标运动模型；人体姿态依赖人体运动和骨骼结构。

3. **Observation Model 不同**  
   地面用点到平面残差；SLAM 用重投影误差或点云匹配残差；目标跟踪用检测框与外观特征；人体姿态用 heatmap、关键点和骨骼约束。

---

## 7. 关键修正点

相比初稿，需要注意几个概念边界：

1. **State 不等于 Observation**  
   Ground Mask、图像、点云、检测框、heatmap 更像 Observation，而不是 State。

2. **State 应该是隐藏变量，不是输出结果本身**  
   例如 Ground Detection 输出 Ground Mask，但真正可作为 State 的通常是地面几何参数或地面结构 Belief。

3. **Observation Model 很重要**  
   它连接 State 和 Observation，回答：如果 State 是真的，我应该看到什么？

4. **Prediction Model 不一定来自物理模型**  
   它可以来自物理、几何、时序假设，也可以来自神经网络或数据驱动模型。关键是它提供当前 State 的先验估计。

5. **Correction 修正的是 Belief，不只是修正数值**  
   机器人维护的是关于 State 的不确定估计，而不是单个确定答案。

---

## 8. 一句话总结

> **机器人算法不是由任务名称定义的，而是由 State 定义的。**

一旦 State 定义清楚，Prediction Model、Observation Model 和 Correction 机制就会自然浮现。SLAM、Ground Detection、目标跟踪和人体姿态估计看似不同，本质上都是在维护不同隐藏状态的 Belief。

## 修订说明

2026-10-04：状态不要求是最小变量集，也不必全部隐藏；区分状态变量与其 Belief。这里的“最小”是建模偏好，不是状态的必要定义。
