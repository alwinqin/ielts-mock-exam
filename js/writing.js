let writingTestData = null;
let writingAnswers = {};
let writingCurrentTask = 'task1';
let writingTimer = null;
let writingTimeRemaining = 3600; // 60 min

function writingBeforeUnload(e) {
  if (writingTimer !== null) {
    e.preventDefault();
    e.returnValue = '';
  }
}

function renderWritingExam(testData) {
  writingTestData = testData;
  writingAnswers = loadWritingAnswers(testData.id) || { task1: '', task2: '' };
  writingCurrentTask = 'task1';
  writingTimeRemaining = 3600;

  window.addEventListener('beforeunload', writingBeforeUnload);

  // Restore timer state
  const saved = loadWritingState(testData.id);
  if (saved) {
    writingTimeRemaining = saved.remaining || 3600;
    writingCurrentTask = saved.currentTask || 'task1';
  }

  const container = document.getElementById('mainContent');
  container.innerHTML = `
    <div class="writing-container">
      <div class="writing-topbar">
        <span class="test-title">Writing ${testData.id.toUpperCase()}</span>
        <div class="timer" id="writingTimerDisplay">${formatTime(writingTimeRemaining)}</div>
        <span class="progress-text" id="writingWordCount">
          ${t('wordCount')}: 0/400+ ${t('words')}
        </span>
        <button class="btn btn-primary btn-small" data-action="writing-show-submit">${t('submit')}</button>
      </div>
      <div class="writing-tabs">
        <button class="writing-tab active" data-task="task1" data-action="writing-switch-task">${t('task1')}</button>
        <button class="writing-tab" data-task="task2" data-action="writing-switch-task">${t('task2')}</button>
      </div>
      <div class="writing-main">
        <div class="writing-prompt" id="writingPrompt"></div>
        <div class="writing-editor" id="writingEditor"></div>
      </div>
    </div>
  `;

  renderWritingTask('task1');
  startWritingTimer();
}

function renderWritingTask(task) {
  writingCurrentTask = task;
  document.querySelectorAll('.writing-tab').forEach(t => t.classList.toggle('active', t.dataset.task === task));

  const data = writingTestData[task];
  if (!data) return;

  // Prompt panel
  const promptPanel = document.getElementById('writingPrompt');
  promptPanel.innerHTML = `
    <div class="writing-prompt-header">
      <h3>${task === 'task1' ? t('task1') : t('task2')}</h3>
      <span style="font-size:0.8rem;color:var(--text-muted);">${task === 'task1' ? '150 words, 20 min' : '250 words, 40 min'}</span>
    </div>
    <div class="writing-prompt-body">
      <p><strong>${data.title || ''}</strong></p>
      <p>${data.prompt || ''}</p>
    </div>
  `;

  // Editor panel
  const editorPanel = document.getElementById('writingEditor');
  const userText = writingAnswers[task] || '';
  const wordCount = countWords(userText);

  editorPanel.innerHTML = `
    <div class="writing-editor-area">
      <textarea id="writingTextarea" data-input="writing-input" placeholder="${t('yourWriting')}...">${escapeHtml(userText)}</textarea>
    </div>
    <div class="writing-wordcount">
      <span>${t('wordCount')}: <strong id="wcCount">${wordCount}</strong> ${t('words')}</span>
      <span style="margin-left:16px;color:var(--text-muted);">
        ${task === 'task1' ? t('minWords', { n: 150 }) : t('minWords', { n: 250 })}
      </span>
    </div>
  `;
}

function onWritingInput() {
  const ta = document.getElementById('writingTextarea');
  if (!ta) return;
  writingAnswers[writingCurrentTask] = ta.value;
  saveWritingAnswers(writingTestData.id, writingAnswers);

  const wc = document.getElementById('wcCount');
  if (wc) wc.textContent = countWords(ta.value);

  // Update total word count in topbar
  updateWritingProgress();
}

function updateWritingProgress() {
  const el = document.getElementById('writingWordCount');
  if (!el) return;
  const total = countWords((writingAnswers.task1 || '') + ' ' + (writingAnswers.task2 || ''));
  const task1Words = countWords(writingAnswers.task1 || '');
  const task2Words = countWords(writingAnswers.task2 || '');
  const minMet = task1Words >= 150 && task2Words >= 250;
  el.innerHTML = `${t('wordCount')}: ${total}/400+ ${t('words')}`;
  el.style.color = minMet ? '' : 'var(--color-warning)';
  el.style.fontWeight = minMet ? '' : '600';
}

function countWords(text) {
  if (!text || !text.trim()) return 0;
  return text.trim().split(/\s+/).length;
}

function switchWritingTask(task) {
  if (writingCurrentTask === task) return;
  // Save current textarea content
  const ta = document.getElementById('writingTextarea');
  if (ta) writingAnswers[writingCurrentTask] = ta.value;
  saveWritingAnswers(writingTestData.id, writingAnswers);

  renderWritingTask(task);
}

function startWritingTimer() {
  if (writingTimer) { clearInterval(writingTimer); }

  writingTimer = setInterval(() => {
    writingTimeRemaining--;
    const el = document.getElementById('writingTimerDisplay');
    if (el) {
      el.textContent = formatTime(writingTimeRemaining);
      el.className = 'timer';
      if (writingTimeRemaining <= 120) el.classList.add('danger');
      else if (writingTimeRemaining <= 300) el.classList.add('warning');
    }

    // Save state every 30 seconds
    if (writingTimeRemaining % 30 === 0) {
      const ta = document.getElementById('writingTextarea');
      if (ta) writingAnswers[writingCurrentTask] = ta.value;
      saveWritingAnswers(writingTestData.id, writingAnswers);
      saveWritingState(writingTestData.id, {
        remaining: writingTimeRemaining,
        currentTask: writingCurrentTask
      });
    }

    if (writingTimeRemaining <= 0) {
      clearInterval(writingTimer);
      writingTimer = null;
      showWritingSubmitModal();
    }
  }, 1000);
}

function showWritingSubmitModal() {
  const task1Wc = countWords(writingAnswers.task1 || '');
  const task2Wc = countWords(writingAnswers.task2 || '');

  const overlay = document.createElement('div');
  overlay.className = 'modal-overlay';
  overlay.innerHTML = `
    <div class="modal">
      <h2>${t('submitConfirm')}</h2>
      <p>${t('submitConfirmDesc')}</p>
      <p style="font-size:0.85rem;color:var(--text-secondary);margin-top:8px;">
        ${t('task1')}: ${task1Wc} ${t('words')} | ${t('task2')}: ${task2Wc} ${t('words')}
      </p>
      <div class="modal-actions">
        <button class="btn btn-secondary" data-action="close-modal">${t('cancel')}</button>
        <button class="btn btn-primary" data-action="writing-submit">${t('confirm')}</button>
      </div>
    </div>
  `;
  document.body.appendChild(overlay);
}

function submitWriting() {
  window.removeEventListener('beforeunload', writingBeforeUnload);
  if (writingTimer) { clearInterval(writingTimer); writingTimer = null; }

  // Save final answers
  const ta = document.getElementById('writingTextarea');
  if (ta) writingAnswers[writingCurrentTask] = ta.value;
  saveWritingAnswers(writingTestData.id, writingAnswers);
  saveWritingState(writingTestData.id, { remaining: writingTimeRemaining, currentTask: writingCurrentTask, completed: true });

  document.querySelectorAll('.modal-overlay').forEach(el => el.remove());
  window.location.hash = `#/writing-review/${writingTestData.id}`;
}
