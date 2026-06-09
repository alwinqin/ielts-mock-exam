# Changelog

## [2.0.0] — Unreleased (Tauri Desktop Edition)

### Added
- **Tauri Desktop Application**: macOS (.dmg) and Windows (.msi) support
- **Whisper.cpp Sidecar**: Offline speech transcription via Rust backend
- **Transcribe Interface Abstraction**: Tauri native > HTTP server > Web Speech API fallback chain
- **Local Chart.js**: Vendored chart.min.js, no CDN dependency
- **Autonomous CI/CD Pipeline**: 3-layer validation (pre-commit / CI push / scheduled audit)
- **Desktop CI Builds**: GitHub Actions for macOS universal + Windows MSVC
- **Pre-commit Hook**: Blocks commits with CRITICAL data issues
- **Scheduled Deep Audit**: Daily automated quality checks + issue management
- **Quality Dashboard**: Automated quality metrics generation
- **App Window Configuration**: minWidth 1024, minHeight 600

### Changed
- **Environment Detection**: Added `isTauri` flag alongside `isFileProtocol`
- **Audio Path Resolution**: Tauri resource_dir for desktop, relative paths for web
- **Data Loading**: `isFileProtocol || isTauri` condition for bundle usage
- **CSP Headers**: Proper Content-Security-Policy for Tauri WebView

### Security
- CSP defined in tauri.conf.json (script-src, connect-src, media-src)
- No external CDN dependencies at runtime
- Audio files served from Tauri resources (not external paths)

---

## [1.1.0] — 2026-06-09 (8-Phase V1.1 Optimization)

### Added
- **Modal System** (js/modal.js): ESC close, focus trap, aria-modal
- **Wrong Book** (js/wrong-book.js): Filter, master, redo, practice modes
- **Dashboard** (js/dashboard.js): Radar, line, stacked bar charts
- **QA Pipeline**: run_qa.sh, CI/CD, data regression detection
- **Skip-to-content Link**: Accessibility enhancement
- **Keyboard Shortcuts**: F key for flagging questions
- **Audio Speed Control**: 0.5x – 1.5x for listening
- **Writing Self-Assessment Save**: Slider values persisting to localStorage
- **Word Count Warning**: Red color when below minimum

### Changed
- **i18n**: 160 → 191 translation keys, 100% listening coverage
- **Dark Mode**: System prefers-color-scheme detection
- **CSS**: Full custom property system, spinner, error states
- **Accessibility**: ARIA roles, touch targets (40px), focus styles
- **Code Quality**: var → let/const, event listener cleanup
- **E2E Tests**: 37 → 43 test cases

### Fixed
- XSS vulnerabilities with escapeHtml()
- beforeunload event listener cleanup
- FormData blob sending in speaking module
- Part 2 auto-stop timer
- Template literal syntax errors in listening.js

---

## [1.0.0] — 2026-06 (Initial Release)

### Added
- **Reading Module**: 48 test sets, 13 question types, 60-min timer
- **Listening Module**: 38 test sets, 4 sections, audio playback
- **Writing Module**: 38 test sets, Task 1 + Task 2, word count
- **Speaking Module**: 38 test sets, Part 1/2/3, recording + transcription
- **Cambridge IELTS 14–20**: Complete data for all 4 skills
- **i18n**: English + Chinese bilingual (~160 keys)
- **Dark Mode**: Light/dark theme with CSS variables
- **History**: Attempt records with band scores
- **Offline Mode**: data-bundle.js for file:// protocol
- **Answer Key Verification**: 99.8% validation rate (2,236/2,240)
- **Legacy Tests**: 20 reading, 10 listening, 10 writing, 10 speaking
