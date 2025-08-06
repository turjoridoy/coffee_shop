// Tea Time - Sales Focused PWA
let isOnline = navigator.onLine;

// PWA Installation
let deferredPrompt;
let installBannerShown = false;

// Check if app is already installed
function isAppInstalled() {
    return window.matchMedia('(display-mode: standalone)').matches ||
        window.navigator.standalone === true;
}

// Show installation banner for first-time visitors
function showInstallBanner() {
    if (isAppInstalled() || installBannerShown) return;

    // Check if user has dismissed the banner before
    const bannerDismissed = localStorage.getItem('installBannerDismissed');
    if (bannerDismissed) return;

    // Show banner after a short delay
    setTimeout(() => {
        const banner = document.getElementById('installBanner');
        if (banner) {
            banner.style.display = 'block';
            installBannerShown = true;
        }
    }, 2000);
}

window.addEventListener('beforeinstallprompt', (e) => {
    console.log('beforeinstallprompt event fired');
    // Prevent Chrome 67 and earlier from automatically showing the prompt
    e.preventDefault();
    // Stash the event so it can be triggered later
    deferredPrompt = e;

    console.log('Install prompt available, deferredPrompt set');

    // Show the install button
    const installButton = document.getElementById('installButton');
    if (installButton) {
        installButton.style.display = 'block';
        console.log('Install button shown');
    }

    // Show banner for first-time visitors
    showInstallBanner();
});

// Debug: Log when app is installed
window.addEventListener('appinstalled', (evt) => {
    console.log('App was installed successfully');
    showToast('App installed successfully! 🎉', 'success');
    hideAllInstallElements();
});

// Handle install button click
document.addEventListener('DOMContentLoaded', function () {
    const installButton = document.getElementById('installButton');
    const bannerInstallButton = document.getElementById('bannerInstallButton');
    const bannerDismissButton = document.getElementById('bannerDismissButton');

    // Handle main install button
    if (installButton) {
        installButton.addEventListener('click', async () => {
            if (deferredPrompt) {
                await triggerInstall();
            }
        });
    }

    // Handle banner install button
    if (bannerInstallButton) {
        bannerInstallButton.addEventListener('click', async () => {
            if (deferredPrompt) {
                await triggerInstall();
            }
            hideInstallBanner();
        });
    }

    // Handle banner dismiss button
    if (bannerDismissButton) {
        bannerDismissButton.addEventListener('click', () => {
            hideInstallBanner();
        });
    }

    // Show banner for first-time visitors
    showInstallBanner();
});

// Trigger installation
async function triggerInstall() {
    console.log('triggerInstall called, deferredPrompt:', !!deferredPrompt);
    if (!deferredPrompt) {
        console.log('No deferredPrompt available');
        showToast('Install prompt not available. Please refresh the page.', 'error');
        return;
    }

    try {
        console.log('Showing install prompt...');
        // Show the install prompt
        deferredPrompt.prompt();
        // Wait for the user to respond to the prompt
        const { outcome } = await deferredPrompt.userChoice;
        console.log(`User response to the install prompt: ${outcome}`);

        if (outcome === 'accepted') {
            console.log('Installation accepted by user');
            showToast('App installed successfully! 🎉', 'success');
            // Hide all install elements
            hideAllInstallElements();
        } else {
            console.log('Installation cancelled by user');
            showToast('Installation cancelled', 'warning');
        }

        // Clear the deferredPrompt variable
        deferredPrompt = null;
    } catch (error) {
        console.error('Installation failed:', error);
        showToast('Installation failed. Please try again.', 'error');
    }
}

// Hide installation banner
function hideInstallBanner() {
    const banner = document.getElementById('installBanner');
    if (banner) {
        banner.style.display = 'none';
    }
    // Remember that user dismissed the banner
    localStorage.setItem('installBannerDismissed', 'true');
}

