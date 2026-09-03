# README 视觉资产

本目录只服务仓库说明，不随运行时 Skill 加载。图片之外的正文完整保留使用步骤、判断方法和书目，图片不可见时仍可阅读。

| 文件 | 来源与格式 | 用途 |
| --- | --- | --- |
| [studio-hero.png](studio-hero.png) | 2026-09-03 使用内置 image_gen 生成；2172 × 724 PNG，约 2.5 MB | 从建筑线稿到城市与景观的概念插画；无第三方参考图 |
| [concept-to-space.svg](concept-to-space.svg) | 本项目原创、可编辑 SVG；1200 × 620 | 合成教学示意：共享主张如何变成空间动作与验证 |

两幅图均不代表真实场地、学生项目、测量、性能或合规证据。SVG 中的文字有正文说明和替代文本；未嵌入外部字体、脚本或远程图片。修改关系图时直接编辑 SVG，避免维护多个内容不一致的截图。

## 封面生成提示词

使用内置 `image_gen`，未使用 CLI 生图或外部图片。最终生成提示词如下：

```text
Use case: stylized-concept. Asset type: original GitHub README editorial hero for an open-source architecture, urban planning and landscape design studio coach. Create a refined architectural publication illustration, panoramic 3:1 composition. One continuous miniature spatial study connects a small open courtyard building, a walkable urban street edge and a terraced planted waterside landscape. Progress from delicate graphite site-contour and plan lines at one end into a precise warm-white physical architectural maquette toward the middle, with a restrained sage green tree canopy and pale blue-grey water toward the other. Tiny understated human silhouettes convey approachable everyday scale. A few translucent tracing-paper layers imply iteration and careful study, not technology spectacle. Warm off-white paper background, subtle grain, soft daylight, charcoal fine linework, sage and muted rust accents. Sophisticated quiet composition, generous breathing room, strong clear silhouette at small size, no excessive detail. Pure image: no lettering, no labels, no captions, no typography, no logos, no watermarks, no border. This is an illustrative learning scene, not a rendering of a real site or a technical performance diagram.
```
