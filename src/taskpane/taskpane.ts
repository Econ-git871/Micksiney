/**
 * Taskpane entry point
 * Main UI logic for the Table to Shapes add-in
 */

import './taskpane.css';
import { ConversionOptions } from '../core/types';
import { convertTableToShapes, checkTableSelection } from '../core/converter';

// DOM Elements
let statusIndicator: HTMLElement;
let statusIcon: HTMLElement;
let statusText: HTMLElement;
let convertBtn: HTMLButtonElement;
let refreshBtn: HTMLButtonElement;
let progressSection: HTMLElement;
let progressFill: HTMLElement;
let progressText: HTMLElement;
let resultSection: HTMLElement;
let resultMessage: HTMLElement;

// Checkbox elements
let keepBorderCheckbox: HTMLInputElement;
let keepBackgroundCheckbox: HTMLInputElement;
let keepTextCheckbox: HTMLInputElement;
let keepTextFormatCheckbox: HTMLInputElement;
let deleteOriginalCheckbox: HTMLInputElement;

/**
 * Initialize the add-in when Office is ready
 */
Office.onReady((info) => {
  if (info.host === Office.HostType.PowerPoint) {
    initializeUI();
    setupEventListeners();
    checkSelection();
  }
});

/**
 * Initialize UI element references
 */
function initializeUI(): void {
  // Status elements
  statusIndicator = document.getElementById('statusIndicator')!;
  statusIcon = document.getElementById('statusIcon')!;
  statusText = document.getElementById('statusText')!;

  // Buttons
  convertBtn = document.getElementById('convertBtn') as HTMLButtonElement;
  refreshBtn = document.getElementById('refreshBtn') as HTMLButtonElement;

  // Progress elements
  progressSection = document.getElementById('progressSection')!;
  progressFill = document.getElementById('progressFill')!;
  progressText = document.getElementById('progressText')!;

  // Result elements
  resultSection = document.getElementById('resultSection')!;
  resultMessage = document.getElementById('resultMessage')!;

  // Checkboxes
  keepBorderCheckbox = document.getElementById('keepBorder') as HTMLInputElement;
  keepBackgroundCheckbox = document.getElementById('keepBackground') as HTMLInputElement;
  keepTextCheckbox = document.getElementById('keepText') as HTMLInputElement;
  keepTextFormatCheckbox = document.getElementById('keepTextFormat') as HTMLInputElement;
  deleteOriginalCheckbox = document.getElementById('deleteOriginal') as HTMLInputElement;
}

/**
 * Set up event listeners
 */
function setupEventListeners(): void {
  convertBtn.addEventListener('click', handleConvert);
  refreshBtn.addEventListener('click', checkSelection);

  // Handle text format checkbox dependency
  keepTextCheckbox.addEventListener('change', () => {
    keepTextFormatCheckbox.disabled = !keepTextCheckbox.checked;
    if (!keepTextCheckbox.checked) {
      keepTextFormatCheckbox.checked = false;
    }
  });

  // Listen for selection changes
  Office.context.document.addHandlerAsync(
    Office.EventType.DocumentSelectionChanged,
    checkSelection
  );
}

/**
 * Check if a table is selected and update UI
 */
async function checkSelection(): Promise<void> {
  hideResult();

  try {
    const result = await checkTableSelection();

    if (result.isValid) {
      setStatus('ready', '●', result.message);
      convertBtn.disabled = false;
    } else {
      setStatus('default', '○', result.message);
      convertBtn.disabled = true;
    }
  } catch (error) {
    setStatus('error', '✕', '检查选择时发生错误');
    convertBtn.disabled = true;
  }
}

/**
 * Handle convert button click
 */
async function handleConvert(): Promise<void> {
  // Get conversion options
  const options: ConversionOptions = {
    keepBorder: keepBorderCheckbox.checked,
    keepBackground: keepBackgroundCheckbox.checked,
    keepText: keepTextCheckbox.checked,
    keepTextFormat: keepTextFormatCheckbox.checked,
    deleteOriginal: deleteOriginalCheckbox.checked,
  };

  // Disable buttons during conversion
  convertBtn.disabled = true;
  refreshBtn.disabled = true;

  // Show progress
  showProgress();
  setStatus('processing', '◐', '正在转换...');

  try {
    const result = await convertTableToShapes(options, (progress, message) => {
      updateProgress(progress, message);
    });

    if (result.success) {
      showResult('success', result.message);
      setStatus('ready', '✓', '转换完成');
    } else {
      showResult('error', result.message);
      setStatus('error', '✕', result.message);
    }
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : '转换失败';
    showResult('error', errorMessage);
    setStatus('error', '✕', errorMessage);
  }

  // Re-enable buttons
  refreshBtn.disabled = false;
  hideProgress();

  // Check selection again to update state
  setTimeout(checkSelection, 500);
}

/**
 * Set status indicator state
 */
function setStatus(
  state: 'default' | 'ready' | 'error' | 'processing',
  icon: string,
  text: string
): void {
  statusIndicator.className = 'status-indicator';

  switch (state) {
    case 'ready':
      statusIndicator.classList.add('ready');
      break;
    case 'error':
      statusIndicator.classList.add('error');
      break;
    case 'processing':
      statusIndicator.classList.add('processing');
      break;
  }

  statusIcon.textContent = icon;
  statusText.textContent = text;
}

/**
 * Show progress section
 */
function showProgress(): void {
  progressSection.style.display = 'block';
  progressFill.style.width = '0%';
  progressText.textContent = '正在准备...';
}

/**
 * Update progress bar
 */
function updateProgress(progress: number, message: string): void {
  progressFill.style.width = `${progress}%`;
  progressText.textContent = message;
}

/**
 * Hide progress section
 */
function hideProgress(): void {
  progressSection.style.display = 'none';
}

/**
 * Show result message
 */
function showResult(type: 'success' | 'error', message: string): void {
  resultSection.style.display = 'block';
  resultMessage.className = 'result-message ' + type;
  resultMessage.textContent = message;
}

/**
 * Hide result section
 */
function hideResult(): void {
  resultSection.style.display = 'none';
}
