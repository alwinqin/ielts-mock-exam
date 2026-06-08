# IELTS Mock Exam — Project Handover

## 项目背景

一个纯前端的雅思模拟考试系统，覆盖听说读写四项。用户通过浏览器访问，所有数据存储在 localStorage。

## 需求到开发的全过程

### 阶段一：阅读模块 (Reading)
- 用户需求：雅思阅读模拟考试，10套真题库
- 技术选型：纯前端 HTML/CSS/JS，无框架无构建工具
- 数据格式：JSON 静态题库，每套3篇文章40题
- 功能：60分钟倒计时、答案自动保存到 localStorage、提交自动评分(雅思9分制)、答题回顾、历史统计、错题本
- 交互：SPA hash 路由（`#/exam/test1`, `#/review/test1`, `#/history`）
- 中英双语：i18n 词库方案，`t()` 函数渲染

### 阶段二：听力模块 (Listening)
- 需求：10套听力题，4个Section共40题，模拟真实考试流程
- 音频：用户要求用本地语音引擎 → 发现系统 TTS 不自然 → 改用 edge-tts（微软神经TTS）
- 流程重写：30秒预读 → 播放音频答题 → 手动进入下一Section → 全部完成后10分钟填写
- 已修复 Bug：Section 标签显示不全（`S section` → `Section`）、底部操作栏不显示（`listeningFooter` div 丢失）、`renderListeningSectionContent` 函数不存在

### 阶段三：写作模块 (Writing)
- 需求：10套写作题，Task 1（图表描述）+ Task 2（议论文）
- 功能：60分钟计时、Task1/Task2 分栏切换、字数统计、自动保存、参考范文对比、自评表
- 已修复 Bug：标题"雅思阅读模拟考试"→"雅思模拟考试"、模板字符串嵌套乱码

### 阶段四：口语模块 (Speaking)
- 需求：10套口语题，Part 1/2/3 完整流程
- 录音：浏览器 MediaRecorder API
- 转写：发现本机安装了 openai-whisper 和 whisper-cli → 用 Python 创建 speech-server.py
- 功能：逐题录音、播放回听、Whisper 转写文字

## 架构总览

### 路由
| Hash | 功能 |
|------|------|
| `#/` | 首页，选择试题 |
| `#/exam/testN` | 阅读考试 |
| `#/review/testN` | 阅读回顾 |
| `#/listening-exam/testN` | 听力考试 |
| `#/listening-review/testN` | 听力回顾 |
| `#/writing-exam/testN` | 写作考试 |
| `#/writing-review/testN` | 写作回顾 |
| `#/speaking-exam/testN` | 口语考试 |
| `#/dashboard` | 数据仪表盘 |
| `#/history` | 历史统计 |
| `#/wrong-book` | 错题本 |

### 数据层 (data.js)
所有数据操作函数集中在 data.js，按模块前缀区分 localStorage key：
- 阅读：`exam_state_`, `user_answers_`, `flagged_`, `timer_`
- 听力：`listening_state_`, `listening_answers_`, `listening_flagged_`, `listening_timer_`
- 写作：`writing_state_`, `writing_answers_`, `writing_current`
- 口语：`speaking_state_` (自评数据持久化)
- 通用：`attempt_history`, `listening_attempt_history`, `mastered_wrong_questions`, `ielts_theme`, `ielts_lang`

### i18n 机制
- i18n.js 定义 `en` 和 `zh` 两个词库 (~191 翻译键)
- `t(key, params)` 函数根据 `i18n.currentLang` 返回对应语言文本
- 切换语言：`switchLang('en'|'zh')` 重新渲染所有 `data-i18n` 属性
- 共享 `TYPE_LABELS` 常量和 `formatTypeName(type)` 函数

### 计时器
- timer.js 提供通用 Timer 对象，用于阅读60分钟倒计时
- 听力有自己的计时逻辑（预读30秒 + Section 播放 + 填写10分钟）
- 写作有自己的60分钟计时，字数统计低于最低要求时警告

### 主题系统
- CSS 变量体系支持浅色/深色双主题
- `data-theme` 属性在 `<html>` 上切换
- `localStorage('ielts_theme')` 持久化
- 自动检测 `prefers-color-scheme` 系统偏好

## 关键文件入口函数

| JS 文件 | 入口函数 | 说明 |
|---------|---------|------|
| exam.js | `renderExam(testData)` | 渲染阅读考试页面 |
| listening.js | `renderListeningExam(testData)` | 渲染听力考试页面 |
| writing.js | `renderWritingExam(testData)` | 渲染写作考试页面 |
| speaking.js | `renderSpeakingExam(testData)` | 渲染口语考试页面 |
| review.js | `renderReview(testData, attempt, container)` | 阅读回顾 |
| listening-review.js | `renderListeningReview(testData, attempt, container)` | 听力回顾 |
| writing-review.js | `renderWritingReview(testData, container)` | 写作回顾 + 自评保存 |
| wrong-book.js | `renderWrongBook(container)` | 错题本 (筛选/掌握/重做) |
| dashboard.js | `renderDashboard(container)` | 数据仪表盘 (Chart.js) |
| history.js | `renderHistoryPage(container)` | 历史统计 |
| modal.js | `showModal(options)` | 通用模态对话框 |
| cambridge-adapter.js | `adaptCambridgeTest(data)` | 剑桥数据格式适配 |
| app.js | `App.init()` | 应用启动入口, 主题切换, 错误恢复 |

## 已知问题和遗留事项

