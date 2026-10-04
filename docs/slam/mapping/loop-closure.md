---
title: 回环检测与全局校正
description: 怎样验证“来过这里”，并把可靠回环用于地图校正？
icon: book-open
course: Robot Perception & SLAM
part: Part IV Mapping and SLAM
week: 4
chapter: 46
chapter_type: lecture
status: organized
tags: [slam, mapping, state-estimation]
---

# 回环检测与全局校正

## 本章目标

怎样验证“来过这里”，并把可靠回环用于地图校正？

## 前置知识

[数据关联](../spatial/data-association.md)、[Pose Graph](pose-graph.md)、[关键帧与局部建图](keyframes-local-mapping.md)。

## 定义与假设

检索只生成候选，接受回环需要几何验证与一致性证据；保守门限、连续帧检查和鲁棒权重是工程策略，不能保证消除所有错误回环。

## 核心问题


先把最重要的一句话放在前面：

Loop Closure 的核心不是“图像看起来像”，而是“确认当前地点和历史地点在几何上确实是同一个地方” 前者只是候选。 后者才能真正加进 SLAM Graph。

## 地点识别与候选检索

### 1. 为什么需要 Loop Closure？

假设机器人从 A 出发：

```
A → B → C → D → E
```

每一步 odometry 都有一点误差：

$$
\epsilon_1,\epsilon_2,\dots
$$

长期以后：

Drift 越来越大。

如果机器人一直往未知区域走，其实很难判断：

> 到底漂了多少？

但是如果最后回到 A：

```
A → B → C → D
↑             ↓
└───── E ←────┘
```

Camera 突然看到：

> “等等，这个地方好像和一开始一样。”

于是产生：

$$
x_E\leftrightarrow x_A
$$

这种长距离约束。 这就是 Loop Closure。

### 2. Loop Closure 真正提供什么？

很多入门介绍会说：

> Loop Closure 就是识别曾经来过的场景。

这只是第一半。

对于 SLAM 来说，真正有价值的是：

Relative Geometric Constraint

也就是说最终要得到：

$$
Z_{ij}
$$

描述：

> 当前 Keyframe $$i$$ 和历史 Keyframe $$j$$ 之间的相对 Pose 应该是多少。

然后才能放进：

Pose Graph

### 3. 完整 Loop Closure Pipeline

我们先把整条链摆出来：

```
Current Keyframe
      ↓
Place Recognition
      ↓
Historical Candidates
      ↓
Appearance Check
      ↓
Feature Matching
      ↓
Geometric Verification
      ↓
Relative Pose Estimation
      ↓
Loop Accepted?
      ↓ yes
Create Loop Constraint
      ↓
Pose Graph / Map Correction
```

这一章就沿着这条链讲。

### 4. 第一步：Place Recognition

当前 Keyframe：

$$
K_t
$$

历史已经有：

$$
K_1,K_2,\dots,K_{t-1}
$$

问题：

> 当前这张图和历史哪张图最像？

最笨的方法当然可以：

$$
K_t
$$

和过去所有图逐张匹配。

但如果有：

$$
100000
$$

个 Keyframes， 计算量会非常大。

所以需要：

Image Retrieval 快速找几个最可能的候选。

### 5. Place Recognition 和 Feature Matching 不一样

这两个概念非常容易混。

#### Place Recognition

回答：

> 当前整张图，和历史哪几个地点可能是同一地方？

属于：

Global retrieval

#### Feature Matching

回答：

> 两张已经选定的图里，具体哪些 feature 是对应的？

属于：

Local correspondence

所以：

```
Place Recognition
        ↓
找到候选 Image / Keyframe

Feature Matching
        ↓
找到具体点对应
```

两层完全不同。

### 6. 为什么不能一开始直接 Feature Match 所有历史帧？

因为代价太高。

比如：

$$
50000
$$

个历史 Keyframes。

每帧：

$$
1000
$$

个 features。

如果全量 brute-force：

> 完全没必要。

所以 Place Recognition 相当于：

Coarse Retrieval

