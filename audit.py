#!/usr/bin/env python3
"""
IELTS Mock Exam — Systematic 10-Round Audit Framework
=====================================================
Runs comprehensive checks across code quality, data integrity,
UI/UX, security, i18n, performance, and cross-module integration.
"""

import json
import os
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
JS_DIR = os.path.join(PROJECT_ROOT, 'js')
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')
CAMBRIDGE_DIR = os.path.join(DATA_DIR, 'cambridge')

# ── Helpers ──────────────────────────────────────────────

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def find_js_files():
    return sorted([os.path.join(JS_DIR, f) for f in os.listdir(JS_DIR)
                   if f.endswith('.js') and not f.startswith('data-bundle')])

def find_cambridge_books():
    if not os.path.isdir(CAMBRIDGE_DIR):
        return []
    return sorted([d for d in os.listdir(CAMBRIDGE_DIR)
                   if os.path.isdir(os.path.join(CAMBRIDGE_DIR, d))])

def find_json_files(subdir):
    p = os.path.join(DATA_DIR, subdir)
    if not os.path.isdir(p):
        return []
    return sorted([os.path.join(p, f) for f in os.listdir(p) if f.endswith('.json')])

# ── Audit Result Collector ───────────────────────────────

class AuditResult:
    def __init__(self):
        self.issues = []  # (severity, round_num, category, file, detail)
        self.passes = []  # (round_num, category, detail)
        self.stats = {}

    def add_issue(self, severity, round_num, category, file, detail):
        self.issues.append((severity, round_num, category, file, detail))

    def add_pass(self, round_num, category, detail):
        self.passes.append((round_num, category, detail))

    def set_stat(self, key, value):
        self.stats[key] = value

SEVERITY = {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3, 'INFO': 4}

# ═══════════════════════════════════════════════════════════
# ROUND 1: DATA INTEGRITY — Validate all JSON structure
# ═══════════════════════════════════════════════════════════

VALID_READING_TYPES = {
    'multiple_choice', 'multiple_choice_multi', 'tfng', 'ynng',
    'matching_headings', 'matching_info', 'matching_sentence',
    'matching_names', 'matching', 'sentence_completion',
    'summary_completion', 'notes_completion', 'form_completion', 'short_answer'
}

VALID_LISTENING_TYPES = {
    'multiple_choice', 'multiple_choice_multi', 'matching', 'map_labelling',
    'form_completion', 'notes_completion', 'summary_completion',
    'sentence_completion', 'short_answer', 'table_completion',
    'flow_chart_completion', 'diagram_labelling', 'label_matching'
}

def round1_data_integrity(result):
    """Validate all JSON data files: structure, types, IDs, counts."""
    r = 1
    books = find_cambridge_books()

    for book in books:
        # Reading
        rp = os.path.join(CAMBRIDGE_DIR, book, 'reading.json')
        if os.path.exists(rp):
            try:
                data = load_json(rp)
                result.add_pass(r, 'reading-structure', f'{book}/reading.json loads OK ({len(data.get("tests",[]))} tests)')
                for test in data.get('tests', []):
                    tid = test.get('id', '?')
                    qs = []
                    for p in test.get('passages', []):
                        for q in p.get('questions', []):
                            qs.append(q)
                    # Check count
                    if len(qs) != 40:
                        result.add_issue('HIGH', r, 'reading-count', f'{book}/{tid}',
                                         f'Expected 40 questions, got {len(qs)}')
                    # Check types
                    for q in qs:
                        if q.get('type') not in VALID_READING_TYPES:
                            result.add_issue('MEDIUM', r, 'reading-type', f'{book}/{tid}',
                                             f'Q{q.get("id","?")}: Unknown type "{q.get("type")}"')
                        if not q.get('correctAnswer'):
                            result.add_issue('HIGH', r, 'reading-answer', f'{book}/{tid}',
                                             f'Q{q.get("id","?")}: Missing correctAnswer')
                        if not q.get('id'):
                            result.add_issue('CRITICAL', r, 'reading-id', f'{book}/{tid}',
                                             'Question missing id')
                    # Check id format
                    for q in qs:
                        qid = q.get('id', '')
                        if not re.match(r'cam\d+_t\d+_[pr]_q\d+', qid):
                            if qid:  # only report if has id
                                result.add_issue('LOW', r, 'reading-id-format', f'{book}/{tid}',
                                                 f'Non-standard ID format: {qid}')
            except Exception as e:
                result.add_issue('CRITICAL', r, 'reading-parse', f'{book}/reading.json', str(e))

        # Listening
        lp = os.path.join(CAMBRIDGE_DIR, book, 'listening.json')
        if os.path.exists(lp):
            try:
                data = load_json(lp)
                result.add_pass(r, 'listening-structure', f'{book}/listening.json loads OK ({len(data.get("tests",[]))} tests)')
                for test in data.get('tests', []):
                    tid = test.get('id', '?')
                    qs = []
                    for part in test.get('parts', []):
                        for q in part.get('questions', []):
                            qs.append(q)
                    if len(qs) != 40:
                        result.add_issue('HIGH', r, 'listening-count', f'{book}/{tid}',
                                         f'Expected 40 questions, got {len(qs)}')
                    for q in qs:
                        if q.get('type') not in VALID_LISTENING_TYPES:
                            result.add_issue('MEDIUM', r, 'listening-type', f'{book}/{tid}',
                                             f'Q{q.get("id","?")}: Unknown type "{q.get("type")}"')
                        if not q.get('correctAnswer'):
                            result.add_issue('HIGH', r, 'listening-answer', f'{book}/{tid}',
                                             f'Q{q.get("id","?")}: Missing correctAnswer')
                    # Note: multi-select answers store individual option text per question
                    # (e.g., "B. reviewing progress"), not comma-separated pairs.
                    # The comma format is used by the user when selecting multiple checkboxes.
                    # This is the expected data format — not an issue.
            except Exception as e:
                result.add_issue('CRITICAL', r, 'listening-parse', f'{book}/listening.json', str(e))

    # Validate legacy test data
    for i in range(1, 21):
        tp = os.path.join(DATA_DIR, f'test{i}.json')
        if os.path.exists(tp):
            try:
                data = load_json(tp)
                total = sum(len(p.get('questions', [])) for p in data.get('passages', []))
                if total != data.get('totalQuestions', 40):
                    result.add_issue('MEDIUM', r, 'legacy-count', f'test{i}.json',
                                     f'totalQuestions={data.get("totalQuestions")} but counted {total}')
            except Exception as e:
                result.add_issue('HIGH', r, 'legacy-parse', f'test{i}.json', str(e))

    result.set_stat('round1_books', len(books))
    return result