### 听力
- [ ] 音频播放完后不会自动触发 `ended` 事件跳转 → 现在是手动点击 Next Section
- [ ] 如果外置硬盘没挂载，音频静默跳过（已处理 `onAudioError`）
- [ ] edge-tts 生成的音频还是机器合成音，想更自然可以用 OpenAI TTS API

### 口语
- [ ] speech-server.py 只在本地运行，需要浏览器能访问 localhost:8081
- [ ] 没有保存口语录音到本地磁盘
- [ ] 转写结果没有持久化（刷新页面丢失）

### 通用
- [ ] 所有数据存在 localStorage，清除浏览器数据会丢失全部进度
- [ ] 没有用户登录/多用户支持
- [ ] 阅读/听力的 Redo 按钮在工作，写作/口语还没有
- [ ] 可以用 nw.js 或 Electron 打包成桌面应用

## V1.1 已解决的问题

以下问题已在 8-Phase 优化中修复：

### 安全
- [x] XSS 漏洞：所有 `innerHTML` 用户数据均经过 `escapeHtml()` 转义
- [x] beforeunload 保护：写作/口语未提交时拦截刷新/关闭，提交后移除监听
- [x] alert/confirm 替换为自定义 modal（焦点锁定, ESC 关闭, aria-modal）

### 国际化
- [x] 听力模块 20+ 硬编码字符串 → 全部提取到 i18n.js (191 键)
- [x] `formatTypeName()` 统一提取为共享函数

### 主题与无障碍
- [x] Dark Mode：CSS 变量体系完善，`prefers-color-scheme` 自动检测
- [x] 跳过导航链接 (skip-link)
- [x] ARIA 属性：tab/tabpanel 角色, aria-label, aria-controls
- [x] 触控优化：按钮最小 40px 触控区域

### UX
- [x] CSS spinner 加载动画 + 错误重试按钮
- [x] 写作字数不足时红色警告
- [x] 键盘快捷键 `F` 键标记题目
- [x] 听力变速播放 (0.5x–1.5x) + 进度点导航

### 代码质量
- [x] `listening.js` 中 10 处 `var` → `let`/`const`
- [x] 事件监听器清理 (beforeunload, 音频事件)
- [x] localStorage 配额检查 + 历史记录上限

### 功能增强
- [x] 写作自评滑块持久化保存到 localStorage
- [x] Part 2 演讲计时器自动停止录音
- [x] 仪表盘写作/口语自评数据接入雷达图
- [x] 口语 FormData 修复 (Blob 发送)

## 项目文件 (80+ 个)

```
ielts-reading-exam/
├── README.md                        # 使用说明
├── HANDOVER.md                      # 本文件 - 项目移交文档
├── REQUIREMENTS_V1.0.md             # V1.0 需求规格说明
├── index.html                       # 入口页面
├── speech-server.py                 # 口语转写服务器 (Whisper)
├── run_qa.sh                        # 一键 QA 验证脚本
├── .github/workflows/ci.yml         # GitHub Actions CI 配置
├── css/style.css                    # 全局样式 (~1200 行, CSS 变量体系)
├── js/
│   ├── app.js                       # 路由 + 主题切换 + 错误恢复
│   ├── i18n.js                      # 中英双语词库 (~191 键)
│   ├── data.js                      # localStorage 数据层
│   ├── data-bundle.js               # 离线数据包 (自动生成, ~1.6 MB)
│   ├── timer.js                     # 计时器模块
│   ├── modal.js                     # 通用模态对话框
│   ├── cambridge-adapter.js         # 剑桥数据格式适配器
│   ├── exam.js                      # 阅读考试
│   ├── listening.js                 # 听力考试
│   ├── speaking.js                  # 口语考试
│   ├── writing.js                   # 写作考试
│   ├── review.js                    # 阅读回顾
│   ├── listening-review.js          # 听力回顾
│   ├── writing-review.js            # 写作回顾 + 自评保存
│   ├── wrong-book.js                # 错题本
│   ├── history.js                   # 历史统计
│   └── dashboard.js                 # 数据仪表盘 (Chart.js)
├── e2e/
│   ├── validate-system.spec.js      # Playwright E2E (43 用例)
│   └── playwright.config.js         # Playwright 配置
├── data/
│   ├── test1~20.json                # 阅读题库
│   ├── listening/test1~10.json      # 听力题库
│   ├── writing/test1~10.json        # 写作题库
│   ├── speaking/test1~10.json       # 口语题库
│   ├── cambridge/cam14~cam20/       # 剑桥 IELTS 14-20 真题
│   ├── ground_truth/answer_keys.json # 编译答案键 (99.8% 验证率)
│   └── validation_reports/          # QA 验证报告归档
└── data/listening/audio/            # 听力音频 (外置硬盘)
```

## 在任意电脑运行

```bash
# 1. 解压项目
unzip ielts-mock-exam.zip

# 2. 启动主服务器
cd ielts-reading-exam
python3 -m http.server 8080

# 3. 可选：启动口语转写
pip3 install openai-whisper
python3 speech-server.py

# 4. 浏览器打开
open http://localhost:8080
```

## 如果新的 Claude Code 要接管

1. **先读这个文件** — 了解项目全貌
2. **运行服务器查看效果** — `python3 -m http.server 8080`
3. **运行 QA 验证** — `bash run_qa.sh --quick` 确认系统完好
4. **看具体 JS 文件** — 入口函数如上表，从 app.js 开始追踪路由
5. **建议先改一个简单的** — 比如修改 i18n 词条或样式，熟悉流程
6. **改完运行 QA** — 每次改动后 `bash run_qa.sh` 确保零回归
7. **memory 系统** — 本文件对应的 memory 文件在 `.claude/projects/*/memory/` 下，记录了开发过程中的所有决策和 Bug 修复