先从 50000 个缩到比如：

$$
5
$$

个 candidate。 再做精细 geometry。

### 7. 经典方法：Bag of Words

视觉 SLAM 历史上一个很重要的方法：

Bag of Visual Words

简称：

$$
BoW
$$

ORB-SLAM 系列非常经典地使用这一类思想。

### 8. Bag of Words 的直觉

自然语言里，一篇文章可以表示成：

> 它出现了哪些词，每个词出现多少次。

例如：

```
robot: 10
camera: 5
slam: 8
map: 6
```

不太关心这些词在文章中的精确位置。 视觉里做类似事情。

把很多 local descriptors：

$$
d_1,d_2,\dots,d_N
$$

映射成：

Visual Words

### 9. 什么是 Visual Word？

假设训练阶段收集了海量 ORB descriptors。 然后做聚类。

例如：

```
descriptor cluster 1 → word 1
descriptor cluster 2 → word 2
descriptor cluster 3 → word 3
...
```

于是一个 ORB descriptor：

$$
d
$$

可以被量化成：

$$
word_k
$$

一张图片里所有 descriptors 最后变成：

```
word 3
word 17
word 17
word 102
word 7
...
```

于是整张图可以表示成一个：

word histogram

### 10. 为什么这个表示适合快速检索？

因为两张图如果来自同一地点， 通常会看到类似的 local visual patterns。 所以它们的 visual word 分布会比较接近。

于是可以快速计算：

$$
score(K_t,K_j)
$$

找最像的历史 Keyframes。 这比对所有 descriptor 做完整精细匹配便宜很多。

### 11. Vocabulary Tree

实际 BoW 往往不会用一个平坦的大词典。

而会建立：

Vocabulary Tree

例如：

```
             root
          /   |   \
         /    |    \
       A      B     C
      / \    / \
    A1 A2  B1 B2
```

Descriptor 逐层比较， 最后落到某个 leaf word。 这样检索效率更高。

### 12. TF-IDF 为什么会出现？

有些 visual words 很常见。

比如大量场景都有：

- 普通墙角
- 窗框
- 重复纹理

这种 word 区分能力不强。 但某些 rare words 很有辨识度。

所以类似文本搜索里的：

$$
TF-IDF
$$

对常见 word 降权， 对稀有、区分度高的 word 增权。

核心思想：

不是所有视觉特征都有同样的 place-recognition 价值

### 13. BoW 只是在说“看起来像”

这一点特别重要。

如果：

$$
score(K_t,K_j)
$$

很高，

只能说：

> 当前图像和历史图像 appearance 很像。

不能直接说：

They are the same place 为什么？

因为有：

Perceptual Aliasing

## 感知混淆与几何验证

### 14. Perceptual Aliasing 是什么？

就是：

> 不同地点看起来很像。

例如长走廊：

```
门  门  门  门  门
```

另一个楼层：

```
门  门  门  门  门
```

视觉 appearance 可能非常接近。

还有：

- 地下停车场
- 办公室格子间
- 仓库货架
- 酒店走廊
- 高速公路
- 重复建筑外墙

这都会产生：

False Loop Candidate

### 15. False Positive 和 False Negative

Loop Recognition 有两种错误。

#### False Positive

实际上没来过，

但系统说：

> 来过。

这是：

假闭环

#### False Negative

实际上来过， 但系统没认出来。

这是：

漏闭环

### 16. 哪个更危险？

通常：

False Positive 更危险

漏掉一个 loop：

> 轨迹继续漂。

虽然不好，但系统通常还能工作。

错加一个 loop：

> 可能直接把整个地图拉坏。

所以 Loop Closure 的设计常偏向：

$$
\boxed{ High\ Precision > High\ Recall }
$$

也就是：

> 宁可少闭一些，也不能乱闭。

这是一个很重要的工程原则。

### 17. 为什么还要做 Geometric Verification？

Place Recognition 给 candidate：

$$
K_t\leftrightarrow K_j
$$

接下来真正问：

> 两张图里的 feature correspondence，能不能被同一个几何模型解释？

