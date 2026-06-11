// ===== Wrong Answer Book Module =====
// Collects wrong answers across reading and listening modules,
// supports filtering by question type, redo practice, and mastered marking.

let _wrongBookActiveFilter = 'all';
let _wrongBookItems = [];
let _wrongBookTypeStats = {};
let _wrongBookSubModule = 'list'; // 'list' | 'redo'

// ---- data collection ----

function collectAllWrongAnswers() {
  const items = [];

  // Reading attempts
  const readingHistory = getAttemptHistory();
  readingHistory.forEach(attempt => {
    if (attempt.wrongAnswers) {
      attempt.wrongAnswers.forEach(w => {
        items.push({
          ...w,
          module: 'reading',
          date: attempt.date,
          sourceLabel: attempt.testId.toUpperCase() + ' - ' + t('reading')
        });
      });
    }
  });

  // Listening attempts
  const listeningHistory = getListeningAttemptHistory();
  listeningHistory.forEach(attempt => {
    if (attempt.wrongAnswers) {
      attempt.wrongAnswers.forEach(w => {
        items.push({
          ...w,
          module: 'listening',
          date: attempt.date,
          sourceLabel: attempt.testId.toUpperCase() + ' - ' + t('listening')
        });
      });
    }
  });

  // Sort by date descending
  items.sort((a, b) => new Date(b.date) - new Date(a.date));

  return items;
}

function computeTypeStats(items) {
  const stats = {};
  items.forEach(item => {
    const t = item.type || 'unknown';
    if (!stats[t]) stats[t] = 0;
    stats[t]++;
  });
  return stats;
}

// Type label mapping — uses shared formatTypeName from i18n.js
function getTypeLabel(type) {
  return formatTypeName(type);
}

// ---- page render ----

function renderWrongBookPage(container) {
  _wrongBookItems = collectAllWrongAnswers();
  _wrongBookTypeStats = computeTypeStats(_wrongBookItems);
  _wrongBookActiveFilter = 'all';
  _wrongBookSubModule = 'list';

  if (_wrongBookItems.length === 0) {
    container.innerHTML = `
      <div class="wrong-book-container">
        <h1 data-i18n="wrongBook">${t('wrongBook')}</h1>
        <div class="wrong-book-empty">
          <p data-i18n="wrongBookEmpty">${t('wrongBookEmpty')}</p>
          <a href="#/" class="btn btn-primary" data-i18n="backToTests">${t('backToTests')}</a>
        </div>
      </div>
    `;
    return;
  }

  container.innerHTML = `
    <div class="wrong-book-container">
      <h1 data-i18n="wrongBook">${t('wrongBook')}</h1>

      <div class="wrong-book-stats">
        <div class="stats-cards" id="wrongBookStats"></div>
      </div>

      <div class="type-filter-bar" id="typeFilterBar"></div>

      <!-- Weakness quick-link -->
      <div style="text-align:right;margin-bottom:12px;" id="weaknessLink"></div>

      <div id="wrongBookList"></div>

      <div style="text-align:center;margin-top:20px;">
        <a href="#/" class="btn btn-secondary" data-i18n="backToTests">${t('backToTests')}</a>
      </div>
    </div>
  `;

  renderWrongBookStats();
  renderTypeFilterBar();
  renderWeaknessLink();
  renderWrongList('all');
}

function renderWrongBookStats() {
  const el = document.getElementById('wrongBookStats');
  if (!el) return;

  const totalTypes = Object.keys(_wrongBookTypeStats).length;
  const topType = Object.entries(_wrongBookTypeStats).sort((a, b) => b[1] - a[1])[0];

  el.innerHTML = `
    <div class="stat-card">
      <div class="stat-value">${_wrongBookItems.length}</div>
      <div class="stat-label" data-i18n="wrongCount">${t('wrongCount')}</div>
    </div>
    <div class="stat-card">
      <div class="stat-value">${totalTypes}</div>
      <div class="stat-label" data-i18n="typeDistribution">${t('typeDistribution')}</div>
    </div>
    ${topType ? `
      <div class="stat-card">
        <div class="stat-value" style="font-size:1rem;">${getTypeLabel(topType[0])}</div>
        <div class="stat-label">${topType[1]} ${t('wrongAnswers')}</div>
      </div>
    ` : ''}
  `;
}

