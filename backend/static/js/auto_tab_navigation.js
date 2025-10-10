
// Auto Tab Navigation for Product Form
document.addEventListener('DOMContentLoaded', function() {
    // Tab navigation elements
    const tabButtons = document.querySelectorAll('.tab-nav-item');
    const tabContents = document.querySelectorAll('.tab-content');

    // Form fields for each tab
    const tabFields = {
        'basic-info': [
            'id_name',
            'id_description',
            'id_category'
        ],
        'pricing': [
            'id_price',
            'id_discount'
        ],
        'inventory': [
            'id_stock',
            'id_low_stock_threshold'
        ],
        'gallery': [
            'id_image',
            'id_gallery'
        ],
        'details': [
            'id_sku',
            'id_weight',
            'id_dimensions',
            'id_material',
            'id_color'
        ],
        'seo': [
            'id_meta_title',
            'id_meta_description',
            'id_meta_keywords'
        ],
        'features': [
            'id_status',
            'id_featured',
            'id_available'
        ]
    };

    // Initialize first tab as active
    const firstTab = document.querySelector('.tab-nav-item');
    if (firstTab) {
        firstTab.classList.add('active');
    }
    
    const firstContent = document.querySelector('.tab-content');
    if (firstContent) {
        firstContent.classList.add('active');
    }
    
    // Add event listeners to all tab buttons
    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            const tabId = this.getAttribute('data-tab');
            // Simply switch to the clicked tab without auto-navigation
            switchToTab(tabId);
        });
    });

    // Check if a tab is filled
    function isTabFilled(tabId) {
        const fieldIds = tabFields[tabId] || [];

        for (const fieldId of fieldIds) {
            const field = document.getElementById(fieldId);

            // Skip optional fields
            if (field && field.hasAttribute('required')) {
                if (!field.value.trim()) {
                    return false;
                }
            }

            // Check if field is empty
            if (field && !field.value.trim()) {
                return false;
            }
        }

        return true;
    }

    // Move to next tab
    function moveToNextTab(currentTabId) {
        const currentIndex = Array.from(tabButtons).findIndex(button => 
            button.getAttribute('data-tab') === currentTabId
        );

        if (currentIndex < tabButtons.length - 1) {
            const nextButton = tabButtons[currentIndex + 1];
            nextButton.click();
        }
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

    // Notification function
    function showNotification(message, type = 'info') {
        // Remove existing notifications
        const existingNotification = document.querySelector('.notification');
        if (existingNotification) {
            existingNotification.remove();
        }

        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <div class="notification-content">
                <i class="fas ${type === 'success' ? 'fa-check-circle' : type === 'warning' ? 'fa-exclamation-circle' : 'fa-info-circle'}"></i>
                <span>${message}</span>
            </div>
        `;

        // Add styles
        const style = document.createElement('style');
        style.textContent = `
            .notification {
                position: fixed;
                top: 20px;
                right: 20px;
                padding: 15px 20px;
                border-radius: 5px;
                color: white;
                z-index: 10000;
                animation: slideIn 0.3s ease-out;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
                max-width: 300px;
            }

            .notification-success {
                background-color: #28a745;
            }

            .notification-warning {
                background-color: #ffc107;
                color: #212529;
            }

            .notification-info {
                background-color: #17a2b8;
            }

            .notification-content {
                display: flex;
                align-items: center;
            }

            .notification-content i {
                margin-right: 10px;
            }

            @keyframes slideIn {
                from {
                    transform: translateX(100%);
                    opacity: 0;
                }
                to {
                    transform: translateX(0);
                    opacity: 1;
                }
            }

            @keyframes slideOut {
                from {
                    transform: translateX(0);
                    opacity: 1;
                }
                to {
                    transform: translateX(100%);
                    opacity: 0;
                }
            }
        `;
        document.head.appendChild(style);

        document.body.appendChild(notification);

        // Remove notification after 5 seconds
        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease-out';
            setTimeout(() => {
                notification.remove();
            }, 300);
        }, 5000);
    }

    // Add slideOut animation if not already added
    if (!document.querySelector('style[data-auto-tab-style]')) {
        const slideOutStyle = document.createElement('style');
        slideOutStyle.setAttribute('data-auto-tab-style', 'true');
        slideOutStyle.textContent = `
            @keyframes slideOut {
                from {
                    transform: translateX(0);
                    opacity: 1;
                }
                to {
                    transform: translateX(100%);
                    opacity: 0;
                }
            }
        `;
        document.head.appendChild(slideOutStyle);
    }
});
