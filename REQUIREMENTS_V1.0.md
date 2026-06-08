# 雅思模拟考试系统 V1.0 — 需求说明

## 1. 项目概述

### 1.1 项目定位

面向雅思考生的离线可用、全真模拟考试平台。覆盖阅读、听力、写作、口语四大模块，收录 Cambridge IELTS 14–20（学术类）全部真题数据，支持中英文双语界面。

### 1.2 核心目标

- 提供与真实雅思考试一致的答题体验（计时、题型、流程）
- 自动评分并生成雅思 band score（1–9 分制）
- 错题收集与针对性练习
- 数据仪表盘追踪学习进度
- 离线可用（通过 file:// 协议无需服务器）

### 1.3 技术边界

| 项目 | 选型 |
|------|------|
| 架构 | 纯前端 SPA，客户端渲染 |
| 路由 | Hash-based（`#/`） |
| 数据 | 静态 JSON + localStorage 持久化 |
| 依赖 | 零生产依赖（仅 Chart.js CDN 用于图表） |
| 离线 | 通过 `data-bundle.js` 内联全部数据支持 file:// |
| 语音 | 可选 Flask + Whisper 服务（口语转写） |

---

## 2. 功能模块

### 2.1 阅读考试

**考试流程：**
- 60 分钟倒计时，超时自动提交
- 左侧文章面板 + 右侧题目面板，支持段落间跳转
- 每篇文章 13–14 题，共 3 篇文章 40 题

**支持的题型（13 种）：**

| 题型 | 类型标识 | 交互方式 |
|------|----------|----------|
| TRUE/FALSE/NOT GIVEN | `tfng` | 三选一按钮 |
| YES/NO/NOT GIVEN | `ynng` | 三选一按钮 |
| 单选题 | `multiple_choice` | 单选按钮 (A/B/C/D) |
| 多选题 | `multiple_choice_multi` | 复选框 |
| 段落标题匹配 | `matching_headings` | 下拉选择 (i–x) |
| 信息匹配 | `matching_info` | 下拉选择 (A–G) |
| 句子匹配 | `matching_sentence` | 下拉选择 |
| 人名匹配 | `matching_names` | 下拉选择 |
| 句子填空 | `sentence_completion` | 文本输入 |
| 摘要填空 | `summary_completion` | 文本输入 |
| 笔记填空 | `notes_completion` | 文本输入 |
| 表格填空 | `form_completion` | 文本输入 |
| 简答题 | `short_answer` | 文本输入 |

**评分与回顾：**
- 自动对比用户答案与正确答案
- 生成雅思 band score（40 题 → 9 分制映射表）
- 回顾页面：逐题展示用户答案 vs 正确答案，附带中英文解析
- 支持筛选（全部 / 仅错误 / 未答）

### 2.2 听力考试

**考试流程（模拟真实考试）：**
1. 30 秒预览阶段（不可答题）
2. 音频播放阶段（可答题）
3. 阶段结束自动切换
4. 全部 4 个部分完成后 → 10 分钟答案转写阶段
5. 阶段导航使用进度点指示器

**额外功能：**
- 变速播放（0.5x / 0.75x / 1.0x / 1.25x / 1.5x）
- 内联音频播放器（每部分独立播放）
- 支持 4 种音频格式（MP3 / M4A / WMA / 备用路径）

**评分与回顾：**
- 40 题自动评分，生成 band score
- 回顾页面：按部分统计正确率，逐题对比

### 2.3 写作考试

**考试流程：**
- 60 分钟计时器
- Task 1（150 词，20 分钟建议）+ Task 2（250 词，40 分钟建议）
- 实时字数统计
- 自动保存（每 30 秒）+ beforeunload 拦截防误退出

**回顾与自评：**
- 并排展示用户写作与参考范文
- 四项标准自评滑块（1–5 分）：
  - Task Achievement（任务完成度）
  - Coherence & Cohesion（连贯与衔接）
  - Lexical Resource（词汇资源）
  - Grammatical Range & Accuracy（语法范围与准确性）

**写作题型分类（14 种）：**

| Task 1 | Task 2 |
|--------|--------|
| bar_chart / line_graph / pie_chart | opinion_essay |
| table / mixed_chart | discussion_essay |
| map_comparison / process_diagram | advantage_disadvantage |
| | problem_solution / two_part_question |
| | positive_negative_development / direct_question |

### 2.4 口语考试

**考试流程：**
- **Part 1**（4–5 题）：逐题显示，支持录音 / 回放 / 转写
- **Part 2**（话题卡片）：
  - 1 分钟准备倒计时
  - 2 分钟发言倒计时，计时结束自动停止录音
  - 显示话题提示要点
- **Part 3**（延伸讨论）：按主题分组的问题列表