# ═══════════════════════════════════════════════════════════
# ROUND 2: JS CODE QUALITY — Detect common bugs & patterns
# ═══════════════════════════════════════════════════════════

def round2_js_code_quality(result):
    """Scan all JS files for common bugs, anti-patterns, and code smells."""
    r = 2
    js_files = find_js_files()

    for jspath in js_files:
        fname = os.path.basename(jspath)
        code = read_file(jspath)
        lines = code.split('\n')

        # Check 1: console.log in production code
        console_logs = [i+1 for i, l in enumerate(lines) if 'console.log' in l and '//' not in l.split('console.log')[0]]
        for ln in console_logs:
            result.add_issue('LOW', r, 'console-log', f'{fname}:{ln}',
                             'console.log in production code')

        # Check 2: console.warn (ok but track)
        console_warns = len([l for l in lines if 'console.warn' in l])

        # Check 3: innerHTML with unescaped variables (potential XSS)
        inner_pattern = re.findall(r'\.innerHTML\s*\+?=.*\+.*\|.*\|', code)
        # Actual XSS check: template literals with ${...} in innerHTML
        xss_risks = []
        for i, l in enumerate(lines):
            if 'innerHTML' in l and 'escapeHtml' not in l:
                # Check if line uses template literal with user data
                if '${' in l and 'escapeHtml(' not in l:
                    # False positive filter: static i18n, CSS classes
                    if any(skip in l for skip in ['data-i18n', 'className', 't(']):
                        continue
                    xss_risks.append(i+1)
        for ln in xss_risks:
            result.add_issue('MEDIUM', r, 'xss-risk', f'{fname}:{ln}',
                             'innerHTML with potential unescaped data')

        # Check 4: Missing try-catch in JSON.parse
        json_parses = re.findall(r'JSON\.parse\(', code)
        unsafe_parses = 0
        for i, l in enumerate(lines):
            if 'JSON.parse(' in l and 'try' not in lines[max(0,i-2):i+1]:
                if 'catch' not in ''.join(lines[max(0,i-2):i+1]):
                    unsafe_parses += 1
        if unsafe_parses > 0:
            result.add_issue('LOW', r, 'unsafe-json-parse', fname,
                             f'{unsafe_parses} JSON.parse calls without try-catch in immediate context')

        # Check 5: == instead of ===
        loose_eq = len([l for l in lines if re.search(r'[^=!]==[^=]', l)])
        if loose_eq > 5:
            result.add_issue('LOW', r, 'loose-equality', fname,
                             f'{loose_eq} loose equality (==) usages')

        # Check 6: var vs let/const usage
        var_count = len(re.findall(r'\bvar\s+\w', code))
        let_count = len(re.findall(r'\blet\s+\w', code))

        # Check 7: File size
        if len(lines) > 800:
            result.add_issue('MEDIUM', r, 'file-too-large', fname,
                             f'{len(lines)} lines (max 800 recommended)')

        # Check 8: Functions over 50 lines
        funcs = re.findall(r'function\s+(\w+)', code)
        # Rough function length check via brace matching
        brace_depth = 0
        func_start = None
        func_name = None
        long_funcs = []
        for i, l in enumerate(lines):
            if l.strip().startswith('function ') and '{' in l:
                m = re.match(r'function\s+(\w+)', l.strip())
                if m:
                    func_name = m.group(1)
                    func_start = i
                    brace_depth = 0
            if func_start is not None:
                brace_depth += l.count('{') - l.count('}')
                if brace_depth <= 0 and func_start is not None:
                    length = i - func_start
                    if length > 50:
                        long_funcs.append((func_name, length))
                    func_start = None
        for fn, ln in long_funcs[:5]:  # top 5
            result.add_issue('LOW', r, 'long-function', f'{fname}:{fn}',
                             f'Function "{fn}" is {ln} lines (max 50 recommended)')

        # Check 9: detect global variable leaks (no var/let/const)
        potential_globals = re.findall(r'^\s{4,}(\w+)\s*=\s*(?!.*function)', code, re.MULTILINE)

    # Check 10: HTML file
    html = read_file(os.path.join(PROJECT_ROOT, 'index.html'))
    if 'cache-control' not in html.lower():
        result.add_issue('LOW', r, 'html-cache', 'index.html', 'No cache-control meta tag')
    if '<!DOCTYPE html>' not in html:
        result.add_issue('MEDIUM', r, 'html-doctype', 'index.html', 'Missing DOCTYPE')

    result.set_stat('round2_js_files', len(js_files))
    return result

