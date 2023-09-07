from core.models import Product, Category, ListCategory, SubCategory, Vendor, CartOrder, CartOrderItems, ProductImages, ProductReview, Wishlist, Address


def default(request):
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()
    listcategories = ListCategory.objects.all()
    products = Product.objects.all()
    try:
        address = Address.objects.get(user= request.user)
    except:
        address=None
    return{
        'categories': categories,
        'subcategories': subcategories,
        'listcategories': listcategories,
        'address': address,
        'products': products,
        
    }