let speakingTestData = null;
let speakingCurrentPart = 1;
let speakingPart1Index = 0;
let speakingMediaRecorder = null;
let speakingAudioChunks = [];
let speakingRecordings = {};
let speakingTranscriptions = {};
let speakingPrepTimer = null;
let speakingPart2Timer = null;
let speakingPart2TimeRemaining = 120;

function speakingBeforeUnload(e) {
  if (Object.keys(speakingRecordings).length > 0) {
    e.preventDefault();
    e.returnValue = '';
  }
}

function renderSpeakingExam(testData) {
  speakingTestData = testData;
  speakingCurrentPart = 1;
  speakingPart1Index = 0;
  speakingRecordings = {};
  speakingTranscriptions = {};

  window.addEventListener('beforeunload', speakingBeforeUnload);

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
      ${q.followUp ? `<div class="speaking-followup" style="margin-top:8px;color:var(--text-muted);font-size:0.85rem;">Follow-up: ${escapeHtml(q.followUp)}</div>` : ''}

      <div class="speaking-controls">
        <button class="btn btn-primary" id="speakingRecordBtn" data-action="speaking-record" data-qid="${qid}">${t('startRecording')}</button>
        <button class="btn btn-secondary" id="speakingPlayBtn" data-action="speaking-play" data-qid="${qid}" ${!hasRecording ? 'disabled' : ''}>${t('playRecording')}</button>
        <button class="btn btn-secondary" id="speakingTranscribeBtn" data-action="speaking-transcribe" data-qid="${qid}" ${!hasRecording ? 'disabled' : ''}>${t('transcribe')}</button>
      </div>
      <div class="volume-meter" style="height:6px;background:var(--color-border);border-radius:3px;margin-top:8px;display:none;">
        <div class="volume-bar" style="height:100%;width:0%;background:var(--color-success);border-radius:3px;transition:width 0.1s;"></div>
      </div>

      <div id="speakingRecordingStatus" style="margin-top:8px;font-size:0.85rem;color:var(--text-muted);"></div>

      ${hasTranscription ? `<div class="speaking-transcription"><strong>${t('transcription')}:</strong><br>${escapeHtml(speakingTranscriptions[qid])}</div>` : ''}
      ${hasRecording ? `<div class="speaking-recording-saved">${t('recordingSaved')} (${getRecordingSize(qid)})</div>` : ''}

      <div style="margin-top:20px;">
        <button class="btn btn-primary" data-action="speaking-next-part1">${t('nextQuestion')} →</button>
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
        <p style="color:var(--color-warning);font-weight:600;margin:16px 0;">
          ${t('prepTime')}: <span id="speakingPrepTimer">1:00</span>
        </p>
        <button class="btn btn-primary" data-action="speaking-start-prep">Start Preparation (1 min)</button>
      </div>

      <div id="speakingPart2Controls" style="display:none;">
        <div id="speakingPart2Timer" style="text-align:center;margin-bottom:12px;font-size:1.5rem;font-weight:700;color:var(--text-heading);"></div>
        <div class="speaking-controls">
          <button class="btn btn-primary" data-action="speaking-record" data-qid="${qid}">${t('startRecording')}</button>
          <button class="btn btn-secondary" data-action="speaking-play" data-qid="${qid}">${t('playRecording')}</button>
          <button class="btn btn-secondary" data-action="speaking-transcribe" data-qid="${qid}">${t('transcribe')}</button>
        </div>
        <div id="speakingRecordingStatus2" style="margin-top:8px;font-size:0.85rem;color:var(--text-muted);"></div>
      </div>

      <div id="speakingPart2Result"></div>

      <div style="margin-top:20px;">
        <button class="btn btn-primary" data-action="speaking-start-part3">${t('nextPart')} →</button>
      </div>
    </div>
  `;
}

function startSpeakingPrep() {
  document.getElementById('speakingPrepSection').innerHTML = `
    <p style="color:var(--color-warning);font-weight:600;margin:16px 0;">
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
      if (remaining <= 5) el.style.color = 'var(--color-danger)';
    }
    if (remaining <= 0) {
      clearInterval(speakingPrepTimer);
      speakingPrepTimer = null;
      if (el) el.textContent = t('timeUpStartSpeaking');
      startSpeakingTimer();
    }
  }, 1000);
}

