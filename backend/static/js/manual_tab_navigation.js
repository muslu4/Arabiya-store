
// Manual Tab Navigation for Product Form
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
        });
    });

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

    // Function to get next tab
    function getNextTab(currentTabId) {
        const currentIndex = Array.from(tabButtons).findIndex(btn => 
            btn.getAttribute('data-tab') === currentTabId
        );

        if (currentIndex < tabButtons.length - 1) {
            return tabButtons[currentIndex + 1].getAttribute('data-tab');
        }
        return null;
    }

    // Function to get previous tab
    function getPreviousTab(currentTabId) {
        const currentIndex = Array.from(tabButtons).findIndex(btn => 
            btn.getAttribute('data-tab') === currentTabId
        );

        if (currentIndex > 0) {
            return tabButtons[currentIndex - 1].getAttribute('data-tab');
        }
        return null;
    }

    // Add keyboard navigation (optional)
    document.addEventListener('keydown', function(e) {
        if (e.key === 'ArrowRight') {
            // Move to next tab
            const activeTab = document.querySelector('.tab-nav-item.active');
            if (activeTab) {
                const currentTabId = activeTab.getAttribute('data-tab');
                const nextTabId = getNextTab(currentTabId);
                if (nextTabId) {
                    switchToTab(nextTabId);
                }
            }
        } else if (e.key === 'ArrowLeft') {
            // Move to previous tab
            const activeTab = document.querySelector('.tab-nav-item.active');
            if (activeTab) {
                const currentTabId = activeTab.getAttribute('data-tab');
                const previousTabId = getPreviousTab(currentTabId);
                if (previousTabId) {
                    switchToTab(previousTabId);
                }
            }
        }
    });
});