比如找到：

$$
100
$$

个 feature matches。

然后：

$$
RANSAC
$$

估计：

- Essential Matrix
- PnP Pose
- Sim(3)
- SE(3)

看有多少：

Inliers 支持这个 model。

### 18. 举个例子

BoW 觉得两个停车场图像非常像。

Feature matching 得到：

$$
120
$$

个 appearance matches。

但是进行几何验证后：

$$
8
$$

个 inliers。

这说明：

> 虽然视觉纹理相似，但这些 features 无法由一个合理相机变换同时解释。

所以：

$$
Reject
$$

### 19. 真 Loop 会是什么样？

假设两个 Keyframes 真的是同一地点。

Feature matches：

$$
150
$$

个。

RANSAC 后：

$$
110
$$

个 inliers。

而且这些点满足统一：

$$
SE(3)/Sim(3)
$$

几何。 那 confidence 就会很高。

于是：

$$
\boxed{ Appearance + Geometry }
$$

共同确认 Loop。

### 20. 为什么几何验证这么强？

因为 appearance coincidence 很容易。

但如果几十、上百个 feature 都满足：

同一个 R,t 就困难得多。

这意味着：

> 不仅“长得像”，整个空间结构也对应得上。

所以 geometry 是一个非常强的 consistency check。

### 21. Loop Closure 的几何问题是哪一类？

取决于系统。

#### Monocular

如果只有两个 2D images：

$$
2D-2D
$$

可以用：

Essential Matrix 但如果有已有 MapPoints，

也可能使用：

$$
3D-2D
$$

PnP。

#### Stereo / RGB-D

可以拥有：

$$
3D-3D
$$

correspondences。

于是求：

$$
SE(3)
$$

#### Monocular SLAM with scale drift

很多经典系统会估：

$$
Sim(3)
$$

因为需要同时检查 / 修正：

$$
Scale
$$

### 22. 为什么 ORB-SLAM 的 monocular loop 常关注 Sim(3)？

上一章已经讲了一部分。

因为单目地图长期可能：

scale drift

例如早期两个 Keyframes 认为距离：

$$
5
$$

个 arbitrary units。

后面漂成：

$$
5.5
$$

如果 loop 只用：

$$
SE(3)
$$

不能调整尺度。

所以使用：

$$
Sim(3): p'=sRp+t
$$

额外估：

$$
s
$$

## 连续一致性、重定位与地图融合

### 23. Loop Detection 为什么常使用连续一致性？

假设某一帧：

$$
K_{1000}
$$

突然说：

> K50 很像。

可能只是偶然。

如果接下来：

$$
K_{1001}
$$

也和：

$$
K_{51}
$$

相似，

然后：

$$
K_{1002}
$$

又和：

$$
K_{52}
$$

相似， 那就可信很多。

因为形成：

```
current sequence:
1000 → 1001 → 1002

history:
50   → 51   → 52
```

这是：

Temporal Consistency

### 24. 为什么序列一致性这么有效？

单张图片可能因为重复纹理误识别。 但连续多帧都恰好匹配到一段连续历史轨迹， 概率就低很多。

所以 Loop Closure 不一定只看：

one image

而会看：

sequence consistency

### 25. Spatial Consistency 也一样

如果 candidate Keyframe：

$$
K_{50}
$$

和当前很像，

而：

$$
K_{49},K_{51},K_{52}
$$

这些 covisible neighbors 也都匹配得上， 可信度会进一步提高。

所以可以利用：

Covisibility Graph 做 loop verification。 这又和 Chapter 41 接上了。

### 26. Loop Closure 不是一个独立孤岛

它会大量复用前面已有的信息：

- Keyframes
- Descriptors
- Covisibility Graph
- MapPoints
- Feature Matching
- PnP
- RANSAC

所以好的 SLAM 架构会让这些模块互相复用。

### 27. Loop Closure 和 Relocalization 为什么很像？

Relocalization 的问题：

> Tracking 丢了，我现在在哪？

Loop Closure：

> Tracking 没丢，但我是不是回到了以前的地点？

