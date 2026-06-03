let speakingTestData = null;
let speakingCurrentPart = 1;
let speakingPart1Index = 0;
let speakingMediaRecorder = null;
let speakingAudioChunks = [];
let speakingRecordings = {};
let speakingTranscriptions = {};
let speakingPrepTimer = null;

function renderSpeakingExam(testData) {
  speakingTestData = testData;
  speakingCurrentPart = 1;
  speakingPart1Index = 0;
  speakingRecordings = {};
  speakingTranscriptions = {};

  const container = document.getElementById('mainContent');
  container.innerHTML = `
    <div class="speaking-container">
      <div class="speaking-topbar">
        <span class="test-title">${testData.id.toUpperCase()} - ${t('speaking')}</span>
        <span class="phase-badge" id="speakingPhaseBadge">${t('part1')}</span>
        <span class="progress-text" id="speakingProgress"></span>
      </div>
      <div class="speaking-progress-bar">
        <div class="progress-track">
          <div class="progress-step current" id="spPart1"><div class="step-dot">1</div><div class="step-label">${t('part1')}</div></div>
          <div class="progress-step" id="spPart2"><div class="step-dot">2</div><div class="step-label">${t('part2')}</div></div>
          <div class="progress-step" id="spPart3"><div class="step-dot">3</div><div class="step-label">${t('part3')}</div></div>
        </div>
      </div>
      <div class="speaking-main" id="speakingMain"></div>
    </div>
  `;

  renderPart1Question();
}

function renderPart1Question() {
  const questions = speakingTestData.part1 || [];
  if (speakingPart1Index >= questions.length) {
    startPart2();
    return;
  }

  const q = questions[speakingPart1Index];
  const qNum = speakingPart1Index + 1;
  const total = questions.length;

  document.getElementById('speakingPhaseBadge').textContent = `${t('part1')} (Q${qNum}/${total})`;
  document.getElementById('speakingProgress').textContent = '';
  document.querySelectorAll('.progress-step').forEach(s => s.classList.remove('current'));
  document.getElementById('spPart1').classList.add('current');

  const main = document.getElementById('speakingMain');
  const qid = `p1_q${speakingPart1Index}`;
  const hasRecording = speakingRecordings[qid];
  const hasTranscription = speakingTranscriptions[qid];

  main.innerHTML = `
    <div class="speaking-question-panel">
      <h3>${t('part1')} - Question ${qNum}</h3>
      <div class="speaking-question-text">${escapeHtml(q.question)}</div>
      ${q.followUp ? `<div class="speaking-followup" style="margin-top:8px;color:#888;font-size:0.85rem;">Follow-up: ${escapeHtml(q.followUp)}</div>` : ''}

      <div class="speaking-controls">
        <button class="btn btn-primary" id="speakingRecordBtn" onclick="toggleRecording('${qid}')">${t('startRecording')}</button>
        <button class="btn btn-secondary" id="speakingPlayBtn" onclick="playRecording('${qid}')" ${!hasRecording ? 'disabled' : ''}>${t('playRecording')}</button>
        <button class="btn btn-secondary" id="speakingTranscribeBtn" onclick="transcribeRecording('${qid}')" ${!hasRecording ? 'disabled' : ''}>${t('transcribe')}</button>
      </div>

      <div id="speakingRecordingStatus" style="margin-top:8px;font-size:0.85rem;color:#888;"></div>

      ${hasTranscription ? `<div class="speaking-transcription"><strong>${t('transcription')}:</strong><br>${escapeHtml(speakingTranscriptions[qid])}</div>` : ''}
      ${hasRecording ? `<div class="speaking-recording-saved">${t('recordingSaved')} (${getRecordingSize(qid)})</div>` : ''}

      <div style="margin-top:20px;">
        <button class="btn btn-primary" onclick="nextPart1Question()">${t('nextQuestion')} →</button>
      </div>
    </div>
  `;
}

function nextPart1Question() {
  speakingPart1Index++;
  renderPart1Question();
}