// Hide all install elements
function hideAllInstallElements() {
    const installButton = document.getElementById('installButton');
    const banner = document.getElementById('installBanner');
    const installGuideButton = document.getElementById('installGuideButton');

    if (installButton) {
        installButton.style.display = 'none';
    }

    if (banner) {
        banner.style.display = 'none';
    }

    if (installGuideButton) {
        installGuideButton.style.display = 'none';
    }
}

// Handle app installed event
window.addEventListener('appinstalled', (evt) => {
    console.log('App was installed');
    showToast('App installed successfully! 🎉', 'success');
    hideAllInstallElements();
});

// Installation guide functions
function showInstallGuide() {
    const modal = document.getElementById('installGuideModal');
    if (modal) {
        modal.style.display = 'flex';
        document.body.style.overflow = 'hidden';
    }
}

function closeInstallGuide() {
    const modal = document.getElementById('installGuideModal');
    if (modal) {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto';
    }
}

// Close modal when clicking outside
document.addEventListener('DOMContentLoaded', function () {
    const modal = document.getElementById('installGuideModal');
    if (modal) {
        modal.addEventListener('click', function (e) {
            if (e.target === modal) {
                closeInstallGuide();
            }
        });
    }
});

// Register service worker
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/service-worker.js', {
            scope: '/'
        })
            .then((registration) => {
                console.log('SW registered successfully: ', registration);

                // Check if there's an update available
                registration.addEventListener('updatefound', () => {
                    const newWorker = registration.installing;
                    newWorker.addEventListener('statechange', () => {
                        if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
                            console.log('New service worker available');
                        }
                    });
                });
            })
            .catch((registrationError) => {
                console.error('SW registration failed: ', registrationError);
                // Try to register without scope if it fails
                navigator.serviceWorker.register('/service-worker.js')
                    .then((registration) => {
                        console.log('SW registered without scope: ', registration);
                    })
                    .catch((error) => {
                        console.error('SW registration completely failed: ', error);
                    });
            });
    });
}

// Initialize app
document.addEventListener('DOMContentLoaded', function () {
    // Debug: Check if manifest is accessible
    fetch('/manifest.json')
        .then(response => {
            if (response.ok) {
                console.log('Manifest is accessible');
                return response.json();
            } else {
                console.error('Manifest not accessible:', response.status);
            }
        })
        .then(manifest => {
            if (manifest) {
                console.log('Manifest loaded:', manifest.name);
            }
        })
        .catch(error => {
            console.error('Failed to load manifest:', error);
        });

    loadDashboardData();
    loadTodaySalesCount();
    loadStockData();
    loadPaymentMethods();
    loadProducts();
    loadQuickActions();
    updateConnectionStatus();

    // Event listeners
    window.addEventListener('online', updateConnectionStatus);
    window.addEventListener('offline', updateConnectionStatus);

    // Form event listeners
    document.getElementById('saleQuantity').addEventListener('input', calculateSaleTotal);
    document.getElementById('salePrice').addEventListener('input', calculateSaleTotal);

    // Product selection event listener
    document.getElementById('saleProduct').addEventListener('change', onProductSelect);

    // Check if app is installed and show appropriate UI
    if (isAppInstalled()) {
        document.body.classList.add('pwa-installed');
        hideAllInstallElements();
    }

    // Show installation instructions for mobile users
    if (isMobileDevice() && !isAppInstalled()) {
        showMobileInstallInstructions();
    }
});

// Check if device is mobile
function isMobileDevice() {
    return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
}

// Show mobile installation instructions
function showMobileInstallInstructions() {
    // This will be called for mobile users who haven't installed the app
    console.log('Mobile device detected - showing install instructions');

    // Add a subtle hint in the header
    const header = document.querySelector('.app-header');
    if (header) {
        const installHint = document.createElement('div');
        installHint.style.cssText = 'position: absolute; top: 50%; right: 20px; transform: translateY(-50%); font-size: 0.8rem; opacity: 0.8;';
        installHint.innerHTML = '📱 Tap menu → "Add to Home Screen"';
        header.appendChild(installHint);

        // Remove hint after 10 seconds
        setTimeout(() => {
            installHint.remove();
        }, 10000);
    }
}