function startSpeakingTimer() {
  speakingPart2TimeRemaining = 120;
  if (speakingPart2Timer) { clearInterval(speakingPart2Timer); }
  const timerEl = document.getElementById('speakingPart2Timer');
  if (timerEl) timerEl.textContent = '2:00';

  speakingPart2Timer = setInterval(() => {
    speakingPart2TimeRemaining--;
    if (timerEl) {
      const m = Math.floor(speakingPart2TimeRemaining / 60);
      const s = speakingPart2TimeRemaining % 60;
      timerEl.textContent = `${m}:${s.toString().padStart(2, '0')}`;
      if (speakingPart2TimeRemaining <= 30) timerEl.style.color = 'var(--color-warning)';
      if (speakingPart2TimeRemaining <= 10) timerEl.style.color = 'var(--color-danger)';
    }
    if (speakingPart2TimeRemaining <= 0) {
      clearInterval(speakingPart2Timer);
      speakingPart2Timer = null;
      if (timerEl) timerEl.textContent = t('timeUp');
      if (speakingMediaRecorder && speakingMediaRecorder.state === 'recording') {
        stopRecording();
      }
    }
  }, 1000);
}

function startPart3() {
  speakingCurrentPart = 3;
  // Flatten part3 topic groups into a flat question list
  const part3Data = speakingTestData.part3 || [];
  let topics;
  if (Array.isArray(part3Data)) {
    topics = part3Data;
  } else {
    topics = part3Data.topics || [];
  }
  const questions = [];
  topics.forEach(topic => {
    (topic.questions || []).forEach(q => questions.push(q));
  });
  let idx = 0;

  document.getElementById('speakingPhaseBadge').textContent = t('part3');
  document.querySelectorAll('.progress-step').forEach(s => s.classList.remove('current'));
  document.getElementById('spPart3').classList.add('current');

  const main = document.getElementById('speakingMain');
  renderPart3Question(questions, idx, main);
}

