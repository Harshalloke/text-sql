/**
 * anomaly.js — ML Anomaly & Outlier Detection
 * CALM Design: Short written findings with one minimal chart underneath
 * and a link to see the rows. No dashboard widgets.
 */

(function () {
    "use strict";

    let currentTableNames = [];
    let currentTableName = null;
    let isScanning = false;

    const btnScan       = document.getElementById("btn-scan-anomaly");
    const btnScanText   = document.getElementById("btn-scan-anomaly-text");
    const modal         = document.getElementById("anomaly-modal");
    const backdrop      = document.getElementById("anomaly-backdrop");
    const closeBtn      = document.getElementById("anomaly-close");
    const summaryEl     = document.getElementById("anomaly-summary");
    const resultsEl     = document.getElementById("anomaly-results");
    const loadingEl     = document.getElementById("anomaly-loading");
    const tablePicker   = document.getElementById("anomaly-table-picker");
    const tableSelect   = document.getElementById("anomaly-table-select");
    const btnRunOnTable = document.getElementById("btn-run-on-table");

    window.AnomalyScanner = {
        onConnect: function (tableNames) {
            currentTableNames = tableNames || [];
            currentTableName = currentTableNames[0] || null;
            populateTablePicker();
        },
        onDisconnect: function () {
            currentTableNames = [];
            currentTableName = null;
        }
    };

    function populateTablePicker() {
        if (!tablePicker) return;
        tablePicker.innerHTML = "";
        currentTableNames.forEach(function (name) {
            const opt = document.createElement("option");
            opt.value = name;
            opt.textContent = name;
            tablePicker.appendChild(opt);
        });
        if (currentTableNames.length > 1 && tableSelect) {
            tableSelect.style.display = "flex";
        }
    }

    if (btnScan) {
        btnScan.addEventListener("click", function () {
            if (isScanning) return;
            openModal();
            runScan(currentTableName);
        });
    }

    if (backdrop) backdrop.addEventListener("click", closeModal);
    if (closeBtn) closeBtn.addEventListener("click", closeModal);

    if (btnRunOnTable) {
        btnRunOnTable.addEventListener("click", function () {
            currentTableName = tablePicker.value;
            runScan(currentTableName);
        });
    }

    if (tablePicker) {
        tablePicker.addEventListener("change", function () {
            currentTableName = tablePicker.value;
        });
    }

    function openModal() {
        if (!modal) return;
        modal.style.display = "flex";
        if (summaryEl) summaryEl.innerHTML = "";
        if (loadingEl) loadingEl.style.display = "block";
    }

    function closeModal() {
        if (!modal) return;
        modal.style.display = "none";
    }

    function runScan(tableName) {
        if (!tableName) {
            showError("No table available to scan.");
            return;
        }

        isScanning = true;
        if (btnScanText) btnScanText.textContent = "Scanning...";
        if (loadingEl) loadingEl.style.display = "block";
        if (summaryEl) summaryEl.innerHTML = "";

        fetch("/api/anomaly", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ table: tableName, contamination: 0.1 })
        })
        .then(function (res) { return res.json(); })
        .then(function (data) {
            isScanning = false;
            if (btnScanText) btnScanText.textContent = "Scan anomalies";
            if (loadingEl) loadingEl.style.display = "none";

            if (!data.success) {
                showError(data.error || "Anomaly detection could not complete.");
                return;
            }
            renderCalmFindings(data);
        })
        .catch(function (err) {
            isScanning = false;
            if (btnScanText) btnScanText.textContent = "Scan anomalies";
            if (loadingEl) loadingEl.style.display = "none";
            showError("Scan failed: " + err.message);
        });
    }

    function renderCalmFindings(data) {
        const rows = data.rows || [];
        const anomalies = rows.filter(r => r._is_anomaly === 1);
        const anomalyPct = data.total_rows > 0
            ? ((anomalies.length / data.total_rows) * 100).toFixed(1)
            : 0;

        let primaryFinding = '';
        if (anomalies.length === 0) {
            primaryFinding = `Scanned ${data.total_rows} rows in ${data.table_name}. No significant outliers detected.`;
        } else {
            const first = anomalies[0];
            const keyCols = data.numeric_cols_used || [];
            const colName = keyCols[0] || 'value';
            const val = first[colName];
            primaryFinding = `Found ${anomalies.length} unusual record(s) out of ${data.total_rows} in ${data.table_name} (${anomalyPct}%). Row 1 has ${colName} = ${val}, scoring highest on deviation.`;
        }

        summaryEl.innerHTML = `
            <div class="finding-box">
                <p class="finding-statement">${primaryFinding}</p>
                <div class="finding-chart" style="height: 180px; position: relative;">
                    <canvas id="anomaly-calm-chart"></canvas>
                </div>
                <div style="margin-top: 12px; display: flex; justify-content: space-between; align-items: baseline;">
                    <button type="button" class="finding-link" id="btn-toggle-anomaly-rows">See matching rows (${anomalies.length})</button>
                    <span style="font-size: var(--text-xs); color: var(--mute);">Isolation Forest + LOF</span>
                </div>
            </div>
        `;

        // Render minimal bar chart of anomaly score distribution
        requestAnimationFrame(() => {
            const canvas = document.getElementById("anomaly-calm-chart");
            if (!canvas) return;

            const style = getComputedStyle(document.documentElement);
            const accent = style.getPropertyValue('--accent').trim() || '#2F6B57';
            const line = style.getPropertyValue('--line').trim() || '#DDE0DB';
            const mute = style.getPropertyValue('--mute').trim() || '#7A8085';

            const topSample = rows.slice(0, 15);
            const labels = topSample.map((_, i) => `#${i + 1}`);
            const scores = topSample.map(r => r._anomaly_score);
            const bgColors = topSample.map(r => r._is_anomaly === 1 ? accent : line);

            new Chart(canvas, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        data: scores,
                        backgroundColor: bgColors,
                        borderWidth: 0,
                        borderRadius: 0,
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false },
                        tooltip: { enabled: true }
                    },
                    scales: {
                        x: {
                            ticks: { color: mute, font: { family: 'Onest', size: 11 } },
                            grid: { display: false }
                        },
                        y: {
                            ticks: { color: mute, font: { family: 'Onest', size: 11 } },
                            grid: { color: line }
                        }
                    }
                }
            });
        });

        // Toggle rows viewer
        const toggleBtn = document.getElementById("btn-toggle-anomaly-rows");
        if (toggleBtn) {
            toggleBtn.addEventListener("click", () => {
                if (anomalies.length > 0) {
                    Database.viewTableData(data.table_name);
                    closeModal();
                }
            });
        }
    }

    function showError(msg) {
        if (!summaryEl) return;
        summaryEl.innerHTML = `<p class="safety-statement--bad" style="font-size: var(--text-sm);">${msg}</p>`;
    }
})();