function renderTypeFilterBar() {
  const el = document.getElementById('typeFilterBar');
  if (!el) return;

  const types = Object.keys(_wrongBookTypeStats).sort();
  let html = `<button class="type-filter-btn ${_wrongBookActiveFilter === 'all' ? 'active' : ''}" data-action="wrong-book-set-filter" data-filter="all')" data-i18n="allTypes">${t('allTypes')} (${_wrongBookItems.length})</button>`;

  types.forEach(t => {
    const count = _wrongBookTypeStats[t];
    const isActive = _wrongBookActiveFilter === t;
    html += `<button class="type-filter-btn ${isActive ? 'active' : ''}" data-action="wrong-book-set-filter" data-filter="${t}')">${getTypeLabel(t)} (${count})</button>`;
  });

  el.innerHTML = html;
}

function renderWeaknessLink() {
  const el = document.getElementById('weaknessLink');
  if (!el) return;

  const worstType = Object.entries(_wrongBookTypeStats).sort((a, b) => b[1] - a[1])[0];
  if (worstType && worstType[1] >= 2) {
    el.innerHTML = `<a href="#" class="btn btn-small btn-danger" data-action="wrong-book-start-practice" data-type="${worstType[0]}" data-i18n="practiceWeakTypes">${t('practiceWeakTypes')}: ${getTypeLabel(worstType[0])}</a>`;
  }
}

function setWrongBookFilter(type) {
  _wrongBookActiveFilter = type;
  renderTypeFilterBar();
  renderWrongList(type);
}

function renderWrongList(filterType) {
  const el = document.getElementById('wrongBookList');
  if (!el) return;

  const filtered = filterType === 'all' ? _wrongBookItems : _wrongBookItems.filter(w => w.type === filterType);

  if (filtered.length === 0) {
    el.innerHTML = `<div class="wrong-book-empty"><p data-i18n="noWrongAnswers">${t('noWrongAnswers')}</p></div>`;
    return;
  }

  let html = '';
  filtered.forEach((w, idx) => {
    const qid = `${w.testId}-${w.questionNumber}`;
    const mastered = isMastered(qid);

    html += `
      <div class="wrong-item ${mastered ? 'mastered' : ''}" id="wi-${idx}">
        <div class="wrong-item-header">
          <span class="wrong-item-source">${escapeHtml(w.sourceLabel || w.testId.toUpperCase())} — ${t('question')} ${w.questionNumber}</span>
          <span class="wrong-item-type-badge">${getTypeLabel(w.type)}</span>
        </div>
        <div class="wrong-item-question">${escapeHtml(w.question)}</div>
        <div class="wrong-item-answer">
          <span data-i18n="yourAnswer">${t('yourAnswer')}</span>: <span class="user-answer">${escapeHtml(w.yourAnswer) || '(empty)'}</span>
          &nbsp;|&nbsp; <span data-i18n="correctAnswer">${t('correctAnswer')}</span>: <span class="correct-answer">${escapeHtml(w.correctAnswer)}</span>
          ${mastered ? `<span class="mastered-badge" style="margin-left:8px;" data-i18n="mastered">${t('mastered')}</span>` : ''}
        </div>
        <div class="wrong-item-actions">
          <button class="btn btn-small btn-primary" data-action="wrong-book-redo" data-testid="${w.testId}" data-qnum="${w.questionNumber}" data-module="${w.module}" data-i18n="redoWrongQuestion">${t('redoWrongQuestion')}</button>
          ${mastered
            ? `<button class="btn btn-small btn-secondary" data-action="wrong-book-unmark-mastered" data-qid="${qid}" data-i18n="markMastered">${t('markMastered')}</button>`
            : `<button class="btn btn-small btn-secondary" data-action="wrong-book-mark-mastered" data-qid="${qid}" data-i18n="markMastered">${t('markMastered')}</button>`
          }
        </div>
      </div>
    `;
  });

  el.innerHTML = html;
}

// ---- mastered marking ----

