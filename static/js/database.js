/**
 * Database Connection Module
 * Handles the connect modal, DB type switching, and schema tree rendering.
 */

const Database = (() => {
    // --- DOM references ---
    const els = {};
    let currentDbType = 'sqlite';

    function init() {
        // Cache elements
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
        els.connectForm = document.getElementById('connect-form');
        els.connectError = document.getElementById('connect-error');
        els.connectionStatus = document.getElementById('connection-status');
        els.schemaExplorer = document.getElementById('schema-explorer');
        els.schemaTree = document.getElementById('schema-tree');
        els.submitBtn = document.getElementById('btn-submit-connect');

        // DB type tabs
        els.dbTabs = document.querySelectorAll('.db-tab');
        els.formSqlite = document.getElementById('form-sqlite');
        els.formMysql = document.getElementById('form-mysql');
        els.formPostgresql = document.getElementById('form-postgresql');

        // Modal Top Tabs
        els.modalTabs = document.querySelectorAll('.modal-tab');
        els.uploadForm = document.getElementById('upload-form');
        els.connectDbContainer = document.getElementById('connect-db-container');

        // Drop Zone
        els.dropZone = document.getElementById('drop-zone');
        els.fileInput = document.getElementById('file-input');
        els.dropZonePrompt = els.dropZone.querySelector('.drop-zone__prompt');
        els.btnSubmitUpload = document.getElementById('btn-submit-upload');

        // Events
        els.btnConnect.addEventListener('click', openModal);
        els.btnCloseModal.addEventListener('click', closeModal);
        els.btnCancelConnect.addEventListener('click', closeModal);
        els.modalBackdrop.addEventListener('click', closeModal);
        els.btnDisconnect.addEventListener('click', disconnect);
        els.connectForm.addEventListener('submit', handleConnect);
        els.btnRefreshSchema.addEventListener('click', refreshSchema);
        
        // Data viewer events
        els.dataViewerClose.addEventListener('click', closeDataViewer);
        els.dataViewerBackdrop.addEventListener('click', closeDataViewer);

        els.dbTabs.forEach(tab => {
            tab.addEventListener('click', () => switchDbType(tab.dataset.type));
        });

        // Modal top tabs
        els.modalTabs.forEach(tab => {
            tab.addEventListener('click', () => switchModalTab(tab.dataset.tab));
        });

        // Drop zone events
        els.fileInput.addEventListener('change', handleFileSelect);
        els.dropZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            els.dropZone.classList.add('drop-zone--over');
        });
        els.dropZone.addEventListener('dragleave', () => {
            els.dropZone.classList.remove('drop-zone--over');
        });
        els.dropZone.addEventListener('drop', (e) => {
            e.preventDefault();
            els.dropZone.classList.remove('drop-zone--over');
            if (e.dataTransfer.files.length) {
                els.fileInput.files = e.dataTransfer.files;
                handleFileSelect();
            }
        });
        els.uploadForm.addEventListener('submit', handleUpload);
    }

    function switchModalTab(tabName) {
        els.modalTabs.forEach(t => t.classList.remove('active'));
        document.querySelector(`.modal-tab[data-tab="${tabName}"]`).classList.add('active');

        if (tabName === 'upload') {
            els.connectForm.style.display = 'none';
            els.connectDbContainer.style.display = 'none';
            els.uploadForm.style.display = 'block';
        } else {
            els.uploadForm.style.display = 'none';
            els.connectForm.style.display = 'block';
            els.connectDbContainer.style.display = 'block';
        }
    }

    function handleFileSelect() {
        if (els.fileInput.files.length > 0) {
            els.dropZonePrompt.textContent = els.fileInput.files[0].name;
            els.btnSubmitUpload.disabled = false;
        } else {
            els.dropZonePrompt.textContent = "Drag & Drop CSV or Excel file here or click to browse";
            els.btnSubmitUpload.disabled = true;
        }
    }

    async function handleUpload(e) {
        e.preventDefault();
        
        if (!els.fileInput.files.length) return;
        
        const file = els.fileInput.files[0];
        const formData = new FormData();
        formData.append('file', file);

        els.connectError.style.display = 'none';
        
        // UI loading state
        els.btnSubmitUpload.disabled = true;
        els.btnSubmitUpload.querySelector('.btn__text').style.display = 'none';
        els.btnSubmitUpload.querySelector('.btn__loader').style.display = 'inline-flex';

        try {
            const res = await fetch('/api/upload', {
                method: 'POST',
                body: formData
            });

            const data = await res.json();
            
            if (data.success) {
                closeModal();
                setConnected(data.schema);
                App.toast('File uploaded and database connected successfully!');
                Chat.fetchInsights();
                Chat.enableInput();
            } else {
                showError(data.error || 'Upload failed');
            }
        } catch (err) {
            showError('Network error during upload');
        } finally {
            // Reset UI
            els.btnSubmitUpload.disabled = false;
            els.btnSubmitUpload.querySelector('.btn__text').style.display = 'inline';
            els.btnSubmitUpload.querySelector('.btn__loader').style.display = 'none';
        }
    }

    function openModal() {
        els.modal.style.display = 'flex';
        els.connectError.style.display = 'none';
        // Focus first input
        setTimeout(() => {
            const visibleForm = document.querySelector('.connect-form__fields:not([style*="display: none"]) input');
            if (visibleForm) visibleForm.focus();
        }, 100);
    }

    function closeModal() {
        els.modal.style.display = 'none';
    }

    function switchDbType(type) {
        currentDbType = type;
        els.dbTabs.forEach(t => t.classList.toggle('db-tab--active', t.dataset.type === type));
        els.formSqlite.style.display = type === 'sqlite' ? '' : 'none';
        els.formMysql.style.display = type === 'mysql' ? '' : 'none';
        els.formPostgresql.style.display = type === 'postgresql' ? '' : 'none';
        els.connectError.style.display = 'none';
    }

    async function handleConnect(e) {
        e.preventDefault();
        els.connectError.style.display = 'none';

        // Show loader
        const btnText = els.submitBtn.querySelector('.btn__text');
        const btnLoader = els.submitBtn.querySelector('.btn__loader');
        btnText.style.display = 'none';
        btnLoader.style.display = 'inline-flex';
        els.submitBtn.disabled = true;

        // Build payload
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
                App.toast('Connected to database!', 'success');
                Chat.fetchInsights();
                Chat.enableInput();
            } else {
                showError(data.error || 'Connection failed.');
            }
        } catch (err) {
            showError('Could not reach the server. Is it running?');
        } finally {
            btnText.style.display = '';
            btnLoader.style.display = 'none';
            els.submitBtn.disabled = false;
        }
    }

    function showError(msg) {
        els.connectError.textContent = msg;
        els.connectError.style.display = 'block';
    }

    function setConnected(schema) {
        els.connectionStatus.className = 'connection-status connection-status--connected';
        els.connectionStatus.querySelector('.connection-status__text').textContent =
            `${schema.database_name} (${schema.database_type})`;
        els.btnConnect.style.display = 'none';
        els.btnDisconnect.style.display = '';
        els.schemaExplorer.style.display = '';
        const mlTools = document.getElementById('ml-tools');
        if (mlTools) mlTools.style.display = 'block';
        renderSchemaTree(schema);
    }

    function setDisconnected() {
        els.connectionStatus.className = 'connection-status connection-status--disconnected';
        els.connectionStatus.querySelector('.connection-status__text').textContent = 'Not connected';
        els.btnConnect.style.display = '';
        els.btnDisconnect.style.display = 'none';
        els.schemaExplorer.style.display = 'none';
        els.schemaTree.innerHTML = '';
        const mlTools = document.getElementById('ml-tools');
        if (mlTools) mlTools.style.display = 'none';
        if (window.AnomalyScanner) AnomalyScanner.onDisconnect();
    }

    async function disconnect() {
        try {
            await fetch('/api/disconnect', { method: 'POST' });
        } catch (_) { /* ignore */ }
        setDisconnected();
        Chat.disableInput();
        Chat.addAssistantMessage('Disconnected from database. Connect a new database to continue.');
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
        } catch (err) {
            App.toast('Failed to refresh schema', 'error');
        }
    }

    async function viewTableData(tableName) {
        els.dataViewerTitle.textContent = `Data: ${tableName}`;
        els.dataViewerContent.innerHTML = '';
        els.dataViewerLoader.style.display = 'flex';
        els.dataViewerModal.style.display = 'flex';

        try {
            const res = await fetch(`/api/table_data?table=${encodeURIComponent(tableName)}`);
            const data = await res.json();
            
            els.dataViewerLoader.style.display = 'none';

            if (data.success) {
                if (data.data && data.data.rows && data.data.rows.length > 0) {
                    const tableEl = Visualization.renderTable(data.data);
                    els.dataViewerContent.appendChild(tableEl);
                } else {
                    els.dataViewerContent.innerHTML = '<div style="padding: 20px; text-align: center; color: var(--text-tertiary);">No data found in this table.</div>';
                }
            } else {
                els.dataViewerContent.innerHTML = `<div style="padding: 20px; color: var(--accent-danger);">${data.error || 'Failed to load data.'}</div>`;
            }
        } catch (err) {
            els.dataViewerLoader.style.display = 'none';
            els.dataViewerContent.innerHTML = '<div style="padding: 20px; color: var(--accent-danger);">Network error while fetching data.</div>';
        }
    }

    function closeDataViewer() {
        els.dataViewerModal.style.display = 'none';
    }

    function renderSchemaTree(schema) {
        els.schemaTree.innerHTML = '';

        for (const [tableName, tableInfo] of Object.entries(schema.tables)) {
            const tableEl = document.createElement('div');
            tableEl.className = 'schema-table';

            const header = document.createElement('div');
            header.className = 'schema-table__header';
            header.innerHTML = `
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="9" y1="21" x2="9" y2="9"/></svg>
                <span class="schema-table__name">${tableName}</span>
                <span class="schema-table__count">${tableInfo.row_count}</span>
                <button class="btn btn--icon schema-table__action" title="View Table Data" onclick="event.stopPropagation(); Database.viewTableData('${tableName}');">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
                </button>
                <svg class="schema-table__chevron" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 18l6-6-6-6"/></svg>
            `;

            header.addEventListener('click', () => tableEl.classList.toggle('expanded'));

            const columns = document.createElement('div');
            columns.className = 'schema-table__columns';

            for (const col of tableInfo.columns) {
                const colEl = document.createElement('div');
                colEl.className = 'schema-column';
                const isPk = tableInfo.primary_keys.includes(col.name);
                colEl.innerHTML = `
                    <span>${col.name}</span>
                    ${isPk ? '<span class="schema-column__pk">PK</span>' : ''}
                    <span class="schema-column__type">${col.type}</span>
                `;
                columns.appendChild(colEl);
            }

            tableEl.appendChild(header);
            tableEl.appendChild(columns);
            els.schemaTree.appendChild(tableEl);
        }
        // Notify AnomalyScanner of available tables
        const tableNames = Object.keys(schema.tables);
        if (window.AnomalyScanner) AnomalyScanner.onConnect(tableNames);
    }

    return { init, openModal, closeModal, setConnected, setDisconnected, viewTableData };
})();