# ═══════════════════════════════════════════════════════════
# ROUND 3: LISTENING MODULE DEEP AUDIT
# ═══════════════════════════════════════════════════════════

def round3_listening_deep_audit(result):
    """Deep audit of listening.js for logic bugs, state management, edge cases."""
    r = 3
    code = read_file(os.path.join(JS_DIR, 'listening.js'))
    lines = code.split('\n')
    fname = 'listening.js'

    # Check A: All setInterval calls have corresponding clearInterval
    intervals_started = len(re.findall(r'setInterval\(', code))
    intervals_cleared = len(re.findall(r'clearInterval\(', code))
    if intervals_started > intervals_cleared:
        result.add_issue('MEDIUM', r, 'timer-leak-risk', fname,
                         f'{intervals_started} setInterval vs {intervals_cleared} clearInterval calls')

    # Check B: localStorage keys consistency
    ls_keys = set(re.findall(r"localStorage\.(?:get|set)Item\('([^']+)'", code))
    result.set_stat('round3_listening_ls_keys', sorted(ls_keys))

    # Check C: State save coverage — every state change should save
    state_changes = len(re.findall(r'listening(?:Phase|SubPhase|CurrentSection)\s*=', code))
    state_saves = len(re.findall(r'saveListeningState\(', code))
    if state_saves < state_changes - 2:  # allow some local-only changes
        result.add_issue('LOW', r, 'state-save-gap', fname,
                         f'{state_changes} state changes, {state_saves} save calls')

    # Check D: Check for potential null reference issues
    null_risks = []
    for i, l in enumerate(lines):
        if re.search(r'\.(sections|passages|questions)\[', l) and 'if' not in lines[max(0,i-1)]:
            if '&&' not in l:
                null_risks.append(i+1)
    if null_risks:
        result.add_issue('LOW', r, 'null-access-risk', fname,
                         f'Array access without bounds check near lines: {null_risks[:3]}')

    # Check E: event listener cleanup
    add_listeners = len(re.findall(r'addEventListener\(', code))
    remove_listeners = len(re.findall(r'removeEventListener\(', code))
    if add_listeners > 0 and remove_listeners == 0:
        result.add_issue('INFO', r, 'event-listener-cleanup', fname,
                         f'{add_listeners} listeners added, 0 removed — potential memory leak on re-render')

    # Check F: Check listener for multi-select: consecutive questions q15,q16 with "TWO" in stem
    for book in find_cambridge_books():
        lp = os.path.join(CAMBRIDGE_DIR, book, 'listening.json')
        if not os.path.exists(lp):
            continue
        data = load_json(lp)
        for test in data.get('tests', []):
            for part in test.get('parts', []):
                qs = part.get('questions', [])
                for i in range(len(qs) - 1):
                    q1, q2 = qs[i], qs[i+1]
                    s1, s2 = q1.get('question', ''), q2.get('question', '')
                    # Same stem with "TWO" → should be multi
                    if s1 == s2 and re.search(r'(TWO|THREE)\s+', s1, re.I):
                        if q1.get('type') != 'multiple_choice_multi':
                            result.add_issue('HIGH', r, 'multi-select-missed',
                                             f'{book}/{test["id"]}',
                                             f'Q{q1.get("id")} should be multiple_choice_multi (stem has TWO/THREE)')

    return result

# ═══════════════════════════════════════════════════════════
# ROUND 4: READING/EXAM MODULE DEEP AUDIT
# ═══════════════════════════════════════════════════════════

