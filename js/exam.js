let currentTestData = null;
let currentAnswers = {};
let currentFlagged = [];
let currentPassageIndex = 0;
let allQuestions = [];

function renderExam(testData) {
  currentTestData = testData;
  currentAnswers = loadAnswers(testData.id);
  currentFlagged = loadFlagged(testData.id);
  currentPassageIndex = 0;

  // Build flat question list
  allQuestions = [];
  testData.passages.forEach((p, pi) => {
    p.questions.forEach(q => {
      allQuestions.push({ ...q, passageIndex: pi });
    });
  });

  const container = document.getElementById('mainContent');
  container.innerHTML = `
    <div class="exam-container">
      <div class="exam-topbar">
        <span class="test-title">${testData.id.toUpperCase()} - ${t('reading')}</span>
        <div class="timer" id="timerDisplay" role="timer" aria-live="polite" aria-label="Time remaining: 60 minutes">60:00</div>
        <span class="progress-text">
          <strong id="answeredCount">${Object.keys(currentAnswers).length}</strong>/${testData.totalQuestions} ${t('answered')}
          | <strong id="flaggedCount">${currentFlagged.length}</strong> ${t('flagged')}
        </span>
        <button class="btn btn-primary btn-small" onclick="showSubmitModal()" data-i18n="submit">${t('submit')}</button>
      </div>
      <div class="exam-main">
        <div class="exam-passage" id="passagePanel"></div>
        <div class="exam-questions" id="questionsPanel"></div>
      </div>
      <div class="question-nav" id="questionNav"></div>
    </div>
  `;

  renderPassageTabs();
  renderPassageContent(0);
  renderQuestions(0);
  renderQuestionNav();

  // Start timer
  Timer.init(testData.id, () => autoSubmit());

  // Track focused question for keyboard shortcuts
  window._examActiveQid = null;
  // Keyboard shortcut: 'f' to flag/unflag the last-focused question
  window._examShortcutHandler = function(e) {
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA' || e.target.tagName === 'SELECT') return;
    if (e.key === 'f' || e.key === 'F') {
      e.preventDefault();
      if (window._examActiveQid) toggleFlag(window._examActiveQid);
    }
  };
  document.addEventListener('keydown', window._examShortcutHandler);

  // If exam was already completed, don't start timer
  const state = loadExamState(testData.id);
  if (state && state.completed) {
    // Don't allow answering, show review mode
  } else {
    // Check if there's saved timer state to know if we should start
    const savedTimer = Timer.loadState(testData.id);
    if (savedTimer && savedTimer.remaining < 3600) {
      // Resume existing exam
      Timer.start();
    } else {
      // New exam
      saveExamState(testData.id, { startedAt: Date.now(), completed: false });
      Timer.start();
    }
  }
}

function renderPassageTabs() {
  const panel = document.getElementById('passagePanel');
  let tabsHtml = '<div class="passage-tabs">';
  let contentHtml = '';
  currentTestData.passages.forEach((p, i) => {
    tabsHtml += `<div class="passage-tab ${i === 0 ? 'active' : ''}" role="tab" aria-selected="${i === 0}" aria-controls="passage-${i}" onclick="switchPassage(${i})">${t('passage')} ${i + 1}: ${p.title}</div>`;
    contentHtml += `
      <div class="passage-content ${i === 0 ? 'active' : ''}" id="passage-${i}" role="tabpanel" data-passage="${i}">
        <h2>${t('passage')} ${i + 1}: ${p.title}</h2>
        <div class="passage-text">${escapeHtml(p.text)}</div>
      </div>
    `;
  });
  tabsHtml += '</div>';
  panel.innerHTML = tabsHtml + contentHtml;
}

function renderPassageContent(index) {
  document.querySelectorAll('.passage-tab').forEach((tab, i) => { tab.classList.toggle('active', i === index); tab.setAttribute('aria-selected', i === index); });
  document.querySelectorAll('.passage-content').forEach((el, i) => el.classList.toggle('active', i === index));
}

function switchPassage(index) {
  currentPassageIndex = index;
  renderPassageContent(index);
  renderQuestions(index);
}

