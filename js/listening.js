let listeningTestData = null;
let listeningAnswers = {};
let listeningFlagged = [];
let listeningPhase = 'pre_playback';
let listeningSubPhase = null; // 'preview' | 'playing' | 'section_end'
let listeningCurrentSection = 0;
let listeningCompletedSections = [];
let listeningAudioEl = null;
let listeningAllQuestions = [];
let listeningPhaseTimer = null;

const PREVIEW_SECONDS = 30;

function createAudioElement() {
  if (listeningAudioEl) return;
  listeningAudioEl = document.createElement('audio');
  listeningAudioEl.preload = 'auto';
  document.body.appendChild(listeningAudioEl);
  listeningAudioEl.addEventListener('ended', () => {
    // Audio finished: stay in 'playing' mode, user can click Next Section
    updateAudioBar();
  });
  listeningAudioEl.addEventListener('error', () => {
    console.warn('Audio error on section', listeningCurrentSection);
  });
}

function startSectionPreview(sectionIndex) {
  listeningCurrentSection = sectionIndex;
  listeningSubPhase = 'preview';

  // Show section tabs and questions - but disable question inputs
  switchListeningSection(sectionIndex);
  renderListeningQuestions(sectionIndex, true);
  updateAudioBar();
  renderListeningFooter(); // Footer is rendered FIRST, creating previewTimer element

  // Start 30s preview countdown
  let remaining = PREVIEW_SECONDS;
  if (listeningPhaseTimer) { clearInterval(listeningPhaseTimer); }

  listeningPhaseTimer = setInterval(() => {
    remaining--;
    const previewEl = document.getElementById('previewTimer');
    if (previewEl) {
      previewEl.textContent = `Preview: ${remaining}s`;
      if (remaining <= 5) previewEl.style.color = '#d32f2f';
    }
    if (remaining <= 0) {
      clearInterval(listeningPhaseTimer);
      listeningPhaseTimer = null;
      if (previewEl) previewEl.textContent = 'Preview ended - click Play';
      // Update buttons
      updateAudioBar();
      renderListeningFooter();
    }
  }, 1000);

  // Save state
  saveListeningState(listeningTestData.id, {
    phase: 'playing', subPhase: 'preview',
    currentSection: sectionIndex, completedSections: listeningCompletedSections
  });
}

function startSectionAudio() {
  if (listeningSubPhase !== 'preview' && listeningSubPhase !== 'section_end') return;

  // Stop preview timer
  if (listeningPhaseTimer) { clearInterval(listeningPhaseTimer); listeningPhaseTimer = null; }

  listeningSubPhase = 'playing';

  // Enable question inputs
  renderListeningQuestions(listeningCurrentSection, false);
  updateAudioBar();
  renderListeningFooter();

  // Start audio playback
  playAudioForSection(listeningCurrentSection);
}

function playAudioForSection(sectionIndex) {
  if (!listeningAudioEl) createAudioElement();
  const section = listeningTestData.sections[sectionIndex];
  if (!section) return;

  const audioPath = `data/listening/audio/${section.audioFile || `${listeningTestData.id}_s${sectionIndex + 1}.mp3`}`;
  listeningAudioEl.src = audioPath;
  listeningAudioEl.currentTime = 0;
  listeningAudioEl.play().catch(e => {
    console.warn('Audio play error:', e.message);
    // Still let user proceed even without audio
  });

  saveListeningState(listeningTestData.id, {
    phase: 'playing', subPhase: 'playing',
    currentSection: sectionIndex, completedSections: listeningCompletedSections
  });
}

function completeSection() {
  // Mark section as completed
  if (!listeningCompletedSections.includes(listeningCurrentSection)) {
    listeningCompletedSections.push(listeningCurrentSection);
  }

  // Stop audio
  if (listeningAudioEl) { listeningAudioEl.pause(); listeningAudioEl.src = ''; }

  listeningSubPhase = 'section_end';
  updateAudioBar();
  renderListeningFooter();
  renderListeningQuestions(listeningCurrentSection, true);

  // Mark section tab as played
  document.querySelectorAll('.section-tab').forEach((tab, i) => {
    if (listeningCompletedSections.includes(i)) tab.classList.add('played');
  });

  // Update section content to show "complete" status
  const content = document.querySelector(`.section-content[data-section="${listeningCurrentSection}"]`);
  if (content) {
    let existing = content.querySelector('.section-status');
    if (!existing) {
      const status = document.createElement('div');
      status.className = 'section-status';
      status.textContent = '✓ Completed';
      status.style.cssText = 'color:#2e7d32;font-weight:600;margin-top:8px;';
      content.appendChild(status);
    }
  }

  saveListeningState(listeningTestData.id, {
    phase: 'playing', subPhase: 'section_end',
    currentSection: listeningCurrentSection, completedSections: listeningCompletedSections
  });
}

