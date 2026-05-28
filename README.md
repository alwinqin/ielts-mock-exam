# IELTS Mock Exam System — 雅思模拟考试系统

听说读写四项全功能雅思模拟考试系统，纯前端运行，无需后端服务器（口语转写除外）。

## 项目结构

```
ielts-reading-exam/
├── README.md                        # 本文件
├── index.html                       # 入口页面
├── speech-server.py                 # 口语转写服务器 (Whisper)
├── css/
│   └── style.css                    # 全局样式
├── js/
│   ├── app.js                       # 路由 + 状态管理
│   ├── i18n.js                      # 中英双语词库
│   ├── data.js                      # localStorage 数据层
│   ├── timer.js                     # 计时器模块
│   ├── exam.js                      # 阅读考试逻辑
│   ├── listening.js                 # 听力考试逻辑
│   ├── speaking.js                  # 口语考试逻辑
│   ├── writing.js                   # 写作考试逻辑
│   ├── review.js                    # 阅读答题回顾
│   ├── listening-review.js          # 听力答题回顾
│   ├── writing-review.js            # 写作答题回顾
│   └── history.js                   # 历史统计
├── data/
│   ├── test1~10.json                # 阅读题库 (各40题)
│   ├── listening/test1~10.json      # 听力题库 (各40题)
│   ├── writing/test1~10.json        # 写作题库 (Task1+Task2)
│   └── speaking/test1~10.json       # 口语题库 (Part1/2/3)
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
| 10套真题库 | 每套3篇文章, 40题 |
| 题型 | TFNG, 多选, 标题匹配, 句子完成, 简答 |
| 计时 | 60分钟倒计时 |
| 自动保存 | 答案和计时每30秒存localStorage |
| 评分 | 提交后自动评分, 雅思9分制 |
| 回顾 | 查看答案对比和解析(中英双语) |
| 历史 | 练习记录, 错题本, 薄弱题型分析 |

### 听力 (Listening)
| 功能 | 说明 |
|------|------|
| 10套真题库 | 每套4个Section, 各10题 |
| 题型 | 表格填空, 多选, 句子完成, 简答 |
| 音频 | 微软神经TTS (edge-tts) 英式/澳式发音 |
| 流程 | 30秒预读 → 播放音频(可答题) → 下一Section |
| 音频文件 | 存储在外置硬盘 /Volumes/EcommerceHDD/ielts-audio/listening/ |
| 填写时间 | 4个Section播放完后10分钟填写 |
| 评分 | 自动评分 |

### 写作 (Writing)
| 功能 | 说明 |
|------|------|
| 10套题 | Task 1 + Task 2 |
| 计时 | 60分钟, Task1/Task2 分栏切换 |
| 字数统计 | 实时显示字数 |
| 自动保存 | 每30秒存localStorage |
| 参考范文 | 提交后可对比参考范文 |
| 自评表 | 4项评分指标滑动条自评 |

### 口语 (Speaking)
| 功能 | 说明 |
|------|------|
| 10套题 | Part 1/2/3 完整流程 |
| 录音 | 浏览器 MediaRecorder API |
| 转写 | Whisper tiny 本地模型 (需启动 speech-server.py) |
| Part 1 | 4-5个问题, 逐题录音 |
| Part 2 | 话题卡 + 1分钟准备倒计时 + 录音 |
| Part 3 | 3-4个延伸讨论问题 |

## 技术栈
- 纯前端 HTML/CSS/JS (无框架)
- 所有数据存储在 localStorage
- SPA 架构, hash 路由
- 中英双语界面, 一键切换
- 听力音频: edge-tts 微软神经TTS
- 口语转写: OpenAI Whisper (本地 tiny 模型)

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
