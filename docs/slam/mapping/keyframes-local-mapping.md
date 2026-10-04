---
title: 关键帧与局部建图
description: 如何控制状态与地图规模，同时保留有效几何信息？
icon: book-open
course: Robot Perception & SLAM
part: Part IV Mapping and SLAM
week: 4
chapter: 41
chapter_type: lecture
status: organized
tags: [slam, mapping, state-estimation]
---

# 关键帧与局部建图

## 本章目标

如何控制状态与地图规模，同时保留有效几何信息？

## 前置知识

[Visual SLAM 前端](visual-frontend.md)、[Gauge Freedom](gauge-freedom.md)。

## 定义与假设

以关键帧视觉 SLAM 为主例；共视邻域、筛选阈值和线程划分属于系统设计选择，不能当作所有 SLAM 都采用的固定标准。

## 核心问题


## 关键帧选择与视差

### 1. 为什么不能把每一帧都永久保存？

假设相机：

$$
30\ FPS
$$

机器人运行：

$$
10\ min
$$

那就是：

$$
30\times60\times10=18000
$$

帧。

如果运行一小时：

$$
108000
$$

帧。

如果每一帧都作为状态进入后端：

$$
x_0,x_1,\dots,x_{108000}
$$

然后还有几十万个甚至几百万个 landmarks。 这显然会越来越重。

所以第一个问题就是：

> 所有 Frame 的价值一样吗？

答案显然是：

$$
\boxed{No}
$$

### 2. 相邻 Frame 往往高度冗余

假设机器人运动很慢：

```
Frame 100
Frame 101
Frame 102
Frame 103
```

它们可能几乎长这样：

```
100: ●  ▲  ■
101: ●  ▲  ■
102: ●  ▲  ■
103: ●  ▲  ■
```

只有几个 pixel 的变化。 那么保存四个完整状态，带来的新信息其实很少。

也就是说：

Frame count  ≠  Information amount 这和上一章讲 feature number 一样。 不是数据越多越好。

重要的是：

新增信息量

### 3. Keyframe 是什么？

Keyframe 可以理解成：

> 从连续 Frame 中挑出来的、值得长期保留的重要帧。

比如：

```
F1 F2 F3 F4 F5 F6 F7 F8 F9
   ↑        ↑           ↑
  KF1      KF2         KF3
```

普通 Frame：

> 用来短期 Tracking。

Keyframe：

> 进入地图和后端，承担长期几何约束。

所以：

$$
\boxed{ Keyframe = compressed trajectory representation }
$$

### 4. 为什么说它是“信息压缩”？

假设：

$$
F_{100}
$$

和：

$$
F_{101}
$$

视觉上几乎一样。

它们看到的 landmarks：

$$
90\%
$$

都相同。 那这两帧提供的 constraint 高度重复。 所以只保留其中一个， 往往不会损失多少信息。

Keyframe selection 的本质就是：

丢掉大量重复 measurement，只保留有代表性的状态

### 5. 什么时候应该插入一个新 Keyframe？

这个问题没有唯一规则。 但可以从“新信息是否足够多”来理解。

常见因素有：

- 相机移动距离够大
- Rotation 够大
- 与上一 Keyframe overlap 降低
- 新看到很多 landmarks
- Tracking quality 下降
- 有足够新的 parallax

所以可以抽象成：

Is this frame sufficiently different?

### 6. 仅仅移动距离大就一定要插 Keyframe 吗？

不一定。

比如相机：

```
→ 0.5m
```

但看的都是：

$$
100m
$$

远处建筑。 图像 parallax 可能很小。

反过来移动：

$$
5cm
$$

但在非常近的桌面旁边。 parallax 可能已经很明显。

所以：

Physical motion  ≠  Visual information Keyframe 决策最好考虑实际观测变化。

### 7. Parallax 为什么特别重要？

因为新 Keyframe 往往还承担一个任务：

Triangulate new MapPoints

如果两个 keyframes 太近：

```
KF1 KF2
 \   \
  \   \
```

baseline 很小。 Triangulation 很不稳定。

如果：

