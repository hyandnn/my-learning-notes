---
title: 现代 SLAM 流程与系统设计
description: 如何把状态估计模块组织成可持续运行的实时机器人系统？
icon: book-open
course: Robot Perception & SLAM
part: Part IV Mapping and SLAM
week: 4
chapter: 48
chapter_type: lecture
status: organized
tags: [slam, mapping, state-estimation]
---

# 现代 SLAM 流程与系统设计

## 本章目标

如何把状态估计模块组织成可持续运行的实时机器人系统？

## 前置知识

[关键帧与局部建图](keyframes-local-mapping.md)、[回环](loop-closure.md)、[视觉／激光惯性状态估计](visual-lidar-inertial.md)。

## 定义与假设

正文以关键帧、多线程、多频率 SLAM 为例。不同系统可以采用 Filtering、Smoothing 或混合架构；模块执行频率、内存预算与地图表示应服从任务需求。

## 核心问题


前面 Chapter 37–47，我们其实一直在拆零件：

State, Observation, Feature, Keyframe, BA, Factor Graph, Pose Graph, Loop, IMU... 这一章不再增加一个新的算法，而是把所有东西重新装成一台真正可以跑起来的机器人系统。

这一章最核心的问题是：

一个现代 SLAM 系统，为什么必须被设计成多个时间尺度、多个模块共同工作的系统？

## 多时间尺度与模块职责

### 1. 先看最终大图

一套比较完整的 SLAM 系统，可以抽象成：

```
Sensors
   ↓
Preprocessing / Synchronization
   ↓
High-frequency State Propagation
   ↓
Front-end Tracking / Data Association
   ↓
Current Pose Estimate
   ↓
Keyframe Decision
   ↓
Local Mapping
   ↓
Local Optimization
   ↓
Loop / Relocalization
   ↓
Global Optimization
   ↓
Persistent Map
```

如果是 Visual-Inertial：

```
 Camera ──────────────┐
                      ↓
                 Visual Front-end
                      ↓
IMU → Propagation → Current State
                      ↓
                 Keyframe
                      ↓
          Sliding Window / Local BA
                      ↓
                Loop Closure
                      ↓
             Global Optimization
```

这个图先放在脑子里。 后面我们逐层解释为什么系统必然会长成这样。

### 2. 为什么不能只有一个“大优化器”？

最理想主义的设计可能是：

> 所有 Camera、IMU、LiDAR 数据全部保存。

然后每来一个 measurement：

重新优化从机器人出生到现在的全部 State 理论上很漂亮。 工程上完全不可行。

机器人运行时间：

$$
t\uparrow
$$

State 数量不断增加：

$$
N\uparrow
$$

Measurement 数量也不断增加。

如果每次都 Full Smoothing：

$$
Cost\uparrow\uparrow
$$

最终系统根本无法实时运行。

所以 SLAM 面临一个根本矛盾：

想利用长期历史

但同时：

必须实时响应当前运动

这直接催生了：

Multi-timescale Architecture

### 3. 第一个时间尺度：Sensor Rate

不同 sensor 本来就不是一个频率。

比如：

IMU：

$$
200\sim1000Hz
$$

Camera：

$$
20\sim60Hz
$$

LiDAR：

$$
10\sim20Hz
$$

GPS：

$$
1\sim10Hz
$$

Loop Closure：

> 甚至几秒、几十秒才发生一次。

所以你根本不可能把所有模块设计成：

$$
30Hz
$$

统一执行。

这也是为什么机器人状态估计天然是一个：

Multi-rate System

### 4. 高频层：Propagation

以 VIO 为例。

IMU 每：

$$
5ms
$$

来一个 measurement。 你不可能等下一张 Camera Image 才知道机器人动了。

所以利用 IMU：

$$
X_t \xrightarrow{IMU} X_{t+\Delta t}^{pred}
$$

不断传播：

$$
Pose
$$

Velocity Orientation 这是最快的一层。

它负责：

Short-term responsiveness

### 5. 为什么高频 Propagation 不追求长期准确？

因为 IMU 会漂。

所以这一层的目标不是：

> “给我一个永远正确的世界坐标。”

而是：

>  **从上一份可靠状态出发，在短时间内快速预测现在大概在哪。**

因此：

Propagation