它们第一步几乎一样：

Current Image  →  Historical Place Retrieval

然后：

Feature Matching Geometric Verification

### 28. 两者区别在哪里？

#### Relocalization

目标：

Recover Current Pose 因为 Tracking 已经 lost。

#### Loop Closure

目标：

Discover a long-range constraint 当前 Pose 原本有 estimate， 只是可能 drift。 所以 Loop Closure 会纠正 graph。

### 29. 可以这样理解

Relocalization：

> “我迷路了，告诉我现在在哪。”

Loop Closure：

> “我知道自己大概在哪，但突然发现这里和以前一个地方是同一个，那我的历史轨迹可能漂了。”

这两者非常接近，但系统状态不同。

### 30. Loop Closure Accepted 以后发生什么？

假设：

$$
K_i
$$

和：

$$
K_j
$$

确认是 Loop。

得到了：

$$
Z_{ij}^{loop}
$$

接下来一般会：

第一，做局部 map / pose alignment。

第二，加入：

Loop Factor

第三，执行：

Pose Graph Optimization

第四，修正：

$$
Keyframes + MapPoints
$$

必要时：

第五，Global BA。

### 31. 为什么 Loop Closure 后地图会突然“跳一下”？

因为在 Loop 前：

trajectory 已经有 drift。 Loop factor 加入后， 优化会修改大量历史 Keyframe Poses。

可视化里就会看到：

> 整条轨迹突然收回来。

这不是 estimator 不稳定。

而是：

Global correction

### 32. MapPoint Fusion

Loop 后还有一个很重要的问题。

假设第一次经过某处，建立了一组 landmarks：

$$
A_1,A_2,A_3
$$

第二次绕回来时，因为之前不知道是同一地方，

又建立：

$$
B_1,B_2,B_3
$$

实际上：

$$
A_1=B_1
$$

$$
A_2=B_2
$$

……

所以 Loop Closure 后还应该：

Fuse duplicate MapPoints

### 33. 为什么不 Fusion 会怎样？

地图里会出现：

```
wall copy 1
wall copy 2
```

虽然轨迹拉回来了， 但同一个真实物体有两份 landmark representation。

这样会：

- 冗余
- association 混乱
- BA 约束割裂

所以 map fusion 很重要。

### 34. Map Fusion 实际上又是 Data Association

没错。

Loop Closure 后要回答：

> 当前区域的 MapPoint A 和历史区域的 MapPoint B，是不是同一个真实点？

所以：

Loop Closure 本质仍然大量依赖 Data Association 这件事从 Chapter 37 到现在一直没有消失。

### 35. 为什么说 Loop Closure 是“高层 Data Association”？

普通 Tracking：

$$
feature_t \leftrightarrow feature_{t+1}
$$

是在近邻时间做 association。

Loop Closure：

$$
place_t \leftrightarrow place_{t-10000}
$$

是在很长时间跨度做 association。

所以可以理解：

$$
\boxed{ Loop\ Closure = Long-term Data Association }
$$

这是一个非常好的统一视角。

## 长期变化与学习型检索

### 36. Tracking 为什么比 Loop Closure 容易？

Tracking 有一个很强 prior：

$$
T_t\approx T_{t-1}
$$

所以 feature 大概在哪都知道。

Loop Closure 中：

$$
K_t
$$

可能对应历史任何一个：

$$
K_j
$$

搜索空间大得多。

而且经过很长时间：

- 光照变化
- 视角变化
- 物体移动
- 季节变化
- 家具变化

所以 loop recognition 更难。

### 37. Viewpoint Change

同一个地点：

第一次：

```
Camera → building
```

第二次：

```
building ← Camera
```

视角差 180°。 两张图 appearance 可能差很多。 于是传统 local descriptors 可能很难匹配。

这会导致：

False Negative

### 38. Illumination Change

同一个地点：

白天：

$$
I_{day}
$$

晚上：

$$
I_{night}
$$

可能差异非常大。 所以 place recognition 如果严重依赖 raw appearance， 鲁棒性会下降。

