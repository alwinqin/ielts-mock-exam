// localStorage helpers

function loadExamState(testId) {
  try {
    const data = localStorage.getItem(`exam_state_${testId}`);
    return data ? JSON.parse(data) : null;
  } catch { return null; }
}

function saveExamState(testId, state) {
  localStorage.setItem(`exam_state_${testId}`, JSON.stringify(state));
}

function loadAnswers(testId) {
  try {
    const data = localStorage.getItem(`user_answers_${testId}`);
    return data ? JSON.parse(data) : {};
  } catch { return {}; }
}

function saveAnswers(testId, answers) {
  localStorage.setItem(`user_answers_${testId}`, JSON.stringify(answers));
}

function loadFlagged(testId) {
  try {
    const data = localStorage.getItem(`flagged_${testId}`);
    return data ? JSON.parse(data) : [];
  } catch { return []; }
}

function saveFlagged(testId, flagged) {
  localStorage.setItem(`flagged_${testId}`, JSON.stringify(flagged));
}

function getAttemptHistory() {
  try {
    const data = localStorage.getItem('attempt_history');
    return data ? JSON.parse(data) : [];
  } catch { return []; }
}

function saveAttempt(attempt) {
  const history = getAttemptHistory();
  history.push(attempt);
  localStorage.setItem('attempt_history', JSON.stringify(history));
}

function clearExamData(testId) {
  localStorage.removeItem(`exam_state_${testId}`);
  localStorage.removeItem(`user_answers_${testId}`);
  localStorage.removeItem(`flagged_${testId}`);
  localStorage.removeItem(`timer_${testId}`);
}

function loadListeningAnswers(testId) {
  try { return JSON.parse(localStorage.getItem(`listening_answers_${testId}`)) || {}; } catch { return {}; }
}
function saveListeningAnswers(testId, answers) {
  localStorage.setItem(`listening_answers_${testId}`, JSON.stringify(answers));
}
function loadListeningState(testId) {
  try { return JSON.parse(localStorage.getItem(`listening_state_${testId}`)); } catch { return null; }
}
function saveListeningState(testId, state) {
  localStorage.setItem(`listening_state_${testId}`, JSON.stringify(state));
}
function loadListeningFlagged(testId) {
  try { return JSON.parse(localStorage.getItem(`listening_flagged_${testId}`)) || []; } catch { return []; }
}
function saveListeningFlagged(testId, flagged) {
  localStorage.setItem(`listening_flagged_${testId}`, JSON.stringify(flagged));
}
function getListeningAttemptHistory() {
  try { return JSON.parse(localStorage.getItem('listening_attempt_history')) || []; } catch { return []; }
}
function saveListeningAttempt(attempt) {
  const h = getListeningAttemptHistory();
  h.push(attempt);
  localStorage.setItem('listening_attempt_history', JSON.stringify(h));
}
function clearListeningData(testId) {
  ['listening_answers_','listening_state_','listening_flagged_','listening_timer_'].forEach(p => localStorage.removeItem(p+testId));
}

function bandScore(rawScore) {
  if (rawScore >= 39) return 9.0;
  if (rawScore >= 37) return 8.5;
  if (rawScore >= 35) return 8.0;
  if (rawScore >= 33) return 7.5;
  if (rawScore >= 30) return 7.0;
  if (rawScore >= 27) return 6.5;
  if (rawScore >= 23) return 6.0;
  if (rawScore >= 20) return 5.5;
  if (rawScore >= 16) return 5.0;
  if (rawScore >= 13) return 4.5;
  if (rawScore >= 10) return 4.0;
  if (rawScore >= 7) return 3.5;
  if (rawScore >= 5) return 3.0;
  if (rawScore >= 3) return 2.5;
  return 2.0;
}

function formatTime(seconds) {
  const m = Math.floor(seconds / 60);
  const s = seconds % 60;
  return `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
}

function formatDuration(seconds) {
  const m = Math.floor(seconds / 60);
  const s = seconds % 60;
  return `${m}${t('min')} ${s}${t('seconds')}`;
}

function loadWritingAnswers(testId) {
  try { return JSON.parse(localStorage.getItem(`writing_answers_${testId}`)); } catch { return null; }
}
function saveWritingAnswers(testId, answers) {
  localStorage.setItem(`writing_answers_${testId}`, JSON.stringify(answers));
}
function loadWritingState(testId) {
  try { return JSON.parse(localStorage.getItem(`writing_state_${testId}`)); } catch { return null; }
}
function saveWritingState(testId, state) {
  localStorage.setItem(`writing_state_${testId}`, JSON.stringify(state));
}
function clearWritingData(testId) {
  localStorage.removeItem(`writing_answers_${testId}`);
  localStorage.removeItem(`writing_state_${testId}`);
}

// Wrong-book data helpers
function getMasteredQuestions() {
  try { return JSON.parse(localStorage.getItem('mastered_wrong_questions')) || []; } catch { return []; }
}
function saveMasteredQuestion(qid) {
  const list = getMasteredQuestions();
  if (!list.includes(qid)) {
    list.push(qid);
    localStorage.setItem('mastered_wrong_questions', JSON.stringify(list));
  }
}
function removeMasteredQuestion(qid) {
  const list = getMasteredQuestions().filter(id => id !== qid);
  localStorage.setItem('mastered_wrong_questions', JSON.stringify(list));
}
function isMastered(qid) {
  return getMasteredQuestions().includes(qid);
}

function escapeHtml(text) {
  if (!text) return '';
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

// Clear ALL history data across all modules
function clearAllHistoryData() {
  // Known localStorage key prefixes for all test data
  const keyPatterns = [
    'exam_state_', 'user_answers_', 'flagged_', 'timer_',
    'listening_answers_', 'listening_state_', 'listening_flagged_', 'listening_timer_',
    'writing_answers_', 'writing_state_'
  ];
  const keysToRemove = [];
  for (let i = 0; i < localStorage.length; i++) {
    const key = localStorage.key(i);
    if (key && keyPatterns.some(p => key.startsWith(p))) {
      keysToRemove.push(key);
    }
  }
  keysToRemove.forEach(k => localStorage.removeItem(k));
  // Remove history arrays
  localStorage.removeItem('attempt_history');
  localStorage.removeItem('listening_attempt_history');
  localStorage.removeItem('mastered_wrong_questions');
}
