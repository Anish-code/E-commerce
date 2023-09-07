from decimal import Decimal
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Count, Avg
from core.models import Product, Category, SubCategory, ListCategory,  Vendor, CartOrder, CartOrderItems, ProductImages, ProductReview, Wishlist, Address
from taggit.models import Tag
from core.forms import ProductReview, ProductReviewform
from django.contrib import messages
from django.template.loader import render_to_string
import xmltodict
import requests
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle




# Create your views here.
def index(request):
    productsfeatured = Product.objects.filter(product_status= "published", featured = True).order_by("-id")
    context = {
        "productsfeatured": productsfeatured,
        
    }
    
    return render(request, 'core/index.html', context)

def product_list_view(request):
    products= Product.objects.filter(product_status="published")
    context = {
        "products": products,
        
    }
    return render(request, 'core/product-list.html', context)


def category_list_view(request):
    categories = Category.objects.all().annotate(product_count= Count("category"))
    context = {
        "categories": categories,
    }
    return render(request, 'core/category-list.html', context)

def subcategory_list_view(request, cid):
    category= Category.objects.get(cid= cid)
    subcategories= SubCategory.objects.filter(category= category)
    context = {
        "category": category,
        "subcategories": subcategories,
    }
    return render(request, 'core/subcategory-list.html', context)   


def listcategory_list_view(request, scid):
    subcategory= SubCategory.objects.get(scid= scid)
    listcategories= ListCategory.objects.filter(subcategory= subcategory)
    context = {
        "subcategory": subcategory,
        "listcategories": listcategories,
    }
    return render(request, 'core/listcategory-list.html', context)  


def subcategory_product_list_view(request, scid):
    
    subcategory = SubCategory.objects.get(scid = scid)
    category= Category.objects.all()
    products = Product.objects.filter(product_status= "published", subcategory=subcategory)
    
    
    
    context = {
        
        "subcategory": subcategory,
        "products": products,
        "category": category,
        
    }
    return render(request, "core/subcategory-product-list.html", context)


def listcategory_product_list_view(request, lcid):
    
    listcategory = ListCategory.objects.get(lcid = lcid)
    category= Category.objects.all()
    products = Product.objects.filter(product_status= "published", listcategory=listcategory)
    
    
    
    context = {
        
        
        "listcategory": listcategory,
        "products": products,
        "category": category,
        
    }
    return render(request, "core/listcategory-product-list.html", context)


def vendor_list_view(request):
    vendors= Vendor.objects.all()
   
    context = {
        "vendors": vendors,
        
        
    }
    return render(request, "core/vendor-list.html", context)



def vendors_detail_view(request, vid):
    vendors= Vendor.objects.get(vid = vid)
    products = Product.objects.filter(vendor= vendors, product_status="published")
    context = {
        "vendors": vendors,
        "products": products,
    }
    return render(request, "core/vendors-detail.html", context)

def product_detail_view(request, pid):
    product= Product.objects.get(pid= pid)
    products= Product.objects.filter(category= product.category).exclude(pid=pid)
    p_image= product.p_images.all()
    # getting all the product reviews
    reviews = ProductReview.objects.filter(product= product).order_by("-date")
    
    # getting average review
    average_rating = ProductReview.objects.filter(product= product).aggregate(rating= Avg('rating'))
    
    #product Review form
    review_form= ProductReviewform()
    make_review = True
    
    if request.user.is_authenticated:
        user_review_count= ProductReview.objects.filter(user=request.user, product= product).count()
        
        if user_review_count > 0:
            make_review =False
            
    
    
    context ={
        "p": product,
        "products": products,
        "p_image": p_image,
        "make_review": make_review,
        "reviews": reviews,
        "average_rating": average_rating,
        "review_form": review_form,
        
    }
    
    return render(request, "core/product-detail.html", context)
 
 
def tag_list(request, tag_slug= None):
    products= Product.objects.filter(product_status= "published").order_by("-id")
    tag= None
    
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        products = products.filter(tag__in=[tag])
        
    context ={
        "products": products,
        
    }
    
    return render(request, "core/tag.html", context)
        
def ajax_add_review(request, pid):
    product= Product.objects.get(pid=pid)
    user= request.user
    
    review= ProductReview.objects.create(
        
        user= user,
        product= product,
        review= request.POST['review'],
        rating= request.POST['rating'],
        
        
    )
    
    context = {
        'user': user.username,
        'review': request.POST['review'],
        'rating': request.POST['rating'],
        
    }
    
    average_reviews= ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))
    
    return JsonResponse(
        {
            'bool': True,
            'context': context,
            'avg_reviews': average_reviews,
        
        }
    )
    