更关注：

- 低延迟
- 高频
- 连续

而不是长期 global consistency。

### 6. 第二层：Tracking / Odometry

Camera / LiDAR measurement 到来后：

> 根据外部环境重新约束 Motion。

视觉：

$$
Image_t
$$

通过：

- feature
- optical flow
- map projection
- PnP

估计：

$$
T_t
$$

LiDAR：

通过：

- scan matching
- point-to-plane
- map registration

修正：

$$
T_t
$$

这一层负责：

Local Motion Estimation

### 7. 为什么 Tracking 必须优先？

因为如果 Tracking 挂了：

Current Pose 就不知道了。

那后续：

- Mapping
- Planning
- Control
- Obstacle Avoidance

全部都会受到影响。

所以在实时机器人里，经常有一个工程原则：

Tracking has higher priority than map refinement

比如 Local BA 算不完：

> 可以先中断。

但 Camera 新帧来了：

> Tracking 得继续。

### 8. Tracking 本质上在回答什么？

一句话：

Where am I now?

而且重点是：

$$
now
$$

所以它通常使用：

- Motion Prior
- Local Map
- Recent Keyframes

不会每帧查询整个世界。 这是一个局部实时问题。

### 9. 第三层：Keyframe Management

不是所有 Tracking Frame 都值得永久保存。

于是系统判断：

Should this frame become a Keyframe?

判断依据可能包括：

- motion
- overlap
- parallax
- tracking quality
- information gain
- mapping demand

然后把连续高频 trajectory：

$$
F_1,F_2,F_3,\dots
$$

压缩成：

$$
KF_1,KF_2,KF_3,\dots
$$

### 10. Keyframe 是连接“实时”和“地图”的桥

普通 Frame：

> 更多是暂时性的。

Keyframe：

> 进入长期状态表示。

所以可以把系统分成：

Ephemeral State

和：

Persistent State 普通 Tracking Frame 更接近前者。 Keyframe / MapPoint 更接近后者。

### 11. 第四层：Local Mapping

Keyframe 来了以后：

Insert KF

↓

寻找 Covisible Keyframes

↓

创建 / 更新 Landmarks

↓

Cull Bad Points

↓

Local BA / Sliding Window Optimization

↓

Cull Redundant Keyframes

这层解决：

How should my local map look?

### 12. Tracking 与 Local Mapping 的区别

Tracking：

current state

Local Mapping：

local persistent structure 前者强调实时。 后者强调局部一致性。

例如 Tracking 可能认为：

$$
T_t=T^{track}
$$

随后 Local BA 又改成：

$$
T_t=T^{optimized}
$$

这是完全正常的。

### 13. 所以 State 不是“一算出来就永久固定”

这是 SLAM 和很多 Frame-wise Perception 很不同的一点。

Object Detection：

$$
Image_t \rightarrow BBox_t
$$

输出完基本就结束。

SLAM：

$$
Image_t \rightarrow State_t
$$

但是未来：

$$
Measurement_{t+100}
$$

可能反过来修改：

$$
State_t
$$

所以：

SLAM State is revisable 这就是 Smoothing 思想。

### 14. 第五层：Loop Closure

Tracking 和 Local Mapping 都偏局部。

它们无法彻底解决：

Long-term Drift

所以系统还需要一个更慢、更全局的线程：

Loop Closure

它问：

> “当前地点是不是和很久以前某个地方相同？”

这是：

Long-term Data Association

### 15. Loop 不需要每帧都跑得非常重

因为闭环不是每帧发生。

所以可以：

- Keyframe-level 执行
- 低频执行
- 后台检索历史地图

它对 latency 的要求没有 Tracking 那么严格。

但是：

正确性要求非常高 因为错误 loop 破坏全局地图。

### 16. 于是出现一个很有意思的系统设计

不同模块有不同优先级：

|模块|典型尺度|核心目标|
|---|---|---|
|IMU Propagation|毫秒|低延迟|
|Tracking|帧级|当前 Pose|
|Local Mapping|局部 Keyframes|局部精度|
|Loop Closure|长时间|长期关联|
|Global Optimization|全局|全局一致性|

所以：

不同时间尺度承担不同责任 这是现代 SLAM 系统设计最核心的思想之一。

