/* ============================================
   BEACON -- Application Logic
   ============================================ */

// ---- Language System ----

let currentLanguage = 'en';

const UI_STRINGS = {
    en: {
        // Tabs
        tabScanner: 'Scam Scanner',
        tabContracts: 'Contract Reader',
        tabRights: 'Rights Navigator',
        // Scanner panel
        scanHeading: 'Scan a Message',
        scanSubheading: 'Paste any suspicious email, text, letter, or message below.',
        scanPlaceholder: 'Paste the suspicious message here...\n\nExample: \'Dear valued customer, your account has been compromised. Click here immediately to verify your identity or your account will be permanently closed within 24 hours...\'',
        scanContextPlaceholder: 'Optional: Add context (e.g., \'I received this via text from an unknown number\')',
        scanBtn: 'Analyze Message',
        scanExample: 'Try Example',
        scanClear: 'Clear',
        scanUpload: 'Upload Screenshot (multimodal)',
        scanResultPlaceholder: 'Results will appear here',
        scanResultHint: 'Paste a message and click "Analyze" to get started.',
        // Contract panel
        contractHeading: 'Analyze a Document',
        contractSubheading: 'Paste contract text, lease terms, loan agreements, or any legal document.',
        contractPlaceholder: 'Paste the contract or document text here...',
        contractBtn: 'Analyze Document',
        contractExample: 'Try Example',
        contractClear: 'Clear',
        contractResultPlaceholder: 'Results will appear here',
        contractResultHint: 'Paste a document and click "Analyze" to get started.',
        // Rights panel
        rightsHeading: 'Know Your Rights',
        rightsSubheading: 'Describe your situation and Beacon will explain your legal protections.',
        rightsPlaceholder: 'Describe your situation...\n\nExample: \'My landlord is refusing to return my security deposit. I lived in the apartment for 2 years, left it clean, and gave 30 days notice. They say they\'re keeping it for normal wear and tear.\'',
        rightsBtn: 'Find My Rights',
        rightsExample: 'Try Example',
        rightsClear: 'Clear',
        rightsResultPlaceholder: 'Results will appear here',
        rightsResultHint: 'Describe your situation and click "Find My Rights" to get started.',
        // Loading
        loadingDeepAnalysis: 'Running deep analysis with Gemma 4...',
        loadingNoFlags: 'No instant red flags. Running deep analysis with Gemma 4...',
        loadingAnalyzeScreenshot: 'Analyzing screenshot with Gemma 4 vision...',
        loadingAnalyzeMessage: 'Analyzing message with Gemma 4...',
        loadingDocument: 'Analyzing document with Gemma 4...',
        loadingRights: 'Researching your rights with Gemma 4...',
        // Errors
        analysisFailed: 'Analysis failed',
        // Common
        back: 'Back',
        remove: 'Remove',
    },
    es: {
        tabScanner: 'Detector de Estafas',
        tabContracts: 'Lector de Contratos',
        tabRights: 'Navegador de Derechos',
        scanHeading: 'Analizar un Mensaje',
        scanSubheading: 'Pegue cualquier correo, texto o mensaje sospechoso a continuacion.',
        scanPlaceholder: 'Pegue el mensaje sospechoso aqui...\n\nEjemplo: \'Estimado cliente, su cuenta ha sido comprometida. Haga clic aqui inmediatamente para verificar su identidad o su cuenta sera cerrada permanentemente en 24 horas...\'',
        scanContextPlaceholder: 'Opcional: Agregue contexto (ej., \'Recibi esto por mensaje de un numero desconocido\')',
        scanBtn: 'Analizar Mensaje',
        scanExample: 'Probar Ejemplo',
        scanClear: 'Limpiar',
        scanUpload: 'Subir captura de pantalla',
        scanResultPlaceholder: 'Los resultados apareceran aqui',
        scanResultHint: 'Pegue un mensaje y haga clic en "Analizar" para comenzar.',
        contractHeading: 'Analizar un Documento',
        contractSubheading: 'Pegue texto de contrato, terminos de arrendamiento o cualquier documento legal.',
        contractPlaceholder: 'Pegue el texto del contrato o documento aqui...',
        contractBtn: 'Analizar Documento',
        contractExample: 'Probar Ejemplo',
        contractClear: 'Limpiar',
        contractResultPlaceholder: 'Los resultados apareceran aqui',
        contractResultHint: 'Pegue un documento y haga clic en "Analizar" para comenzar.',
        rightsHeading: 'Conozca Sus Derechos',
        rightsSubheading: 'Describa su situacion y Beacon le explicara sus protecciones legales.',
        rightsPlaceholder: 'Describa su situacion...\n\nEjemplo: \'Mi arrendador se niega a devolver mi deposito de seguridad. Vivi en el apartamento por 2 anos, lo deje limpio y di 30 dias de aviso.\'',
        rightsBtn: 'Buscar Mis Derechos',
        rightsExample: 'Probar Ejemplo',
        rightsClear: 'Limpiar',
        rightsResultPlaceholder: 'Los resultados apareceran aqui',
        rightsResultHint: 'Describa su situacion y haga clic en "Buscar Mis Derechos" para comenzar.',
        loadingDeepAnalysis: 'Ejecutando analisis profundo con Gemma 4...',
        loadingNoFlags: 'Sin alertas inmediatas. Ejecutando analisis profundo con Gemma 4...',
        loadingAnalyzeScreenshot: 'Analizando captura con vision Gemma 4...',
        loadingAnalyzeMessage: 'Analizando mensaje con Gemma 4...',
        loadingDocument: 'Analizando documento con Gemma 4...',
        loadingRights: 'Investigando sus derechos con Gemma 4...',
        analysisFailed: 'El analisis fallo',
        back: 'Volver',
        remove: 'Eliminar',
    },
};

function getStr(key) {
    if (UI_STRINGS[currentLanguage] && UI_STRINGS[currentLanguage][key]) {
        return UI_STRINGS[currentLanguage][key];
    }
    return UI_STRINGS.en[key] || key;
}

function changeLanguage(lang) {
    currentLanguage = lang;
    applyLanguageToUI();
}

function applyLanguageToUI() {
    // Tabs
    const tabLabels = document.querySelectorAll('.tab[data-tab] span');
    const tabMap = { scanner: 'tabScanner', contracts: 'tabContracts', rights: 'tabRights' };
    document.querySelectorAll('.tab[data-tab]').forEach(tab => {
        const key = tabMap[tab.dataset.tab];
        if (key) {
            const span = tab.querySelector('span');
            if (span) span.textContent = getStr(key);
        }
    });

    // Scanner panel
    const scanHeader = document.querySelector('#panel-scanner .input-header h2');
    if (scanHeader) scanHeader.textContent = getStr('scanHeading');
    const scanSub = document.querySelector('#panel-scanner .input-header p');
    if (scanSub) scanSub.textContent = getStr('scanSubheading');
    const scanInput = document.getElementById('scanInput');
    if (scanInput) scanInput.placeholder = getStr('scanPlaceholder');
    const scanCtx = document.getElementById('scanContext');
    if (scanCtx) scanCtx.placeholder = getStr('scanContextPlaceholder');
    const scanBtn = document.getElementById('scanBtn');
    if (scanBtn) {
        const icon = scanBtn.querySelector('i');
        scanBtn.innerHTML = '';
        if (icon) scanBtn.appendChild(icon);
        scanBtn.appendChild(document.createTextNode(' ' + getStr('scanBtn')));
    }

    // Contract panel
    const contractHeader = document.querySelector('#panel-contracts .input-header h2');
    if (contractHeader) contractHeader.textContent = getStr('contractHeading');
    const contractSub = document.querySelector('#panel-contracts .input-header p');
    if (contractSub) contractSub.textContent = getStr('contractSubheading');
    const contractInput = document.getElementById('contractInput');
    if (contractInput) contractInput.placeholder = getStr('contractPlaceholder');
    const contractBtn = document.getElementById('contractBtn');
    if (contractBtn) {
        const icon = contractBtn.querySelector('i');
        contractBtn.innerHTML = '';
        if (icon) contractBtn.appendChild(icon);
        contractBtn.appendChild(document.createTextNode(' ' + getStr('contractBtn')));
    }

    // Rights panel
    const rightsHeader = document.querySelector('#panel-rights .input-header h2');
    if (rightsHeader) rightsHeader.textContent = getStr('rightsHeading');
    const rightsSub = document.querySelector('#panel-rights .input-header p');
    if (rightsSub) rightsSub.textContent = getStr('rightsSubheading');
    const rightsInput = document.getElementById('rightsInput');
    if (rightsInput) rightsInput.placeholder = getStr('rightsPlaceholder');
    const rightsBtn = document.getElementById('rightsBtn');
    if (rightsBtn) {
        const icon = rightsBtn.querySelector('i');
        rightsBtn.innerHTML = '';
        if (icon) rightsBtn.appendChild(icon);
        rightsBtn.appendChild(document.createTextNode(' ' + getStr('rightsBtn')));
    }

    // Update example/clear button labels in each panel
    document.querySelectorAll('.input-actions').forEach(actions => {
        const panel = actions.closest('.panel');
        if (!panel) return;
        const panelId = panel.id;
        const btns = actions.querySelectorAll('.btn-ghost');
        btns.forEach(btn => {
            const onclick = btn.getAttribute('onclick') || '';
            if (onclick.includes('Example')) {
                const icon = btn.querySelector('i');
                const prefix = panelId === 'panel-scanner' ? 'scan' : panelId === 'panel-contracts' ? 'contract' : 'rights';
                btn.innerHTML = '';
                if (icon) btn.appendChild(icon);
                btn.appendChild(document.createTextNode(' ' + getStr(prefix + 'Example')));
            } else if (onclick.includes('clear') || onclick.includes('Clear')) {
                const icon = btn.querySelector('i');
                const prefix = panelId === 'panel-scanner' ? 'scan' : panelId === 'panel-contracts' ? 'contract' : 'rights';
                btn.innerHTML = '';
                if (icon) btn.appendChild(icon);
                btn.appendChild(document.createTextNode(' ' + getStr(prefix + 'Clear')));
            }
        });
    });

    // Back button
    const backBtn = document.querySelector('.app-nav-left .btn-ghost');
    if (backBtn) {
        const icon = backBtn.querySelector('i');
        backBtn.innerHTML = '';
        if (icon) backBtn.appendChild(icon);
        backBtn.appendChild(document.createTextNode(' ' + getStr('back')));
    }

    lucide.createIcons();
}

