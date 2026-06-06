function renderListeningReview(testData, attempt, container) {
  const allQuestions = [];
  testData.sections.forEach((s, si) => {
    s.questions.forEach(q => {
      allQuestions.push({ ...q, sectionIndex: si, sectionTitle: s.title });
    });
  });

  const unanswered = allQuestions.filter(q => !attempt.answers[q.id] || !attempt.answers[q.id].trim()).length;
  const wrongCount = attempt.total - attempt.score - unanswered;

  // Section breakdown
  let sectionHtml = '';
  testData.sections.forEach((s, si) => {
    const secQs = s.questions;
    const secCorrect = secQs.filter(q => {
      const ua = (attempt.answers[q.id] || '').trim().toLowerCase();
      return ua === (q.correctAnswer || '').trim().toLowerCase();
    }).length;
    sectionHtml += `<span style="margin:0 8px;font-size:0.85rem;">${t('section').replace('S','')} ${si+1}: ${secCorrect}/${secQs.length}</span>`;
  });

  container.innerHTML = `
    <div class="review-container">
      <div class="score-overview">
        <div><span data-i18n="score">${t('score')}</span>: <span class="score-number">${attempt.score}</span>/${attempt.total}</div>
        <div style="margin-top:8px;"><span data-i18n="bandScore">${t('bandScore')}</span>: <span class="band-number">${attempt.bandScore}</span></div>
        <div class="score-details">
          <div class="score-detail-item">${t('correctAnswers')}: <strong>${attempt.score}</strong></div>
          <div class="score-detail-item">${t('wrongAnswers')}: <strong>${wrongCount}</strong></div>
          <div class="score-detail-item">${t('unanswered')}: <strong>${unanswered}</strong></div>
        </div>
        <div style="margin-top:12px;">${sectionHtml}</div>
      </div>

      <div class="review-filters">
        <button class="btn btn-small btn-primary active" onclick="setListeningFilter(this,'all')" data-i18n="all">${t('all')}</button>
        <button class="btn btn-small btn-secondary" onclick="setListeningFilter(this,'wrong')" data-i18n="wrongOnly">${t('wrongOnly')}</button>
        <button class="btn btn-small btn-secondary" onclick="setListeningFilter(this,'unanswered')" data-i18n="unanswered">${t('unanswered')}</button>
      </div>

      <div id="listeningReviewQuestions"></div>

      <div style="text-align:center;margin-top:20px;">
        <a href="#/" class="btn btn-secondary" data-i18n="backToTests">${t('backToTests')}</a>
        <a href="#/listening-history" class="btn btn-secondary" data-i18n="history">${t('history')}</a>
      </div>
    </div>
  `;

  window._listeningReviewData = { allQuestions, attempt };
  renderListeningReviewQuestions(allQuestions, attempt, 'all');
}

function setListeningFilter(btn, filter) {
  document.querySelectorAll('.review-filters .btn').forEach(b => {
    b.className = 'btn btn-small btn-secondary';
  });
  btn.className = 'btn btn-small btn-primary active';

  const { allQuestions, attempt } = window._listeningReviewData || {};
  if (allQuestions && attempt) {
    renderListeningReviewQuestions(allQuestions, attempt, filter);
  }
}

function renderListeningReviewQuestions(allQuestions, attempt, filter) {
  const container = document.getElementById('listeningReviewQuestions');
  if (!container) return;

  let html = '';
  let count = 0;

  allQuestions.forEach((q, idx) => {
    const userAns = attempt.answers[q.id] || '';
    const isCorrect = userAns.trim().toLowerCase() === (q.correctAnswer || '').trim().toLowerCase();
    const isUnanswered = !userAns.trim();
    const statusClass = isUnanswered ? 'unanswered' : isCorrect ? 'correct' : 'wrong';

    if (filter === 'wrong' && (isCorrect || isUnanswered)) return;
    if (filter === 'unanswered' && !isUnanswered) return;

    count++;

    html += `
      <div class="review-question ${statusClass}">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
          <strong>${t('question')} ${idx + 1}</strong>
          <span style="font-size:0.75rem;color:var(--text-muted);">${t('section').replace('S','')} ${q.sectionIndex + 1}</span>
        </div>
        <div class="question-text">${escapeHtml(q.question)}</div>
        <div class="review-answer">
          <span data-i18n="yourAnswer">${t('yourAnswer')}</span>: <span class="user-answer ${isCorrect ? 'correct' : ''}">${escapeHtml(userAns) || '<em style="color:var(--text-muted);">(empty)</em>'}</span>
          ${isCorrect ? '<span style="color:var(--color-success);margin-left:8px;">&#10003;</span>' : ''}
          ${!isCorrect ? `| <span data-i18n="correctAnswer">${t('correctAnswer')}</span>: <span class="correct-answer">${escapeHtml(q.correctAnswer)}</span>` : ''}
        </div>
        <div class="review-explanation">
          <strong data-i18n="explanation">${t('explanation')}</strong>: ${escapeHtml(q.explanation) || t('noBilingualData')}
        </div>
      </div>
    `;
  });

  if (count === 0) {
    html = `<div class="empty-state" data-i18n="noWrongAnswers">${t('noWrongAnswers')}</div>`;
  }

  container.innerHTML = html;
}