### 17. 为什么不能让 Loop Closure 负责 Tracking？

因为 Loop Closure：

- 搜索空间大
- 计算重
- 低频
- 要非常保守

拿它做每帧实时定位完全不合适。

### 18. 为什么也不能只做 Tracking？

因为：

$$
x_t\rightarrow x_{t+1}
$$

这种局部关系一定会积累 drift。

所以只有 Tracking：

$$
\boxed{ VO / Odometry }
$$

而不是完整意义上的长期 SLAM。

### 19. 为什么不能只做 Local BA？

Local BA 可以：

> 把最近这一小块地图做得很好。

但如果：

$$
500m
$$

以前积累了误差， 当前局部 BA 通常不会主动修正。

所以还需要：

Global Constraint

和：

Global Optimization

## 局部精度、全局一致与前后端

### 20. 局部准确与全局一致是两个不同目标

这是非常重要的工程认知。

#### Local Accuracy

短距离：

$$
T_t^{-1}T_{t+1}
$$

很精确。

#### Global Consistency

长时间：

$$
T_0^{-1}T_{10000}
$$

仍然合理。

一个系统可以：

> Local 很准，但 Global 漂得很远。

这正是很多 Odometry 系统。

### 21. 所以现代 SLAM 是 Hierarchical 的

大致可以看成：

#### Level 1

Sensor integration Raw measurements

#### Level 2

Tracking / Odometry Local motion

#### Level 3

Local Mapping Local geometry

#### Level 4

Loop / Pose Graph Global consistency

这是一个非常典型的：

Hierarchical Estimation System

### 22. Front-end 和 Back-end 到底怎么划分？

我们现在可以给一个比 Chapter 37 更成熟的定义。

#### Front-end

主要负责：

从原始 Sensor Data 中产生可靠 Measurement Constraints

例如：

- Feature Extraction
- Optical Flow
- Stereo Matching
- ICP Correspondence
- Data Association
- PnP
- Scan Matching
- Place Retrieval

#### Back-end

主要负责：

根据这些 Constraints 统一估计 State

例如：

- BA
- Sliding Window
- Factor Graph Optimization
- Pose Graph Optimization

### 23. 但是边界不是绝对的

比如 PnP 里也有 optimization。 ICP 也可以迭代优化。

所以不要机械认为：

> 有 Optimization 就是 Backend。

更准确的区别是：

Front-end 更偏：

Measurement formation

Backend 更偏：

Joint state consistency

### 24. Modern Front-end 越来越“学习化”

传统：

ORB, SIFT, Optical Flow, ICP

现代方法越来越多：

- learned features
- learned matching
- learned depth
- learned optical flow
- neural place recognition
- learned stereo

甚至直接学习：

$$
Image\ Pair\rightarrow Correspondence / Motion
$$

### 25. 那是不是 Geometry 快没用了？

不是。 这点非常重要。

即使 neural network 提供：

$$
Depth
$$

或者：

Feature Match

系统仍然需要知道：

> 这些东西怎样约束 Pose？

最终仍然经常进入：

$$
SE(3)
$$

Projection

$$
Factor
$$

Residual Optimization

所以：

Learning can improve measurement, Geometry organizes the state 这是目前理解现代机器人感知很有用的视角。

### 26. Learned Stereo 在这个体系中是什么角色？

以你熟悉的 Stereo 为例：

$$
I_L,I_R \rightarrow Disparity
$$

这实际上是：

Dense geometric measurement generation

它给后续模块提供：

$$
Depth
$$

但机器人还要继续解决：

- Temporal Tracking
- Motion
- Map Consistency
- State Fusion

所以 Stereo Model 并不等于 SLAM。

它是：

$$
\boxed{ SLAM / Perception 系统里的一个 Measurement Module }
$$

### 27. Object Detection 在 SLAM 里又是什么角色？

传统 SLAM 不一定需要 OD。

但 Semantic SLAM 里：

Object Detection

可以提供：

- dynamic object rejection
- semantic landmarks
- object-level association
- map semantics

例如：

chair, door, car 都可以进入更高级 map。

但 geometry 仍然需要解决：

> 它在哪里？

而不是只有：

> 它是什么？

### 28. Geometry 与 Semantics 是两个不同问题

Geometry：

Where?

Semantics：

