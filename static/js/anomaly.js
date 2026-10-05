/**
 * anomaly.js — ML Anomaly & Outlier Detection Frontend
 * Handles the "Scan for ML Anomalies" button and renders the results modal.
 * Communicates with /api/anomaly — 100% local ML, no Gemini API.
 */

(function () {
    "use strict";

    // -----------------------------------------------------------------------
    // State
    // -----------------------------------------------------------------------
    let currentTableNames = [];    // All available tables from DB schema
    let currentTableName = null;   // Currently selected table to analyze
    let isScanning = false;

    // -----------------------------------------------------------------------
    // DOM References
    // -----------------------------------------------------------------------
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

    // -----------------------------------------------------------------------
    // Bootstrap — expose API for database.js to call on connection
    // -----------------------------------------------------------------------
    window.AnomalyScanner = {
        onConnect: function (tableNames) {
            currentTableNames = tableNames || [];
            const mlTools = document.getElementById("ml-tools");
            if (mlTools) mlTools.style.display = "block";
            // Default to first table
            currentTableName = currentTableNames[0] || null;
            populateTablePicker();
        },
        onDisconnect: function () {
            const mlTools = document.getElementById("ml-tools");
            if (mlTools) mlTools.style.display = "none";
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
        if (currentTableNames.length > 1) {
            tableSelect.style.display = "flex";
        }
    }

    // -----------------------------------------------------------------------
    // Event Listeners
    // -----------------------------------------------------------------------
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

    // -----------------------------------------------------------------------
    // Modal Controls
    // -----------------------------------------------------------------------
    function openModal() {
        if (!modal) return;
        modal.style.display = "flex";
        document.body.style.overflow = "hidden";
        summaryEl.innerHTML = "";
        showLoading(true);
    }

    function closeModal() {
        if (!modal) return;
        modal.style.display = "none";
        document.body.style.overflow = "";
    }

    // -----------------------------------------------------------------------
    // Core Scan Function
    // -----------------------------------------------------------------------
    function runScan(tableName) {
        if (!tableName) {
            showError("No table selected. Please connect a database first.");
            return;
        }

        isScanning = true;
        if (btnScanText) btnScanText.textContent = "Scanning...";
        if (btnScan) btnScan.disabled = true;
        showLoading(true);
        summaryEl.innerHTML = "";

        fetch("/api/anomaly", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ table: tableName, contamination: 0.1 })
        })
        .then(function (res) { return res.json(); })
        .then(function (data) {
            isScanning = false;
            if (btnScanText) btnScanText.textContent = "Scan for ML Anomalies";
            if (btnScan) btnScan.disabled = false;
            showLoading(false);

            if (!data.success) {
                showError(data.error || "Analysis failed.");
                return;
            }
            renderResults(data);
        })
        .catch(function (err) {
            isScanning = false;
            if (btnScanText) btnScanText.textContent = "Scan for ML Anomalies";
            if (btnScan) btnScan.disabled = false;
            showLoading(false);
            showError("Network error: " + err.message);
        });
    }

    // -----------------------------------------------------------------------
    // Render Results
    // -----------------------------------------------------------------------
    function renderResults(data) {
        // --- Summary Cards ---
        const anomalyPct = data.total_rows > 0
            ? ((data.anomaly_count / data.total_rows) * 100).toFixed(1)
            : 0;

        summaryEl.innerHTML = `
            <div class="anomaly-stat anomaly-stat--total">
                <div class="anomaly-stat__val">${data.total_rows}</div>
                <div class="anomaly-stat__label">Total Rows</div>
            </div>
            <div class="anomaly-stat anomaly-stat--clean">
                <div class="anomaly-stat__val">${data.normal_count}</div>
                <div class="anomaly-stat__label">Normal</div>
            </div>
            <div class="anomaly-stat anomaly-stat--flag">
                <div class="anomaly-stat__val">${data.anomaly_count}</div>
                <div class="anomaly-stat__label">Anomalies Found</div>
            </div>
            <div class="anomaly-stat anomaly-stat--pct">
                <div class="anomaly-stat__val">${anomalyPct}%</div>
                <div class="anomaly-stat__label">Anomaly Rate</div>
            </div>
            <div class="anomaly-meta">
                <div class="anomaly-meta__item">
                    <span class="anomaly-meta__key">Models Used</span>
                    <span class="anomaly-meta__val">${(data.summary.models_used || []).join(" + ")}</span>
                </div>
                <div class="anomaly-meta__item">
                    <span class="anomaly-meta__key">Numeric Columns Analyzed</span>
                    <span class="anomaly-meta__val">${(data.numeric_cols_used || []).join(", ")}</span>
                </div>
                <div class="anomaly-meta__item">
                    <span class="anomaly-meta__key">Table</span>
                    <span class="anomaly-meta__val">${data.table_name}</span>
                </div>
            </div>
        `;

        // --- Build Table ---
        const columns = data.columns || [];
        const rows = data.rows || [];

        if (rows.length === 0) {
            resultsEl.innerHTML = `<p style="color:var(--text-secondary);padding:20px;text-align:center;">No rows to display.</p>`;
            return;
        }

        // Sort: anomalies first, then by score descending
        const sorted = rows.slice().sort(function (a, b) {
            if (b._is_anomaly !== a._is_anomaly) return b._is_anomaly - a._is_anomaly;
            return b._anomaly_score - a._anomaly_score;
        });

        let tableHtml = `
            <div class="anomaly-table-wrap">
                <table class="anomaly-table">
                    <thead>
                        <tr>
                            <th class="anomaly-th--score">Score</th>
                            <th class="anomaly-th--status">Status</th>
                            ${columns.map(function(c){ return `<th>${escHtml(c)}</th>`; }).join("")}
                        </tr>
                    </thead>
                    <tbody>
        `;

        sorted.forEach(function (row) {
            const score = row._anomaly_score || 0;
            const isAnomaly = row._is_anomaly;
            const reasons = row._reasons || [];
            const rowClass = isAnomaly ? "anomaly-row--flagged" : "";
            const scoreClass = score >= 80 ? "score--critical"
                             : score >= 60 ? "score--high"
                             : score >= 40 ? "score--medium"
                             : "score--normal";

            const reasonHtml = (isAnomaly && reasons.length > 0)
                ? `<div class="anomaly-reasons">${reasons.map(function(r){ return `<span class="anomaly-reason">${escHtml(r)}</span>`; }).join("")}</div>`
                : "";

            const badge = isAnomaly
                ? `<span class="anomaly-badge anomaly-badge--flag">⚠ Outlier</span>`
                : `<span class="anomaly-badge anomaly-badge--ok">✓ Normal</span>`;

            const dataCells = columns.map(function (col) {
                const val = row[col];
                return `<td>${val === null || val === undefined ? '<span style="opacity:0.3">null</span>' : escHtml(String(val))}</td>`;
            }).join("");

            tableHtml += `
                <tr class="${rowClass}" title="${isAnomaly && reasons.length ? reasons.join(" · ") : ""}">
                    <td>
                        <div class="anomaly-score-bar">
                            <div class="anomaly-score-fill ${scoreClass}" style="width:${score}%"></div>
                            <span class="anomaly-score-num ${scoreClass}">${score}</span>
                        </div>
                        ${reasonHtml}
                    </td>
                    <td>${badge}</td>
                    ${dataCells}
                </tr>
            `;
        });

        tableHtml += `</tbody></table></div>`;
        resultsEl.innerHTML = tableHtml;
    }

    function showLoading(show) {
        if (!loadingEl) return;
        if (show) {
            loadingEl.style.display = "flex";
            resultsEl.style.display = "block";
        } else {
            loadingEl.style.display = "none";
        }
    }

    function showError(msg) {
        resultsEl.innerHTML = `
            <div class="anomaly-error">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#f87171" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
                <p>${escHtml(msg)}</p>
            </div>`;
    }

    function escHtml(str) {
        return String(str)
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;");
    }

})();