// ---- History System (localStorage) ----

const beaconHistory = {
    _key: 'beacon_history',
    _maxEntries: 50,

    _read() {
        try {
            const raw = localStorage.getItem(this._key);
            return raw ? JSON.parse(raw) : [];
        } catch {
            return [];
        }
    },

    _write(entries) {
        try {
            localStorage.setItem(this._key, JSON.stringify(entries));
        } catch { /* quota exceeded -- silently fail */ }
    },

    save(type, input, result) {
        const entries = this._read();
        const entry = {
            id: Date.now().toString(36) + Math.random().toString(36).slice(2, 7),
            type,
            input,
            result,
            timestamp: new Date().toISOString()
        };
        entries.unshift(entry);
        if (entries.length > this._maxEntries) {
            entries.length = this._maxEntries;
        }
        this._write(entries);
        renderHistoryDrawer();
        return entry;
    },

    getAll() {
        return this._read();
    },

    getByType(type) {
        return this._read().filter(e => e.type === type);
    },

    clear() {
        this._write([]);
        renderHistoryDrawer();
    },

    delete(id) {
        const entries = this._read().filter(e => e.id !== id);
        this._write(entries);
        renderHistoryDrawer();
    }
};

// History drawer state
let historyFilterType = 'all';

function toggleHistoryDrawer() {
    const drawer = document.getElementById('historyDrawer');
    const overlay = document.getElementById('historyOverlay');
    const isOpen = drawer.classList.contains('open');
    if (isOpen) {
        drawer.classList.remove('open');
        overlay.classList.remove('open');
    } else {
        renderHistoryDrawer();
        drawer.classList.add('open');
        overlay.classList.add('open');
    }
}

function filterHistory(type) {
    historyFilterType = type;
    document.querySelectorAll('.history-filter').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.filter === type);
    });
    renderHistoryDrawer();
}

function clearAllHistory() {
    if (!confirm('Clear all analysis history? This cannot be undone.')) return;
    beaconHistory.clear();
}

function deleteHistoryEntry(id) {
    beaconHistory.delete(id);
}

function timeAgo(dateStr) {
    const now = Date.now();
    const then = new Date(dateStr).getTime();
    const diff = now - then;
    const seconds = Math.floor(diff / 1000);
    const minutes = Math.floor(seconds / 60);
    const hours = Math.floor(minutes / 60);
    const days = Math.floor(hours / 24);

    if (seconds < 60) return 'just now';
    if (minutes < 60) return minutes + ' min ago';
    if (hours < 24) return hours + 'h ago';
    if (days === 1) return 'yesterday';
    if (days < 7) return days + 'd ago';
    return new Date(dateStr).toLocaleDateString();
}

function getTypeIcon(type) {
    if (type === 'scan') return 'scan-eye';
    if (type === 'contract') return 'file-search';
    if (type === 'rights') return 'scale';
    return 'clock';
}

function getTypeLabel(type) {
    if (type === 'scan') return 'Scam Scan';
    if (type === 'contract') return 'Contract';
    if (type === 'rights') return 'Rights';
    return type;
}

function getTrustScoreBadge(entry) {
    if (entry.type !== 'scan' || !entry.result || entry.result.trust_score === undefined) return '';
    const score = entry.result.trust_score;
    let cls;
    if (score <= 20) cls = 'history-score-dangerous';
    else if (score <= 40) cls = 'history-score-high-risk';
    else if (score <= 60) cls = 'history-score-suspicious';
    else if (score <= 80) cls = 'history-score-uncertain';
    else cls = 'history-score-safe';
    return `<span class="history-score-badge ${cls}">${score}/100</span>`;
}

function renderHistoryDrawer() {
    const container = document.getElementById('historyList');
    const clearBtn = document.getElementById('clearHistoryBtn');
    if (!container) return;
    let entries = historyFilterType === 'all'
        ? beaconHistory.getAll()
        : beaconHistory.getByType(historyFilterType);

    if (entries.length === 0) {
        container.innerHTML = `
            <div class="history-empty">
                <i data-lucide="clock"></i>
                <p>No history yet. Run an analysis to see it here.</p>
            </div>`;
        if (clearBtn) clearBtn.style.display = 'none';
        lucide.createIcons();
        return;
    }

    if (clearBtn) clearBtn.style.display = '';

    container.innerHTML = entries.map(entry => {
        const preview = (entry.input || '').slice(0, 60) + ((entry.input || '').length > 60 ? '...' : '');
        return `
            <div class="history-entry" onclick="loadHistoryEntry('${entry.id}')">
                <div class="history-entry-top">
                    <div class="history-entry-icon">
                        <i data-lucide="${getTypeIcon(entry.type)}"></i>
                    </div>
                    <div class="history-entry-meta">
                        <span class="history-entry-type">${getTypeLabel(entry.type)}</span>
                        <span class="history-entry-time">${timeAgo(entry.timestamp)}</span>
                    </div>
                    <button class="history-entry-delete" onclick="event.stopPropagation(); deleteHistoryEntry('${entry.id}')" title="Delete entry">
                        <i data-lucide="x"></i>
                    </button>
                </div>
                <div class="history-entry-preview">${preview.replace(/</g, '&lt;').replace(/>/g, '&gt;')}</div>
                ${getTrustScoreBadge(entry)}
            </div>`;
    }).join('');
    lucide.createIcons();
}

function loadHistoryEntry(id) {
    const entries = beaconHistory.getAll();
    const entry = entries.find(e => e.id === id);
    if (!entry) return;

    // Close the drawer
    toggleHistoryDrawer();

    // Switch to the correct tab
    const tabMap = { scan: 'scanner', contract: 'contracts', rights: 'rights' };
    const tab = tabMap[entry.type];
    if (tab) switchTab(tab);

    // Fill in input and render the result
    if (entry.type === 'scan') {
        document.getElementById('scanInput').value = entry.input || '';
        if (entry.result) renderScanResult(entry.result, document.getElementById('scanResult'));
    } else if (entry.type === 'contract') {
        document.getElementById('contractInput').value = entry.input || '';
        if (entry.result) renderContractResult(entry.result, document.getElementById('contractResult'));
    } else if (entry.type === 'rights') {
        document.getElementById('rightsInput').value = entry.input || '';
        if (entry.result) renderRightsResult(entry.result, document.getElementById('rightsResult'));
    }
    lucide.createIcons();
}

// ---- Navigation ----

function showApp(tab) {
    document.getElementById('landing').style.display = 'none';
    document.getElementById('app').style.display = 'flex';
    if (tab) switchTab(tab);
    checkHealth();
    lucide.createIcons();
}

function showLanding() {
    document.getElementById('app').style.display = 'none';
    document.getElementById('landing').style.display = 'block';
    lucide.createIcons();
}

function switchTab(tab) {
    document.querySelectorAll('.tab').forEach(t => {
        t.classList.remove('active');
        t.setAttribute('aria-selected', 'false');
    });
    document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
    const activeTab = document.querySelector(`.tab[data-tab="${tab}"]`);
    activeTab.classList.add('active');
    activeTab.setAttribute('aria-selected', 'true');
    document.getElementById(`panel-${tab}`).classList.add('active');
}

// ---- Image Upload (Multimodal) ----

let scanImageB64 = '';

function handleImageUpload(event) {
    const file = event.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = function(e) {
        const dataUrl = e.target.result;
        // Extract base64 portion (remove data:image/...;base64, prefix)
        scanImageB64 = dataUrl.split(',')[1];
        document.getElementById('previewImg').src = dataUrl;
        document.getElementById('imagePreview').style.display = 'flex';
    };
    reader.readAsDataURL(file);
}

function clearImage() {
    scanImageB64 = '';
    document.getElementById('scanImage').value = '';
    document.getElementById('imagePreview').style.display = 'none';
}

// ---- Health Check ----

async function checkHealth() {
    const indicator = document.getElementById('statusIndicator');
    const dot = indicator.querySelector('.status-dot');
    const text = indicator.querySelector('.status-text');

    try {
        const res = await fetch('/health');
        const data = await res.json();
        if (data.model_status.gemma4_ready) {
            dot.className = 'status-dot online';
            text.textContent = 'Gemma 4 Ready';
        } else if (data.model_status.ollama_running) {
            dot.className = 'status-dot';
            text.textContent = 'Pull Gemma 4 model';
        } else {
            dot.className = 'status-dot offline';
            text.textContent = 'Start Ollama';
        }
    } catch {
        dot.className = 'status-dot offline';
        text.textContent = 'Backend offline';
    }
}

// ---- Scam Scanner ----

const SCAN_EXAMPLES = [
    `Subject: URGENT -- Your Apple ID has been compromised

Dear Customer,

We have detected unauthorized access to your Apple ID from an unknown device in Russia. Your account will be permanently locked in 24 hours unless you verify your identity immediately.

Click here to verify your account: http://apple-id-secure-verify.com/login

You must act NOW to prevent:
- Loss of all iCloud data
- Unauthorized purchases on your account
- Identity theft

This is your final warning. Failure to verify within 24 hours will result in permanent account deletion.

Apple Security Team
Case #APL-2024-889271`,

    `Hey! This is Mike from the IRS. We've been trying to reach you about your overdue tax payment of $4,892.31. A warrant has been issued for your arrest if this isn't resolved today. Please call us back immediately at 1-800-555-0147 or purchase $4,892 in Apple gift cards and read us the numbers. This is your final notice before legal action.`,

    `Congratulations! You've been selected as the winner of our $1,000,000 International Lottery! Your ticket number 47-29-81 was drawn on March 15th. To claim your prize, please send a processing fee of $499.99 via Western Union to our claims department. Contact Mr. James Williams at claims@intl-lottery-winners.net with your full name, address, bank details, and a copy of your ID.`
];