function startPart2() {
  speakingCurrentPart = 2;
  const cue = speakingTestData.part2;

  document.getElementById('speakingPhaseBadge').textContent = t('part2');
  document.querySelectorAll('.progress-step').forEach(s => s.classList.remove('current'));
  document.getElementById('spPart2').classList.add('current');

  const main = document.getElementById('speakingMain');
  const qid = 'part2';

  main.innerHTML = `
    <div class="speaking-question-panel">
      <h3>${t('part2')} - ${t('cueCard')}</h3>
      <div class="speaking-cue-card">
        <p><strong>${escapeHtml(cue.cueCard)}</strong></p>
        <ul style="margin-top:8px;">
          ${(cue.bulletPoints || []).map(b => `<li>${escapeHtml(b)}</li>`).join('')}
        </ul>
      </div>

      <div id="speakingPrepSection">
        <p style="color:#e65100;font-weight:600;margin:16px 0;">
          ${t('prepTime')}: <span id="speakingPrepTimer">1:00</span>
        </p>
        <button class="btn btn-primary" onclick="startSpeakingPrep()">Start Preparation (1 min)</button>
      </div>

      <div id="speakingPart2Controls" style="display:none;">
        <div class="speaking-controls">
          <button class="btn btn-primary" onclick="toggleRecording('${qid}')">${t('startRecording')}</button>
          <button class="btn btn-secondary" onclick="playRecording('${qid}')">${t('playRecording')}</button>
          <button class="btn btn-secondary" onclick="transcribeRecording('${qid}')">${t('transcribe')}</button>
        </div>
        <div id="speakingRecordingStatus2" style="margin-top:8px;font-size:0.85rem;color:#888;"></div>
      </div>

      <div id="speakingPart2Result"></div>

      <div style="margin-top:20px;">
        <button class="btn btn-primary" onclick="startPart3()">${t('nextPart')} →</button>
      </div>
    </div>
  `;
}

function startSpeakingPrep() {
  document.getElementById('speakingPrepSection').innerHTML = `
    <p style="color:#e65100;font-weight:600;margin:16px 0;">
      ${t('prepTime')}: <span id="speakingPrepTimer" style="font-size:1.3rem;">1:00</span>
    </p>
  `;
  document.getElementById('speakingPart2Controls').style.display = 'block';

  let remaining = 60;
  if (speakingPrepTimer) { clearInterval(speakingPrepTimer); }
  speakingPrepTimer = setInterval(() => {
    remaining--;
    const el = document.getElementById('speakingPrepTimer');
    if (el) {
      const m = Math.floor(remaining / 60);
      const s = remaining % 60;
      el.textContent = `${m}:${s.toString().padStart(2, '0')}`;
      if (remaining <= 5) el.style.color = '#d32f2f';
    }
    if (remaining <= 0) {
      clearInterval(speakingPrepTimer);
      speakingPrepTimer = null;
      if (el) el.textContent = 'Time\'s up! Start speaking!';
    }
  }, 1000);
}

function startPart3() {
  speakingCurrentPart = 3;
  const questions = speakingTestData.part2?.followUpQuestions || [];
  let idx = 0;

  document.getElementById('speakingPhaseBadge').textContent = t('part3');
  document.querySelectorAll('.progress-step').forEach(s => s.classList.remove('current'));
  document.getElementById('spPart3').classList.add('current');

  const main = document.getElementById('speakingMain');
  renderPart3Question(questions, idx, main);
}

function renderPart3Question(questions, idx, main) {
  if (idx >= questions.length) {
    main.innerHTML = `
      <div class="speaking-question-panel" style="text-align:center;">
        <h3>${t('speaking')} - ${t('finish')}</h3>
        <p style="margin:20px 0;color:#666;">You have completed all parts of the speaking test.</p>
        <p style="margin-bottom:20px;color:#888;">Review your recordings and transcriptions above.</p>
        <a href="#/" class="btn btn-primary">${t('backToTests')}</a>
      </div>
    `;
    return;
  }

  const q = questions[idx];
  const qid = `p3_q${idx}`;
  const hasRecording = speakingRecordings[qid];
  const escapedQ = escapeHtml(q).replace(/'/g, "\\'");

  main.innerHTML = `
    <div class="speaking-question-panel">
      <h3>${t('part3')} - Question ${idx + 1}</h3>
      <div class="speaking-question-text">${escapeHtml(q)}</div>

      <div class="speaking-controls">
        <button class="btn btn-primary" id="speakingRecordBtn">${t('startRecording')}</button>
        <button class="btn btn-secondary" id="speakingPlayBtn" ${!hasRecording ? 'disabled' : ''}>${t('playRecording')}</button>
        <button class="btn btn-secondary" id="speakingTranscribeBtn" ${!hasRecording ? 'disabled' : ''}>${t('transcribe')}</button>
      </div>

      <div id="speakingRecordingStatus" style="margin-top:8px;font-size:0.85rem;color:#888;"></div>
      <div id="speakingPart3Result"></div>

      <div style="margin-top:20px;">
        <button class="btn btn-primary" id="speakingNextBtn">${t('nextQuestion')} →</button>
      </div>
    </div>
  `;

  // Attach event listeners (safe, no inline onclick)
  document.getElementById('speakingRecordBtn').addEventListener('click', () => toggleRecording(qid));
  document.getElementById('speakingPlayBtn').addEventListener('click', () => playRecording(qid));
  document.getElementById('speakingTranscribeBtn').addEventListener('click', () => transcribeRecording(qid));
  document.getElementById('speakingNextBtn').addEventListener('click', () => {
    renderPart3Question(questions, idx + 1, main);
  });
}

// Recording utilities
function toggleRecording(qid) {
  const btn = document.getElementById('speakingRecordBtn') || document.querySelector('.speaking-controls .btn-primary');
  if (speakingMediaRecorder && speakingMediaRecorder.state === 'recording') {
    stopRecording();
    return;
  }
  startRecording(qid);
}

function startRecording(qid) {
  if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
    alert('Recording not supported in this browser. Please use Chrome, Firefox, or Edge.');
    return;
  }

  navigator.mediaDevices.getUserMedia({ audio: true }).then(stream => {
    speakingAudioChunks = [];
    const options = { mimeType: getSupportedMimeType() };
    speakingMediaRecorder = new MediaRecorder(stream, options);

    speakingMediaRecorder.ondataavailable = (e) => {
      if (e.data.size > 0) speakingAudioChunks.push(e.data);
    };

    speakingMediaRecorder.onstop = () => {
      const blob = new Blob(speakingAudioChunks, { type: options.mimeType || 'audio/webm' });
      speakingRecordings[qid] = blob;
      stream.getTracks().forEach(t => t.stop());

      const status = document.getElementById('speakingRecordingStatus') || document.getElementById('speakingRecordingStatus2');
      if (status) status.innerHTML = `<span style="color:#2e7d32;">${t('recordingSaved')} (${(blob.size/1024).toFixed(0)} KB)</span>`;

      // Enable play and transcribe buttons
      document.querySelectorAll('#speakingPlayBtn, #speakingTranscribeBtn').forEach(b => b.disabled = false);

      // Update result area
      const result = document.getElementById('speakingPart2Result') || document.getElementById('speakingPart3Result');
      if (result) {
        result.innerHTML = `<div class="speaking-recording-saved" style="margin-top:8px;">${t('recordingSaved')}</div>`;
      }

      updateAllButtons();
    };

    speakingMediaRecorder.start();
    updateAllButtons(qid);
    const status = document.getElementById('speakingRecordingStatus') || document.getElementById('speakingRecordingStatus2');
    if (status) status.innerHTML = '<span style="color:#e65100;">Recording... click Stop to finish</span>';
  }).catch(e => {
    alert('Microphone access denied. Please allow microphone access to use the speaking test.');
    console.error(e);
  });
}