function nextSection() {
  completeSection();

  const nextIdx = listeningCurrentSection + 1;
  if (nextIdx < listeningTestData.sections.length) {
    // Start next section preview
    startSectionPreview(nextIdx);
  } else {
    // All sections done → transfer phase
    enterTransferPhase();
  }
}

function renderListeningExam(testData) {
  listeningTestData = testData;
  listeningAnswers = loadListeningAnswers(testData.id);
  listeningFlagged = loadListeningFlagged(testData.id);
  listeningCurrentSection = 0;
  listeningCompletedSections = [];
  listeningPhase = 'pre_playback';
  listeningSubPhase = null;

  // Build flat question list
  listeningAllQuestions = [];
  testData.sections.forEach((s, si) => {
    s.questions.forEach(q => {
      listeningAllQuestions.push({ ...q, sectionIndex: si });
    });
  });

  const savedState = loadListeningState(testData.id);
  if (savedState) {
    if (savedState.phase === 'transfer') {
      listeningPhase = 'transfer';
      listeningCompletedSections = savedState.completedSections || [];
      listeningCurrentSection = savedState.currentSection || 0;
    } else if (savedState.phase === 'ended') {
      listeningPhase = 'ended';
      listeningCompletedSections = savedState.completedSections || [];
    } else if (savedState.phase === 'playing' && savedState.subPhase) {
      listeningPhase = 'playing';
      listeningSubPhase = savedState.subPhase;
      listeningCurrentSection = savedState.currentSection || 0;
      listeningCompletedSections = savedState.completedSections || [];
    }
  }

  createAudioElement();

  const container = document.getElementById('mainContent');

  container.innerHTML = `
    <div class="listening-container">
      <div class="listening-topbar">
        <span class="test-title">${testData.id.toUpperCase()} - ${t('listening')}</span>
        <span class="phase-badge" id="phaseBadge">
          ${listeningPhase === 'transfer' ? t('transferPhase') :
            listeningPhase === 'ended' ? t('listeningEnded') :
            listeningSubPhase === 'preview' ? 'Preview Time' :
            listeningSubPhase === 'playing' ? 'Listening' :
            listeningSubPhase === 'section_end' ? 'Section Complete' :
            t('playbackPhase')}
        </span>
        ${listeningPhase === 'transfer' || listeningPhase === 'ended' ? `<div class="timer" id="listeningTimerDisplay">10:00</div>` : ''}
        <span class="progress-text">
          <strong id="listeningAnswered">${Object.keys(listeningAnswers).length}</strong>/40 ${t('answered')}
          | <strong id="listeningFlagged">${listeningFlagged.length}</strong> ${t('flagged')}
        </span>
        ${listeningPhase === 'transfer' ? `<button class="btn btn-primary btn-small" onclick="showListeningSubmitModal()">${t('submit')}</button>` : ''}
      </div>

      <div class="listening-progress-bar" id="listeningProgressBar"></div>

      <div class="listening-main">
        <div class="listening-passage" id="listeningPassagePanel"></div>
        <div class="listening-questions" id="listeningQuestionsPanel"></div>
      </div>
      <div class="listening-footer-bar" id="listeningFooter"></div>
    </div>
  `;

  renderSectionTabs();

  if (listeningPhase === 'pre_playback') {
    // Show start screen
    const panel = document.getElementById('listeningPassagePanel');
    panel.innerHTML = `
      <div style="padding:40px;text-align:center;">
        <h2 style="color:#1a3a5c;margin-bottom:16px;">IELTS Listening Test</h2>
        <p style="color:#666;margin-bottom:8px;">4 sections, 40 questions</p>
        <p style="color:#666;margin-bottom:24px;">Total time: ~30 minutes + 10 minutes transfer</p>
        <button class="btn btn-primary" onclick="startExam()" style="font-size:1.1rem;padding:12px 40px;">
          Start Exam
        </button>
      </div>
    `;
    const qPanel = document.getElementById('listeningQuestionsPanel');
    qPanel.innerHTML = `
      <div style="padding:40px;text-align:center;color:#999;">
        <p>Click "Start Exam" to begin the listening test.</p>
        <p style="margin-top:8px;">Each section has 30 seconds preview time, then audio playback.</p>
      </div>
    `;
  } else if (listeningPhase === 'playing') {
    renderSectionTabs();
    switchListeningSection(listeningCurrentSection);
    renderListeningQuestions(listeningCurrentSection, listeningSubPhase !== 'playing');
    updateAudioBar();
    renderListeningFooter();

    if (listeningSubPhase === 'preview' && listeningPhaseTimer === null) {
      // Resume preview countdown logic handled in startSectionPreview
    }
  } else if (listeningPhase === 'transfer') {
    renderSectionTabs();
    switchListeningSection(listeningCurrentSection);
    renderListeningQuestions(listeningCurrentSection, false);
    updateAudioBar();
    renderListeningFooter();
    startTransferTimer();
  }

  updateListeningProgress();
}