function loadScanExample() {
    const example = SCAN_EXAMPLES[Math.floor(Math.random() * SCAN_EXAMPLES.length)];
    document.getElementById('scanInput').value = example;
}

function clearScan() {
    document.getElementById('scanInput').value = '';
    document.getElementById('scanContext').value = '';
    clearImage();
    document.getElementById('scanResult').innerHTML = `
        <div class="result-placeholder">
            <i data-lucide="shield"></i>
            <h3>Results will appear here</h3>
            <p>Paste a message and click "Analyze" to get started.</p>
        </div>`;
    lucide.createIcons();
}

// ---- Quick Scan (pre-screener only, instant, no AI needed) ----

async function runQuickScan() {
    const content = document.getElementById('scanInput').value.trim();
    if (!content) return;
    const btn = document.getElementById('quickScanBtn');
    const resultDiv = document.getElementById('scanResult');
    btn.disabled = true;
    try {
        const res = await fetch('/api/scan/prescreen', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ content })
        });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        const score = data.preliminary_score;
        let colorClass, bgClass;
        if (score <= 20) { colorClass = 'score-dangerous'; bgClass = 'bg-dangerous'; }
        else if (score <= 40) { colorClass = 'score-high-risk'; bgClass = 'bg-high-risk'; }
        else if (score <= 60) { colorClass = 'score-suspicious'; bgClass = 'bg-suspicious'; }
        else if (score <= 80) { colorClass = 'score-uncertain'; bgClass = 'bg-uncertain'; }
        else { colorClass = 'score-safe'; bgClass = 'bg-safe'; }
        const riskLabel = score <= 20 ? 'DANGEROUS' : score <= 40 ? 'HIGH RISK' : score <= 60 ? 'SUSPICIOUS' : score <= 80 ? 'UNCERTAIN' : 'LIKELY SAFE';
        resultDiv.innerHTML = `
            <div class="trust-score-display ${bgClass}" style="margin-bottom:1rem;">
                <div class="trust-score-value ${colorClass}" style="font-size:3rem;">${score}</div>
                <div class="trust-score-label ${colorClass}">${riskLabel}</div>
                <div style="font-size:0.8rem;color:var(--text-muted);margin-top:0.5rem;">Quick Scan (rule-based, instant)</div>
            </div>
            ${data.flag_count > 0 ? `
            <div class="result-section">
                <div class="result-section-title">Red Flags Found (${data.flag_count})</div>
                <ul class="red-flags-list">
                    ${data.instant_flags.map(f => `<li class="red-flag-item"><svg class="red-flag-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>${f}</li>`).join('')}
                </ul>
            </div>` : `
            <div class="result-section">
                <div class="result-card" style="border-left:3px solid var(--success);"><div class="result-text">No immediate red flags detected. For thorough AI analysis, use Deep Scan.</div></div>
            </div>`}
            <div class="result-section" style="margin-top:1rem;">
                <div class="result-card" style="background:var(--info-bg);border:1px solid var(--info-border);">
                    <div class="result-text" style="font-size:0.85rem;color:#1e40af;">Quick Scan uses pattern matching and runs instantly without AI. For comprehensive analysis with explanations, use <strong>Deep Scan</strong>.</div>
                </div>
            </div>`;
        lucide.createIcons();
        if (typeof beaconHistory !== 'undefined') {
            beaconHistory.save('scan', content, { trust_score: score, risk_level: riskLabel, scam_type: 'Quick Scan', red_flags: data.instant_flags, explanation: 'Quick Scan (rule-based)', recommended_actions: [], safe_alternatives: '' });
        }
    } catch (err) {
        resultDiv.innerHTML = `<div class="result-placeholder"><h3>Quick scan failed</h3><p>${err.message}</p></div>`;
        lucide.createIcons();
    } finally { btn.disabled = false; }
}

async function runScan() {
    const content = document.getElementById('scanInput').value.trim();
    if (!content && !scanImageB64) return;

    const btn = document.getElementById('scanBtn');
    const resultDiv = document.getElementById('scanResult');

    btn.disabled = true;

    // Stage 1: Instant pre-screening (rule-based, <1ms)
    if (content && !scanImageB64) {
        try {
            const preRes = await fetch('/api/scan/prescreen', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ content })
            });
            if (preRes.ok) {
                const preData = await preRes.json();
                if (preData.flag_count > 0) {
                    resultDiv.innerHTML = `
                        <div style="margin-bottom:1rem;">
                            <div class="result-section-title">Instant Pre-Scan (${preData.flag_count} flags found)</div>
                            ${preData.instant_flags.map(f => `
                                <div class="red-flag-item" style="margin-bottom:0.25rem;">
                                    <svg class="red-flag-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                        <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
                                        <line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/>
                                    </svg>
                                    ${f}
                                </div>
                            `).join('')}
                            <div style="font-size:0.8rem;color:var(--text-muted);margin-top:0.5rem;">Preliminary score: ${preData.preliminary_score}/100</div>
                        </div>
                        <div class="loading-pulse">
                            <div class="loading-spinner"></div>
                            <div class="loading-text">${getStr('loadingDeepAnalysis')}</div>
                        </div>`;
                } else {
                    resultDiv.innerHTML = `
                        <div class="loading-pulse">
                            <div class="loading-spinner"></div>
                            <div class="loading-text">${getStr('loadingNoFlags')}</div>
                        </div>`;
                }
            }
        } catch { /* pre-screen is best-effort */ }
    } else {
        const analyzeMode = scanImageB64 ? getStr('loadingAnalyzeScreenshot') : getStr('loadingAnalyzeMessage');
        resultDiv.innerHTML = `
            <div class="loading-pulse">
                <div class="loading-spinner"></div>
                <div class="loading-text">${analyzeMode}</div>
            </div>`;
    }

    // Stage 2: Full Gemma 4 LLM analysis
    try {
        const res = await fetch('/api/scan', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                content,
                image: scanImageB64,
                context: document.getElementById('scanContext').value.trim(),
                language: currentLanguage
            })
        });

        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        renderScanResult(data, resultDiv);

        // Save to local history
        beaconHistory.save('scan', content || '[screenshot]', data);

        // Trigger trusted contact alert if dangerous
        if (data.trust_score <= 20) {
            triggerDangerAlert(data);
        }
    } catch (err) {
        resultDiv.innerHTML = `
            <div class="result-placeholder">
                <i data-lucide="alert-triangle"></i>
                <h3>${getStr('analysisFailed')}</h3>
                <p>${err.message}. Make sure Ollama is running with Gemma 4.</p>
            </div>`;
    } finally {
        btn.disabled = false;
        lucide.createIcons();
    }
}

function renderScanResult(data, container) {
    const score = data.trust_score;
    const circumference = 2 * Math.PI * 54;
    const offset = circumference - (score / 100) * circumference;

    let colorClass, bgClass, strokeColor;
    if (score <= 20) { colorClass = 'score-dangerous'; bgClass = 'bg-dangerous'; strokeColor = '#ef4444'; }
    else if (score <= 40) { colorClass = 'score-high-risk'; bgClass = 'bg-high-risk'; strokeColor = '#dc2626'; }
    else if (score <= 60) { colorClass = 'score-suspicious'; bgClass = 'bg-suspicious'; strokeColor = '#f59e0b'; }
    else if (score <= 80) { colorClass = 'score-uncertain'; bgClass = 'bg-uncertain'; strokeColor = '#6b7280'; }
    else { colorClass = 'score-safe'; bgClass = 'bg-safe'; strokeColor = '#10b981'; }

    const riskLabel = data.risk_level.replace(/_/g, ' ');

    container.innerHTML = `
        <div class="trust-score-display ${bgClass}">
            <div class="trust-score-ring">
                <svg viewBox="0 0 120 120">
                    <circle class="bg-ring" cx="60" cy="60" r="54"/>
                    <circle class="score-ring" cx="60" cy="60" r="54"
                        stroke="${strokeColor}"
                        stroke-dasharray="${circumference}"
                        stroke-dashoffset="${offset}"/>
                </svg>
                <div class="trust-score-value ${colorClass}">${score}</div>
            </div>
            <div class="trust-score-label ${colorClass}">${riskLabel}</div>
            ${data.scam_type !== 'Unknown' ? `<div style="font-size:0.85rem;color:var(--text-secondary);margin-top:0.5rem;">Type: ${data.scam_type}</div>` : ''}
        </div>

        ${data.explanation ? `
        <div class="result-section">
            <div class="result-section-title">What This Means</div>
            <div class="result-card">
                <div class="result-text">${data.explanation}</div>
            </div>
        </div>` : ''}

        ${data.red_flags && data.red_flags.length > 0 ? `
        <div class="result-section">
            <div class="result-section-title">Red Flags Found (${data.red_flags.length})</div>
            <ul class="red-flags-list">
                ${data.red_flags.map(flag => `
                    <li class="red-flag-item">
                        <svg class="red-flag-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
                            <line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/>
                        </svg>
                        ${flag}
                    </li>
                `).join('')}
            </ul>
        </div>` : ''}

        ${data.recommended_actions && data.recommended_actions.length > 0 ? `
        <div class="result-section">
            <div class="result-section-title">What You Should Do</div>
            <ul class="actions-list">
                ${data.recommended_actions.map(action => `
                    <li class="action-item">
                        <svg class="action-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <polyline points="20 6 9 17 4 12"/>
                        </svg>
                        ${action}
                    </li>
                `).join('')}
            </ul>
        </div>` : ''}

        ${data.safe_alternatives ? `
        <div class="result-section">
            <div class="result-section-title">Safe Alternative</div>
            <div class="result-card" style="border-left: 3px solid var(--success);">
                <div class="result-text">${data.safe_alternatives}</div>
            </div>
        </div>` : ''}

        <div class="export-bar">
            <button onclick="printResults('scan')" class="btn btn-ghost btn-sm"><i data-lucide="printer"></i> Print</button>
            <button onclick="copyResults('scan')" class="btn btn-ghost btn-sm"><i data-lucide="copy"></i> Copy</button>
        </div>
    `;
}

