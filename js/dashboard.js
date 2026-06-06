// ===== Data Dashboard =====

const DASHBOARD_CHARTS = {};

function renderDashboard(container) {
  const readingHistory = getAttemptHistory();
  const listeningHistory = getListeningAttemptHistory();
  const allAttempts = [
    ...readingHistory.map(a => ({ ...a, skill: 'reading' })),
    ...listeningHistory.map(a => ({ ...a, skill: 'listening' }))
  ].sort((a, b) => new Date(a.date) - new Date(b.date));

  if (allAttempts.length === 0) {
    container.innerHTML = `
      <div class="dashboard-container">
        <h1 class="dashboard-title">${t('dashboard')}</h1>
        <div class="dashboard-empty">
          <p>${t('practiceMakesPerfect')}</p>
          <a href="#/" class="btn btn-primary">${t('backToTests')}</a>
        </div>
      </div>
    `;
    return;
  }

  const stats = computeDashboardStats(readingHistory, listeningHistory, allAttempts);

  container.innerHTML = `
    <div class="dashboard-container">
      <h1 class="dashboard-title">${t('dashboard')}</h1>

      <div class="dashboard-stats-row" id="dashboardStats"></div>

      <div class="dashboard-charts-row">
        <div class="dashboard-card dashboard-card--half">
          <h3 class="dashboard-card-title">${t('skillComparison')}</h3>
          <div class="chart-wrap"><canvas id="chartSkillRadar"></canvas></div>
        </div>
        <div class="dashboard-card dashboard-card--half">
          <h3 class="dashboard-card-title">${t('bandScoreTrend')}</h3>
          <div class="chart-wrap"><canvas id="chartTrendLine"></canvas></div>
        </div>
      </div>

      <div class="dashboard-card">
        <h3 class="dashboard-card-title">${t('questionTypePerformance')}</h3>
        <div class="chart-wrap chart-wrap--tall"><canvas id="chartTypeBar"></canvas></div>
      </div>

      <div class="dashboard-card">
        <h3 class="dashboard-card-title">${t('recentAttempts')}</h3>
        <div class="dashboard-table-wrap" id="dashboardTable"></div>
      </div>
    </div>
  `;

  renderStatCards(stats);
  renderRecentTable(allAttempts);
  renderSkillRadar(stats);
  renderTrendLine(allAttempts);
  renderTypeBar(readingHistory, listeningHistory);
}

function computeDashboardStats(readingHistory, listeningHistory, allAttempts) {
  const totalAttempts = allAttempts.length;
  const totalCorrect = allAttempts.reduce((s, a) => s + a.score, 0);
  const totalQuestions = allAttempts.reduce((s, a) => s + a.total, 0);
  const avgAccuracy = totalQuestions > 0 ? Math.round((totalCorrect / totalQuestions) * 100) : 0;
  const avgBand = allAttempts.length > 0
    ? (allAttempts.reduce((s, a) => s + a.bandScore, 0) / allAttempts.length)
    : 0;
  const bestBand = allAttempts.length > 0
    ? Math.max(...allAttempts.map(a => a.bandScore))
    : 0;
  const totalTimeSec = allAttempts.reduce((s, a) => s + (a.timeTaken || 0), 0);
  const totalTimeMin = Math.round(totalTimeSec / 60);

  const readingBands = readingHistory.map(a => a.bandScore);
  const listeningBands = listeningHistory.map(a => a.bandScore);
  const readingAvg = readingBands.length > 0 ? readingBands.reduce((s, v) => s + v, 0) / readingBands.length : 0;
  const listeningAvg = listeningBands.length > 0 ? listeningBands.reduce((s, v) => s + v, 0) / listeningBands.length : 0;

  const readingAttempts = readingHistory.length;
  const listeningAttempts = listeningHistory.length;

  return {
    totalAttempts, avgAccuracy, avgBand, bestBand, totalTimeMin, totalTimeSec,
    readingAvg, listeningAvg, readingAttempts, listeningAttempts,
    readingHistory, listeningHistory
  };
}

