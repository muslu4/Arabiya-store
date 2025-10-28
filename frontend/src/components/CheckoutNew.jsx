import { useState, useEffect } from 'react';
import { api, endpoints } from '../api';
import { formatCurrency, getFreeShippingThreshold, calculateShippingFee } from '../utils/currency';

const Checkout = ({ cart, onCheckout, onClose, appliedCoupon, couponDiscount }) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);
  const [user, setUser] = useState(null);

  // Load user data and coupon data from localStorage on component mount
  useEffect(() => {
    const userData = localStorage.getItem('user');
    if (userData) {
      try {
        const parsedUser = JSON.parse(userData);
        setUser(parsedUser);
      } catch (error) {
        console.error('Error parsing user data:', error);
      }
    }

    // Load coupon data if not passed as props (fallback to localStorage)
    if (!appliedCoupon && !couponDiscount) {
      const storedCoupon = localStorage.getItem('appliedCoupon');
      const storedDiscount = localStorage.getItem('couponDiscount');
      // Note: We'll use the props if provided, otherwise these can be loaded
    }
  }, [appliedCoupon, couponDiscount]);

  const [formData, setFormData] = useState({
    customerName: '',
    customerPhone: '',
    customerAddress: '',
    governorate: '',
    paymentMethod: 'cash',
  });

  // Update form data when user data is loaded
  useEffect(() => {
    if (user) {
      setFormData({
        customerName: user.name || user.username || '',
        customerPhone: user.phone || '',
        customerAddress: user.address || '',
        governorate: user.governorate || '',
        paymentMethod: 'cash',
      });
    }
  }, [user]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Validation
    if (!formData.customerName.trim()) {
      setError('الرجاء إدخال الاسم');
      return;
    }

    if (!formData.customerPhone.trim()) {
      setError('الرجاء إدخال رقم الهاتف');
      return;
    }

    if (!formData.customerAddress.trim()) {
      setError('الرجاء إدخال العنوان الكامل');
      return;
    }

    if (!formData.governorate) {
      setError('الرجاء اختيار المحافظة');
      return;
    }

    setLoading(true);
    setError('');

    // Validate cart is not empty
    if (!cart || cart.length === 0) {
      setError('سلة التسوق فارغة. يرجى إضافة منتجات قبل إتمام الطلب.');
      setLoading(false);
      return;
    }

    try {
      // Calculate subtotal and total weight
      const subtotal = cart.reduce((sum, item) => {
        const itemPrice = item.price || 0;
        const itemQuantity = item.quantity || 0;
        return sum + (itemPrice * itemQuantity);
      }, 0);

      // Calculate total weight (in kg)
      const totalWeight = cart.reduce((sum, item) => {
        const itemWeight = item.weight || 0.5; // افتراض 0.5 كجم إذا لم يكن الوزن محدداً
        const itemQuantity = item.quantity || 0;
        return sum + (itemWeight * itemQuantity);
      }, 0);

      // Calculate delivery fee based on weight
      const deliveryFee = calculateShippingFee(totalWeight, subtotal);
      // Calculate total with coupon discount applied
      const totalAfterCoupon = subtotal + deliveryFee - (couponDiscount || 0);

      // Prepare order data matching backend expectations
      const orderData = {
        customer_name: formData.customerName,
        customer_phone: formData.customerPhone,
        customer_email: formData.customerEmail || '',
        customer_address: formData.customerAddress,
        governorate: formData.governorate,
        additional_info: formData.additionalInfo || '',
        payment_method: formData.paymentMethod === 'cash' ? 'cash_on_delivery' : 'bank_transfer',
        subtotal: subtotal,
        delivery_fee: deliveryFee,
        coupon_code: appliedCoupon?.code || null,
        coupon_discount: couponDiscount || 0,
        total: totalAfterCoupon,
        items: cart.map(item => ({
          product_id: item.id,
          product_name: item.name,
          price: item.price,
          quantity: item.quantity,
          total_price: item.price * item.quantity
        })),
      };

      console.log('Sending order data:', orderData); // Log the data being sent

      // Send order to backend using create endpoint
      const response = await api.post(endpoints.createOrder, orderData);

      // Clear cart and show success message
      localStorage.removeItem('cart');
      onCheckout();
      setSuccess(true);

      // Redirect to home after 3 seconds
      setTimeout(() => {
        onClose();
      }, 3000);

    } catch (err) {
      console.error('Error creating order:', err);
      console.error('Error response:', err.response);
      console.error('Error data:', err.response?.data);
      console.error('Error status:', err.response?.status);

      // عرض رسالة خطأ أكثر تفصيلاً
      if (err.response?.data?.message) {
        setError(`حدث خطأ: ${err.response.data.message}`);
      } else if (err.response?.status === 400) {
        setError('بيانات الطلب غير صالحة. يرجى التحقق من جميع الحقول المطلوبة.');
      } else if (err.response?.status === 500) {
        setError('حدث خطأ في الخادم. يرجى المحاولة مرة أخرى لاحقاً.');
      } else {
        setError('حدث خطأ أثناء إرسال الطلب. يرجى المحاولة مرة أخرى.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4" onClick={onClose}>
      <div className="bg-white rounded-xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto" onClick={(e) => e.stopPropagation()}>
        <div className="p-6">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-bold text-gray-800">إتمام الطلب</h2>
            <button 
              onClick={onClose}
              className="text-gray-500 hover:text-gray-700 p-1 rounded-full hover:bg-gray-100"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          {success ? (
            <div className="text-center py-12">
              <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-8 h-8 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <h3 className="text-xl font-bold text-gray-800 mb-2">تم إتمام الطلب بنجاح!</h3>
              <p className="text-gray-600">سيتم التواصل معك قريباً لتأكيد تفاصيل الطلب</p>
            </div>
          ) : (
            <>
              {error && (
                <div className="mb-6 p-3 bg-red-50 text-red-700 rounded-lg flex items-center">
                  <svg className="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  {error}
                </div>
              )}

              <form onSubmit={handleSubmit}>
                <div className="mb-6">
                  <h3 className="text-lg font-semibold mb-4 text-gray-700">معلومات العميل</h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-gray-700 mb-2">الاسم الكامل *</label>
                      <input
                        type="text"
                        name="customerName"
                        value={formData.customerName}
                        onChange={handleInputChange}
                        className="input-field"
                        required
                      />
                    </div>
                    <div>
                      <label className="block text-gray-700 mb-2">رقم الهاتف *</label>
                      <input
                        type="tel"
                        name="customerPhone"
                        value={formData.customerPhone}
                        onChange={handleInputChange}
                        className="input-field"
                        required
                      />
                    </div>


                  </div>
                </div>

                <div className="mb-6">
                  <h3 className="text-lg font-semibold mb-4 text-gray-700">عنوان التوصيل *</h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-gray-700 mb-2">المحافظة *</label>
                      <select
                        name="governorate"
                        value={formData.governorate}
                        onChange={handleInputChange}
                        className="input-field"
                        required
                      >
                        <option value="">اختر المحافظة</option>
                        <option value="بغداد">بغداد</option>
                        <option value="البصرة">البصرة</option>
                        <option value="الموصل">الموصل</option>
                        <option value="النجف">النجف</option>
                        <option value="كربلاء">كربلاء</option>
                        <option value="الأنبار">الأنبار</option>
                        <option value="أربيل">أربيل</option>
                        <option value="دهوك">دهوك</option>
                        <option value="السليمانية">السليمانية</option>
                        <option value="ميسان">ميسان</option>
                        <option value="واسط">واسط</option>
                        <option value="ديالى">ديالى</option>
                        <option value="صلاح الدين">صلاح الدين</option>
                        <option value="نينوى">نينوى</option>
                        <option value="بابل">بابل</option>
                        <option value="ذي قار">ذي قار</option>
                        <option value="القادسية">القادسية</option>
                        <option value="مثنى">مثنى</option>
                        <option value="كركوك">كركوك</option>
                      </select>
                    </div>
                    <div className="md:col-span-2">
                      <label className="block text-gray-700 mb-2">العنوان الكامل *</label>
                      <textarea
                        name="customerAddress"
                        value={formData.customerAddress}
                        onChange={handleInputChange}
                        className="input-field"
                        rows="3"
                        placeholder="أدخل العنوان بالتفصيل (المنطقة، الشارع، رقم المبنى، الطابق، الشقة، إلخ)"
                        required
                      ></textarea>
                    </div>
                  </div>
                  </div>

                <div className="mb-6">
                  <h3 className="text-lg font-semibold mb-4 text-gray-700">طريقة الدفع</h3>
                  <div className="space-y-3">
                    <label className="flex items-center p-3 border rounded-lg cursor-pointer hover:bg-gray-50">
                      <input
                        type="radio"
                        name="paymentMethod"
                        value="cash"
                        checked={formData.paymentMethod === 'cash'}
                        onChange={handleInputChange}
                        className="ml-2"
                      />
                      <span className="mr-2">الدفع عند الاستلام</span>
                    </label>
                    <label className="flex items-center p-3 border rounded-lg cursor-pointer hover:bg-gray-50">
                      <input
                        type="radio"
                        name="paymentMethod"
                        value="bank_transfer"
                        checked={formData.paymentMethod === 'bank_transfer'}
                        onChange={handleInputChange}
                        className="ml-2"
                      />
                      <span className="mr-2">تحويل بنكي</span>
                    </label>
                  </div>
                </div>

                <div className="mb-6">
                  <h3 className="text-lg font-semibold mb-4 text-gray-700">ملف الطلب</h3>
                  <div className="bg-gray-50 rounded-lg p-4">
                    <div className="space-y-3">
                      {cart.map(item => (
                        <div key={item.id} className="flex justify-between">
                          <span>{item.name} × {item.quantity}</span>
                          <span>{formatCurrency(item.price * item.quantity)}</span>
                        </div>
                      ))}
                    </div>
                    <div className="border-t border-gray-200 mt-3 pt-3 space-y-2">
                      <div className="flex justify-between text-gray-700">
                        <span>المجموع الفرعي:</span>
                        <span>{formatCurrency(cart.reduce((total, item) => total + (item.price * item.quantity), 0))}</span>
                      </div>
                      {(() => {
                        const subtotal = cart.reduce((total, item) => total + (item.price * item.quantity), 0);
                        const totalWeight = cart.reduce((sum, item) => {
                          const itemWeight = item.weight || 0.5; // افتراض 0.5 كجم إذا لم يكن الوزن محدداً
                          const itemQuantity = item.quantity || 0;
                          return sum + (itemWeight * itemQuantity);
                        }, 0);
                        const shippingCost = calculateShippingFee(totalWeight, subtotal);
                        return (
                          <>
                            <div className="flex justify-between text-gray-700">
                              <span>أجور التوصيل:</span>
                              <span className={shippingCost === 0 ? 'text-green-600 font-medium' : ''}>
                                {shippingCost === 0 ? 'مجاني' : formatCurrency(shippingCost)}
                              </span>
                            </div>
                            {couponDiscount > 0 && (
                              <div className="flex justify-between text-green-600 font-medium">
                                <span>خصم الكوبون:</span>
                                <span>-{formatCurrency(couponDiscount)}</span>
                              </div>
                            )}
                            {subtotal < getFreeShippingThreshold() && (
                              <div className="text-xs text-gray-500 text-center py-1">
                                أضف {formatCurrency(getFreeShippingThreshold() - subtotal)} للحصول على توصيل مجاني
                              </div>
                            )}
                            <div className="flex justify-between font-bold text-lg border-t pt-2">
                              <span>الإجمالي:</span>
                              <span>{formatCurrency(subtotal + shippingCost - (couponDiscount || 0))}</span>
                            </div>
                          </>
                        );
                      })()}
                    </div>
                  </div>
                </div>

                <div className="flex justify-end space-x-3">
                  <button
                    type="button"
                    onClick={onClose}
                    className="px-6 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50"
                  >
                    إلغاء
                  </button>
                  <button
                    type="submit"
                    disabled={loading}
                    className="px-6 py-2 bg-gradient-to-r from-amber-800 to-green-700 text-white rounded-lg font-medium hover:from-amber-900 hover:to-green-800 transition-all disabled:opacity-70"
                  >
                    {loading ? 'جاري الإرسال...' : 'إتمام الطلب'}
                  </button>
                </div>
              </form>
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default Checkout;