// ---- Contract Reader ----

const CONTRACT_EXAMPLE = `RESIDENTIAL LEASE AGREEMENT

1. RENT: Tenant agrees to pay $1,850 per month. Late fees of $150 will be assessed for payments received after the 3rd of each month. Additional $50 per day late fee after the 5th.

2. SECURITY DEPOSIT: Tenant shall pay a security deposit of $3,700 (2x rent). Landlord may deduct for any damage, including normal wear and tear, cleaning fees, and repainting costs regardless of condition.

3. MAINTENANCE: Tenant is responsible for ALL maintenance and repairs under $500, including plumbing, electrical, and appliance repairs. Tenant must use landlord's preferred contractor at tenant's expense.

4. ENTRY: Landlord reserves the right to enter the premises at any time without notice for inspections, repairs, or showing the unit to prospective tenants.

5. LEASE TERMINATION: Early termination requires 90 days written notice AND payment of 3 months rent as a penalty. Landlord may terminate lease with 15 days notice for any reason.

6. ARBITRATION: All disputes must be resolved through binding arbitration using an arbitrator selected by the landlord. Tenant waives all rights to jury trial or class action.

7. UTILITIES: Tenant is responsible for all utilities including water, sewer, and trash, which will be billed through landlord's billing system at a $35/month processing fee.

8. PET POLICY: Pets allowed with $500 non-refundable pet deposit plus $75/month pet rent per animal. Landlord defines "pet" to include emotional support animals.

9. RENEWAL: Lease automatically renews for 12 months unless tenant provides 60 days written notice. Rent increases of up to 15% may apply upon renewal.`;

function loadContractExample() {
    document.getElementById('contractInput').value = CONTRACT_EXAMPLE;
    document.getElementById('contractType').value = 'lease';
}

async function handleContractFile(event) {
    const file = event.target.files[0];
    if (!file) return;
    const nameEl = document.getElementById('contractFileName');
    nameEl.textContent = file.name;

    if (file.name.endsWith('.txt') || file.name.endsWith('.rtf')) {
        document.getElementById('contractInput').value = await file.text();
    } else if (file.name.endsWith('.pdf')) {
        try {
            if (!window.pdfjsLib) {
                await new Promise((resolve, reject) => {
                    const s = document.createElement('script');
                    s.src = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/4.4.168/pdf.min.mjs';
                    s.type = 'module';
                    s.onload = resolve;
                    s.onerror = reject;
                    document.head.appendChild(s);
                });
                await new Promise(r => setTimeout(r, 1500));
            }
            if (window.pdfjsLib) {
                const pdf = await window.pdfjsLib.getDocument({ data: await file.arrayBuffer() }).promise;
                let text = '';
                for (let i = 1; i <= pdf.numPages; i++) {
                    const page = await pdf.getPage(i);
                    const content = await page.getTextContent();
                    text += content.items.map(item => item.str).join(' ') + '\n\n';
                }
                document.getElementById('contractInput').value = text.trim();
            } else {
                nameEl.textContent = file.name + ' -- PDF reader unavailable, paste text manually';
            }
        } catch (err) {
            nameEl.textContent = file.name + ' -- could not read PDF, paste text manually';
        }
    } else {
        nameEl.textContent = file.name + ' -- for Word docs, copy and paste the text instead';
    }
}

function clearContract() {
    document.getElementById('contractInput').value = '';
    document.getElementById('contractType').value = '';
    if (document.getElementById('contractFile')) document.getElementById('contractFile').value = '';
    if (document.getElementById('contractFileName')) document.getElementById('contractFileName').textContent = '';
    document.getElementById('contractResult').innerHTML = `
        <div class="result-placeholder">
            <i data-lucide="file-search"></i>
            <h3>Results will appear here</h3>
            <p>Paste a document and click "Analyze" to get started.</p>
        </div>`;
    lucide.createIcons();
}

async function runContract() {
    const content = document.getElementById('contractInput').value.trim();
    if (!content) return;

    const btn = document.getElementById('contractBtn');
    const resultDiv = document.getElementById('contractResult');

    btn.disabled = true;
    resultDiv.innerHTML = `
        <div class="loading-pulse">
            <div class="loading-spinner"></div>
            <div class="loading-text">${getStr('loadingDocument')}</div>
        </div>`;

    try {
        const res = await fetch('/api/contract', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                content,
                document_type: document.getElementById('contractType').value,
                language: currentLanguage
            })
        });

        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        renderContractResult(data, resultDiv);

        // Save to local history
        beaconHistory.save('contract', content, data);
    } catch (err) {
        resultDiv.innerHTML = `
            <div class="result-placeholder">
                <i data-lucide="alert-triangle"></i>
                <h3>${getStr('analysisFailed')}</h3>
                <p>${err.message}. Make sure Ollama is running with Gemma 4.</p>
            </div>`;
    } finally {
        btn.disabled = false;
        lucide.createIcons();
    }
}

function renderContractResult(data, container) {
    container.innerHTML = `
        ${data.document_type ? `<div style="font-size:0.8rem;font-weight:600;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.05em;margin-bottom:0.5rem;">${data.document_type}</div>` : ''}

        ${data.summary ? `
        <div class="result-section">
            <div class="result-section-title">Summary</div>
            <div class="result-card">
                <div class="result-text">${data.summary}</div>
            </div>
        </div>` : ''}

        ${data.flagged_items && data.flagged_items.length > 0 ? `
        <div class="result-section">
            <div class="result-section-title">Flagged Concerns (${data.flagged_items.length})</div>
            ${data.flagged_items.map(item => {
                const sev = (item.severity || 'INFO').toUpperCase();
                const cls = sev === 'CRITICAL' ? 'flagged-critical' : sev === 'WARNING' ? 'flagged-warning' : 'flagged-info';
                return `
                <div class="flagged-item ${cls}">
                    <div class="flagged-severity" style="color: ${sev === 'CRITICAL' ? 'var(--danger)' : sev === 'WARNING' ? 'var(--warning)' : 'var(--info)'};">${sev}</div>
                    ${item.clause ? `<div class="flagged-clause">"${item.clause}"</div>` : ''}
                    <div class="flagged-concern">${item.concern || ''}</div>
                    ${item.typical_standard ? `<div style="font-size:0.8rem;color:var(--text-muted);margin-top:0.5rem;">Fair standard: ${item.typical_standard}</div>` : ''}
                </div>`;
            }).join('')}
        </div>` : ''}

        ${data.hidden_costs && data.hidden_costs.length > 0 ? `
        <div class="result-section">
            <div class="result-section-title">Hidden Costs</div>
            ${data.hidden_costs.map(cost => `
                <div class="flagged-item flagged-warning">
                    <div class="flagged-concern">${cost.cost}</div>
                    ${cost.estimated_impact ? `<div style="font-size:0.85rem;color:var(--warning);font-weight:600;margin-top:0.25rem;">Estimated impact: ${cost.estimated_impact}</div>` : ''}
                </div>
            `).join('')}
        </div>` : ''}

        ${data.key_terms && data.key_terms.length > 0 ? `
        <div class="result-section">
            <div class="result-section-title">Key Terms Explained</div>
            ${data.key_terms.map(term => `
                <div class="right-item">
                    <div class="right-name">${term.term}</div>
                    <div class="right-explanation">${term.plain_english || ''}</div>
                    ${term.impact ? `<div style="font-size:0.8rem;color:var(--text-muted);margin-top:0.25rem;">Impact: ${term.impact}</div>` : ''}
                </div>
            `).join('')}
        </div>` : ''}

        ${data.overall_assessment ? `
        <div class="result-section">
            <div class="result-section-title">Overall Assessment</div>
            <div class="result-card" style="border-left: 3px solid var(--beacon-primary);">
                <div class="result-text">${data.overall_assessment}</div>
            </div>
        </div>` : ''}

        ${data.questions_to_ask && data.questions_to_ask.length > 0 ? `
        <div class="result-section">
            <div class="result-section-title">Questions to Ask Before Signing</div>
            <ul class="actions-list">
                ${data.questions_to_ask.map(q => `
                    <li class="action-item">
                        <svg class="action-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/>
                        </svg>
                        ${q}
                    </li>
                `).join('')}
            </ul>
        </div>` : ''}

        <div class="export-bar">
            <button onclick="printResults('contract')" class="btn btn-ghost btn-sm"><i data-lucide="printer"></i> Print</button>
            <button onclick="copyResults('contract')" class="btn btn-ghost btn-sm"><i data-lucide="copy"></i> Copy</button>
        </div>
    `;
}

// ---- Rights Navigator ----

const RIGHTS_EXAMPLES = [
    `My landlord is refusing to return my security deposit. I lived in the apartment for 2 years, left it clean, and gave 30 days notice. They say they're keeping it for "normal wear and tear" and repainting. I have move-in and move-out photos showing the place was in good condition.`,

    `I was fired from my job after telling HR about safety violations in the warehouse. My boss said it was for "poor performance" but I have good reviews from the last 3 years. I think it was retaliation. I'm the only person who reported the violations.`,

    `A debt collector keeps calling me about a medical bill from 3 years ago. They call multiple times a day, including at 6am and after 10pm. They threatened to garnish my wages and told my neighbor about the debt when they couldn't reach me. The original bill was $2,400 but they say I now owe $4,100 with interest.`
];

