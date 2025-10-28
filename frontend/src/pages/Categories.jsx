import { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { api, endpoints } from '../api';
import { formatCurrency } from '../utils/currency';
import Footer from '../components/Footer';

const Categories = ({ user }) => {
  const [categories, setCategories] = useState([]);
  const [products, setProducts] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [loading, setLoading] = useState(true);
  const [cart, setCart] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    console.log('Component mounted, fetching initial data');
    fetchCategories();
    loadCart();
  }, []);
  
  // Add a manual refresh button in the UI
  const ManualRefreshButton = () => (
    <button
      onClick={refreshData}
      className="p-2 text-gray-600 hover:text-primary-600 transition-colors"
      title="تحديث البيانات"
    >
      <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
      </svg>
    </button>
  );

  const refreshData = () => {
    console.log('Refreshing data...');
    // Reset selected category to force refresh
    setSelectedCategory(null);
    setCategories([]);
    setProducts([]);
    
    // Fetch fresh data
    setTimeout(() => {
      fetchCategories();
      if (selectedCategory) {
        fetchProductsByCategory(selectedCategory);
      }
    }, 100);
  };

  useEffect(() => {
    if (selectedCategory) {
      fetchProductsByCategory(selectedCategory);
    }
  }, [selectedCategory]);

  const fetchCategories = async () => {
    try {
      setLoading(true);
      const response = await api.get(endpoints.categories);
      const data = response.data;
      const list = Array.isArray(data) ? data : (data?.results || []);
      console.log('Fetched categories:', list);
      setCategories(list);
    } catch (error) {
      console.error('Error fetching categories:', error);
      setCategories([]);
    } finally {
      setLoading(false);
    }
  };

  const fetchProductsByCategory = async (categoryId) => {
    try {
      setLoading(true);
      console.log(`Fetching products for category ID: ${categoryId}`);
      
      // Try using the new endpoint first
      const response = await api.get(`${endpoints.productsByCategory}${categoryId}/products/`);
      const data = response.data;
      const list = Array.isArray(data) ? data : (data?.results || []);
      
      console.log(`Found ${list.length} products for category ${categoryId}`);

      // Normalize to match UI expectations
      const normalized = list.map((p) => ({
        ...p,
        image: p.main_image_url || p.main_image || null,
        stock: typeof p.stock_quantity === 'number' ? p.stock_quantity : (p.is_in_stock ? 1 : 0),
        discount: typeof p.discount_percentage === 'number' ? p.discount_percentage : (p.discount || 0),
      }));

      setProducts(normalized);
      console.log('Normalized products:', normalized);
    } catch (error) {
      console.error('Error fetching products:', error);
      setProducts([]);
    } finally {
      setLoading(false);
    }
  };

  const loadCart = () => {
    const savedCart = localStorage.getItem('cart');
    if (savedCart) {
      setCart(JSON.parse(savedCart));
    }
  };

  const handleCartChange = (newCart) => {
    setCart(newCart);
    localStorage.setItem('cart', JSON.stringify(newCart));
  };

  const addToCart = (product) => {
    const existingItem = cart.find(item => item.id === product.id);
    let newCart;

    if (existingItem) {
      newCart = cart.map(item =>
        item.id === product.id
          ? { ...item, quantity: item.quantity + 1 }
          : item
      );
    } else {
      newCart = [...cart, { ...product, quantity: 1 }];
    }

    handleCartChange(newCart);

    // Show success message
    showNotification('تم إضافة المنتج للسلة بنجاح!');
  };

  const showNotification = (message) => {
    const notification = document.createElement('div');
    notification.className = 'fixed top-4 right-4 bg-green-500 text-white px-6 py-3 rounded-lg shadow-lg z-50 bounce-in';
    notification.textContent = message;
    document.body.appendChild(notification);

    setTimeout(() => {
      notification.remove();
    }, 3000);
  };

  const getCartItemCount = () => {
    return cart.reduce((total, item) => total + item.quantity, 0);
  };

  if (loading && categories.length === 0) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary-500"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 pb-16">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-4 space-x-reverse">
              <button
                onClick={() => navigate(-1)}
                className="p-2 text-gray-600 hover:text-primary-600 transition-colors"
              >
                <svg className="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                </svg>
              </button>
              <Link to="/" className="flex items-center space-x-2 space-x-reverse">
                <div className="bg-gradient-to-r from-primary-500 to-secondary-500 text-white w-8 h-8 rounded-lg flex items-center justify-center font-bold">
                  E
                </div>
                <span className="text-xl font-bold text-primary-600">العربية فون</span>
              </Link>
            </div>

            <div className="flex items-center space-x-4 space-x-reverse">
              <div className="relative">
                <Link to="/" className="p-2 text-gray-600 hover:text-primary-600 transition-colors">
                  <svg className="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 3h2l.4 2M7 13h10l4-8H5.4m0 0L7 13m0 0l-2.5 5M7 13l2.5 5m0 0h8" />
                  </svg>
                  {cart.length > 0 && (
                    <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center">
                      {getCartItemCount()}
                    </span>
                  )}
                </Link>
              </div>
              {/* Refresh */}
              <ManualRefreshButton />
              {user && (
                <span className="text-gray-700">مرحباً، {user.phone}</span>
              )}
            </div>
          </div>
        </div>
      </header>

      {/* Page Title */}
      <div className="bg-gradient-to-r from-amber-800 to-amber-600 py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-3xl md:text-4xl font-bold text-white mb-4">تصفح الفئات</h1>
          <p className="text-xl text-white opacity-90 max-w-2xl mx-auto">
            اكتشف منتجاتنا المميزة المصنفة حسب الفئات
          </p>
        </div>
      </div>

      {/* Categories Grid */}
      {!selectedCategory && (
        <section className="py-12 bg-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            {categories.length === 0 ? (
              <div className="text-center py-16">
                <div className="inline-block p-6 rounded-full bg-gray-100 mb-6">
                  <svg className="w-16 h-16 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                  </svg>
                </div>
                <h3 className="text-2xl font-bold text-gray-700 mb-3">لا توجد فئات</h3>
                <p className="text-gray-600 max-w-md mx-auto mb-6">لا توجد فئات متاحة حالياً</p>
                <Link to="/" className="btn-primary">
                  العودة للرئيسية
                </Link>
              </div>
            ) : (
              <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
                {categories.map((category) => (
                  <div
                    key={category.id}
                    className="bg-white rounded-xl shadow-md overflow-hidden hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1 border border-gray-100 cursor-pointer"
                    onClick={() => setSelectedCategory(category.id)}
                  >
                    <div className="p-6 text-center">
                      <div className="w-16 h-16 bg-gradient-to-r from-amber-100 to-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                        <svg className="h-8 w-8 text-amber-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
                        </svg>
                      </div>
                      <h3 className="text-lg font-semibold text-gray-800 mb-2">{category.name}</h3>
                      <p className="text-gray-600 text-sm mb-4">
                        {category.description || 'اكتشف منتجات هذه الفئة'}
                      </p>
                      <button className="text-indigo-600 font-medium hover:text-indigo-800 transition-colors flex items-center justify-center">
                        عرض المنتجات
                        <svg className="h-4 w-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                        </svg>
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </section>
      )}

      {/* Products Grid */}
      {selectedCategory && (
        <section className="py-12 bg-gradient-to-b from-white to-gray-50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex items-center justify-between mb-8">
              <button
                onClick={() => setSelectedCategory(null)}
                className="flex items-center text-indigo-600 hover:text-indigo-800 transition-colors"
              >
                <svg className="h-5 w-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                </svg>
                العودة للفئات
              </button>
              <h2 className="text-2xl font-bold text-gray-800">
                {categories.find(c => c.id === selectedCategory)?.name || 'المنتجات'}
              </h2>
              <div></div> {/* Empty div for spacing */}
            </div>

            {loading ? (
              <div className="flex justify-center items-center h-64">
                <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-primary-500"></div>
              </div>
            ) : products.length === 0 ? (
              <div className="text-center py-16">
                <div className="inline-block p-6 rounded-full bg-gray-100 mb-6">
                  <svg className="w-16 h-16 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
                  </svg>
                </div>
                <h3 className="text-2xl font-bold text-gray-700 mb-3">لا توجد منتجات</h3>
                <p className="text-gray-600 max-w-md mx-auto mb-6">لا توجد منتجات في هذه الفئة حالياً</p>
                <button
                  onClick={() => setSelectedCategory(null)}
                  className="btn-primary"
                >
                  العودة للفئات
                </button>
              </div>
            ) : (
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 md:gap-8">
                {products.map((product, index) => (
                  <div
                    key={product.id}
                    className="product-card bg-white rounded-xl shadow-md overflow-hidden hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1 border border-gray-100 fade-in cursor-pointer"
                    style={{ animationDelay: `${index * 0.1}s` }}
                    onClick={() => navigate(`/product/${product.id}`)}
                  >
                    {/* Product Image */}
                    <div className="relative overflow-hidden bg-gradient-to-br from-gray-50 to-gray-100 h-64">
                      <img
                        src={product.image || '/placeholder-product.png'}
                        alt={product.name}
                        className="w-full h-full object-cover transition-transform duration-500 hover:scale-105"
                      />
                      {product.discount > 0 && (
                        <div className="absolute top-3 right-3 bg-gradient-to-r from-red-500 to-red-600 text-white px-3 py-1 rounded-full text-xs font-bold shadow-lg flex items-center">
                          <span className="mr-1">خصم</span>
                          <span>{product.discount}%</span>
                        </div>
                      )}
                      {product.stock <= 5 && product.stock > 0 && (
                        <div className="absolute top-3 left-3 bg-gradient-to-r from-orange-500 to-orange-600 text-white px-3 py-1 rounded-full text-sm font-medium shadow-lg flex items-center">
                          <svg className="h-4 w-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                          </svg>
                          <span className="mr-1">متبقي {product.stock}</span>
                        </div>
                      )}
                      {product.stock === 0 && (
                        <div className="absolute inset-0 bg-gradient-to-t from-black/70 to-black/50 flex items-center justify-center">
                          <div className="text-center p-4">
                            <span className="text-white font-bold text-xl block mb-2">نفد المخزون</span>
                            <span className="text-white/80 text-sm">غير متوفر حالياً</span>
                          </div>
                        </div>
                      )}
                    </div>

                    {/* Product Info */}
                    <div className="p-5 bg-gradient-to-b from-white to-gray-50 border-t border-gray-100">
                      <div className="flex justify-between items-start mb-3">
                        <h4 className="font-bold text-lg text-gray-800 line-clamp-3 flex-1 pr-3">
                          {product.name}
                        </h4>
                        {product.brand && (
                          <span className="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded-full whitespace-nowrap">
                            {product.brand}
                          </span>
                        )}
                      </div>
                      <p className="text-gray-600 text-sm mb-4 line-clamp-2 pr-2">
                        {product.description || 'لا يوجد وصف متاح للمنتج'}
                      </p>

                      {/* Price */}
                      <div className="flex items-center justify-between mb-5 pb-3 border-b border-gray-100">
                        <div className="flex items-center space-x-2 space-x-reverse">
                          {product.discount > 0 ? (
                            <>
                              <span className="text-xl font-bold text-indigo-600 flex items-center">
                                {formatCurrency(product.price * (1 - product.discount / 100))}
                                <span className="text-xs text-gray-500 mr-2">د.ع</span>
                              </span>
                              <span className="text-sm text-gray-500 line-through flex items-center">
                                {formatCurrency(product.price)}
                                <span className="text-xs text-gray-500 mr-1">د.ع</span>
                              </span>
                            </>
                          ) : (
                            <span className="text-xl font-bold text-indigo-600 flex items-center">
                              {formatCurrency(product.price)}
                              <span className="text-xs text-gray-500 mr-2">د.ع</span>
                            </span>
                          )}
                        </div>
                      </div>

                      {/* Action Buttons */}
                      <div className="flex space-x-2 space-x-reverse">
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            addToCart(product);
                          }}
                          disabled={product.stock === 0}
                          className={`flex-1 py-2.5 px-4 rounded-lg font-medium transition-all ${product.stock === 0
                            ? 'bg-gray-200 text-gray-500 cursor-not-allowed'
                            : 'btn-primary shadow-md hover:shadow-lg'
                            }`}
                        >
                          {product.stock === 0 ? (
                            <span className="flex items-center justify-center">
                              <svg className="h-4 w-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636" />
                              </svg>
                              نفد المخزون
                            </span>
                          ) : (
                            <span className="flex items-center justify-center">
                              <svg className="h-4 w-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 3h2l.4 2M7 13h10l4-8H5.4m0 0L7 13m0 0l-2.5 5M7 13l2.5 5m0 0h8" />
                              </svg>
                              أضف للسلة
                            </span>
                          )}
                        </button>
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            navigate(`/product/${product.id}`);
                          }}
                          className="px-4 py-2.5 border border-amber-500 text-amber-700 rounded-lg hover:bg-amber-50 transition-colors flex items-center"
                        >
                          <svg className="h-4 w-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                          </svg>
                          تفاصيل
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </section>
      )}
      <Footer />
    </div>
  );
};

export default Categories;
