/**
 * App Controller
 * Initializes all modules, manages global state, sidebar toggles, and toasts.
 */

const App = (() => {
    function init() {
        // Initialize all modules
        Database.init();
        Chat.init();
        History.init();

        // Sidebar toggles
        setupSidebars();

        // Check initial status
        checkStatus();
    }

    function setupSidebars() {
        const leftSidebar = document.getElementById('sidebar-left');
        const rightSidebar = document.getElementById('sidebar-right');

        // Left sidebar toggle
        document.getElementById('btn-toggle-left').addEventListener('click', () => {
            leftSidebar.classList.add('collapsed');
            document.getElementById('btn-open-left').style.display = 'block';
        });

        document.getElementById('btn-open-left').addEventListener('click', () => {
            leftSidebar.classList.remove('collapsed');
            leftSidebar.classList.add('mobile-open');
            document.getElementById('btn-open-left').style.display = 'none';
        });

        // Right sidebar toggle
        document.getElementById('btn-toggle-right').addEventListener('click', () => {
            rightSidebar.classList.toggle('collapsed');
        });

        document.getElementById('btn-toggle-right-close').addEventListener('click', () => {
            rightSidebar.classList.add('collapsed');
        });

        document.getElementById('btn-open-right')?.addEventListener('click', () => {
            rightSidebar.classList.remove('collapsed');
            rightSidebar.classList.add('mobile-open');
        });

        // Close mobile sidebar on backdrop click
        document.addEventListener('click', (e) => {
            if (window.innerWidth <= 1024) {
                if (!leftSidebar.contains(e.target) && !e.target.closest('#btn-open-left')) {
                    leftSidebar.classList.remove('mobile-open');
                }
                if (!rightSidebar.contains(e.target) && !e.target.closest('#btn-open-right')) {
                    rightSidebar.classList.remove('mobile-open');
                }
            }
        });
    }

    async function checkStatus() {
        try {
            const res = await fetch('/api/status');
            const data = await res.json();

            if (!data.api_key_configured) {
                Chat.addAssistantMessage(
                    '⚠️ **Gemini API key is not configured.** Please set your `GEMINI_API_KEY` in the `.env` file. ' +
                    'You can get a free key at [Google AI Studio](https://aistudio.google.com/apikey).'
                );
            }

            if (data.connected) {
                // Already connected (session restored)
                const schemaRes = await fetch('/api/schema');
                const schemaData = await schemaRes.json();
                if (schemaData.success) {
                    Database.setConnected(schemaData.schema);
                    Chat.fetchInsights();
                    Chat.enableInput();
                }
            }
        } catch (err) {
            Chat.addAssistantMessage(
                '❌ **Cannot connect to the server.** Please make sure the Flask server is running on `http://127.0.0.1:5000`.'
            );
        }
    }

    /**
     * Show a toast notification.
     * @param {string} message
     * @param {'success'|'error'|'info'} type
     */
    function toast(message, type = 'info') {
        const container = document.getElementById('toast-container');
        const toastEl = document.createElement('div');
        toastEl.className = `toast toast--${type}`;
        toastEl.textContent = message;
        container.appendChild(toastEl);

        setTimeout(() => {
            toastEl.classList.add('toast-out');
            setTimeout(() => toastEl.remove(), 300);
        }, 4000);
    }

    // --- Boot ---
    document.addEventListener('DOMContentLoaded', init);

    return { toast };
})();