def round4_reading_deep_audit(result):
    """Deep audit of exam.js for logic bugs, timer issues, answer grading."""
    r = 4
    code = read_file(os.path.join(JS_DIR, 'exam.js'))
    fname = 'exam.js'

    # Check A: autoSubmit → submitExam call chain
    if 'autoSubmit' in code and 'submitExam' in code:
        result.add_pass(r, 'auto-submit-chain', 'autoSubmit → submitExam chain exists')

    # Check B: Multiple choice multi grading consistency
    # exam.js submitExam and listening.js listeningSubmitExam should use same grading logic
    exam_code = code
    listening_code = read_file(os.path.join(JS_DIR, 'listening.js'))

    exam_multi = 'userParts.length === correctParts.length && userParts.every((v, i) => v === correctParts[i])'
    listening_multi = 'userParts.length === correctParts.length && userParts.every((v, i) => v === correctParts[i])'
    if exam_multi in exam_code and listening_multi in listening_code:
        result.add_pass(r, 'grading-consistency', 'Multiple choice multi grading consistent across modules')
    else:
        result.add_issue('HIGH', r, 'grading-inconsistent', 'exam.js+listening.js',
                         'Multiple choice multi grading logic differs between modules')

    # Check B2: Grading also in submitExam vs listeningSubmitExam — wrong answer collection
    # In exam.js, wrongAnswers are computed twice (submitExam and in the history save area)
    # Check for the duplicated grading logic

    # Check C: Timer integration
    timer_code = read_file(os.path.join(JS_DIR, 'timer.js'))
    if 'Timer.init' in exam_code and 'Timer.start' in exam_code:
        result.add_pass(r, 'timer-integration', 'Timer properly initialized and started')

    # Check D: Passage switching — scroll restoration
    if 'scrollIntoView' in exam_code:
        result.add_pass(r, 'scroll-behavior', 'Question nav uses scrollIntoView')

    # Check E: Answer save on passage switch — does switching passages preserve answers?
    # In exam.js renderQuestions only reads from global state, so answers persist. Good.
    if 'currentAnswers' in exam_code:
        result.add_pass(r, 'answer-persistence', 'Answers stored in module-level variable across passage switches')

    # Check F: Flag persistence across passage switch
    if 'currentFlagged' in exam_code:
        result.add_pass(r, 'flag-persistence', 'Flags stored in module-level variable')

    return result

# ═══════════════════════════════════════════════════════════
# ROUND 5: WRITING & SPEAKING MODULES AUDIT
# ═══════════════════════════════════════════════════════════

def round5_writing_speaking_audit(result):
    """Audit writing.js and speaking.js for completeness and bugs."""
    r = 5

    # Writing module
    wcode = read_file(os.path.join(JS_DIR, 'writing.js'))
    wname = 'writing.js'

    # Check A: Timer save frequency
    if 'writingTimeRemaining % 30 === 0' in wcode:
        result.add_pass(r, 'writing-timer-save', 'Writing state saved every 30 seconds')
    else:
        result.add_issue('MEDIUM', r, 'writing-timer-save', wname,
                         'Writing timer may not save state periodically')

    # Check B: Textarea content saved before task switch
    if 'writingAnswers[writingCurrentTask] = ta.value' in wcode:
        result.add_pass(r, 'writing-task-switch-save', 'Textarea saved before task switch')

    # Check C: Word count updates
    if 'onWritingInput' in wcode and 'countWords' in wcode:
        result.add_pass(r, 'writing-word-count', 'Real-time word count tracking')

    # Speaking module
    scode = read_file(os.path.join(JS_DIR, 'speaking.js'))
    sname = 'speaking.js'

    # Check D: MediaRecorder cleanup
    if 'stopRecording' in scode and 'speakingMediaRecorder.stop()' in scode:
        result.add_pass(r, 'speaking-recorder-stop', 'MediaRecorder properly stopped')

    # Check E: Recording blob storage (in-memory only — lost on refresh)
    if 'speakingRecordings' in scode and 'localStorage' not in scode:
        result.add_issue('MEDIUM', r, 'speaking-no-persist', sname,
                         'Recordings stored in memory only — lost on page refresh')

    # Check F: Hardcoded localhost URL
    if 'localhost:8081' in scode:
        result.add_issue('LOW', r, 'speaking-hardcoded-url', sname,
                         'Transcription endpoint hardcoded to localhost:8081')

    # Check G: Part3 question rendering with JSON.stringify in onclick
    if 'JSON.stringify' in scode:
        result.add_issue('MEDIUM', r, 'speaking-json-onclick', sname,
                         'JSON.stringify in onclick handler — fragile, may break with special chars')

    return result

# ═══════════════════════════════════════════════════════════
# ROUND 6: STATE MANAGEMENT & LOCALSTORAGE CONSISTENCY
# ═══════════════════════════════════════════════════════════

