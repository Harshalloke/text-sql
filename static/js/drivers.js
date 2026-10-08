/**
 * drivers.js — Key-Driver Analysis Frontend
 * CALM Design: Short written findings with one minimal chart underneath
 * and a link to see the rows.
 */

document.addEventListener('DOMContentLoaded', () => {
    const btnAnalyzeDrivers = document.getElementById('btn-analyze-drivers');
    const driversModal = document.getElementById('drivers-modal');
    const driversClose = document.getElementById('drivers-close');
    const driversBackdrop = document.getElementById('drivers-backdrop');

    const tablePicker = document.getElementById('drivers-table-picker');
    const targetPicker = document.getElementById('drivers-target-picker');
    const btnRunDrivers = document.getElementById('btn-run-drivers');

    const driversLoading = document.getElementById('drivers-loading');
    const driversContent = document.getElementById('drivers-content');

    if (!btnAnalyzeDrivers) return;

    let currentSchema = null;

    btnAnalyzeDrivers.addEventListener('click', async () => {
        driversModal.style.display = 'flex';
        driversContent.style.display = 'none';
        driversContent.innerHTML = '';

        try {
            const res = await fetch('/api/schema');
            const data = await res.json();
            if (data.success) {
                currentSchema = data.schema;
                populateTablePicker();
            }
        } catch (_) {}
    });

    const closeModal = () => {
        if (driversModal) driversModal.style.display = 'none';
    };

    if (driversClose) driversClose.addEventListener('click', closeModal);
    if (driversBackdrop) driversBackdrop.addEventListener('click', closeModal);

    function populateTablePicker() {
        if (!currentSchema || !currentSchema.tables) return;
        tablePicker.innerHTML = '';
        Object.keys(currentSchema.tables).forEach(table => {
            const opt = document.createElement('option');
            opt.value = table;
            opt.textContent = table;
            tablePicker.appendChild(opt);
        });

        if (tablePicker.options.length > 0) {
            populateTargetPicker(tablePicker.value);
        }
    }

    if (tablePicker) {
        tablePicker.addEventListener('change', (e) => {
            populateTargetPicker(e.target.value);
        });
    }

    function populateTargetPicker(tableName) {
        if (!currentSchema || !currentSchema.tables || !currentSchema.tables[tableName]) return;
        targetPicker.innerHTML = '';

        const cols = currentSchema.tables[tableName].columns;
        cols.forEach(col => {
            const opt = document.createElement('option');
            opt.value = col.name;
            opt.textContent = col.name;
            targetPicker.appendChild(opt);
        });
    }

    if (btnRunDrivers) {
        btnRunDrivers.addEventListener('click', async () => {
            const table = tablePicker.value;
            const target = targetPicker.value;
            if (!table || !target) return;

            driversContent.style.display = 'none';
            if (driversLoading) driversLoading.style.display = 'block';

            try {
                const res = await fetch('/api/drivers', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ table, target })
                });
                const data = await res.json();

                if (driversLoading) driversLoading.style.display = 'none';

                if (!data.success) {
                    driversContent.style.display = 'block';
                    driversContent.innerHTML = `<p class="safety-statement--bad">${data.error || 'Could not analyze drivers.'}</p>`;
                    return;
                }

                renderDrivers(data, table);
            } catch (_) {
                if (driversLoading) driversLoading.style.display = 'none';
                driversContent.style.display = 'block';
                driversContent.innerHTML = '<p class="safety-statement--bad">Network error during analysis.</p>';
            }
        });
    }

    function renderDrivers(data, tableName) {
        driversContent.style.display = 'block';

        if (!data.drivers || data.drivers.length === 0) {
            driversContent.innerHTML = '<p style="color:var(--mute);font-size:var(--text-xs);padding:12px 0;">No significant drivers identified.</p>';
            return;
        }

        const top = data.drivers[0];
        const findingText = `"${top.column}" is the primary driver of ${data.target_column}, accounting for ${top.importance_percent}% of variance across ${data.total_rows_analyzed} rows.`;

        let barsHtml = '';
        data.drivers.slice(0, 5).forEach((d, i) => {
            const isPrimary = i === 0;
            const colorVar = isPrimary ? 'var(--accent)' : 'var(--mute)';
            barsHtml += `
                <div style="display: flex; flex-direction: column; gap: 4px; font-size: var(--text-xs);">
                    <div style="display: flex; justify-content: space-between;">
                        <span style="color: var(--ink); font-weight: ${isPrimary ? '400' : '300'};">${d.column}</span>
                        <span style="color: var(--mute); font-variant-numeric: tabular-nums;">${d.importance_percent}%</span>
                    </div>
                    <div style="width: 100%; height: 4px; background: var(--line);">
                        <div style="width: ${d.importance_percent}%; height: 100%; background: ${colorVar};"></div>
                    </div>
                </div>
            `;
        });

        driversContent.innerHTML = `
            <div class="finding-box">
                <p class="finding-statement">${findingText}</p>
                <div style="display: flex; flex-direction: column; gap: 12px; margin: 16px 0;">
                    ${barsHtml}
                </div>
                <div style="display: flex; justify-content: space-between; align-items: baseline; margin-top: 14px;">
                    <button type="button" class="finding-link" id="btn-drivers-view-table">View rows for ${tableName}</button>
                    <span style="font-size: var(--text-xs); color: var(--mute);">Random Forest Feature Importances</span>
                </div>
            </div>
        `;

        const viewTableBtn = document.getElementById('btn-drivers-view-table');
        if (viewTableBtn) {
            viewTableBtn.addEventListener('click', () => {
                Database.viewTableData(tableName);
                closeModal();
            });
        }
    }
});