### 39. Seasonal Change

尤其室外长期地图：

```
summer:
green trees

winter:
snow + bare trees
```

甚至同一地点可能完全不像。

这叫：

Appearance Change 长期 SLAM 特别难。

### 40. Dynamic Scene Change

办公室里：

- 椅子挪了
- 箱子没了
- 人很多
- 门开了/关了

但是几何地点仍然相同。

所以好的 Place Recognition 应该尽量找到：

Persistent place identity 而不是被短期物体状态完全支配。

### 41. Learned Place Recognition 为什么越来越重要？

传统 BoW 使用：

local handcrafted features

现代方法可以学习一个 global image descriptor：

$$
g(I)\in\mathbb R^D
$$

比如一张图片最后变成一个：

$$
512D
$$

或类似维度的向量。

然后做：

nearest neighbor search 找到相似地点。

代表思想包括：

- NetVLAD
- learned global descriptors
- modern retrieval transformers

具体模型名以后需要时再细讲。

### 42. Global Descriptor 和 Local Descriptor 不一样

Global descriptor：

$$
g(I)
$$

描述整张图。

主要用于：

Retrieval 也就是找候选 place。

Local descriptors：

$$
d_1,d_2,\dots
$$

描述局部 feature。

主要用于：

$$
\boxed{ Correspondence + Geometric\ Verification }
$$

所以现代 pipeline 往往还是：

```
Global Descriptor
      ↓
Candidate Retrieval
      ↓
Local Feature Matching
      ↓
Geometry
```

这个两级结构非常自然。

### 43. 为什么不用 Learned Retrieval 直接确认 Loop？

原因还是一样：

Appearance score 不是 geometry

再强的 global descriptor 也可能：

- 误认相似建筑
- 误认重复走廊
- 被场景 bias 影响

所以在高可靠 SLAM 系统里：

Geometric Verification 仍然非常重要

### 44. Loop Candidate Retrieval 本身也是 Search 问题

假设有：

$$
N
$$

个 historical keyframes。

每个都有 descriptor：

$$
g_i
$$

当前：

$$
g_t
$$

需要找：

$$
\arg\min_i d(g_t,g_i)
$$

大型地图可能用：

- inverted index
- approximate nearest neighbor
- hierarchical vocabulary
- vector database-like retrieval structures

目标都是：

不要 O(N) 地做昂贵比较

## 接受、延迟决策与异常回环

### 45. 为什么不能把最近几十帧当 Loop Candidate？

因为当前帧和最近帧当然很像。 但那不是 Loop。

例如：

$$
K_t
$$

和：

$$
K_{t-1}
$$

一定高度相似。 如果不排除 temporal neighborhood，

系统会每帧都认为：

> 闭环了！

所以 candidate retrieval 通常会排除：

$$
|t-j|<T_{min}
$$

的近期 Keyframes。

### 46. 这其实是在区分 Local Continuity 和 Long-term Return

相邻帧相似：

Tracking 很正常。

Loop Closure 关心：

Temporal distance large, spatial distance small

也就是：

> 时间上很远，空间上又回来了。

### 47. 一个完整 True Loop 需要哪些证据？

可以粗略想成四层：

#### Layer 1：Appearance

global similarity

#### Layer 2：Local Match

feature correspondence

#### Layer 3：Geometry

consistent pose transform

#### Layer 4：Context

例如：

- temporal consistency
- covisibility consistency
- neighboring keyframes support

证据层层增强。

### 48. 为什么 Loop Closure 要这么保守？

因为它是一个：

High leverage decision

一次正确 loop：

> 可以修正几百米 drift。

一次错误 loop：

> 也可以毁掉几百米地图。

所以系统不会因为：

$$
Similarity = 0.91
$$

就立刻闭环。 通常会用多种 evidence。

### 49. 从 Bayesian 角度怎么看？

我们实际上在判断两个 hypothesis：

$$
H_1: \text{same place}
$$

$$
H_0: \text{different place}
$$

根据：

- appearance
- geometry
- temporal context