function startExam() {
  listeningPhase = 'playing';
  listeningCurrentSection = 0;
  listeningCompletedSections = [];

  renderSectionTabs();
  renderProgressBar();
  startSectionPreview(0);
}

function renderSectionTabs() {
  const panel = document.getElementById('listeningPassagePanel');
  if (!panel) return;
  let tabsHtml = '<div class="section-tabs">';
  let contentHtml = '';
  listeningTestData.sections.forEach((s, i) => {
    const played = listeningCompletedSections.includes(i);
    const isCurrent = i === listeningCurrentSection;
    const cls = `${isCurrent ? 'active' : ''} ${played ? 'played' : ''}`;
    tabsHtml += `<div class="section-tab ${cls}" onclick="switchListeningSection(${i})">
      ${t('section')} ${i + 1}${played ? ' ✓' : ''}
    </div>`;
    contentHtml += `
      <div class="section-content ${isCurrent ? 'active' : ''}" data-section="${i}">
        <h2>${t('section')} ${i + 1}: ${s.title || ''}</h2>
        <div class="section-subtitle">${s.subtitle || ''}</div>
      </div>
    `;
  });
  tabsHtml += '</div>';
  panel.innerHTML = tabsHtml + contentHtml;
}

function renderProgressBar() {
  const bar = document.getElementById('listeningProgressBar');
  if (!bar) return;
  let html = '<div class="progress-track">';
  listeningTestData.sections.forEach((s, i) => {
    const played = listeningCompletedSections.includes(i);
    const isCurrent = i === listeningCurrentSection;
    const statusClass = played ? 'played' : isCurrent ? 'current' : 'pending';
    const label = `${t('section')} ${i + 1}`;
    html += `<div class="progress-step ${statusClass}">
      <div class="step-dot">${played ? '✓' : i + 1}</div>
      <div class="step-label">${label}</div>
    </div>`;
  });
  html += '</div>';
  bar.innerHTML = html;
}

function switchListeningSection(index) {
  listeningCurrentSection = index;
  document.querySelectorAll('.section-tab').forEach((tab, i) => tab.classList.toggle('active', i === index));
  document.querySelectorAll('.section-content').forEach((el, i) => el.classList.toggle('active', i === index));

  // Only render questions for sections that have been reached
  if (listeningPhase === 'transfer' || listeningCompletedSections.includes(index) || index <= listeningCurrentSection) {
    const disabled = listeningCompletedSections.includes(index) && listeningPhase !== 'transfer';
    renderListeningQuestions(index, disabled);
  } else {
    const qPanel = document.getElementById('listeningQuestionsPanel');
    if (qPanel) qPanel.innerHTML = '<div style="padding:24px;text-align:center;color:#999;">This section is not yet available.</div>';
  }
  updateAudioBar();
}

