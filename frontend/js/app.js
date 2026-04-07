/* ============================================
   BEACON -- Application Logic
   ============================================ */

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
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
    document.querySelector(`.tab[data-tab="${tab}"]`).classList.add('active');
    document.getElementById(`panel-${tab}`).classList.add('active');
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
    document.getElementById('scanResult').innerHTML = `
        <div class="result-placeholder">
            <i data-lucide="shield"></i>
            <h3>Results will appear here</h3>
            <p>Paste a message and click "Analyze" to get started.</p>
        </div>`;
    lucide.createIcons();
}

async function runScan() {
    const content = document.getElementById('scanInput').value.trim();
    if (!content) return;

    const btn = document.getElementById('scanBtn');
    const resultDiv = document.getElementById('scanResult');

    btn.disabled = true;
    resultDiv.innerHTML = `
        <div class="loading-pulse">
            <div class="loading-spinner"></div>
            <div class="loading-text">Analyzing message with Gemma 4...</div>
        </div>`;

    try {
        const res = await fetch('/api/scan', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                content,
                context: document.getElementById('scanContext').value.trim()
            })
        });

        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        renderScanResult(data, resultDiv);
    } catch (err) {
        resultDiv.innerHTML = `
            <div class="result-placeholder">
                <i data-lucide="alert-triangle"></i>
                <h3>Analysis failed</h3>
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

function clearContract() {
    document.getElementById('contractInput').value = '';
    document.getElementById('contractType').value = '';
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
            <div class="loading-text">Analyzing document with Gemma 4...</div>
        </div>`;

    try {
        const res = await fetch('/api/contract', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                content,
                document_type: document.getElementById('contractType').value
            })
        });

        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        renderContractResult(data, resultDiv);
    } catch (err) {
        resultDiv.innerHTML = `
            <div class="result-placeholder">
                <i data-lucide="alert-triangle"></i>
                <h3>Analysis failed</h3>
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
            <div class="loading-text">Researching your rights with Gemma 4...</div>
        </div>`;

    try {
        const res = await fetch('/api/rights', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                situation,
                category: document.getElementById('rightsCategory').value
            })
        });

        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        renderRightsResult(data, resultDiv);
    } catch (err) {
        resultDiv.innerHTML = `
            <div class="result-placeholder">
                <i data-lucide="alert-triangle"></i>
                <h3>Analysis failed</h3>
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
    `;
}

// ---- Initialize ----

document.addEventListener('DOMContentLoaded', () => {
    lucide.createIcons();
});
