function renderHistoryPage(container) {
  const history = getAttemptHistory();
  const stats = calculateStats(history);
  const wrongAnswers = collectWrongAnswers(history);
  const weakTypes = analyzeWeakTypes(history);
  const allTestIds = [...new Set(history.map(h => h.testId))];

  let html = `
    <div class="history-container">
      <h1 data-i18n="statistics">${t('statistics')}</h1>
  `;

  if (history.length === 0) {
    html += `<div class="empty-state" data-i18n="historyEmpty">${t('historyEmpty')}</div>`;
    html += `<div style="text-align:center;margin-top:16px;"><a href="#/" class="btn btn-primary" data-i18n="backToTests">${t('backToTests')}</a></div>`;
    html += '</div>';
    container.innerHTML = html;
    return;
  }

  // Stats cards
  html += `
    <div class="stats-cards">
      <div class="stat-card"><div class="stat-value">${stats.totalAttempts}</div><div class="stat-label" data-i18n="totalAttempts">${t('totalAttempts')}</div></div>
      <div class="stat-card"><div class="stat-value">${(stats.avgScore).toFixed(1)}</div><div class="stat-label" data-i18n="avgScore">${t('avgScore')}</div></div>
      <div class="stat-card"><div class="stat-value">${stats.avgBand.toFixed(1)}</div><div class="stat-label" data-i18n="avgBand">${t('avgBand')}</div></div>
    </div>
  `;

  // Weak types
  if (weakTypes.length > 0) {
    html += `<div class="wrong-book-section"><h2 data-i18n="weakTypes">${t('weakTypes')}</h2><div class="stats-cards">`;
    weakTypes.slice(0, 3).forEach(wt => {
      html += `<div class="stat-card"><div class="stat-value" style="font-size:1rem;">${escapeHtml(wt.type)}</div><div class="stat-label">${wt.wrongCount} ${t('wrongAnswers')} / ${wt.totalCount} ${t('total')} (${Math.round(wt.wrongPercent)}%)</div></div>`;
    });
    html += `</div></div>`;
  }

  // Attempt history table
  html += `<h2 style="font-size:1.2rem;margin:20px 0 12px;color:var(--text-heading);" data-i18n="history">${t('history')}</h2>`;
  html += `<div class="history-table-wrap"><table class="history-table">
    <thead><tr><th data-i18n="test">${t('test')}</th><th data-i18n="date">${t('date')}</th><th data-i18n="score">${t('score')}</th><th data-i18n="bandScore">${t('bandScore')}</th><th data-i18n="timeUsed">${t('timeUsed')}</th><th data-i18n="action">${t('action')}</th></tr></thead>
    <tbody>
  `;

  history.slice().reverse().forEach((attempt, idx) => {
    const d = new Date(attempt.date);
    const dateStr = d.toLocaleDateString(i18n.currentLang === 'zh' ? 'zh-CN' : 'en-US');
    html += `<tr>
      <td>${attempt.testId.toUpperCase()}</td>
      <td>${dateStr}</td>
      <td>${attempt.score}/${attempt.total}</td>
      <td>${attempt.bandScore}</td>
      <td>${formatDuration(attempt.timeTaken)}</td>
      <td><a href="#/review/${attempt.testId}" class="btn btn-small btn-primary" data-i18n="review">${t('review')}</a></td>
    </tr>`;
  });

  html += `</tbody></table></div>`;

  // Wrong answer book
  html += `<div class="wrong-book-section"><h2 data-i18n="wrongBook">${t('wrongBook')}</h2>`;
  if (wrongAnswers.length === 0) {
    html += `<div class="empty-state" data-i18n="wrongBookEmpty">${t('wrongBookEmpty')}</div>`;
  } else {
    html += `<div id="wrongAnswerList">`;
    wrongAnswers.forEach(wa => {
      html += `<div class="wrong-group">
        <h3>${wa.testId.toUpperCase()} - ${t('question')} ${wa.questionNumber} (${wa.type})</h3>
        <div class="review-question wrong">
          <div style="font-size:0.85rem;margin-bottom:4px;">${escapeHtml(wa.question)}</div>
          <div class="review-answer">
            <span data-i18n="yourAnswer">${t('yourAnswer')}</span>: <span class="user-answer">${escapeHtml(wa.yourAnswer) || '(empty)'}</span>
            &nbsp;|&nbsp; <span data-i18n="correctAnswer">${t('correctAnswer')}</span>: <span class="correct-answer">${escapeHtml(wa.correctAnswer)}</span>
          </div>
        </div>
      </div>`;
    });
    html += `</div>`;
  }
  html += `</div>`;

  html += `<div style="text-align:center;margin-top:20px;">
    <a href="#/" class="btn btn-primary" data-i18n="backToTests">${t('backToTests')}</a>
    <button class="btn btn-danger" style="margin-top:12px;" onclick="onClearAllHistory()" data-i18n="clearAllHistory">${t('clearAllHistory')}</button>
  </div>`;
  html += `</div>`;

  container.innerHTML = html;
}

