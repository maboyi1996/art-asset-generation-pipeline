# PDF Prop Templates

These templates come from the user's verified art SOP and must be used for prop Step 8 analysis and Step 9 main image prompt generation.

## Prop Analysis Template

```markdown
# 道具小传模板 V1

## 1. 道具基础信息
道具名称：
状态名：
所属剧本 / 集数：
首次出现场景：
主要使用者：
关联角色：
所属空间：
一句话定位：

例：
不是“普通手机”，而是“Luna 在高奢晚宴中寻找 Michael 的情绪锚点”。

---

## 2. 剧本证据摘录
只摘剧本中直接支持道具判断的内容。

首次出现：
-

具体动作：
-

相关对白：
-

与角色关系：
-

与剧情转折关系：
-

---

## 3. 道具剧情功能
这个道具为什么重要？

推动剧情：
-

暴露人物：
-

制造误会 / 冲突：
-

强化空间：
-

视觉记忆点：
-

---

## 4. 道具所属角色
这个道具属于谁，或者最能代表谁？

主要归属角色：
使用者：
被影响者：
道具体现的角色特质：
道具与角色关系：

---

## 5. 道具外观设计
这一部分给美术用，必须具体。

尺寸：
形状：
颜色：
材质：
新旧程度：
使用痕迹：
精致程度：
品牌 / 阶层感：
危险性 / 亲密性 / 日常性：
是否需要特写：

---

## 6. 道具与场景关系
道具不是悬浮物，要知道它放在哪里。

所在场景：
摆放位置：
周围环境：
光线影响：
材质反光：
是否被角色持握：
是否与其他道具组合出现：

---

## 7. 镜头表现方式
这个道具应该怎么拍？

适合景别：
- 特写 / 极近特写 / 中景 / 静物主图

适合角度：
- 俯拍 / 侧拍 / 手持视角 / 桌面静物 / 镜面反射

适合光线：
-

适合情绪：
-

画面重点：
-

---

## 8. 美术执行重点
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

## 9. 后续生图准备词库
道具类型关键词：
材质关键词：
颜色关键词：
使用痕迹关键词：
场景关键词：
镜头关键词：
氛围关键词：
负面关键词：
```

## Prop Main Image Prompt Template

```text
[道具名称], isolated prop main reference image, clean white background, single object only, no environment, no people, no hands, no text, no visible brand logo. The image must prioritize story accuracy and high material quality.

This prop belongs to [角色 / 场景 / 世界观]. It should be fully separated from the original environment, but still preserve its story-specific state: [剧情状态 / 使用痕迹 / 阶层感 / 角色归属].

The prop is [准确道具类型], not [容易跑偏的错误类型]. It should include [核心结构 1], [核心结构 2], [核心结构 3], [必须可见部件], and [体现用途或身份的细节].

Core story details that must appear:
- [剧情必需细节 1]
- [剧情必需细节 2]
- [剧情必需细节 3]

Material quality:
[材质 1] should look [质感要求],
[材质 2] should show [反光 / 纹理 / 使用痕迹],
[材质 3] should feel [新旧程度 / 保养状态],
with realistic surface detail, believable scale, correct material thickness, physically plausible reflection behavior, and no plastic or fake CGI texture.

Condition:
[全新 / 使用过但保养好 / 陈旧 / 破损 / 被污染 / 被临时使用后的状态]. The condition must match the story, not a generic product catalog.

Composition:
centered product-reference composition, [角度], full object visible, enough padding around the prop, [视觉中心] as the main anchor, [必须可见部件] clearly visible. Clean natural shadow underneath is allowed, but no environment reflection.

Lighting:
soft neutral studio lighting, clean white background, controlled highlights on [反光材质], visible detail in [深色材质]. The lighting should reveal material texture clearly, not create dramatic scene mood.

Visual style:
real isolated prop reference photograph, realistic material texture, believable scale and material thickness, correct reflection behavior, practical and believable, clean but not stylized, not PBR product render, not commercial luxury advertisement.

Photographic realism guard:
real isolated prop reference photograph, believable scale, correct material thickness, physically plausible reflection behavior, natural wear or condition matching the story, soft neutral lighting, natural shadow under the object, no PBR product render, no luxury catalog polish, no environment reflections, no hands, no extra objects, no readable text, no watermark.

Avoid:
[原剧情环境],
[人物 / 手],
[text, watermark, visible brand logo],
[错误道具类型],
[错误材质],
[错误状态],
[错误时代 / 用途 / 风格],
random extra objects,
dramatic scene lighting,
environment reflections,
PBR product render,
luxury catalog polish,
plastic surfaces,
fake CGI look,
cartoon style,
anime style,
unreadable shape.
```