// Load quick actions from API
async function loadQuickActions() {
    try {
        const response = await apiRequest('/products/quick_actions/');
        const quickActions = Array.isArray(response) ? response : response.results || [];

        const quickActionsContainer = document.getElementById('quickActionsContainer');
        if (!quickActionsContainer) return;

        if (quickActions.length === 0) {
            quickActionsContainer.innerHTML = '<p style="text-align: center; color: #666; padding: 20px;">No quick actions configured</p>';
        } else {
            quickActionsContainer.innerHTML = quickActions.map(product => `
                <button class="btn btn-primary btn-full" onclick="showQuickSale('${product.name}', ${product.price})">
                    ${getProductIcon(product.name)} ${product.name}
                </button>
            `).join('');
        }

        console.log('Quick actions loaded:', quickActions.length);
    } catch (error) {
        console.error('Failed to load quick actions:', error);
        showAlert('Failed to load quick actions', 'warning');
    }
}

function getProductIcon(productName) {
    const name = productName.toLowerCase();
    if (name.includes('coffee')) return '☕';
    if (name.includes('tea') || name.includes('chai')) return '🍵';
    if (name.includes('samosa')) return '🥟';
    if (name.includes('burger')) return '🍔';
    if (name.includes('fries')) return '🍟';
    if (name.includes('cake')) return '🍰';
    if (name.includes('ice cream')) return '🍦';
    if (name.includes('cola') || name.includes('sprite') || name.includes('pepsi')) return '🥤';
    if (name.includes('water')) return '💧';
    return '📦';
}

// API Request function
async function apiRequest(endpoint, options = {}) {
    const baseUrl = window.location.origin;
    const url = `${baseUrl}/api${endpoint}`;

    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
        },
    };

    const finalOptions = { ...defaultOptions, ...options };

    try {
        const response = await fetch(url, finalOptions);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('API request failed:', error);
        throw error;
    }
}

// Get CSRF token from Django
function getCSRFToken() {
    const token = document.querySelector('[name=csrfmiddlewaretoken]');
    return token ? token.value : '';
}



// Load payment methods from API
async function loadPaymentMethods() {
    try {
        const response = await apiRequest('/payment-methods/');
        console.log('Payment methods API response:', response);

        // Handle different response formats
        const paymentMethods = Array.isArray(response) ? response : (response.results || []);

        const paymentSelect = document.getElementById('salePayment');

        // Clear existing options
        paymentSelect.innerHTML = '';

        // Add payment methods from API
        paymentMethods.forEach((method, index) => {
            const option = document.createElement('option');
            option.value = method.id;
            option.textContent = method.name;
            paymentSelect.appendChild(option);

            // Select the first payment method by default
            if (index === 0) {
                option.selected = true;
            }
        });

        console.log('Payment methods loaded:', paymentMethods.length);
    } catch (error) {
        console.error('Failed to load payment methods:', error);
        showAlert('Failed to load payment methods', 'warning');
    }
}

