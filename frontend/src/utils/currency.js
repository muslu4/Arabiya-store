// Centralized currency formatting for Iraqi Dinar (IQD)
// Reads optional overrides from environment variables
// REACT_APP_CURRENCY_SYMBOL, REACT_APP_CURRENCY_CODE, REACT_APP_FREE_SHIPPING_THRESHOLD

const SYMBOL = process.env.REACT_APP_CURRENCY_SYMBOL || 'د.ع';
const CODE = process.env.REACT_APP_CURRENCY_CODE || 'IQD';

// Default threshold: 200,000 IQD (can be overridden via env)
const FREE_SHIPPING_THRESHOLD = Number(
    process.env.REACT_APP_FREE_SHIPPING_THRESHOLD || 200000
);

// Simple formatter: IQD has no minor units typically, but keep 2 decimals if needed
export function formatCurrency(value, { withCode = false } = {}) {
    const num = Number(value || 0);
    const formatted = num.toLocaleString('ar-IQ', {
        minimumFractionDigits: 0,
        maximumFractionDigits: 0,
    });
    return withCode ? `${formatted} ${CODE}` : `${formatted} ${SYMBOL}`;
}

export function formatCurrencyWithDecimals(value, { withCode = false } = {}) {
    const num = Number(value || 0);
    const formatted = num.toLocaleString('ar-IQ', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
    });
    return withCode ? `${formatted} ${CODE}` : `${formatted} ${SYMBOL}`;
}

export function getFreeShippingThreshold() {
    return FREE_SHIPPING_THRESHOLD;
}