function markAsMastered(qid) {
  saveMasteredQuestion(qid);
  renderWrongList(_wrongBookActiveFilter);
}

function unmarkMastered(qid) {
  removeMasteredQuestion(qid);
  renderWrongList(_wrongBookActiveFilter);
}

// ---- redo practice ----

let _redoTestData = null;
let _redoQuestion = null;
let _redoQuestionsAll = [];
let _redoQuestionsOnly = [];

// Practice mode state
let _practiceMode = false;
let _practiceType = null;
let _practiceIndex = 0;
let _practiceItems = [];

function startWrongRedo(testId, questionNumber, module) {
  _practiceMode = false;

  let loadPromise;
  if (testId.startsWith('cam')) {
    loadPromise = module === 'listening'
      ? App.loadCambridgeListeningTest(testId)
      : App.loadCambridgeReadingTest(testId);
  } else {
    const prefix = module === 'listening' ? 'listening/' : '';
    loadPromise = fetch(`data/${prefix}${testId}.json`).then(r => r.json());
  }

  loadPromise.then(testData => {
    // Find the question
    const allQs = [];
    if (module === 'listening') {
      testData.sections.forEach(s => s.questions.forEach(q => allQs.push(q)));
    } else {
      testData.passages.forEach(p => p.questions.forEach(q => allQs.push(q)));
    }

    // Find by questionNumber (1-indexed)
    const q = allQs[questionNumber - 1];
    if (!q) return;

    _redoTestData = testData;
    _redoQuestion = q;
    _redoQuestionsAll = allQs;
    _redoQuestionsOnly = [q];

    renderRedoPanel(q, module);
  }).catch(() => {
    showModal({ message: t('errorLoadData') });
  });
}

function startPracticeMode(type) {
  _practiceType = type;
  _practiceItems = _wrongBookItems.filter(w => w.type === type);

  if (_practiceItems.length === 0) return;

  _practiceMode = true;
  _practiceIndex = 0;
  loadPracticeQuestion(0);
}

function loadPracticeQuestion(index) {
  if (index >= _practiceItems.length) {
    // All done
    const container = document.getElementById('mainContent');
    container.innerHTML = `
      <div class="wrong-book-container">
        <h1 data-i18n="practiceMode">${t('practiceMode')}</h1>
        <div class="wrong-book-empty">
          <p style="color:var(--color-success);font-weight:600;font-size:1.1rem;" data-i18n="noWrongAnswers">${t('noWrongAnswers')}</p>
          <p style="margin-top:8px;color:var(--text-secondary);">${_practiceItems.length} ${t('wrongAnswers')} — ${t('done')}</p>
          <a href="#/wrong-book" class="btn btn-primary" style="margin-top:16px;" data-i18n="wrongBook">${t('wrongBook')}</a>
        </div>
      </div>
    `;
    return;
  }

  const item = _practiceItems[index];
  startWrongRedo(item.testId, item.questionNumber, item.module);
}