```
KF1              KF2
  \              /
   \            /
       Point
```

parallax 足够， depth 才能可靠恢复。 所以 Keyframe spacing 不能太小。

### 8. 但也不能太大

如果两个 Keyframes 距离太远：

```
KF1 ---------------- KF2
```

可能 overlap 已经太少。 Feature association 变困难。

于是：

- Matching 数量下降
- Tracking risk 增加
- Triangulation correspondence 减少

所以本质上是在平衡：

$$
\boxed{ Too\ similar \quad vs \quad Too\ different }
$$

### 9. 普通 Frame 去哪里了？

这个问题很重要。 普通 Frame 并不是“没用”。

它们常常承担：

Tracking 也就是实时估计当前 Pose。

例如：

```
KF0

F1
F2
F3
F4

KF1
```

F1～F4 都可以利用 Map 做 PnP， 得到各自 Pose。 但可能不会全部永久进入地图。

所以可以理解成：

Every frame is tracked, but not every frame is mapped

### 10. Tracking 和 Mapping 开始分工了

现在 SLAM 系统自然出现两个时间尺度。

#### 高频

Tracking 每帧都做。

目标：

> 当前机器人在哪？

要求：

- 快
- 实时
- 局部

#### 低频

Mapping 只对 Keyframe 做。

目标：

> 地图怎么扩展？局部状态怎么优化？

可以慢一点。

所以：

```
Camera 30 FPS
↓
Tracking 30 Hz

Keyframes
↓
Mapping maybe lower rate
```

这就是现代 SLAM 常见的多线程结构的来源。

## 局部地图与共视关系

### 11. Local Map 是什么？

假设整个地图已经有：

$$
100000
$$

个 MapPoints。

当前 Camera 在地图某个小区域：

```
Global Map:

. . . . . . . . . .
. . . . [camera] . .
. . . . . . . . . .
```

Tracking 当前帧时， 真的需要和全地图 10 万个点匹配吗？ 当然没必要。 大多数 point 根本看不到。

所以系统只拿当前附近相关的那部分：

Local Map

### 12. Local Map 不是一定按“物理距离”定义

这一点很重要。

你可能觉得：

> Local 就是离 Camera 最近 5 米。

有时可以这么做，

但视觉 SLAM 更常根据：

$$
\boxed{ Visibility / Covisibility }
$$

来定义。

也就是说：

> 哪些 Keyframe 和当前 Frame 共享很多 MapPoints？

这些才是真正视觉上“邻近”的节点。

### 13. Covisibility 是什么？

假设 Keyframe A 和 B 都看到了很多相同 landmarks。

比如：

$$
A
$$

看见：

$$
\{1,2,3,4,5,6\}
$$

B 看见：

$$
\{2,3,4,5,6,7\}
$$

它们共享：

$$
5
$$

个 landmarks。

那 A 和 B：

Covisibility high

所以建立一条关系：

```
KF A ===== KF B
```

边的权重可以是：

shared MapPoints count

### 14. Covisibility Graph

如果多个 Keyframes：

```
KF1 ---- KF2
 |      / |
 |     /  |
KF3 ---- KF4
```

边表示共享很多 landmarks。

这就是：

Covisibility Graph 它非常有用。 因为当前 Frame 如果靠近 KF2，

那 KF2 的强 covisible neighbors：

$$
KF1,KF3,KF4
$$

大概率也和当前区域相关。

于是这些 Keyframes 和它们的 MapPoints 就组成：

Local Map

### 15. 为什么 Covisibility 比时间邻近更合理？

假设机器人：

```
走了一圈
```

当前时刻：

$$
t=10000
$$

但它回到了：

$$
t=100
$$

附近。

在时间上：

$$
10000
$$

和：

$$
100
$$

差得很远。 但空间上它们其实很近。

如果只按时间窗口：

$$
t-10,\dots,t
$$

就看不到旧区域。

而 covisibility 能反映：

Spatial relationship 这比单纯时间邻近更强。

### 16. Local Mapping 到底做什么？

一个新 Keyframe 进入 Mapping 后，通常会做几类事情。