// Load products from API
async function loadProducts() {
    try {
        const response = await apiRequest('/products/');
        console.log('Products API response:', response);

        // Handle different response formats
        const products = Array.isArray(response) ? response : (response.results || []);

        const productSelect = document.getElementById('saleProduct');

        // Clear existing options
        productSelect.innerHTML = '<option value="">Select Product</option>';

        // Add products from API
        products.forEach(product => {
            const option = document.createElement('option');
            option.value = product.id;

            // Add stock status to product name for stockable products
            if (product.product_type === 'stockable') {
                if (product.stock_quantity <= 0) {
                    option.textContent = `${product.name} - ৳${product.price} (OUT OF STOCK)`;
                    option.disabled = true; // Disable out of stock products
                } else if (product.stock_quantity <= product.min_stock_level) {
                    option.textContent = `${product.name} - ৳${product.price} (LOW STOCK: ${product.stock_quantity})`;
                } else {
                    option.textContent = `${product.name} - ৳${product.price}`;
                }
            } else {
                option.textContent = `${product.name} - ৳${product.price}`;
            }

            option.dataset.price = product.price;
            option.dataset.productType = product.product_type;
            option.dataset.stockQuantity = product.stock_quantity;
            option.dataset.categoryName = product.category_name;
            productSelect.appendChild(option);
        });

        console.log('Products loaded:', products.length);
    } catch (error) {
        console.error('Failed to load products:', error);
        showAlert('Failed to load products', 'warning');
    }
}

function onProductSelect() {
    const productSelect = document.getElementById('saleProduct');
    const selectedOption = productSelect.options[productSelect.selectedIndex];

    if (selectedOption && selectedOption.value && !selectedOption.disabled) {
        const price = parseFloat(selectedOption.dataset.price);
        const productType = selectedOption.dataset.productType;
        const stockQuantity = parseInt(selectedOption.dataset.stockQuantity);
        const categoryName = selectedOption.dataset.categoryName;

        // Set the price
        document.getElementById('salePrice').value = price;

        // Show category and stock info
        const productInfo = document.getElementById('productInfo') || createProductInfo();
        productInfo.innerHTML = `
            <div style="margin-top: 5px; font-size: 0.9rem; color: #666;">
                <p>Category: ${categoryName}</p>
                ${productType === 'stockable' ? `<p>Available Stock: ${stockQuantity}</p>` : '<p>Instant Product</p>'}
            </div>
        `;
        productInfo.style.display = 'block';

        // Show stock warning for stockable products
        if (productType === 'stockable') {
            if (stockQuantity <= 0) {
                productSelect.style.borderColor = '#ff4444';
                showToast('This product is out of stock! Please restock before selling.', 'error');
                // Clear the selection for out-of-stock products
                productSelect.value = '';
                return;
            } else if (stockQuantity <= 5) {
                productSelect.style.borderColor = '#ffaa00';
                showToast('Low stock warning!', 'warning');
            } else {
                productSelect.style.borderColor = '';
            }
        } else {
            productSelect.style.borderColor = '';
        }

        calculateSaleTotal();
    } else {
        const productInfo = document.getElementById('productInfo');
        if (productInfo) {
            productInfo.style.display = 'none';
        }
        productSelect.style.borderColor = '';

        // If disabled option was selected, clear it
        if (selectedOption && selectedOption.disabled) {
            productSelect.value = '';
            showToast('This product is out of stock! Please select another product.', 'error');
        }
    }
}

function createProductInfo() {
    const productInfo = document.createElement('div');
    productInfo.id = 'productInfo';
    productInfo.style.cssText = 'margin-top: 5px; font-size: 0.9rem; color: #666;';
    document.getElementById('saleProduct').parentNode.appendChild(productInfo);
    return productInfo;
}

// Update connection status
function updateConnectionStatus() {
    isOnline = navigator.onLine;
    const statusDot = document.getElementById('statusDot');
    const statusText = document.getElementById('statusText');

    if (isOnline) {
        statusDot.className = 'status-dot online';
        statusText.textContent = 'Online';
    } else {
        statusDot.className = 'status-dot offline';
        statusText.textContent = 'Offline';
    }
}

