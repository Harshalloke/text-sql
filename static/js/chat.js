/**
 * Chat Module
 * Manages the chat interface — sending messages, rendering responses,
 * handling confirmations, and displaying results.
 */

const Chat = (() => {
    const els = {};
    let inputHistory = [];
    let historyIndex = -1;

    function init() {
        els.messages = document.getElementById('messages');
        els.input = document.getElementById('chat-input');
        els.btnSend = document.getElementById('btn-send');
        els.typingIndicator = document.getElementById('typing-indicator');

        // Send message
        els.btnSend.addEventListener('click', sendMessage);
        els.input.addEventListener('keydown', handleKeyDown);

        // Auto-resize textarea
        els.input.addEventListener('input', autoResize);

        // Example chips
        document.querySelectorAll('.example-chip').forEach(chip => {
            chip.addEventListener('click', () => {
                if (!els.input.disabled) {
                    els.input.value = chip.dataset.query;
                    sendMessage();
                }
            });
        });
    }

    function handleKeyDown(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
        // Input history navigation
        if (e.key === 'ArrowUp' && els.input.value === '') {
            e.preventDefault();
            if (historyIndex < inputHistory.length - 1) {
                historyIndex++;
                els.input.value = inputHistory[inputHistory.length - 1 - historyIndex];
                autoResize();
            }
        }
        if (e.key === 'ArrowDown' && historyIndex >= 0) {
            e.preventDefault();
            historyIndex--;
            els.input.value = historyIndex >= 0
                ? inputHistory[inputHistory.length - 1 - historyIndex]
                : '';
            autoResize();
        }
    }

    function autoResize() {
        els.input.style.height = 'auto';
        els.input.style.height = Math.min(els.input.scrollHeight, 120) + 'px';
    }

    async function fetchInsights() {
        showTyping();
        try {
            const res = await fetch('/api/insights');
            const data = await res.json();
            hideTyping();

            if (data.success && data.insights && data.insights.length > 0) {
                renderInsights(data.insights);
            } else {
                addAssistantMessage("Connected! Start asking questions.");
            }
        } catch (err) {
            hideTyping();
            addAssistantMessage("Connected! Start asking questions.");
        }
    }

    function renderInsights(insights) {
        const msgEl = createAssistantMessage();
        const bubble = msgEl.querySelector('.message__bubble');
        
        let html = `
            <p style="margin-bottom: var(--space-md);">Database connected successfully! I've scanned your data.</p>
            <div class="insights-bubble">
                <h4>💡 Auto-Discovered Insights</h4>
                <p style="margin-bottom: 12px; color: var(--text-secondary); font-size: 0.9rem;">Here is what I found in your data:</p>
                <ul style="margin: 0; padding-left: 20px; color: var(--text-primary); font-size: 1.05rem;">
        `;
        
        insights.forEach(insight => {
            // Apply slight styling to the labels (Trend:, Warning:, Opportunity:)
            const formattedInsight = insight.replace(/^(Trend:|Warning:|Opportunity:)/i, '<strong>$1</strong>');
            html += `<li style="margin-bottom: 10px; line-height: 1.5;">${formattedInsight}</li>`;
        });
        
        html += `</ul></div>`;
        
        bubble.innerHTML = html;
        els.messages.appendChild(msgEl);
        scrollToBottom();
    }

    async function sendMessage() {
        const text = els.input.value.trim();
        if (!text) return;

        // Add to input history
        inputHistory.push(text);
        historyIndex = -1;

        // Add user message bubble
        addUserMessage(text);

        // Clear input
        els.input.value = '';
        autoResize();

        // Show typing indicator
        showTyping();

        try {
            const res = await fetch('/api/query', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query: text }),
            });

            const data = await res.json();
            hideTyping();

            if (!data.success) {
                addAssistantMessage(data.error || 'Something went wrong. Please try again.');
                return;
            }

            handleResponse(data);

        } catch (err) {
            hideTyping();
            addAssistantMessage('Could not reach the server. Please make sure it is running.');
        }

        // Refresh history
        History.refresh();
    }

    function handleResponse(data) {
        switch (data.type) {
            case 'query_result':
                renderQueryResult(data);
                break;
            case 'confirmation_required':
                renderConfirmation(data);
                break;
            case 'modification_result':
                addAssistantMessage(data.message, data.sql);
                break;
            case 'clarification':
                addAssistantMessage(data.message);
                break;
            case 'error':
                addAssistantMessage(data.message);
                break;
            default:
                addAssistantMessage(data.message || 'Received an unknown response.');
        }
    }

    // --- Render query results with table + chart ---
    function renderQueryResult(data) {
        const msgEl = createAssistantMessage();
        const bubble = msgEl.querySelector('.message__bubble');

        // TL;DR (Executive Summary)
        if (data.tldr) {
            const tldrEl = document.createElement('div');
            tldrEl.style.cssText = 'background: rgba(var(--accent-primary-rgb), 0.1); border-left: 3px solid var(--accent-primary); padding: var(--space-sm) var(--space-md); margin-bottom: var(--space-md); border-radius: 0 var(--radius-sm) var(--radius-sm) 0; font-size: 0.95rem; line-height: 1.5;';
            tldrEl.innerHTML = `<strong>💡 TL;DR:</strong> ${formatText(data.tldr)}`;
            bubble.appendChild(tldrEl);
        } else {
            // Fallback explanation if no TL;DR
            const explanation = document.createElement('p');
            explanation.innerHTML = formatText(data.message || 'Here are your results:');
            bubble.appendChild(explanation);
        }

        // Row count
        const countInfo = document.createElement('p');
        countInfo.style.cssText = 'font-size:0.78rem;color:var(--text-tertiary);margin-top:4px;';
        countInfo.textContent = `${data.data.row_count} row(s) returned`;
        bubble.appendChild(countInfo);

        // Data table
        if (data.data && data.data.rows && data.data.rows.length > 0) {
            const table = Visualization.renderTable(data.data);
            bubble.appendChild(table);

            // Try chart
            const chart = Visualization.renderChart(data.data);
            if (chart) {
                bubble.appendChild(chart);
            }
        }

        // Follow-up chips
        if (data.follow_ups && data.follow_ups.length > 0) {
            const chipContainer = document.createElement('div');
            chipContainer.style.cssText = 'display: flex; flex-wrap: wrap; gap: var(--space-sm); margin-top: var(--space-md);';
            
            data.follow_ups.forEach(q => {
                const chip = document.createElement('button');
                chip.className = 'example-chip';
                chip.textContent = q;
                chip.addEventListener('click', () => {
                    if (!els.input.disabled) {
                        els.input.value = q;
                        sendMessage();
                    }
                });
                chipContainer.appendChild(chip);
            });
            bubble.appendChild(chipContainer);
        }

        // SQL toggle
        if (data.sql) {
            bubble.appendChild(createSqlToggle(data.sql));
        }

        els.messages.appendChild(msgEl);
        scrollToBottom();
    }

    // --- Render confirmation prompt ---
    function renderConfirmation(data) {
        const msgEl = createAssistantMessage();
        const bubble = msgEl.querySelector('.message__bubble');

        // Explanation
        const explanation = document.createElement('p');
        explanation.innerHTML = formatText(data.message);
        bubble.appendChild(explanation);

        // Confirmation card
        const card = document.createElement('div');
        card.className = 'confirmation-card';

        const preview = data.preview;
        const levelClass = preview.safety_level === 'critical'
            ? 'confirmation-card__header--critical'
            : preview.safety_level === 'warning'
                ? 'confirmation-card__header--warning'
                : 'confirmation-card__header--info';

        const icon = preview.safety_level === 'critical' ? '🚨' :
                     preview.safety_level === 'warning' ? '⚠️' : 'ℹ️';

        card.innerHTML = `
            <div class="confirmation-card__header ${levelClass}">
                ${icon} Action Preview
            </div>
            <div class="confirmation-card__details">
                <span class="confirmation-card__label">Operation:</span>
                <span class="confirmation-card__value">${preview.operation}</span>
                <span class="confirmation-card__label">Affected Rows:</span>
                <span class="confirmation-card__value">${preview.affected_rows >= 0 ? preview.affected_rows : 'Unknown'}</span>
                <span class="confirmation-card__label">SQL:</span>
                <span class="confirmation-card__value">${escapeHtml(preview.sql)}</span>
            </div>
            ${preview.warning ? `
                <div class="confirmation-card__warning confirmation-card__warning--${preview.safety_level}">
                    ${preview.warning}
                </div>
            ` : ''}
            <div class="confirmation-card__actions">
                <button class="btn btn--ghost btn-cancel-op">Cancel</button>
                <button class="btn ${preview.safety_level === 'critical' ? 'btn--warning' : 'btn--success'} btn-confirm-op">
                    ${preview.safety_level === 'critical' ? '⚠️ Confirm Anyway' : '✓ Confirm'}
                </button>
            </div>
        `;

        // Confirm handler
        card.querySelector('.btn-confirm-op').addEventListener('click', async () => {
            card.querySelector('.confirmation-card__actions').innerHTML =
                '<span class="spinner"></span> Executing...';

            try {
                const res = await fetch('/api/confirm', { method: 'POST' });
                const result = await res.json();
                card.querySelector('.confirmation-card__actions').innerHTML =
                    result.success ? '✅ Done' : '❌ Failed';

                if (result.type === 'modification_result') {
                    App.toast(result.message, 'success');
                } else if (result.type === 'error') {
                    App.toast(result.message, 'error');
                }
                addAssistantMessage(result.message, result.sql);
            } catch (err) {
                card.querySelector('.confirmation-card__actions').innerHTML = '❌ Error';
                App.toast('Failed to execute operation', 'error');
            }
            History.refresh();
        });

        // Cancel handler
        card.querySelector('.btn-cancel-op').addEventListener('click', async () => {
            try {
                await fetch('/api/cancel', { method: 'POST' });
            } catch (_) { /* ignore */ }
            card.querySelector('.confirmation-card__actions').innerHTML = '🚫 Cancelled';
            addAssistantMessage('Operation cancelled. No changes were made.');
        });

        bubble.appendChild(card);
        els.messages.appendChild(msgEl);
        scrollToBottom();
    }

    // --- Public: add messages ---
    function addUserMessage(text) {
        const msg = document.createElement('div');
        msg.className = 'message message--user';
        msg.innerHTML = `
            <div class="message__avatar">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
            </div>
            <div class="message__content">
                <div class="message__bubble">${escapeHtml(text)}</div>
            </div>
        `;
        els.messages.appendChild(msg);
        scrollToBottom();
    }

    function addAssistantMessage(text, sql) {
        const msgEl = createAssistantMessage();
        const bubble = msgEl.querySelector('.message__bubble');
        bubble.innerHTML = formatText(text);

        if (sql) {
            bubble.appendChild(createSqlToggle(sql));
        }

        els.messages.appendChild(msgEl);
        scrollToBottom();
    }

    // --- Helpers ---
    function createAssistantMessage() {
        const msg = document.createElement('div');
        msg.className = 'message message--assistant';
        msg.innerHTML = `
            <div class="message__avatar">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <ellipse cx="12" cy="5" rx="9" ry="3"/>
                    <path d="M3 5v14c0 1.66 4.03 3 9 3s9-1.34 9-3V5"/>
                    <path d="M3 12c0 1.66 4.03 3 9 3s9-1.34 9-3"/>
                </svg>
            </div>
            <div class="message__content">
                <div class="message__bubble"></div>
            </div>
        `;
        return msg;
    }

    function createSqlToggle(sql) {
        const container = document.createElement('div');
        container.className = 'message__sql';

        const toggle = document.createElement('button');
        toggle.className = 'sql-toggle';
        toggle.innerHTML = `
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg>
            Show SQL
        `;

        const block = document.createElement('pre');
        block.className = 'sql-block';
        block.textContent = sql;

        toggle.addEventListener('click', () => {
            block.classList.toggle('visible');
            toggle.innerHTML = block.classList.contains('visible')
                ? '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg> Hide SQL'
                : '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg> Show SQL';
        });

        container.appendChild(toggle);
        container.appendChild(block);
        return container;
    }

    function formatText(text) {
        if (!text) return '';
        // Simple markdown-ish formatting
        return text
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\n/g, '<br>');
    }

    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    let typingInterval;
    const typingTexts = [
        "Analyzing data patterns...",
        "Consulting the database...",
        "Synthesizing insights...",
        "Running analytical queries...",
        "Generating data trends..."
    ];

    function showTyping() {
        els.typingIndicator.style.display = 'flex';
        scrollToBottom();
        
        const textEl = document.getElementById('typing-text');
        if (textEl) {
            let i = 0;
            textEl.textContent = typingTexts[0];
            typingInterval = setInterval(() => {
                i = (i + 1) % typingTexts.length;
                textEl.textContent = typingTexts[i];
            }, 2500);
        }
    }

    function hideTyping() {
        els.typingIndicator.style.display = 'none';
        if (typingInterval) {
            clearInterval(typingInterval);
        }
    }

    function scrollToBottom() {
        requestAnimationFrame(() => {
            els.messages.scrollTop = els.messages.scrollHeight;
        });
    }

    function enableInput() {
        els.input.disabled = false;
        els.btnSend.disabled = false;
        els.input.focus();
    }

    function disableInput() {
        els.input.disabled = true;
        els.btnSend.disabled = true;
    }

    return { init, addUserMessage, addAssistantMessage, enableInput, disableInput, sendMessage, fetchInsights };
})();
