/**
 * History Module
 * Renders the operation history sidebar and keeps it updated.
 */

const History = (() => {
    const els = {};

    function init() {
        els.list = document.getElementById('history-list');
        els.statTotal = document.getElementById('stat-total');
        els.statSuccess = document.getElementById('stat-success');
        els.statFailed = document.getElementById('stat-failed');
    }

    /**
     * Fetch and render the latest history from the server.
     */
    async function refresh() {
        try {
            const res = await fetch('/api/history');
            const data = await res.json();
            if (data.success) {
                renderHistory(data.history);
                renderStats(data.stats);
            }
        } catch (_) { /* ignore */ }
    }

    function renderStats(stats) {
        els.statTotal.textContent = stats.total || 0;
        els.statSuccess.textContent = stats.successful || 0;
        els.statFailed.textContent = stats.failed || 0;
    }

    function renderHistory(history) {
        if (!history || history.length === 0) {
            els.list.innerHTML = `
                <div class="history-empty">
                    <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.4">
                        <circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>
                    </svg>
                    <p>No operations yet</p>
                </div>
            `;
            return;
        }

        els.list.innerHTML = '';
        history.forEach(item => {
            const el = document.createElement('div');
            el.className = 'history-item';

            const time = formatTime(item.timestamp);
            const statusClass = item.success ? 'history-item__status--success' : 'history-item__status--error';
            const statusText = item.success ? '✓ Success' : '✗ Failed';

            el.innerHTML = `
                <div class="history-item__header">
                    <span class="history-item__badge history-item__badge--${item.operation_type}">${item.operation_type}</span>
                    <span class="history-item__time">${time}</span>
                </div>
                <div class="history-item__request">${escapeHtml(item.user_request)}</div>
                <div class="history-item__meta">
                    <span class="${statusClass}">${statusText}</span>
                    ${item.affected_rows > 0 ? `<span>${item.affected_rows} row(s)</span>` : ''}
                </div>
            `;

            // Click to show details in chat
            el.addEventListener('click', () => {
                Chat.addAssistantMessage(
                    `**History Entry #${item.id}**\n\n` +
                    `**Request:** ${item.user_request}\n` +
                    `**Operation:** ${item.operation_type}\n` +
                    `**Explanation:** ${item.explanation}\n` +
                    `**Status:** ${item.success ? 'Success' : 'Failed'}\n` +
                    `**Rows affected:** ${item.affected_rows}\n` +
                    (item.error ? `**Error:** ${item.error}\n` : '') +
                    `**Time:** ${new Date(item.timestamp).toLocaleString()}`,
                    item.sql
                );
            });

            els.list.appendChild(el);
        });
    }

    function formatTime(timestamp) {
        const date = new Date(timestamp);
        const now = new Date();
        const diffMs = now - date;
        const diffMin = Math.floor(diffMs / 60000);

        if (diffMin < 1) return 'Just now';
        if (diffMin < 60) return `${diffMin}m ago`;
        if (diffMin < 1440) return `${Math.floor(diffMin / 60)}h ago`;
        return date.toLocaleDateString();
    }

    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    return { init, refresh };
})();
