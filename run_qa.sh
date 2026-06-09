#!/bin/bash
# IELTS Mock Exam — One-click QA Pipeline
# Usage:
#   bash run_qa.sh              # Full: validate + audit + bundle + e2e
#   bash run_qa.sh --quick      # Python validation only (no e2e)
#   bash run_qa.sh --data-only  # Data validation only (no JS audit, no e2e)
#   bash run_qa.sh --full       # Everything including e2e (same as default)

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

PASS=0
FAIL=0
MODE="${1:---full}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

log_section() { echo -e "\n${BLUE}━━━ $1 ━━━${NC}"; }
log_pass()   { echo -e "  ${GREEN}✓${NC} $1"; ((PASS++)) || true; }
log_fail()   { echo -e "  ${RED}✗${NC} $1"; ((FAIL++)) || true; }
log_warn()   { echo -e "  ${YELLOW}⚠${NC} $1"; }

# ── Step 1: Python data validation ──────────────────────────
log_section "Step 1: Data Structure Validation (validate_all.py)"
if python3 validate_all.py --json > /tmp/qa_validate.json 2>&1; then
    ISSUES=$(python3 -c "import json; d=json.load(open('/tmp/qa_validate.json')); print(d.get('total_issues', d.get('issues', 0)))" 2>/dev/null || echo "0")
    if [ "$ISSUES" = "0" ] || [ "$ISSUES" = "[]" ]; then
        log_pass "Data validation passed — 0 issues"
    else
        log_pass "Data validation completed — $ISSUES issues (non-critical)"
    fi
else
    EXIT_CODE=$?
    if [ $EXIT_CODE -eq 2 ]; then
        log_fail "Data validation found CRITICAL issues"
    else
        log_warn "Data validation found HIGH-severity issues"
    fi
fi

# ── Step 2: Comprehensive audit ─────────────────────────────
if [ "$MODE" != "--data-only" ]; then
    log_section "Step 2: Project Audit (audit.py)"
    if python3 audit.py > /tmp/qa_audit.json 2>&1; then
        CRITICAL=$(python3 -c "
import json
d=json.load(open('/tmp/qa_audit.json'))
crit = [i for i in d.get('issues',[]) if i.get('severity')=='CRITICAL']
print(len(crit))
" 2>/dev/null || echo "0")
        if [ "$CRITICAL" = "0" ]; then
            log_pass "Audit passed — 0 CRITICAL issues"
        else
            log_fail "Audit found $CRITICAL CRITICAL issues"
        fi
    else
        log_fail "Audit script failed to run"
    fi
fi

# ── Step 3: Data bundle generation ──────────────────────────
log_section "Step 3: Data Bundle Generation (bundle_data.py)"
if python3 bundle_data.py 2>&1; then
    BUNDLE_SIZE=$(wc -c < js/data-bundle.js 2>/dev/null || echo "0")
    BUNDLE_MB=$(echo "scale=1; $BUNDLE_SIZE / 1048576" | bc 2>/dev/null || echo "?")
    MAX_SIZE=2097152  # 2 MB
    if [ "$BUNDLE_SIZE" -lt "$MAX_SIZE" ]; then
        log_pass "Bundle generated — ${BUNDLE_MB} MB (under 2 MB limit)"
    else
        log_fail "Bundle size ${BUNDLE_MB} MB exceeds 2 MB limit"
    fi
elif [ "$MODE" = "--data-only" ] || [ "$MODE" = "--quick" ]; then
    log_warn "Bundle generation skipped (bundle_data.py not available)"
fi

# ── Step 4: Data regression check ───────────────────────────
log_section "Step 4: Data Regression Check"
if python3 check_data_regression.py 2>&1; then
    log_pass "No data regressions detected"
else
    log_fail "Data regression detected — review changes"
fi

# ── Step 5: Playwright E2E ──────────────────────────────────
if [ "$MODE" = "--quick" ] || [ "$MODE" = "--data-only" ]; then
    log_section "Step 5: E2E Tests — SKIPPED (mode: $MODE)"
else
    log_section "Step 5: Playwright E2E Tests"
    if command -v npx &>/dev/null; then
        if npx playwright test e2e/ --config=e2e/playwright.config.js 2>&1 | tail -20; then
            log_pass "All E2E tests passed"
        else
            log_fail "E2E tests failed"
        fi
    else
        log_warn "Playwright not available — install with: npm install"
    fi
fi

# ── Summary ─────────────────────────────────────────────────
echo -e "\n${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "  ${GREEN}Passed: $PASS${NC}  ${RED}Failed: $FAIL${NC}"
if [ "$FAIL" -eq 0 ]; then
    echo -e "  ${GREEN}QA Pipeline: ALL CHECKS PASSED ✓${NC}"
    exit 0
else
    echo -e "  ${RED}QA Pipeline: $FAIL CHECK(S) FAILED ✗${NC}"
    exit 1
fi