function loadRightsExample() {
    const example = RIGHTS_EXAMPLES[Math.floor(Math.random() * RIGHTS_EXAMPLES.length)];
    document.getElementById('rightsInput').value = example;

    // Auto-select category based on content
    const text = example.toLowerCase();
    if (text.includes('landlord') || text.includes('tenant')) {
        document.getElementById('rightsCategory').value = 'tenant';
    } else if (text.includes('fired') || text.includes('employer') || text.includes('job')) {
        document.getElementById('rightsCategory').value = 'employee';
    } else if (text.includes('debt') || text.includes('collector')) {
        document.getElementById('rightsCategory').value = 'debt';
    }
}

function clearRights() {
    document.getElementById('rightsInput').value = '';
    document.getElementById('rightsCategory').value = '';
    document.getElementById('rightsResult').innerHTML = `
        <div class="result-placeholder">
            <i data-lucide="scale"></i>
            <h3>Results will appear here</h3>
            <p>Describe your situation and click "Find My Rights" to get started.</p>
        </div>`;
    lucide.createIcons();
}

async function runRights() {
    const situation = document.getElementById('rightsInput').value.trim();
    if (!situation) return;

    const btn = document.getElementById('rightsBtn');
    const resultDiv = document.getElementById('rightsResult');

    btn.disabled = true;
    resultDiv.innerHTML = `
        <div class="loading-pulse">
            <div class="loading-spinner"></div>
            <div class="loading-text">${getStr('loadingRights')}</div>
        </div>`;

    try {
        const res = await fetch('/api/rights', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                situation,
                category: document.getElementById('rightsCategory').value,
                language: currentLanguage
            })
        });

        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        renderRightsResult(data, resultDiv);

        // Save to local history
        beaconHistory.save('rights', situation, data);
    } catch (err) {
        resultDiv.innerHTML = `
            <div class="result-placeholder">
                <i data-lucide="alert-triangle"></i>
                <h3>${getStr('analysisFailed')}</h3>
                <p>${err.message}. Make sure Ollama is running with Gemma 4.</p>
            </div>`;
    } finally {
        btn.disabled = false;
        lucide.createIcons();
    }
}

function renderRightsResult(data, container) {
    container.innerHTML = `
        ${data.situation_summary ? `
        <div class="result-section">
            <div class="result-section-title">Your Situation</div>
            <div class="result-card">
                <div class="result-text">${data.situation_summary}</div>
            </div>
        </div>` : ''}

        ${data.applicable_rights && data.applicable_rights.length > 0 ? `
        <div class="result-section">
            <div class="result-section-title">Your Rights</div>
            ${data.applicable_rights.map(right => `
                <div class="right-item">
                    <div class="right-name">${right.right}</div>
                    <div class="right-explanation">${right.explanation}</div>
                    ${right.legal_basis ? `<div class="right-basis">${right.legal_basis}</div>` : ''}
                </div>
            `).join('')}
        </div>` : ''}

        ${data.immediate_actions && data.immediate_actions.length > 0 ? `
        <div class="result-section">
            <div class="result-section-title">What to Do Next</div>
            <ul class="actions-list">
                ${data.immediate_actions.map(action => `
                    <li class="action-item">
                        <svg class="action-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <polyline points="20 6 9 17 4 12"/>
                        </svg>
                        <div>
                            <strong>${action.action}</strong>
                            ${action.why ? `<div style="font-size:0.8rem;color:var(--text-muted);margin-top:2px;">${action.why}</div>` : ''}
                        </div>
                    </li>
                `).join('')}
            </ul>
        </div>` : ''}

        ${data.documentation_needed && data.documentation_needed.length > 0 ? `
        <div class="result-section">
            <div class="result-section-title">Evidence to Gather</div>
            <div class="result-card">
                <ul style="list-style:disc;padding-left:1.25rem;display:flex;flex-direction:column;gap:0.25rem;">
                    ${data.documentation_needed.map(doc => `<li style="font-size:0.9rem;">${doc}</li>`).join('')}
                </ul>
            </div>
        </div>` : ''}

        ${data.free_resources && data.free_resources.length > 0 ? `
        <div class="result-section">
            <div class="result-section-title">Free Help Available</div>
            ${data.free_resources.map(resource => `
                <div class="resource-item">
                    <div class="resource-name">${resource.name}</div>
                    <div class="resource-desc">${resource.what_they_do}</div>
                    ${resource.how_to_reach ? `<div style="font-size:0.8rem;margin-top:0.25rem;font-family:var(--font-mono);">${resource.how_to_reach}</div>` : ''}
                </div>
            `).join('')}
        </div>` : ''}

        ${data.warnings && data.warnings.length > 0 ? `
        <div class="result-section">
            <div class="result-section-title">Things to Avoid</div>
            ${data.warnings.map(warning => `
                <div class="flagged-item flagged-warning">
                    <div class="flagged-concern">${warning}</div>
                </div>
            `).join('')}
        </div>` : ''}

        ${data.timeline ? `
        <div class="result-section">
            <div class="result-section-title">Important Deadlines</div>
            <div class="result-card" style="border-left: 3px solid var(--warning);">
                <div class="result-text">${data.timeline}</div>
            </div>
        </div>` : ''}

        <div class="result-section" style="margin-top:var(--space-xl);padding-top:var(--space-md);border-top:1px solid var(--border);">
            <div style="font-size:0.8rem;color:var(--text-muted);font-style:italic;">
                This is educational information, not legal advice. For your specific situation, consider consulting with a legal professional through the free resources listed above.
            </div>
        </div>

        <div class="export-bar">
            <button onclick="printResults('rights')" class="btn btn-ghost btn-sm"><i data-lucide="printer"></i> Print</button>
            <button onclick="copyResults('rights')" class="btn btn-ghost btn-sm"><i data-lucide="copy"></i> Copy</button>
        </div>
    `;
}

// ---- Export / Print / Copy ----

function _getLastResultData(type) {
    const entries = beaconHistory.getAll();
    return entries.find(e => e.type === type);
}