function renderQuestions(passageIndex) {
  const panel = document.getElementById('questionsPanel');
  const passage = currentTestData.passages[passageIndex];
  if (!passage) return;

  let html = '';
  passage.questions.forEach((q, qi) => {
    const qid = q.id;
    const userAnswer = currentAnswers[qid] || '';
    const isFlagged = currentFlagged.includes(qid);

    html += `<div class="question-item ${isFlagged ? 'flagged' : ''} ${userAnswer ? 'answered' : ''}" id="q-${escapeHtml(qid)}" data-qid="${escapeHtml(qid)}">`;
    html += `
      <div class="question-header">
        <span class="question-number">${t('question')} ${getQuestionGlobalNumber(qid)}</span>
        <button class="flag-btn ${isFlagged ? 'flagged' : ''}" onclick="toggleFlag('${escapeHtml(qid)}')" data-i18n="${isFlagged ? 'flagged' : 'flag'}" aria-label="${isFlagged ? t('unflag') : t('flag')} question ${getQuestionGlobalNumber(qid)}">${isFlagged ? t('flagged') : t('flag')}</button>
      </div>
    `;
    html += `<div class="question-text">${escapeHtml(q.question)}</div>`;

    // Render based on type
    html += renderQuestionInput(q, qid, userAnswer);

    html += '</div>';
  });
  panel.innerHTML = html;
}

function getQuestionGlobalNumber(qid) {
  for (let i = 0; i < allQuestions.length; i++) {
    if (allQuestions[i].id === qid) return i + 1;
  }
  return '?';
}

function renderQuestionInput(q, qid, userAnswer) {
  switch (q.type) {
    case 'multiple_choice':
      return renderRadioOptions(q, qid, userAnswer);
    case 'multiple_choice_multi':
      return renderCheckboxOptions(q, qid, userAnswer);
    case 'tfng':
      return renderRadioOptions(q, qid, userAnswer, ['True', 'False', 'Not Given']);
    case 'ynng':
      return renderRadioOptions(q, qid, userAnswer, ['YES', 'NO', 'NOT GIVEN']);
    case 'matching_headings':
    case 'matching_info':
    case 'matching_sentence':
    case 'matching_names':
    case 'matching':
      return renderMatchingHeadings(q, qid, userAnswer);
    case 'sentence_completion':
    case 'summary_completion':
    case 'notes_completion':
    case 'form_completion':
      return renderCompletion(q, qid, userAnswer);
    case 'short_answer':
      return renderCompletion(q, qid, userAnswer);
    default:
      return renderCompletion(q, qid, userAnswer);
  }
}

function renderRadioOptions(q, qid, userAnswer, forcedOptions) {
  const options = forcedOptions || q.options;
  let html = '<div class="options">';
  options.forEach(opt => {
    const selected = userAnswer === opt;
    html += `
      <label class="option-label ${selected ? 'selected' : ''}">
        <input type="radio" name="q_${escapeHtml(qid)}" value="${escapeHtml(opt)}" ${selected ? 'checked' : ''} onchange="saveAnswer('${escapeHtml(qid)}', this.value, this)">
        ${escapeHtml(opt)}
      </label>
    `;
  });
  html += '</div>';
  return html;
}

function renderMatchingHeadings(q, qid, userAnswer) {
  let html = '<div class="options">';
  html += `<select class="matching-select" onchange="saveAnswer('${escapeHtml(qid)}', this.value, this)" style="padding:6px;border:1px solid var(--border-color);border-radius:4px;width:100%;">`;
  html += `<option value="">${t('selectAll')}</option>`;
  q.options.forEach(opt => {
    const selected = userAnswer === opt;
    html += `<option value="${escapeHtml(opt)}" ${selected ? 'selected' : ''}>${escapeHtml(opt)}</option>`;
  });
  html += '</select></div>';
  return html;
}

function renderCheckboxOptions(q, qid, userAnswer) {
  const selected = (userAnswer || '').split(',').map(s => s.trim()).filter(Boolean);
  let html = '<div class="options">';
  (q.options || []).forEach(opt => {
    const checked = selected.includes(opt);
    html += `
      <label class="option-label checkbox-label ${checked ? 'selected' : ''}">
        <input type="checkbox" name="q_${escapeHtml(qid)}" value="${escapeHtml(opt)}" ${checked ? 'checked' : ''} onchange="saveCheckboxAnswer('${escapeHtml(qid)}')">
        ${escapeHtml(opt)}
      </label>
    `;
  });
  html += '</div>';
  return html;
}