可以记成：

Insert  →  Triangulate  →  Cull  →  Optimize 我们逐个讲。

## 地图点创建与筛选

### 17. 第一步：Insert Keyframe

当前 Frame 被决定成为 Keyframe。

于是把它的：

- Pose
- Features
- Observations
- Descriptor
- 与 MapPoint 的关联

加入地图结构。

它从：

temporary frame

变成：

persistent state

### 18. 第二步：建立新的 MapPoints

新 Keyframe 会与附近 Keyframes 找 correspondence。

例如：

```
KF_new ↔ KF_old
```

找到：

$$
p_i^{new} \leftrightarrow p_i^{old}
$$

然后 Triangulation：

$$
p^{new},p^{old} \rightarrow P^w
$$

生成新的：

MapPoint

所以：

New Keyframe  →  New landmarks

### 19. 但不是每个 Triangulation 都可信

Triangulate 出来的点必须检查。

常见检查包括：

- positive depth
- reprojection error
- sufficient parallax
- reasonable scale/depth
- appearance consistency

比如如果 triangulated point 在 camera 后方：

$$
Z<0
$$

那显然有问题。

### 20. Positive Depth / Cheirality

真实被相机看到的 3D point 应该在相机前方：

$$
Z>0
$$

如果某个 pose/triangulation 解导致：

$$
Z<0
$$

说明几何解不物理。

这个约束叫：

Cheirality constraint

### 21. Reprojection Check

Triangulation 后得到：

$$
P^w
$$

重新投回两个 Keyframes：

$$
\hat p_1=\pi(T_1P)
$$

$$
\hat p_2=\pi(T_2P)
$$

如果：

$$
\|p_1-\hat p_1\|
$$

很大， 那这个 point 很可能不可靠。 所以地图点创建后仍然要通过 geometry 自检。

### 22. 第三步：MapPoint Culling

地图如果只增不减， 会越来越臃肿。 而且很多新点其实质量很差。

比如某个 MapPoint：

- 只被看到一次
- 很快再也匹配不到
- reprojection residual 很大
- depth 很不稳定

那它没有保留价值。

所以系统会删除：

Bad MapPoints

### 23. 为什么“被多次观察”很重要？

一个 landmark 如果只有：

$$
1
$$

个 observation， 通常几何约束很弱。

如果：

$$
5
$$

个不同 keyframe 都稳定看到它：

```
KF1 \
KF2  \
KF3 --- P
KF4  /
KF5 /
```

那么：

$$
P
$$

位置更可靠， 而且对 Pose estimation 也更有帮助。 所以 observation count 是一个重要质量指标。

### 24. Keyframe 自己也要 Culling

既然 MapPoint 会冗余， Keyframe 也会。

假设：

```
KF1
KF2
KF3
```

KF2 看到的 95% MapPoints， KF1 和 KF3 都已经能很好地观察。 那么 KF2 可能没提供多少独特信息。

这时：

$$
\boxed{ KF2\ is\ redundant }
$$

可以删掉。

### 25. Keyframe Culling 的本质

可以理解成：

> 如果一个 Keyframe 的绝大多数信息都已经被其他 Keyframes 覆盖，那它就不值得继续占状态空间。

这仍然是：

Information compression

所以 Keyframe selection 和 Keyframe culling 是一进一出：

```
Insert useful frames
Delete redundant frames
```

## 局部 BA 与跟踪协作

### 26. 第四步：Local Bundle Adjustment

这是 Local Mapping 最关键的操作之一。

假设当前附近有：

$$
KF_1,KF_2,KF_3
$$

和：

$$
P_1,P_2,\dots,P_N
$$

那么优化：

$$
\{T_i,P_j\}
$$

使 reprojection error 最小：

$$
\min_{\{T_i,P_j\}} \sum_{i,j} \left\| p_{ij} - \pi(T_iP_j) \right\|^2
$$

这就是：

Local Bundle Adjustment

### 27. 为什么叫 Bundle Adjustment？

Bundle 可以理解成：