What?

机器人真正的 world model 往往希望同时知道：

What is where? 这也是现代 Spatial Intelligence / Semantic Mapping 的重要方向。

## 地图表示与导航接口

### 29. Map 到底应该存什么？

没有唯一答案。

最简单 Sparse SLAM：

$$
\boxed{ Keyframes + Sparse\ Landmarks }
$$

Dense Mapping：

$$
Point\ Cloud / TSDF / Voxel
$$

Semantic Map：

$$
Object / Region / Category
$$

Navigation Map：

$$
Occupancy / Traversability
$$

所以：

Map representation depends on downstream task

### 30. 一个定位系统不一定需要漂亮地图

如果目标只是：

Robot Localization

可能只需要：

- sparse keypoints
- compact descriptors
- pose graph

不需要 dense reconstruction。

### 31. 一个规划系统则可能需要另一张 Map

Planner 关心：

Obstacle Free Space Traversability 那么 SLAM sparse landmarks 并不直接够用。

系统可能还有：

Occupancy Grid

或者：

Voxel Map

所以现实机器人经常有：

Multiple Map Representations

### 32. “一张地图解决所有问题”通常不是最优设计

例如：

定位 map：

> 强调稳定 landmark。

避障 map：

> 强调最新的局部 obstacle。

语义 map：

> 强调 object identity。

长期导航 map：

> 强调拓扑和可通行结构。

它们需要的信息不同。

所以成熟系统会把：

Localization Map

和：

Planning Map 在一定程度上分开。

### 33. Local Map 和 Global Map 也有不同职责

Local Map：

High detail, frequently updated

Global Map：

Long-term structure, lower-frequency correction

这和计算机系统：

Cache  ↔  Storage 有点像。

### 34. 为什么机器人需要 Local World Model？

避障 / 控制关心的通常是：

$$
1\sim10m
$$

附近。

没必要每次查询：

整个城市地图

所以真正的机器人 pipeline 往往还有一个非常活跃的：

Local World Model 负责即时决策。

### 35. SLAM 和 Navigation 的接口是什么？

SLAM 通常输出：

$$
Pose
$$

和：

$$
Map
$$

Navigation 使用这些东西：

```
SLAM
 ↓
Localization + Map
 ↓
Planning
 ↓
Trajectory
 ↓
Control
 ↓
Actuator
```

但现实中这个箭头不是完全单向。

### 36. Planning 也可能反过来帮助 Perception

比如前面讲过：

Observability 取决于运动。

如果机器人可以主动选择：

> 往左移动一点，获得更好的 parallax。

那么 Action 本身就可以提高 perception。

这就是：

Active Perception

所以真正高级的机器人：

Perception  ↔  Planning 可能是闭环的。

### 37. 一个经典例子：原地不动无法得到 Depth

Monocular Camera：

如果一直站着：

$$
baseline=0
$$

很多 depth 无法估计。

机器人稍微 sideways move：

$$
baseline>0
$$

parallax 出现。

于是：

$$
Depth\ observability\uparrow
$$

所以运动不是 perception 的干扰。

运动本身可以：

create information

## 故障检测与传感器选择

### 38. Failure Detection 为什么必须存在？

一个成熟 SLAM 系统绝不能假设：

> Tracking 永远不会出错。

它必须判断：

Am I still trustworthy?

比如检查：

- Number of inliers
- Reprojection error
- IMU consistency
- Pose jump
- Map match score
- Optimization residual

如果明显异常：

Tracking Lost 而不是继续自信输出垃圾。

### 39. 为什么“知道自己不知道”非常重要？

如果 Tracking 错了 5m，

但系统仍然报告：

Covariance very small 这是非常危险的。

更好的 estimator 应该：

> 当 information 变弱时，自信度下降。

也就是：

Error estimate and uncertainty should agree 这就是 estimator consistency。

### 40. Tracking Lost 后怎么办？

典型流程：

Tracking Lost

↓

暂停 Mapping / 谨慎输出 Pose

↓

Place Recognition

↓

Relocalization Candidate

↓

Geometric Verification

↓

Recover Pose

↓

Resume Tracking

所以 Relocalization 是系统：

Recovery mechanism

### 41. 如果 Relocalization 也失败呢？

可以：

