const isFileProtocol = window.location.protocol === 'file:';

async function loadTestData(path) {
  // Cambridge path detection on path like "data/cambridge/cam17/reading.json"
  const camInfo = parseCambridgePath(path);
  if (camInfo) {
    let bookData;
    if (isFileProtocol && window.__DATA_BUNDLE__) {
      const books = window.__DATA_BUNDLE__.cambridge || {};
      bookData = books[camInfo.bookId]?.[camInfo.type];
    } else {
      const response = await fetch(path);
      if (!response.ok) throw new Error('HTTP ' + response.status);
      bookData = await response.json();
    }
    if (!bookData || !bookData.tests) throw new Error('Invalid Cambridge data');
    return { _cambridgeBook: true, bookData: bookData, type: camInfo.type, bookId: camInfo.bookId };
  }

  if (isFileProtocol && window.__DATA_BUNDLE__) {
    const parts = path.replace('.json', '').split('/');
    if (parts[0] === 'data' && parts.length === 2) {
      return window.__DATA_BUNDLE__.reading[parts[1]];
    }
    if (parts[0] === 'data' && parts.length === 3) {
      const category = parts[1];
      return window.__DATA_BUNDLE__[category]?.[parts[2]];
    }
    throw new Error('Unknown path: ' + path);
  }
  const response = await fetch(path);
  if (!response.ok) throw new Error('HTTP ' + response.status);
  return response.json();
}

