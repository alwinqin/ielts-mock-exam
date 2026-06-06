/**
 * Reusable modal dialog utility.
 *
 * showModal({
 *   title: 'Confirm',
 *   message: 'Are you sure?',
 *   type: 'confirm',          // 'alert' | 'confirm'
 *   confirmText: 'OK',        // optional
 *   cancelText: 'Cancel',     // optional (confirm only)
 *   onConfirm: () => { ... }, // callback (confirm only)
 * });
 */

function showModal(options = {}) {
  const {
    title = '',
    message = '',
    type = 'alert',
    confirmText = typeof t === 'function' ? t('done') : 'OK',
    cancelText = typeof t === 'function' ? t('close') : 'Cancel',
    onConfirm = null,
  } = options;

  const overlay = document.createElement('div');
  overlay.className = 'modal-overlay';
  overlay.setAttribute('role', 'dialog');
  overlay.setAttribute('aria-modal', 'true');
  overlay.setAttribute('aria-label', title || message);

  const cancelHtml = type === 'confirm'
    ? `<button id="modalCancelBtn" class="btn btn-secondary">${cancelText}</button>`
    : '';

  overlay.innerHTML = `
    <div class="modal">
      ${title ? `<h2>${title}</h2>` : ''}
      <p>${message}</p>
      <div class="modal-actions">
        ${cancelHtml}
        <button id="modalConfirmBtn" class="btn btn-primary">${confirmText}</button>
      </div>
    </div>
  `;

  document.body.appendChild(overlay);

  const confirmBtn = overlay.querySelector('#modalConfirmBtn');
  const cancelBtn = overlay.querySelector('#modalCancelBtn');

  function close() {
    overlay.remove();
    document.removeEventListener('keydown', onKeyDown);
  }

  function confirm() {
    close();
    if (onConfirm) onConfirm();
  }

  function onKeyDown(e) {
    if (e.key === 'Escape') {
      if (type === 'alert') confirm();
      else close();
    }
    if (e.key === 'Enter' && document.activeElement !== cancelBtn) {
      confirm();
    }
  }

  document.addEventListener('keydown', onKeyDown);

  confirmBtn.addEventListener('click', confirm);
  if (cancelBtn) {
    cancelBtn.addEventListener('click', close);
  }

  // Click overlay to close (for alert or if clicking outside the modal)
  overlay.addEventListener('click', function (e) {
    if (e.target === overlay) {
      if (type === 'alert') confirm();
      else close();
    }
  });

  // Focus the confirm button
  requestAnimationFrame(() => confirmBtn.focus());
}
