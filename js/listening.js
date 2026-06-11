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
let listeningPreResolvedAudioSrc = null;

const PREVIEW_SECONDS = 30;
const PLAYBACK_RATES = [0.5, 0.75, 1, 1.25, 1.5];
let listeningPlaybackRate = 1;

function createAudioElement() {
  if (!listeningAudioEl) {
    listeningAudioEl = document.createElement('audio');
    listeningAudioEl.preload = 'auto';
    listeningAudioEl.controls = true;
    listeningAudioEl.style.cssText = 'display:none;width:100%;max-width:100%;border-radius:4px;';
    listeningAudioEl.addEventListener('ended', () => {
      updateAudioBar();
    });
    listeningAudioEl.addEventListener('error', () => {
      console.warn('Audio error on section', listeningCurrentSection);
      const el = document.getElementById('audioErrorMsg');
      if (el) el.style.display = 'block';
    });
    listeningAudioEl.addEventListener('loadedmetadata', () => {
      updateAudioBar();
      const el = document.getElementById('audioErrorMsg');
      if (el) el.style.display = 'none';
    });
    listeningAudioEl.addEventListener('timeupdate', () => {
      updateAudioTimeDisplay();
    });
  }
  // Ensure audio element is in the inline container (handles re-renders)
  const container = document.getElementById('audioPlayerContainer');
  if (container && listeningAudioEl.parentNode !== container) {
    container.appendChild(listeningAudioEl);
  }
  // Render speed controls
  renderSpeedControls();
}

function setPlaybackRate(rate) {
  listeningPlaybackRate = rate;
  if (listeningAudioEl) {
    listeningAudioEl.playbackRate = rate;
  }
  renderSpeedControls();
}

function renderSpeedControls() {
  const container = document.getElementById('audioPlayerContainer');
  if (!container) return;
  // Remove existing speed controls
  const existing = container.querySelector('.speed-controls');
  if (existing) existing.remove();
  // Create speed controls
  const speedDiv = document.createElement('div');
  speedDiv.className = 'speed-controls';
  speedDiv.innerHTML = PLAYBACK_RATES.map(function(r) {
    const active = r === listeningPlaybackRate ? ' active' : '';
    return '<button class="speed-btn' + active + '" data-action="set-playback-rate" data-rate="' + r + '" aria-label="Playback speed ' + r + 'x" aria-pressed="' + (r === listeningPlaybackRate) + '">' + r + 'x</button>';
  }).join('');
  container.appendChild(speedDiv);
}

function showAudioPlayer() {
  if (listeningAudioEl) listeningAudioEl.style.display = 'block';
  const container = document.getElementById('audioPlayerContainer');
  if (container) container.style.display = 'flex';
}
function hideAudioPlayer() {
  if (listeningAudioEl) { listeningAudioEl.pause(); listeningAudioEl.src = ''; listeningAudioEl.style.display = 'none'; }
  const container = document.getElementById('audioPlayerContainer');
  if (container) container.style.display = 'none';
}

