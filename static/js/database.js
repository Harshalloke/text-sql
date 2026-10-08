/**
 * Database Connection Module
 * CALM Design: Quiet connect panel, plain text tabs, inline schema viewer,
 * and quiet table row preview.
 */

const Database = (() => {
    const els = {};
    let currentDbType = 'sqlite';

    function init() {
        // Cache DOM references
        els.btnConnect = document.getElementById('btn-connect');
        els.btnDisconnect = document.getElementById('btn-disconnect');
        els.btnCloseModal = document.getElementById('btn-close-modal');
        els.btnCancelConnect = document.getElementById('btn-cancel-connect');
        els.btnRefreshSchema = document.getElementById('btn-refresh-schema');
        els.modal = document.getElementById('connect-modal');
        els.modalBackdrop = els.modal.querySelector('.modal__backdrop');

        // Data Viewer Modal
        els.dataViewerModal = document.getElementById('data-viewer-modal');
        els.dataViewerClose = document.getElementById('btn-close-data-viewer');
        els.dataViewerBackdrop = els.dataViewerModal.querySelector('.modal__backdrop');
        els.dataViewerTitle = document.getElementById('data-viewer-title');
        els.dataViewerContent = document.getElementById('data-viewer-content');
        els.dataViewerLoader = document.getElementById('data-viewer-loader');

        // Forms and Status
        els.connectForm = document.getElementById('connect-form');
        els.connectError = document.getElementById('connect-error');
        els.connectionStatus = document.getElementById('connection-status');
        els.schemaExplorer = document.getElementById('schema-explorer');
        els.schemaTree = document.getElementById('schema-tree');
        els.submitBtn = document.getElementById('btn-submit-connect');

        // DB Tabs
        els.dbTabs = document.querySelectorAll('.db-tab');
        els.formSqlite = document.getElementById('form-sqlite');
        els.formMysql = document.getElementById('form-mysql');
        els.formPostgresql = document.getElementById('form-postgresql');

        // Upload Form & Toggles
        els.uploadForm = document.getElementById('upload-form');
        els.connectDbContainer = document.getElementById('connect-db-container');
        els.btnSwitchToUpload = document.getElementById('btn-switch-to-upload');
        els.btnSwitchToDb = document.getElementById('btn-switch-to-db');
        els.dropZone = document.getElementById('drop-zone');
        els.fileInput = document.getElementById('file-input');
        els.dropZonePrompt = els.dropZone?.querySelector('.drop-zone__prompt');
        els.btnSubmitUpload = document.getElementById('btn-submit-upload');

        // Event Listeners
        if (els.btnConnect) els.btnConnect.addEventListener('click', openModal);
        if (els.btnCloseModal) els.btnCloseModal.addEventListener('click', closeModal);
        if (els.btnCancelConnect) els.btnCancelConnect.addEventListener('click', closeModal);
        if (els.modalBackdrop) els.modalBackdrop.addEventListener('click', closeModal);
        if (els.btnDisconnect) els.btnDisconnect.addEventListener('click', disconnect);
        if (els.connectForm) els.connectForm.addEventListener('submit', handleConnect);
        if (els.btnRefreshSchema) els.btnRefreshSchema.addEventListener('click', refreshSchema);

        if (els.dataViewerClose) els.dataViewerClose.addEventListener('click', closeDataViewer);
        if (els.dataViewerBackdrop) els.dataViewerBackdrop.addEventListener('click', closeDataViewer);

        els.dbTabs.forEach(tab => {
            tab.addEventListener('click', () => switchDbType(tab.dataset.type));
        });

        // Switch between DB tabs and File Upload
        if (els.btnSwitchToUpload) {
            els.btnSwitchToUpload.addEventListener('click', () => {
                if (els.connectDbContainer) els.connectDbContainer.style.display = 'none';
                if (els.uploadForm) els.uploadForm.style.display = 'block';
                if (els.connectError) els.connectError.style.display = 'none';
            });
        }

        if (els.btnSwitchToDb) {
            els.btnSwitchToDb.addEventListener('click', () => {
                if (els.uploadForm) els.uploadForm.style.display = 'none';
                if (els.connectDbContainer) els.connectDbContainer.style.display = 'block';
                if (els.connectError) els.connectError.style.display = 'none';
            });
        }

        // Drop zone file select
        if (els.dropZone && els.fileInput) {
            els.dropZone.addEventListener('click', () => els.fileInput.click());
            els.fileInput.addEventListener('change', handleFileSelect);

            els.dropZone.addEventListener('dragover', (e) => {
                e.preventDefault();
                els.dropZone.classList.add('dragover');
            });
            els.dropZone.addEventListener('dragleave', () => {
                els.dropZone.classList.remove('dragover');
            });
            els.dropZone.addEventListener('drop', (e) => {
                e.preventDefault();
                els.dropZone.classList.remove('dragover');
                if (e.dataTransfer.files.length) {
                    els.fileInput.files = e.dataTransfer.files;
                    handleFileSelect();
                }
            });
        }

        if (els.uploadForm) {
            els.uploadForm.addEventListener('submit', handleUpload);
        }
    }

    function handleFileSelect() {
        if (els.fileInput.files.length > 0) {
            els.dropZonePrompt.textContent = els.fileInput.files[0].name;
            if (els.btnSubmitUpload) els.btnSubmitUpload.disabled = false;
        } else {
            els.dropZonePrompt.textContent = 'Drag & drop a CSV or Excel file here, or click to browse';
            if (els.btnSubmitUpload) els.btnSubmitUpload.disabled = true;
        }
    }

    async function handleUpload(e) {
        e.preventDefault();
        if (!els.fileInput.files.length) return;

        const file = els.fileInput.files[0];
        const formData = new FormData();
        formData.append('file', file);

        if (els.connectError) els.connectError.style.display = 'none';

        const btnText = els.btnSubmitUpload.querySelector('.btn__text');
        const btnLoader = els.btnSubmitUpload.querySelector('.btn__loader');
        if (btnText) btnText.style.display = 'none';
        if (btnLoader) btnLoader.style.display = 'inline';
        els.btnSubmitUpload.disabled = true;

        try {
            const res = await fetch('/api/upload', {
                method: 'POST',
                body: formData
            });
            const data = await res.json();

            if (data.success) {
                closeModal();
                setConnected(data.schema);
                const tableCount = Object.keys(data.schema.tables || {}).length;
                App.toast(`Connected. Found ${tableCount} table(s).`, 'success');
                Chat.enableInput();
                Chat.showConnectedInsights(data.schema);
            } else {
                showError(data.error || 'Upload failed.');
            }
        } catch (err) {
            showError('Network error during upload.');
        } finally {
            if (btnText) btnText.style.display = 'inline';
            if (btnLoader) btnLoader.style.display = 'none';
            els.btnSubmitUpload.disabled = false;
        }
    }

    function openModal() {
        if (!els.modal) return;
        els.modal.style.display = 'flex';
        if (els.connectError) els.connectError.style.display = 'none';

        setTimeout(() => {
            const activeInput = els.modal.querySelector('.connect-form__fields:not([style*="display: none"]) input');
            if (activeInput) activeInput.focus();
        }, 80);
    }

    function closeModal() {
        if (els.modal) els.modal.style.display = 'none';
    }

    function switchDbType(type) {
        currentDbType = type;
        els.dbTabs.forEach(t => t.classList.toggle('active', t.dataset.type === type));
        if (els.formSqlite) els.formSqlite.style.display = type === 'sqlite' ? '' : 'none';
        if (els.formMysql) els.formMysql.style.display = type === 'mysql' ? '' : 'none';
        if (els.formPostgresql) els.formPostgresql.style.display = type === 'postgresql' ? '' : 'none';
        if (els.connectError) els.connectError.style.display = 'none';
    }

    async function handleConnect(e) {
        e.preventDefault();
        if (els.connectError) els.connectError.style.display = 'none';

        const btnText = els.submitBtn.querySelector('.btn__text');
        const btnLoader = els.submitBtn.querySelector('.btn__loader');
        if (btnText) btnText.style.display = 'none';
        if (btnLoader) btnLoader.style.display = 'inline';
        els.submitBtn.disabled = true;

        const payload = { db_type: currentDbType };
        if (currentDbType === 'sqlite') {
            payload.path = document.getElementById('sqlite-path').value.trim();
        } else if (currentDbType === 'mysql') {
            payload.host = document.getElementById('mysql-host').value.trim() || 'localhost';
            payload.port = document.getElementById('mysql-port').value || '3306';
            payload.user = document.getElementById('mysql-user').value.trim();
            payload.password = document.getElementById('mysql-password').value;
            payload.database = document.getElementById('mysql-database').value.trim();
        } else if (currentDbType === 'postgresql') {
            payload.host = document.getElementById('pg-host').value.trim() || 'localhost';
            payload.port = document.getElementById('pg-port').value || '5432';
            payload.user = document.getElementById('pg-user').value.trim();
            payload.password = document.getElementById('pg-password').value;
            payload.database = document.getElementById('pg-database').value.trim();
        }

        try {
            const res = await fetch('/api/connect', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload),
            });
            const data = await res.json();

            if (data.success) {
                closeModal();
                setConnected(data.schema);
                const tableCount = Object.keys(data.schema.tables || {}).length;
                App.toast(`Connected. Found ${tableCount} table(s).`, 'success');
                Chat.enableInput();
                Chat.showConnectedInsights(data.schema);
            } else {
                showError(data.error || 'Connection failed.');
            }
        } catch (err) {
            showError('Could not reach the server. Please verify Flask is running.');
        } finally {
            if (btnText) btnText.style.display = 'inline';
            if (btnLoader) btnLoader.style.display = 'none';
            els.submitBtn.disabled = false;
        }
    }

    function showError(msg) {
        if (!els.connectError) return;
        els.connectError.textContent = msg;
        els.connectError.style.display = 'block';
    }

    function setConnected(schema) {
        if (els.connectionStatus) {
            els.connectionStatus.className = 'connection-status connection-status--connected';
            const statusText = els.connectionStatus.querySelector('.connection-status__text');
            if (statusText) {
                statusText.textContent = schema.database_name;
            }
        }

        if (els.btnConnect) els.btnConnect.style.display = 'none';
        if (els.btnDisconnect) els.btnDisconnect.style.display = '';

        const mlTools = document.getElementById('ml-tools');
        if (mlTools) mlTools.style.display = 'block';

        renderSchemaTree(schema);

        // Update "Try:" query suggestions in bottom dock
        const tableNames = Object.keys(schema.tables || {});
        Chat.updateTrySuggestions(tableNames);

        if (window.AnomalyScanner) {
            window.AnomalyScanner.onConnect(tableNames);
        }
    }

    function setDisconnected() {
        if (els.connectionStatus) {
            els.connectionStatus.className = 'connection-status connection-status--disconnected';
            const statusText = els.connectionStatus.querySelector('.connection-status__text');
            if (statusText) statusText.textContent = 'Not connected';
        }

        if (els.btnConnect) els.btnConnect.style.display = '';
        if (els.btnDisconnect) els.btnDisconnect.style.display = 'none';
        if (els.schemaExplorer) els.schemaExplorer.style.display = 'none';
        if (els.schemaTree) els.schemaTree.innerHTML = '';

        const mlTools = document.getElementById('ml-tools');
        if (mlTools) mlTools.style.display = 'none';

        if (window.AnomalyScanner) window.AnomalyScanner.onDisconnect();
        if (Chat.resetEmptyState) Chat.resetEmptyState();
    }

    async function disconnect() {
        try {
            await fetch('/api/disconnect', { method: 'POST' });
        } catch (_) {}
        setDisconnected();
        Chat.disableInput();
        Chat.addAssistantMessage('Disconnected. Connect a database to continue.');
        App.toast('Disconnected', 'info');
    }

    async function refreshSchema() {
        try {
            const res = await fetch('/api/schema');
            const data = await res.json();
            if (data.success) {
                renderSchemaTree(data.schema);
                App.toast('Schema refreshed', 'success');
            }
        } catch (_) {
            App.toast('Failed to refresh schema', 'error');
        }
    }

    async function viewTableData(tableName) {
        if (!els.dataViewerModal) return;
        els.dataViewerTitle.textContent = tableName;
        els.dataViewerContent.innerHTML = '';
        els.dataViewerLoader.style.display = 'block';
        els.dataViewerModal.style.display = 'flex';

        try {
            const res = await fetch(`/api/table_data?table=${encodeURIComponent(tableName)}`);
            const data = await res.json();
            els.dataViewerLoader.style.display = 'none';

            if (data.success && data.data && data.data.rows && data.data.rows.length > 0) {
                const tableEl = Visualization.renderTable(data.data);
                els.dataViewerContent.appendChild(tableEl);
            } else {
                els.dataViewerContent.innerHTML = '<div style="font-size: var(--text-xs); color: var(--mute); padding: 12px 0;">No rows found in this table.</div>';
            }
        } catch (_) {
            els.dataViewerLoader.style.display = 'none';
            els.dataViewerContent.innerHTML = '<div class="safety-statement--bad">Could not fetch table rows.</div>';
        }
    }

    function closeDataViewer() {
        if (els.dataViewerModal) els.dataViewerModal.style.display = 'none';
    }

    /**
     * Render inline table list (table names with row counts, quiet preview on click).
     */
    function renderSchemaTree(schema) {
        if (!els.schemaTree) return;
        els.schemaTree.innerHTML = '';

        const container = document.createElement('div');
        container.style.cssText = 'display: flex; flex-direction: column;';

        for (const [tableName, tableInfo] of Object.entries(schema.tables || {})) {
            const row = document.createElement('div');
            row.className = 'table-item';
            row.innerHTML = `
                <span class="table-item__name">${tableName}</span>
                <span class="table-item__count">${tableInfo.row_count} rows</span>
            `;

            // Clicking opens quiet table preview
            row.addEventListener('click', () => {
                viewTableData(tableName);
            });

            container.appendChild(row);
        }

        els.schemaTree.appendChild(container);
    }

    return {
        init,
        openModal,
        closeModal,
        setConnected,
        setDisconnected,
        viewTableData,
        closeDataViewer
    };
})();