const App = {
  currentTest: null,
  tests: [],
  cambridgeBooks: [],
  cambridgeListeningBooks: [],
  cambridgeWritingBooks: [],
  cambridgeSpeakingBooks: [],
  activeTab: localStorage.getItem('ielts_active_tab') || 'reading',

  async init() {
    await this.loadTestList();
    this.setupRouter();
    this.handleRoute();
    window.addEventListener('hashchange', () => this.handleRoute());
  },

  async loadTestList() {
    // Legacy tests
    const legacyTests = [];
    const maxTests = (isFileProtocol && window.__DATA_BUNDLE__)
      ? Object.keys(window.__DATA_BUNDLE__.reading || {}).length
      : 20;
    for (let i = 1; i <= maxTests; i++) {
      legacyTests.push({ id: `test${i}`, title: `Test ${i}`, file: `data/test${i}.json`, source: 'legacy' });
    }

    // Cambridge tests
    const cambridgeBooks = [];
    const cambridgeListeningBooks = [];
    // Try bundle first (works in both file:// and HTTP modes)
    const camData = window.__DATA_BUNDLE__?.cambridge || {};
    for (const bookId of Object.keys(camData)) {
      const reading = camData[bookId]?.reading;
      const listening = camData[bookId]?.listening;
      if (reading && reading.tests) {
        const tests = getCambridgeReadingTests(reading);
        cambridgeBooks.push({ bookId, bookTitle: reading.title, tests, source: 'cambridge' });
      }
      if (listening && listening.tests) {
        const tests = getCambridgeListeningTests(listening);
        cambridgeListeningBooks.push({ bookId, bookTitle: listening.title, tests, source: 'cambridge' });
      }
    }
    // Fallback: if bundle doesn't have Cambridge data, try HTTP fetch
    if (cambridgeBooks.length === 0 && !isFileProtocol) {
      const bookIds = ['cam14', 'cam15', 'cam16', 'cam17', 'cam18', 'cam19', 'cam20'];
      for (const bookId of bookIds) {
        try {
          const resp = await fetch(`data/cambridge/${bookId}/reading.json`);
          if (resp.ok) {
            const data = await resp.json();
            if (data.tests) {
              const tests = getCambridgeReadingTests(data);
              cambridgeBooks.push({ bookId, bookTitle: data.title, tests, source: 'cambridge' });
            }
          }
        } catch (e) { /* not available */ }
        try {
          const resp = await fetch(`data/cambridge/${bookId}/listening.json`);
          if (resp.ok) {
            const data = await resp.json();
            if (data.tests) {
              const tests = getCambridgeListeningTests(data);
              cambridgeListeningBooks.push({ bookId, bookTitle: data.title, tests, source: 'cambridge' });
            }
          }
        } catch (e) { /* not available */ }
      }
    }

    // Cambridge writing tests — scan bundle for cam*_test* keys
    const cambridgeWritingBooks = [];
    const writingData = window.__DATA_BUNDLE__?.writing || {};
    for (const key of Object.keys(writingData)) {
      const m = key.match(/^(cam\d+)_test(\d+)$/);
      if (m) {
        const bookId = m[1];
        const testNum = parseInt(m[2]);
        let book = cambridgeWritingBooks.find(b => b.bookId === bookId);
        if (!book) {
          book = { bookId, bookTitle: `Cambridge IELTS ${bookId.replace('cam', '')}`, tests: [], source: 'cambridge' };
          cambridgeWritingBooks.push(book);
        }
        book.tests.push({ id: key, title: `Test ${testNum}`, bookId, testNumber: testNum });
      }
    }
    cambridgeWritingBooks.forEach(b => b.tests.sort((a, b) => a.testNumber - b.testNumber));
    cambridgeWritingBooks.sort((a, b) => a.bookId.localeCompare(b.bookId));

    // Cambridge speaking tests — scan bundle for cam*_test* keys
    const cambridgeSpeakingBooks = [];
    const speakingData = window.__DATA_BUNDLE__?.speaking || {};
    for (const key of Object.keys(speakingData)) {
      const m = key.match(/^(cam\d+)_test(\d+)$/);
      if (m) {
        const bookId = m[1];
        const testNum = parseInt(m[2]);
        let book = cambridgeSpeakingBooks.find(b => b.bookId === bookId);
        if (!book) {
          book = { bookId, bookTitle: `Cambridge IELTS ${bookId.replace('cam', '')}`, tests: [], source: 'cambridge' };
          cambridgeSpeakingBooks.push(book);
        }
        book.tests.push({ id: key, title: `Test ${testNum}`, bookId, testNumber: testNum });
      }
    }
    cambridgeSpeakingBooks.forEach(b => b.tests.sort((a, b) => a.testNumber - b.testNumber));
    cambridgeSpeakingBooks.sort((a, b) => a.bookId.localeCompare(b.bookId));

    this.tests = legacyTests;
    this.cambridgeBooks = cambridgeBooks;
    this.cambridgeListeningBooks = cambridgeListeningBooks;
    this.cambridgeWritingBooks = cambridgeWritingBooks;
    this.cambridgeSpeakingBooks = cambridgeSpeakingBooks;
  },

  getTestStatus(testId) {
    const state = loadExamState(testId);
    const history = getAttemptHistory();
    const attempts = history.filter(h => h.testId === testId);
    const bestScore = attempts.length > 0 ? Math.max(...attempts.map(a => a.score)) : null;

    if (state && !state.completed) return { status: 'in_progress', bestScore };
    if (state && state.completed) return { status: 'completed', bestScore };
    return { status: 'new', bestScore };
  },

  getListeningStatus(testId) {
    const state = loadListeningState(testId);
    const history = getListeningAttemptHistory();
    const attempts = history.filter(h => h.testId === testId);
    const bestScore = attempts.length > 0 ? Math.max(...attempts.map(a => a.score)) : null;

    if (state && !state.completed) return { status: 'in_progress', bestScore };
    if (state && state.completed) return { status: 'completed', bestScore };
    return { status: 'new', bestScore };
  },

  switchTab(tab) {
    this.activeTab = tab;
    localStorage.setItem('ielts_active_tab', tab);
    const main = document.getElementById('mainContent');
    this.renderTestSelect(main);
  },

  setupRouter() {
    // routing handled in handleRoute
  },

  handleRoute() {
    const hash = window.location.hash.slice(1) || '/';
    const main = document.getElementById('mainContent');
    if (!main) return;

    if (hash === '/' || hash === '') {
      this.renderTestSelect(main);
    } else if (hash.startsWith('/exam/')) {
      const testId = hash.split('/exam/')[1];
      this.showExam(testId);
    } else if (hash.startsWith('/review/')) {
      const testId = hash.split('/review/')[1];
      this.showReview(testId);
    } else if (hash.startsWith('/listening-exam/')) {
      const testId = hash.split('/listening-exam/')[1];
      this.showListeningExam(testId);
    } else if (hash.startsWith('/listening-review/')) {
      const testId = hash.split('/listening-review/')[1];
      this.showListeningReview(testId);
    } else if (hash === '/wrong-book') {
      this.showWrongBook(main);
    } else if (hash.startsWith('/wrong-book/')) {
      this.showWrongBook(main);
    } else if (hash === '/history') {
      this.showHistory(main);
    } else if (hash === '/listening-history') {
      this.showListeningHistory(main);
    } else if (hash.startsWith('/writing-exam/')) {
      const testId = hash.split('/writing-exam/')[1];
      this.showWritingExam(testId);
    } else if (hash.startsWith('/writing-review/')) {
      const testId = hash.split('/writing-review/')[1];
      this.showWritingReview(testId);
    } else if (hash.startsWith('/speaking-exam/')) {
      const testId = hash.split('/speaking-exam/')[1];
      this.showSpeakingExam(testId);
    } else {
      this.renderTestSelect(main);
    }
  },

  renderTestSelect(container) {
    container.innerHTML = `
      <div class="test-select">
        <h1 data-i18n="selectTest">${t('selectTest')}</h1>
        <div class="tab-nav">
          <button class="tab-btn ${this.activeTab === 'reading' ? 'active' : ''}" onclick="App.switchTab('reading')" data-i18n="reading">${t('reading')}</button>
          <button class="tab-btn ${this.activeTab === 'listening' ? 'active' : ''}" onclick="App.switchTab('listening')" data-i18n="listening">${t('listening')}</button>
          <button class="tab-btn ${this.activeTab === 'writing' ? 'active' : ''}" onclick="App.switchTab('writing')" data-i18n="writing">${t('writing')}</button>
          <button class="tab-btn ${this.activeTab === 'speaking' ? 'active' : ''}" onclick="App.switchTab('speaking')" data-i18n="speaking">${t('speaking')}</button>
        </div>
        <div class="test-grid" id="testGrid"></div>
        <div class="sidebar-actions">
          <a href="#/history" class="btn btn-secondary" data-i18n="viewHistory">${t('viewHistory')}</a>
          <a href="#/wrong-book" class="btn btn-secondary" style="margin-left:8px;" data-i18n="wrongBook">${t('wrongBook')}</a>
        </div>
      </div>
    `;
    const grid = document.getElementById('testGrid');
    if (this.activeTab === 'listening') {
      this.renderListeningGrid(grid);
    } else if (this.activeTab === 'writing') {
      this.renderWritingGrid(grid);
    } else if (this.activeTab === 'speaking') {
      this.renderSpeakingGrid(grid);
    } else {
      this.renderReadingGrid(grid);
    }
  },

  _buildTestCards(tests, examType) {
    const pathMap = {
      reading:  { exam: '#/exam/',            review: '#/review/'            },
      listening:{ exam: '#/listening-exam/',   review: '#/listening-review/'   },
      writing:  { exam: '#/writing-exam/',    review: null                   },
      speaking: { exam: '#/speaking-exam/',   review: null                   }
    };
    const paths = pathMap[examType];
    const parts = [];
    tests.forEach(test => {
      let status, bestScore;
      if (examType === 'listening') {
        const s = this.getListeningStatus(test.id);
        status = s.status; bestScore = s.bestScore;
      } else if (examType === 'reading') {
        const s = this.getTestStatus(test.id);
        status = s.status; bestScore = s.bestScore;
      } else {
        status = 'new'; bestScore = null;
      }

      const statusLabel = t(status === 'in_progress' ? 'inProgress' : status === 'completed' ? 'completed' : 'newTest');
      const bestScoreHtml = bestScore !== null ? `<span class="best-score">${t('bestScore')}: ${bestScore}/40</span>` : '';
      const actionText = status === 'in_progress' ? t('resumeExam') : t('startExam');
      const actionLink = paths.exam + test.id;
      const reviewLink = paths.review && status === 'completed' ? paths.review + test.id : null;

      let bodyHtml = bestScoreHtml;
      if (examType === 'writing') {
        bodyHtml = `<span style="font-size:0.8rem;color:#888;">${t('task1')}: 150 ${t('words')} (20 min)<br>${t('task2')}: 250 ${t('words')} (40 min)</span>`;
      } else if (examType === 'speaking') {
        bodyHtml = `<span style="font-size:0.8rem;color:#888;">${t('part1')} (4-5 min)<br>${t('part2')} (3-4 min)<br>${t('part3')} (4-5 min)</span>`;
      }

      parts.push(`
        <div class="test-card ${status}">
          <div class="test-card-header">
            <h3>${test.title}</h3>
            <span class="status-badge ${status}">${statusLabel}</span>
          </div>
          <div class="test-card-body">${bodyHtml}</div>
          <div class="test-card-actions">
            <a href="${actionLink}" class="btn btn-primary">${actionText}</a>
            ${reviewLink ? `<a href="${reviewLink}" class="btn btn-secondary" style="margin-left:6px;">${t('review')}</a>` : ''}
            ${status !== 'new' ? `<a href="${actionLink}" class="btn btn-secondary" style="margin-left:6px;" onclick="event.preventDefault(); App.confirmRedo('${test.id}', '${examType}')">${t('redoExam')}</a>` : ''}
          </div>
        </div>
      `);
    });
    return parts.join('');
  },

  _renderBookGroup(book, examType) {
    const bookDiv = document.createElement('div');
    bookDiv.className = 'book-group';
    bookDiv.innerHTML = `
      <div class="book-group-header" onclick="this.parentElement.classList.toggle('collapsed')">
        <span class="book-group-title">${book.bookTitle}</span>
        <span class="book-group-toggle">&#9660;</span>
      </div>
      <div class="book-group-tests">${this._buildTestCards(book.tests, examType)}</div>
    `;
    return bookDiv;
  },

  renderReadingGrid(grid) {
    this._renderGrid(this.cambridgeBooks, this.tests, 'reading', grid);
  },

  _renderGrid(books, legacyTests, examType, grid) {
    (books || []).forEach(book => {
      grid.appendChild(this._renderBookGroup(book, examType));
    });
    if (legacyTests.length > 0 && books.length > 0) {
      grid.insertAdjacentHTML('beforeend', `<div class="section-header">${t('moreTests')}</div>`);
    }
    grid.insertAdjacentHTML('beforeend', this._buildTestCards(legacyTests, examType));
  },

  renderListeningGrid(grid) {
    const legacy = [];
    for (let i = 1; i <= 10; i++) {
      legacy.push({ id: `test${i}`, title: `${t('listening')} ${i}` });
    }
    this._renderGrid(this.cambridgeListeningBooks, legacy, 'listening', grid);
  },

  async showExam(testId) {
    const container = document.getElementById('mainContent');
    container.innerHTML = `<div class="loading">${t('loading')}</div>`;

    try {
      if (testId.startsWith('cam')) {
        this.currentTest = await this.loadCambridgeReadingTest(testId);
      } else {
        this.currentTest = await loadTestData(`data/${testId}.json`);
      }
      if (!this.currentTest || !this.currentTest.passages) throw new Error('Invalid data format');
      renderExam(this.currentTest);
    } catch (e) {
      console.error('Exam error:', e);
      container.innerHTML = `<div class="error">${t('errorLoadData')}<br><small style="color:#999">${escapeHtml(e.message)}</small></div>`;
    }
  },

  async loadCambridgeReadingTest(testId) {
    const parts = testId.split('_');
    const bookId = parts[0]; // e.g., "cam17"
    const path = `data/cambridge/${bookId}/reading.json`;
    const result = await loadTestData(path);
    if (result._cambridgeBook) {
      return getCambridgeReadingTest(result.bookData, testId);
    }
    // In bundle mode, the result might already be the test data
    if (result.passages) return result;
    throw new Error('Cambridge test not found');
  },

  async loadCambridgeListeningTest(testId) {
    const parts = testId.split('_');
    const bookId = parts[0];
    const path = `data/cambridge/${bookId}/listening.json`;
    const result = await loadTestData(path);
    if (result._cambridgeBook) {
      return getCambridgeListeningTest(result.bookData, testId);
    }
    if (result.sections) return result;
    throw new Error('Cambridge listening test not found');
  },

  async showListeningExam(testId) {
    const container = document.getElementById('mainContent');
    container.innerHTML = `<div class="loading">${t('loading')}</div>`;

    try {
      let testData;
      if (testId.startsWith('cam')) {
        testData = await this.loadCambridgeListeningTest(testId);
      } else {
        testData = await loadTestData(`data/listening/${testId}.json`);
      }
      if (!testData || !testData.sections) throw new Error('Invalid data format');
      renderListeningExam(testData);
    } catch (e) {
      console.error('Listening exam error:', e);
      container.innerHTML = `<div class="error">${t('errorLoadData')}<br><small style="color:#999">${escapeHtml(e.message)}</small></div>`;
    }
  },

  showReview(testId) {
    const container = document.getElementById('mainContent');
    this._showReview(testId, container);
  },

  _showReview(testId, container) {
    const state = loadExamState(testId);
    const answers = loadAnswers(testId);

    // Look for latest attempt in history
    const history = getAttemptHistory();
    const attempt = history.filter(h => h.testId === testId).pop();

    if (!attempt && Object.keys(answers).length === 0) {
      container.innerHTML = `<div class="error"><p data-i18n="noHistory">${t('noHistory')}</p><a href="#/" class="btn btn-primary" data-i18n="backToTests">${t('backToTests')}</a></div>`;
      return;
    }

    const loadPromise = testId.startsWith('cam')
      ? this.loadCambridgeReadingTest(testId)
      : loadTestData(`data/${testId}.json`);

    loadPromise.then(testData => {
      if (attempt) {
        renderReview(testData, attempt, container);
      } else {
        const tempAttempt = {
          testId: testId,
          score: 0,
          total: testData.totalQuestions,
          bandScore: 0,
          timeTaken: 0,
          answers: { ...answers }
        };
        let correct = 0;
        const allQs = [];
        testData.passages.forEach(p => p.questions.forEach(q => allQs.push(q)));
        allQs.forEach(q => {
          const userAns = (answers[q.id] || '').trim().toLowerCase();
          const correctAns = (q.correctAnswer || '').trim().toLowerCase();
          if (userAns === correctAns) correct++;
        });
        tempAttempt.score = correct;
        tempAttempt.bandScore = bandScore(correct);
        renderReview(testData, tempAttempt, container);
      }
    }).catch(() => {
      container.innerHTML = `<div class="error">${t('errorLoadData')}</div>`;
    });
  },

  showListeningReview(testId) {
    const container = document.getElementById('mainContent');
    const history = getListeningAttemptHistory();
    const attempt = history.filter(h => h.testId === testId).pop();

    if (!attempt) {
      container.innerHTML = `<div class="error"><p data-i18n="noHistory">${t('noHistory')}</p><a href="#/" class="btn btn-primary" data-i18n="backToTests">${t('backToTests')}</a></div>`;
      return;
    }

    const loadPromise = testId.startsWith('cam')
      ? this.loadCambridgeListeningTest(testId)
      : loadTestData(`data/listening/${testId}.json`);

    loadPromise.then(testData => {
      renderListeningReview(testData, attempt, container);
    }).catch(() => {
      container.innerHTML = `<div class="error">${t('errorLoadData')}</div>`;
    });
  },

  showListeningHistory(container) {
    renderListeningHistoryPage(container);
  },

  showHistory(container) {
    renderHistoryPage(container);
  },

  showWrongBook(container) {
    renderWrongBookPage(container);
  },

  renderWritingGrid(grid) {
    const legacy = [];
    for (let i = 1; i <= 10; i++) {
      legacy.push({ id: `test${i}`, title: `${t('writing')} ${i}` });
    }
    this._renderGrid(this.cambridgeWritingBooks, legacy, 'writing', grid);
  },

  async showWritingExam(testId) {
    const container = document.getElementById('mainContent');
    container.innerHTML = `<div class="loading">${t('loading')}</div>`;
    try {
      const testData = await loadTestData(`data/writing/${testId}.json`);
      renderWritingExam(testData);
    } catch (e) {
      console.error('Writing exam error:', e);
      container.innerHTML = `<div class="error">${t('errorLoadData')}<br><small style="color:#999">${escapeHtml(e.message)}</small></div>`;
    }
  },

  showWritingReview(testId) {
    const container = document.getElementById('mainContent');
    loadTestData(`data/writing/${testId}.json`).then(testData => {
      renderWritingReview(testData, container);
    }).catch(() => {
      container.innerHTML = `<div class="error">${t('errorLoadData')}</div>`;
    });
  },

  renderSpeakingGrid(grid) {
    const legacy = [];
    for (let i = 1; i <= 10; i++) {
      legacy.push({ id: `test${i}`, title: `${t('speaking')} ${i}` });
    }
    this._renderGrid(this.cambridgeSpeakingBooks, legacy, 'speaking', grid);
  },

  async showSpeakingExam(testId) {
    const container = document.getElementById('mainContent');
    container.innerHTML = `<div class="loading">${t('loading')}</div>`;
    try {
      const testData = await loadTestData(`data/speaking/${testId}.json`);
      renderSpeakingExam(testData);
    } catch (e) {
      console.error('Speaking exam error:', e);
      container.innerHTML = `<div class="error">${t('errorLoadData')}<br><small style="color:#999">${escapeHtml(e.message)}</small></div>`;
    }
  },

  confirmRedo(testId, type) {
    const label = type === 'listening' ? t('listening') : t('reading');
    const overlay = document.createElement('div');
    overlay.className = 'modal-overlay';
    overlay.innerHTML = `
      <div class="modal">
        <h2>${t('redoExam')} ${label}</h2>
        <p>${t('submitConfirmDesc')}</p>
        <div class="modal-actions">
          <button class="btn btn-secondary" onclick="this.closest('.modal-overlay').remove()" data-i18n="cancel">${t('cancel')}</button>
          <button class="btn btn-primary" onclick="this.closest('.modal-overlay').remove(); App._doRedo('${testId}', '${type}')" data-i18n="confirm">${t('confirm')}</button>
        </div>
      </div>
    `;
    document.body.appendChild(overlay);
  },

  _doRedo(testId, type) {
    if (type === 'listening') {
      if (typeof listeningPhaseTimer !== 'undefined' && listeningPhaseTimer) {
        clearInterval(listeningPhaseTimer);
        listeningPhaseTimer = null;
      }
      clearListeningData(testId);
      window.location.hash = `#/listening-exam/${testId}`;
    } else {
      clearExamData(testId);
      window.location.hash = `#/exam/${testId}`;
    }
  }
};

window.addEventListener('DOMContentLoaded', () => App.init());