> 很多 Camera rays 像一束束光线一样共同连接到 3D points。

比如：

```
KF1 \   |   /
     \  |  /
       P
     /  |  \
KF2 /   |   \ KF3
```

Optimization 同时调整：

Camera Poses

和：

$$
3D\ Points
$$

让所有 rays 与 observations 尽可能一致。 所以叫 Bundle Adjustment。 Chapter 43 会完整讲数学。 现在先建立直觉。

### 28. 为什么是 Local BA，而不是每次 Global BA？

如果地图已经有：

$$
10000
$$

个 Keyframes，

每插入一帧都优化全部变量：

Global BA 实时性完全不行。

所以日常只优化：

Current neighborhood

即：

Local BA 而真正全局的大优化，

只在：

- Loop Closure
- 离线 refinement
- 特定时机

才执行。

### 29. Local BA 优化哪些变量？

一个常见做法：

#### Active Keyframes

当前局部区域里的 Keyframes：

$$
\{KF_{active}\}
$$

允许优化。

#### Local MapPoints

这些 Keyframes 看到的 MapPoints：

$$
\{P_{local}\}
$$

允许优化。

#### Boundary / Fixed Keyframes

局部地图之外，

但和 local points 有 observation 的 Keyframes：

$$
\{KF_{fixed}\}
$$

保持不动。

### 30. 为什么要有 Fixed Boundary？

假设只优化局部区域：

```
Global map ---- [ Local Area ]
```

如果 local area 没和外部绑定， 它可能整体漂。

所以需要外围一些 Keyframes：

$$
fixed
$$

作为边界约束。

类似：

```
fixed ---- variable ---- variable ---- fixed
```

这样 local optimization 不会和 global map 脱节。

### 31. 这其实也是 Gauge Fixing

局部 BA 本身也可能存在整体自由度。

所以：

- 固定某些外围 Pose
- 或固定其中一个 Keyframe

本质还是上一章讲的：

Gauge fixing 你会发现这些章节其实一直在互相连接。

### 32. Tracking 和 Local Mapping 怎么协作？

可以这样看。

#### Tracking 线程

每来一帧：

$$
Image_t
$$

快速估：

$$
T_t
$$

主要目标：

Realtime

#### Local Mapping 线程

收到新 Keyframe：

- triangulate
- update map
- cull bad points
- local BA

主要目标：

Local consistency

所以：

```
Camera
  ↓
Tracking ───────────→ Current Pose
  │
  └── if new keyframe
           ↓
      Local Mapping
           ↓
      Update Local Map
           ↓
       back to Tracking
```

### 33. 为什么多线程特别自然？

因为 Tracking 必须跟相机帧率走。

如果 Local BA 突然耗时：

$$
100ms
$$

不能让 Camera tracking 停下来。 否则后面帧全堆住了。

所以很多 SLAM 系统自然做成：

Tracking Thread Local Mapping Thread Loop Closing Thread 这不是纯软件工程习惯， 而是不同模块天然有不同时间尺度。

### 34. 这里顺便理解 ORB-SLAM 为什么结构这么经典

ORB-SLAM 经典上就是这种模块化思路：

Tracking 负责当前帧。 Local Mapping 维护局部地图。 Loop Closing 维护长期全局一致性。 所以如果你未来去读 ORB-SLAM 源码，

不要把它看成：

> 三个作者随便分出来的模块。

而是三个不同空间/时间尺度：

```
Tracking:
milliseconds / current frame

Local Mapping:
seconds / local neighborhood

Loop Closing:
long-term / global map
```

### 35. Local Map 如何帮助 Tracking？

假设当前 Camera Pose 有一个初值：

$$
T_t^{pred}
$$

系统根据这个 pose， 可以预测哪些 local MapPoints 应该落到当前图像内。

比如：

$$
P_j^w
$$

转换到 Camera：

$$
P_j^c=T_{cw}P_j^w
$$

然后投影：

$$
\hat p_j=\pi(P_j^c)
$$

如果在图像范围内：

> 它可能可见。

于是只在：

$$
\hat p_j
$$

附近搜索 feature。