- 继续尝试
- 重新初始化一张新 local map
- 后面再 Map Merge
- 依赖其他 sensors 临时维持

这取决于系统设计。

例如：

```
Map A
tracking lost
↓
new Map B
↓
later discover overlap
↓
Map Merge
```

这比让错误轨迹一直污染原地图更稳健。

### 42. 所以地图也可能存在多个 Component

并不是永远只有：

one connected map

系统可能暂时有：

$$
M_1,M_2,M_3
$$

之后发现重叠：

$$
M_1\leftrightarrow M_3
$$

再合并。

这在：

- 多机器人
- 多 session
- Tracking recovery

里都很自然。

### 43. Modern SLAM 不只是“算法精度”

真正工程评价至少包括：

Accuracy Robustness Latency Compute

$$
Memory
$$

Recovery Long-term Stability 一个离线 ATE 清晰的算法，

如果：

$$
2FPS
$$

也未必适合机器人。

### 44. Accuracy 和 Robustness 不一样

Accuracy：

> 正常工作时有多准。

Robustness：

> 环境变坏时还能不能继续工作。

例如算法 A：

$$
1cm
$$

精度，但经常 Tracking Lost。

算法 B：

$$
3cm
$$

但几乎不丢。 实际产品里 B 可能更好。

### 45. Average Performance 也不够

机器人特别关心：

Tail Failure

也就是极端场景：

- 黑暗
- 镜面
- 快速运动
- 大量动态物
- 重复环境
- 传感器抖动

平均误差很好，

但某些 corner case 突然：

$$
Pose\ jump\ 2m
$$

可能就很危险。

### 46. 所以现代系统常做大量 Consistency Checks

例如：

视觉说：

$$
\Delta R=60^\circ
$$

但 Gyro 说：

$$
\Delta R=2^\circ
$$

那应该怀疑某一边。

Stereo 说：

$$
Depth=0.3m
$$

但 temporal geometry 极不一致， 也值得检查。

这其实就是我们前面一直说的：

Cross-modal residual

### 47. Sensor Fusion 的一个更高级理解

传感器融合不只是：

> “信息更多所以更准。”

还有一个巨大价值：

Mutual verification Camera 可以检查 IMU。 IMU 可以检查 Camera。 Stereo depth 可以检查 monocular motion geometry。 LiDAR 可以检查 visual localization。 多个 measurement models 互相交叉约束，

错误更容易暴露。

### 48. 但是 Sensor 越多不一定越好

每多一个 sensor：

你也会多出：

- Calibration
- Synchronization
- Noise Model
- Failure Mode
- Compute
- Code complexity

所以：

More sensors ≠  Better system automatically

真正关键是：

> 新 sensor 是否补充了原系统真正缺失的信息？

### 49. 一个很好的 Sensor Selection 思路

不要先问：

> “这个 sensor 很厉害吗？”

而应该问：

$$
\boxed{ 它能补我当前哪些 weak / unobservable directions？ }
$$

例如：

Monocular 缺 scale：

$$
Stereo / IMU
$$

可以帮助。

VIO 缺 absolute position：

$$
GPS / UWB
$$

可以帮助。

视觉怕 darkness：

$$
LiDAR / Radar
$$

可以帮助。 这个思路比堆 sensor 更科学。

### 50. SLAM 系统设计其实就是 Information Engineering

现在回看整个 Part IV，你会发现所有设计都围绕一个问题：

Information 从哪里来，怎么保留，怎么压缩，怎么组合？

Camera：

产生视觉几何 information。

IMU：

产生动力学 information。

Keyframe：

压缩冗余 frame。

Schur Complement：

消掉 landmark，保留 pose information。

Marginalization：

消掉旧 state，保留历史 information。

Pose Graph：

把低层 measurement 压缩成 pose constraint。

Loop Closure：

注入长时间跨度 information。 这其实是一条非常统一的主线。

## 信息压缩与完整运行流程

### 51. 为什么 SLAM 中“删东西”这么重要？

你可能发现：

- Cull MapPoint
- Cull Keyframe
- Marginalize State
- Eliminate Landmark
- Compress to Pose Graph

一直在删。

原因很简单：

Data keeps growing 而机器人计算资源有限。

所以核心不是：

> 保存所有信息。

而是：