// Tab management
function showTab(tabName) {
    // Hide all tab contents
    const tabContents = document.querySelectorAll('.tab-content');
    tabContents.forEach(content => content.classList.remove('active'));

    // Remove active class from all nav tabs
    const navTabs = document.querySelectorAll('.nav-tab');
    navTabs.forEach(tab => tab.classList.remove('active'));

    // Remove active class from bottom nav items
    const bottomNavItems = document.querySelectorAll('.bottom-nav-item');
    bottomNavItems.forEach(item => item.classList.remove('active'));

    // Show selected tab
    document.getElementById(tabName).classList.add('active');

    // Add active class to corresponding nav tab
    const activeNavTab = document.querySelector(`[onclick="showTab('${tabName}')"]`);
    if (activeNavTab) {
        activeNavTab.classList.add('active');
    }

    // Add active class to corresponding bottom nav item
    const activeBottomNavItem = document.querySelector(`.bottom-nav-item[onclick="showTab('${tabName}')"]`);
    if (activeBottomNavItem) {
        activeBottomNavItem.classList.add('active');
    }

    // Load data based on tab
    if (tabName === 'dashboard') {
        loadDashboardData();
        loadStockData();
    } else if (tabName === 'today') {
        loadTodaysSales();
    } else if (tabName === 'reports') {
        loadReports();
    }
}

// Load dashboard data
async function loadDashboardData() {
    try {
        const data = await apiRequest('/dashboard-data/');

        // Update summary
        document.getElementById('todaySales').textContent = data.today_total.toLocaleString();
        document.getElementById('todayTransactions').textContent = data.today_count;
        document.getElementById('monthlyRevenue').textContent = data.monthly_total.toLocaleString();

    } catch (error) {
        console.error('Failed to load dashboard data:', error);
        showAlert('Failed to load dashboard data', 'error');
    }
}

// Load today's sales count
async function loadTodaySalesCount() {
    try {
        const data = await apiRequest('/today-sales-count/');
        displayTodaySalesCount(data);
    } catch (error) {
        console.error('Failed to load today\'s sales count:', error);
        showAlert('Failed to load today\'s sales count', 'error');
    }
}

// Display today's sales count
function displayTodaySalesCount(data) {
    document.getElementById('todaySales').textContent = `৳${data.today_total.toLocaleString()}`;
    document.getElementById('todayTransactions').textContent = data.today_count;
}

// Load stock data
async function loadStockData() {
    try {
        const response = await apiRequest('/products/');
        const products = Array.isArray(response) ? response : response.results || [];

        // Filter only stockable products
        const stockableProducts = products.filter(product => product.product_type === 'stockable');

        displayStockData(stockableProducts);
    } catch (error) {
        console.error('Failed to load stock data:', error);
        showAlert('Failed to load stock data', 'error');
    }
}

// Display stock data
function displayStockData(products) {
    const container = document.getElementById('stockContainer');
    const loading = document.getElementById('stockLoading');
    const tbody = document.getElementById('stockBody');

    if (products.length === 0) {
        tbody.innerHTML = '<tr><td colspan="4" style="text-align: center; color: #666;">No stockable products found</td></tr>';
    } else {
        tbody.innerHTML = products.map(product => {
            let statusClass = '';
            let statusText = '';

            if (product.stock_quantity <= 0) {
                statusClass = 'stock-out';
                statusText = 'Out of Stock';
            } else if (product.stock_quantity <= product.min_stock_level) {
                statusClass = 'stock-low';
                statusText = 'Low Stock';
            } else {
                statusClass = 'stock-ok';
                statusText = 'In Stock';
            }

            return `
                <tr class="${statusClass}">
                    <td>${product.name}</td>
                    <td>${product.category_name}</td>
                    <td>${product.stock_quantity}</td>
                    <td><span class="status-badge ${statusClass}">${statusText}</span></td>
                </tr>
            `;
        }).join('');
    }

    loading.style.display = 'none';
    container.style.display = 'block';
}

// Sales Functions
function calculateSaleTotal() {
    const quantity = parseFloat(document.getElementById('saleQuantity').value) || 0;
    const price = parseFloat(document.getElementById('salePrice').value) || 0;
    document.getElementById('saleTotal').value = (quantity * price).toFixed(2);
}

