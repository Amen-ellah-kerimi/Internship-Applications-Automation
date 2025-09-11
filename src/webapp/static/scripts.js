// Flash message fade-out
document.addEventListener("DOMContentLoaded", function() {
    const flashes = document.querySelectorAll('.flash');
    flashes.forEach(function(flash) {
        setTimeout(function() {
            flash.style.opacity = '0';
            setTimeout(function() {
                flash.remove();
            }, 600);
        }, 3500);
    });
});

// Confirm before scraping new candidates
function confirmScrape() {
    return confirm("Are you sure you want to scrape new candidates?");
}

// Table sorting
function sortTable(n) {
    const table = document.getElementById("candidates-table");
    let switching = true, dir = "asc", switchcount = 0;
    while (switching) {
        switching = false;
        const rows = table.rows;
        for (let i = 1; i < rows.length - 1; i++) {
            let shouldSwitch = false;
            let x = rows[i].getElementsByTagName("TD")[n];
            let y = rows[i + 1].getElementsByTagName("TD")[n];
            let xContent = x.textContent.trim().toLowerCase();
            let yContent = y.textContent.trim().toLowerCase();
            if (dir === "asc" ? xContent > yContent : xContent < yContent) {
                shouldSwitch = true;
                break;
            }
        }
        if (shouldSwitch) {
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
            switchcount++;
        } else if (switchcount === 0 && dir === "asc") {
            dir = "desc";
            switching = true;
        }
    }
}
