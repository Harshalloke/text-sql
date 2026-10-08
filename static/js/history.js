/**
 * History Module
 * CALM Design: Right slide-in panel, list of past questions with relative time,
 * click to re-ask.
 */

const History = (() => {
    const els = {};

    function init() {
        els.list = document.getElementById('history-list');
        els.statTotal = document.getElementById('stat-total');
        els.statSuccess = document.getElementById('stat-success');
        els.statFailed = document.getElementById('stat-failed');
    }

    async function refresh() {
        try {
            const res = await fetch('/api/history');
            const data = await res.json();
            if (data.success) {
                renderHistory(data.history);
                renderStats(data.stats);
            }
        } catch (_) {}
    }

    function renderStats(stats) {
        if (!stats) return;
        if (els.statTotal) els.statTotal.textContent = stats.total || 0;
        if (els.statSuccess) els.statSuccess.textContent = stats.successful || 0;
        if (els.statFailed) els.statFailed.textContent = stats.failed || 0;
    }

    function renderHistory(history) {
        if (!els.list) return;

        if (!history || history.length === 0) {
            els.list.innerHTML = '<div style="font-size: var(--text-xs); color: var(--mute);">No operations yet.</div>';
            return;
        }

        els.list.innerHTML = '';
        history.forEach(item => {
            const el = document.createElement('div');
            el.className = 'history-item';

            const time = formatTime(item.timestamp);
            const statusLabel = item.success ? '' : '<span style="color:var(--bad)">failed</span>';

            el.innerHTML = `
                <div class="history-item__query">${escapeHtml(item.user_request)}</div>
                <div class="history-item__meta">
                    <span>${time}</span>
                    ${statusLabel}
                </div>
            `;

            // Click to re-ask
            el.addEventListener('click', () => {
                const input = document.getElementById('chat-input');
                if (input && !input.disabled) {
                    input.value = item.user_request;
                    const rightSidebar = document.getElementById('sidebar-right');
                    if (rightSidebar) rightSidebar.classList.remove('open');
                    Chat.sendMessage();
                }
            });

            els.list.appendChild(el);
        });
    }

    function formatTime(timestamp) {
        if (!timestamp) return '';
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
        if (!text) return '';
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    return { init, refresh };
})();