function startSectionPreview(sectionIndex) {
  listeningCurrentSection = sectionIndex;
  listeningSubPhase = 'preview';
  resolveAudioSrc(sectionIndex);

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
      previewEl.textContent = `${t('previewCountdown', { n: remaining })}`;
      if (remaining <= 5) previewEl.style.color = 'var(--color-danger)';
    }
    if (remaining <= 0) {
      clearInterval(listeningPhaseTimer);
      listeningPhaseTimer = null;
      if (previewEl) previewEl.textContent = t('previewEnded');
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

function resolveAudioSrc(sectionIndex) {
  const section = listeningTestData.sections[sectionIndex];
  if (!section) return Promise.resolve(null);
  const isCambridge = listeningTestData._source === 'cambridge' || listeningTestData.id.startsWith('cam');
  const audioPrefix = isCambridge ? 'data/cambridge/audio/' : 'data/listening/audio/';
  const audioFile = section.audioFile || `${listeningTestData.id}_s${sectionIndex + 1}.mp3`;
  var relativePath = audioPrefix + audioFile;

  if (window.__TAURI__ || window.__TAURI_INTERNALS__) {
    var invokeFn = (window.__TAURI__ && window.__TAURI__.core && window.__TAURI__.core.invoke) || (window.__TAURI_INTERNALS__ && window.__TAURI_INTERNALS__.invoke);
    var convertFn = (window.__TAURI__ && window.__TAURI__.core && window.__TAURI__.core.convertFileSrc) || (window.__TAURI_INTERNALS__ && window.__TAURI_INTERNALS__.convertFileSrc);
    if (invokeFn && convertFn) {
      return invokeFn('get_audio_path', { testId: listeningTestData.id, sectionIdx: sectionIndex }).then(function(audioDir) {
        listeningPreResolvedAudioSrc = convertFn(audioDir + '/' + audioFile);
        return listeningPreResolvedAudioSrc;
      }).catch(function(e) {
        console.warn('Tauri audio path error:', e);
        listeningPreResolvedAudioSrc = relativePath;
        return null;
      });
    } else {
      listeningPreResolvedAudioSrc = relativePath;
      return Promise.resolve(null);
    }
  } else {
    listeningPreResolvedAudioSrc = relativePath;
    return Promise.resolve(listeningPreResolvedAudioSrc);
  }
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
  var section = listeningTestData.sections[sectionIndex];
  if (!section) return;

  // Use pre-resolved URL if available, otherwise fall back to resolving now
  if (listeningPreResolvedAudioSrc) {
    listeningAudioEl.src = listeningPreResolvedAudioSrc;
    listeningPreResolvedAudioSrc = null;
  } else {
    var isCambridge = listeningTestData._source === 'cambridge' || listeningTestData.id.startsWith('cam');
    var audioPrefix = isCambridge ? 'data/cambridge/audio/' : 'data/listening/audio/';
    var audioFile = section.audioFile || `${listeningTestData.id}_s${sectionIndex + 1}.mp3`;
    listeningAudioEl.src = audioPrefix + audioFile;
  }

  listeningAudioEl.currentTime = 0;
  listeningAudioEl.playbackRate = listeningPlaybackRate;
  listeningAudioEl.play().catch(function(e) {
    console.warn('Audio play error:', e.message);
    var el = document.getElementById('audioErrorMsg');
    if (el) el.style.display = 'block';
  });

  // Show audio player
  showAudioPlayer();

  saveListeningState(listeningTestData.id, {
    phase: 'playing', subPhase: 'playing',
    currentSection: sectionIndex, completedSections: listeningCompletedSections
  });
}

function updateAudioTimeDisplay() {
  const el = document.getElementById('audioTimeDisplay');
  if (!el || !listeningAudioEl) return;
  const cur = formatTime(Math.floor(listeningAudioEl.currentTime));
  const dur = listeningAudioEl.duration ? formatTime(Math.floor(listeningAudioEl.duration)) : '--:--';
  const pct = listeningAudioEl.duration ? Math.round((listeningAudioEl.currentTime / listeningAudioEl.duration) * 100) : 0;
  el.innerHTML = `<span>${cur} / ${dur}</span><div class="mini-progress"><div class="mini-progress-fill" style="width:${pct}%"></div></div>`;
}

function completeSection() {
  // Mark section as completed
  if (!listeningCompletedSections.includes(listeningCurrentSection)) {
    listeningCompletedSections.push(listeningCurrentSection);
  }

  // Stop audio
  hideAudioPlayer();

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
      status.textContent = t('sectionCompleted');
      status.style.cssText = 'color:var(--color-success);font-weight:600;margin-top:8px;';
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
  if (listeningPhaseTimer) { clearInterval(listeningPhaseTimer); listeningPhaseTimer = null; }
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

  const container = document.getElementById('mainContent');

  container.innerHTML = `
    <div class="listening-container">
      <div class="listening-topbar">
        <span class="test-title">${testData.id.toUpperCase()} - ${t('listening')}</span>
        <span class="phase-badge" id="phaseBadge" aria-live="polite">
          ${listeningPhase === 'transfer' ? t('transferPhase') :
            listeningPhase === 'ended' ? t('listeningEnded') :
            listeningSubPhase === 'preview' ? t('previewTime') :
            listeningSubPhase === 'playing' ? t('listeningPhaseLabel') :
            listeningSubPhase === 'section_end' ? t('sectionCompleteStatus') :
            t('playbackPhase')}
        </span>
        ${listeningPhase === 'transfer' || listeningPhase === 'ended' ? `<div class="timer" id="listeningTimerDisplay" role="timer" aria-live="polite" aria-label="Transfer time remaining: 10 minutes">10:00</div>` : ''}
        <span id="audioTimeDisplay" style="font-size:0.8rem;color:var(--text-muted);"></span>
        <span id="audioErrorMsg" style="display:none;color:var(--color-warning);font-size:0.8rem;">${t('audioNotAvailable')}</span>
        <span class="progress-text">
          <strong id="listeningAnswered">${Object.keys(listeningAnswers).length}</strong>/40 ${t('answered')}
          | <strong id="listeningFlagged">${listeningFlagged.length}</strong> ${t('flagged')}
        </span>
        ${listeningPhase === 'transfer' ? `<button class="btn btn-primary btn-small" data-action="show-listening-submit">${t('submit')}</button>` : ''}
      </div>

      <div class="listening-progress-bar" id="listeningProgressBar"></div>

      <div id="audioPlayerContainer" class="audio-bar" style="display:none;"></div>

      <div class="listening-main">
        <div class="listening-passage" id="listeningPassagePanel"></div>
        <div class="listening-questions" id="listeningQuestionsPanel"></div>
      </div>
      <div class="listening-footer-bar" id="listeningFooter"></div>
    </div>
  `;

  // Must be called after DOM is created so #audioPlayerContainer exists
  createAudioElement();

  renderSectionTabs();

  if (listeningPhase === 'pre_playback') {
    // Show start screen
    const panel = document.getElementById('listeningPassagePanel');
    panel.innerHTML = `
      <div style="padding:40px;text-align:center;">
        <h2 style="color:var(--text-heading);margin-bottom:16px;">${t('listeningTestTitle')}</h2>
        <p style="color:var(--text-secondary);margin-bottom:8px;">${t('listeningTestInfo')}</p>
        <p style="color:var(--text-secondary);margin-bottom:24px;">${t('listeningTestTime')}</p>
        <button class="btn btn-primary" data-action="start-listening-exam" style="font-size:1.1rem;padding:12px 40px;">
          ${t('startExam')}
        </button>
      </div>
    `;
    const qPanel = document.getElementById('listeningQuestionsPanel');
    qPanel.innerHTML = `
      <div style="padding:40px;text-align:center;color:var(--text-muted);">
        <p>${t('listeningStartHint')}</p>
        <p style="margin-top:8px;">${t('listeningPreviewHint')}</p>
      </div>
    `;
  } else if (listeningPhase === 'playing') {
    renderSectionTabs();
    switchListeningSection(listeningCurrentSection);
    renderListeningQuestions(listeningCurrentSection, listeningSubPhase !== 'playing');
    updateAudioBar();
    renderListeningFooter();

    if (listeningSubPhase === 'preview' && listeningPhaseTimer === null) {
      startSectionPreview(listeningCurrentSection);
    } else if (listeningSubPhase === 'playing') {
      resolveAudioSrc(listeningCurrentSection).then(function() {
        playAudioForSection(listeningCurrentSection);
      });
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
    tabsHtml += `<div class="section-tab ${cls}" id="section-tab-${i}" role="tab" aria-selected="${isCurrent}" aria-controls="section-content-${i}" data-action="switch-listening-section" data-section="${i}">
      ${t('section')} ${i + 1}${played ? ' ✓' : ''}
    </div>`;
    contentHtml += `
      <div class="section-content ${isCurrent ? 'active' : ''}" id="section-content-${i}" role="tabpanel" aria-labelledby="section-tab-${i}">
        <h2>${t('section')} ${i + 1}: ${s.title || ''}</h2>
        <div class="section-subtitle">${s.subtitle || ''}</div>
        ${renderSectionContext(s)}
      </div>
    `;
  });
  tabsHtml += '</div>';
  panel.innerHTML = tabsHtml + contentHtml;
}

function renderSectionContext(section) {
  if (!section || !section.questions || section.questions.length === 0) return '';
  const qTypes = new Set(section.questions.map(q => q.type));
  const formTypes = ['notes_completion', 'form_completion', 'summary_completion', 'sentence_completion'];
  const hasFormContent = section.questions.some(q => formTypes.includes(q.type));
  if (!hasFormContent) return '';

  let html = '<div class="listening-context-box">';
  html += '<div class="listening-context-text">';
  section.questions.forEach((q, idx) => {
    let displayText = q.question.replace(/^\\d+\\.\\s*/, '');
    // Fallback for placeholder questions
    if (/^Question\s+\d+/.test(displayText) || displayText === 'ONE WORD ONLY.' || displayText === 'ONE WORD AND/OR A NUMBER.') {
      displayText = 'Question ' + (idx + 1) + ' - refer to the original question paper';
    }
    html += `<span class="context-line"><span class="context-num">${idx + 1}</span> ${escapeHtml(displayText)}</span>`;
  });
  html += '</div></div>';
  return html;
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
  const prevSection = listeningCurrentSection;
  listeningCurrentSection = index;
  document.querySelectorAll('.section-tab').forEach((tab, i) => { tab.classList.toggle('active', i === index); tab.setAttribute('aria-selected', i === index); });
  document.querySelectorAll('.section-content').forEach((el, i) => el.classList.toggle('active', i === index));

  // Only render questions for sections that have been reached
  if (listeningPhase === 'transfer' || listeningCompletedSections.includes(index) || index <= prevSection) {
    const disabled = listeningCompletedSections.includes(index) && listeningPhase !== 'transfer';
    renderListeningQuestions(index, disabled);
  } else {
    const qPanel = document.getElementById('listeningQuestionsPanel');
    if (qPanel) qPanel.innerHTML = '<div style="padding:24px;text-align:center;color:var(--text-muted);">' + t('sectionNotAvailable') + '</div>';
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
        <button class="flag-btn ${isFlagged ? 'flagged' : ''}" data-action="toggle-listening-flag" data-qid="${qid}" ${disabled ? 'disabled' : ''} aria-label="${isFlagged ? t('unflag') : t('flag')} question ${getListeningGlobalNum(qid)}">${isFlagged ? t('flagged') : t('flag')}</button>
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
      // Detect if options are just letter labels (missing full text)
      const areLabels = (q.options || []).every(opt => opt.length <= 2);
      (q.options || []).forEach(opt => {
        const sel = userAnswer === opt;
        const label = areLabels ? t('optionLetter', { n: opt }) : opt;
        mcHtml += `<label class="option-label ${sel ? 'selected' : ''}"><input type="radio" name="lq_${qid}" value="${escapeHtml(opt)}" ${sel ? 'checked' : ''} data-change="save-listening-answer" data-qid="${qid}" ${ds}>${escapeHtml(label)}</label>`;
      });
      if (areLabels && (q.options || []).length > 0) {
        mcHtml += '<div class="option-hint">' + t('referToPaper') + '</div>';
      }
      mcHtml += '</div>';
      return mcHtml;
    case 'multiple_choice_multi':
      return renderListeningCheckboxOptions(q, qid, userAnswer, disabled);
    case 'tfng':
      return renderListeningRadioOptions(q, qid, userAnswer, ['True', 'False', 'Not Given'], disabled);
    case 'ynng':
      return renderListeningRadioOptions(q, qid, userAnswer, ['YES', 'NO', 'NOT GIVEN'], disabled);
    case 'matching_headings':
    case 'matching_info':
    case 'matching_sentence':
    case 'matching_names':
    case 'matching':
      return renderListeningMatching(q, qid, userAnswer, disabled);
    case 'sentence_completion':
    case 'summary_completion':
    case 'notes_completion':
    case 'form_completion':
    case 'short_answer':
      return `<div class="options"><label class="option-label"><input type="text" value="${escapeHtml(userAnswer)}" data-change="save-listening-answer" data-qid="${qid}" placeholder="..." style="flex:1;padding:6px;" ${ds}></label></div>`;
    default:
      return `<div class="options"><label class="option-label"><input type="text" value="${escapeHtml(userAnswer)}" data-change="save-listening-answer" data-qid="${qid}" placeholder="..." style="flex:1;padding:6px;" ${ds}></label></div>`;
  }
}

function renderListeningRadioOptions(q, qid, userAnswer, options, disabled) {
  const ds = disabled ? 'disabled' : '';
  let html = '<div class="options">';
  options.forEach(opt => {
    const sel = userAnswer === opt;
    html += `<label class="option-label ${sel ? 'selected' : ''}"><input type="radio" name="lq_${qid}" value="${escapeHtml(opt)}" ${sel ? 'checked' : ''} data-change="save-listening-answer" data-qid="${qid}" ${ds}>${escapeHtml(opt)}</label>`;
  });
  html += '</div>';
  return html;
}

function renderListeningCheckboxOptions(q, qid, userAnswer, disabled) {
  const ds = disabled ? 'disabled' : '';
  const selected = (userAnswer || '').split(',').map(s => s.trim()).filter(Boolean);
  let html = '<div class="options">';
  (q.options || []).forEach(opt => {
    const checked = selected.includes(opt);
    html += `<label class="option-label checkbox-label ${checked ? 'selected' : ''}"><input type="checkbox" name="lq_${qid}" value="${escapeHtml(opt)}" ${checked ? 'checked' : ''} data-change="save-listening-checkbox" data-qid="${qid}" ${ds}>${escapeHtml(opt)}</label>`;
  });
  html += '</div>';
  return html;
}

function renderListeningMatching(q, qid, userAnswer, disabled) {
  const ds = disabled ? 'disabled' : '';
  let html = '<div class="options">';
  html += `<select class="matching-select" data-change="save-listening-answer" data-qid="${escapeHtml(qid)}" style="padding:6px;border:1px solid var(--border-color);border-radius:4px;width:100%;" ${ds}>`;
  html += `<option value="">${t('selectAll')}</option>`;
  (q.options || []).forEach(opt => {
    const sel = userAnswer === opt;
    html += `<option value="${escapeHtml(opt)}" ${sel ? 'selected' : ''}>${escapeHtml(opt)}</option>`;
  });
  html += '</select></div>';
  return html;
}

function saveListeningCheckboxAnswer(qid) {
  if (listeningSubPhase === 'preview' || listeningSubPhase === 'section_end') return;
  const checked = [];
  document.querySelectorAll(`input[name="lq_${qid}"]:checked`).forEach(cb => {
    checked.push(cb.value);
  });
  const value = checked.join(', ');
  listeningAnswers[qid] = value;
  saveListeningAnswers(listeningTestData.id, listeningAnswers);
  const qi = document.getElementById(`lq-${qid}`);
  if (qi) {
    if (value) qi.classList.add('answered');
    else qi.classList.remove('answered');
  }
  document.querySelectorAll(`#lq-${qid} .checkbox-label`).forEach(l => {
    const cb = l.querySelector('input[type="checkbox"]');
    l.classList.toggle('selected', cb && cb.checked);
  });
  updateListeningProgress();
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
  if (qi) {
    if (value) qi.classList.add('answered');
    else qi.classList.remove('answered');
  }
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
    phaseBadge.textContent = t('previewTime');
    phaseBadge.className = 'phase-badge preview';
  } else if (listeningSubPhase === 'playing') {
    phaseBadge.textContent = t('listeningSectionPhase', { n: listeningCurrentSection + 1 });
    phaseBadge.className = 'phase-badge playback';
  } else if (listeningSubPhase === 'section_end') {
    phaseBadge.textContent = t('sectionCompleteStatus');
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
        <button class="btn btn-primary" data-action="show-listening-submit">${t('submit')}</button>
        <span style="margin-left:12px;font-size:0.85rem;color:var(--text-secondary);">${t('transferDesc')}</span>
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
        <span style="font-size:0.85rem;color:var(--color-warning);font-weight:600;">
          ${t('previewTimeLabel')}<span id="previewTimer" aria-live="polite">${t('previewCountdown', { n: PREVIEW_SECONDS })}</span>
        </span>
        <span style="margin-left:12px;font-size:0.85rem;color:var(--text-muted);">${t('readQuestionsHint')}</span>
        <button class="btn btn-primary btn-small" data-action="start-section-audio" style="margin-left:auto;">${t('startAudioBtn')}</button>
      </div>
    `;
  } else if (listeningSubPhase === 'playing') {
    const nextBtn = listeningCurrentSection < listeningTestData.sections.length - 1 ?
      `<button class="btn btn-primary btn-small" data-action="next-section" style="margin-left:8px;">${t('completeSectionBtn')}</button>` :
      `<button class="btn btn-primary btn-small" data-action="next-section" style="margin-left:8px;">${t('finishTransferBtn')}</button>`;
    footer.innerHTML = `
      <div class="listening-footer-bar">
        <button class="play-btn" data-action="toggle-play-pause">
          ${listeningAudioEl && !listeningAudioEl.paused ? t('pauseAudio') : t('playAudio')}
        </button>
        <span style="margin-left:8px;font-size:0.85rem;color:var(--text-muted);">${t('sectionAnswerHint', { n: listeningCurrentSection + 1 })}</span>
        ${nextBtn}
      </div>
    `;
  } else if (listeningSubPhase === 'section_end') {
    footer.innerHTML = `
      <div class="listening-footer-bar">
        <span style="color:var(--color-success);font-weight:600;">${t('sectionCompletedLabel', { n: listeningCurrentSection + 1 })}</span>
        <button class="btn btn-primary btn-small" data-action="next-section" style="margin-left:12px;">
          ${listeningCurrentSection < listeningTestData.sections.length - 1 ? t('startSectionBtn', { n: listeningCurrentSection + 2 }) : t('startTransferBtn')}
        </button>
      </div>
    `;
  }
}

function enterTransferPhase() {
  listeningPhase = 'transfer';
  listeningSubPhase = null;

  if (listeningPhaseTimer) { clearInterval(listeningPhaseTimer); listeningPhaseTimer = null; }
  hideAudioPlayer();

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
      submitBtn.setAttribute('data-action', 'show-listening-submit');
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
  const st = loadListeningState(listeningTestData.id) || {};
  let remaining = st.transferRemaining || 600;

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
      ${unanswered > 0 ? `<p style="color:var(--color-warning);font-weight:600;">${t('submitWarningUnanswered', { n: unanswered })}</p>` : ''}
      <div class="modal-actions">
        <button class="btn btn-secondary" data-action="close-modal">${t('cancel')}</button>
        <button class="btn btn-primary" data-action="listening-submit-exam">${t('confirm')}</button>
      </div>
    </div>
  `;
  document.body.appendChild(overlay);
}

function listeningSubmitExam(isAuto) {
  if (listeningPhaseTimer) { clearInterval(listeningPhaseTimer); listeningPhaseTimer = null; }
  hideAudioPlayer();

  let correct = 0;
  const wrongItems = [];
  listeningAllQuestions.forEach((q, idx) => {
    const isCorrect = gradeAnswer(listeningAnswers[q.id], q.correctAnswer, q.type);
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
          <button class="btn btn-primary" data-action="close-auto-submit" data-redirect="#/listening-review/${listeningTestData.id}">${t('viewReview')}</button>
        </div>
      </div>
    `;
    document.body.appendChild(overlay);
  } else {
    window.location.hash = `#/listening-review/${listeningTestData.id}`;
  }
}