尽量删除变量和冗余表示，同时保留有价值的信息

### 52. 这就是一个在线系统和离线算法最大的差别

离线 SfM：

> 数据有限，可以慢慢算。

Online SLAM：

Data stream never ends 如果系统 complexity 随时间无限增长， 它迟早会崩。

所以真正优秀的 SLAM 设计必须考虑：

Bounded computation 或者至少增长可控。

### 53. SLAM 的状态生命周期

可以把 State 分为：

#### 新生

Current Frame / New Landmark

↓

#### 活跃

Sliding Window / Local Map

↓

#### 压缩

Marginalized / Pose Graph

↓

#### 长期保存

Keyframe / Persistent Map

↓

#### 可能删除

Redundant / Bad State

这实际上就是：

State Lifecycle Management

### 54. 一个现代 Visual-Inertial SLAM 的完整流程

现在我们真的从传感器开始走一遍。

#### Step 1：IMU 到达

得到：

$$
\omega_m,a_m
$$

利用当前：

R,p,v,b

做 propagation：

$$
X_t\rightarrow X_{t+\Delta t}^{pred}
$$

产生高频 Pose。

#### Step 2：Camera Image 到达

进行：

- undistortion
- feature extraction / tracking
- correspondence

利用 IMU prediction 缩小搜索范围。

#### Step 3：Visual Pose Correction

根据：

$$
2D-2D
$$

或：

$$
3D-2D
$$

得到 visual constraints。 把当前 Pose 修正。

#### Step 4：判断 Keyframe

检查：

- motion
- parallax
- feature count
- overlap

如果信息足够新：

Frame →  Keyframe

#### Step 5：Preintegrate IMU

将上一个 Keyframe 到当前 Keyframe 之间的 IMU：

$$
\{\omega_k,a_k\}
$$

压缩为：

$$
\Delta R,\Delta v,\Delta p
$$

形成：

IMU Factor

#### Step 6：Local / Sliding Window Optimization

Variables：

$$
Pose+Velocity+Bias+Landmarks
$$

Factors：

$$
Visual + IMU + Prior
$$

求：

$$
X^*
$$

#### Step 7：Marginalization

窗口太大：

$$
N>N_{max}
$$

移除旧 State。

把历史信息变成：

$$
Prior
$$

继续约束活跃窗口。

#### Step 8：Local Mapping

创建 / 更新 landmarks， 删除 bad points， 维护 covisibility。

#### Step 9：Loop Detection

当前 Keyframe 查询历史：

Place Recognition 得到候选。

#### Step 10：Geometric Verification

确认：

same place

并估计：

$$
SE(3)/Sim(3)
$$

relative transform。

#### Step 11：Global Optimization

加入：

Loop Factor

执行：

Pose Graph Optimization 修正长期 drift。

#### Step 12：Map Correction

修正：

- Keyframes
- MapPoints
- duplicates

必要时：

Global BA 最终整个地图重新一致。

### 55. 这十二步并不是严格串行

这是很重要的一点。

真实系统往往：

```
Tracking Thread
Local Mapping Thread
Loop Thread
Optimization Thread
```

并行工作。

所以不是：

> 一帧完整执行 12 步之后才处理下一帧。

而是多个模块异步推进。

### 56. 多线程为什么会带来新问题？

因为不同线程会同时读写：

$$
Map
$$

例如：

Tracking 正在使用：

MapPoint P Local Mapping 同时想删除 P。 Loop Closure 同时又在整体改 Pose。

于是出现：

Concurrency Problem

### 57. 所以真正 SLAM 工程里还有大量“非算法问题”

比如：

- mutex
- map ownership
- state version
- thread synchronization
- queue management
- interruption
- stale data

这些东西论文里经常不显眼， 但产品实现非常重要。

### 58. 一个很危险的问题：使用“旧地图”

比如 Tracking 正在根据：

$$
T_i^{old}
$$

做 projection。

此时 Loop Optimization 完成：

$$
T_i^{new}
$$

如果没有正确同步， Tracking 可能瞬间使用前后不一致的地图。

所以地图更新往往需要：

$$
\boxed{ Atomic / coordinated update }
$$

### 59. 实时系统为什么经常允许“近似”？

因为如果追求：

mathematical optimum 可能计算永远跟不上。