这叫：

Projection Matching

### 36. 为什么 Projection Matching 比全图匹配快？

如果知道一个 landmark 理论上应该在：

$$
(u,v)
$$

附近，

就不用在：

$$
640\times480
$$

整张图里搜。

只在一个小 window：

$$
(u\pm r,v\pm r)
$$

搜索。 所以 Motion Prediction + Map 提供了一个非常强的 prior。 这也是地图反过来帮助 Tracking 的具体体现。

### 37. Map 不只是点云，它还有“观察关系”

在 SLAM 里，真正重要的地图通常不只是：

$$
P_1,P_2,P_3
$$

这些 3D 坐标。

还有：

Who observed whom

例如：

```
KF1 → P1, P2, P3
KF2 → P2, P3, P4
KF3 → P4, P5
```

这些 observation relations 才构成后端优化的图。

所以“地图”其实包含：

- geometry
- appearance
- observation topology

### 38. 这就是为什么 SLAM Map 比普通 Point Cloud 更丰富

普通 point cloud：

$$
\{P_i\}
$$

可能只有 3D 坐标。

而 SLAM MapPoint 往往还会保存：

- 3D position
- descriptor
- normal/view direction
- observation count
- visible count
- associated keyframes

所以它是一个：

Landmark state 而不只是一个 xyz 点。

### 39. Landmark 的 Descriptor 怎么定义？

一个 landmark 会被多个 Keyframes 看到。

比如：

$$
d_1,d_2,d_3,d_4
$$

那它的 descriptor 可以选一个代表。

例如 ORB 系统可能选：

> 与其他 descriptors 总距离较小的那个。

为什么不简单 average？

因为 ORB descriptor 是：

$$
binary
$$

直接平均并没有很自然的意义。

### 40. Viewing Direction 为什么有用？

同一个 MapPoint：

```
     Camera A
       \
        P
       /
Camera B
```

如果当前 Camera 从完全不同的方向看它， 它的 appearance 可能变化很大， 甚至根本看不到。

所以 landmark 可以记录：

average viewing direction

当前视角偏差太大时：

> 不优先匹配。

这也是减少错误 association 的办法。

### 41. Scale Prediction 也可以来自 Map

ORB feature 是多尺度 pyramid 检测的。

某个 MapPoint 如果离 Camera 很近：

> 在图像里应该更大。

离得远：

> 应该落在更高层 pyramid。

所以根据 landmark depth / distance，

可以预测：

expected scale level 然后只在合理尺度搜索。 这进一步减少匹配搜索空间。

### 42. 所以一个成熟前端不是“暴力 matching”

它会利用很多 prior：

Pose prediction Projection

$$
Scale
$$

Viewing angle Descriptor Geometry 逐层筛选。 这才是工业/成熟系统里真正高效的 association。

## 计算预算、窗口与状态生命周期

### 43. Local Map 的大小也是一个设计问题

Local Map 太小：

not enough constraints Tracking 容易不稳。

太大：

too expensive

所以它也是：

Accuracy vs Efficiency 的平衡。

实际系统可能按：

- Covisibility score
- nearest keyframes
- recent keyframes
- tree neighbors

组合选取。

### 44. 为什么 Keyframe 不是固定每 10 帧一个？

因为：

Frame index

和：

Information gain 没直接关系。

机器人如果静止：

```
10 秒不动
```

即使过了 300 帧， 也可能不需要新 Keyframe。

如果快速转弯：

```
0.2 秒
```

场景变化很大， 可能很快就需要一个。

所以：

$$
\boxed{ Keyframe\ policy\ should\ be\ event/information\ driven }
$$

而不是纯时间驱动。

### 45. 为什么 Keyframe 插得太密不好？

如果 Keyframes 太密：

- BA 变量变多
- Covisibility Graph 变大
- MapPoints 高度重复
- 计算增加
- memory 增加

但新增信息很小。

于是：

Redundancy explosion

### 46. 插得太稀也不好

如果 Keyframe 太少：

- baseline 太大
- overlap 太低
- feature association 困难
- triangulation 断层
- local map 不连续

