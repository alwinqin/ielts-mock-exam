function renderWritingReview(testData, container) {
  const answers = loadWritingAnswers(testData.id) || { task1: '', task2: '' };
  const task1Wc = countWords(answers.task1 || '');
  const task2Wc = countWords(answers.task2 || '');

  container.innerHTML = `
    <div class="review-container">
      <div class="score-overview">
        <h2 style="margin-bottom:12px;">${t('writing')} ${testData.id.toUpperCase()}</h2>
        <div class="score-details">
          <div class="score-detail-item">${t('task1')}: <strong>${task1Wc} ${t('words')}</strong></div>
          <div class="score-detail-item">${t('task2')}: <strong>${task2Wc} ${t('words')}</strong></div>
        </div>
      </div>

      <div class="writing-review-tabs">
        <button class="writing-tab active" onclick="showWritingTaskReview('task1', this)">${t('task1')}</button>
        <button class="writing-tab" onclick="showWritingTaskReview('task2', this)">${t('task2')}</button>
      </div>

      <div id="writingReviewContent"></div>

      <div style="text-align:center;margin-top:20px;">
        <a href="#/" class="btn btn-secondary">${t('backToTests')}</a>
      </div>
    </div>
  `;

  showWritingTaskReview('task1', document.querySelector('.writing-review-tabs .active'));
}

function showWritingTaskReview(task, btn) {
  document.querySelectorAll('.writing-review-tabs .writing-tab').forEach(t => t.classList.remove('active'));
  if (btn) btn.classList.add('active');

  const data = window._writingReviewData || window._writingReviewTestData;
  // Get test data from global
  const testId = document.querySelector('.score-overview h2')?.textContent?.match(/TEST\d+/i)?.[0]?.toLowerCase() || '';
  const testData = window._writingReviewTestData;
  if (!testData || !testData[task]) return;

  const answers = loadWritingAnswers(testData.id) || {};
  const userText = answers[task] || '';
  const modelText = testData[task].modelAnswer || '';
  const title = testData[task].title || '';

  const container = document.getElementById('writingReviewContent');
  container.innerHTML = `
    <div style="margin-bottom:16px;">
      <h3 style="color:var(--text-heading);margin-bottom:8px;">${task === 'task1' ? 'Task 1: ' : 'Task 2: '}${title}</h3>
      <p style="font-size:0.85rem;color:var(--text-secondary);margin-bottom:12px;">${testData[task].prompt || ''}</p>
    </div>

    <div style="display:flex;gap:16px;flex-wrap:wrap;">
      <div style="flex:1;min-width:300px;">
        <h4 style="color:var(--text-primary);margin-bottom:8px;">${t('yourWriting')}</h4>
        <div style="background:var(--bg-subtle);border:1px solid var(--border-color);border-radius:6px;padding:16px;font-size:0.9rem;line-height:1.7;white-space:pre-wrap;min-height:200px;max-height:500px;overflow-y:auto;">
          ${escapeHtml(userText) || '<em style="color:var(--text-muted);">(no content)</em>'}
        </div>
        <p style="font-size:0.8rem;color:var(--text-muted);margin-top:4px;">${t('wordCount')}: ${countWords(userText)} ${t('words')}</p>
      </div>
      <div style="flex:1;min-width:300px;">
        <h4 style="color:var(--color-success);margin-bottom:8px;">${t('modelAnswer')}</h4>
        <div style="background:var(--color-success-bg);border:1px solid var(--color-success-border);border-radius:6px;padding:16px;font-size:0.9rem;line-height:1.7;white-space:pre-wrap;max-height:500px;overflow-y:auto;">
          ${modelText || '<em style="color:var(--text-muted);">Model answer not available.</em>'}
        </div>
      </div>
    </div>

    <div style="margin-top:24px;padding:16px;background:var(--bg-surface);border-radius:8px;border:1px solid var(--border-color);">
      <h4 style="color:var(--text-heading);margin-bottom:12px;">${t('selfAssess')}</h4>
      <p style="font-size:0.85rem;color:var(--text-muted);margin-bottom:12px;">Compare your writing with the model answer and assess yourself:</p>
      <table style="width:100%;border-collapse:collapse;font-size:0.85rem;">
        <tr>
          <th style="text-align:left;padding:8px;border-bottom:1px solid var(--border-color);color:var(--text-secondary);">Criterion</th>
          <th style="text-align:center;padding:8px;border-bottom:1px solid var(--border-color);color:var(--text-secondary);">1</th>
          <th style="text-align:center;padding:8px;border-bottom:1px solid var(--border-color);color:var(--text-secondary);">2</th>
          <th style="text-align:center;padding:8px;border-bottom:1px solid var(--border-color);color:var(--text-secondary);">3</th>
          <th style="text-align:center;padding:8px;border-bottom:1px solid var(--border-color);color:var(--text-secondary);">4</th>
          <th style="text-align:center;padding:8px;border-bottom:1px solid var(--border-color);color:var(--text-secondary);">5</th>
        </tr>
        <tr><td style="padding:6px;border-bottom:1px solid #f0f0f0;">${t('taskAchievement')}</td><td colspan="5" style="padding:6px;border-bottom:1px solid #f0f0f0;"><input type="range" min="1" max="5" value="3" style="width:100%;" oninput="this.nextElementSibling.textContent=this.value"></td><td style="padding:6px;border-bottom:1px solid #f0f0f0;font-size:0.8rem;color:var(--text-muted);">3</td></tr>
        <tr><td style="padding:6px;border-bottom:1px solid #f0f0f0;">${t('coherence')}</td><td colspan="5" style="padding:6px;border-bottom:1px solid #f0f0f0;"><input type="range" min="1" max="5" value="3" style="width:100%;" oninput="this.nextElementSibling.textContent=this.value"></td><td style="padding:6px;border-bottom:1px solid #f0f0f0;font-size:0.8rem;color:var(--text-muted);">3</td></tr>
        <tr><td style="padding:6px;border-bottom:1px solid #f0f0f0;">${t('lexicalResource')}</td><td colspan="5" style="padding:6px;border-bottom:1px solid #f0f0f0;"><input type="range" min="1" max="5" value="3" style="width:100%;" oninput="this.nextElementSibling.textContent=this.value"></td><td style="padding:6px;border-bottom:1px solid #f0f0f0;font-size:0.8rem;color:var(--text-muted);">3</td></tr>
        <tr><td style="padding:6px;">${t('grammar')}</td><td colspan="5" style="padding:6px;"><input type="range" min="1" max="5" value="3" style="width:100%;" oninput="this.nextElementSibling.textContent=this.value"></td><td style="padding:6px;font-size:0.8rem;color:var(--text-muted);">3</td></tr>
      </table>
    </div>
  `;
}

// Keep test data globally for review
window._writingReviewTestData = null;

// Override the renderWritingReview call to store testData
const _origRenderWritingReview = window.renderWritingReview;
window.renderWritingReview = function(testData, container) {
  window._writingReviewTestData = testData;
  renderWritingReview(testData, container);
};
