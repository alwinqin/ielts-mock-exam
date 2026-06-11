# IELTS Mock Exam System — 雅思模拟考试系统

听说读写四项全功能雅思模拟考试系统，支持 Web 浏览器和 Tauri 桌面应用。

## 项目结构

```
ielts-reading-exam/
├── README.md
├── index.html                       # 入口页面
├── speech-server.py                 # 口语转写服务器 (Whisper)
├── setup-audio.sh                   # 音频文件设置脚本
├── build-www.sh                     # Tauri 前端构建脚本
├── run_qa.sh                        # 一键QA验证脚本
├── bundle_data.py                   # 数据打包脚本
├── validate_all.py                  # 数据结构验证
├── audit.py                         # 项目审计
├── check_data_regression.py         # 答案键回归检测
├── .github/workflows/ci.yml         # CI 自动验证流水线
├── css/
│   └── style.css                    # 全局样式 (CSS 变量体系)
├── js/
│   ├── app.js                       # 路由 + 主题切换 + 事件代理
│   ├── i18n.js                      # 中英双语词库 (~199 键)
│   ├── data.js                      # localStorage 数据层
│   ├── data-bundle.js               # 自动生成, 内联全部 JSON (~1.6 MB)
│   ├── timer.js                     # 计时器模块
│   ├── modal.js                     # 通用模态对话框
│   ├── exam.js                      # 阅读考试逻辑
│   ├── listening.js                 # 听力考试逻辑
│   ├── speaking.js                  # 口语考试逻辑
│   ├── writing.js                   # 写作考试逻辑
│   ├── review.js                    # 阅读答题回顾
│   ├── listening-review.js          # 听力答题回顾
│   ├── writing-review.js            # 写作答题回顾 + 自评表保存
│   ├── wrong-book.js                # 错题本 (筛选/掌握/重做)
│   ├── history.js                   # 历史统计
│   ├── dashboard.js                 # 数据仪表盘 (Chart.js)
│   └── vendor/
│       └── chart.min.js             # Chart.js 本地副本
├── e2e/
│   ├── validate-system.spec.js      # Playwright E2E (50 用例)
│   └── playwright.config.js         # Playwright 配置
├── data/
│   ├── cambridge/cam14~cam20/       # 剑桥 IELTS 14-20 真题
│   ├── ground_truth/answer_keys.json # 编译答案键 (99.8% 验证率)
│   └── validation_reports/          # QA 验证报告归档
├── src-tauri/                       # Tauri v2 桌面应用 (Rust)
│   ├── Cargo.toml
│   ├── tauri.conf.json
│   ├── src/
│   │   ├── lib.rs                   # Rust backend + Tauri commands
│   │   └── main.rs                  # 应用入口
│   └── icons/                       # 应用图标
└── data/cambridge/audio/            # 听力音频文件 (需手动设置)
```

## 启动方式

### Web 浏览器
```bash
python3 -m http.server 8899
```
浏览器打开 http://localhost:8899

### Tauri 桌面应用
```bash
npm ci
npx tauri dev     # 开发模式
npx tauri build   # 生产构建 (生成 .dmg / .msi)
```

### 可选: 口语转写服务器
```bash
python3 speech-server.py
```

### 听力音频设置
剑桥听力音频文件受版权保护，需自行设置：
```bash
bash setup-audio.sh /path/to/your/audio/files
```

## 功能说明

### 阅读 (Reading)
- 28 套剑桥 IELTS 14-20 真题，每套 3 篇文章，40 题
- 题型：TFNG, YNNG, 多选, 标题匹配, 信息匹配, 句子填空, 摘要填空 等 13 种
- 60 分钟倒计时，超时自动提交
- 键盘快捷键 `F` 标记/取消标记题目
- 自动保存答案和计时 (localStorage, 每 30 秒)
- 自动评分，雅思 9 分制

### 听力 (Listening)
- 28 套剑桥 IELTS 14-20 真题，每套 4 个 Section
- 真实剑桥音频，支持 MP3 格式
- 流程：30 秒预读 → 播放音频 → 手动进入下一 Section
- 变速播放：0.5x / 0.75x / 1.0x / 1.25x / 1.5x
- 4 个 Section 播放完后 10 分钟填写时间

### 写作 (Writing)
- 28 套剑桥 IELTS 14-20 真题，Task 1 + Task 2
- 实时字数统计，低于最低要求时变红警告
- 60 分钟计时，Task1/Task2 分栏切换
- 参考范文对比 + 4 项评分指标自评表

### 口语 (Speaking)
- 28 套剑桥 IELTS 14-20 真题，Part 1/2/3
- 浏览器 MediaRecorder API，逐题独立录音
- Whisper tiny 本地模型转写 (需启动 speech-server.py)
- Part 2: 话题卡 + 1 分钟准备 + 2 分钟发言计时

### 错题本
- 聚合所有阅读/听力错题
- 按题型筛选、标记掌握、重做模式、练习模式
- 数据持久化到 localStorage

### 数据仪表盘
- 技能雷达图 (听说读写四项 band score)
- 趋势折线图 (历次 band score 走势)
- 题型堆叠图 (各题型正确/错误分布)
- 统计卡片 (总次数, 平均分, 最高分, 学习时长)

### 主题切换
- 浅色/深色双主题，CSS 自定义属性体系
- 自动检测系统 `prefers-color-scheme`
- localStorage 持久化

### QA 验证管线
```bash
bash run_qa.sh          # 一键运行全量验证
bash run_qa.sh --quick  # 仅 Python 验证
bash run_qa.sh --full   # 含 Playwright E2E
```
- 三层验证: Pre-commit → CI Pipeline → 定期深度审计
- Python 数据验证 + 答案键快照对比 + Playwright E2E (50 用例)
- GitHub Actions CI 自动运行

## 技术栈
- 纯前端 HTML/CSS/JS (无框架，零生产依赖)
- SPA 架构，hash 路由 (17 个 JS 模块)
- 所有数据存储在 localStorage (按模块前缀分区)
- 中英双语界面 (~199 翻译键, `t()` 函数渲染)
- CSS 自定义属性体系 (浅色/深色双主题)
- Tauri v2 桌面应用 (Rust + WKWebView/WebView2)
- 口语转写: OpenAI Whisper (本地 tiny 模型)
- 离线支持: `data-bundle.js` 内联全部数据, 支持 file:// 协议
- 数据仪表盘: Chart.js (本地副本, 无 CDN 依赖)
- E2E 测试: Playwright (50 用例)
- QA 管线: Python 验证脚本 + 答案键快照对比 + CI 自动化

## 在其他电脑上运行

### 直接拷贝
项目是纯静态文件（除音频外），直接拷贝整个文件夹：
```bash
cp -r ielts-reading-exam /destination/path
cd /destination/path
python3 -m http.server 8899
```

### 听力音频
运行 `bash setup-audio.sh` 检查音频状态。剑桥音频文件需从合法来源自行获取。

### 口语转写
```bash
pip3 install openai-whisper
python3 speech-server.py
```