function saveCheckboxAnswer(qid) {
  const checked = [];
  document.querySelectorAll(`input[name="q_${qid}"]:checked`).forEach(cb => {
    checked.push(cb.value);
  });
  const value = checked.join(', ');
  if (value) {
    currentAnswers[qid] = value;
  } else {
    delete currentAnswers[qid];
  }
  saveAnswers(currentTestData.id, currentAnswers);

  const questionItem = document.getElementById(`q-${qid}`);
  if (questionItem) {
    if (value) {
      questionItem.classList.add('answered');
    } else {
      questionItem.classList.remove('answered');
    }
  }

  document.querySelectorAll(`#q-${qid} .checkbox-label`).forEach(l => {
    const cb = l.querySelector('input[type="checkbox"]');
    l.classList.toggle('selected', cb && cb.checked);
  });

  updateProgress();
  renderQuestionNav();
}

function renderCompletion(q, qid, userAnswer) {
  return `
    <div class="options">
      <label class="option-label">
        <input type="text" value="${escapeHtml(userAnswer)}" onchange="saveAnswer('${escapeHtml(qid)}', this.value, this)" placeholder="..." style="flex:1;padding:6px;border:1px solid var(--border-color);border-radius:4px;">
      </label>
    </div>
  `;
}

function saveAnswer(qid, value, el) {
  if (value) {
    currentAnswers[qid] = value;
  } else {
    delete currentAnswers[qid];
  }
  saveAnswers(currentTestData.id, currentAnswers);

  // Update UI
  const questionItem = document.getElementById(`q-${qid}`);
  if (questionItem) {
    if (value) {
      questionItem.classList.add('answered');
      questionItem.classList.remove('unanswered');
    } else {
      questionItem.classList.remove('answered');
      questionItem.classList.add('unanswered');
    }
  }

  // Update option label styles
  if (el && el.type === 'radio') {
    document.querySelectorAll(`#q-${qid} .option-label`).forEach(l => l.classList.remove('selected'));
    el.closest('.option-label')?.classList.add('selected');
  }

  updateProgress();
  renderQuestionNav();
}

function toggleFlag(qid) {
  const idx = currentFlagged.indexOf(qid);
  if (idx >= 0) {
    currentFlagged.splice(idx, 1);
  } else {
    currentFlagged.push(qid);
  }
  saveFlagged(currentTestData.id, currentFlagged);

  // Update UI
  const questionItem = document.getElementById(`q-${qid}`);
  if (questionItem) questionItem.classList.toggle('flagged');

  const flagBtn = questionItem?.querySelector('.flag-btn');
  if (flagBtn) {
    flagBtn.classList.toggle('flagged');
    const flaggedNow = currentFlagged.includes(qid);
    flagBtn.textContent = flaggedNow ? t('flagged') : t('flag');
    flagBtn.dataset.i18n = flaggedNow ? 'flagged' : 'flag';
  }

  updateProgress();
  renderQuestionNav();
}

function updateProgress() {
  const answeredEl = document.getElementById('answeredCount');
  const flaggedEl = document.getElementById('flaggedCount');
  if (answeredEl) answeredEl.textContent = Object.keys(currentAnswers).length;
  if (flaggedEl) flaggedEl.textContent = currentFlagged.length;
}

function renderQuestionNav() {
  const nav = document.getElementById('questionNav');
  if (!nav) return;

  const total = allQuestions.length;
  let html = '';
  for (let i = 0; i < total; i++) {
    const q = allQuestions[i];
    const isAnswered = !!currentAnswers[q.id];
    const isFlagged = currentFlagged.includes(q.id);
    const cls = `question-nav-btn ${isAnswered ? 'answered' : ''} ${isFlagged ? 'flagged' : ''}`;
    html += `<button class="${cls}" onclick="scrollToQuestion('${escapeHtml(q.id)}')" aria-label="Question ${i + 1}${isAnswered ? ', answered' : ''}${isFlagged ? ', flagged' : ''}">${i + 1}</button>`;
  }
  if (nav) nav.innerHTML = html;
}