function renderListeningHistoryPage(container) {
  const history = getListeningAttemptHistory();
  const stats = calculateListeningStats(history);

  let html = `
    <div class="history-container">
      <h1 data-i18n="statistics">${t('statistics')}</h1>
  `;

  if (history.length === 0) {
    html += `<div class="empty-state" data-i18n="historyEmpty">${t('historyEmpty')}</div>`;
    html += `<div style="text-align:center;margin-top:16px;"><a href="#/" class="btn btn-primary" data-i18n="backToTests">${t('backToTests')}</a></div></div>`;
    container.innerHTML = html;
    return;
  }

  html += `
    <div class="stats-cards">
      <div class="stat-card"><div class="stat-value">${stats.totalAttempts}</div><div class="stat-label" data-i18n="totalAttempts">${t('totalAttempts')}</div></div>
      <div class="stat-card"><div class="stat-value">${stats.avgScore.toFixed(1)}</div><div class="stat-label" data-i18n="avgScore">${t('avgScore')}</div></div>
      <div class="stat-card"><div class="stat-value">${stats.avgBand.toFixed(1)}</div><div class="stat-label" data-i18n="avgBand">${t('avgBand')}</div></div>
    </div>
  `;

  html += `<h2 style="font-size:1.2rem;margin:20px 0 12px;color:var(--text-heading);" data-i18n="history">${t('history')}</h2>`;
  html += `<div class="history-table-wrap"><table class="history-table">
    <thead><tr><th data-i18n="test">${t('test')}</th><th data-i18n="date">${t('date')}</th><th data-i18n="score">${t('score')}</th><th data-i18n="bandScore">${t('bandScore')}</th><th data-i18n="action">${t('action')}</th></tr></thead>
    <tbody>
  `;

  history.slice().reverse().forEach(attempt => {
    const d = new Date(attempt.date);
    const dateStr = d.toLocaleDateString(i18n.currentLang === 'zh' ? 'zh-CN' : 'en-US');
    html += `<tr>
      <td>${t('listening')} ${attempt.testId.toUpperCase().replace('TEST','')}</td>
      <td>${dateStr}</td>
      <td>${attempt.score}/${attempt.total}</td>
      <td>${attempt.bandScore}</td>
      <td><a href="#/listening-review/${attempt.testId}" class="btn btn-small btn-primary" data-i18n="review">${t('review')}</a></td>
    </tr>`;
  });

  html += `</tbody></table></div>`;
  html += `<div style="text-align:center;margin-top:20px;">
    <a href="#/" class="btn btn-primary" data-i18n="backToTests">${t('backToTests')}</a>
    <button class="btn btn-danger" style="margin-top:12px;display:block;margin-left:auto;margin-right:auto;" onclick="onClearAllHistory()" data-i18n="clearAllHistory">${t('clearAllHistory')}</button>
  </div>`;
  html += `</div>`;

  container.innerHTML = html;
}

function calculateListeningStats(history) {
  if (history.length === 0) return { totalAttempts: 0, avgScore: 0, avgBand: 0 };
  const totalAttempts = history.length;
  const totalScore = history.reduce((sum, h) => sum + h.score, 0);
  const avgScore = totalScore / totalAttempts;
  const avgBand = history.reduce((sum, h) => sum + h.bandScore, 0) / totalAttempts;
  return { totalAttempts, avgScore, avgBand };
}

// Expose for app.js
window.renderListeningReview = renderListeningReview;
window.renderListeningHistoryPage = renderListeningHistoryPage;
