import { useEffect, useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import { api } from '../api';
import { formatCurrency, getFreeShippingThreshold } from '../utils/currency';
import Cart from '../components/CartNew';
import CheckoutNew from '../components/CheckoutNew';

const ProductDetail = ({ user }) => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const [quantity, setQuantity] = useState(1);
  const [selectedImage, setSelectedImage] = useState(0);
  const [cart, setCart] = useState([]);
  const [isCartOpen, setIsCartOpen] = useState(false);
  const [isCheckoutOpen, setIsCheckoutOpen] = useState(false);

  useEffect(() => {
    fetchProduct();
    loadCart();
  }, [id]);

  const fetchProduct = async () => {
    try {
      const response = await api.get(`/products/${id}/`);
      setProduct(response.data);
    } catch (error) {
      console.error('Error fetching product:', error);
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

  const toggleCart = () => {
    setIsCartOpen(!isCartOpen);
  };

  const handleCheckout = () => {
    setIsCartOpen(false);
    setIsCheckoutOpen(true);
  };

  const handleCheckoutComplete = () => {
    setCart([]);
    localStorage.removeItem('cart');
    setIsCheckoutOpen(false);
    showNotification('تم إتمام طلبك بنجاح!');
  };

  const addToCart = () => {
    const existingItem = cart.find(item => item.id === product.id);
    let newCart;

    if (existingItem) {
      newCart = cart.map(item =>
        item.id === product.id
          ? { ...item, quantity: item.quantity + quantity }
          : item
      );
    } else {
      newCart = [...cart, { ...product, quantity }];
    }

    setCart(newCart);
    localStorage.setItem('cart', JSON.stringify(newCart));

    // Show success message
    showNotification(`تم إضافة ${quantity} من ${product.name} للسلة بنجاح!`);
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

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary-500"></div>
      </div>
    );
  }

  if (!product) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="text-gray-400 text-6xl mb-4">😞</div>
          <h2 className="text-2xl font-bold text-gray-600 mb-4">المنتج غير موجود</h2>
          <Link to="/" className="btn-primary">
            العودة للرئيسية
          </Link>
        </div>
      </div>
    );
  }

  // Normalize numeric fields and images to avoid runtime errors
  const priceNum = Number(product?.price ?? 0);
  const discountNum = Number((product?.discount ?? product?.discount_percentage) ?? 0);
  const stockCount = typeof product?.stock_quantity === 'number' ? product.stock_quantity : (product?.is_in_stock ? 1 : 0);
  const finalPrice = discountNum > 0 ? priceNum * (1 - discountNum / 100) : priceNum;

  const productImages = Array.isArray(product?.all_images) && product.all_images.length > 0
    ? product.all_images
    : [product?.main_image || product?.image || 'https://via.placeholder.com/600x400/f3f4f6/9ca3af?text=صورة+المنتج'];

  return (
    <div className="min-h-screen bg-gray-50">
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
                <button onClick={toggleCart} className="p-2 text-gray-600 hover:text-primary-600 transition-colors">
                  <svg className="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 3h2l.4 2M7 13h10l4-8H5.4m0 0L7 13m0 0l-2.5 5M7 13l2.5 5m0 0h8" />
                  </svg>
                  {getCartItemCount() > 0 && (
                    <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center">
                      {getCartItemCount()}
                    </span>
                  )}
                </button>
              </div>
              {user && (
                <span className="text-gray-700">مرحباً، {user.phone}</span>
              )}
            </div>
          </div>
        </div>
      </header>

      {/* Breadcrumb */}
      <div className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <nav className="flex" aria-label="Breadcrumb">
            <ol className="flex items-center space-x-4 space-x-reverse">
              <li>
                <Link to="/" className="text-gray-500 hover:text-primary-600 transition-colors">
                  الرئيسية
                </Link>
              </li>
              <li>
                <svg className="flex-shrink-0 h-5 w-5 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clipRule="evenodd" />
                </svg>
              </li>
              <li>
                <span className="text-gray-700 font-medium">{product.name}</span>
              </li>
            </ol>
          </nav>
        </div>
      </div>

      {/* Product Details */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
          {/* Product Images */}
          <div className="space-y-4">
            {/* Main Image */}
            <div className="aspect-w-1 aspect-h-1 bg-gray-200 rounded-xl overflow-hidden">
              <img
                src={productImages[selectedImage]}
                alt={product.name}
                className="w-full h-96 object-cover"
              />
              {discountNum > 0 && (
                <div className="absolute top-4 right-4 bg-red-500 text-white px-3 py-1 rounded-lg font-bold">
                  -{discountNum}%
                </div>
              )}
              {stockCount <= 5 && stockCount > 0 && (
                <div className="absolute top-4 left-4 bg-orange-500 text-white px-3 py-1 rounded-lg">
                  متبقي {stockCount}
                </div>
              )}
              {stockCount === 0 && (
                <div className="absolute inset-0 bg-black/50 flex items-center justify-center">
                  <span className="text-white font-bold text-2xl">نفد المخزون</span>
                </div>
              )}
            </div>

            {/* Thumbnail Images */}
            {productImages.length > 1 && (
              <div className="flex space-x-4 space-x-reverse overflow-x-auto">
                {productImages.map((image, index) => (
                  <button
                    key={index}
                    onClick={() => setSelectedImage(index)}
                    className={`flex-shrink-0 w-20 h-20 rounded-lg overflow-hidden border-2 transition-colors ${selectedImage === index
                      ? 'border-primary-500'
                      : 'border-gray-200 hover:border-gray-300'
                      }`}
                  >
                    <img
                      src={image}
                      alt={`${product.name} ${index + 1}`}
                      className="w-full h-full object-cover"
                    />
                  </button>
                ))}
              </div>
            )}
          </div>

          {/* Product Info */}
          <div className="space-y-6">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-2">{product.name}</h1>
              {product.category && (
                <p className="text-primary-600 font-medium">{product.category.name}</p>
              )}
            </div>

            {/* Price */}
            <div className="flex items-center space-x-4 space-x-reverse">
              <span className="text-4xl font-bold text-primary-600">
                {formatCurrency(finalPrice)}
              </span>
              {discountNum > 0 && (
                <span className="text-xl text-gray-500 line-through">
                  {formatCurrency(priceNum)}
                </span>
              )}
            </div>

            {/* Description */}
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">وصف المنتج</h3>
              <p className="text-gray-700 leading-relaxed">{product.description}</p>
            </div>

            {/* Features */}
            {product.features && product.features.length > 0 && (
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">المميزات</h3>
                <ul className="space-y-2">
                  {product.features.map((feature, index) => (
                    <li key={index} className="flex items-center space-x-2 space-x-reverse">
                      <svg className="h-5 w-5 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                      </svg>
                      <span className="text-gray-700">{feature}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Stock Status */}
            <div className="flex items-center space-x-2 space-x-reverse">
              <span className="text-gray-700">حالة المخزون:</span>
              {stockCount > 0 ? (
                <span className="text-green-600 font-semibold">
                  متوفر ({stockCount} قطعة)
                </span>
              ) : (
                <span className="text-red-600 font-semibold">نفد المخزون</span>
              )}
            </div>

            {/* Quantity Selector */}
            {product.stock > 0 && (
              <div className="flex items-center space-x-4 space-x-reverse">
                <span className="text-gray-700">الكمية:</span>
                <div className="flex items-center border border-gray-300 rounded-lg">
                  <button
                    onClick={() => setQuantity(Math.max(1, quantity - 1))}
                    className="px-3 py-2 text-gray-600 hover:text-primary-600 transition-colors"
                  >
                    -
                  </button>
                  <span className="px-4 py-2 border-x border-gray-300 font-semibold">
                    {quantity}
                  </span>
                  <button
                    onClick={() => setQuantity(Math.min(product.stock, quantity + 1))}
                    className="px-3 py-2 text-gray-600 hover:text-primary-600 transition-colors"
                  >
                    +
                  </button>
                </div>
              </div>
            )}

            {/* Action Buttons */}
            <div className="flex space-x-4 space-x-reverse">
              <button
                onClick={addToCart}
                disabled={stockCount === 0}
                className={`flex-1 py-4 px-6 rounded-lg font-semibold text-lg transition-all ${stockCount === 0
                  ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                  : 'btn-primary'
                  }`}
              >
                {stockCount === 0 ? 'نفد المخزون' : `أضف للسلة - ${formatCurrency((finalPrice || 0) * quantity)}`}
              </button>
              <button
                onClick={() => {
                  // Get favorites from localStorage
                  const favorites = JSON.parse(localStorage.getItem('favorites') || '[]');
                  const isFavorite = favorites.some(item => item.id === product.id);

                  if (isFavorite) {
                    // Remove from favorites
                    const newFavorites = favorites.filter(item => item.id !== product.id);
                    localStorage.setItem('favorites', JSON.stringify(newFavorites));
                    showNotification('تم إزالة المنتج من المفضلة');
                  } else {
                    // Add to favorites
                    favorites.push(product);
                    localStorage.setItem('favorites', JSON.stringify(favorites));
                    showNotification('تم إضافة المنتج للمفضلة');
                  }
                }}
                className="px-6 py-4 border border-primary-500 text-primary-600 rounded-lg hover:bg-primary-50 transition-colors"
              >
                <svg className="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                </svg>
              </button>
            </div>

            {/* Shipping Info */}
            <div className="bg-gray-50 rounded-lg p-4 space-y-3">
              <div className="flex items-center space-x-3 space-x-reverse">
                <svg className="h-5 w-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
                </svg>
                <span className="text-gray-700">توصيل مجاني للطلبات أكثر من {formatCurrency(getFreeShippingThreshold())}</span>
              </div>
              <div className="flex items-center space-x-3 space-x-reverse">
                <svg className="h-5 w-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span className="text-gray-700">ضمان الجودة والاستبدال</span>
              </div>
              <div className="flex items-center space-x-3 space-x-reverse">
                <svg className="h-5 w-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1" />
                </svg>
                <span className="text-gray-700">دفع آمن ومضمون</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Related Products */}
      <div className="bg-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-8 text-center">منتجات مشابهة</h2>
          <div className="text-center text-gray-500">
            <p>سيتم عرض المنتجات المشابهة هنا</p>
          </div>
        </div>
      </div>

      {/* Cart Component */}
      {isCartOpen && (
        <Cart
          cart={cart}
          onCartChange={setCart}
          onClose={toggleCart}
          handleCheckout={handleCheckout}
        />
      )}

      {/* Checkout Component */}
      {isCheckoutOpen && (
        <CheckoutNew
          cart={cart}
          onCheckout={handleCheckoutComplete}
          onClose={() => setIsCheckoutOpen(false)}
        />
      )}
    </div>
  );
};

export default ProductDetail;