def search_view(request):
    query = request.GET.get("q") 
    
    products = Product.objects.filter(title__icontains= query).order_by("-date")
    
    context = {
        "products": products,
        "query": query,
        
    } 
    
    return render(request, "core/search.html", context)


def add_to_cart(request):
    cart_product = {}
    
    
    cart_product[str(request.GET['id'])] = {
        'title': request.GET['title'],
        'qty': request.GET['qty'],
        
        'price': request.GET['price'],

        'image': request.GET['image'],
        'pid': request.GET['pid'],
        
        
    }
    
    
    if 'cart_data_obj' in request.session:
        if str(request.GET['id']) in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = int(cart_product[str(request.GET['id'])]['qty'])
            cart_data.update(cart_data)
            request.session['cart_data_obj'] = cart_data
        
        else:
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_product)
            request.session['cart_data_obj'] = cart_data
            
    else:
        request.session['cart_data_obj']= cart_product
    
    return JsonResponse({"data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj'])})


def cart_view(request):
    cart_total_amt=0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amt += int(item['qty']) * float(item['price'])
        return render(request, 'core/cart.html',{"cart_data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amt': cart_total_amt})
    
    else:
        messages.warning(request, "Your cart is empty")
        return redirect("core:index")


   

def delete_item_from_cart(request):
    product_id= str(request.GET['id'])
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data= request.session["cart_data_obj"]
            del request.session['cart_data_obj'][product_id]
            request.session['cart_data_obj'] = cart_data
            
            
        cart_total_amt=0
        if 'cart_data_obj' in request.session:
            for p_id, item in request.session['cart_data_obj'].items():
                cart_total_amt += int(item['qty']) * float(item['price'])
            
    context = render_to_string('core/async/cart.html',{"cart_data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amt': cart_total_amt})
    return JsonResponse({"data": context})
            
    
def update_cart(request):
    product_id= str(request.GET['id'])
    product_qty= request.GET['qty']
    
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data= request.session["cart_data_obj"]
            cart_data[str(request.GET["id"])]['qty']= product_qty
            request.session['cart_data_obj'] = cart_data
            
            
        cart_total_amt=0
        if 'cart_data_obj' in request.session:
            for p_id, item in request.session['cart_data_obj'].items():
                cart_total_amt += int(item['qty']) * float(item['price'])
            
    context = render_to_string('core/async/cart.html',{"cart_data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amt': cart_total_amt})
    return JsonResponse({"data": context})  

import uuid
     
@login_required
def checkout_view(request):
    cart_total_amt=0
    total_amount = 0
    
    if 'cart_data_obj' in request.session:
        # Getting total amount for esewa
        
        for p_id, item in request.session['cart_data_obj'].items():
            total_amount += int(item['qty']) * float(item['price'])
        
        
        # Create Order object
        
        order= CartOrder.objects.create(
            user=request.user,
            price=total_amount,
 
            
        )
        
        # Getting total amount for the cart
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amt += int(item['qty']) * float(item['price'])
            
            cart_order_items = CartOrderItems.objects.create(
                order= order,
                invoice_no= "INVOICE_NO-"+ str(order.id),
                item=item['title'],
                image=item['image'],
                qty=item['qty'],
                price=item['price'],
                total=float(item['qty'])*float(item['price'])
                
            )
            
    # esewa
    url ="https://uat.esewa.com.np/epay/transrec"
    data = {
            'amt': cart_total_amt,
            'scd': 'EPAYTEST',
            'rid': "refId"+ str(order.id),
            'pid':uuid.uuid4(),
        }
            
                
            
    
    # pid= uuid.uuid4()
    host = request.get_host()
    paypal_dict= {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': cart_total_amt,
        'item_name': "Order-Item_No-"+str(order.id),
        'invoice': "INvoice-No-"+str(order.id),
        'currency_code': "USD",
        'notify_url': "https://{}{}".format(host, reverse("core:paypal-ipn")),
        'return_url': "https://{}{}".format(host, reverse("core:payment-completed")),
        'cancel_url': "https://{}{}".format(host, reverse("core:payment-failed")),   
    }
    
    paypal_payment_button = PayPalPaymentsForm(initial=paypal_dict)
    pid=uuid.uuid4()
    cart_total_amt = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            qty = int(item.get('qty', 0))
            price = item.get('price', '0')
            if price and price.replace('.', '', 1).isdigit():
                cart_total_amt += qty * float(price)
        return render(request, 'core/checkout.html', {"cart_data": request.session['cart_data_obj'], 
                                                      'totalcartitems': len(request.session['cart_data_obj']),
                                                      'cart_total_amt': cart_total_amt, 
                                                      'pid':pid,
                                                      'paypal_payment_button': paypal_payment_button})

     
    return render(request, 'core/checkout.html')

@login_required
def esewa_callback_view(request):
    order_id = request.GET.get("order_id")
    price = request.GET.get("price")
    refId = request.GET.get("refId")
    url ="https://uat.esewa.com.np/epay/transrec"
    data = {
            'amt': price,
            'scd': 'EPAYTEST',
            'rid': refId,
            'pid':order_id,
        }
    cart_total_amt = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            qty = int(item.get('qty', 0))
            price = item.get('price', '0')
            if price and price.replace('.', '', 1).isdigit():
                cart_total_amt += qty * float(price)
    response = requests.post(url, data=data)
    json_response =xmltodict.parse(response.content)
    status = json_response["response"]["response_code"]

    if status != "Success":
        return redirect("payment_failed")
    cartorder = get_object_or_404(CartOrder,order_id=order_id)

    cartorder.paid_status=True
    if cartorder.price != int(cart_total_amt):
     return redirect("payment_failed")
    cartorder.price =int(float(cart_total_amt))
    cartorder.save()
    return render(request,'core/payment-completed.html')


@login_required
def payment_failed(request):
    return render(request,'core/payment_failed.html')


@login_required
def payment_completed_view(request):
    cart_total_amt = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            qty = int(item.get('qty', 0))
            price = item.get('price', '0')
            if price and price.replace('.', '', 1).isdigit():
                cart_total_amt += qty * float(price)

    
    return render(request, 'core/payment-completed.html', {"cart_data": request.session['cart_data_obj'], 
                                                      'totalcartitems': len(request.session['cart_data_obj']),
                                                      'cart_total_amt': cart_total_amt
                                                      })



def payment_failed_view(request):
    return render(request, 'core/payment-failed.html')


@login_required
def download_invoice(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'

    doc = SimpleDocTemplate(response, pagesize=landscape(letter))
    elements = []
    cart_total_amt = 0
    if 'cart_data_obj' in request.session:
        cart_data_obj = request.session['cart_data_obj']
        for p_id, item in cart_data_obj.items():
            cart_total_amt += int(item['qty']) * float(item['price'])
        
    cart_data = cart_data_obj  # Assuming this method fetches cart data from somewhere
    
    data = [['Item', 'Unit Price', 'Quantity', 'Price']]
    for product_id, item in cart_data.items():
        data.append([
            item['title'],
            item['price'],
            item['qty'],
            float(item['price']) * int(item['qty']),
        ])
    data.append(['Total:','','', cart_total_amt])
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(table)

    doc.build(elements)
    return response


@login_required
def dashboard(request):
    orders = CartOrder.objects.filter(user= request.user).order_by("-id")
    address= Address.objects.filter(user=request.user)
    # if request.method == "POST":
    #     address=request.POST.get("address")
    #     phoneno=request.POST.get("phoneno")
    #     email=request.POST.get("email")
        
    #     new_address= Address.objects.create(
    #         user=request.user,
    #         address= address,
    #         contact_no= phoneno,
    #         email=email,
    #     )
    #     messages.success(request, "Address Added Succesfully")
    #     return redirect("core:dashboard")
        
    
    context = {
        "orders": orders,
        "address": address,
    }
    return render (request, 'core/dashboard.html', context)


def order_detail(request, id):
    order=CartOrder.objects.get(user=request.user, id=id)
    order_items= CartOrderItems.objects.filter(order=order)
    context = {
        'order_items': order_items,
    }
    return render(request, 'core/order-detail.html', context)

def addressbook(request):
    address = Address.objects.filter(user= request.user)
    if request.method == "POST":
        address=request.POST.get("address")
        phoneno=request.POST.get("phoneno")
        email=request.POST.get("email")
        
        new_address= Address.objects.create(
            user=request.user,
            address= address,
            contact_no= phoneno,
            email=email,
            status=True,
        )
        messages.success(request, "Address Added Succesfully")
        return redirect("core:addressbook")
    context = {
        "address": address,
    }
    
    return render(request, 'core/addressbook.html', context)


@login_required
def wishlist_view(request):
    wishlist=Wishlist.objects.all()
    
    context = {
        "w": wishlist
    }
    
    return render(request, "core/wishlist.html", context)


def add_to_wishlist(request):
    product_id=request.GET['id']
    product= Product.objects.get(pid=product_id)
    
    context= {}
    
    wishlist_count = Wishlist.objects.filter(product= product, user= request.user).count()
    print(wishlist_count)
    
    if wishlist_count> 0:
        context ={
            "bool": True
        }
    else:
        new_wishlist = Wishlist.objects.create(
            product=product,
            user= request.user,
        )
        
        context = {
            "bool": True
        }
        
    return JsonResponse(context)