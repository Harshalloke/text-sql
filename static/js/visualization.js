/**
 * Visualization Module
 * CALM Design: Borderless tables with hairline separators, staggered row fade-ins,
 * right-aligned numbers, and minimal Chart.js charts styled to design tokens.
 */

const Visualization = (() => {
    const ROWS_PER_PAGE = 25;

    function getThemeTokens() {
        const style = getComputedStyle(document.documentElement);
        return {
            ink: style.getPropertyValue('--ink').trim() || '#1F2326',
            mute: style.getPropertyValue('--mute').trim() || '#7A8085',
            line: style.getPropertyValue('--line').trim() || '#DDE0DB',
            soft: style.getPropertyValue('--soft').trim() || '#E8EAE5',
            accent: style.getPropertyValue('--accent').trim() || '#2F6B57',
            bg: style.getPropertyValue('--bg').trim() || '#F2F3F0'
        };
    }

    /**
     * Render a borderless data table with staggered row fade-in.
     */
    function renderTable(data) {
        if (!data || !data.columns || data.columns.length === 0) {
            return createEmptyMessage('No data to display.');
        }

        const wrapper = document.createElement('div');
        wrapper.className = 'data-table-wrapper';

        const table = document.createElement('table');
        table.className = 'data-table';

        // Check which columns are numeric for right-alignment & tabular-nums
        const rows = data.rows || [];
        const numericCols = new Set();
        data.columns.forEach(col => {
            const hasData = rows.length > 0;
            const allNumeric = hasData && rows.every(r => {
                const val = r[col];
                return val === null || val === '' || !isNaN(Number(val));
            });
            if (allNumeric) numericCols.add(col);
        });

        // Header
        const thead = document.createElement('thead');
        const headerRow = document.createElement('tr');
        data.columns.forEach(col => {
            const th = document.createElement('th');
            th.textContent = col;
            if (numericCols.has(col)) {
                th.classList.add('is-numeric');
            }
            headerRow.appendChild(th);
        });
        thead.appendChild(headerRow);
        table.appendChild(thead);

        // Body
        const tbody = document.createElement('tbody');
        const totalPages = Math.ceil(rows.length / ROWS_PER_PAGE);

        function renderPage(page) {
            tbody.innerHTML = '';
            const start = page * ROWS_PER_PAGE;
            const end = Math.min(start + ROWS_PER_PAGE, rows.length);

            for (let i = start; i < end; i++) {
                const tr = document.createElement('tr');
                // Staggered fade-in (70ms per row)
                tr.style.setProperty('--row-i', i - start);

                data.columns.forEach(col => {
                    const td = document.createElement('td');
                    const val = rows[i][col];
                    td.textContent = val === null ? '—' : val;
                    if (numericCols.has(col)) {
                        td.classList.add('is-numeric');
                    }
                    tr.appendChild(td);
                });
                tbody.appendChild(tr);
            }

            // Update footer info
            const footer = wrapper.querySelector('.data-table__footer');
            if (footer && totalPages > 1) {
                const pagination = footer.querySelector('.data-table__pagination');
                pagination.innerHTML = '';
                for (let p = 0; p < totalPages; p++) {
                    const btn = document.createElement('button');
                    btn.textContent = p + 1;
                    if (p === page) btn.className = 'active';
                    btn.addEventListener('click', () => renderPage(p));
                    pagination.appendChild(btn);
                }
            }
        }

        table.appendChild(tbody);
        wrapper.appendChild(table);

        if (totalPages > 1) {
            const footer = document.createElement('div');
            footer.className = 'data-table__footer';
            footer.innerHTML = `
                <span>Showing 1–${Math.min(ROWS_PER_PAGE, rows.length)} of ${rows.length}</span>
                <div class="data-table__pagination"></div>
            `;
            wrapper.appendChild(footer);
        }

        renderPage(0);
        return wrapper;
    }

    /**
     * Render Chart.js chart adhering strictly to CALM tokens.
     */
    function renderChart(data, forcedType = null) {
        if (!data || !data.columns || data.rows.length < 1 || data.columns.length < 2) {
            return null;
        }

        const chartInfo = detectChartType(data);
        if (!chartInfo) return null;

        const effectiveType = forcedType || chartInfo.type;

        const container = document.createElement('div');
        container.className = 'chart-container';

        const canvas = document.createElement('canvas');
        container.appendChild(canvas);

        requestAnimationFrame(() => {
            createCalmChart(canvas, { ...chartInfo, type: effectiveType }, data);
        });

        return container;
    }

    function detectChartType(data) {
        const cols = data.columns;
        const rows = data.rows;
        const labelCol = cols[0];

        const numericCols = cols.slice(1).filter(col => {
            return rows.every(row => {
                const v = row[col];
                return v === null || v === '' || !isNaN(Number(v));
            });
        });

        if (numericCols.length === 0) return null;

        let type = 'bar';
        const isTimeSeries = rows.some(row => {
            const val = String(row[labelCol]);
            return /^\d{4}[-/]/.test(val) || /jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec/i.test(val);
        });

        if (isTimeSeries || rows.length > 10) {
            type = 'line';
        }

        return { type, labelCol, numericCols };
    }

    function createCalmChart(canvas, chartInfo, data) {
        const { type, labelCol, numericCols } = chartInfo;
        const tokens = getThemeTokens();
        const labels = data.rows.map(r => String(r[labelCol] ?? ''));

        // Palette: Highlight series uses --accent, others use subtle ink/mute tones
        const datasets = numericCols.map((col, i) => {
            const isPrimary = i === 0;
            const seriesColor = isPrimary ? tokens.accent : tokens.mute;

            return {
                label: col,
                data: data.rows.map(r => r[col] === null ? 0 : Number(r[col])),
                backgroundColor: type === 'bar' ? seriesColor : 'transparent',
                borderColor: seriesColor,
                borderWidth: 1.5,
                borderRadius: 0, // No rounded bars
                tension: 0.1, // Minimal curve
                pointRadius: type === 'line' ? 3 : 0,
                pointHoverRadius: type === 'line' ? 5 : 0,
                pointBackgroundColor: seriesColor,
            };
        });

        return new Chart(canvas, {
            type: type === 'line' ? 'line' : 'bar',
            data: { labels, datasets },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                animation: {
                    duration: 250,
                },
                plugins: {
                    legend: {
                        display: numericCols.length > 1,
                        position: 'top',
                        align: 'end',
                        labels: {
                            color: tokens.mute,
                            font: { family: 'Onest', size: 13, weight: '300' },
                            boxWidth: 8,
                            boxHeight: 8,
                            usePointStyle: true,
                        },
                    },
                    tooltip: {
                        backgroundColor: tokens.bg,
                        titleColor: tokens.ink,
                        bodyColor: tokens.ink,
                        borderColor: tokens.line,
                        borderWidth: 1,
                        padding: 10,
                        titleFont: { family: 'Onest', size: 13, weight: '400' },
                        bodyFont: { family: 'Onest', size: 13, weight: '300' },
                        displayColors: false,
                    },
                },
                scales: {
                    x: {
                        grid: {
                            display: false,
                            drawBorder: false,
                        },
                        ticks: {
                            color: tokens.mute,
                            font: { family: 'Onest', size: 13, weight: '300' },
                            maxRotation: 0,
                            autoSkip: true,
                            maxTicksLimit: 8,
                        },
                        border: {
                            color: tokens.line,
                            width: 1,
                        },
                    },
                    y: {
                        grid: {
                            color: tokens.line,
                            drawBorder: false,
                            lineWidth: 1,
                        },
                        ticks: {
                            color: tokens.mute,
                            font: { family: 'Onest', size: 13, weight: '300' },
                        },
                        border: {
                            display: false,
                        },
                    },
                },
            },
        });
    }

    /**
     * Export data rows as CSV file.
     */
    function exportToCsv(data, filename = 'querymind_data.csv') {
        if (!data || !data.columns || !data.rows) return;
        const cols = data.columns;
        const csvRows = [cols.join(',')];

        data.rows.forEach(r => {
            const values = cols.map(c => {
                const val = r[c] === null ? '' : String(r[c]);
                return `"${val.replace(/"/g, '""')}"`;
            });
            csvRows.push(values.join(','));
        });

        const blob = new Blob([csvRows.join('\n')], { type: 'text/csv;charset=utf-8;' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }

    function createEmptyMessage(text) {
        const div = document.createElement('div');
        div.style.cssText = 'padding: 16px 0; color: var(--mute); font-size: var(--text-xs);';
        div.textContent = text;
        return div;
    }

    return { renderTable, renderChart, exportToCsv, detectChartType };
})();