async function addSale(event) {
    event.preventDefault();

    // Get form values before resetting
    const productId = document.getElementById('saleProduct').value;
    const quantity = document.getElementById('saleQuantity').value;
    const unitPrice = document.getElementById('salePrice').value;
    const paymentMethodId = document.getElementById('salePayment').value;
    const customerName = document.getElementById('saleCustomerName')?.value || '';
    const customerPhone = document.getElementById('saleCustomerPhone')?.value || '';
    const notes = document.getElementById('saleNotes')?.value || '';

    // Validate required fields
    if (!productId || !quantity || !unitPrice || !paymentMethodId) {
        showAlert('Please fill in all required fields', 'error');
        return;
    }

    // Additional validation for dropdowns
    if (productId === '' || paymentMethodId === '') {
        showAlert('Please select a product and payment method', 'error');
        return;
    }

    // Check stock availability for stockable products
    const productSelect = document.getElementById('saleProduct');
    const selectedOption = productSelect.options[productSelect.selectedIndex];
    const productType = selectedOption.dataset.productType;
    const stockQuantity = parseInt(selectedOption.dataset.stockQuantity);
    const requestedQuantity = parseInt(quantity);

    if (productType === 'stockable') {
        if (stockQuantity <= 0) {
            showToast('This product is out of stock! Please restock before selling.', 'error');
            return;
        }

        if (requestedQuantity > stockQuantity) {
            showToast(`Insufficient stock! Available: ${stockQuantity}, Requested: ${requestedQuantity}`, 'error');
            return;
        }
    }

    const sale = {
        product: parseInt(productId),
        quantity: parseInt(quantity),
        unit_price: parseFloat(unitPrice),
        payment_method: parseInt(paymentMethodId),
        customer_name: customerName,
        customer_phone: customerPhone,
        notes: notes
    };

    console.log('Sending sale data:', sale);
    console.log('Product ID type:', typeof sale.product, 'Value:', sale.product);
    console.log('Payment Method ID type:', typeof sale.payment_method, 'Value:', sale.payment_method);

    try {
        await apiRequest('/sales/', {
            method: 'POST',
            body: JSON.stringify(sale)
        });

        showToast('Sale added successfully! 🎉');

        // Reset form
        document.getElementById('saleForm').reset();

        // Reload products and payment methods to restore defaults
        loadProducts();
        loadPaymentMethods();

        // Reload dashboard data
        loadDashboardData();
        loadTodaySalesCount();
        loadStockData();

    } catch (error) {
        console.error('Failed to add sale:', error);

        // Handle specific error messages from backend
        if (error.response && error.response.data && error.response.data.error) {
            showToast(error.response.data.error, 'error');
        } else {
            showToast('Failed to add sale. Please try again.', 'error');
        }
    }
}

function showQuickSale(item, price) {
    // Find and select the appropriate product
    const productSelect = document.getElementById('saleProduct');
    const itemLower = item.toLowerCase();

    // Find and select the appropriate product by exact name match
    for (let option of productSelect.options) {
        const productName = option.textContent.split(' - ')[0].toLowerCase(); // Get just the product name part
        if (productName === itemLower) {
            option.selected = true;
            onProductSelect(); // Trigger product selection to set price and other fields
            break;
        }
    }

    // Set quantity to 1
    document.getElementById('saleQuantity').value = 1;
    calculateSaleTotal();

    // Switch to sales tab
    showTab('sales');

    // Focus on quantity field for easy editing
    document.getElementById('saleQuantity').focus();
}

// Load today's sales
async function loadTodaysSales() {
    try {
        const data = await apiRequest('/sales/today/');
        displayTodaysSales(data);
    } catch (error) {
        console.error('Failed to load today\'s sales:', error);
        showAlert('Failed to load today\'s sales', 'error');
    }
}

