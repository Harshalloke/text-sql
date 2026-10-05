/**
 * Visualization Module
 * Renders data tables with pagination and Chart.js charts for query results.
 */

const Visualization = (() => {
    const ROWS_PER_PAGE = 25;

    /**
     * Render a data table with pagination.
     * @param {Object} data - { columns: string[], rows: Object[], row_count: number }
     * @returns {HTMLElement}
     */
    function renderTable(data) {
        if (!data || !data.columns || data.columns.length === 0) {
            return createEmptyMessage('No data to display.');
        }

        const wrapper = document.createElement('div');
        wrapper.className = 'data-table-wrapper';

        const table = document.createElement('table');
        table.className = 'data-table';

        // Header
        const thead = document.createElement('thead');
        const headerRow = document.createElement('tr');
        data.columns.forEach(col => {
            const th = document.createElement('th');
            th.textContent = col;
            headerRow.appendChild(th);
        });
        thead.appendChild(headerRow);
        table.appendChild(thead);

        // Body
        const tbody = document.createElement('tbody');
        const rows = data.rows || [];
        const totalPages = Math.ceil(rows.length / ROWS_PER_PAGE);
        let currentPage = 0;

        function renderPage(page) {
            tbody.innerHTML = '';
            const start = page * ROWS_PER_PAGE;
            const end = Math.min(start + ROWS_PER_PAGE, rows.length);

            for (let i = start; i < end; i++) {
                const tr = document.createElement('tr');
                data.columns.forEach(col => {
                    const td = document.createElement('td');
                    const val = rows[i][col];
                    td.textContent = val === null ? 'NULL' : val;
                    td.title = val === null ? 'NULL' : String(val);
                    tr.appendChild(td);
                });
                tbody.appendChild(tr);
            }

            // Update footer
            const footer = wrapper.querySelector('.data-table__footer');
            if (footer) {
                footer.querySelector('.data-table__info').textContent =
                    `Showing ${start + 1}–${end} of ${rows.length} rows`;

                const pagination = footer.querySelector('.data-table__pagination');
                pagination.innerHTML = '';
                if (totalPages > 1) {
                    for (let p = 0; p < Math.min(totalPages, 10); p++) {
                        const btn = document.createElement('button');
                        btn.textContent = p + 1;
                        btn.className = p === page ? 'active' : '';
                        btn.addEventListener('click', () => {
                            currentPage = p;
                            renderPage(p);
                        });
                        pagination.appendChild(btn);
                    }
                    if (totalPages > 10) {
                        const ellipsis = document.createElement('span');
                        ellipsis.textContent = `… ${totalPages}`;
                        ellipsis.style.cssText = 'font-size:0.72rem;color:var(--text-tertiary);padding:0 4px;';
                        pagination.appendChild(ellipsis);
                    }
                }
            }
        }

        table.appendChild(tbody);
        wrapper.appendChild(table);

        // Footer with pagination
        const footer = document.createElement('div');
        footer.className = 'data-table__footer';
        footer.innerHTML = `
            <span class="data-table__info">Showing 1–${Math.min(ROWS_PER_PAGE, rows.length)} of ${rows.length} rows</span>
            <div class="data-table__pagination"></div>
        `;
        wrapper.appendChild(footer);

        renderPage(0);
        return wrapper;
    }

    /**
     * Detect if data is chart-worthy and render a chart if so.
     * @param {Object} data - { columns: string[], rows: Object[] }
     * @returns {HTMLElement|null}
     */
    function renderChart(data) {
        if (!data || !data.columns || data.rows.length < 2 || data.columns.length < 2) {
            return null;
        }

        // Detect chart type based on data structure
        const chartInfo = detectChartType(data);
        if (!chartInfo) return null;

        const container = document.createElement('div');
        container.className = 'chart-container';

        const canvas = document.createElement('canvas');
        container.appendChild(canvas);

        // Render after DOM insertion
        requestAnimationFrame(() => {
            createChart(canvas, chartInfo, data);
        });

        return container;
    }

    function detectChartType(data) {
        const cols = data.columns;
        const rows = data.rows;

        if (cols.length < 2 || rows.length === 0) return null;

        // Check if first column is labels and second+ are numbers
        const labelCol = cols[0];
        const numericCols = cols.slice(1).filter(col => {
            return rows.every(row => {
                const v = row[col];
                return v === null || !isNaN(Number(v));
            });
        });

        if (numericCols.length === 0) return null;

        // Determine chart type
        let type = 'bar';

        // If <= 8 categories and 1 numeric column, use doughnut
        if (rows.length <= 8 && numericCols.length === 1) {
            type = 'doughnut';
        }
        // If many rows, use line
        else if (rows.length > 12) {
            type = 'line';
        }

        // Check for time-like labels
        const isTimeSeries = rows.some(row => {
            const val = String(row[labelCol]);
            return /^\d{4}[-/]/.test(val) || /jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec/i.test(val);
        });

        if (isTimeSeries) type = 'line';

        return { type, labelCol, numericCols };
    }

    function createChart(canvas, chartInfo, data) {
        const { type, labelCol, numericCols } = chartInfo;
        const labels = data.rows.map(r => String(r[labelCol]));

        const colors = [
            'rgba(79, 140, 255, 0.8)',
            'rgba(167, 139, 250, 0.8)',
            'rgba(52, 211, 153, 0.8)',
            'rgba(251, 191, 36, 0.8)',
            'rgba(248, 113, 113, 0.8)',
            'rgba(96, 165, 250, 0.8)',
            'rgba(251, 146, 60, 0.8)',
            'rgba(168, 85, 247, 0.8)',
        ];

        const bgColors = colors.map(c => c.replace('0.8', '0.15'));

        const datasets = numericCols.map((col, i) => {
            const colorIdx = i % colors.length;
            return {
                label: col,
                data: data.rows.map(r => r[col] === null ? 0 : Number(r[col])),
                backgroundColor: type === 'doughnut' ? colors : bgColors[colorIdx],
                borderColor: type === 'doughnut' ? 'rgba(6, 8, 15, 0.8)' : colors[colorIdx],
                borderWidth: type === 'doughnut' ? 2 : 2,
                tension: 0.3,
                fill: type === 'line',
                pointRadius: type === 'line' ? 4 : undefined,
                pointHoverRadius: type === 'line' ? 6 : undefined,
            };
        });

        new Chart(canvas, {
            type,
            data: { labels, datasets },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: numericCols.length > 1 || type === 'doughnut',
                        labels: { color: '#94a3b8', font: { family: 'Inter', size: 11 } },
                    },
                    tooltip: {
                        backgroundColor: 'rgba(15, 20, 40, 0.9)',
                        titleFont: { family: 'Inter' },
                        bodyFont: { family: 'Inter' },
                        borderColor: 'rgba(148, 163, 184, 0.1)',
                        borderWidth: 1,
                    },
                },
                scales: type !== 'doughnut' ? {
                    x: {
                        ticks: { color: '#64748b', font: { family: 'Inter', size: 10 } },
                        grid: { color: 'rgba(148, 163, 184, 0.06)' },
                    },
                    y: {
                        ticks: { color: '#64748b', font: { family: 'Inter', size: 10 } },
                        grid: { color: 'rgba(148, 163, 184, 0.06)' },
                    },
                } : undefined,
            },
        });
    }

    function createEmptyMessage(text) {
        const div = document.createElement('div');
        div.style.cssText = 'text-align:center;padding:16px;color:var(--text-tertiary);font-size:0.85rem;';
        div.textContent = text;
        return div;
    }

    return { renderTable, renderChart };
})();
