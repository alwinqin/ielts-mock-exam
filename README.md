# IELTS Mock Exam System — 雅思模拟考试系统

听说读写四项全功能雅思模拟考试系统，纯前端运行，无需后端服务器（口语转写除外）。

## 项目结构

```
ielts-reading-exam/
├── README.md                        # 本文件
├── HANDOVER.md                      # 项目移交文档
├── REQUIREMENTS_V1.0.md             # V1.0 需求说明
├── index.html                       # 入口页面
├── speech-server.py                 # 口语转写服务器 (Whisper)
├── run_qa.sh                        # 一键QA验证脚本
├── .github/workflows/ci.yml         # CI 自动验证流水线
├── css/
│   └── style.css                    # 全局样式 (~1200 行, CSS 变量体系)
├── js/
│   ├── app.js                       # 路由 + 主题切换 + 错误恢复
│   ├── i18n.js                      # 中英双语词库 (~191 键)
│   ├── data.js                      # localStorage 数据层
│   ├── data-bundle.js               # 自动生成, 内联全部 JSON (~1.6 MB, 支持 file://)
│   ├── timer.js                     # 计时器模块
│   ├── modal.js                     # 通用模态对话框
│   ├── cambridge-adapter.js         # 剑桥数据格式适配器
│   ├── exam.js                      # 阅读考试逻辑
│   ├── listening.js                 # 听力考试逻辑
│   ├── speaking.js                  # 口语考试逻辑
│   ├── writing.js                   # 写作考试逻辑
│   ├── review.js                    # 阅读答题回顾
│   ├── listening-review.js          # 听力答题回顾
│   ├── writing-review.js            # 写作答题回顾 + 自评表保存
│   ├── wrong-book.js                # 错题本 (筛选/掌握/重做)
│   ├── history.js                   # 历史统计
│   └── dashboard.js                 # 数据仪表盘 (Chart.js 图表)
├── e2e/
│   ├── validate-system.spec.js      # Playwright E2E (43 用例)
│   └── playwright.config.js         # Playwright 配置
├── data/
│   ├── test1~20.json                # 阅读题库 (各40题)
│   ├── listening/test1~10.json      # 听力题库 (各40题)
│   ├── writing/test1~10.json        # 写作题库 (Task1+Task2)
│   ├── speaking/test1~10.json       # 口语题库 (Part1/2/3)
│   ├── cambridge/cam14~cam20/       # 剑桥 IELTS 14-20 真题
│   ├── ground_truth/answer_keys.json # 编译答案键 (99.8% 验证率)
│   └── validation_reports/          # QA 验证报告归档
└── (听力音频文件在外置硬盘:
     /Volumes/EcommerceHDD/ielts-audio/listening/)
```

## 启动方式

### 必须: 主服务器
```bash
cd ~/ielts-reading-exam
python3 -m http.server 8080
```

### 可选: 口语转写服务器 (仅使用口语时需要)
```bash
cd ~/ielts-reading-exam
python3 speech-server.py
```

### 访问
浏览器打开 http://localhost:8080

## 功能说明

### 阅读 (Reading)
| 功能 | 说明 |
|------|------|
| 48套真题库 | 剑桥 IELTS 14-20 (28套) + 遗留测试 (20套), 每套3篇文章, 40题 |
| 题型 | TFNG, YNNG, 多选, 标题匹配, 信息匹配, 句子填空, 摘要填空 等13种 |
| 计时 | 60分钟倒计时, 超时自动提交 |
| 键盘快捷键 | `F` 键标记/取消标记题目 |
| 自动保存 | 答案和计时每30秒存localStorage |
| 评分 | 提交后自动评分, 雅思9分制 |
| 回顾 | 查看答案对比和解析(中英双语), 筛选(全部/仅错误/未答) |
| 错题本 | 按题型筛选, 标记已掌握, 重做模式 |

### 听力 (Listening)
| 功能 | 说明 |
|------|------|
| 38套真题库 | 剑桥 IELTS 14-20 (28套) + 遗留测试 (10套), 每套4个Section |
| 题型 | 表格填空, 多选, 句子完成, 简答, 匹配 等 |
| 音频 | 微软神经TTS (edge-tts) 英式/澳式发音, 支持 MP3/M4A/WMA |
| 流程 | 30秒预读 → 播放音频(可答题) → 手动进入下一Section |
| 变速播放 | 0.5x / 0.75x / 1.0x / 1.25x / 1.5x |
| 进度导航 | 进度点指示器显示各 Section 完成状态 |
| 填写时间 | 4个Section播放完后10分钟填写 |
| 评分 | 自动评分, band score 映射 |

