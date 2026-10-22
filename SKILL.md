---
name: ivdr-classification-codes
label: IVDR分类与代码分析
description: "为体外诊断（IVD）产品输出 EU IVDR 分类、IVR/IVS/IVT/IVP/IVD 代码、EMDN 代码及认证路径判断（扩证 vs 新增 Group）。Use when the user asks for: IVDR classification of an IVD product (Class A/B/C/D), IVR code assignment, EMDN code lookup, MDCG 2020-16 classification rules, MDCG 2021-14 IVR codes, EUDAMED registration codes, or whether a new IVD item can be added to an existing CE certificate (scope extension) vs needs a new group. Typical inputs: product intended use (e.g. chemiluminescence immunoassay for a biomarker), analyte name, product family. Triggers: 产品分类、IVDR分类、IVR代码、EMDN代码、扩证、CE证书范围、体外诊断注册、classification of IVD, EMDN lookup, IVR code."
---

# IVDR 分类与代码分析

为 IVD 产品输出完整的欧盟注册前置分析：IVDR 分类、IVR 代码、横向代码（IVS/IVT/IVP/IVD）、EMDN 代码，以及认证路径判断。

## 工作流总览

1. **确认产品预期用途**（从用户描述或产品 IFU/表格中提取）
2. **判定 IVDR 分类**（读 `references/classification-rules.md`）
3. **赋 IVR 主代码 + 横向代码**（读 `references/ivr-codes.md`）
4. **查 EMDN 代码**（跑 `scripts/search_emdn.py`，需 EMDN Excel）
5. **判断认证路径**（扩证 vs 新增 Group）
6. **按标准模板输出**（见下）

## 第一步：确认产品预期用途

从用户输入提取以下要素（缺则问或做合理假设并在输出中声明）：

- **分析物**（analyte）：如 sST2、anti-HAV、H.pylori IgG、Dengue NS1
- **方法学**：如 CLIA、ELISA、NAT、快速检测
- **样本类型**：血清/血浆/全血/尿液/脑脊液等
- **目标疾病/状态**：心衰、AMI、感染、癌症筛查等
- **使用者**：实验室专业人员 / 自测 / 近患者
- **预期用途声明原文**：特别注意"筛查（screening）"、"监测（monitoring）"、"辅助诊断（aid in diagnosis）"等关键词

## 第二步：判定 IVDR 分类

读 `references/classification-rules.md`，按决策树逐条核对：

1. Rule 1/2（Class D：献血筛查、血型）
2. Rule 3(a)-(m)（Class C）——**重点核对 3(b) 血液/脑脊液传染原检测（排除抗体）、3(g) 疾病分期、3(h) 癌症筛查、3(j) 监测调整患者管理、3(k) 危及生命疾病管理**
3. Rule 4（自测→C；近患者→按预期用途）
4. Rule 5（通用实验室/仪器/容器→A）
5. Rule 6（兜底→B）

**关键分水岭**：抗体检测 vs 抗原/核酸检测（传染原本身）——前者通常 B（Rule 6），后者通常 C（Rule 3b/c）。预期用途声明（如"胃癌筛查"）可改变分类。

## 第三步：赋 IVR 主代码 + 横向代码

读 `references/ivr-codes.md`：

- **主 IVR**：按 2017/2185 列表顺序取第一个适用代码（如 0301 癌症、0503 传染原、0602 特定疾病生理标志物等）
- **横向代码**：
  - IVS 1007（含赋值质控品/校准品时）
  - IVS 1008（含仪器）/ IVS 1010（含软件）
  - IVT 2005 + 2006（生物技术+化学处理制造，免疫试剂常用）
  - IVP 3007（免疫分析）或按方法学
  - IVD 4008（免疫学）+ 学科代码（4012 病毒学 / 4001 细菌学等）

## 第四步：查 EMDN 代码

需要 EMDN 最新版 Excel（用户提供或从任务资源获取）：

```bash
# 按关键词搜索（支持多关键词 AND）
python3 scripts/search_emdn.py <emdn.xlsx> "ST2" "cardiac"
python3 scripts/search_emdn.py <emdn.xlsx> "dengue"

# 查看某代码的完整层级路径
python3 scripts/search_emdn.py <emdn.xlsx> --path W01021314
```

要点：
- 选 **terminal=YES 的终端代码**
- 记录完整层级路径（如 W01 试剂 → W0105 传染病 → …）
- 同一分析物可能只有一个通用终端项（如 DENGUE VIRUS 未细分 NS1/IgG/IgM），三个产品共用同一 EMDN 代码
- 配套代码：质控品（如 W010508xxxx）、校准品（如 W01050809xx）、仪器（W02010201 全自动免疫分析仪）

## 第五步：判断认证路径（扩证 vs 新增 Group）

判断逻辑（输出时必须明确说明）：

1. **代码维度**：新产品 IVR 代码是否已包含在既有 CE 证书的 NB 授权范围内？
   - 同一 IVR 代码组（如都属 0503 传染原）→ 扩证可行
   - 不同 IVR 代码组（如新增 0301 癌症 vs 现有 0602 心脏标志物）→ 需先与 NB 确认扩展授权
2. **技术维度**：是否引入新技术/新工艺代码（IVT/IVP）？同平台（如 iFlash CLIA）则不引入。
3. **分类维度**：新产品分类是否落在既有证书覆盖的分类范围内？Class C 证书通常覆盖 B/C。
4. **结论**：大概率扩证 → 说明需向 NB 确认的点（IVR 授权范围、condition/limitation）。

## 输出模板（严格遵循）

```markdown
## {产品名} — IVDR 分类与代码分析

**产品定位：** {从预期用途提取的一句话摘要}

---

### 一、IVDR 分类：**Class {A/B/C/D}**

**依据规则：**
- {Rule X} — {规则要点}（{MDCG 2020-16 rev.5 第 X 页示例/依据}）
- {排除说明：为何不适用更高/更低规则}

### 二、IVR 代码（2017/2185，MDCG 2021-14）

**主代码：IVR {XXXX}** — {定义}
- {适用性论证}
- {排除代码说明}

**横向代码：**
| 代码 | 内容 | 适用性 |
|---|---|---|
| IVS 1007 | 带赋值质控品 | 适用/不适用 |

### 三、EMDN 代码（v2026）

| 层级 | EMDN 代码 | 术语 | 适用对象 |
|---|---|---|---|
| ... | **WXXXXXXXXX** | ... | 主代码 |

路径：{完整层级}

### 四、认证路径判断：{扩证优先 / 需确认 / 新增 Group}

**判断逻辑：** {代码维度/技术维度/分类维度逐条}

**结论：** {明确结论}

**需向 NB 确认：** {列出确认点}

---

**依据来源：**
- MDCG 2020-16 rev.5（{日期}）：{引用要点}
- MDCG 2021-14（{日期}）：{引用要点}
- EMDN v{年份}：{代码}

> 说明：以上为法规分析结论；IVR 最终赋码由公告机构确认，EMDN 按最终产品组成在 EUDAMED 注册时填报。
```

## 注意事项

- **不编造**：EMDN 代码必须从实际 Excel 中查得；分类必须有 MDCG 规则/示例依据；找不到就说明，不猜测。
- **预期用途驱动**：分类完全取决于预期用途声明，用户描述与 IFU 不一致时以 IFU 为准并向用户指出差异。
- **配套代码按需**：校准品/质控品/仪器是否在注册单元内，决定 IVS/IVT/IVP 及 EMDN 配套代码是否列出。
- **多项产品批量处理**：逐项输出独立记录，不合并、不省略。
