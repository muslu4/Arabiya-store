
// Product Form JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Tab functionality - Manual navigation
    const tabButtons = document.querySelectorAll('.tab-nav-item');
    const tabContents = document.querySelectorAll('.tab-content');

    // Function to switch tabs manually
    window.switchTab = function(tabId) {
        // Remove active class from all tabs and contents
        tabButtons.forEach(btn => btn.classList.remove('active'));
        tabContents.forEach(content => content.classList.remove('active'));

        // Find and activate the requested tab
        const targetTab = document.querySelector(`[data-tab="${tabId}"]`);
        const targetContent = document.getElementById(tabId);

        if (targetTab && targetContent) {
            targetTab.classList.add('active');
            targetContent.classList.add('active');
        }
    };

    // Keep click functionality as well
    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            const tabId = this.getAttribute('data-tab');
            window.switchTab(tabId);
            updateTabIndicator();
        });
    });

    // Manual navigation function
    window.navigateTab = function(direction) {
        const activeTab = document.querySelector('.tab-nav-item.active');
        const tabs = Array.from(tabButtons);
        const currentIndex = tabs.indexOf(activeTab);

        let newIndex;
        if (direction === 'next') {
            newIndex = (currentIndex + 1) % tabs.length;
        } else if (direction === 'prev') {
            newIndex = (currentIndex - 1 + tabs.length) % tabs.length;
        }

        const newTabId = tabs[newIndex].getAttribute('data-tab');
        window.switchTab(newTabId);
        updateTabIndicator();

        // Scroll to top on mobile
        if (window.innerWidth <= 768) {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        }
    };

    // Add swipe support for mobile
    let touchStartX = 0;
    let touchEndX = 0;

    document.addEventListener('touchstart', function(e) {
        touchStartX = e.changedTouches[0].screenX;
    }, false);

    document.addEventListener('touchend', function(e) {
        touchEndX = e.changedTouches[0].screenX;
        handleSwipe();
    }, false);

    function handleSwipe() {
        // Only handle swipe if it's significant enough
        if (Math.abs(touchEndX - touchStartX) < 50) return;

        if (touchEndX < touchStartX) {
            // Swiped left - go to next tab
            navigateTab('next');
        }
        if (touchEndX > touchStartX) {
            // Swiped right - go to previous tab
            navigateTab('prev');
        }
    }

    // Update tab indicator
    function updateTabIndicator() {
        const activeTab = document.querySelector('.tab-nav-item.active');
        const tabs = Array.from(tabButtons);
        const currentIndex = tabs.indexOf(activeTab) + 1; // +1 for 1-based index

        document.querySelector('.current-tab').textContent = currentIndex;

        // Update button states
        const prevBtn = document.querySelector('.prev-btn');
        const nextBtn = document.querySelector('.next-btn');

        prevBtn.disabled = currentIndex === 1;
        nextBtn.disabled = currentIndex === tabs.length;
    }

    // Initialize tab indicator
    updateTabIndicator();

    // Auto-populate related fields
    const nameField = document.getElementById('id_name');
    const skuField = document.getElementById('id_sku');
    const metaTitleField = document.getElementById('id_meta_title');

    if (nameField && skuField) {
        nameField.addEventListener('input', function() {
            // Auto-generate SKU from name if empty
            if (!skuField.value) {
                const sku = this.value.replace(/[^a-zA-Z0-9]/g, '-').toLowerCase();
                skuField.value = sku.substring(0, 20);
            }
        });
    }

    if (nameField && metaTitleField) {
        nameField.addEventListener('input', function() {
            // Auto-populate meta title if empty
            if (!metaTitleField.value) {
                metaTitleField.value = this.value;
            }
        });
    }

    // Image preview functionality
    const imageField = document.getElementById('id_image');
    const imagePreview = document.querySelector('.image-upload img');
    const uploadBtn = document.querySelector('.upload-btn');

    if (imageField && imagePreview && uploadBtn) {
        uploadBtn.addEventListener('click', function() {
            imageField.click();
        });

        imageField.addEventListener('change', function() {
            if (this.files && this.files[0]) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    imagePreview.src = e.target.result;
                };
                reader.readAsDataURL(this.files[0]);
            }
        });
    }

    // Form validation
    const form = document.querySelector('#product_form');
    if (form) {
        form.addEventListener('submit', function(e) {
            const name = document.getElementById('id_name').value.trim();
            const description = document.getElementById('id_description').value.trim();
            const category = document.getElementById('id_category').value;

            if (!name) {
                e.preventDefault();
                alert('يرجى إدخال اسم المنتج');
                return;
            }

            if (!description) {
                e.preventDefault();
                alert('يرجى إدخال وصف المنتج');
                return;
            }

            if (!category) {
                e.preventDefault();
                alert('يرجى اختيار قسم المنتج');
                return;
            }
        });
    }

    // Price calculation
    const priceField = document.getElementById('id_price');
    const discountField = document.getElementById('id_discount');
    const specialPriceField = document.getElementById('id_special_price');
    const finalPriceElement = document.createElement('div');
    finalPriceElement.className = 'form-row';
    finalPriceElement.innerHTML = '<label>السعر النهائي</label><div class="final-price">0 د.ع</div>';

    if (priceField && discountField) {
        priceField.addEventListener('input', calculateFinalPrice);
        discountField.addEventListener('input', calculateFinalPrice);

        function calculateFinalPrice() {
            const price = parseFloat(priceField.value) || 0;
            const discount = parseFloat(discountField.value) || 0;
            const finalPrice = price * (1 - discount / 100);

            if (!document.querySelector('.final-price')) {
                priceField.parentNode.parentNode.appendChild(finalPriceElement);
            }

            document.querySelector('.final-price').textContent = finalPrice.toFixed(2) + ' د.ع';
        }
    }

    // Auto-save functionality
    let autoSaveTimer;
    const saveButton = document.querySelector('.submit-row input[type="submit"]');

    if (saveButton) {
        const fields = form.querySelectorAll('input, select, textarea');

        fields.forEach(field => {
            field.addEventListener('input', function() {
                clearTimeout(autoSaveTimer);
                autoSaveTimer = setTimeout(() => {
                    // Show auto-save notification
                    showNotification('تم حفظ التغييرات تلقائياً', 'success');
                }, 3000);
            });
        });
    }

    // Notification function
    function showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <div class="notification-content">
                <i class="fas ${type === 'success' ? 'fa-check-circle' : 'fa-info-circle'}"></i>
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
            }

            .notification-success {
                background-color: #28a745;
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

    // Add slideOut animation
    const slideOutStyle = document.createElement('style');
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
});