更新：

$$
p(H_1|Z)
$$

只有足够高才接受。

这和 Part II 学过的：

Multi-hypothesis 本质一样。

### 50. 为什么“不确定时延迟决定”很合理？

假设当前 candidate 有点像， 但 geometry support 不够强。

不一定非要：

$$
Accept
$$

或：

Reject forever

可以等待：

$$
K_{t+1},K_{t+2}
$$

更多 evidence。 如果连续三帧都支持同一历史区域， 再接受。

这就是我们以前讲的：

Defer decision until more information

### 51. Loop Closure 和 Sequential Estimation 其实很一致

每一帧增加 evidence：

$$
Belief_{t} \rightarrow Belief_{t+1}
$$

所以 place recognition 并不一定必须是：

> 单帧 one-shot 分类。

也可以是：

Sequential Evidence Accumulation 这个思路非常普遍。

### 52. False Loop 被加入后能不能撤销？

一些系统可以。

最简单系统可能：

> 一加进去就永久存在。

更 robust 的系统可以：

- robust kernel
- switchable constraints
- dynamic covariance scaling
- loop hypothesis management

允许后续 evidence 发现：

> 这条 loop 不对。

然后弱化甚至禁用。

### 53. 为什么这比“永远相信第一次决定”合理？

因为 perception 本身有不确定性。 尤其 Loop Closure 是离散 Data Association。 一次 recognition score 不是绝对真理。

所以允许：

Hypothesis revision 是更加稳健的状态估计思想。

### 54. Loop Closure 和 Map Merge

假设机器人有两张独立建立的地图：

$$
Map_A
$$

和：

$$
Map_B
$$

如果发现：

$$
KF_A
$$

和：

$$
KF_B
$$

其实是同一个地点，

就可以求：

$$
T_{AB}
$$

然后把两张地图对齐、合并。

所以：

Map Merging 本质上和 Loop Closure 极其相似。

### 55. 区别只是在“是不是同一条轨迹”

Loop Closure：

> 同一 session 的过去和现在连起来。

Map Merge：

> 两个原本独立的 map components 连起来。

数学上都是：

$$
\boxed{ 发现两个 previously disconnected / weakly connected graph regions 之间的新约束 }
$$

### 56. Multi-Robot SLAM 也是类似

Robot A 地图：

$$
G_A
$$

Robot B 地图：

$$
G_B
$$

当它们发现共同地点：

$$
A_i\leftrightarrow B_j
$$

就得到：

Inter-Robot Loop 两张 Pose Graph 可以合成一个。 所以 Loop Closure 的思想其实非常通用。

### 57. Loop Closure 对 Map Drift 的修正不是魔法

它不能纠正所有问题。

如果从没回到已知地点：

No loop, no loop information 那系统仍然会漂。

所以 SLAM 并不是：

> 加了 Loop Closure 就永远不漂。

它只能在发生 revisit 时利用新的约束修正。

### 58. 如果环境本身没有可辨识特征呢？

比如：

- 超长重复走廊
- 空白墙
- 完全重复货架

Place Recognition 本身就很困难。

这时可能需要融合：

- LiDAR geometry
- IMU
- Wi-Fi / UWB
- GPS
- known markers
- semantic landmarks

来增强 place identity。

### 59. 为什么 Semantic Information 可能帮助 Loop Closure？

例如图像纹理变化很大，

但系统识别到：

```
elevator
fire door
room 301
stairs
```

这些高层语义可能比低层 texture 更稳定。

所以长期 SLAM 会越来越关注：

$$
\boxed{ Geometry + Appearance + Semantics }
$$

而不是只靠一种 signal。

### 60. 但 Semantic 也可能有 Alias

比如：

$$
100
$$

扇一模一样的门。 “door”这个 semantic label 完全不够定位。 所以语义只是额外 information， 不能自动解决 Data Association。

还是要结合：

- spatial arrangement
- context
- geometry

## 模块接口与完整流程

### 61. Loop Closure 的输出到底是什么？

不是：

$$
\boxed{ true/false }
$$

