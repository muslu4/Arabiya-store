// Centralized currency formatting for Iraqi Dinar (IQD)
// Reads optional overrides from environment variables
// REACT_APP_CURRENCY_SYMBOL, REACT_APP_CURRENCY_CODE, REACT_APP_FREE_SHIPPING_THRESHOLD

const SYMBOL = process.env.REACT_APP_CURRENCY_SYMBOL || 'د.ع';
const CODE = process.env.REACT_APP_CURRENCY_CODE || 'IQD';

// Default threshold: 100,000 IQD (can be overridden via env)
const FREE_SHIPPING_THRESHOLD = Number(
    process.env.REACT_APP_FREE_SHIPPING_THRESHOLD || 100000
);

// Simple formatter: IQD has no minor units typically, but keep 2 decimals if needed
export function formatCurrency(value, { withCode = false } = {}) {
    const num = Number(value || 0);
    const formatted = num.toLocaleString('en-US', {
        minimumFractionDigits: 0,
        maximumFractionDigits: 0,
    });
    return withCode ? `${formatted} ${CODE}` : `${formatted} ${SYMBOL}`;
}

export function formatCurrencyWithDecimals(value, { withCode = false } = {}) {
    const num = Number(value || 0);
    const formatted = num.toLocaleString('en-US', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
    });
    return withCode ? `${formatted} ${CODE}` : `${formatted} ${SYMBOL}`;
}

export function getFreeShippingThreshold() {
    return FREE_SHIPPING_THRESHOLD;
}

/**
 * حساب رسوم التوصيل بناءً على الوزن الإجمالي
 * @param {number} totalWeight - الوزن الإجمالي بالكيلوغرام
 * @param {number} subtotal - المجموع الفرعي للطلب
 * @returns {number} - رسوم التوصيل بالدينار العراقي
 */
export function calculateShippingFee(totalWeight, subtotal) {
    // إذا كان المجموع أكثر من عتبة الشحن المجاني، الشحن مجاني
    if (subtotal >= FREE_SHIPPING_THRESHOLD) {
        return 0;
    }
    
    // حساب رسوم التوصيل بناءً على الوزن
    // السعر الأساسي: 1000 د.ع لكل كيلوغرام
    const pricePerKg = 1000;
    const baseWeight = 0.5; // الوزن الأساسي المجاني (نصف كيلو)
    
    if (totalWeight <= baseWeight) {
        return 1000; // رسوم أساسية للأوزان الخفيفة
    }
    
    // حساب الوزن الإضافي
    const additionalWeight = Math.ceil(totalWeight - baseWeight);
    const shippingFee = 1000 + (additionalWeight * pricePerKg);
    
    return shippingFee;
}