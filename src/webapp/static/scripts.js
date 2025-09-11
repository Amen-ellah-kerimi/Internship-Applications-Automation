// Modal download confirmation for attachments
document.addEventListener("DOMContentLoaded", function() {
    const modal = document.getElementById("download-modal");
    const closeModal = document.getElementById("close-modal");
    const filenameSpan = document.getElementById("modal-filename");
    const downloadLink = document.getElementById("modal-download-link");
    document.querySelectorAll('.download-btn').forEach(function(btn) {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const filename = btn.getAttribute('data-filename');
            const folder = btn.getAttribute('data-folder') || 'attachments';
            filenameSpan.textContent = filename;
            downloadLink.href = `/${folder}/${filename}`;
            downloadLink.setAttribute('download', filename);
            modal.style.display = 'block';
        });
    });
    closeModal.onclick = function() {
        modal.style.display = 'none';
    };
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    };
});
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
