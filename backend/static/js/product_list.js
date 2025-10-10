
// Product List JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Toggle all checkboxes
    const toggleCheckbox = document.getElementById('toggle');
    if (toggleCheckbox) {
        toggleCheckbox.addEventListener('change', function() {
            const checkboxes = document.querySelectorAll('input[name="_selected_action"]');
            checkboxes.forEach(checkbox => {
                checkbox.checked = this.checked;
            });
        });
    }

    // Search functionality
    const searchInput = document.querySelector('#changelist-search input');
    if (searchInput) {
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                performSearch();
            }
        });
    }

    // Bulk actions
    const actionSelect = document.getElementById('action-select');
    if (actionSelect) {
        actionSelect.addEventListener('change', function() {
            const selectedAction = this.value;
            if (selectedAction) {
                const confirmationMessage = getConfirmationMessage(selectedAction);
                if (confirm(confirmationMessage)) {
                    performBulkAction();
                } else {
                    this.value = '';
                }
            }
        });
    }

    // Search function
    function performSearch() {
        const searchQuery = document.querySelector('#changelist-search input').value;
        const currentUrl = new URL(window.location.href);

        if (searchQuery) {
            currentUrl.searchParams.set('q', searchQuery);
        } else {
            currentUrl.searchParams.delete('q');
        }

        currentUrl.searchParams.set('p', 1); // Reset to first page

        window.location.href = currentUrl.toString();
    }

    // Bulk action function
    function performBulkAction() {
        const selectedAction = document.getElementById('action-select').value;
        if (!selectedAction) return;

        const selectedItems = Array.from(document.querySelectorAll('input[name="_selected_action"]:checked'))
            .map(checkbox => checkbox.value);

        if (selectedItems.length === 0) {
            showNotification('الرجاء اختيار منتجات واحدة على الأقل', 'warning');
            return;
        }

        const form = document.createElement('form');
        form.method = 'POST';
        form.action = window.location.pathname;

        // Add CSRF token
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        const csrfInput = document.createElement('input');
        csrfInput.type = 'hidden';
        csrfInput.name = 'csrfmiddlewaretoken';
        csrfInput.value = csrfToken;
        form.appendChild(csrfInput);

        // Add action and selected items
        const actionInput = document.createElement('input');
        actionInput.type = 'hidden';
        actionInput.name = 'action';
        actionInput.value = selectedAction;
        form.appendChild(actionInput);

        selectedItems.forEach(item => {
            const itemInput = document.createElement('input');
            itemInput.type = 'hidden';
            itemInput.name = '_selected_action';
            itemInput.value = item;
            form.appendChild(itemInput);
        });

        document.body.appendChild(form);
        form.submit();
    }

    // Get confirmation message for bulk actions
    function getConfirmationMessage(action) {
        const messages = {
            'activate': 'هل أنت متأكد من تفعيل المنتجات المحددة؟',
            'deactivate': 'هل أنت متأكد من تعطيل المنتجات المحددة؟',
            'delete': 'هل أنت متأكد من حذف المنتجات المحددة؟ هذه العملة لا يمكن التراجع عنها.',
            'featured': 'هل أنت متأكد من إضافة المنتجات المحددة إلى القائمة المميزة؟',
            'unfeatured': 'هل أنت متأكد من إزالة المنتجات المحددة من القائمة المميزة؟'
        };

        return messages[action] || 'هل أنت متأكد من تنفيذ هذا الإجراء؟';
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
    if (!document.querySelector('style[data-product-list-style]')) {
        const slideOutStyle = document.createElement('style');
        slideOutStyle.setAttribute('data-product-list-style', 'true');
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

    // Filter functionality
    const filterLinks = document.querySelectorAll('#changelist-filter li a');
    if (filterLinks.length > 0) {
        filterLinks.forEach(link => {
            link.addEventListener('click', function(e) {
                e.preventDefault();

                // Update active state
                filterLinks.forEach(l => l.classList.remove('active'));
                this.classList.add('active');

                // Update URL
                const url = new URL(this.href);
                window.location.href = url.toString();
            });
        });
    }

    // Export functionality
    const exportButton = document.querySelector('.export-button');
    if (exportButton) {
        exportButton.addEventListener('click', function() {
            const exportFormat = this.getAttribute('data-format');
            const selectedItems = Array.from(document.querySelectorAll('input[name="_selected_action"]:checked'))
                .map(checkbox => checkbox.value);

            let url = new URL(window.location.pathname + '/export/');
            url.searchParams.set('format', exportFormat);

            if (selectedItems.length > 0) {
                selectedItems.forEach(item => {
                    url.searchParams.append('ids', item);
                });
            }

            window.location.href = url.toString();
        });
    }
});