function renderRedoPanel(q, module) {
  const container = document.getElementById('wrongBookList');
  if (!container) return;

  // Scroll to top
  container.scrollIntoView({ behavior: 'smooth' });

  const typeLabel = getTypeLabel(q.type);
  const prefix = _practiceMode ? `${t('practiceMode')} (${_practiceIndex + 1}/${_practiceItems.length})` : '';

  let html = `
    <div class="redo-panel" id="redoPanel">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">
        <h3>${prefix || t('redoWrongQuestion')}</h3>
        <span class="wrong-item-type-badge">${typeLabel}</span>
      </div>
      <div class="question-text">${escapeHtml(q.question)}</div>
  `;

  // Render based on question type
  if (q.type === 'multiple_choice' || q.type === 'tfng' || q.type === 'ynng') {
    let options;
    if (q.type === 'tfng') options = ['True', 'False', 'Not Given'];
    else if (q.type === 'ynng') options = ['YES', 'NO', 'NOT GIVEN'];
    else options = q.options || [];
    html += '<div class="options" id="redoOptions">';
    options.forEach(opt => {
      html += `<label class="option-label"><input type="radio" name="redo_answer" value="${escapeHtml(opt)}">${escapeHtml(opt)}</label>`;
    });
    html += '</div>';
  } else if (q.type === 'multiple_choice_multi') {
    html += '<div class="options" id="redoOptions">';
    (q.options || []).forEach(opt => {
      html += `<label class="option-label checkbox-label"><input type="checkbox" name="redo_answer" value="${escapeHtml(opt)}">${escapeHtml(opt)}</label>`;
    });
    html += '</div>';
  } else if (q.type === 'matching_headings' || q.type === 'matching_info' || q.type === 'matching_sentence' || q.type === 'matching_names' || q.type === 'matching') {
    html += '<div class="options">';
    html += `<select id="redoSelect" style="padding:6px;border:1px solid var(--border-color);border-radius:4px;width:100%;">`;
    html += `<option value="">${t('selectAll')}</option>`;
    (q.options || []).forEach(opt => {
      html += `<option value="${escapeHtml(opt)}">${escapeHtml(opt)}</option>`;
    });
    html += '</select></div>';
  } else {
    // text input
    html += `<div class="options"><label class="option-label"><input type="text" id="redoTextInput" placeholder="..." style="flex:1;padding:6px;border:1px solid var(--border-color);border-radius:4px;"></label></div>`;
  }

  html += `
      <div style="margin-top:16px;display:flex;gap:8px;">
        <button class="btn btn-primary" data-action="wrong-book-submit-redo" data-i18n="submit">${t('submit')}</button>
        <button class="btn btn-secondary" data-action="wrong-book-cancel-redo" data-i18n="cancel">${t('cancel')}</button>
      </div>
      <div id="redoResult"></div>
    </div>
  `;

  container.innerHTML = html;
}

function submitRedoAnswer() {
  if (!_redoQuestion) { showModal({ message: t('errorLoadData') }); return; }
  const resultEl = document.getElementById('redoResult');
  if (!resultEl) return;

  // Get user answer
  let userAnswer = '';
  const checkboxes = document.querySelectorAll('#redoOptions input[name="redo_answer"]:checked');
  if (checkboxes.length > 0) {
    // Checkbox (multiple_choice_multi)
    const values = [];
    checkboxes.forEach(cb => values.push(cb.value));
    userAnswer = values.join(', ');
  } else {
    const radioChecked = document.querySelector('#redoOptions input[name="redo_answer"]:checked');
    if (radioChecked) {
      userAnswer = radioChecked.value;
    } else {
      const selectEl = document.getElementById('redoSelect');
      if (selectEl) userAnswer = selectEl.value;
      else {
        const textEl = document.getElementById('redoTextInput');
        if (textEl) userAnswer = textEl.value;
      }
    }
  }

  const isCorrect = gradeAnswer(userAnswer, _redoQuestion.correctAnswer, _redoQuestion.type);

  resultEl.innerHTML = `
    <div class="redo-result ${isCorrect ? 'correct' : 'wrong'}">
      ${isCorrect ? '&#10003; ' + t('correctAnswers') : '&#10007; ' + t('wrongAnswers')}
      <span style="font-weight:400;margin-left:8px;">
        | ${t('yourAnswer')}: ${escapeHtml(userAnswer) || '(empty)'}
        ${!isCorrect ? '| ' + t('correctAnswer') + ': ' + escapeHtml(_redoQuestion.correctAnswer) : ''}
      </span>
    </div>
    <div class="redo-explanation">
      <strong data-i18n="explanation">${t('explanation')}</strong>: ${escapeHtml(_redoQuestion.explanation) || t('noBilingualData')}
    </div>
  `;

  // In practice mode, show next button
  if (_practiceMode) {
    resultEl.innerHTML += `
      <div style="margin-top:12px;">
        <button class="btn btn-primary" data-action="wrong-book-next-practice" data-i18n="nextQuestion">${_practiceIndex < _practiceItems.length - 1 ? t('nextQuestion') : t('done')}</button>
      </div>
    `;
  }
}

function nextPracticeQuestion() {
  _practiceIndex++;
  loadPracticeQuestion(_practiceIndex);
}

function cancelRedo() {
  const container = document.getElementById('wrongBookList');
  if (container) renderWrongList(_wrongBookActiveFilter);
  _practiceMode = false;
}