所以同样不好。

### 47. Keyframe Selection 其实就是“采样理论”

你可以把连续 trajectory：

$$
x(t)
$$

看成一个连续过程。 Frame 是高频采样。

Keyframe 则是：

> 根据环境和运动动态降采样。

但它不是均匀 downsample。

而是：

Adaptive sampling

信息变化大：

> 多采。

变化小：

> 少采。

这个理解很不错。

### 48. Mapping Thread 跟不上怎么办？

真实系统可能出现：

Tracking：

$$
30 FPS
$$

但 Mapping 处理 Keyframe 很慢。

如果不断插新 Keyframe：

```
KF queue:
KF1 KF2 KF3 KF4 KF5 ...
```

队列会积压。

于是系统常常会：

- 减少新 Keyframe 插入
- 暂停部分 Mapping 工作
- 中止当前 Local BA

优先保证：

Tracking not lost 因为 tracking 一旦丢失，代价更大。

### 49. 为什么 Local BA 可以被打断？

假设正在优化：

$$
KF_{20}\sim KF_{30}
$$

突然又来了一个新 Keyframe。 如果 Tracking 急需新的 Map 更新， 可能选择中止当前 optimization。

因为 BA 不是：

> 必须一次算到底才有意义。

实时 SLAM 首先是一个在线系统。

所以需要：

Anytime behavior 能算多少算多少，实时优先。

### 50. Keyframe 和 Loop Closure 有什么关系？

Keyframes 还有另一个很重要的职责：

Place Recognition Loop Closure 不可能拿当前 Frame 和过去几十万原始 Frame 全比较。

所以通常只在 Keyframes 之间做：

Current KF  ↔  Past KFs

因此 Keyframe 也是：

> 长期记忆的视觉摘要。

### 51. 所以 Keyframe 同时承担三种角色

这个值得记住。

#### 第一

Trajectory compression：

reduce state count

#### 第二

Mapping anchor：

$$
triangulation + BA
$$

#### 第三

Place recognition unit：

$$
loop\ closure / relocalization
$$

所以 Keyframe 不是简单“每隔几帧保存一张图”。

### 52. Keyframe 与 Landmark 是双向关系

可以想成：

```
Keyframe  ←→  MapPoint
```

Keyframe 保存：

> 我看到了哪些 MapPoints。

MapPoint 保存：

> 哪些 Keyframes 看到了我。

这形成 bipartite graph：

```
KF1 ---- P1
 |  \    |
 |   \   |
 P2   \ KF2
```

Bundle Adjustment 本质上就在这个 graph 上优化。

### 53. 这实际上已经接近 Factor Graph 了

Variable：

$$
T_i
$$

$$
P_j
$$

Observation：

$$
z_{ij}
$$

Factor：

$$
r_{ij} = z_{ij}-\pi(T_iP_j)
$$

于是：

```
Pose nodes
Landmark nodes
Measurement factors
```

所以 Local Mapping 的数据结构本身已经在为后面的：

Factor Graph 铺路。

### 54. Local Map 和 Global Map 的关系

不要理解成两个完全独立地图。

更准确是：

Local Map  ⊂  Global Map 它是当前活跃的工作集。

类似 CPU cache：

```
Global Map = memory

Local Map = active cache
```

当前需要的状态拿出来频繁访问。 其余部分先放着。 这个比喻其实非常准确。

### 55. Sliding Window 和 Local Map 有什么联系？

后面 Visual-Inertial SLAM 中经常会看到：

Sliding Window

例如只优化最近：

$$
10
$$

个 states。

这和 Local Mapping 思想非常类似：

> 只维护一个 active set。

区别是：

Sliding Window 常更强调：

recent temporal states

而 Visual SLAM Local Map 可能更强调：

$$
covisibility / spatial\ neighborhood
$$

### 56. 为什么 VIO 更喜欢时间窗口？

因为 IMU constraints 天然连接：

$$
x_t \leftrightarrow x_{t+1}
$$

所以时间连续性很强。

于是：

$$
x_{t-k},\dots,x_t
$$