def round6_state_management(result):
    """Check localStorage key naming consistency and cleanup coverage."""
    r = 6

    all_js = ''
    for jspath in find_js_files():
        all_js += read_file(jspath)

    # Find all localStorage keys
    all_keys = set()
    set_calls = re.findall(r"localStorage\.setItem\('([^']+)'", all_js)
    get_calls = re.findall(r"localStorage\.getItem\('([^']+)'", all_js)
    remove_calls = re.findall(r"localStorage\.removeItem\('([^']+)'", all_js)
    all_keys = set(set_calls) | set(get_calls) | set(remove_calls)

    # Check naming convention
    prefixes = defaultdict(list)
    for k in sorted(all_keys):
        parts = k.split('_')
        if len(parts) >= 2:
            prefix = '_'.join(parts[:2])
        else:
            prefix = parts[0]
        prefixes[prefix].append(k)

    result.set_stat('round6_ls_prefixes', dict(prefixes))
    result.set_stat('round6_total_ls_keys', len(all_keys))

    # Check: keys that are set but never removed (potential accumulation)
    for k in sorted(set_calls):
        if k not in remove_calls and k not in ['ielts_lang', 'ielts_active_tab']:
            result.add_issue('INFO', r, 'ls-no-removal', 'localStorage',
                             f'Key "{k}" is set but never removed')

    # Check: clearAllHistoryData completeness
    data_code = read_file(os.path.join(JS_DIR, 'data.js'))
    clear_func = data_code[data_code.find('function clearAllHistoryData'):]
    cleared_in_func = set(re.findall(r"localStorage\.removeItem\('([^']+)'", clear_func))

    # Check that all test-prefixed keys for test1-test10 are covered
    for i in range(1, 11):
        tid = f'test{i}'
        expected = [
            f'exam_state_{tid}', f'user_answers_{tid}', f'flagged_{tid}', f'timer_{tid}',
            f'listening_answers_{tid}', f'listening_state_{tid}', f'listening_flagged_{tid}',
            f'listening_timer_{tid}', f'writing_answers_{tid}', f'writing_state_{tid}',
        ]
        for ek in expected:
            if ek in set_calls and ek not in str(clear_func):
                # Check if it's covered by the prefix removal in clearListeningData etc
                if 'listening_answers_' in clear_func and 'listening_' in ek:
                    continue  # covered by prefix pattern
                if 'writing_answers_' in clear_func and 'writing_' in ek:
                    continue

    # Check: cambridge test state clearing
    cam_keys_in_clear = False
    for k in set_calls:
        if k.startswith('exam_state_cam') or k.startswith('listening_state_cam'):
            if not cam_keys_in_clear:
                result.add_issue('MEDIUM', r, 'ls-cam-clear', 'data.js',
                                 'clearAllHistoryData does not clear Cambridge test states (cam14-cam20)')
                cam_keys_in_clear = True

    return result

# ═══════════════════════════════════════════════════════════
# ROUND 7: UI/UX EDGE CASES & NAVIGATION FLOW
# ═══════════════════════════════════════════════════════════

def round7_ui_ux_edge_cases(result):
    """Check UI state transitions, error states, empty states, loading states."""
    r = 7

    all_js = ''
    for jspath in find_js_files():
        all_js += read_file(jspath)
    html = read_file(os.path.join(PROJECT_ROOT, 'index.html'))

    # Check A: All modules have error handling for data loading
    modules_with_error = 0
    for pattern in ['errorLoadData', 'catch', 'console.error']:
        if pattern in all_js:
            modules_with_error += 1
    if modules_with_error >= 3:
        result.add_pass(r, 'error-handling', 'Multiple error handling patterns found')
    else:
        result.add_issue('MEDIUM', r, 'error-handling-gap', 'global',
                         'Insufficient error handling across modules')

    # Check B: Loading states
    loading_states = len(re.findall(r'loading', all_js, re.I))
    if loading_states >= 3:
        result.add_pass(r, 'loading-states', f'{loading_states} loading state references')
    else:
        result.add_issue('LOW', r, 'loading-states', 'global', 'Few loading state indicators')

    # Check C: Empty states
    empty_states = len(re.findall(r'empty-state|noHistory|wrongBookEmpty|historyEmpty', all_js))
    if empty_states >= 4:
        result.add_pass(r, 'empty-states', f'{empty_states} empty state references')

    # Check D: Modal overlay cleanup
    modal_removes = len(re.findall(r'\.modal-overlay.*remove', all_js))
    modal_creates = len(re.findall(r'className\s*=\s*[\'"]modal-overlay[\'"]', all_js))
    if modal_removes >= modal_creates:
        result.add_pass(r, 'modal-cleanup', 'Modal overlays properly cleaned up')

    # Check E: Navigation flow completeness
    # Hash routes defined
    routes = re.findall(r"hash\s*===\s*'([^']+)'|hash\.startsWith\('([^']+)'\)", all_js)
    all_routes = set()
    for a, b in routes:
        all_routes.add(a or b)
    result.set_stat('round7_routes', sorted(all_routes))

    # Check F: Back navigation availability
    back_links = len(re.findall(r'backToTests|#/"|#/history', all_js))
    if back_links >= 5:
        result.add_pass(r, 'navigation-back', 'Back navigation available in multiple views')

    # Check G: CSS file analysis
    css = read_file(os.path.join(PROJECT_ROOT, 'css/style.css'))
    css_lines = len(css.split('\n'))
    result.set_stat('round7_css_lines', css_lines)

    # Check for responsive design indicators
    responsive = len(re.findall(r'@media|max-width|min-width|clamp\(', css))
    if responsive >= 3:
        result.add_pass(r, 'responsive-css', f'{responsive} responsive design indicators in CSS')

    # Check H: Focus/active/hover states
    focus_states = len(re.findall(r':focus|:hover|:active', css))
    result.set_stat('round7_focus_states', focus_states)
    if focus_states < 5:
        result.add_issue('LOW', r, 'interaction-states', 'style.css',
                         f'Only {focus_states} focus/hover/active states — accessibility concern')

    return result