function renderStatCards(stats) {
  const el = document.getElementById('dashboardStats');
  if (!el) return;

  const cards = [
    { label: t('totalAttempts'), value: stats.totalAttempts, sub: `${t('reading')}: ${stats.readingAttempts} | ${t('listening')}: ${stats.listeningAttempts}` },
    { label: t('avgBand'), value: stats.avgBand.toFixed(1), sub: `${t('avgScore')}: ${stats.avgAccuracy}%` },
    { label: t('bestScore'), value: stats.bestBand.toFixed(1), sub: t('bandScore') },
    { label: t('timeUsed'), value: formatTotalTime(stats.totalTimeSec), sub: t('total') }
  ];

  el.innerHTML = cards.map(c => `
    <div class="stat-card">
      <div class="stat-card-value">${c.value}</div>
      <div class="stat-card-label">${c.label}</div>
      <div class="stat-card-sub">${c.sub}</div>
    </div>
  `).join('');
}

function renderRecentTable(allAttempts) {
  const el = document.getElementById('dashboardTable');
  if (!el) return;

  const recent = [...allAttempts].reverse().slice(0, 10);
  const rows = recent.map((a, i) => {
    const d = new Date(a.date);
    const dateStr = d.toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: 'numeric' });
    const timeStr = formatTime(a.timeTaken || 0);
    const skillLabel = a.skill === 'reading' ? t('reading') : t('listening');
    const reviewHash = a.skill === 'reading' ? `#/review/${a.testId}` : `#/listening-review/${a.testId}`;
    return `
      <tr>
        <td>${recent.length - i}</td>
        <td>${dateStr}</td>
        <td><span class="skill-badge skill-badge--${a.skill}">${skillLabel}</span></td>
        <td>${a.testId}</td>
        <td><strong>${a.score}/${a.total}</strong></td>
        <td><span class="band-badge">${a.bandScore.toFixed(1)}</span></td>
        <td>${timeStr}</td>
        <td><a href="${reviewHash}" class="btn btn-small btn-secondary">${t('review')}</a></td>
      </tr>
    `;
  }).join('');

  el.innerHTML = `
    <table class="dashboard-table">
      <thead><tr>
        <th>#</th><th>${t('date')}</th><th>${t('skill')}</th><th>${t('test')}</th><th>${t('score')}</th><th>${t('bandScore')}</th><th>${t('timeUsed')}</th><th>${t('action')}</th>
      </tr></thead>
      <tbody>${rows || `<tr><td colspan="8" style="text-align:center;color:var(--text-muted);padding:24px;">${t('noHistory')}</td></tr>`}</tbody>
    </table>
  `;
}