function exportResults(type) {
    const entry = _getLastResultData(type);
    if (!entry || !entry.result) return '';

    const data = entry.result;
    const timestamp = new Date(entry.timestamp).toLocaleString();
    let typeLabel, body;

    if (type === 'scan') {
        typeLabel = 'Scam Scan';
        const riskLabel = (data.risk_level || '').replace(/_/g, ' ');
        body = `
            <h2 style="margin:0 0 4px;">Trust Score: ${data.trust_score}/100</h2>
            <p style="margin:0 0 16px;color:#666;text-transform:uppercase;font-weight:700;letter-spacing:0.05em;">${riskLabel}</p>
            ${data.scam_type && data.scam_type !== 'Unknown' ? `<p style="margin:0 0 16px;color:#555;">Scam Type: ${data.scam_type}</p>` : ''}
            ${data.explanation ? `<h3 style="margin:20px 0 6px;font-size:14px;text-transform:uppercase;color:#888;">What This Means</h3><p style="margin:0 0 16px;line-height:1.7;">${data.explanation}</p>` : ''}
            ${data.red_flags && data.red_flags.length > 0 ? `<h3 style="margin:20px 0 6px;font-size:14px;text-transform:uppercase;color:#888;">Red Flags (${data.red_flags.length})</h3><ul style="margin:0 0 16px;padding-left:20px;">${data.red_flags.map(f => `<li style="margin-bottom:6px;color:#991b1b;">${f}</li>`).join('')}</ul>` : ''}
            ${data.recommended_actions && data.recommended_actions.length > 0 ? `<h3 style="margin:20px 0 6px;font-size:14px;text-transform:uppercase;color:#888;">Recommended Actions</h3><ul style="margin:0 0 16px;padding-left:20px;">${data.recommended_actions.map(a => `<li style="margin-bottom:6px;">${a}</li>`).join('')}</ul>` : ''}
            ${data.safe_alternatives ? `<h3 style="margin:20px 0 6px;font-size:14px;text-transform:uppercase;color:#888;">Safe Alternative</h3><p style="margin:0 0 16px;line-height:1.7;">${data.safe_alternatives}</p>` : ''}
        `;
    } else if (type === 'contract') {
        typeLabel = 'Contract Analysis';
        body = `
            ${data.document_type ? `<p style="margin:0 0 16px;color:#666;text-transform:uppercase;font-weight:700;letter-spacing:0.05em;">${data.document_type}</p>` : ''}
            ${data.summary ? `<h3 style="margin:20px 0 6px;font-size:14px;text-transform:uppercase;color:#888;">Summary</h3><p style="margin:0 0 16px;line-height:1.7;">${data.summary}</p>` : ''}
            ${data.flagged_items && data.flagged_items.length > 0 ? `<h3 style="margin:20px 0 6px;font-size:14px;text-transform:uppercase;color:#888;">Flagged Concerns (${data.flagged_items.length})</h3>${data.flagged_items.map(item => {
                const sev = (item.severity || 'INFO').toUpperCase();
                return `<div style="margin-bottom:10px;padding:10px;border-left:4px solid ${sev === 'CRITICAL' ? '#ef4444' : sev === 'WARNING' ? '#f59e0b' : '#3b82f6'};background:${sev === 'CRITICAL' ? '#fef2f2' : sev === 'WARNING' ? '#fffbeb' : '#eff6ff'};"><strong style="font-size:12px;text-transform:uppercase;color:${sev === 'CRITICAL' ? '#ef4444' : sev === 'WARNING' ? '#f59e0b' : '#3b82f6'};">${sev}</strong>${item.clause ? `<div style="font-style:italic;color:#555;margin:4px 0;">"${item.clause}"</div>` : ''}<div>${item.concern || ''}</div>${item.typical_standard ? `<div style="font-size:13px;color:#888;margin-top:4px;">Fair standard: ${item.typical_standard}</div>` : ''}</div>`;
            }).join('')}` : ''}
            ${data.hidden_costs && data.hidden_costs.length > 0 ? `<h3 style="margin:20px 0 6px;font-size:14px;text-transform:uppercase;color:#888;">Hidden Costs</h3>${data.hidden_costs.map(cost => `<div style="margin-bottom:10px;padding:10px;border-left:4px solid #f59e0b;background:#fffbeb;"><div>${cost.cost}</div>${cost.estimated_impact ? `<div style="font-size:13px;color:#f59e0b;font-weight:600;margin-top:4px;">Estimated impact: ${cost.estimated_impact}</div>` : ''}</div>`).join('')}` : ''}
            ${data.key_terms && data.key_terms.length > 0 ? `<h3 style="margin:20px 0 6px;font-size:14px;text-transform:uppercase;color:#888;">Key Terms</h3>${data.key_terms.map(term => `<div style="margin-bottom:10px;padding:10px;border:1px solid #e2e8f0;border-radius:6px;"><strong>${term.term}</strong><div style="color:#555;margin-top:4px;">${term.plain_english || ''}</div>${term.impact ? `<div style="font-size:13px;color:#888;margin-top:4px;">Impact: ${term.impact}</div>` : ''}</div>`).join('')}` : ''}
            ${data.overall_assessment ? `<h3 style="margin:20px 0 6px;font-size:14px;text-transform:uppercase;color:#888;">Overall Assessment</h3><p style="margin:0 0 16px;line-height:1.7;">${data.overall_assessment}</p>` : ''}
            ${data.questions_to_ask && data.questions_to_ask.length > 0 ? `<h3 style="margin:20px 0 6px;font-size:14px;text-transform:uppercase;color:#888;">Questions to Ask</h3><ul style="margin:0 0 16px;padding-left:20px;">${data.questions_to_ask.map(q => `<li style="margin-bottom:6px;">${q}</li>`).join('')}</ul>` : ''}
        `;
    } else if (type === 'rights') {
        typeLabel = 'Rights Analysis';
        body = `
            ${data.situation_summary ? `<h3 style="margin:20px 0 6px;font-size:14px;text-transform:uppercase;color:#888;">Your Situation</h3><p style="margin:0 0 16px;line-height:1.7;">${data.situation_summary}</p>` : ''}
            ${data.applicable_rights && data.applicable_rights.length > 0 ? `<h3 style="margin:20px 0 6px;font-size:14px;text-transform:uppercase;color:#888;">Your Rights</h3>${data.applicable_rights.map(right => `<div style="margin-bottom:10px;padding:10px;border:1px solid #e2e8f0;border-radius:6px;"><strong>${right.right}</strong><div style="color:#555;margin-top:4px;">${right.explanation}</div>${right.legal_basis ? `<div style="font-size:12px;color:#888;margin-top:4px;font-family:monospace;">${right.legal_basis}</div>` : ''}</div>`).join('')}` : ''}
            ${data.immediate_actions && data.immediate_actions.length > 0 ? `<h3 style="margin:20px 0 6px;font-size:14px;text-transform:uppercase;color:#888;">What to Do Next</h3><ul style="margin:0 0 16px;padding-left:20px;">${data.immediate_actions.map(a => `<li style="margin-bottom:6px;"><strong>${a.action}</strong>${a.why ? ' -- ' + a.why : ''}</li>`).join('')}</ul>` : ''}
            ${data.documentation_needed && data.documentation_needed.length > 0 ? `<h3 style="margin:20px 0 6px;font-size:14px;text-transform:uppercase;color:#888;">Evidence to Gather</h3><ul style="margin:0 0 16px;padding-left:20px;">${data.documentation_needed.map(d => `<li style="margin-bottom:6px;">${d}</li>`).join('')}</ul>` : ''}
            ${data.free_resources && data.free_resources.length > 0 ? `<h3 style="margin:20px 0 6px;font-size:14px;text-transform:uppercase;color:#888;">Free Resources</h3>${data.free_resources.map(r => `<div style="margin-bottom:10px;padding:10px;background:#ecfdf5;border:1px solid #a7f3d0;border-radius:6px;"><strong style="color:#065f46;">${r.name}</strong><div style="color:#047857;font-size:14px;margin-top:4px;">${r.what_they_do}</div>${r.how_to_reach ? `<div style="font-size:12px;margin-top:4px;font-family:monospace;">${r.how_to_reach}</div>` : ''}</div>`).join('')}` : ''}
            ${data.warnings && data.warnings.length > 0 ? `<h3 style="margin:20px 0 6px;font-size:14px;text-transform:uppercase;color:#888;">Things to Avoid</h3><ul style="margin:0 0 16px;padding-left:20px;color:#991b1b;">${data.warnings.map(w => `<li style="margin-bottom:6px;">${w}</li>`).join('')}</ul>` : ''}
            ${data.timeline ? `<h3 style="margin:20px 0 6px;font-size:14px;text-transform:uppercase;color:#888;">Important Deadlines</h3><p style="margin:0 0 16px;line-height:1.7;">${data.timeline}</p>` : ''}
            <p style="font-size:13px;color:#888;font-style:italic;margin-top:20px;padding-top:12px;border-top:1px solid #e2e8f0;">This is educational information, not legal advice. For your specific situation, consider consulting with a legal professional.</p>
        `;
    } else {
        return '';
    }

    return `<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Beacon - ${typeLabel} Report</title>
<style>body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;max-width:700px;margin:0 auto;padding:40px 24px;color:#0f172a;line-height:1.6;}h1{font-size:22px;margin:0;}h2{font-size:20px;}h3{font-size:14px;}@media print{body{padding:20px;}}</style>
</head><body>
<div style="margin-bottom:24px;padding-bottom:16px;border-bottom:2px solid #3b82f6;">
    <h1 style="color:#3b82f6;margin:0;">Beacon</h1>
    <p style="margin:4px 0 0;color:#888;font-size:14px;">Privacy-First AI Protection</p>
</div>
<div style="margin-bottom:24px;">
    <p style="margin:0;font-size:18px;font-weight:700;">${typeLabel} Report</p>
    <p style="margin:4px 0 0;color:#888;font-size:13px;">${timestamp}</p>
</div>
${body}
<div style="margin-top:32px;padding-top:16px;border-top:1px solid #e2e8f0;font-size:12px;color:#888;">
    <p style="margin:0 0 4px;">Generated by Beacon -- Privacy-First AI Protection. Powered by Gemma 4. https://github.com/credwine/beacon</p>
    <p style="margin:0;">This analysis was performed locally on your device. No data was transmitted.</p>
</div>
</body></html>`;
}

function printResults(type) {
    const html = exportResults(type);
    if (!html) return;

    const printWindow = window.open('', '_blank');
    if (!printWindow) return;

    printWindow.document.write(html);
    printWindow.document.close();

    printWindow.onload = function () {
        printWindow.focus();
        printWindow.print();
    };
}