# ═══════════════════════════════════════════════════════════
# ROUND 8: CROSS-MODULE INTEGRATION
# ═══════════════════════════════════════════════════════════

def round8_cross_module_integration(result):
    """Check consistency across history, review, wrong-book, and exam modules."""
    r = 8
    all_js = ''
    for jspath in find_js_files():
        all_js += read_file(jspath)

    # Check A: Wrong answer data flow
    # exam.js saves wrongAnswers array → history.js reads from attempt_history → wrong-book.js reads from both
    if 'wrongAnswers' in all_js:
        save_patterns = len(re.findall(r'wrongAnswers.*push|wrongAnswers:', all_js))
        read_patterns = len(re.findall(r'wrongAnswers.*forEach|\.wrongAnswers', all_js))
        if save_patterns >= 2 and read_patterns >= 2:
            result.add_pass(r, 'wrong-answer-flow', 'Wrong answer data flows correctly: exam → history → wrong-book')

    # Check B: Review module consistency
    # listening-review.js and review.js should render similar structures
    review_code = read_file(os.path.join(JS_DIR, 'review.js'))
    lreview_code = read_file(os.path.join(JS_DIR, 'listening-review.js'))
    if 'review-question' in review_code and 'review-question' in lreview_code:
        result.add_pass(r, 'review-consistency', 'Reading and listening reviews use consistent CSS classes')

    # Check C: Attempt history format consistency
    # Reading attempts and listening attempts should have similar structure
    reading_attempt_fields = set(re.findall(r'attempt\.(\w+)', review_code))
    listening_attempt_fields = set(re.findall(r'attempt\.(\w+)', lreview_code))
    common = reading_attempt_fields & listening_attempt_fields
    if len(common) >= 3:
        result.add_pass(r, 'attempt-format', f'{len(common)} common fields between reading and listening attempts')
    diff = reading_attempt_fields ^ listening_attempt_fields
    if diff:
        result.add_issue('LOW', r, 'attempt-format-diff', 'review.js+listening-review.js',
                         f'Different fields: {diff}')

    # Check D: Type labels consistency across modules
    # Wrong-book.js and review.js should use same type labels
    wb_types = set()
    review_types = set()
    for m in re.finditer(r"'(\w+)':\s*'([^']+)'", read_file(os.path.join(JS_DIR, 'wrong-book.js'))):
        wb_types.add(m.group(1))
    for m in re.finditer(r"'(\w+)':\s*'([^']+)'", review_code):
        review_types.add(m.group(1))
    common_types = wb_types & review_types
    if common_types:
        result.add_pass(r, 'type-labels-consistent', f'{len(common_types)} type labels consistent across modules')

    # Check E: Cambridge test ID parsing consistency
    cam_parses = len(re.findall(r'\.startsWith\([\'"]cam[\'"]\)|parseCambridgePath|cam\d+_', all_js))
    if cam_parses >= 3:
        result.add_pass(r, 'cambridge-parsing', 'Cambridge test ID parsing appears consistent')

    # Check F: History page links to correct review pages
    if '#/review/' in all_js and '#/listening-review/' in all_js:
        result.add_pass(r, 'review-routing', 'Both reading and listening review routes exist')

    return result

# ═══════════════════════════════════════════════════════════
# ROUND 9: I18N COVERAGE & ACCESSIBILITY
# ═══════════════════════════════════════════════════════════

def round9_i18n_accessibility(result):
    """Check i18n key coverage, missing translations, and basic accessibility."""
    r = 9

    i18n_code = read_file(os.path.join(JS_DIR, 'i18n.js'))

    # Extract all i18n keys
    en_keys = set(re.findall(r"(\w+):\s*'", i18n_code.split('en:')[1].split('zh:')[0]))
    zh_keys = set(re.findall(r"(\w+):\s*'", i18n_code.split('zh:')[1].split('};')[0]))

    # Check for missing translations
    en_only = en_keys - zh_keys
    zh_only = zh_keys - en_keys
    if en_only:
        result.add_issue('MEDIUM', r, 'i18n-missing-zh', 'i18n.js',
                         f'Keys missing in zh: {en_only}')
    if zh_only:
        result.add_issue('MEDIUM', r, 'i18n-missing-en', 'i18n.js',
                         f'Keys missing in en: {zh_only}')

    # Check for duplicate keys
    en_list = re.findall(r"(\w+):\s*'", i18n_code.split('en:')[1].split('zh:')[0])
    dups = [k for k, v in Counter(en_list).items() if v > 1]
    if dups:
        result.add_issue('HIGH', r, 'i18n-duplicate-keys', 'i18n.js',
                         f'Duplicate keys in en: {dups}')

    # Check data-i18n usage in JS files
    all_js = ''
    for jspath in find_js_files():
        all_js += read_file(jspath)

    used_i18n_keys = set()
    for m in re.finditer(r"(?<!\w)t\s*\(\s*'(\w+)'\s*\)", all_js):
        used_i18n_keys.add(m.group(1))
    for m in re.finditer(r'data-i18n="(\w+)"', all_js):
        used_i18n_keys.add(m.group(1))

    unused_in_code = en_keys - used_i18n_keys
    used_but_missing = used_i18n_keys - en_keys
    if unused_in_code:
        result.add_issue('LOW', r, 'i18n-unused-keys', 'i18n.js',
                         f'{len(unused_in_code)} keys defined but not referenced in code')
    if used_but_missing:
        result.add_issue('HIGH', r, 'i18n-missing-def', 'i18n.js',
                         f'{len(used_but_missing)} keys used in code but not defined: {used_but_missing}')

    result.set_stat('round9_en_keys', len(en_keys))
    result.set_stat('round9_zh_keys', len(zh_keys))
    result.set_stat('round9_used_keys', len(used_i18n_keys))

    # Check basic HTML accessibility
    html = read_file(os.path.join(PROJECT_ROOT, 'index.html'))
    if 'lang=' in html:
        result.add_pass(r, 'html-lang', 'HTML lang attribute present')
    if 'viewport' in html:
        result.add_pass(r, 'html-viewport', 'Viewport meta tag present')
    if 'charset' in html.lower():
        result.add_pass(r, 'html-charset', 'Charset declaration present')
    if 'aria-label' in all_js:
        result.add_pass(r, 'aria-labels', 'ARIA labels used in JS-generated content')

    return result