### 写作 (Writing)
| 功能 | 说明 |
|------|------|
| 38套题 | 剑桥 IELTS 14-20 (28套) + 遗留测试 (10套), Task 1 + Task 2 |
| 字数统计 | 实时显示字数, 低于最低要求时变红警告 |
| 计时 | 60分钟, Task1/Task2 分栏切换 |
| 自动保存 | 每30秒存localStorage, beforeunload 防误退出 |
| 参考范文 | 提交后可对比参考范文 |
| 自评表 | 4项评分指标滑动条自评, 可保存到 localStorage |

### 口语 (Speaking)
| 功能 | 说明 |
|------|------|
| 38套题 | 剑桥 IELTS 14-20 (28套) + 遗留测试 (10套), Part 1/2/3 |
| 录音 | 浏览器 MediaRecorder API, 逐题独立录音 |
| 转写 | Whisper tiny 本地模型 (需启动 speech-server.py) |
| Part 1 | 4-5个问题, 逐题录音/回放 |
| Part 2 | 话题卡 + 1分钟准备倒计时 + 2分钟发言计时, 自动停止录音 |
| Part 3 | 3-4个延伸讨论问题 |

### 错题本 (Wrong Book)
| 功能 | 说明 |
|------|------|
| 自动收集 | 聚合所有阅读/听力尝试中的错题 |
| 题型筛选 | 按题型筛选 (多选, TFNG, 填空 等) |
| 掌握标记 | 标记"已掌握"持久化到 localStorage |
| 重做模式 | 单独重做任意错题 |
| 练习模式 | 按题型筛选后顺序刷题 |

### 数据仪表盘 (Dashboard)
| 功能 | 说明 |
|------|------|
| 技能雷达图 | 阅读/听力/写作/口语 四项 band score 对比 |
| 趋势折线图 | 历次 band score 走势 (阅读+听力双线) |
| 题型堆叠图 | 各题型正确/错误分布, 按准确率排序 |
| 统计卡片 | 总尝试次数, 平均分, 最高分, 总学习时长 |
| 自评数据 | 写作/口语自评分数自动接入雷达图 |

### 主题切换
- 浅色/深色双主题, CSS 自定义属性体系
- 自动检测系统 `prefers-color-scheme`
- Header 主题切换按钮, localStorage 持久化

### QA 验证管线
```bash
bash run_qa.sh          # 一键运行全量验证 (Python + bundle + E2E)
bash run_qa.sh --quick  # 仅 Python 验证
bash run_qa.sh --full   # 含 Playwright E2E
```
- 三层验证: Pre-commit → CI Pipeline → 定期深度审计
- Python 数据验证 + 答案键快照对比 + Playwright E2E (43 用例)
- GitHub Actions CI 自动运行

## 技术栈
- 纯前端 HTML/CSS/JS (无框架, 零生产依赖)
- SPA 架构, hash 路由 (18 个 JS 模块)
- 所有数据存储在 localStorage (按模块前缀分区)
- 中英双语界面 (~191 翻译键, `t()` 函数渲染)
- CSS 自定义属性体系 (浅色/深色双主题)
- 听力音频: edge-tts 微软神经TTS, 支持变速播放
- 口语转写: OpenAI Whisper (本地 tiny 模型)
- 离线支持: `data-bundle.js` 内联全部数据, 支持 file:// 协议
- 数据仪表盘: Chart.js CDN
- E2E 测试: Playwright (43 用例)
- QA 管线: Python 验证脚本 + 答案键快照对比 + CI 自动化

## 在其他电脑上运行

### 方式1: 直接拷贝 (无需音频)
项目是纯静态文件，直接拷贝整个文件夹到任何电脑：
```bash
cp -r ~/ielts-reading-exam /U盘或移动硬盘/path
```
然后在目标电脑上运行:
```bash
cd path/ielts-reading-exam
python3 -m http.server 8080
```

### 方式2: 需要听力音频
听力音频存储在 `/Volumes/EcommerceHDD/ielts-audio/listening/`，需要一起拷贝。
音频文件是 MP3 格式，外置硬盘有 870GB 可用空间。

### 方式3: 需要口语转写
speech-server.py 依赖 Python 和 whisper：
```bash
pip3 install openai-whisper
python3 speech-server.py
```

## 需要我帮助 Debug 或完善时

随时打开这个项目目录，运行以下命令启动服务器:
```bash
cd ~/ielts-reading-exam && python3 -m http.server 8080
```

然后告诉我具体的问题或想新增的功能。