function renderListeningQuestions(sectionIndex, disabled) {
  const panel = document.getElementById('listeningQuestionsPanel');
  const section = listeningTestData.sections[sectionIndex];
  if (!section || !panel) return;

  let html = '';
  section.questions.forEach((q) => {
    const qid = q.id;
    const userAnswer = listeningAnswers[qid] || '';
    const isFlagged = listeningFlagged.includes(qid);

    html += `<div class="question-item ${isFlagged ? 'flagged' : ''} ${userAnswer ? 'answered' : ''}" id="lq-${qid}">`;
    html += `
      <div class="question-header">
        <span class="question-number">${t('question')} ${getListeningGlobalNum(qid)}</span>
        <button class="flag-btn ${isFlagged ? 'flagged' : ''}" onclick="toggleListeningFlag('${qid}')" ${disabled ? 'disabled' : ''}>${isFlagged ? 'Flagged' : 'Flag'}</button>
      </div>
    `;
    html += `<div class="question-text">${escapeHtml(q.question)}</div>`;
    html += renderListeningQuestionInput(q, qid, userAnswer, disabled);
    html += '</div>';
  });
  panel.innerHTML = html;
}

function getListeningGlobalNum(qid) {
  for (let i = 0; i < listeningAllQuestions.length; i++) {
    if (listeningAllQuestions[i].id === qid) return i + 1;
  }
  return '?';
}

function renderListeningQuestionInput(q, qid, userAnswer, disabled) {
  const ds = disabled ? 'disabled' : '';
  switch (q.type) {
    case 'multiple_choice':
      let mcHtml = '<div class="options">';
      (q.options || []).forEach(opt => {
        const sel = userAnswer === opt;
        mcHtml += `<label class="option-label ${sel ? 'selected' : ''}"><input type="radio" name="lq_${qid}" value="${escapeHtml(opt)}" ${sel ? 'checked' : ''} onchange="saveListeningAnswer('${qid}', this.value)" ${ds}>${escapeHtml(opt)}</label>`;
      });
      mcHtml += '</div>';
      return mcHtml;
    default:
      return `<div class="options"><label class="option-label"><input type="text" value="${escapeHtml(userAnswer)}" onchange="saveListeningAnswer('${qid}', this.value)" placeholder="..." style="flex:1;padding:6px;" ${ds}></label></div>`;
  }
}

function updateListeningProgress() {
  const ae = document.getElementById('listeningAnswered');
  const fe = document.getElementById('listeningFlagged');
  if (ae) ae.textContent = Object.keys(listeningAnswers).length;
  if (fe) fe.textContent = listeningFlagged.length;
}

function saveListeningAnswer(qid, value) {
  if (listeningSubPhase === 'preview' || listeningSubPhase === 'section_end') return;
  listeningAnswers[qid] = value;
  saveListeningAnswers(listeningTestData.id, listeningAnswers);
  const qi = document.getElementById(`lq-${qid}`);
  if (qi) qi.classList.add('answered');
  updateListeningProgress();
}

function toggleListeningFlag(qid) {
  const idx = listeningFlagged.indexOf(qid);
  if (idx >= 0) listeningFlagged.splice(idx, 1);
  else listeningFlagged.push(qid);
  saveListeningFlagged(listeningTestData.id, listeningFlagged);
  const qi = document.getElementById(`lq-${qid}`);
  if (qi) qi.classList.toggle('flagged');
  updateListeningProgress();
}

function updateAudioBar() {
  const phaseBadge = document.getElementById('phaseBadge');
  if (!phaseBadge) return;

  if (listeningSubPhase === 'preview') {
    phaseBadge.textContent = 'Preview Time';
    phaseBadge.className = 'phase-badge preview';
  } else if (listeningSubPhase === 'playing') {
    phaseBadge.textContent = `Listening - Section ${listeningCurrentSection + 1}`;
    phaseBadge.className = 'phase-badge playback';
  } else if (listeningSubPhase === 'section_end') {
    phaseBadge.textContent = 'Section Complete';
    phaseBadge.className = 'phase-badge ended';
  } else if (listeningPhase === 'transfer') {
    phaseBadge.textContent = t('transferPhase');
    phaseBadge.className = 'phase-badge transfer';
  } else if (listeningPhase === 'pre_playback') {
    phaseBadge.textContent = t('playbackPhase');
    phaseBadge.className = 'phase-badge';
  }
}