function displayTodaysSales(sales) {
    const container = document.getElementById('todaySalesContainer');
    const loading = document.getElementById('todaySalesLoading');
    const tbody = document.getElementById('todaySalesBody');

    if (sales.length === 0) {
        tbody.innerHTML = '<tr><td colspan="4" style="text-align: center; color: #666;">No sales today</td></tr>';
    } else {
        tbody.innerHTML = sales.map(sale => `
            <tr>
                <td>${new Date(sale.created_at).toLocaleTimeString()}</td>
                <td>${sale.product_name}</td>
                <td>${sale.quantity}</td>
                <td>৳${sale.total_amount}</td>
            </tr>
        `).join('');
    }

    loading.style.display = 'none';
    container.style.display = 'block';
}

// Load reports data
async function loadReports() {
    try {
        const data = await apiRequest('/dashboard-data/');

        // Generate summary text
        generateSummaryText(data);

        // Show reports container
        document.getElementById('reportsLoading').style.display = 'none';
        document.getElementById('reportsContainer').style.display = 'block';

    } catch (error) {
        console.error('Failed to load reports:', error);
        showAlert('Failed to load reports', 'error');
    }
}



// Generate summary text for copying
function generateSummaryText(data) {
    const today = new Date().toLocaleDateString();
    let summaryText = `📊 Coffee Shop Daily Report - ${today}\n\n`;

    // Summary section
    summaryText += `📈 SUMMARY:\n`;
    summaryText += `• Today's Sales: ৳${data.today_total.toLocaleString()}\n`;
    summaryText += `• Transactions: ${data.today_count}\n`;
    summaryText += `• Monthly Revenue: ৳${data.monthly_total.toLocaleString()}\n\n`;

    // Category breakdown
    if (data.category_breakdown && data.category_breakdown.length > 0) {
        summaryText += `📋 CATEGORY BREAKDOWN:\n`;
        data.category_breakdown.forEach(category => {
            summaryText += `• ${category.category__name || 'Unknown'}: ${category.count} sales (৳${category.total.toLocaleString()})\n`;
        });
    } else {
        summaryText += `📋 CATEGORY BREAKDOWN:\n• No category data available\n`;
    }

    // Payment method breakdown
    if (data.payment_breakdown && data.payment_breakdown.length > 0) {
        summaryText += `\n💳 PAYMENT METHODS:\n`;
        data.payment_breakdown.forEach(payment => {
            summaryText += `• ${payment.payment_method__name || 'Unknown'}: ${payment.count} transactions (৳${payment.total.toLocaleString()})\n`;
        });
    }

    document.getElementById('summaryText').value = summaryText;
}

// Copy summary to clipboard
async function copySummary() {
    const summaryText = document.getElementById('summaryText').value;

    try {
        await navigator.clipboard.writeText(summaryText);
        showAlert('Summary copied to clipboard!', 'success');
    } catch (error) {
        // Fallback for older browsers
        const textArea = document.getElementById('summaryText');
        textArea.select();
        document.execCommand('copy');
        showAlert('Summary copied to clipboard!', 'success');
    }
}

// Utility Functions
function showAlert(message, type = 'info') {
    // Create alert element
    const alert = document.createElement('div');
    alert.className = `alert alert-${type}`;
    alert.textContent = message;

    // Add to page
    document.body.appendChild(alert);

    // Remove after 3 seconds
    setTimeout(() => {
        alert.remove();
    }, 3000);
}

// Toast Notification Function
function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    const toastMessage = document.getElementById('toast-message');

    // Set message
    toastMessage.textContent = message;

    // Set icon based on type
    const toastIcon = toast.querySelector('.toast-icon');
    if (type === 'error') {
        toastIcon.textContent = '❌';
    } else if (type === 'warning') {
        toastIcon.textContent = '⚠️';
    } else {
        toastIcon.textContent = '✅';
    }

    // Show toast
    toast.classList.add('show');

    // Hide after 3 seconds
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}