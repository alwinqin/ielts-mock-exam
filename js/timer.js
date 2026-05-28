const Timer = {
  TOTAL_TIME: 3600, // 60 minutes in seconds
  SAVE_INTERVAL: 30, // save every 30 seconds
  remaining: 3600,
  running: false,
  intervalId: null,
  saveIntervalId: null,
  testId: null,
  onExpire: null,

  init(testId, onExpire) {
    this.testId = testId;
    this.onExpire = onExpire;

    // Restore saved timer state
    const saved = this.loadState(testId);
    if (saved && !saved.completed) {
      const elapsed = Math.floor((Date.now() - saved.savedAt) / 1000);
      this.remaining = Math.max(0, saved.remaining - elapsed);
    } else {
      this.remaining = this.TOTAL_TIME;
    }

    this.render();
    if (!saved || saved.remaining === this.TOTAL_TIME) {
      this.saveState();
    }
  },

  start() {
    if (this.running) return;
    this.running = true;

    this.intervalId = setInterval(() => {
      this.remaining--;
      this.render();
      if (this.remaining <= 0) {
        this.stop();
        if (this.onExpire) this.onExpire();
      }
    }, 1000);

    this.saveIntervalId = setInterval(() => this.saveState(), this.SAVE_INTERVAL * 1000);
  },

  stop() {
    this.running = false;
    if (this.intervalId) { clearInterval(this.intervalId); this.intervalId = null; }
    if (this.saveIntervalId) { clearInterval(this.saveIntervalId); this.saveIntervalId = null; }
  },

  pause() {
    this.running = false;
    if (this.intervalId) { clearInterval(this.intervalId); this.intervalId = null; }
    if (this.saveIntervalId) { clearInterval(this.saveIntervalId); this.saveIntervalId = null; }
    this.saveState();
  },

  resume() {
    if (!this.running && this.remaining > 0) this.start();
  },

  getRemaining() { return this.remaining; },
  getTimeUsed() { return this.TOTAL_TIME - this.remaining; },

  render() {
    const el = document.getElementById('timerDisplay');
    if (!el) return;
    el.textContent = formatTime(this.remaining);
    el.className = 'timer';
    if (this.remaining <= 60) el.classList.add('danger');
    else if (this.remaining <= 300) el.classList.add('warning');
  },

  saveState() {
    if (!this.testId) return;
    const state = {
      remaining: this.remaining,
      savedAt: Date.now(),
      completed: false
    };
    localStorage.setItem(`timer_${this.testId}`, JSON.stringify(state));
  },

  loadState(testId) {
    try {
      const data = localStorage.getItem(`timer_${testId}`);
      return data ? JSON.parse(data) : null;
    } catch { return null; }
  },

  clear(testId) {
    localStorage.removeItem(`timer_${testId}`);
  }
};
