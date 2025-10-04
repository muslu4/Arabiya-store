import { useEffect, useState } from 'react';
import * as axios from 'axios';
import { Link, useNavigate } from 'react-router-dom';
import { api } from '../api';
import BottomNav from '../components/BottomNav';
import Cart from '../components/CartNew';
import Checkout from '../components/CheckoutNew';
import TopBar from '../components/TopBar';
import BannerSlider from '../components/BannerSlider';
import { formatCurrency } from '../utils/currency';

const Home = ({ user, setUser }) => {
  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('');
  const [cart, setCart] = useState([]);
  const [isCartOpen, setIsCartOpen] = useState(false);
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isCheckoutOpen, setIsCheckoutOpen] = useState(false);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    fetchProducts();
    fetchCategories();
    loadCart();
  }, []);

  const refreshData = () => {
    fetchProducts();
    fetchCategories();
  };

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (isMenuOpen && !event.target.closest('.relative')) {
        setIsMenuOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isMenuOpen]);

  const fetchProducts = async () => {
    try {
      const response = await axios.default.get('http://127.0.0.1:8000/api/products/');
      console.log('API Response:', response);
      const data = response.data;
      const list = Array.isArray(data) ? data : (data?.results || []);
      console.log('Products list:', list);
      // Normalize to match UI expectations
      const normalized = list.map((p) => ({
        ...p,
        image: p.image || p.main_image_url || p.main_image || null,
        stock: typeof p.stock_quantity === 'number' ? p.stock_quantity : (p.is_in_stock ? 1 : 0),
        discount: typeof p.discount_percentage === 'number' ? p.discount_percentage : 0,
      }));
      console.log('Normalized products:', normalized);
      setProducts(normalized);
    } catch (error) {
      console.error('Error fetching products:', error);
      setProducts([]);
    } finally {
      setLoading(false);
    }
  };

  const fetchCategories = async () => {
    try {
      const response = await axios.default.get('http://127.0.0.1:8000/api/products/categories/');
      console.log('Categories API Response:', response);
      const data = response.data;
      const list = Array.isArray(data) ? data : (data?.results || []);
      console.log('Categories list:', list);
      setCategories(list);
    } catch (error) {
      console.error('Error fetching categories:', error);
      setCategories([]);
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
    // Create notification element
    const notification = document.createElement('div');
    notification.className = 'fixed top-4 right-4 bg-green-500 text-white px-6 py-3 rounded-lg shadow-lg z-50 bounce-in';
    notification.textContent = message;
    document.body.appendChild(notification);

    // Remove after 3 seconds
    setTimeout(() => {
      notification.remove();
    }, 3000);
  };

  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setUser(null);
    navigate('/login');
  };

  const toggleCart = () => {
    setIsCartOpen(!isCartOpen);
  };

  const handleCheckout = () => {
    setIsCartOpen(false);
    setIsCheckoutOpen(true);
  };

  const handleCheckoutComplete = () => {
    setCart([]);
    setIsCheckoutOpen(false);
    window.location.reload();
  };

  const filteredProducts = products.filter(product => {
    console.log('Filtering product:', product, 'selectedCategory:', selectedCategory);
    const matchesCategory = !selectedCategory || product.category === selectedCategory;
    const matchesSearch = searchTerm === '' || 
      (product.name && product.name.toLowerCase().includes(searchTerm.toLowerCase())) ||
      (product.description && product.description.toLowerCase().includes(searchTerm.toLowerCase()));
    return matchesCategory && matchesSearch;
  });

  const getCartItemCount = () => {
    return cart.reduce((total, item) => total + item.quantity, 0);
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary-500"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 pb-16">{/* pb for bottom nav */}
      {isCartOpen && <Cart cart={cart} onCartChange={handleCartChange} onClose={toggleCart} handleCheckout={handleCheckout} />}
      {isCheckoutOpen && <Checkout cart={cart} onCheckout={handleCheckoutComplete} onClose={() => setIsCheckoutOpen(false)} />}
      {/* Top bar */}
      <TopBar />
      {/* Banner Slider */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <BannerSlider />
      </div>
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-100 sticky top-0 z-40 backdrop-blur-sm bg-opacity-95">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            {/* Logo and Title */}
            <div className="flex items-center space-x-4 space-x-reverse">
              <div className="relative">
                <img src="/logo192.png" alt="M" className="w-10 h-10 rounded-lg shadow-md" />
                <div className="absolute -bottom-1 -right-1 w-3 h-3 bg-green-500 rounded-full border-2 border-white"></div>
              </div>
              <div>
                <h1 className="text-2xl font-bold gradient-text">MIMI STORE</h1>
                <span className="text-xs text-gray-500 block">متجر إلكتروني عراقي</span>
              </div>
            </div>

            {/* Search + Icons */}
            <div className="flex items-center gap-4">
              {/* Search icon (mobile) */}
              <button className="p-2.5 text-gray-600 hover:text-indigo-600 transition-colors rounded-lg hover:bg-indigo-50 md:hidden">
                <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </button>
              {/* Cart */}
              <div className="relative">
                <button onClick={toggleCart} className="p-2.5 text-gray-600 hover:text-indigo-600 transition-colors rounded-lg hover:bg-indigo-50 relative">
                  <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 3h2l.4 2M7 13h10l4-8H5.4m0 0L7 13m0 0l-2.5 5M7 13l2.5 5m0 0h8" />
                  </svg>
                  {getCartItemCount() > 0 && (
                    <span className="absolute -top-1 -right-1 bg-gradient-to-r from-red-500 to-red-600 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center font-medium shadow-md">
                      {getCartItemCount()}
                    </span>
                  )}
                </button>
              </div>
              {/* Refresh */}
              <button
                onClick={refreshData}
                className="p-2 text-gray-600 hover:text-indigo-600 transition-colors rounded-lg hover:bg-indigo-50"
                title="تحديث البيانات"
              >
                <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
              </button>
              {/* Menu */}
              <div className="relative">
                <button 
                  onClick={() => setIsMenuOpen(!isMenuOpen)} 
                  className="p-2 text-gray-600 hover:text-indigo-600 transition-colors rounded-lg hover:bg-indigo-50"
                >
                  <svg className="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                  </svg>
                </button>
                
                {/* Categories Dropdown */}
                {isMenuOpen && (
                  <div className="absolute right-0 mt-2 w-56 bg-white rounded-xl shadow-xl py-2 z-50 border border-gray-100 overflow-hidden transition-all duration-300 transform origin-top-right">
                    <div className="bg-gradient-to-r from-indigo-500 to-purple-500 px-4 py-2 text-white text-sm font-medium">
                      تصفح حسب الفئة
                    </div>
                    <button
                      onClick={() => {
                        setSelectedCategory('');
                        setIsMenuOpen(false);
                      }}
                      className="block w-full text-right px-4 py-3 text-sm text-gray-700 hover:bg-indigo-50 hover:text-indigo-600 transition-colors flex items-center justify-end"
                    >
                      <span className="mr-2">جميع المنتجات</span>
                      <svg className="h-4 w-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                      </svg>
                    </button>
                    <div className="border-t border-gray-100 my-1"></div>
                    {categories.map(category => (
                      <button
                        key={category.id}
                        onClick={() => {
                          setSelectedCategory(category.id);
                          setIsMenuOpen(false);
                        }}
                        className="block w-full text-right px-4 py-3 text-sm text-gray-700 hover:bg-indigo-50 hover:text-indigo-600 transition-colors flex items-center justify-end"
                      >
                        <span className="mr-2">{category.name}</span>
                        <svg className="h-4 w-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                        </svg>
                      </button>
                    ))}
                  </div>
                )}
              </div>

              {/* Desktop search */}
              <div className="hidden md:block w-72">
                <div className="relative">
                  <input
                    type="text"
                    placeholder="ابحث..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="w-full px-4 py-2 pr-10 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  />
                  <div className="absolute inset-y-0 right-0 pr-3 flex items-center">
                    <svg className="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                    </svg>
                  </div>
                </div>
              </div>

              {/* User */}
              {user ? (
                <div className="hidden md:flex items-center space-x-4 space-x-reverse">
                  <span className="text-gray-700">مرحباً، {user.phone}</span>
                  {user.is_admin && (
                    <Link to="/admin" className="btn-secondary py-2 px-3">لوحة الإدارة</Link>
                  )}
                  <button onClick={logout} className="text-red-600 hover:text-red-700">تسجيل خروج</button>
                </div>
              ) : (
                <Link to="/login" className="hidden md:inline-block btn-primary py-2 px-4">تسجيل دخول</Link>
              )}
            </div>
          </div>
        </div>
      </header>

      {/* Banner Section */}
      <div className="relative w-full h-64 overflow-hidden rounded-xl mx-4 mt-6 shadow-xl bg-gradient-to-r from-indigo-500 to-purple-600 flex items-center justify-center">
        <div className="absolute inset-0 bg-black/20"></div>
        <div className="relative z-10 text-center p-6 text-white">
          <h2 className="text-3xl md:text-4xl font-bold mb-3">مرحباً في MIMI STORE</h2>
          <p className="text-lg md:text-xl mb-4 max-w-2xl mx-auto">أفضل منتجات الإلكترونيات والهواتف الذكية في العراق</p>
          <div className="flex flex-wrap justify-center gap-4 mt-6">
            <Link to="/categories" className="bg-white text-indigo-600 px-6 py-2.5 rounded-lg font-medium hover:bg-indigo-50 transition-colors shadow-lg">
              تصفح الفئات
            </Link>
            <Link to="/offers" className="bg-transparent border-2 border-white text-white px-6 py-2.5 rounded-lg font-medium hover:bg-white/10 transition-colors">
              عروض خاصة
            </Link>
          </div>
        </div>
      </div>



      {/* Categories Filter */}
      <section className="py-8 bg-white border-b border-gray-100 mt-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-wrap justify-center gap-3 md:gap-4">
            <button
              onClick={() => setSelectedCategory('')}
              className={`px-5 py-2.5 rounded-full font-medium transition-all ${selectedCategory === '' ? 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white shadow-md' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'} flex items-center`}
            >
              <svg className="h-4 w-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
              <span className="mr-2">جميع المنتجات</span>
            </button>
            {categories.map(category => (
              <button
                key={category.id}
                onClick={() => setSelectedCategory(category.id)}
                className={`px-5 py-2.5 rounded-full font-medium transition-all ${selectedCategory === category.id ? 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white shadow-md' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'} flex items-center`}
              >
                <svg className="h-4 w-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
                <span className="mr-2">{category.name}</span>
              </button>
            ))}
          </div>
        </div>
      </section>

      {/* Products Grid */}
      <section className="py-12 bg-gradient-to-b from-white to-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h3 className="text-3xl md:text-4xl font-bold mb-4 text-gray-800 inline-block relative">
              منتجاتنا
              <div className="absolute -bottom-2 left-1/2 transform -translate-x-1/2 w-16 h-1 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-full"></div>
            </h3>
            <p className="text-gray-600 max-w-2xl mx-auto">اكتشف أحدث المنتجات الإلكترونية بأفضل الأسعار وجودة في العراق</p>
          </div>

          {filteredProducts.length === 0 ? (
            <div className="text-center py-16 fade-in">
              <div className="inline-block p-6 rounded-full bg-gray-100 mb-6">
                <svg className="w-16 h-16 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
                </svg>
              </div>
              <h3 className="text-2xl font-bold text-gray-700 mb-3">لا توجد منتجات</h3>
              <p className="text-gray-600 max-w-md mx-auto mb-6">لم يتم العثور على منتجات تطابق بحثك. جرب تعديل كلمات البحث أو تصفح جميع الأقسام.</p>
              <div className="flex flex-wrap justify-center gap-4">
                <button 
                  onClick={() => {
                    setSelectedCategory('');
                    setSearchTerm('');
                  }} 
                  className="btn-primary"
                >
                  عرض جميع المنتجات
                </button>
                <button 
                  onClick={() => setSearchTerm('')} 
                  className="btn-secondary"
                >
                  إعادة البحث
                </button>
              </div>
            </div>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 md:gap-8">
              {filteredProducts.map((product, index) => (
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
                      <h4 className="font-bold text-lg text-gray-800 line-clamp-2 flex-1 pr-3">
                        {product.name}
                      </h4>
                      <span className="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded-full whitespace-nowrap">
                        {product.brand || 'علامة تجارية'}
                      </span>
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
                        className="px-4 py-2.5 border border-indigo-500 text-indigo-600 rounded-lg hover:bg-indigo-50 transition-colors flex items-center"
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

      {/* Footer */}
      <footer className="bg-gray-800 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div>
              <h3 className="text-xl font-bold mb-4">MIMI STORE</h3>
              <p className="text-gray-300">
                متجرك الإلكتروني المفضل للحصول على أفضل المنتجات بأسعار مميزة
              </p>
            </div>
            <div>
              <h4 className="font-semibold mb-4">روابط سريعة</h4>
              <ul className="space-y-2 text-gray-300">
                <li><a href="#" className="hover:text-white transition-colors">الرئيسية</a></li>
                <li><a href="#" className="hover:text-white transition-colors">المنتجات</a></li>
                <li><a href="#" className="hover:text-white transition-colors">من نحن</a></li>
                <li><a href="#" className="hover:text-white transition-colors">اتصل بنا</a></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">خدمة العملاء</h4>
              <ul className="space-y-2 text-gray-300">
                <li><a href="#" className="hover:text-white transition-colors">سياسة الإرجاع</a></li>
                <li><a href="#" className="hover:text-white transition-colors">الشحن والتوصيل</a></li>
                <li><a href="#" className="hover:text-white transition-colors">الأسئلة الشائعة</a></li>
                <li><a href="#" className="hover:text-white transition-colors">الدعم الفني</a></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">تواصل معنا</h4>
              <div className="space-y-2 text-gray-300">
                <a href="tel:+9647712345679" className="hover:text-white transition-colors block">📞 +964 771 234 5679</a>
                <a href="https://wa.me/9647712345679" target="_blank" rel="noopener noreferrer" className="hover:text-white transition-colors block">💬 واتساب</a>
                <a href="https://t.me/mimistore" target="_blank" rel="noopener noreferrer" className="hover:text-white transition-colors block">📱 تيليجرام</a>
                <p>📍 بغداد، العراق</p>
              </div>
            </div>
          </div>
          <div className="border-t border-gray-700 mt-8 pt-8 text-center text-gray-300">
            <p>&copy; 2024 MIMI STORE. جميع الحقوق محفوظة.</p>
          </div>
        </div>
      </footer>

      {/* Bottom Navigation (Mobile) */}
      <div className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 md:hidden">
        <div className="grid grid-cols-4 gap-1">
          <button className="flex flex-col items-center py-2 text-primary-600">
            <svg className="h-6 w-6 mb-1" fill="currentColor" viewBox="0 0 24 24">
              <path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z" />
            </svg>
            <span className="text-xs">الرئيسية</span>
          </button>
          <button className="flex flex-col items-center py-2 text-gray-600">
            <svg className="h-6 w-6 mb-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
            <span className="text-xs">البحث</span>
          </button>
          <button className="flex flex-col items-center py-2 text-gray-600 relative">
            <svg className="h-6 w-6 mb-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 3h2l.4 2M7 13h10l4-8H5.4m0 0L7 13m0 0l-2.5 5M7 13l2.5 5m0 0h8" />
            </svg>
            {getCartItemCount() > 0 && (
              <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full h-4 w-4 flex items-center justify-center">
                {getCartItemCount()}
              </span>
            )}
            <span className="text-xs">السلة</span>
          </button>
          <button className="flex flex-col items-center py-2 text-gray-600">
            <svg className="h-6 w-6 mb-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
            <span className="text-xs">الحساب</span>
          </button>
        </div>
      </div>
      {/* Bottom Navigation */}
      <BottomNav />
    </div>
  );
};

export default Home;
