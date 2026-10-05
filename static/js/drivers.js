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
    
    if(!btnAnalyzeDrivers) return;

    let currentSchema = null;

    // Open Modal
    btnAnalyzeDrivers.addEventListener('click', async () => {
        driversModal.style.display = 'flex';
        driversContent.style.display = 'none';
        driversContent.innerHTML = '';
        
        // Fetch schema to populate dropdowns
        try {
            const res = await fetch('/api/schema');
            const data = await res.json();
            if(data.success) {
                currentSchema = data.schema;
                populateTablePicker();
            }
        } catch(e) {
            console.error(e);
        }
    });

    const closeModal = () => {
        driversModal.style.display = 'none';
    };
    driversClose.addEventListener('click', closeModal);
    driversBackdrop.addEventListener('click', closeModal);

    function populateTablePicker() {
        if(!currentSchema || !currentSchema.tables) return;
        tablePicker.innerHTML = '';
        Object.keys(currentSchema.tables).forEach(table => {
            const opt = document.createElement('option');
            opt.value = table;
            opt.textContent = table;
            tablePicker.appendChild(opt);
        });
        
        if(tablePicker.options.length > 0) {
            populateTargetPicker(tablePicker.value);
        }
    }

    tablePicker.addEventListener('change', (e) => {
        populateTargetPicker(e.target.value);
    });

    function populateTargetPicker(tableName) {
        if(!currentSchema || !currentSchema.tables || !currentSchema.tables[tableName]) return;
        targetPicker.innerHTML = '';
        
        const cols = currentSchema.tables[tableName].columns;
        cols.forEach(col => {
            const opt = document.createElement('option');
            opt.value = col.name;
            opt.textContent = col.name;
            targetPicker.appendChild(opt);
        });
    }

    btnRunDrivers.addEventListener('click', async () => {
        const table = tablePicker.value;
        const target = targetPicker.value;
        if(!table || !target) return;

        driversContent.style.display = 'none';
        driversLoading.style.display = 'flex';
        
        try {
            const res = await fetch('/api/drivers', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ table, target })
            });
            const data = await res.json();
            
            driversLoading.style.display = 'none';
            
            if(!data.success) {
                driversContent.style.display = 'block';
                driversContent.innerHTML = `<div class="anomaly-error">Error: ${data.error}</div>`;
                return;
            }
            
            renderDrivers(data);
        } catch(e) {
            driversLoading.style.display = 'none';
            driversContent.style.display = 'block';
            driversContent.innerHTML = `<div class="anomaly-error">Network error.</div>`;
        }
    });

    function renderDrivers(data) {
        driversContent.style.display = 'block';
        
        if(!data.drivers || data.drivers.length === 0) {
            driversContent.innerHTML = `<div style="text-align:center; padding: 30px; color: var(--text-tertiary);">No meaningful drivers found.</div>`;
            return;
        }

        let html = `
            <div style="margin-bottom: 20px; font-size: 0.85rem; color: var(--text-secondary);">
                Analyzed <strong>${data.total_rows_analyzed}</strong> rows to find what drives <strong>${data.target_column}</strong>.
            </div>
            <div style="display: flex; flex-direction: column; gap: 12px;">
        `;

        data.drivers.forEach(d => {
            const pct = d.importance_percent;
            html += `
                <div class="driver-row">
                    <div style="display:flex; justify-content:space-between; margin-bottom: 6px;">
                        <span style="font-family: var(--font-heading); font-weight: 600; font-size: 0.85rem; color: #fff;">${d.column}</span>
                        <span style="font-family: var(--font-mono); font-size: 0.8rem; color: #93c5fd;">${pct}%</span>
                    </div>
                    <div style="width: 100%; background: rgba(255,255,255,0.05); height: 8px; border-radius: 4px; overflow: hidden;">
                        <div style="width: ${pct}%; background: linear-gradient(90deg, #60a5fa, #3b82f6); height: 100%; border-radius: 4px; transition: width 1s ease-out;"></div>
                    </div>
                </div>
            `;
        });

        html += `</div>`;
        driversContent.innerHTML = html;
    }
});