**录音功能：**
- 使用浏览器 MediaRecorder API
- 每道题独立录音，支持回放
- 可选转写（需启动 `speech-server.py`，调用 Whisper）

### 2.5 错题本

- 聚合所有阅读和听力尝试中的错题
- 按题型筛选（多选题 / TFNG / 填空题等）
- 标记"已掌握"（persist 到 `localStorage('mastered_wrong_questions')`）
- 两种练习模式：
  - **重做模式**：单独重做任意错题
  - **练习模式**：按题型筛选后顺序刷题
- 显示题型统计（正确率 / 已掌握 / 待复习）

### 2.6 历史记录

- 展示所有尝试记录（测试名称、日期、分数、band score、用时）
- 支持清除全部历史（带确认对话框）

### 2.7 数据仪表盘

使用 Chart.js 渲染，自动聚合 localStorage 中所有考试数据：

| 图表 | 类型 | 内容 |
|------|------|------|
| 技能对比 | 雷达图 | 阅读 / 听力 / 写作 / 口语 band score 对比 (自动收集) |
| 分数趋势 | 折线图 | 历次阅读+听力 band score 走势 (双线) |
| 题型表现 | 堆叠条形图 | 各题型正确/错误分布 (按准确率排序) |

统计卡片：总尝试次数、平均 band score、最高 band score、总学习时长

- 写作自评分数从 `writing_state_*` localStorage 键自动收集
- 口语自评分数从 `speaking_state_*` localStorage 键自动收集
- 空数据时显示引导提示

### 2.8 主题切换

- 浅色 / 深色双主题，CSS 自定义属性体系 (设计令牌)
- 切换按钮，持久化到 `localStorage('ielts_theme')`
- 自动检测系统 `prefers-color-scheme`，用户手动选择优先
- 深色主题完整覆盖所有组件（含预览徽章、转写区域等边缘场景）

### 2.9 国际化 (i18n)

- 中英文双语（约 191 个翻译键）
- 语言切换按钮，持久化到 `localStorage('ielts_lang')`
- 使用 `data-i18n` 属性标记可翻译元素

---

## 3. 数据架构

### 3.1 数据目录结构

```
data/
├── test1.json ~ test20.json              # 遗留阅读测试
├── listening/test1.json ~ test10.json    # 遗留听力测试
├── listening/audio/                      # MP3 音频 (44 文件)
├── writing/test1.json ~ test10.json      # 遗留写作测试
├── writing/cam14_test1.json ~ cam20_test4.json  # 剑桥写作 (28 文件)
├── speaking/test1.json ~ test10.json     # 遗留口语测试
├── speaking/cam14_test1.json ~ cam20_test4.json # 剑桥口语 (28 文件)
├── cambridge/
│   ├── audio/                            # 剑桥听力音频 (MP3)
│   ├── cam14/ ~ cam20/                   # 各书阅读/听力/写作/口语 JSON
│   └── pdf/                              # 原始剑桥 PDF 文件
├── ground_truth/
│   └── answer_keys.json                  # 编译答案键 (477 KB)
└── validation_reports/                   # QA 验证报告 + 答案键快照
```

### 3.2 答案验证体系

**answer_keys.json** 包含所有剑桥题目的规范答案：

```json
{
  "answers": {
    "cam17": {
      "listening": {
        "test1": {
          "1": {
            "answer": "litter",
            "extracted": "litter",
            "confidence": "high",
            "type": "form_completion",
            "source": "vlm_verified"
          }
        }
      }
    }
  }
}
```

**置信度层级：**
| 级别 | 含义 | 验证方式 |
|------|------|----------|
| `high` | 已通过多源交叉验证 | VLM 提取 + JSON 对比一致 |
| `medium` | 单一来源提取 | 仅 OCR 或仅 VLM |
| `low` | 未经验证 | 仅存在 JSON 中 |

**验证统计（V1.0 终态）：**
- 总答案数：2,240
- 已验证 (high)：2,236 (99.8%)
- 未验证 (json_only)：4 (cam20 残留)

---

## 4. 收录内容

### 4.1 Cambridge IELTS 系列

| 书籍 | 阅读 | 听力 | 写作 | 口语 | 状态 |
|------|------|------|------|------|------|
| Cam 14 | 4 套 (160 题) | 4 套 (160 题) | 4 套 | 4 套 | 完整 |
| Cam 15 | 4 套 (160 题) | 4 套 (160 题) | 4 套 | 4 套 | 完整 |
| Cam 16 | 4 套 (160 题) | 4 套 (160 题) | 4 套 | 4 套 | 完整 |
| Cam 17 | 4 套 (160 题) | 4 套 (160 题) | 4 套 | 4 套 | 完整 |
| Cam 18 | 4 套 (160 题) | 4 套 (160 题) | 4 套 | 4 套 | 完整 |
| Cam 19 | 4 套 (160 题) | 4 套 (160 题) | 4 套 | 4 套 | 完整 |
| Cam 20 | 4 套 (160 题) | 4 套 (160 题) | 4 套 | 4 套 | 完整 |