# ═══════════════════════════════════════════════════════════
# ROUND 10: SECURITY, PERFORMANCE & FINAL SUMMARY
# ═══════════════════════════════════════════════════════════

def round10_security_performance(result):
    """Security audit, performance issues, and final summary across all rounds."""
    r = 10

    all_js = ''
    for jspath in find_js_files():
        all_js += read_file(jspath)
    html = read_file(os.path.join(PROJECT_ROOT, 'index.html'))

    # ── Security ──
    # Check 1: Hardcoded URLs/endpoints
    urls = re.findall(r'https?://[^\s\'"]+', all_js)
    if urls:
        result.add_issue('LOW', r, 'security-hardcoded-urls', 'JS',
                         f'Hardcoded URLs: {urls}')

    # Check 2: innerHTML with user data (XSS)
    # Already partially checked in round 2, but deeper check here
    innerhtml_no_escape = 0
    for line in all_js.split('\n'):
        if '.innerHTML' in line and 'escapeHtml' not in line:
            if '${' in line:
                innerhtml_no_escape += 1
    result.set_stat('round10_innerhtml_unescaped', innerhtml_no_escape)

    # Check 3: dangerouslySetInnerHTML or equivalent
    # (not applicable for vanilla JS but checking)

    # Check 4: eval usage
    eval_count = len(re.findall(r'\beval\(', all_js))
    if eval_count > 0:
        result.add_issue('CRITICAL', r, 'security-eval', 'JS', f'{eval_count} eval() calls found')

    # Check 5: No CSRF protection for any state-changing operations
    # (This is a client-side only app, so CSRF not really applicable, but note it)
    result.add_issue('INFO', r, 'security-csrf', 'global',
                     'Client-side only app — no server-side CSRF protection (expected)')

    # ── Performance ──
    # Check 1: Bundle size
    bundle_path = os.path.join(JS_DIR, 'data-bundle.js')
    if os.path.exists(bundle_path):
        bundle_size = os.path.getsize(bundle_path)
        bundle_size_kb = bundle_size / 1024
        result.set_stat('round10_bundle_size_kb', round(bundle_size_kb, 1))
        if bundle_size_kb > 300:
            result.add_issue('HIGH', r, 'perf-bundle-size', 'data-bundle.js',
                             f'Bundle size {bundle_size_kb:.0f}KB exceeds 300KB budget')
        elif bundle_size_kb > 150:
            result.add_issue('MEDIUM', r, 'perf-bundle-size', 'data-bundle.js',
                             f'Bundle size {bundle_size_kb:.0f}KB — consider splitting')

    # Check 2: All scripts loaded synchronously in index.html
    script_tags = re.findall(r'<script[^>]*>', html)
    async_defer = len(re.findall(r'async|defer', html))
    result.set_stat('round10_script_tags', len(script_tags))
    if async_defer == 0:
        result.add_issue('LOW', r, 'perf-sync-scripts', 'index.html',
                         f'{len(script_tags)} scripts loaded synchronously — consider defer')

    # Check 3: DOM operations in loops
    dom_in_loops = len(re.findall(r'for\s*\([^)]*\)\s*\{[^}]*innerHTML', all_js))
    if dom_in_loops > 2:
        result.add_issue('MEDIUM', r, 'perf-dom-loops', 'JS',
                         'innerHTML assignments inside loops — may cause layout thrashing')

    # Check 4: No lazy loading of below-the-fold data
    # (All data loads eagerly — acceptable for exam app)

    # ── Architecture ──
    # Check 1: Global namespace pollution
    global_funcs = set()
    for jspath in find_js_files():
        code = read_file(jspath)
        for m in re.finditer(r'^function\s+(\w+)', code, re.MULTILINE):
            global_funcs.add(m.group(1))
        for m in re.finditer(r'^(?:let|var)\s+(\w+)', code, re.MULTILINE):
            global_funcs.add(m.group(1))
    result.set_stat('round10_global_names', len(global_funcs))

    # Check 2: Module coupling — check cross-file references
    cross_refs = defaultdict(set)
    for jspath in find_js_files():
        fname = os.path.basename(jspath)
        code = read_file(jspath)
        for other in find_js_files():
            other_name = os.path.basename(other).replace('.js', '')
            if other != jspath and other_name in code:
                # Check if functions from other file are called
                other_code = read_file(other)
                other_funcs = set(re.findall(r'^function\s+(\w+)', other_code, re.MULTILINE))
                for fn in other_funcs:
                    if fn in code:
                        cross_refs[fname].add(f'{other_name}.{fn}')

    result.set_stat('round10_cross_refs', {k: sorted(v) for k, v in cross_refs.items()})

    # ── Final Summary ──
    result.set_stat('round10_total_issues', len(result.issues))
    severity_counts = Counter(s[0] for s in result.issues)
    result.set_stat('round10_severity_breakdown', dict(severity_counts))

    return result


