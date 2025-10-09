
// Cache Buster Utility
// This utility helps prevent caching issues by adding timestamps to API requests

// Function to add cache busting parameter to URLs
function addCacheBuster(url) {
    const separator = url.includes('?') ? '&' : '?';
    return `${url}${separator}_t=${Date.now()}`;
}

// Enhanced API request function with cache busting
async function apiRequestWithCacheBusting(endpoint, options = {}) {
    const url = addCacheBuster(`${API_BASE_URL}${endpoint}`);
    const config = {
        headers: {
            'Content-Type': 'application/json',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
            ...options.headers
        },
        ...options
    };

    if (authToken) {
        config.headers.Authorization = `Bearer ${authToken}`;
    }

    try {
        console.log('Making API request to:', url);
        const response = await fetch(url, config);

        if (!response.ok) {
            console.error('Response not OK:', response.status, response.statusText);
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        const data = await response.json();
        console.log('API response:', data);
        return data;
    } catch (error) {
        console.error('API Error:', error);

        // More specific error messages
        if (error.name === 'TypeError' && error.message.includes('fetch')) {
            showToast('فشل في الاتصال بالخادم. تأكد من تشغيل Backend', 'error');
        } else if (error.message.includes('CORS')) {
            showToast('مشكلة في إعدادات CORS', 'error');
        } else {
            showToast(error.message || 'حدث خطأ في الاتصال', 'error');
        }

        throw error;
    }
}

// Override the original apiRequest function with our cache-busting version
window.apiRequest = apiRequestWithCacheBusting;

// Function to refresh data periodically
function setupPeriodicRefresh(refreshInterval = 300000) { // Default: 5 minutes
    setInterval(async () => {
        console.log('Refreshing data from server...');
        try {
            await loadCategories();
            await loadFeaturedProducts();
            console.log('Data refreshed successfully');
        } catch (error) {
            console.error('Failed to refresh data:', error);
        }
    }, refreshInterval);
}

// Function to force refresh data
async function forceRefreshData() {
    console.log('Force refreshing data from server...');
    try {
        showLoading();
        await loadCategories();
        await loadFeaturedProducts();
        showToast('تم تحديث البيانات بنجاح');
    } catch (error) {
        console.error('Failed to force refresh data:', error);
        showToast('فشل في تحديث البيانات', 'error');
    } finally {
        hideLoading();
    }
}

// Add a refresh button to the UI
function addRefreshButton() {
    const refreshBtn = document.createElement('button');
    refreshBtn.innerHTML = '<i class="fas fa-sync-alt"></i>';
    refreshBtn.className = 'refresh-btn';
    refreshBtn.title = 'تحديث البيانات';
    refreshBtn.addEventListener('click', forceRefreshData);

    // Add the button to the header
    const header = document.querySelector('header') || document.body;
    header.appendChild(refreshBtn);
}

// Initialize cache buster when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Add refresh button
    addRefreshButton();

    // Setup periodic refresh
    setupPeriodicRefresh();

    // Add styles for the refresh button
    const style = document.createElement('style');
    style.textContent = `
        .refresh-btn {
            position: fixed;
            bottom: 20px;
            right: 20px;
            width: 50px;
            height: 50px;
            border-radius: 50%;
            background-color: #4CAF50;
            color: white;
            border: none;
            cursor: pointer;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 18px;
            z-index: 1000;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            transition: all 0.3s ease;
        }
        .refresh-btn:hover {
            background-color: #45a049;
            transform: scale(1.1);
        }
        .refresh-btn:active {
            transform: scale(0.9);
        }
        .refresh-btn i.fa-spin {
            animation: spin 1s linear infinite;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    `;
    document.head.appendChild(style);
});