自然形成一个 window。 而纯视觉地图则可以大量利用空间上的 covisibility。

### 57. Marginalization 提前预告

Sliding Window 有一个问题：

> 旧 state 移出 window 后，它的信息怎么办？

不能简单删除。 否则历史 information 全没了。

所以需要：

Marginalization 把旧状态的信息压缩成一个 prior， 继续约束剩余状态。 这以后讲 VIO 时会详细讲。

它其实又回到一个主题：

How to compress information

### 58. 现在你应该看到 Part IV 的一条暗线

Chapter 37：

$$
Trajectory + Map
$$

状态会越来越大。

Chapter 38：

EKF 用 covariance 压缩历史。

Chapter 41：

Keyframe / Local Map 用选择性状态压缩规模。

以后：

Marginalization：

用概率方式压缩旧状态。

Pose Graph：

把 landmark level constraints 压缩成 pose-level constraints。

这些其实都在解决同一个工程难题：

如何保留有用 information，同时控制计算复杂度

### 59. 一个完整的 Local Mapping Pipeline

现在可以把它整理为：

```
Current Frame
     ↓
Tracking
     ↓
Should create Keyframe?
     ↓ yes
Insert New Keyframe
     ↓
Find Covisible Keyframes
     ↓
Match Features
     ↓
Triangulate New MapPoints
     ↓
Cull Bad MapPoints
     ↓
Local Bundle Adjustment
     ↓
Cull Redundant Keyframes
     ↓
Update Local Map
```

这就是 Chapter 41 最核心的系统流程。

### 60. 用一个具体例子走一遍

机器人当前有：

$$
KF_{10}
$$

然后运行了几帧：

```
F11
F12
F13
F14
```

F14 与 KF10 已经有明显 baseline。

于是：

$$
F14\rightarrow KF_{14}
$$

系统发现 KF14 与：

$$
KF_{10},KF_9,KF_8
$$

共享很多 features。

于是构建 Local Map：

$$
\{KF_8,KF_9,KF_{10},KF_{14}\}
$$

KF14 与 KF10 找到一些还没有 3D MapPoint 的 correspondence。

做 triangulation：

$$
p_{14}\leftrightarrow p_{10} \rightarrow P_{new}
$$

生成：

$$
50
$$

个新 landmarks。

其中：

$$
15
$$

个 reprojection error 大， 被删除。

剩：

$$
35
$$

个。

然后 Local BA：

$$
KF_8,KF_9,KF_{10},KF_{14}
$$

加局部 MapPoints， 一起优化。

最后发现：

$$
KF_9
$$

绝大多数 MapPoints 已被其他 KFs 覆盖， 于是可能删除 KF9。 整个地图规模保持稳定。 这就是一个非常典型的 Local Mapping cycle。

### 61. 为什么 BA 后 MapPoint 会移动？

因为 Triangulation 得到的初始 3D point：

$$
P^{init}
$$

只是根据少数 observations 算出的。

后来更多 Keyframes 看到它：

$$
p_1,p_2,p_3,p_4
$$

于是可以优化：

$$
P
$$

使所有 reprojection error 综合最小。

所以 MapPoint 不是：

> 一旦创建就固定。

它也是 State。

### 62. Camera Pose 也一样

Tracking 给的 Pose：

$$
T_t^{track}
$$

只是当前局部 estimate。

Local BA 以后可能变成：

$$
T_t^{BA}
$$

所以：

Tracking estimate  ≠  final estimate 在线 SLAM 里的状态会持续被未来信息修正。

### 63. 这也是为什么 SLAM 轨迹会“动”

你如果可视化 SLAM， 可能看到历史轨迹突然稍微变形。 这不是 bug。

因为 Local BA / Loop Closure 会修改：

Past Poses 使整体更一致。 所以 SLAM trajectory 不是一条写死的日志。

它是：

Living estimate

### 64. Mapping 和 Perception 有一个根本区别

普通 perception 常常是：

```
Frame in
↓
Result out
↓
done
```

比如 Object Detection：

$$
Image_t\rightarrow Boxes_t
$$