function renderPart3Question(questions, idx, main) {
  if (idx >= questions.length) {
    window.removeEventListener('beforeunload', speakingBeforeUnload);
    main.innerHTML = `
      <div class="speaking-question-panel" style="text-align:center;">
        <h3>${t('speaking')} - ${t('finish')}</h3>
        <p style="margin:20px 0;color:var(--text-secondary);">${t('speakingComplete')}</p>
        <p style="margin-bottom:20px;color:var(--text-muted);">${t('reviewRecordings')}</p>
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

      <div id="speakingRecordingStatus" style="margin-top:8px;font-size:0.85rem;color:var(--text-muted);"></div>
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
    showModal({
      title: t('error'),
      message: t('recordingNotSupported')
    });
    return;
  }

  navigator.mediaDevices.getUserMedia({ audio: true }).then(stream => {
    speakingAudioChunks = [];
    const options = { mimeType: getSupportedMimeType() };
    console.log('Recording started — mimeType:', options.mimeType);
    const tracks = stream.getAudioTracks();
    if (tracks.length > 0) {
      console.log('Mic device:', tracks[0].label);
    }
    speakingMediaRecorder = new MediaRecorder(stream, options);

    // Volume meter
    let audioCtx, analyser, meterAnim;
    const volMeter = document.querySelector('.volume-meter');
    const volBar = document.querySelector('.volume-bar');
    if (volMeter && volBar) {
      try {
        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        analyser = audioCtx.createAnalyser();
        analyser.fftSize = 256;
        audioCtx.createMediaStreamSource(stream).connect(analyser);
        const buf = new Uint8Array(analyser.frequencyBinCount);
        volMeter.style.display = 'block';
        const updateMeter = () => {
          analyser.getByteFrequencyData(buf);
          const avg = buf.reduce((a, b) => a + b, 0) / buf.length;
          const pct = Math.min(100, avg / 128 * 100);
          volBar.style.width = pct + '%';
          volBar.style.background = avg < 5 ? 'var(--color-border)' : avg < 20 ? 'var(--color-warning)' : 'var(--color-success)';
          meterAnim = requestAnimationFrame(updateMeter);
        };
        updateMeter();
      } catch (e) { console.warn('Volume meter not supported:', e); }
    }

    speakingMediaRecorder.ondataavailable = (e) => {
      console.log('DataAvailable — size:', e.data.size);
      if (e.data.size > 0) speakingAudioChunks.push(e.data);
    };

    speakingMediaRecorder.onerror = (e) => {
      console.error('MediaRecorder error:', e);
    };

    speakingMediaRecorder.onstop = () => {
      if (meterAnim) cancelAnimationFrame(meterAnim);
      if (audioCtx) audioCtx.close().catch(() => {});
      if (volMeter) volMeter.style.display = 'none';
      console.log('Recording stopped — chunks:', speakingAudioChunks.length, 'chunks');
      const blob = new Blob(speakingAudioChunks, { type: options.mimeType || 'audio/webm' });
      console.log('Recording blob size:', blob.size, 'bytes');
      speakingRecordings[qid] = blob;
      stream.getTracks().forEach(t => t.stop());

      const status = document.getElementById('speakingRecordingStatus') || document.getElementById('speakingRecordingStatus2');
      if (status) status.innerHTML = `<span style="color:${blob.size > 0 ? 'var(--color-success)' : 'var(--color-danger)'};">${t('recordingSaved')} (${(blob.size/1024).toFixed(0)} KB)</span>`;

      // Enable play and transcribe buttons
      document.querySelectorAll('#speakingPlayBtn, #speakingTranscribeBtn').forEach(b => b.disabled = false);

      // Update result area
      const result = document.getElementById('speakingPart2Result') || document.getElementById('speakingPart3Result');
      if (result) {
        result.innerHTML = `<div class="speaking-recording-saved" style="margin-top:8px;">${t('recordingSaved')} (${(blob.size/1024).toFixed(0)} KB)</div>`;
      }

      updateAllButtons();
    };

    speakingMediaRecorder.start();
    updateAllButtons(qid);
    const status = document.getElementById('speakingRecordingStatus') || document.getElementById('speakingRecordingStatus2');
    if (status) status.innerHTML = '<span style="color:var(--color-warning);">Recording... click Stop to finish</span>';
  }).catch(e => {
    showModal({ message: t('microphoneDenied') });
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
  console.log('playRecording called — qid:', qid, 'available keys:', Object.keys(speakingRecordings));
  const blob = speakingRecordings[qid];
  if (!blob) {
    console.error('No recording found for qid:', qid);
    return;
  }
  console.log('Playing — size:', blob.size, 'bytes, type:', blob.type);

  const url = URL.createObjectURL(blob);
  const audio = new Audio(url);
  audio.onloadedmetadata = () => console.log('Audio duration:', audio.duration, 's');
  audio.onerror = () => console.error('Audio error:', audio.error);
  audio.play().then(() => {
    console.log('Playback started OK');
  }).catch(e => {
    console.error('Playback failed:', e.message);
  });
}

function transcribeRecording(qid) {
  const blob = speakingRecordings[qid];
  if (!blob) return;

  const btn = document.querySelector('#speakingTranscribeBtn') || document.querySelectorAll('.btn-secondary')[1];
  if (btn) btn.textContent = t('transcribing');

  transcribeAudio(blob)
    .then(text => {
      speakingTranscriptions[qid] = text;
      if (btn) btn.textContent = t('transcribe');

      const resultArea = document.getElementById('speakingPart2Result') || document.getElementById('speakingPart3Result') || document.getElementById('speakingMain');
      const transDiv = document.createElement('div');
      transDiv.className = 'speaking-transcription';
      transDiv.innerHTML = `<strong>${t('transcription')}:</strong><br>${escapeHtml(text) || '(no speech detected)'}`;

      const existing = document.querySelector('.speaking-question-panel');
      if (existing) {
        const old = existing.querySelector('.speaking-transcription');
        if (old) old.remove();
        existing.appendChild(transDiv);
      }
    })
    .catch(e => {
      if (btn) btn.textContent = t('transcribe');
      showModal({ message: t('transcriptionServerDown') });
      console.error(e);
    });
}

async function transcribeAudio(blob) {
  if (typeof isTauri !== 'undefined' && isTauri && window.__TAURI__) {
    const buf = await blob.arrayBuffer();
    const bytes = Array.from(new Uint8Array(buf));
    return await window.__TAURI__.core.invoke('transcribe', { audio: bytes });
  }
  if (typeof isFileProtocol !== 'undefined' && !isFileProtocol) {
    try {
      const resp = await fetch('http://localhost:8081/transcribe', { method: 'POST', body: blob });
      if (resp.ok) {
        const data = await resp.json();
        return data.text || '';
      }
    } catch (e) {
      // Server not available — fall through to Web Speech API
    }
  }
  if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
    return new Promise((resolve, reject) => {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      const recognition = new SpeechRecognition();
      recognition.lang = 'en-US';
      recognition.interimResults = false;
      recognition.maxAlternatives = 1;
      const audioUrl = URL.createObjectURL(blob);
      const audio = new Audio(audioUrl);
      recognition.onresult = (event) => {
        resolve(event.results[0][0].transcript);
        URL.revokeObjectURL(audioUrl);
      };
      recognition.onerror = (event) => {
        URL.revokeObjectURL(audioUrl);
        reject(new Error('Speech recognition error: ' + event.error));
      };
      recognition.onend = () => URL.revokeObjectURL(audioUrl);
      audio.onended = () => recognition.stop();
      recognition.start();
      audio.play().catch(e => reject(e));
    });
  }
  throw new Error('No transcription method available');
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