所以机器人更现实的目标：

Good enough, on time

而不是：

Perfect, too late

比如：

10ms 内 95% 精度，

可能比：

500ms 后 99% 精度 更有价值。

### 60. SLAM 是一个 Anytime System

所谓 Anytime：

> 给我更多时间，我可以继续 refine。

但现在需要结果时：

> 我也能立即给一个可用估计。

例如：

IMU Propagation：

rough but immediate

Tracking：

$$
better
$$

Local BA：

$$
better
$$

Global Optimization：

globally better

所以精度逐层提高：

Prediction  →  Local Correction  →  Local Optimization  →  Global Correction

### 61. 这是一种清晰的系统设计

短时间：

> 我先给你一个答案。

更多 measurement 来：

> 我修正答案。

长期信息来：

> 我甚至可以修改过去。

所以机器人对世界的认识不是一次性生成。

而是：

Progressively refined belief

## 学习型方法与系统分析

### 62. 现代 End-to-End SLAM 是否会改变这一切？

近年来确实有很多 neural / end-to-end 方法：

$$
Images \rightarrow Trajectory / Map
$$

网络承担越来越多：

- Feature
- Flow
- Depth
- Matching
- Optimization-like update

但即使内部实现变了，

从系统需求看仍然逃不开：

- current state
- temporal association
- geometry
- uncertainty / confidence
- long-term consistency
- memory management
- loop / revisiting

所以经典 SLAM 的这些概念不会因为模型变成 Transformer 就失去价值。

### 63. 学经典 SLAM 的意义不是为了永远用 ORB

这一点我希望你现在已经很明确。

我们真正学的是：

$$
State
$$

Measurement Observability Data Association Optimization Information Compression Consistency 这些是机器人状态估计的基本问题。 ORB、SIFT、某个网络只是具体工具。

### 64. 看一个陌生 SLAM 系统，你现在应该怎么拆？

以后读一篇论文，先不看它的 fancy 名字。

直接问：

#### 1

它的：

State 是什么？

#### 2

有哪些：

$$
\boxed{ Sensors / Measurements？ }
$$

#### 3

每种 measurement 定义了什么：

Residual？

#### 4

哪些 state direction：

$$
\boxed{ Observable / Weak / Unobservable？ }
$$

#### 5

Front-end 怎样产生：

Data Association？

#### 6

Optimization 是：

$$
\boxed{ Filtering / Sliding\ Window / Full\ Smoothing？ }
$$

#### 7

旧信息怎么处理：

$$
\boxed{ Marginalization / Keyframe / Elimination？ }
$$

#### 8

有没有：

$$
\boxed{ Loop / Global\ Constraint？ }
$$

这八个问题下来， 大多数 SLAM / VIO / LIO 系统都能拆出骨架。

### 65. 一个陌生机器人定位系统也一样

比如论文说：

> “我们提出 XXX-Fusion++，融合 Camera、Radar、IMU。”

先别管名字。

你问：

$$
State?
$$

可能：

Pose,velocity,bias

Camera：

Reprojection Factor

Radar：

$$
Doppler / Range\ Factor
$$

IMU：

Preintegration

窗口：

$$
10\ states
$$

旧 state：

Marginalize

全局：

$$
Loop
$$

### 66. 这就是这一整个 Part IV 真正想培养的能力

不是：

> 背出 ORB-SLAM pipeline。

而是：

看到一个机器人 State Estimation System，就能从信息流和约束关系把它拆开

> 修订说明：从原地不动无法恢复 depth 的例子指未给定已知几何的单目多视图三角化；双目、RGB-D、LiDAR 或已知物体尺度不受该说法限制。多时间尺度与 anytime 输出是常见设计思路，不意味着所有 SLAM 实现都满足同样的实时保证。

## 自测

本章的系统分析问题与八道综合自测统一放在 [Part IV 回顾与自测](summary.md)，可先用本章流程解释，再展开答案检查。

## 相关章节与来源

- 上一章：[视觉／激光惯性状态估计](visual-lidar-inertial.md)
- 下一篇：[Part IV 回顾与自测](summary.md)
- 来源：本次新增 Part IV Chapter 48 课堂草稿；保留核心推理、例子与自测，删除聊天开场和重复课程预告。