**合计：28 套真题，1,120 道阅读题 + 1,120 道听力题**

### 4.2 遗留测试

- 阅读：20 套独立测试（test1–test20）
- 听力：10 套独立测试（test1–test10）
- 写作：10 套独立测试
- 口语：10 套独立测试

---

## 5. 技术实现

### 5.1 前端架构

```
index.html                         # SPA 入口
css/style.css                      # 全局样式 (~1200 行, CSS 变量体系)
js/
├── app.js                         # 路由、主题切换、错误恢复、测试选择页
├── data-bundle.js                 # 自动生成，内联全部 JSON 数据 (~1.6 MB)
├── data.js                        # localStorage 持久化层 + band score 映射
├── modal.js                       # 通用模态对话框 (焦点锁定, ESC 关闭)
├── timer.js                       # 倒计时器组件
├── cambridge-adapter.js           # 剑桥数据格式 → 应用格式适配
├── i18n.js                        # 中英文国际化 (~191 键) + formatTypeName
├── exam.js                        # 阅读考试渲染与评分 (键盘快捷键 F)
├── listening.js                   # 听力考试渲染与评分 (变速播放, ARIA)
├── listening-review.js            # 听力回顾
├── review.js                      # 阅读回顾 (筛选, 解析)
├── writing.js                     # 写作考试 (字数警告, beforeunload)
├── writing-review.js              # 写作回顾与自评保存
├── speaking.js                    # 口语考试（含录音/回放/转写）
├── wrong-book.js                  # 错题本 (筛选/掌握/重做/练习)
├── history.js                     # 历史记录
└── dashboard.js                   # 数据仪表盘 (Chart.js, 自评数据收集)
```

### 5.2 路由表

| Hash | 页面 |
|------|------|
| `#/` | 测试选择页（阅读/听力/写作/口语 四选项卡） |
| `#/exam/:id` | 阅读考试 |
| `#/review/:id` | 阅读回顾 |
| `#/listening-exam/:id` | 听力考试 |
| `#/listening-review/:id` | 听力回顾 |
| `#/writing-exam/:id` | 写作考试 |
| `#/writing-review/:id` | 写作回顾 |
| `#/speaking-exam/:id` | 口语考试 |
| `#/dashboard` | 数据仪表盘 (Chart.js 图表) |
| `#/history` | 历史记录 (搜索/筛选/导出) |
| `#/wrong-book` | 错题本 (筛选/掌握/重做/练习) |

### 5.3 离线运行

`bundle_data.py` 扫描 `data/` 目录，将所有 JSON 文件打包为 `js/data-bundle.js`：

```javascript
window.__DATA_BUNDLE__ = {
  reading: { ... },      // 所有阅读测试
  listening: { ... },    // 所有听力测试
  writing: { ... },      // 所有写作测试
  speaking: { ... },     // 所有口语测试
  cambridge: { ... }     // 剑桥书籍数据
};
```

应用检测 `file://` 协议时自动回退到数据包模式，无需 HTTP 服务器即可运行。

### 5.4 评分映射表

40 题原始分 → 雅思 band score（学术类阅读/听力通用）：

| 原始分 | Band | 原始分 | Band |
|--------|------|--------|------|
| 39–40 | 9.0 | 23–25 | 6.0 |
| 37–38 | 8.5 | 20–22 | 5.5 |
| 35–36 | 8.0 | 16–19 | 5.0 |
| 33–34 | 7.5 | 13–15 | 4.5 |
| 30–32 | 7.0 | 10–12 | 4.0 |
| 27–29 | 6.5 | | |

### 5.5 E2E 测试

- 框架：Playwright 1.52
- 测试文件：`e2e/validate-system.spec.js`（~900 行，13 个测试组，43 个测试用例）
- 覆盖范围：应用外壳、阅读/听力/写作/口语模块、跨模块集成、深色模式、无障碍、模态框、仪表盘、错题本空状态、错题本数据操作、i18n 持久化、skip-link 可见性
- 运行：`npx playwright test e2e/ --config=e2e/playwright.config.js`

### 5.6 QA 验证管线

三层自动化验证体系：