function copyResults(type) {
    const entry = _getLastResultData(type);
    if (!entry || !entry.result) return;

    const data = entry.result;
    const timestamp = new Date(entry.timestamp).toLocaleString();
    let lines = [];

    lines.push('BEACON ANALYSIS REPORT');
    lines.push('='.repeat(40));

    if (type === 'scan') {
        lines.push(`Type: Scam Scan`);
        lines.push(`Date: ${timestamp}`);
        lines.push('');
        lines.push(`Trust Score: ${data.trust_score}/100`);
        lines.push(`Risk Level: ${(data.risk_level || '').replace(/_/g, ' ')}`);
        if (data.scam_type && data.scam_type !== 'Unknown') lines.push(`Scam Type: ${data.scam_type}`);
        if (data.explanation) {
            lines.push('');
            lines.push('--- What This Means ---');
            lines.push(data.explanation);
        }
        if (data.red_flags && data.red_flags.length > 0) {
            lines.push('');
            lines.push(`--- Red Flags (${data.red_flags.length}) ---`);
            data.red_flags.forEach(f => lines.push(`  * ${f}`));
        }
        if (data.recommended_actions && data.recommended_actions.length > 0) {
            lines.push('');
            lines.push('--- Recommended Actions ---');
            data.recommended_actions.forEach(a => lines.push(`  * ${a}`));
        }
        if (data.safe_alternatives) {
            lines.push('');
            lines.push('--- Safe Alternative ---');
            lines.push(data.safe_alternatives);
        }
    } else if (type === 'contract') {
        lines.push(`Type: Contract Analysis`);
        lines.push(`Date: ${timestamp}`);
        if (data.document_type) lines.push(`Document Type: ${data.document_type}`);
        if (data.summary) {
            lines.push('');
            lines.push('--- Summary ---');
            lines.push(data.summary);
        }
        if (data.flagged_items && data.flagged_items.length > 0) {
            lines.push('');
            lines.push(`--- Flagged Concerns (${data.flagged_items.length}) ---`);
            data.flagged_items.forEach(item => {
                const sev = (item.severity || 'INFO').toUpperCase();
                lines.push(`  [${sev}] ${item.concern || ''}`);
                if (item.clause) lines.push(`    Clause: "${item.clause}"`);
                if (item.typical_standard) lines.push(`    Fair standard: ${item.typical_standard}`);
            });
        }
        if (data.hidden_costs && data.hidden_costs.length > 0) {
            lines.push('');
            lines.push('--- Hidden Costs ---');
            data.hidden_costs.forEach(cost => {
                lines.push(`  * ${cost.cost}`);
                if (cost.estimated_impact) lines.push(`    Estimated impact: ${cost.estimated_impact}`);
            });
        }
        if (data.key_terms && data.key_terms.length > 0) {
            lines.push('');
            lines.push('--- Key Terms ---');
            data.key_terms.forEach(term => {
                lines.push(`  ${term.term}: ${term.plain_english || ''}`);
                if (term.impact) lines.push(`    Impact: ${term.impact}`);
            });
        }
        if (data.overall_assessment) {
            lines.push('');
            lines.push('--- Overall Assessment ---');
            lines.push(data.overall_assessment);
        }
        if (data.questions_to_ask && data.questions_to_ask.length > 0) {
            lines.push('');
            lines.push('--- Questions to Ask ---');
            data.questions_to_ask.forEach(q => lines.push(`  * ${q}`));
        }
    } else if (type === 'rights') {
        lines.push(`Type: Rights Analysis`);
        lines.push(`Date: ${timestamp}`);
        if (data.situation_summary) {
            lines.push('');
            lines.push('--- Your Situation ---');
            lines.push(data.situation_summary);
        }
        if (data.applicable_rights && data.applicable_rights.length > 0) {
            lines.push('');
            lines.push('--- Your Rights ---');
            data.applicable_rights.forEach(right => {
                lines.push(`  * ${right.right}`);
                lines.push(`    ${right.explanation}`);
                if (right.legal_basis) lines.push(`    Legal basis: ${right.legal_basis}`);
            });
        }
        if (data.immediate_actions && data.immediate_actions.length > 0) {
            lines.push('');
            lines.push('--- What to Do Next ---');
            data.immediate_actions.forEach(a => {
                lines.push(`  * ${a.action}${a.why ? ' -- ' + a.why : ''}`);
            });
        }
        if (data.documentation_needed && data.documentation_needed.length > 0) {
            lines.push('');
            lines.push('--- Evidence to Gather ---');
            data.documentation_needed.forEach(d => lines.push(`  * ${d}`));
        }
        if (data.free_resources && data.free_resources.length > 0) {
            lines.push('');
            lines.push('--- Free Resources ---');
            data.free_resources.forEach(r => {
                lines.push(`  * ${r.name}: ${r.what_they_do}`);
                if (r.how_to_reach) lines.push(`    Contact: ${r.how_to_reach}`);
            });
        }
        if (data.warnings && data.warnings.length > 0) {
            lines.push('');
            lines.push('--- Things to Avoid ---');
            data.warnings.forEach(w => lines.push(`  * ${w}`));
        }
        if (data.timeline) {
            lines.push('');
            lines.push('--- Important Deadlines ---');
            lines.push(data.timeline);
        }
        lines.push('');
        lines.push('Note: This is educational information, not legal advice.');
    }

    lines.push('');
    lines.push('-'.repeat(40));
    lines.push('Generated by Beacon -- Privacy-First AI Protection.');
    lines.push('Powered by Gemma 4. https://github.com/credwine/beacon');
    lines.push('This analysis was performed locally on your device. No data was transmitted.');

    const text = lines.join('\n');

    navigator.clipboard.writeText(text).then(() => {
        showCopyToast();
    }).catch(() => {
        // Fallback for older browsers
        const ta = document.createElement('textarea');
        ta.value = text;
        ta.style.position = 'fixed';
        ta.style.opacity = '0';
        document.body.appendChild(ta);
        ta.select();
        document.execCommand('copy');
        document.body.removeChild(ta);
        showCopyToast();
    });
}

function showCopyToast() {
    let toast = document.getElementById('copyToast');
    if (!toast) {
        toast = document.createElement('div');
        toast.id = 'copyToast';
        toast.className = 'copy-toast';
        toast.innerHTML = '<div class="copy-toast-content"><i data-lucide="check"></i> <span>Copied to clipboard</span></div>';
        document.body.appendChild(toast);
    }
    toast.style.display = 'block';
    toast.style.animation = 'toastSlideIn 0.3s ease-out';
    lucide.createIcons();

    setTimeout(() => {
        toast.style.animation = 'toastSlideOut 0.3s ease-out forwards';
        setTimeout(() => {
            toast.style.display = 'none';
        }, 300);
    }, 2000);
}

// ---- Trusted Contacts & Alerts ----

const RELATIONSHIP_LABELS = {
    spouse: 'Spouse / Partner',
    child: 'Son / Daughter',
    parent: 'Parent',
    sibling: 'Sibling',
    caregiver: 'Caregiver',
    friend: 'Friend',
    other: 'Other',
};

async function loadContacts() {
    try {
        const res = await fetch('/api/alerts/contacts');
        if (!res.ok) return;
        const contacts = await res.json();
        renderContactsList(contacts);
    } catch { /* best-effort */ }
}

async function loadAlertHistory() {
    try {
        const res = await fetch('/api/alerts/history');
        if (!res.ok) return;
        const history = await res.json();
        renderAlertHistory(history);
    } catch { /* best-effort */ }
}

function renderContactsList(contacts) {
    const container = document.getElementById('contactsList');
    if (!contacts || contacts.length === 0) {
        container.innerHTML = `
            <div class="result-placeholder" style="padding:var(--space-xl);">
                <i data-lucide="users"></i>
                <h3>No contacts yet</h3>
                <p>Add a trusted contact above to enable scam alerts.</p>
            </div>`;
        lucide.createIcons();
        return;
    }

    container.innerHTML = contacts.map(c => {
        const details = [c.email, c.phone].filter(Boolean).join(' | ');
        const relLabel = RELATIONSHIP_LABELS[c.relationship] || c.relationship;
        return `
            <div class="contact-item">
                <div class="contact-info">
                    <div class="contact-name">${c.name}</div>
                    ${details ? `<div class="contact-details">${details}</div>` : ''}
                    <div class="contact-relationship">${relLabel}</div>
                </div>
                <div class="contact-delete">
                    <button class="btn-danger" onclick="deleteContact('${c.id}')">
                        <i data-lucide="trash-2"></i>
                        Remove
                    </button>
                </div>
            </div>`;
    }).join('');
    lucide.createIcons();
}

function renderAlertHistory(history) {
    const container = document.getElementById('alertHistory');
    if (!history || history.length === 0) {
        container.innerHTML = `
            <div class="result-placeholder" style="padding:var(--space-xl);">
                <i data-lucide="bell-off"></i>
                <h3>No alerts yet</h3>
                <p>Alerts will appear here when Beacon detects a dangerous scam.</p>
            </div>`;
        lucide.createIcons();
        return;
    }

    container.innerHTML = history.map(alert => {
        const time = new Date(alert.timestamp).toLocaleString();
        const contacts = alert.contacts_notified ? alert.contacts_notified.join(', ') : 'None';
        return `
            <div class="alert-history-item">
                <div class="alert-history-header">
                    <div class="alert-history-score">Trust Score: ${alert.trust_score}/100</div>
                    <div class="alert-history-time">${time}</div>
                </div>
                <div class="alert-history-type">${alert.scam_type || 'Unknown scam type'}</div>
                <div class="alert-history-contacts"><strong>Contacts alerted:</strong> ${contacts}</div>
            </div>`;
    }).join('');
    lucide.createIcons();
}

async function addContact() {
    const name = document.getElementById('contactName').value.trim();
    const email = document.getElementById('contactEmail').value.trim();
    const phone = document.getElementById('contactPhone').value.trim();
    const relationship = document.getElementById('contactRelationship').value;

    if (!name) {
        alert('Please enter a contact name.');
        return;
    }
    if (!email && !phone) {
        alert('Please enter at least an email or phone number.');
        return;
    }

    try {
        const res = await fetch('/api/alerts/contacts', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, email, phone, relationship })
        });

        if (!res.ok) {
            const err = await res.json();
            alert(err.detail || 'Failed to add contact');
            return;
        }

        // Clear form
        document.getElementById('contactName').value = '';
        document.getElementById('contactEmail').value = '';
        document.getElementById('contactPhone').value = '';
        document.getElementById('contactRelationship').value = 'spouse';

        // Reload contacts list
        loadContacts();
    } catch (err) {
        alert('Failed to add contact: ' + err.message);
    }
}

async function deleteContact(contactId) {
    if (!confirm('Remove this trusted contact?')) return;

    try {
        const res = await fetch(`/api/alerts/contacts/${contactId}`, {
            method: 'DELETE'
        });
        if (!res.ok) {
            alert('Failed to remove contact');
            return;
        }
        loadContacts();
    } catch (err) {
        alert('Failed to remove contact: ' + err.message);
    }
}

async function triggerDangerAlert(scanResult) {
    try {
        const res = await fetch('/api/alerts/trigger', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                trust_score: scanResult.trust_score,
                risk_level: scanResult.risk_level,
                scam_type: scanResult.scam_type,
                explanation: scanResult.explanation,
                red_flags: scanResult.red_flags || [],
                recommended_actions: scanResult.recommended_actions || [],
                safe_alternatives: scanResult.safe_alternatives || ''
            })
        });

        if (!res.ok) return;
        const data = await res.json();

        if (data.status === 'triggered' && data.alert) {
            const names = data.alert.contacts_notified.join(', ');
            showAlertToast(`Alert sent to ${names}`);
        }
    } catch { /* alert triggering is best-effort */ }
}

function showAlertToast(message) {
    const toast = document.getElementById('alertToast');
    const msgEl = document.getElementById('alertToastMessage');
    msgEl.textContent = message;
    toast.style.display = 'block';
    toast.style.animation = 'toastSlideIn 0.3s ease-out';
    lucide.createIcons();

    setTimeout(() => {
        toast.style.animation = 'toastSlideOut 0.3s ease-out forwards';
        setTimeout(() => {
            toast.style.display = 'none';
        }, 300);
    }, 5000);
}

// ---- Dark Mode ----

function toggleTheme() {
    const root = document.documentElement;
    const currentTheme = root.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    root.setAttribute('data-theme', newTheme);
    localStorage.setItem('beacon-theme', newTheme);
    updateThemeIcons(newTheme);
}