function renderListeningFooter() {
  const footer = document.getElementById('listeningFooter');
  if (!footer) return;

  if (listeningPhase === 'pre_playback') {
    footer.innerHTML = '';
    return;
  }
  if (listeningPhase === 'transfer') {
    footer.innerHTML = `
      <div class="listening-footer-bar">
        <button class="btn btn-primary" onclick="showListeningSubmitModal()">${t('submit')}</button>
        <span style="margin-left:12px;font-size:0.85rem;color:#666;">${t('transferDesc')}</span>
      </div>
    `;
    return;
  }
  if (listeningPhase === 'ended') {
    footer.innerHTML = '';
    return;
  }

  if (listeningSubPhase === 'preview') {
    footer.innerHTML = `
      <div class="listening-footer-bar">
        <span style="font-size:0.85rem;color:#e65100;font-weight:600;">
          Preview Time: <span id="previewTimer">Preview: ${PREVIEW_SECONDS}s</span>
        </span>
        <span style="margin-left:12px;font-size:0.85rem;color:#888;">Read the questions. You cannot answer during preview.</span>
        <button class="btn btn-primary btn-small" onclick="startSectionAudio()" style="margin-left:auto;">Start Audio ▸</button>
      </div>
    `;
  } else if (listeningSubPhase === 'playing') {
    const nextBtn = listeningCurrentSection < listeningTestData.sections.length - 1 ?
      `<button class="btn btn-primary btn-small" onclick="nextSection()" style="margin-left:8px;">Complete Section & Next ▸</button>` :
      `<button class="btn btn-primary btn-small" onclick="nextSection()" style="margin-left:8px;">Finish & Start Transfer ▸</button>`;
    footer.innerHTML = `
      <div class="listening-footer-bar">
        <button class="play-btn" onclick="if(listeningAudioEl && listeningAudioEl.paused) { listeningAudioEl.play(); } else if(listeningAudioEl) { listeningAudioEl.pause(); }">
          ${listeningAudioEl && !listeningAudioEl.paused ? 'Pause' : 'Play'}
        </button>
        <span style="margin-left:8px;font-size:0.85rem;color:#888;">Section ${listeningCurrentSection + 1} - Answer the questions while listening</span>
        ${nextBtn}
      </div>
    `;
  } else if (listeningSubPhase === 'section_end') {
    footer.innerHTML = `
      <div class="listening-footer-bar">
        <span style="color:#2e7d32;font-weight:600;">Section ${listeningCurrentSection + 1} Completed ✓</span>
        <button class="btn btn-primary btn-small" onclick="nextSection()" style="margin-left:12px;">
          ${listeningCurrentSection < listeningTestData.sections.length - 1 ? 'Start Section ' + (listeningCurrentSection + 2) + ' ▸' : 'Start 10-min Transfer ▸'}
        </button>
      </div>
    `;
  }
}

function enterTransferPhase() {
  listeningPhase = 'transfer';
  listeningSubPhase = null;

  if (listeningPhaseTimer) { clearInterval(listeningPhaseTimer); listeningPhaseTimer = null; }
  if (listeningAudioEl) { listeningAudioEl.pause(); listeningAudioEl.src = ''; }

  // Change UI
  const topbar = document.querySelector('.listening-topbar');
  if (topbar) {
    const timerEl = document.createElement('div');
    timerEl.id = 'listeningTimerDisplay';
    timerEl.className = 'timer';
    timerEl.textContent = '10:00';
    const progText = topbar.querySelector('.progress-text');
    if (progText) progText.parentNode.insertBefore(timerEl, progText);

    if (!topbar.querySelector('.btn-primary')) {
      const submitBtn = document.createElement('button');
      submitBtn.className = 'btn btn-primary btn-small';
      submitBtn.onclick = showListeningSubmitModal;
      submitBtn.textContent = t('submit');
      topbar.appendChild(submitBtn);
    }
  }

  // Enable all question inputs in all sections
  listeningCompletedSections = [0, 1, 2, 3]; // mark all as accessible
  renderSectionTabs();
  renderProgressBar();
  switchListeningSection(0);
  renderListeningQuestions(0, false);
  updateAudioBar();
  renderListeningFooter();
  startTransferTimer();

  saveListeningState(listeningTestData.id, { phase: 'transfer', completedSections: [0,1,2,3] });
}