function onClearAllHistory() {
  showModal({
    type: 'confirm',
    title: t('clearAllHistory'),
    message: t('clearAllHistoryConfirm'),
    onConfirm: function () {
      clearAllHistoryData();
      const main = document.getElementById('mainContent');
      main.innerHTML = `
        <div class="history-container" style="text-align:center;padding:60px 24px;">
          <p style="font-size:1.1rem;color:var(--color-success);margin-bottom:16px;" data-i18n="clearAllHistoryDone">${t('clearAllHistoryDone')}</p>
          <a href="#/" class="btn btn-primary" data-i18n="backToTests">${t('backToTests')}</a>
        </div>
      `;
    }
  });
}

function calculateStats(history) {
  if (history.length === 0) return { totalAttempts: 0, avgScore: 0, avgBand: 0 };
  const totalAttempts = history.length;
  const totalScore = history.reduce((sum, h) => sum + h.score, 0);
  const avgScore = totalScore / totalAttempts;
  const avgBand = history.reduce((sum, h) => sum + h.bandScore, 0) / totalAttempts;
  return { totalAttempts, avgScore, avgBand };
}

function collectWrongAnswers(history) {
  const wrongs = [];
  history.forEach(attempt => {
    // We need test data to get question text. Since we can't load ALL test data here,
    // we store minimal info during the attempt save.
    // For now, we show what we can from the attempt data
    // A full implementation would load the test JSON and match
    if (attempt.wrongAnswers) {
      attempt.wrongAnswers.forEach(w => wrongs.push(w));
    }
  });
  return wrongs;
}

function analyzeWeakTypes(history) {
  const typeWrong = {};
  const typeTotal = {};

  history.forEach(attempt => {
    // Use typeCounts from saved attempt if available (new records)
    if (attempt.typeCounts) {
      Object.entries(attempt.typeCounts).forEach(([type, total]) => {
        if (!typeTotal[type]) typeTotal[type] = 0;
        typeTotal[type] += total;
        if (!typeWrong[type]) typeWrong[type] = 0;
      });
    }
    if (attempt.wrongAnswers) {
      attempt.wrongAnswers.forEach(w => {
        const t = w.type || 'unknown';
        typeWrong[t] = (typeWrong[t] || 0) + 1;
        if (!typeTotal[t]) typeTotal[t] = 0; // legacy data fallback
      });
    }
  });

  return Object.entries(typeTotal)
    .sort((a, b) => (typeWrong[b[0]] || 0) - (typeWrong[a[0]] || 0))
    .map(([type, totalCount]) => {
      const wrongCount = typeWrong[type] || 0;
      return {
        type,
        wrongCount,
        totalCount,
        wrongPercent: totalCount > 0 ? (wrongCount / totalCount) * 100 : 0
      };
    });
}
