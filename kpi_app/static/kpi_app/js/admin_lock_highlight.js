// Admin Row Highlighting for Approved Records
document.addEventListener('DOMContentLoaded', function () {
    function highlightLockedRows() {
        var rows = document.querySelectorAll('#result_list tbody tr');

        rows.forEach(function (row) {
            var approvedIndicator = row.querySelector('.approved-status-indicator[data-approved="true"]');

            if (approvedIndicator) {
                row.classList.add('row-locked');

                // Apply Approved Style (Light Green)
                var cells = row.querySelectorAll('td, th');
                cells.forEach(function (cell) {
                    cell.style.setProperty('background-color', '#d1e7dd', 'important'); // Light Green
                    cell.style.setProperty('color', '#0f5132', 'important');
                });
            } else {
                row.classList.remove('row-locked');
                var cells = row.querySelectorAll('td, th');
                cells.forEach(function (cell) {
                    cell.style.removeProperty('background-color');
                    cell.style.removeProperty('color');
                });
            }
        });
    }

    // Run immediately
    highlightLockedRows();

    // Run periodically to handle dynamic admin updates (filtering, sorting)
    setInterval(highlightLockedRows, 1000);
});
