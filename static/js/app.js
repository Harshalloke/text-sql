/**
 * App Controller
 * Initializes all modules, manages global state, theme toggle, and keyboard shortcuts.
 */

const App = (() => {
    function init() {
        // Init theme from localStorage if set
        initTheme();

        // Initialize all modules
        Database.init();
        Chat.init();
        History.init();

        // Setup UI triggers
        setupNav();
        setupShortcuts();

        // Check initial server and connection status
        checkStatus();
    }

    function initTheme() {
        const savedTheme = localStorage.getItem('qm_theme');
        if (savedTheme) {
            document.documentElement.setAttribute('data-theme', savedTheme);
        }

        const themeBtn = document.getElementById('btn-toggle-theme');
        if (themeBtn) {
            themeBtn.addEventListener('click', toggleTheme);
        }
    }

    function toggleTheme() {
        const current = document.documentElement.getAttribute('data-theme');
        let next;

        if (current === 'dark') {
            next = 'light';
        } else if (current === 'light') {
            next = 'dark';
        } else {
            // If unset, detect system preference and flip
            const isDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
            next = isDark ? 'light' : 'dark';
        }

        document.documentElement.setAttribute('data-theme', next);
        localStorage.setItem('qm_theme', next);
    }

    function setupNav() {
        const rightSidebar = document.getElementById('sidebar-right');
        const btnToggleRight = document.getElementById('btn-toggle-right');
        const btnToggleRightClose = document.getElementById('btn-toggle-right-close');

        // History slide panel
        if (btnToggleRight && rightSidebar) {
            btnToggleRight.addEventListener('click', () => {
                rightSidebar.classList.toggle('open');
                if (rightSidebar.classList.contains('open')) {
                    History.refresh();
                }
            });
        }

        if (btnToggleRightClose && rightSidebar) {
            btnToggleRightClose.addEventListener('click', () => {
                rightSidebar.classList.remove('open');
            });
        }

        // Tables inline toggle
        const schemaExplorer = document.getElementById('schema-explorer');
        const btnTablesNav = document.getElementById('btn-tables-nav');
        const btnEmptyTables = document.getElementById('btn-empty-tables');
        const btnCloseTables = document.getElementById('btn-close-tables');

        const toggleTables = () => {
            if (!schemaExplorer) return;
            const isVisible = schemaExplorer.style.display !== 'none';
            schemaExplorer.style.display = isVisible ? 'none' : 'block';
            if (!isVisible) {
                schemaExplorer.scrollIntoView({ behavior: 'smooth' });
            }
        };

        if (btnTablesNav) btnTablesNav.addEventListener('click', toggleTables);
        if (btnEmptyTables) btnEmptyTables.addEventListener('click', toggleTables);
        if (btnCloseTables) {
            btnCloseTables.addEventListener('click', () => {
                if (schemaExplorer) schemaExplorer.style.display = 'none';
            });
        }

        // Empty state connect button
        const btnEmptyConnect = document.getElementById('btn-empty-connect');
        if (btnEmptyConnect) {
            btnEmptyConnect.addEventListener('click', () => {
                Database.openModal();
            });
        }

        // Model indicator
        const modelIndicator = document.getElementById('model-indicator');
        if (modelIndicator) {
            modelIndicator.addEventListener('click', () => {
                toast('Running on Gemini 2.5 Flash / Pro model pipeline', 'info');
            });
        }

        // Close right sidebar if clicking outside
        document.addEventListener('click', (e) => {
            if (rightSidebar && rightSidebar.classList.contains('open')) {
                if (!rightSidebar.contains(e.target) && !btnToggleRight.contains(e.target)) {
                    rightSidebar.classList.remove('open');
                }
            }
        });
    }

    function setupShortcuts() {
        document.addEventListener('keydown', (e) => {
            // '/' shortcut focuses the input if not already inside an input or textarea
            if (e.key === '/' && !['INPUT', 'TEXTAREA'].includes(document.activeElement.tagName)) {
                e.preventDefault();
                const input = document.getElementById('chat-input');
                if (input && !input.disabled) {
                    input.focus();
                }
            }

            // 'Escape' closes open panels
            if (e.key === 'Escape') {
                const rightSidebar = document.getElementById('sidebar-right');
                if (rightSidebar) rightSidebar.classList.remove('open');
                Database.closeModal();
                Database.closeDataViewer();
                const anomalyModal = document.getElementById('anomaly-modal');
                if (anomalyModal) anomalyModal.style.display = 'none';
                const driversModal = document.getElementById('drivers-modal');
                if (driversModal) driversModal.style.display = 'none';
            }
        });
    }

    async function checkStatus() {
        try {
            const res = await fetch('/api/status');
            const data = await res.json();

            if (!data.api_key_configured) {
                Chat.addAssistantMessage('Gemini API key is not configured in .env. Natural language queries will be unavailable until a key is added.');
            }

            if (data.connected) {
                const schemaRes = await fetch('/api/schema');
                const schemaData = await schemaRes.json();
                if (schemaData.success) {
                    Database.setConnected(schemaData.schema);
                    Chat.enableInput();
                    Chat.showConnectedInsights(schemaData.schema);
                }
            }
        } catch (err) {
            Chat.addAssistantMessage('Cannot connect to the server. Please verify the Flask server is running.');
        }
    }

    /**
     * Show a calm, quiet toast.
     */
    function toast(message, type = 'info') {
        const container = document.getElementById('toast-container');
        if (!container) return;
        const toastEl = document.createElement('div');
        toastEl.className = `toast toast--${type}`;
        toastEl.textContent = message;
        container.appendChild(toastEl);

        setTimeout(() => {
            toastEl.style.opacity = '0';
            setTimeout(() => toastEl.remove(), 200);
        }, 3200);
    }

    document.addEventListener('DOMContentLoaded', init);

    return { toast };
})();