每帧相对独立。

SLAM 则是：

```
Frame in
↓
Update persistent state
↓
Future frames may revise past state
```

也就是：

Persistent world model 这是 SLAM 系统设计非常不同的地方。

### 65. 这和机器人系统的长期记忆很接近

你可以把：

Keyframes 理解成视觉长期记忆的骨架。

MapPoints 是：

environment structure

Covisibility Graph 是：

memory association

所以 SLAM 某种程度上就是：

> 在构建一个不断修正的空间记忆。

### 66. 本章最重要的七句话

第一：

Every frame is not equally informative

第二：

$$
\boxed{ Keyframe = trajectory 的信息压缩 }
$$

第三：

Tracking 每帧运行，Mapping 主要处理 Keyframes

第四：

Local Map 通常通过 Covisibility 而不是单纯时间定义

第五：

Local Mapping 的主要流程：

Insert  →  Triangulate  →  Cull  →  Optimize

第六：

Local BA

同时优化局部：

$$
Camera\ Poses + MapPoints
$$

第七：

Keyframe 的根本目的不是“少存几张图片”，而是：

最大限度保留几何信息，同时限制状态规模

> 整理说明：关键帧选择与 culling 是信息和计算的权衡，并不保证完全无损；应保留唯一几何观测和连接图的必要状态。Local BA 的固定边界需要充分约束基准，单目尺度仍应按模型检查。

## 思考题

### Q1：为什么相机静止时，不应该每隔固定时间插 Keyframe？

**参考答案**

因为虽然 Frame 数量增加， 但 scene geometry 基本不变。 新增 information 很少。

只会制造：

redundant states

因此 Keyframe 应更依赖：

$$
motion + parallax + information gain
$$

而不是单纯时间。


### Q2：为什么 Keyframe 之间需要一定 parallax？

**参考答案**

因为新 MapPoint 通常依赖多视角 triangulation。

如果：

$$
baseline\approx0
$$

两条 viewing ray 几乎平行， depth uncertainty 很大。 所以需要一定视差。


### Q3：为什么又不能让 Keyframe 间隔过大？

<details>

<summary>参考答案</summary>

因为 overlap 会下降。 Correspondence 变少， Tracking / triangulation 都会更困难。

所以存在一个折中：

enough parallax

但：

enough overlap

</details>

### Q4：为什么 Local Map 不应该简单定义为“最近 10 个 Frame”？

<details>

<summary>参考答案</summary>

因为机器人可能：

Loop back 回到很早以前的位置。 时间上很远， 空间上却很近。 Covisibility 能更好表达真实 spatial neighborhood。

</details>

### Q5：为什么一个 MapPoint 被很多 Keyframes 观察后更有价值？

<details>

<summary>参考答案</summary>

因为：

multiple independent observations 能降低其 position uncertainty， 同时它也能更稳定地约束多个 Camera Poses。 因此它既是更好的地图点， 也是更好的 localization reference。

</details>

### Q6：为什么 Local BA 不需要每次把整个 Global Map 一起优化？

<details>

<summary>参考答案</summary>

因为当前新 Keyframe 对远处地图的直接影响很弱。 大多数新 measurement 只连接附近 Keyframes / MapPoints。 所以利用图的局部稀疏性， 只优化 active neighborhood 就能获得大部分收益。

</details>

### Q7：Keyframe Culling 会不会把有用历史信息直接丢掉？

<details>

<summary>参考答案</summary>

如果策略合理，不会简单“无脑删除”。 只有当一个 Keyframe 的 observations 已经被多个其他 Keyframes 充分覆盖时， 它才被认为高度冗余。 真正独特的几何 constraint 应该保留下来。 所以本质不是删除历史，

而是：

remove redundant representation

</details>

## 相关章节与来源

- 上一章：[Visual SLAM 前端](visual-frontend.md)
- 下一篇：[非线性最小二乘](nonlinear-least-squares.md)
- 来源：本次新增 Part IV Chapter 41 课堂草稿；保留核心推理、例子与自测，删除聊天开场和重复课程预告。