function startTransferTimer() {
  if (listeningPhaseTimer) { clearInterval(listeningPhaseTimer); }
  let remaining = 600;

  listeningPhaseTimer = setInterval(() => {
    remaining--;
    const el = document.getElementById('listeningTimerDisplay');
    if (el) {
      el.textContent = formatTime(remaining);
      el.className = 'timer';
      if (remaining <= 60) el.classList.add('danger');
      else if (remaining <= 120) el.classList.add('warning');
    }
    const st = loadListeningState(listeningTestData.id) || {};
    st.transferRemaining = remaining;
    saveListeningState(listeningTestData.id, st);
    if (remaining <= 0) {
      clearInterval(listeningPhaseTimer);
      listeningPhaseTimer = null;
      listeningSubmitExam(true);
    }
  }, 1000);
}

function showListeningSubmitModal() {
  const unanswered = listeningAllQuestions.filter(q => !listeningAnswers[q.id]).length;
  const overlay = document.createElement('div');
  overlay.className = 'modal-overlay';
  overlay.innerHTML = `
    <div class="modal">
      <h2>${t('submitConfirm')}</h2>
      <p>${t('submitConfirmDesc')}</p>
      ${unanswered > 0 ? `<p style="color:#e65100;font-weight:600;">${t('submitWarningUnanswered', { n: unanswered })}</p>` : ''}
      <div class="modal-actions">
        <button class="btn btn-secondary" onclick="this.closest('.modal-overlay').remove()">${t('cancel')}</button>
        <button class="btn btn-primary" onclick="listeningSubmitExam()">${t('confirm')}</button>
      </div>
    </div>
  `;
  document.body.appendChild(overlay);
}

function listeningSubmitExam(isAuto) {
  if (listeningPhaseTimer) { clearInterval(listeningPhaseTimer); listeningPhaseTimer = null; }
  if (listeningAudioEl) { listeningAudioEl.pause(); listeningAudioEl.src = ''; }

  let correct = 0;
  const wrongItems = [];
  listeningAllQuestions.forEach((q, idx) => {
    const userAns = (listeningAnswers[q.id] || '').trim().toLowerCase();
    const correctAns = (q.correctAnswer || '').trim().toLowerCase();
    const isCorrect = userAns === correctAns;
    if (isCorrect) correct++;
    else {
      wrongItems.push({
        testId: listeningTestData.id,
        questionNumber: idx + 1,
        type: q.type,
        question: q.question,
        yourAnswer: listeningAnswers[q.id] || '',
        correctAnswer: q.correctAnswer
      });
    }
  });

  const score = correct;
  const band = bandScore(score);

  // Type counts for weak type analysis
  const typeCounts = {};
  listeningAllQuestions.forEach(q => {
    if (!typeCounts[q.type]) typeCounts[q.type] = 0;
    typeCounts[q.type]++;
  });

  saveListeningState(listeningTestData.id, { phase: 'ended', completed: true });

  saveListeningAttempt({
    testId: listeningTestData.id,
    date: new Date().toISOString(),
    score: score,
    total: 40,
    bandScore: band,
    answers: { ...listeningAnswers },
    wrongAnswers: wrongItems,
    typeCounts: typeCounts
  });

  document.querySelectorAll('.modal-overlay').forEach(el => el.remove());

  if (isAuto) {
    const overlay = document.createElement('div');
    overlay.className = 'modal-overlay';
    overlay.innerHTML = `
      <div class="modal">
        <h2>${t('timeUp')}</h2>
        <p>${t('listening')} ${t('examEnded')}</p>
        <div class="modal-actions">
          <button class="btn btn-primary" onclick="this.closest('.modal-overlay').remove(); window.location.hash='#/listening-review/${listeningTestData.id}'">${t('viewReview')}</button>
        </div>
      </div>
    `;
    document.body.appendChild(overlay);
  } else {
    window.location.hash = `#/listening-review/${listeningTestData.id}`;
  }
}