```
Layer 1: Pre-commit (秒级)
  └─ validate_all.py --quick  → 阻止 CRITICAL 提交

Layer 2: CI Pipeline (分钟级)
  └─ validate_all.py → audit.py → bundle_data.py → E2E
  └─ check_data_regression.py (答案键快照对比)

Layer 3: 定期深度审计 (周级)
  └─ 全量 VLM 交叉验证抽查
  └─ i18n 覆盖率报告
  └─ localStorage 配额监控
```

**一键运行：**
```bash
bash run_qa.sh           # 全量验证
bash run_qa.sh --quick   # 仅 Python 验证
bash run_qa.sh --data-only # 仅数据验证
```

**工具链：**
| 工具 | 功能 |
|------|------|
| `run_qa.sh` | 一键 QA 编排脚本（彩色输出） |
| `validate_all.py` | 全量数据结构、答案一致性校验 |
| `audit.py` | 项目级审计（生成 audit_report.json） |
| `bundle_data.py` | 离线数据包生成 + 大小检查 (< 2MB) |
| `check_data_regression.py` | 答案键快照对比，防止回归 |
| `.github/workflows/ci.yml` | GitHub Actions 自动 CI |

---

## 6. 数据质量保障

### 6.1 答案提取流水线

```
剑桥官方 PDF → PyMuPDF 渲染 → Qwen3.6-27B VLM 识别
                                    ↓
                          answer_keys.json 编译
                                    ↓
                          JSON 交叉验证 (98%+ 准确率)
                                    ↓
                          标记置信度 (high/medium/low)
```

### 6.2 验证工具链

| 工具 | 功能 |
|------|------|
| `validate_all.py` | 全量数据结构、答案一致性校验 |
| `audit.py` | 项目级审计（生成 audit_report.json） |
| `cross_validate_fix.py` | 跨测试交叉验证修正 |
| `benchmark_qwen_ocr.py` | VLM 识别准确率基准测试 |

### 6.3 已知限制

- 口语评分依赖用户自评（无自动发音评估）
- 写作评分依赖用户自评（无自动作文批改）
- 听力音频为 MP3 文件，首次加载可能有延迟
- 口语转写需额外启动 Python 服务

---

## 7. 运行环境

| 项目 | 要求 |
|------|------|
| 浏览器 | Chrome/Firefox/Safari/Edge 现代版本 |
| HTTP 服务器 | 可选（支持 file:// 直接打开） |
| Python | 3.9+（仅口语转写服务需要） |
| Node.js | 仅 E2E 测试需要 |
| 存储 | localStorage（约 5–10 MB 用于历史数据） |

---

## 8. 版本历史

| 版本 | 日期 | 内容 |
|------|------|------|
| V1.0 | 2026-06 | 初始完整版本：Cam 14–20 全模块收录、中英双语、深色模式、错题本、仪表盘、离线支持、99.8% 答案验证率 |
| V1.1 | 2026-06 | 8-Phase 全面优化：安全加固（XSS 修复/模态框/beforeunload）、i18n 100% 覆盖（191 键）、无障碍（skip-link/ARIA/触控）、UX 增强（spinner/错误恢复/写作警告/键盘快捷键）、代码质量（var→const/事件清理）、功能增强（写作自评保存/仪表盘自评数据/变速播放）、QA 管线（43 E2E/CI/快照对比）、Dark Mode 完善（系统偏好检测） |

### V1.1 新增/修改文件

| 文件 | 状态 | 说明 |
|------|------|------|
| `js/modal.js` | 新增 | 通用模态对话框 (焦点锁定, ESC 关闭, aria-modal) |
| `js/wrong-book.js` | 新增 | 错题本 (筛选/掌握/重做/练习) |
| `js/dashboard.js` | 新增 | 数据仪表盘 (Chart.js 雷达图/折线图/堆叠图) |
| `run_qa.sh` | 新增 | 一键 QA 验证脚本 |
| `.github/workflows/ci.yml` | 新增 | GitHub Actions CI 配置 |
| `check_data_regression.py` | 新增 | 答案键快照回归检测 |
| `e2e/validate-system.spec.js` | 扩展 | 37 → 43 测试用例 |
| `js/i18n.js` | 扩展 | 160 → 191 翻译键, 提取共享 formatTypeName |
| `js/listening.js` | 重构 | var→let/const, 硬编码→t(), ARIA 补充 |
| `js/app.js` | 扩展 | 主题系统检测, 错误重试, spinner 加载 |
| `js/exam.js` | 扩展 | 键盘快捷键, ARIA tabpanel |
| `js/writing.js` | 扩展 | 字数警告, beforeunload 保护 |
| `js/writing-review.js` | 扩展 | 自评滑块持久化保存 |
| `js/speaking.js` | 修复 | FormData Blob 发送, beforeunload 清理 |
| `css/style.css` | 扩展 | CSS 变量完善, dark mode, spinner, skip-link, 触控 |
