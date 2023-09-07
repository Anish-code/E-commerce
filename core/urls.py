from django.urls import include, path

from core.views import add_to_cart, add_to_wishlist, addressbook, ajax_add_review, cart_view, category_list_view, checkout_view, dashboard, delete_item_from_cart, download_invoice, index, listcategory_product_list_view, order_detail, payment_completed_view, payment_failed_view, product_detail_view, product_list_view, search_view, subcategory_list_view, subcategory_product_list_view, tag_list, update_cart, vendors_detail_view, vendor_list_view, wishlist_view

app_name="core"

urlpatterns = [
    path('', index, name="index"),
    path('category/', category_list_view, name="category-list"),
    path('category/<cid>/', subcategory_list_view, name="subcategory-list"),
    path('subcategory/<scid>/', subcategory_product_list_view, name="subcategory-product-list"),
    path('listcategory/<lcid>/', listcategory_product_list_view, name="liscategory-product-list"),
    path('vendors/', vendor_list_view, name="vendor-list"),
    path('vendor/<vid>/', vendors_detail_view, name="vendors-detail"),
    path('product/<pid>/', product_detail_view, name="product-detail"),
    path('products/', product_list_view, name="product-list"),
    path('products/tags/<slug:tag_slug>', tag_list, name="tags"),
    
    path("ajax-add-review/<pid>/", ajax_add_review, name="ajax-add-review"),
    
    path("search/", search_view, name="search"),
    
    
    path("add-to-cart/", add_to_cart, name='add_to_cart'),
    path("cart/", cart_view, name='cart'),
    
    
    path("delete-from-cart/", delete_item_from_cart, name="delete-from-cart"),
    
    path("update-cart/", update_cart, name="update-cart"),
    
    
    path("checkout/", checkout_view, name="checkout"),
    
    path('paypal/', include('paypal.standard.ipn.urls'), name="paypal-ipn"),
    
    path("payment-completed/", payment_completed_view, name="payment-completed"),
    
    
    path("payment-failed/", payment_failed_view, name="payment-failed"),
    
    
  
    
    path('download-invoice/', download_invoice, name='download_invoice'),
    
    path('dashboard/', dashboard, name='dashboard'),
    
    
    path('dashboard/order/<int:id>', order_detail, name='order-detail'),
    
    
    path('dashboard/address/', addressbook, name='addressbook'),
    
    path('wishlist/', wishlist_view, name='wishlist'),
    
    path('add-to-wishlist/', add_to_wishlist, name="add-to-wishlist"),
    
    

]