let reviewTestData = null;
let reviewAttempt = null;
let reviewFilter = 'all';

function renderReview(testData, attempt, container) {
  reviewTestData = testData;
  reviewAttempt = attempt;
  reviewFilter = 'all';

  const allQuestions = [];
  testData.passages.forEach(p => {
    p.questions.forEach(q => {
      allQuestions.push({ ...q, passageTitle: p.title });
    });
  });

  container.innerHTML = `
    <div class="review-container">
      <div class="score-overview">
        <div>
          <span data-i18n="score">${t('score')}</span>:
          <span class="score-number">${attempt.score}</span>/40
        </div>
        <div style="margin-top:8px;">
          <span data-i18n="bandScore">${t('bandScore')}</span>:
          <span class="band-number">${attempt.bandScore}</span>
        </div>
        <div class="score-details">
          <div class="score-detail-item">${t('correctAnswers')}: <strong>${attempt.score}</strong></div>
          <div class="score-detail-item">${t('wrongAnswers')}: <strong>${attempt.total - attempt.score}</strong></div>
          <div class="score-detail-item">${t('unanswered')}: <strong>${countUnanswered(allQuestions, attempt.answers)}</strong></div>
          <div class="score-detail-item">${t('timeUsed')}: <strong>${formatDuration(attempt.timeTaken)}</strong></div>
        </div>
      </div>

      <div class="review-filters">
        <button class="btn btn-small ${reviewFilter === 'all' ? 'btn-primary active' : 'btn-secondary'}" onclick="setReviewFilter('all')" data-i18n="all">${t('all')}</button>
        <button class="btn btn-small ${reviewFilter === 'wrong' ? 'btn-primary active' : 'btn-secondary'}" onclick="setReviewFilter('wrong')" data-i18n="wrongOnly">${t('wrongOnly')}</button>
        <button class="btn btn-small ${reviewFilter === 'unanswered' ? 'btn-primary active' : 'btn-secondary'}" onclick="setReviewFilter('unanswered')" data-i18n="unanswered">${t('unanswered')}</button>
      </div>

      <div id="reviewQuestions"></div>

      <div style="text-align:center;margin-top:20px;">
        <a href="#/" class="btn btn-secondary" data-i18n="backToTests">${t('backToTests')}</a>
        <a href="#/history" class="btn btn-secondary" data-i18n="history">${t('history')}</a>
      </div>
    </div>
  `;

  renderReviewQuestions(allQuestions);
}

function countUnanswered(questions, answers) {
  return questions.filter(q => !answers[q.id] || !answers[q.id].trim()).length;
}

function setReviewFilter(filter) {
  reviewFilter = filter;

  // Update button styles
  document.querySelectorAll('.review-filters .btn').forEach(btn => {
    btn.classList.toggle('btn-primary', btn.textContent.includes(t('all')) && filter === 'all');
    btn.classList.toggle('btn-primary', btn.textContent.includes(t('wrongOnly')) && filter === 'wrong');
    btn.classList.toggle('btn-primary', btn.textContent.includes(t('unanswered')) && filter === 'unanswered');
    btn.classList.toggle('btn-secondary', !btn.classList.contains('btn-primary'));
    btn.classList.toggle('active', false); // will fix
  });

  const allQuestions = [];
  reviewTestData.passages.forEach(p => {
    p.questions.forEach(q => {
      allQuestions.push({ ...q, passageTitle: p.title });
    });
  });
  renderReviewQuestions(allQuestions);
}

function renderReviewQuestions(allQuestions) {
  const container = document.getElementById('reviewQuestions');
  if (!container) return;

  let html = '';
  let count = 0;

  allQuestions.forEach((q, idx) => {
    const userAns = reviewAttempt.answers[q.id] || '';
    const isCorrect = userAns.trim().toLowerCase() === (q.correctAnswer || '').trim().toLowerCase();
    const isUnanswered = !userAns.trim();
    const statusClass = isUnanswered ? 'unanswered' : isCorrect ? 'correct' : 'wrong';

    if (reviewFilter === 'wrong' && (isCorrect || isUnanswered)) return;
    if (reviewFilter === 'unanswered' && !isUnanswered) return;

    count++;

    html += `
      <div class="review-question ${statusClass}">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
          <strong>${t('question')} ${idx + 1}</strong>
          <span style="font-size:0.75rem;color:var(--text-muted);">${formatTypeName(q.type)} | ${q.passageTitle || ''}</span>
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
