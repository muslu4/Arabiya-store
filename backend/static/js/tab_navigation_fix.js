
// Tab Navigation Fix for Product Form
document.addEventListener('DOMContentLoaded', function() {
    // Tab navigation elements
    const tabButtons = document.querySelectorAll('.tab-nav-item');
    const tabContents = document.querySelectorAll('.tab-content');

    // Initialize first tab as active
    const firstTab = document.querySelector('.tab-nav-item');
    if (firstTab) {
        firstTab.classList.add('active');

        // Show first tab content
        const firstTabId = firstTab.getAttribute('data-tab');
        const firstTabContent = document.getElementById(firstTabId);
        if (firstTabContent) {
            firstTabContent.classList.add('active');
        }
    }

    // Add event listeners to all tab buttons
    tabButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const tabId = this.getAttribute('data-tab');
            switchToTab(tabId);

            // Update URL without page reload
            const url = new URL(window.location);
            url.hash = tabId;
            window.history.pushState({}, '', url);
        });
    });

    // Check for tab in URL hash on page load
    const hash = window.location.hash.substring(1);
    if (hash && document.getElementById(hash)) {
        switchToTab(hash);
    }

    // Function to switch to a specific tab
    function switchToTab(tabId) {
        // Remove active class from all tabs and contents
        tabButtons.forEach(btn => btn.classList.remove('active'));
        tabContents.forEach(content => content.classList.remove('active'));

        // Add active class to clicked tab
        const clickedButton = Array.from(tabButtons).find(btn => btn.getAttribute('data-tab') === tabId);
        if (clickedButton) {
            clickedButton.classList.add('active');
        }

        // Show corresponding content
        const tabContent = document.getElementById(tabId);
        if (tabContent) {
            tabContent.classList.add('active');
        }
    }
});