这么简单。

对 Backend 真正有价值的是：

$$
\boxed{ Candidate\ pair + Relative\ transform + Uncertainty }
$$

即：

$$
(i,j,Z_{ij},\Sigma_{ij})
$$

然后建立：

Loop Factor

### 62. Uncertainty 为什么还重要？

假设 loop geometry 很强：

$$
100
$$

个高质量 inliers， reprojection error 很小。

可以设置较强：

$$
\Omega_{loop}
$$

如果只有较弱几何支持， 应该更保守。 否则即使 loop 是真的， 过强的错误 covariance 也会让优化不合理。

所以：

Loop Detection 不只是判断有没有，还应该知道有多可信

### 63. 一个经典 Loop Closure Pipeline

可以记成：

```
1. Current Keyframe
        ↓
2. Compute retrieval representation
        ↓
3. Search historical candidates
        ↓
4. Exclude temporal neighbors
        ↓
5. Consistency filtering
        ↓
6. Local feature matching
        ↓
7. RANSAC geometric verification
        ↓
8. Estimate SE(3) / Sim(3)
        ↓
9. Check inlier count / residual
        ↓
10. Accept loop
        ↓
11. Add loop factor
        ↓
12. Pose graph optimization
        ↓
13. Map-point fusion / correction
```

这一整套才叫成熟的 Loop Closure。

### 64. 为什么 Place Recognition 和 Loop Closure 不应该画等号？

因为 Place Recognition 只完成：

Candidate generation

Loop Closure 真正完成的是：

Geometrically verified long-range state constraint 这是两个层级。

所以有人说：

> “NetVLAD 做 Loop Closure。”

严格来说，更准确应该说：

> NetVLAD 可以做 Loop Candidate Retrieval / Place Recognition。

最终闭环仍然需要系统其他环节。

### 65. 这和 Object Detection 很像

你可以类比一下。

一个 classifier 说：

> 图里可能有 car。

但最终机器人如果要规划，

通常还需要：

- bbox
- depth
- tracking
- geometry

一样。

Place Recognition 说：

> 这里可能以前来过。

但 SLAM 要真正使用，

还需要：

Geometric Relation

### 66. Loop Closure 和你的 Stereo 背景怎么联系？

Stereo 给你：

$$
metric\ 3D
$$

所以如果两个 historical/current stereo keyframes 匹配，

你可以拥有：

$$
3D\leftrightarrow3D
$$

对应。

然后直接估计：

$$
SE(3)
$$

这比纯 monocular 的尺度问题简单不少。 所以 stereo SLAM 的 Loop Geometry 往往更加直接。

### 67. 一个很好的统一理解

我们之前一直讲：

#### Tracking

short-term association

#### Local Mapping

medium-term association

#### Loop Closure

long-term association

所以整个 Visual SLAM 其实可以从一个角度理解成：

不断在不同时间尺度上解决 Data Association

### 68. Tracking 问

> 这个点是不是上一帧那个点？

### 69. Local Mapping 问

> 这个 observation 是不是 Local Map 里的那个 Landmark？

### 70. Loop Closure 问

> 当前这个地点是不是几千帧前那个地点？

从 point 到 place，

本质都是：

Identity Association 只是尺度不同。 这个理解我很推荐你记住。

### 71. Loop Closure 为什么是 SLAM 里最危险的模块之一？

因为它同时具备：

High uncertainty

和：

High global impact

普通 local measurement：

> 影响小，频率高。

Loop：

> 频率低，但一旦加入影响巨大。

所以它需要比普通 Tracking 更严格的 acceptance policy。

### 72. 本章最重要的八句话

第一：

$$
\boxed{ Loop\ Closure = Long-term\ Data\ Association }
$$

第二：

Place Recognition 只负责找 Candidate

第三：

Appearance Similarity  ≠  Same Place

第四：

必须经过：

Geometric Verification

第五：

False Positive 通常比 False Negative 更危险，所以：

Loop Closure 更重 Precision

第六：

真正输出给 Backend 的是：

Relative Pose Constraint

