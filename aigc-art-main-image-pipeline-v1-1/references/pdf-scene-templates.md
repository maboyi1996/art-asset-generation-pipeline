# PDF Scene Templates

These templates come from the user's verified art SOP and must be used for scene Step 8 analysis and Step 9 main image prompt generation.

## Scene Analysis Template

```markdown
# 场景小传模板 V1

## 1. 场景基础信息
场景名称：
状态名：
剧本场次：
时间：
地点层级：
所属世界 / 阶层：
首次出现剧情：
一句话定位：

---

## 2. 剧本证据摘录
只摘剧本里直接支持场景判断的内容，不自由发挥。

场景标题证据：
-

空间描述证据：
-

道具 / 陈设证据：
-

灯光 / 色彩证据：
-

声音 / 氛围证据：
-

角色行为证据：
-

---

## 3. 场景核心功能
这个场景在剧情里承担什么作用？

剧情功能：
-

人物功能：
-

关系功能：
-

情绪功能：
-

视觉记忆点：
-

---

## 4. 空间定位
这个场景到底是什么？不要只写“房间”。

空间类型：
空间级别：
公开 / 私密：
日常 / 非常规：
真实用途：
表面感觉：
隐藏含义：

---

## 5. 空间结构与动线
美术需要知道角色怎么进入、怎么移动、哪里是视觉中心。

入口：
过渡区：
主空间：
视觉中心：
角色行动路线：
上下层关系：
可见区域：
不可见但需要暗示的区域：

---

## 6. 场景元素清单
把画面里应该出现的东西拆出来。

建筑结构：
-

墙面：
-

地面：
-

天花：
-

家具：
-

核心道具：
-

装饰物：
-

可移动物件：
-

背景细节：
-

---

## 7. 材质与质感
这个场景靠什么材质建立质感？

主材质：
-

辅助材质：
-

反光 / 透明 / 柔软 / 冷硬材质：
-

不能使用的材质：
-

---

## 8. 灯光与色彩
时间和情绪如何通过光体现？

主光源：
辅助光：
明暗关系：
色彩倾向：
逆光位置：
阴影区域：
整体色调：
不能出现的光线方向：

---

## 9. 氛围关键词
这些给美术看的词，不要太文学化。

基础氛围：
-

情绪压力：
-

空间温度：
-

危险感来源：
-

等级感来源：
-

---

## 10. 场景与角色关系
这个空间如何反衬人物？

谁属于这个空间：
谁不属于这个空间：
角色进入后的状态：
空间对角色的压迫：
空间暴露了哪个角色的秘密：
空间推动了哪段关系变化：

---

## 11. 美术执行重点
画这个场景时最不能丢的东西。

必须保留：
-

可以变化：
-

不能出现：
-

最重要的视觉反差：
-

一眼识别点：
-

---

## 12. 后续生图准备词库
这里只做词库，不写完整提示词。

场景类型关键词：
空间结构关键词：
材质关键词：
灯光关键词：
氛围关键词：
核心道具关键词：
负面关键词：
```

## Scene Main Image Prompt Template

```text
[场景名称], [场景类型] inside [大地点 / 建筑级别] at [时间]. Main scene reference image, no characters unless required by the scene. The image must prioritize story accuracy and high material quality.

This scene belongs to [剧本世界观 / 阶层 / 角色归属]. It should clearly communicate [剧情功能 / 场景定位], while still working as a high-quality main visual reference for later angle expansion.

The camera is positioned [镜头位置], looking into [主空间] from / through [入口、门、走廊、窗、帘幕等]. The composition should reveal the main spatial layout clearly: [入口关系], [主空间], [视觉中心], [背景结构]. The adjacent space may appear only if it helps explain the story geography.

The room / location must be [准确空间身份], not [容易跑偏的错误空间]. It should include [建筑结构], [墙面], [地面], [天花], [主要固定设施], [家具], [关键装饰], and [体现阶层 / 职业 / 用途的元素].

Core story elements that must appear:
- [剧情必需元素 1]
- [剧情必需元素 2]
- [剧情必需元素 3]
- [剧情必需元素 4]

These elements should be integrated naturally into the scene, not scattered randomly. They must support the story identity of the location without turning the image into a messy action still.

Material quality:
[主材质 1] should look [质感要求],
[主材质 2] should show [反光 / 纹理 / 新旧程度],
[主材质 3] should feel [高级感 / 使用感 / 温度],
with realistic surface details, believable scale, and no plastic or fake CGI texture.

Lighting:
[主光源], [辅助光源], [色温], [明暗关系]. The lighting should support [剧情情绪] and reveal the material texture clearly. Avoid lighting that makes the scene look like [错误风格].

Mood:
[氛围关键词 1], [氛围关键词 2], [氛围关键词 3], [剧情心理感受]. The scene should feel [剧情正确气质], not [错误气质].

Composition:
cinematic [画幅比例] main scene image, high production value, readable spatial layout, strong visual anchor, detailed but not cluttered, no generic stock-photo look.

Visual style:
cinematic realism, [项目风格], high-end production design, realistic materials, controlled lighting, sharp but natural detail, immersive scene quality.

Avoid:
[错误地点], [错误阶层], [错误材质], [错误灯光], [错误风格], [错误时代 / 地域], unrelated props, random clutter, low-quality texture, plastic surfaces, fake CGI look, cartoon style, anime style, watermark, readable text, visible brand logos.
```