function renderSkillRadar(stats) {
  destroyChart('chartSkillRadar');
  const canvas = document.getElementById('chartSkillRadar');
  if (!canvas) return;

  const ctx = canvas.getContext('2d');
  DASHBOARD_CHARTS.chartSkillRadar = new Chart(ctx, {
    type: 'radar',
    data: {
      labels: [t('reading'), t('listening'), t('writing'), t('speaking')],
      datasets: [{
        label: t('avgBand'),
        data: [stats.readingAvg, stats.listeningAvg, 0, 0],
        backgroundColor: 'rgba(74, 139, 194, 0.2)',
        borderColor: 'rgba(74, 139, 194, 1)',
        borderWidth: 2,
        pointBackgroundColor: 'rgba(74, 139, 194, 1)',
        pointRadius: 4
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      scales: {
        r: {
          beginAtZero: true,
          max: 9,
          ticks: { stepSize: 1, backdropColor: 'transparent' },
          pointLabels: { font: { size: 12 } }
        }
      },
      plugins: {
        legend: { display: false }
      }
    }
  });
}

function renderTrendLine(allAttempts) {
  destroyChart('chartTrendLine');
  const canvas = document.getElementById('chartTrendLine');
  if (!canvas) return;

  // Build data points sorted by date
  const sorted = [...allAttempts].sort((a, b) => new Date(a.date) - new Date(b.date));
  const labels = sorted.map((a, i) => {
    const d = new Date(a.date);
    return `${d.getMonth() + 1}/${d.getDate()}`;
  });
  const readingData = sorted.map(a => a.skill === 'reading' ? a.bandScore : null);
  const listeningData = sorted.map(a => a.skill === 'listening' ? a.bandScore : null);

  const ctx = canvas.getContext('2d');
  DASHBOARD_CHARTS.chartTrendLine = new Chart(ctx, {
    type: 'line',
    data: {
      labels,
      datasets: [
        {
          label: t('reading'),
          data: readingData,
          borderColor: 'rgba(74, 139, 194, 1)',
          backgroundColor: 'rgba(74, 139, 194, 0.1)',
          tension: 0.3,
          spanGaps: false,
          pointRadius: 4
        },
        {
          label: t('listening'),
          data: listeningData,
          borderColor: 'rgba(255, 152, 0, 1)',
          backgroundColor: 'rgba(255, 152, 0, 0.1)',
          tension: 0.3,
          spanGaps: false,
          pointRadius: 4
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      scales: {
        y: { min: 0, max: 9, ticks: { stepSize: 1 } }
      },
      plugins: {
        legend: {
          labels: {
            usePointStyle: true,
            boxWidth: 8
          }
        }
      }
    }
  });
}

function renderTypeBar(readingHistory, listeningHistory) {
  destroyChart('chartTypeBar');
  const canvas = document.getElementById('chartTypeBar');
  if (!canvas) return;

  // Aggregate question type stats across all attempts
  const typeStats = {}; // { type: { wrong: n, total: n } }
  const allHistory = [...readingHistory, ...listeningHistory];
  allHistory.forEach(attempt => {
    // Count total questions per type from typeCounts
    if (attempt.typeCounts) {
      Object.entries(attempt.typeCounts).forEach(([type, count]) => {
        if (!typeStats[type]) typeStats[type] = { wrong: 0, total: 0 };
        typeStats[type].total += count;
      });
    }
    // Count wrong answers per type
    (attempt.wrongAnswers || []).forEach(wa => {
      if (!typeStats[wa.type]) typeStats[wa.type] = { wrong: 0, total: 0 };
      typeStats[wa.type].wrong++;
    });
  });

  // Calculate correct counts
  Object.keys(typeStats).forEach(type => {
    typeStats[type].correct = typeStats[type].total - typeStats[type].wrong;
  });

  const entries = Object.entries(typeStats)
    .map(([type, data]) => ({ type, ...data, accuracy: data.total > 0 ? Math.round((data.correct / data.total) * 100) : 0 }))
    .sort((a, b) => a.accuracy - b.accuracy); // weakest first

  if (entries.length === 0) {
    canvas.parentElement.innerHTML = `<p style="text-align:center;color:var(--text-muted);padding:24px;">${t('noHistory')}</p>`;
    return;
  }

  const typeLabels = entries.map(e => formatTypeName(e.type));
  const correctData = entries.map(e => e.correct);
  const wrongData = entries.map(e => e.wrong);

  const ctx = canvas.getContext('2d');
  DASHBOARD_CHARTS.chartTypeBar = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: typeLabels,
      datasets: [
        {
          label: t('correctAnswers'),
          data: correctData,
          backgroundColor: 'rgba(76, 175, 80, 0.7)',
          borderColor: 'rgba(76, 175, 80, 1)',
          borderWidth: 1
        },
        {
          label: t('wrongAnswers'),
          data: wrongData,
          backgroundColor: 'rgba(244, 67, 54, 0.7)',
          borderColor: 'rgba(244, 67, 54, 1)',
          borderWidth: 1
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      indexAxis: 'y',
      scales: {
        x: { stacked: true, title: { display: true, text: t('questions'), font: { size: 12 } } },
        y: { stacked: true }
      },
      plugins: {
        legend: {
          labels: { usePointStyle: true, boxWidth: 8 }
        },
        tooltip: {
          callbacks: {
            afterLabel: function(ctx) {
              const entry = entries[ctx.dataIndex];
              return `Accuracy: ${entry.accuracy}%`;
            }
          }
        }
      }
    }
  });
}

function formatTypeName(type) {
  const map = {
    'multiple_choice': 'Multiple Choice',
    'multiple_choice_multi': 'Multi-Select',
    'tfng': 'True/False/NG',
    'ynng': 'Yes/No/NG',
    'matching_headings': 'Match Headings',
    'matching_info': 'Match Info',
    'matching_sentence': 'Match Sentence',
    'matching_names': 'Match Names',
    'matching': 'Matching',
    'sentence_completion': 'Sentence Comp.',
    'summary_completion': 'Summary Comp.',
    'notes_completion': 'Notes Comp.',
    'form_completion': 'Form Comp.',
    'short_answer': 'Short Answer'
  };
  return map[type] || type;
}

function destroyChart(key) {
  if (DASHBOARD_CHARTS[key]) {
    DASHBOARD_CHARTS[key].destroy();
    delete DASHBOARD_CHARTS[key];
  }
}

function formatTotalTime(seconds) {
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  if (h > 0) return `${h}h ${m}m`;
  return `${m} min`;
}