function updateThemeIcons(theme) {
    const isDark = theme === 'dark';
    document.querySelectorAll('.theme-icon-moon').forEach(el => {
        el.style.display = isDark ? 'none' : '';
    });
    document.querySelectorAll('.theme-icon-sun').forEach(el => {
        el.style.display = isDark ? '' : 'none';
    });
}

function initTheme() {
    const saved = localStorage.getItem('beacon-theme');
    let theme;
    if (saved) {
        theme = saved;
    } else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        theme = 'dark';
    } else {
        theme = 'light';
    }
    document.documentElement.setAttribute('data-theme', theme);
    updateThemeIcons(theme);

    // Listen for OS theme changes when no explicit preference is saved
    if (window.matchMedia) {
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
            if (!localStorage.getItem('beacon-theme')) {
                const osTheme = e.matches ? 'dark' : 'light';
                document.documentElement.setAttribute('data-theme', osTheme);
                updateThemeIcons(osTheme);
            }
        });
    }
}

// ---- Initialize ----

// Override switchTab to load settings data when settings tab is opened
const _originalSwitchTab = switchTab;
switchTab = function(tab) {
    _originalSwitchTab(tab);
    if (tab === 'settings') {
        loadContacts();
        loadAlertHistory();
    }
};

// ---- Keyboard Shortcuts (Accessibility) ----

document.addEventListener('keydown', (e) => {
    // Only active when app is visible
    if (document.getElementById('app').style.display === 'none') return;

    // Alt+1/2/3/4 to switch tabs
    if (e.altKey && !e.ctrlKey && !e.shiftKey) {
        switch (e.key) {
            case '1': e.preventDefault(); switchTab('scanner'); break;
            case '2': e.preventDefault(); switchTab('contracts'); break;
            case '3': e.preventDefault(); switchTab('rights'); break;
            case '4': e.preventDefault(); switchTab('settings'); break;
            case 'h': e.preventDefault(); toggleHistoryDrawer(); break;
        }
    }

    // Ctrl+Enter to submit the active form
    if (e.ctrlKey && e.key === 'Enter') {
        const activePanel = document.querySelector('.panel.active');
        if (!activePanel) return;
        const id = activePanel.id;
        if (id === 'panel-scanner') runScan();
        else if (id === 'panel-contracts') runContract();
        else if (id === 'panel-rights') runRights();
    }

    // Escape to close history drawer
    if (e.key === 'Escape') {
        const drawer = document.getElementById('historyDrawer');
        if (drawer && drawer.classList.contains('open')) {
            toggleHistoryDrawer();
        }
    }
});

// ---- Landing Page Demo Animation ----

const DEMO_SCAMS = [
    {
        text: 'Subject: URGENT -- Your Apple ID has been compromised\n\nDear Customer,\n\nWe detected unauthorized access to your Apple ID from Russia. Your account will be PERMANENTLY LOCKED in 24 hours unless you verify immediately.\n\nClick here: http://apple-id-secure-verify.com/login\n\nApple Security Team',
        score: 5,
        label: 'DANGEROUS',
        flags: [
            'Fake urgency: "permanently locked in 24 hours"',
            'Suspicious URL: apple-id-secure-verify.com is not Apple',
            'Pressure tactic: threatens account deletion',
            'Generic greeting: "Dear Customer" instead of your name'
        ]
    },
    {
        text: 'Hey! This is Mike from the IRS. We have been trying to reach you about your overdue tax payment of $4,892.31. A warrant has been issued for your arrest if this is not resolved today. Please purchase $4,892 in Apple gift cards and read us the numbers. Final notice.',
        score: 3,
        label: 'DANGEROUS',
        flags: [
            'IRS impersonation: IRS never calls demanding immediate payment',
            'Gift card payment demand: no government accepts gift cards',
            'Arrest threat: IRS does not threaten arrest by phone',
            'Fabricated urgency: "must be resolved today"'
        ]
    },
    {
        text: 'Congratulations! You have been selected as the winner of our $1,000,000 International Lottery! Your ticket #47-29-81 was drawn March 15th. To claim your prize, send a processing fee of $499.99 via Western Union to our claims department. Contact: claims@intl-lottery-winners.net',
        score: 2,
        label: 'DANGEROUS',
        flags: [
            'Lottery scam: you cannot win a lottery you never entered',
            'Upfront fee demand: legitimate lotteries never require fees',
            'Western Union payment: untraceable, favored by scammers',
            'Requests personal information: bank details and ID'
        ]
    }
];

let demoRunning = false;
let demoAbortController = null;
let demoPaused = false;

function demoSleep(ms) {
    return new Promise((resolve, reject) => {
        const timer = setTimeout(resolve, ms);
        if (demoAbortController) {
            demoAbortController.signal.addEventListener('abort', () => {
                clearTimeout(timer);
                reject(new DOMException('Aborted', 'AbortError'));
            });
        }
    });
}

async function runLandingDemo() {
    if (demoRunning) return;
    demoRunning = true;

    const inputEl = document.getElementById('demoInput');
    const resultEl = document.getElementById('demoResult');

    if (!inputEl || !resultEl) {
        demoRunning = false;
        return;
    }

    let cycleIndex = 0;

    while (demoRunning) {
        demoAbortController = new AbortController();
        const scam = DEMO_SCAMS[cycleIndex % DEMO_SCAMS.length];
        cycleIndex++;

        try {
            // Reset state
            resultEl.style.opacity = '0';
            const typingSpan = inputEl.querySelector('.demo-typing');
            if (typingSpan) typingSpan.textContent = '';

            // Wait a beat before starting
            await demoSleep(600);

            // Phase 1: Typewriter effect
            const chars = scam.text;
            for (let i = 0; i < chars.length; i++) {
                while (demoPaused) {
                    await demoSleep(200);
                }
                if (typingSpan) typingSpan.textContent = chars.slice(0, i + 1);
                const ch = chars[i];
                let delay = 12;
                if (ch === '\n') delay = 60;
                else if (ch === '.' || ch === '!' || ch === '?') delay = 80;
                else if (ch === ',') delay = 40;
                await demoSleep(delay);
            }

            await demoSleep(400);

            // Phase 2: Show "Analyzing..." pulse
            resultEl.style.opacity = '1';
            resultEl.innerHTML = '<div class="demo-analyzing">Analyzing with Gemma 4...</div>';
            await demoSleep(1800);

            // Phase 3: Restore result structure and animate score
            resultEl.innerHTML = '';
            const scoreContainer = document.createElement('div');
            scoreContainer.className = 'demo-score-container';
            const scoreDiv = document.createElement('div');
            scoreDiv.className = 'demo-score';
            const labelDiv = document.createElement('div');
            labelDiv.className = 'demo-score-label';
            scoreContainer.appendChild(scoreDiv);
            scoreContainer.appendChild(labelDiv);
            const newFlagsDiv = document.createElement('div');
            newFlagsDiv.className = 'demo-flags';
            resultEl.appendChild(scoreContainer);
            resultEl.appendChild(newFlagsDiv);
            resultEl.style.opacity = '1';

            // Animate score from 100 down to target
            const targetScore = scam.score;
            const totalSteps = 60;
            for (let step = 0; step <= totalSteps; step++) {
                while (demoPaused) {
                    await demoSleep(200);
                }
                const progress = step / totalSteps;
                const eased = 1 - Math.pow(1 - progress, 3);
                const currentScore = Math.round(100 - (100 - targetScore) * eased);
                scoreDiv.textContent = currentScore;

                let color;
                if (currentScore > 70) {
                    color = '#10b981';
                    labelDiv.textContent = 'SAFE';
                } else if (currentScore > 50) {
                    color = '#f59e0b';
                    labelDiv.textContent = 'SUSPICIOUS';
                } else if (currentScore > 20) {
                    color = '#ef4444';
                    labelDiv.textContent = 'HIGH RISK';
                } else {
                    color = '#dc2626';
                    labelDiv.textContent = scam.label;
                }
                scoreDiv.style.color = color;
                labelDiv.style.color = color;

                await demoSleep(25);
            }

            scoreDiv.textContent = targetScore;
            scoreDiv.style.color = '#dc2626';
            labelDiv.textContent = scam.label;
            labelDiv.style.color = '#dc2626';

            await demoSleep(300);

            // Phase 4: Reveal red flags one by one
            const flagIcon = '<svg class="demo-flag-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>';

            for (let i = 0; i < scam.flags.length; i++) {
                while (demoPaused) {
                    await demoSleep(200);
                }
                const flagItem = document.createElement('div');
                flagItem.className = 'demo-flag-item';
                flagItem.innerHTML = flagIcon + '<span>' + scam.flags[i] + '</span>';
                newFlagsDiv.appendChild(flagItem);
                flagItem.offsetHeight; // force reflow
                await demoSleep(50);
                flagItem.classList.add('visible');
                await demoSleep(400);
            }

            // Phase 5: Hold the result for 3 seconds
            await demoSleep(3000);

            // Fade out
            resultEl.style.opacity = '0';
            await demoSleep(500);

            if (typingSpan) typingSpan.textContent = '';

        } catch (e) {
            if (e.name === 'AbortError') break;
            throw e;
        }
    }

    demoRunning = false;
}

function stopLandingDemo() {
    demoRunning = false;
    if (demoAbortController) {
        demoAbortController.abort();
        demoAbortController = null;
    }
}

// Auto-pause when demo scrolls out of view
(function initDemoObserver() {
    document.addEventListener('DOMContentLoaded', () => {
        const demoEl = document.querySelector('.hero-demo');
        if (!demoEl) return;

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                demoPaused = !entry.isIntersecting;
            });
        }, { threshold: 0.1 });

        observer.observe(demoEl);
    });
})();

document.addEventListener('DOMContentLoaded', () => {
    initTheme();
    lucide.createIcons();
    // Start the landing demo if on the landing page
    if (document.getElementById('landing') && document.getElementById('landing').style.display !== 'none') {
        runLandingDemo();
    }
});