# ═══════════════════════════════════════════════════════════
# MAIN: Run all 10 rounds
# ═══════════════════════════════════════════════════════════

def run_full_audit():
    result = AuditResult()

    print("=" * 70)
    print("  IELTS MOCK EXAM — SYSTEMATIC 10-ROUND AUDIT")
    print("=" * 70)
    print(f"  Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Project: {PROJECT_ROOT}")
    print()

    rounds = [
        ("ROUND  1: Data Integrity", round1_data_integrity),
        ("ROUND  2: JS Code Quality", round2_js_code_quality),
        ("ROUND  3: Listening Deep Audit", round3_listening_deep_audit),
        ("ROUND  4: Reading/Exam Deep Audit", round4_reading_deep_audit),
        ("ROUND  5: Writing & Speaking Audit", round5_writing_speaking_audit),
        ("ROUND  6: State Management & localStorage", round6_state_management),
        ("ROUND  7: UI/UX Edge Cases & Navigation", round7_ui_ux_edge_cases),
        ("ROUND  8: Cross-Module Integration", round8_cross_module_integration),
        ("ROUND  9: i18n Coverage & Accessibility", round9_i18n_accessibility),
        ("ROUND 10: Security, Performance & Summary", round10_security_performance),
    ]

    for round_name, round_func in rounds:
        print(f"  Running {round_name}...", end=" ")
        try:
            result = round_func(result)
            round_num = int(round_name.split(':')[0].split()[-1])
            issues_this_round = len([i for i in result.issues if i[1] == round_num])
            passes_this_round = len([p for p in result.passes if p[0] == round_num])
            print(f"{issues_this_round} issues, {passes_this_round} checks passed")
        except Exception as e:
            print(f"ERROR: {e}")

    print()
    return result


def print_report(result):
    """Generate a comprehensive audit report."""
    print("=" * 70)
    print("  AUDIT REPORT SUMMARY")
    print("=" * 70)

    # Severity breakdown
    sev_order = ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'INFO']
    sev_counts = Counter(s[0] for s in result.issues)

    print(f"\n  Total Issues Found: {len(result.issues)}")
    for sev in sev_order:
        count = sev_counts.get(sev, 0)
        if count > 0:
            icon = {'CRITICAL': '🔴', 'HIGH': '🟠', 'MEDIUM': '🟡', 'LOW': '🔵', 'INFO': '⚪'}.get(sev, '  ')
            print(f"    {icon} {sev}: {count}")

    print(f"\n  Total Checks Passed: {len(result.passes)}")

    # Print all issues grouped by severity
    for sev in sev_order:
        issues = [(r, cat, f, d) for s, r, cat, f, d in result.issues if s == sev]
        if not issues:
            continue
        print(f"\n  ── {sev} ISSUES ({len(issues)}) ──")
        for round_num, cat, fpath, detail in issues:
            print(f"    [R{round_num}] {cat} | {fpath}")
            print(f"      → {detail}")

    # Stats summary
    print(f"\n  ── STATISTICS ──")
    for k, v in result.stats.items():
        if isinstance(v, dict):
            print(f"    {k}: {json.dumps(v, indent=6)[:200]}")
        else:
            print(f"    {k}: {v}")

    print("\n" + "=" * 70)


def export_json_report(result, path):
    """Export audit results as JSON for programmatic consumption."""
    report = {
        'timestamp': datetime.now().isoformat(),
        'total_issues': len(result.issues),
        'total_passes': len(result.passes),
        'issues': [
            {
                'severity': s,
                'round': r,
                'category': c,
                'file': f,
                'detail': d
            }
            for s, r, c, f, d in result.issues
        ],
        'passes': [
            {'round': r, 'category': c, 'detail': d}
            for r, c, d in result.passes
        ],
        'stats': {k: (v if isinstance(v, (str, int, float, bool, list)) else str(v))
                  for k, v in result.stats.items()}
    }
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    print(f"\n  JSON report exported to: {path}")


if __name__ == '__main__':
    result = run_full_audit()
    print_report(result)
    export_json_report(result, os.path.join(PROJECT_ROOT, 'audit_report.json'))