function stopRecording() {
  if (speakingMediaRecorder && speakingMediaRecorder.state === 'recording') {
    speakingMediaRecorder.stop();
  }
  updateAllButtons();
}

function playRecording(qid) {
  const blob = speakingRecordings[qid];
  if (!blob) return;

  const url = URL.createObjectURL(blob);
  const audio = new Audio(url);
  audio.play();
}

function transcribeRecording(qid) {
  const blob = speakingRecordings[qid];
  if (!blob) return;

  const btn = document.querySelector('#speakingTranscribeBtn') || document.querySelectorAll('.btn-secondary')[1];
  if (btn) btn.textContent = t('transcribing');

  // Convert to WAV for whisper (best compatibility)
  const formData = new FormData();
  formData.append('audio', blob, 'recording.wav');

  fetch('http://localhost:8081/transcribe', {
    method: 'POST',
    body: blob,
    headers: { 'Content-Type': 'application/octet-stream' }
  })
  .then(r => r.json())
  .then(data => {
    const text = data.text || '';
    speakingTranscriptions[qid] = text;
    if (btn) btn.textContent = t('transcribe');

    // Show transcription
    const resultArea = document.getElementById('speakingPart2Result') || document.getElementById('speakingPart3Result') || document.getElementById('speakingMain');
    const transDiv = document.createElement('div');
    transDiv.className = 'speaking-transcription';
    transDiv.innerHTML = `<strong>${t('transcription')}:</strong><br>${escapeHtml(text) || '(no speech detected)'}`;

    // Add to appropriate place
    const existing = document.querySelector('.speaking-question-panel');
    if (existing) {
      const old = existing.querySelector('.speaking-transcription');
      if (old) old.remove();
      existing.appendChild(transDiv);
    }
  })
  .catch(e => {
    if (btn) btn.textContent = t('transcribe');
    alert('Transcription server not running. Start it with: python3 speech-server.py');
    console.error(e);
  });
}

function getSupportedMimeType() {
  const types = ['audio/webm;codecs=opus', 'audio/webm', 'audio/ogg;codecs=opus', 'audio/wav', 'audio/mp4'];
  for (const t of types) {
    if (MediaRecorder.isTypeSupported(t)) return t;
  }
  return 'audio/webm';
}

function getRecordingSize(qid) {
  const b = speakingRecordings[qid];
  return b ? `${(b.size/1024).toFixed(0)} KB` : '';
}

function updateAllButtons(activeQid) {
  document.querySelectorAll('.speaking-controls .btn-primary').forEach(b => {
    if (speakingMediaRecorder && speakingMediaRecorder.state === 'recording') {
      b.textContent = t('stopRecording');
    } else {
      b.textContent = t('startRecording');
    }
  });
}
