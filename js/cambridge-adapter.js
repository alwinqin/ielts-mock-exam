// Cambridge IELTS data adapter — normalizes Cambridge format to app format

function fillQuestionDefaults(q) {
  if (!q.explanation) q.explanation = '';
  return q;
}

function fillSectionDefaults(s) {
  if (!s.subtitle) s.subtitle = '';
  if (!s.duration) s.duration = '';
  return s;
}

function getCambridgeReadingTest(bookData, testId) {
  const t = bookData.tests.find(t => t.id === testId);
  if (!t) return null;

  const passages = t.passages.map(p => ({
    ...p,
    questions: p.questions.map(fillQuestionDefaults)
  }));

  return {
    id: t.id,
    title: `${bookData.title} - Test ${t.testNumber}`,
    totalQuestions: 40,
    passages: passages,
    _source: 'cambridge',
    _bookId: bookData.id
  };
}

function getCambridgeListeningTest(bookData, testId) {
  const t = bookData.tests.find(t => t.id === testId);
  if (!t) return null;

  const sections = (t.parts || []).map((p, idx) => ({
    ...fillSectionDefaults(p),
    sectionIndex: idx
  }));
  sections.forEach(s => {
    s.questions = (s.questions || []).map(fillQuestionDefaults);
  });

  return {
    id: t.id,
    title: `${bookData.title} - Test ${t.testNumber}`,
    totalQuestions: 40,
    sections: sections,
    totalSections: sections.length,
    _source: 'cambridge',
    _bookId: bookData.id
  };
}

function getCambridgeReadingTests(bookData) {
  return (bookData.tests || []).map(t => ({
    id: t.id,
    title: `Test ${t.testNumber}`,
    bookId: bookData.id,
    bookTitle: bookData.title,
    testNumber: t.testNumber
  }));
}

function getCambridgeListeningTests(bookData) {
  return (bookData.tests || []).map(t => ({
    id: t.id,
    title: `Test ${t.testNumber}`,
    bookId: bookData.id,
    bookTitle: bookData.title,
    testNumber: t.testNumber
  }));
}

function parseCambridgePath(path) {
  const m = path.match(/^data\/cambridge\/([^/]+)\/(reading|listening)\.json$/);
  if (!m) return null;
  return { bookId: m[1], type: m[2] };
}

function findCambridgeTestByNumber(bookData, testNumber) {
  return bookData.tests.find(t => t.testNumber === testNumber) || null;
}
