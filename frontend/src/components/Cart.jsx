import { useState } from 'react';
import { formatCurrency } from '../utils/currency';
import { api } from '../api';
import Checkout from './Checkout';

const Cart = ({ cart, onCartChange, onClose, handleCheckout }) => {
  const [notification, setNotification] = useState({ show: false, message: '', type: 'success' });
  const whatsappLink = "https://wa.me/96407744305501";
  const telegramLink = "https://t.me/arabiyaphone";
  const phoneLink = "tel:07744305501";

  const showNotification = (message, type = 'success') => {
    setNotification({ show: true, message, type });
    setTimeout(() => {
      setNotification({ show: false, message: '', type: 'success' });
    }, 3000);
  };

  const handleQuantityChange = (product, newQuantity) => {
    if (newQuantity < 1) {
      // Remove item if quantity is less than 1
      onCartChange(cart.filter(item => item.id !== product.id));
    } else {
      // التحقق من المخزون المتوفر
      if (newQuantity > product.stock) {
        showNotification(`عذراً، المخزون المتوفر فقط ${product.stock} قطعة`, 'error');
        return;
      }
      onCartChange(cart.map(item =>
        item.id === product.id ? { ...item, quantity: newQuantity } : item
      ));
    }
  };

  const getTotalPrice = () => {
    return cart.reduce((total, item) => total + item.price * item.quantity, 0);
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex justify-center items-center" onClick={onClose}>
      <div className="bg-white rounded-lg shadow-xl w-full max-w-md m-4" onClick={(e) => e.stopPropagation()}>
        <div className="p-4 border-b flex justify-between items-center">
          <h2 className="text-xl font-bold">سلة التسوق</h2>
          <button onClick={onClose} className="text-gray-500 hover:text-gray-800">&times;</button>
        </div>
        
        {/* إشعار الخطأ */}
        {notification.show && (
          <div className={`mx-4 mt-4 p-3 rounded-md ${notification.type === 'error' ? 'bg-red-100 text-red-700 border border-red-300' : 'bg-green-100 text-green-700 border border-green-300'}`}>
            <p className="text-sm text-center font-medium">{notification.message}</p>
          </div>
        )}
        
        <div className="p-4" style={{ maxHeight: '60vh', overflowY: 'auto' }}>
          {cart.length === 0 ? (
            <p className="text-center text-gray-500">سلتك فارغة.</p>
          ) : (
            cart.map(item => (
              <div key={item.id} className="flex items-center justify-between py-2 border-b">
                <div className="flex items-center">
                  <img src={item.image || '/placeholder-product-small.png'} alt={item.name} className="w-16 h-16 object-cover rounded-md mr-4" />
                  <div>
                    <p className="font-semibold">{item.name}</p>
                    <p className="text-sm text-gray-600">{formatCurrency(item.price)}</p>
                  </div>
                </div>
                <div className="flex items-center">
                  <button onClick={() => handleQuantityChange(item, item.quantity - 1)} className="px-2 py-1 border rounded-md">-</button>
                  <span className="px-4">{item.quantity}</span>
                  <button onClick={() => handleQuantityChange(item, item.quantity + 1)} className="px-2 py-1 border rounded-md">+</button>
                </div>
              </div>
            ))
          )}
        </div>
        {cart.length > 0 && (
          <div className="p-4 border-t">
            <div className="flex justify-between items-center font-bold text-lg mb-4">
              <span>المجموع:</span>
              <span>{formatCurrency(getTotalPrice())}</span>
            </div>
            <div className="flex flex-col space-y-3">
              <button 
                onClick={handleCheckout}
                className="bg-gradient-to-r from-indigo-600 to-purple-600 text-white text-center py-3 rounded-md font-medium hover:from-indigo-700 hover:to-purple-700 transition-all shadow-md hover:shadow-lg flex items-center justify-center"
              >
                <svg className="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z" />
                </svg>
                إتمام الطلب
              </button>
              <p className="text-center text-sm text-gray-600 mb-2">أو تواصل معنا عبر:</p>
              <div className="grid grid-cols-3 gap-2">
                <a href={whatsappLink} target="_blank" rel="noopener noreferrer" className="bg-green-500 text-white text-center py-2 rounded-md hover:bg-green-600 flex flex-col items-center justify-center">
                  <svg className="w-5 h-5 mb-1" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z" />
                  </svg>
                  <span className="text-xs">واتساب</span>
                </a>
                <a href={telegramLink} target="_blank" rel="noopener noreferrer" className="bg-blue-500 text-white text-center py-2 rounded-md hover:bg-blue-600 flex flex-col items-center justify-center">
                  <svg className="w-5 h-5 mb-1" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M11.944 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 0 0 12 0a12 12 0 0 0-.056 0zm4.962 7.224c.1-.002.439.03.743.336.282.286.287.746.287.746s.083 2.22-.312 3.931c-.358 1.596-1.008 3.115-1.447 4.24-.314.784-.585 1.46-.76 1.903-.423 1.08-.735 1.597-1.207 1.8-.318.13-.627.068-.864-.043-0-.01-2.335-1.468-2.983-1.96-.318-.24-.546-.443-.61-.642-.098-.297.014-.51.09-.717.022-.058.442-1.04.442-1.04s.226-.532-.02-.79c-.236-.24-.543-.216-.69-.21-.18.01-1.16.744-1.16.744-.26.22-.48.26-.765.09-.3-.175-.58-.52-.865-.995-.383-.637-.722-1.39-.722-1.39s-.26-.52-.08-.78c.166-.24.62-.16.62-.16l1.47.09s.3.05.51.22c.18.15.28.41.28.41s.5 1.34.77 2.02c.07.18.23.29.39.3.18.01.42-.06.42-.06s2.48-1.58 2.59-1.67c.1-.08.16-.13.16-.13s.04-.04 0-.1c-.05-.07-.17-.12-.17-.12s-3.86-2.67-4.03-2.81c-.18-.13-.26-.2-.39-.32-.3-.27-.53-.6-.6-.72-.09-.16-.13-.29-.09-.36.06-.11.22-.07.22-.07l1.81.11s.43.05.72.2c.28.15.42.27.63.46.18.16.3.29.45.52.12.18.2.39.25.6.04.16.05.3.03.34-.03.07-.11.11-.11.11s-1.57.9-1.69.98c-.11.07-.2.13-.2.13s-.06.04-.01.13c.04.07.18.21.4.36.22.15.9.59 1.7.95.3.14.54.24.72.31.18.07.3.11.3.11s.12.03.17-.02c.06-.05.06-.18.06-.18s.06-2.3.14-3.04c.02-.22.03-.59.28-.81.2-.18.51-.2.51-.2.08 0 .16.01.23.03z" />
                  </svg>
                  <span className="text-xs">تيليجرام</span>
                </a>
                <a href={phoneLink} className="bg-gray-700 text-white text-center py-2 rounded-md hover:bg-gray-800 flex flex-col items-center justify-center">
                  <svg className="w-5 h-5 mb-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                  </svg>
                  <span className="text-xs">اتصال</span>
                </a>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Cart;
