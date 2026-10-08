/**
 * Chat Module
 * CALM Design: Question as 22px heading, answer joined by 1px left line.
 * No bubbles, no avatars. Soft dots for thinking. Calm safety and error statements.
 */

const Chat = (() => {
    const els = {};
    let inputHistory = [];
    let historyIndex = -1;
    let currentExchange = null;
    let currentAnswerEl = null;

    function init() {
        els.messages = document.getElementById('messages');
        els.input = document.getElementById('chat-input');
        els.btnSend = document.getElementById('btn-send');
        els.typingIndicator = document.getElementById('typing-indicator');
        els.emptyState = document.getElementById('empty-state');
        els.trySuggestions = document.getElementById('try-suggestions');

        // Send message
        els.btnSend.addEventListener('click', sendMessage);
        els.input.addEventListener('keydown', handleKeyDown);

        // Auto-resize / single line handler
        els.input.addEventListener('input', autoResize);

        // Bind initial suggestion chips
        bindExampleChips();
    }

    function bindExampleChips() {
        document.querySelectorAll('.example-chip').forEach(chip => {
            chip.onclick = () => {
                if (!els.input.disabled) {
                    els.input.value = chip.dataset.query || chip.textContent.trim();
                    sendMessage();
                }
            };
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
            }
        }
        if (e.key === 'ArrowDown' && historyIndex >= 0) {
            e.preventDefault();
            historyIndex--;
            els.input.value = historyIndex >= 0
                ? inputHistory[inputHistory.length - 1 - historyIndex]
                : '';
        }
    }

    function autoResize() {
        // Keeps clean single line or expands gently if multi-line
        if (els.input.tagName.toLowerCase() === 'textarea') {
            els.input.style.height = 'auto';
            els.input.style.height = Math.min(els.input.scrollHeight, 120) + 'px';
        }
    }

    async function showConnectedInsights(schema) {
        // Immediately hide empty state so chat section displays insights
        if (els.emptyState) {
            els.emptyState.style.display = 'none';
        }

        // If schema not passed, fetch it
        if (!schema || !schema.tables) {
            try {
                const sRes = await fetch('/api/schema');
                const sData = await sRes.json();
                if (sData.success) schema = sData.schema;
            } catch (_) {}
        }

        const dbName = schema?.database_name || 'Database';
        const tables = schema?.tables || {};
        const tableNames = Object.keys(tables);
        const tableCount = tableNames.length;

        // Create exchange with quiet heading
        const exchange = createExchange(`Connected to ${dbName}`);
        const answer = exchange.querySelector('.exchange__answer');

        // Introductory statement
        const intro = document.createElement('div');
        intro.style.cssText = 'font-size: var(--text-sm); color: var(--ink); margin-bottom: 8px;';
        intro.textContent = `Database connected successfully. Discovered ${tableCount} table(s) ready to query:`;
        answer.appendChild(intro);

        // Table Insights summary table
        if (tableCount > 0) {
            const tableWrap = document.createElement('div');
            tableWrap.style.cssText = 'width: 100%; overflow-x: auto; margin: 4px 0 14px 0;';

            const tbl = document.createElement('table');
            tbl.className = 'data-table';
            tbl.style.margin = '0';

            const thead = document.createElement('thead');
            thead.innerHTML = `
                <tr>
                    <th style="padding: 6px 14px 6px 0;">Table</th>
                    <th style="padding: 6px 14px 6px 0; text-align: right;">Rows</th>
                    <th style="padding: 6px 0 6px 14px;">Columns</th>
                </tr>
            `;
            tbl.appendChild(thead);

            const tbody = document.createElement('tbody');
            tableNames.forEach((tName, idx) => {
                const tInfo = tables[tName] || {};
                const colNames = (tInfo.columns || []).map(c => c.name).join(', ');
                const tr = document.createElement('tr');
                tr.style.setProperty('--row-i', idx);
                tr.innerHTML = `
                    <td style="padding: 8px 14px 8px 0; font-weight: 400; color: var(--ink); cursor: pointer;" title="Click to view first rows">
                        ${tName}
                    </td>
                    <td style="padding: 8px 14px 8px 0; text-align: right; font-variant-numeric: tabular-nums; color: var(--mute);">
                        ${tInfo.row_count ?? 0}
                    </td>
                    <td style="padding: 8px 0 8px 14px; color: var(--mute); font-size: var(--text-xs); max-width: 320px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
                        ${colNames}
                    </td>
                `;

                // Clicking table name previews table data
                tr.querySelector('td').addEventListener('click', () => {
                    Database.viewTableData(tName);
                });

                tbody.appendChild(tr);
            });
            tbl.appendChild(tbody);
            tableWrap.appendChild(tbl);
            answer.appendChild(tableWrap);
        }

        // Container for auto-discovered analytical insights
        const insightsBlock = document.createElement('div');
        insightsBlock.style.cssText = 'display: flex; flex-direction: column; gap: 8px; margin-top: 8px; border-top: 1px solid var(--line); padding-top: 12px;';

        const loadingIndicator = document.createElement('div');
        loadingIndicator.style.cssText = 'font-size: var(--text-xs); color: var(--mute); display: flex; align-items: center; gap: 6px;';
        loadingIndicator.innerHTML = '<span class="typing-indicator__dot"></span> Scanning data for trends & insights...';
        insightsBlock.appendChild(loadingIndicator);
        answer.appendChild(insightsBlock);

        scrollToBottom();

        // Fetch AI/Exploratory Insights from /api/insights with 10s timeout
        try {
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 10000);

            const res = await fetch('/api/insights', { signal: controller.signal });
            clearTimeout(timeoutId);
            const data = await res.json();

            loadingIndicator.remove();

            if (data.success && data.insights && data.insights.length > 0) {
                const header = document.createElement('div');
                header.style.cssText = 'font-size: var(--text-xs); color: var(--mute); margin-bottom: 2px;';
                header.textContent = 'Auto-discovered insights:';
                insightsBlock.appendChild(header);

                data.insights.forEach(item => {
                    const row = document.createElement('div');
                    row.style.cssText = 'font-size: var(--text-sm); line-height: 1.5;';
                    row.innerHTML = formatText(item);
                    insightsBlock.appendChild(row);
                });
            } else {
                renderFallbackTableInsights(insightsBlock, schema);
            }
        } catch (_) {
            loadingIndicator.remove();
            renderFallbackTableInsights(insightsBlock, schema);
        }

        scrollToBottom();
    }

    function renderFallbackTableInsights(container, schema) {
        const tables = schema?.tables || {};
        const tableNames = Object.keys(tables);
        if (tableNames.length === 0) return;

        let largest = { name: tableNames[0], count: tables[tableNames[0]]?.row_count || 0 };
        tableNames.forEach(t => {
            const count = tables[t]?.row_count || 0;
            if (count > largest.count) largest = { name: t, count };
        });

        const header = document.createElement('div');
        header.style.cssText = 'font-size: var(--text-xs); color: var(--mute); margin-bottom: 2px;';
        header.textContent = 'Data summary:';
        container.appendChild(header);

        const row1 = document.createElement('div');
        row1.style.fontSize = 'var(--text-sm)';
        row1.innerHTML = `<strong>Trend:</strong> Largest table is <code>${largest.name}</code> with ${largest.count} records.`;
        container.appendChild(row1);

        const row2 = document.createElement('div');
        row2.style.fontSize = 'var(--text-sm)';
        row2.innerHTML = `<strong>Opportunity:</strong> Ask questions like <em>"Show top records"</em> or <em>"Count records by category"</em>.`;
        container.appendChild(row2);
    }

    // Keep fetchInsights as alias
    async function fetchInsights(schema) {
        await showConnectedInsights(schema);
    }

    async function sendMessage() {
        const text = els.input.value.trim();
        if (!text) return;

        // Hide empty state on first query
        if (els.emptyState) {
            els.emptyState.style.display = 'none';
        }

        // Add to input history
        inputHistory.push(text);
        historyIndex = -1;

        // Create new exchange with 22px heading
        const exchange = createExchange(text);
        currentExchange = exchange;
        currentAnswerEl = exchange.querySelector('.exchange__answer');

        // Clear input
        els.input.value = '';
        autoResize();

        // Show thinking state (three soft fading dots)
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
                renderCalmError(data.error || 'The server could not process this request. Verify the database connection.');
                return;
            }

            handleResponse(data, currentAnswerEl);

        } catch (err) {
            hideTyping();
            renderCalmError('Could not reach the server. Please verify the Flask app is running on port 5000.');
        }

        // Refresh history sidebar
        History.refresh();
    }

    function handleResponse(data, targetEl) {
        if (!targetEl) targetEl = (currentAnswerEl || createExchange('').querySelector('.exchange__answer'));

        switch (data.type) {
            case 'query_result':
                renderQueryResult(data, targetEl);
                break;
            case 'confirmation_required':
                renderConfirmation(data, targetEl);
                break;
            case 'modification_result':
                renderModificationDone(data, targetEl);
                break;
            case 'clarification':
                renderClarification(data, targetEl);
                break;
            case 'error':
                renderCalmError(data.message, targetEl);
                break;
            default:
                renderClarification(data, targetEl);
        }
    }

    // --- Render Query Results (Table, Chart, Show Query) ---
    function renderQueryResult(data, targetEl) {
        // TL;DR / Text Finding first
        if (data.tldr) {
            const tldrEl = document.createElement('div');
            tldrEl.className = 'exchange__tldr';
            tldrEl.innerHTML = formatText(data.tldr);
            targetEl.appendChild(tldrEl);
        } else if (data.message) {
            const msgEl = document.createElement('div');
            msgEl.className = 'exchange__tldr';
            msgEl.innerHTML = formatText(data.message);
            targetEl.appendChild(msgEl);
        }

        // Results Container (swapping Table and Chart)
        if (data.data && data.data.rows && data.data.rows.length > 0) {
            const viewContainer = document.createElement('div');
            viewContainer.style.width = '100%';

            // Table element
            const tableEl = Visualization.renderTable(data.data);
            viewContainer.appendChild(tableEl);

            // Chart container (created lazily on toggle)
            let chartContainer = null;
            let activeView = 'table';
            let activeChartType = null;

            // Small muted action row under the table
            const metaRow = document.createElement('div');
            metaRow.className = 'results-meta-row';

            // 1. "N rows"
            const rowCount = document.createElement('span');
            rowCount.textContent = `${data.data.row_count || data.data.rows.length} rows`;
            metaRow.appendChild(rowCount);

            // 2. "Show query" toggle
            let sqlBlock = null;
            if (data.sql) {
                const queryBtn = document.createElement('button');
                queryBtn.className = 'results-action';
                queryBtn.textContent = 'Show query';
                queryBtn.addEventListener('click', () => {
                    if (!sqlBlock) {
                        sqlBlock = createSqlBlock(data.sql);
                        targetEl.appendChild(sqlBlock);
                    }
                    sqlBlock.classList.toggle('visible');
                    queryBtn.textContent = sqlBlock.classList.contains('visible') ? 'Hide query' : 'Show query';
                });
                metaRow.appendChild(queryBtn);
            }

            // 3. "Export CSV"
            const exportBtn = document.createElement('button');
            exportBtn.className = 'results-action';
            exportBtn.textContent = 'Export CSV';
            exportBtn.addEventListener('click', () => {
                Visualization.exportToCsv(data.data);
            });
            metaRow.appendChild(exportBtn);

            // 4. "Chart" (if data is chart-worthy)
            const canChart = Visualization.detectChartType(data.data);
            if (canChart) {
                const chartToggleBtn = document.createElement('button');
                chartToggleBtn.className = 'results-action';
                chartToggleBtn.textContent = 'Chart';

                const barBtn = document.createElement('button');
                barBtn.className = 'results-action';
                barBtn.textContent = 'Bar';
                barBtn.style.display = 'none';

                const lineBtn = document.createElement('button');
                lineBtn.className = 'results-action';
                lineBtn.textContent = 'Line';
                lineBtn.style.display = 'none';

                const switchToTable = () => {
                    activeView = 'table';
                    tableEl.style.display = '';
                    if (chartContainer) chartContainer.style.display = 'none';
                    chartToggleBtn.textContent = 'Chart';
                    chartToggleBtn.classList.remove('results-action--active');
                    barBtn.style.display = 'none';
                    lineBtn.style.display = 'none';
                };

                const switchToChart = (chartType = null) => {
                    activeView = 'chart';
                    tableEl.style.display = 'none';
                    chartToggleBtn.textContent = 'Table';
                    chartToggleBtn.classList.add('results-action--active');
                    barBtn.style.display = 'inline';
                    lineBtn.style.display = 'inline';

                    if (!chartContainer) {
                        chartContainer = Visualization.renderChart(data.data, chartType);
                        viewContainer.appendChild(chartContainer);
                    } else {
                        chartContainer.remove();
                        chartContainer = Visualization.renderChart(data.data, chartType);
                        viewContainer.appendChild(chartContainer);
                    }
                    chartContainer.style.display = 'block';
                };

                chartToggleBtn.addEventListener('click', () => {
                    if (activeView === 'table') {
                        switchToChart();
                    } else {
                        switchToTable();
                    }
                });

                barBtn.addEventListener('click', () => switchToChart('bar'));
                lineBtn.addEventListener('click', () => switchToChart('line'));

                metaRow.appendChild(chartToggleBtn);
                metaRow.appendChild(barBtn);
                metaRow.appendChild(lineBtn);
            }

            targetEl.appendChild(viewContainer);
            targetEl.appendChild(metaRow);
        }

        // Quiet follow-up suggestions
        if (data.follow_ups && data.follow_ups.length > 0) {
            const followUps = document.createElement('div');
            followUps.style.cssText = 'display: flex; flex-wrap: wrap; gap: 12px; margin-top: 10px; font-size: var(--text-xs); color: var(--mute);';
            const label = document.createElement('span');
            label.textContent = 'Related:';
            followUps.appendChild(label);

            data.follow_ups.forEach(q => {
                const link = document.createElement('button');
                link.className = 'results-action';
                link.textContent = q;
                link.addEventListener('click', () => {
                    if (!els.input.disabled) {
                        els.input.value = q;
                        sendMessage();
                    }
                });
                followUps.appendChild(link);
            });
            targetEl.appendChild(followUps);
        }

        scrollToBottom();
    }

    // --- Safety State: INSERT/UPDATE/DELETE Confirmation ---
    function renderConfirmation(data, targetEl) {
        const preview = data.preview || {};
        const container = document.createElement('div');
        container.className = 'safety-container';

        // Plain sentence in warn color
        const statement = document.createElement('p');
        statement.className = 'safety-statement safety-statement--warn';
        statement.textContent = data.message || `This will modify ${preview.affected_rows ?? 'some'} row(s).`;
        container.appendChild(statement);

        // Text links: Confirm (warn color) and Cancel
        const actionRow = document.createElement('div');
        actionRow.className = 'safety-actions';

        const confirmBtn = document.createElement('button');
        confirmBtn.className = 'safety-btn--confirm';
        confirmBtn.textContent = 'Confirm';

        const cancelBtn = document.createElement('button');
        cancelBtn.className = 'safety-btn--cancel';
        cancelBtn.textContent = 'Cancel';

        actionRow.appendChild(confirmBtn);
        actionRow.appendChild(cancelBtn);
        container.appendChild(actionRow);

        // Confirm handler
        confirmBtn.addEventListener('click', async () => {
            confirmBtn.disabled = true;
            cancelBtn.disabled = true;
            actionRow.textContent = 'Executing...';

            try {
                const res = await fetch('/api/confirm', { method: 'POST' });
                const result = await res.json();

                if (result.success) {
                    statement.className = 'safety-statement safety-statement--done';
                    statement.textContent = result.message || 'Done. Modification executed successfully.';
                    actionRow.remove();
                } else {
                    statement.className = 'safety-statement safety-statement--bad';
                    statement.textContent = result.error || 'Execution failed.';
                    actionRow.remove();
                }
            } catch (_) {
                statement.className = 'safety-statement safety-statement--bad';
                statement.textContent = 'Could not execute the confirmed operation.';
                actionRow.remove();
            }
            History.refresh();
        });

        // Cancel handler
        cancelBtn.addEventListener('click', async () => {
            try {
                await fetch('/api/cancel', { method: 'POST' });
            } catch (_) {}
            statement.className = 'safety-statement';
            statement.style.color = 'var(--mute)';
            statement.textContent = 'Operation cancelled. No changes were made.';
            actionRow.remove();
        });

        targetEl.appendChild(container);
        scrollToBottom();
    }

    // --- Safety State: Done Modification Result ---
    function renderModificationDone(data, targetEl) {
        const p = document.createElement('p');
        p.className = 'safety-statement safety-statement--done';
        p.textContent = data.message || 'Done.';
        targetEl.appendChild(p);

        if (data.sql) {
            targetEl.appendChild(createSqlBlock(data.sql));
        }
        scrollToBottom();
    }

    // --- Clarification / Normal Assistant Message ---
    function renderClarification(data, targetEl) {
        const p = document.createElement('p');
        p.style.fontSize = 'var(--text-sm)';
        p.innerHTML = formatText(data.message || 'No response details.');
        targetEl.appendChild(p);
        scrollToBottom();
    }

    // --- Error: Plain Sentence in bad Color, Calm, No Apologies ---
    function renderCalmError(message, targetEl) {
        if (!targetEl) {
            const exchange = createExchange('');
            targetEl = exchange.querySelector('.exchange__answer');
        }
        const err = document.createElement('p');
        err.className = 'safety-statement safety-statement--bad';
        err.innerHTML = formatText(message);
        targetEl.appendChild(err);
        scrollToBottom();
    }

    // --- Public API for other modules to output messages ---
    function addAssistantMessage(text, sql) {
        if (els.emptyState && els.messages.children.length > 0) {
            els.emptyState.style.display = 'none';
        }
        const exchange = createExchange('');
        const answer = exchange.querySelector('.exchange__answer');
        const p = document.createElement('p');
        p.innerHTML = formatText(text);
        answer.appendChild(p);

        if (sql) {
            answer.appendChild(createSqlBlock(sql));
        }
        scrollToBottom();
    }

    function addUserMessage(text) {
        if (els.emptyState) els.emptyState.style.display = 'none';
        const exchange = createExchange(text);
        currentExchange = exchange;
        currentAnswerEl = exchange.querySelector('.exchange__answer');
        scrollToBottom();
    }

    // --- DOM Helpers ---
    function createExchange(questionText) {
        const exchange = document.createElement('div');
        exchange.className = 'exchange';

        if (questionText) {
            const h2 = document.createElement('h2');
            h2.className = 'exchange__question';
            h2.textContent = questionText;
            exchange.appendChild(h2);
        }

        const answer = document.createElement('div');
        answer.className = 'exchange__answer';
        exchange.appendChild(answer);

        els.messages.appendChild(exchange);
        return exchange;
    }

    function createSqlBlock(sql) {
        const pre = document.createElement('pre');
        pre.className = 'sql-block';
        pre.textContent = sql;

        // Copy on click
        pre.addEventListener('click', () => {
            navigator.clipboard.writeText(sql).then(() => {
                pre.classList.add('copied');
                setTimeout(() => pre.classList.remove('copied'), 1800);
            });
        });

        return pre;
    }

    function updateTrySuggestions(tableNames) {
        if (!els.trySuggestions || !tableNames || tableNames.length === 0) return;
        els.trySuggestions.innerHTML = '<span class="try-suggestions__label">Try:</span>';

        const t1 = tableNames[0];
        const suggestions = [
            `Show 10 rows from ${t1}`,
            `Count of total records in ${t1}`,
            tableNames.length > 1 ? `List tables and row counts` : `Summary statistics of ${t1}`
        ];

        suggestions.forEach(query => {
            const btn = document.createElement('button');
            btn.type = 'button';
            btn.className = 'try-link example-chip';
            btn.dataset.query = query;
            btn.textContent = query;
            btn.onclick = () => {
                if (!els.input.disabled) {
                    els.input.value = query;
                    sendMessage();
                }
            };
            els.trySuggestions.appendChild(btn);
        });
    }

    function formatText(text) {
        if (!text) return '';
        return text
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/`(.*?)`/g, '<code style="font-family:var(--font-mono);font-size:0.9em;background:var(--soft);padding:1px 4px;border-radius:4px;">$1</code>')
            .replace(/\n/g, '<br>');
    }

    function showTyping() {
        els.typingIndicator.style.display = 'flex';
        scrollToBottom();
    }

    function hideTyping() {
        els.typingIndicator.style.display = 'none';
    }

    function scrollToBottom() {
        requestAnimationFrame(() => {
            window.scrollTo({
                top: document.documentElement.scrollHeight,
                behavior: 'smooth'
            });
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

    function resetEmptyState() {
        if (els.emptyState) {
            els.emptyState.style.display = 'block';
        }
    }

    return {
        init,
        addUserMessage,
        addAssistantMessage,
        enableInput,
        disableInput,
        sendMessage,
        fetchInsights,
        showConnectedInsights,
        resetEmptyState,
        updateTrySuggestions
    };
})();