第七：

Loop Accepted 后：

$$
\boxed{ Pose\ Graph\ Optimization + Map\ Correction }
$$

第八：

Relocalization 和 Loop Closure 的前半部分非常像，但：

一个恢复当前 Pose，一个创建长期约束

> 整理说明：回环与重定位共享检索和验证能力，但回环建立跨历史状态的约束，重定位恢复当前状态与已有地图的关系。长期误差是否累积还取决于已有地图重观测与其他有效约束；没有显式回环模块，不等于必然只有纯 dead reckoning。

## 思考题

### Q1：为什么图像检索分数非常高，也不能直接加入 Loop Edge？

<details>

<summary>参考答案</summary>

因为高 retrieval score 只表示：

Appearance Similarity

而重复走廊、停车场、窗户等可能造成：

Perceptual Aliasing 只有经过 feature correspondence 和 geometric verification，

证明这些 observations 能被同一个：

$$
SE(3)/Sim(3)
$$

解释， 才应该形成 Loop Constraint。

</details>

### Q2：为什么 Loop Closure 宁可漏检一些，也不能过于激进？

<details>

<summary>参考答案</summary>

漏掉 loop：

Drift 暂时无法修正 但系统通常仍可继续运行。

错误 loop：

False long-range constraint 可能让全局 optimizer 扭曲整条轨迹和地图。

所以工程上通常更重视：

Precision

</details>

### Q3：为什么需要排除当前帧附近的历史帧？

<details>

<summary>参考答案</summary>

因为：

$$
K_t
$$

和：

$$
K_{t-1}
$$

本来就应该很像。 那属于 Tracking / Local Map 关系， 不是“长时间离开后再次回来”的 Loop。

所以需要：

temporal exclusion

</details>

### Q4：为什么连续多帧都支持同一个历史区域，比单帧高分更可靠？

<details>

<summary>参考答案</summary>

因为随机 appearance aliasing 可能发生一次。

但：

$$
K_t,K_{t+1},K_{t+2}
$$

连续对应：

$$
K_j,K_{j+1},K_{j+2}
$$

说明两段 trajectory 的 appearance 和 temporal structure 都一致。

所以：

Evidence 明显更强。

</details>

### Q5：Loop Closure 和 Relocalization 有什么本质区别？

<details>

<summary>参考答案</summary>

两者都可能：

Image  →  Place Retrieval  →  Feature Matching  →  Geometry

但：

Relocalization：

Tracking lost, recover current pose

Loop Closure：

Tracking alive, discover a new historical constraint

</details>

### Q6：为什么 Loop Closure 后还需要 MapPoint Fusion？

<details>

<summary>参考答案</summary>

因为同一地点第一次和第二次经过时， 可能分别创建两套 landmarks。

闭环只是确认：

> 两个区域其实是同一个地方。

还需要把重复：

MapPoints 重新 association / merge， 才能得到真正统一地图。

</details>

### Q7：为什么 Learned Place Recognition 也不能完全取代 Geometry？

<details>

<summary>参考答案</summary>

因为 neural descriptor 本质仍然是在解决：

$$
Similarity / Retrieval
$$

而 SLAM 最终需要：

Metric geometric relationship

即：

$$
R,t
$$

甚至：

$$
scale
$$

这些要通过 geometric constraints 得到。

</details>

### Q8：如果一个环境完全没有 Loop，SLAM 能不能做到永远不漂？

<details>

<summary>参考答案</summary>

一般不能。 如果没有任何新的绝对或长距离约束， 局部 odometry noise 会持续积累。

除非系统还有：

- GPS
- known global map
- beacon
- global landmark

等绝对 reference。

否则：

Drift is fundamentally unavoidable

</details>

## 相关章节与来源

- 上一章：[Pose Graph Optimization](pose-graph.md)
- 下一篇：[视觉／激光惯性状态估计](visual-lidar-inertial.md)
- 来源：本次新增 Part IV Chapter 46 课堂草稿；保留核心推理、例子与自测，删除聊天开场和重复课程预告。