function scrollToQuestion(qid) {
  // Find which passage this question belongs to
  for (let pi = 0; pi < currentTestData.passages.length; pi++) {
    const found = currentTestData.passages[pi].questions.find(q => q.id === qid);
    if (found) {
      if (pi !== currentPassageIndex) switchPassage(pi);
      break;
    }
  }
  // Scroll to question
  setTimeout(() => {
    const el = document.getElementById(`q-${qid}`);
    if (el) el.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }, 100);
}

function showSubmitModal() {
  const unanswered = allQuestions.filter(q => !currentAnswers[q.id]).length;

  const overlay = document.createElement('div');
  overlay.className = 'modal-overlay';
  overlay.innerHTML = `
    <div class="modal">
      <h2 data-i18n="submitConfirm">${t('submitConfirm')}</h2>
      <p data-i18n="submitConfirmDesc">${t('submitConfirmDesc')}</p>
      ${unanswered > 0 ? `<p style="color:var(--color-warning);font-weight:600;">${t('submitWarningUnanswered', { n: unanswered })}</p>` : ''}
      <div class="modal-actions">
        <button class="btn btn-secondary" onclick="this.closest('.modal-overlay').remove()" data-i18n="cancel">${t('cancel')}</button>
        <button class="btn btn-primary" onclick="submitExam()" data-i18n="confirm">${t('confirm')}</button>
      </div>
    </div>
  `;
  document.body.appendChild(overlay);
}

function submitExam() {
  Timer.stop();

  const testData = currentTestData;
  const answers = currentAnswers;

  // Grade
  let correct = 0;
  const results = {};
  allQuestions.forEach(q => {
    const isCorrect = gradeAnswer(answers[q.id], q.correctAnswer, q.type);
    if (isCorrect) correct++;
    results[q.id] = isCorrect;
  });

  const total = allQuestions.length;
  const score = correct;
  const band = bandScore(score);
  const timeTaken = Timer.getTimeUsed();

  // Save as completed exam state
  saveExamState(testData.id, {
    startedAt: Date.now() - timeTaken * 1000,
    completed: true,
    completedAt: Date.now()
  });

  // Collect wrong answers for the wrong answer book
  const wrongAnswers = [];
  allQuestions.forEach((q, idx) => {
    const userAns = (answers[q.id] || '').trim();
    const correctAns = (q.correctAnswer || '').trim().toLowerCase();
    let isCorrect;
    if (q.type === 'multiple_choice_multi') {
      const userParts = userAns.toLowerCase().split(',').map(s => s.trim()).filter(Boolean).sort();
      const correctParts = correctAns.split(',').map(s => s.trim()).filter(Boolean).sort();
      isCorrect = userParts.length === correctParts.length && userParts.every((v, i) => v === correctParts[i]);
    } else {
      isCorrect = userAns.trim().toLowerCase() === correctAns;
    }
    if (!isCorrect) {
      wrongAnswers.push({
        testId: testData.id,
        questionNumber: idx + 1,
        type: q.type,
        question: q.question,
        yourAnswer: userAns,
        correctAnswer: q.correctAnswer
      });
    }
  });

  // Type counts for weak type analysis
  const typeCounts = {};
  allQuestions.forEach(q => {
    if (!typeCounts[q.type]) typeCounts[q.type] = 0;
    typeCounts[q.type]++;
  });

  // Save attempt to history
  saveAttempt({
    testId: testData.id,
    date: new Date().toISOString(),
    score: score,
    total: total,
    bandScore: band,
    timeTaken: timeTaken,
    answers: { ...answers },
    wrongAnswers: wrongAnswers,
    typeCounts: typeCounts
  });

  Timer.clear(testData.id);

  // Close modal
  document.querySelectorAll('.modal-overlay').forEach(el => el.remove());

  // Redirect to review
  window.location.hash = `#/review/${testData.id}`;
}

function autoSubmit() {
  submitExam();
  // Show a brief notification
  const overlay = document.createElement('div');
  overlay.className = 'modal-overlay';
  overlay.innerHTML = `
    <div class="modal">
      <h2 data-i18n="timeUp">${t('timeUp')}</h2>
      <p data-i18n="timeUpDesc">${t('timeUpDesc')}</p>
      <div class="modal-actions">
        <button class="btn btn-primary" onclick="this.closest('.modal-overlay').remove()" data-i18n="viewReview">${t('viewReview')}</button>
      </div>
    </div>
  `;
  document.body.appendChild(overlay);
}

