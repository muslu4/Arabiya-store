import { useState } from 'react';
import { api, endpoints } from '../api';
import { formatCurrency } from '../utils/currency';

const Checkout = ({ cart, onCheckout, onClose }) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);
  const [formData, setFormData] = useState({
    customerName: '',
    customerPhone: '',
    customerEmail: '',
    customerAddress: '',
    governorate: '',
    city: '',
    neighborhood: '',
    buildingNumber: '',
    apartmentNumber: '',
    additionalInfo: '',
    paymentMethod: 'cash_on_delivery', // Default payment method
  });

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
      setError('الرجاء إدخال العنوان');
      return;
    }

    if (!formData.governorate) {
      setError('الرجاء اختيار المحافظة');
      return;
    }

    if (!formData.city) {
      setError('الرجاء اختيار المدينة');
      return;
    }

    setLoading(true);
    setError('');

    try {
      // Prepare order data
      const orderData = {
        customer_info: {
          name: formData.customerName,
          phone: formData.customerPhone,
          email: formData.customerEmail,
          address: formData.customerAddress,
          governorate: formData.governorate,
          city: formData.city,
          neighborhood: formData.neighborhood,
          building_number: formData.buildingNumber,
          apartment_number: formData.apartmentNumber,
          additional_info: formData.additionalInfo,
          payment_method: formData.paymentMethod,
        },
        items: cart.map(item => ({
          product_id: item.id,
          name: item.name,
          price: item.price,
          quantity: item.quantity,
          total_price: item.price * item.quantity,
        })),
        subtotal: cart.reduce((total, item) => total + (item.price * item.quantity), 0),
        delivery_fee: 5.0, // Fixed delivery fee
        total: cart.reduce((total, item) => total + (item.price * item.quantity), 0) + 5.0,
      };

      // Send order to backend
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
      let errorMessage = 'حدث خطأ أثناء إرسال الطلب. ';
      
      // Check for specific error types
      if (err.response) {
        // Server responded with error status
        if (err.response.status === 401) {
          errorMessage += 'انتهت جلسة العمل. يرجى تسجيل الدخول مرة أخرى.';
        } else if (err.response.status === 500) {
          errorMessage += 'حدث خطأ في الخادم. يرجى المحاولة مرة أخرى لاحقًا.';
        } else if (err.response.status === 404) {
          errorMessage += 'الخدمة غير متاحة مؤقتًا. يرجى المحاولة مرة أخرى لاحقًا.';
        } else {
          errorMessage += 'يرجى التأكد من اتصالك بالإنترنت والمحاولة مرة أخرى.';
        }
      } else if (err.request) {
        // Request was made but no response received
        errorMessage += 'لا يوجد اتصال بالإنترنت. يرجى التحقق من اتصالك والمحاولة مرة أخرى.';
      } else {
        // Something happened in setting up the request
        errorMessage += 'حدث خطأ غير متوقع. يرجى المحاولة مرة أخرى.';
      }
      
      errorMessage += ' إذا استمرت المشكلة، يرجى التواصل مع خدمة العملة على الرقم 07701234567.';
      
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
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
                    <div>
                      <label className="block text-gray-700 mb-2">البريد الإلكتروني</label>
                      <input
                        type="email"
                        name="customerEmail"
                        value={formData.customerEmail}
                        onChange={handleInputChange}
                        className="input-field"
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
                        <option value="قضاء الكرخ">قضاء الكرخ</option>
                        <option value="قضاء الرصافة">قضاء الرصافة</option>
                      </select>
                    </div>
                    <div>
                      <label className="block text-gray-700 mb-2">المدينة *</label>
                      <input
                        type="text"
                        name="city"
                        value={formData.city}
                        onChange={handleInputChange}
                        className="input-field"
                        required
                      />
                    </div>
                    <div>
                      <label className="block text-gray-700 mb-2">حي المنطقة</label>
                      <input
                        type="text"
                        name="neighborhood"
                        value={formData.neighborhood}
                        onChange={handleInputChange}
                        className="input-field"
                      />
                    </div>
                    <div>
                      <label className="block text-gray-700 mb-2">رقم المبنى</label>
                      <input
                        type="text"
                        name="buildingNumber"
                        value={formData.buildingNumber}
                        onChange={handleInputChange}
                        className="input-field"
                      />
                    </div>
                    <div>
                      <label className="block text-gray-700 mb-2">رقم الشقة</label>
                      <input
                        type="text"
                        name="apartmentNumber"
                        value={formData.apartmentNumber}
                        onChange={handleInputChange}
                        className="input-field"
                      />
                    </div>
                  </div>
                  <div className="mt-4">
                    <label className="block text-gray-700 mb-2">العنوان الكامل *</label>
                    <input
                      type="text"
                      name="customerAddress"
                      value={formData.customerAddress}
                      onChange={handleInputChange}
                      className="input-field"
                      required
                    />
                  </div>
                  <div className="mt-4">
                    <label className="block text-gray-700 mb-2">ملاحظات إضافية</label>
                    <textarea
                      name="additionalInfo"
                      value={formData.additionalInfo}
                      onChange={handleInputChange}
                      className="input-field"
                      rows={2}
                    ></textarea>
                  </div>
                </div>

                <div className="mb-6">
                  <h3 className="text-lg font-semibold mb-4 text-gray-700">طريقة الدفع</h3>
                  <div className="space-y-3">
                    <label className="flex items-center p-3 border rounded-lg cursor-pointer hover:bg-gray-50">
                      <input
                        type="radio"
                        name="paymentMethod"
                        value="cash_on_delivery"
                        checked={formData.paymentMethod === 'cash_on_delivery'}
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
                    {cart.length === 0 ? (
                      <p className="text-gray-500 text-center">السلة فارغة</p>
                    ) : (
                      <div className="space-y-3">
                        {cart.map((item) => (
                          <div key={item.id} className="flex justify-between items-center py-2 border-b border-gray-200">
                            <div className="flex-1">
                              <h4 className="font-medium">{item.name}</h4>
                              <p className="text-sm text-gray-500">الكمية: {item.quantity}</p>
                            </div>
                            <div className="text-right">
                              <p className="font-medium">{formatCurrency(item.price)} د.ع</p>
                              <p className="text-sm text-gray-500">المجموع: {formatCurrency(item.price * item.quantity)} د.ع</p>
                            </div>
                          </div>
                        ))}
                        <div className="flex justify-between py-3 font-semibold">
                          <span>المجموع الفرعي</span>
                          <span>{formatCurrency(cart.reduce((total, item) => total + (item.price * item.quantity), 0))} د.ع</span>
                        </div>
                        <div className="flex justify-between py-3">
                          <span>رسوم التوصيل</span>
                          <span>{formatCurrency(5.0)} د.ع</span>
                        </div>
                        <div className="flex justify-between py-3 text-lg font-bold text-indigo-600">
                          <span>الإجمالي</span>
                          <span>{formatCurrency(cart.reduce((total, item) => total + (item.price * item.quantity), 0) + 5.0)} د.ع</span>
                        </div>
                      </div>
                    )}
                  </div>
                </div>

                <div className="flex justify-end gap-4">
                  <button
                    type="button"
                    onClick={onClose}
                    className="px-6 py-3 border border-gray-300 rounded-lg font-medium text-gray-700 hover:bg-gray-50 transition-colors"
                  >
                    إلغاء
                  </button>
                  <button
                    type="submit"
                    disabled={loading || cart.length === 0}
                    className="px-6 py-3 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-lg font-medium hover:shadow-lg transition-all disabled:opacity-50"
                  >
                    {loading ? (
                      <span className="flex items-center justify-center">
                        <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                        جاري الإرسال...
                      </span>
                    ) : (
                      'إتمام الطلب'
                    )}
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
