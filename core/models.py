from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from userauths.models import User
from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField


STATUS_CHOICE = (
    ("processing", "Processing"),
    ("shipped", "Shipped"),
    ("delivered", "Delivered"),
    
    
)

STATUS = (
    ("draft", "Draft"),
    ("disabled", "Disabled"),
    ("in_review", "In Review"),
    ("rejected", "Rejected"),
    ("published", "Published"),
    
    
)



RATING = (
    (1, "⭐☆☆☆☆"),
    (2, "⭐⭐☆☆☆"),
    (3, "⭐⭐⭐☆☆"),
    (4, "⭐⭐⭐⭐☆"),
    (5, "⭐⭐⭐⭐⭐"),
    
    
)



def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)


# Create your models here.
class Category(models.Model):
    cid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="cat", alphabet="abcdefgh12345")
    user= models.ForeignKey(User, on_delete= models.SET_NULL, null=True) 
    
    
    title = models.CharField(max_length=100, default="Medicine")
    subtitle = models.CharField(max_length=100, default="General Medicine", null=True)
    image = models.ImageField(upload_to=user_directory_path, default="category.jpg")
    description = RichTextUploadingField(null=True, blank=True, default="This is a category")
    
    
    class Meta:
        verbose_name_plural = "Categories"
        
    def category_image(self):
        return mark_safe('<img src = "%s" width= "50" height = "50" />' % (self.image.url)) 
    
    def __str__(self):
        return self.title
    
    
class SubCategory(models.Model):
    scid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="subcat", alphabet="abcdefgh12345")
    user= models.ForeignKey(User, on_delete= models.SET_NULL, null=True) 
    category= models.ForeignKey(Category, on_delete= models.SET_NULL, null=True) 
    title = models.CharField(max_length=100, default="General Medicines")
    image = models.ImageField(upload_to=user_directory_path, default="subcategory.jpg")
    description = RichTextUploadingField(null=True, blank=True, default="This is a sub category")
    
    
    class Meta:
        verbose_name_plural = "Sub-Categories"
        
    def subcategory_image(self):
        return mark_safe('<img src = "%s" width= "50" height = "50" />' % (self.image.url)) 
    
    def __str__(self):
        return self.title
    
class ListCategory(models.Model):
    lcid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="liscat", alphabet="abcdefgh12345")
    user= models.ForeignKey(User, on_delete= models.SET_NULL, null=True) 
    category= models.ForeignKey(Category, on_delete= models.SET_NULL, null=True) 
    subcategory= models.ForeignKey(SubCategory, on_delete= models.SET_NULL, null=True) 
    title = models.CharField(max_length=100, default="General Medicines")
    
    
    class Meta:
        verbose_name_plural = "List-Categories"
    
    def __str__(self):
        return self.title

class Tags(models.Model):
    pass
    
class Vendor(models.Model):
    vid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="ven", alphabet="abcdefgh12345")
    
    title = models.CharField(max_length=100, default="ABC Pharma Co.")
    image = models.ImageField(upload_to=user_directory_path, default="vendor.jpg")
    # description = models.TextField(null=True, blank=True, default="I am an amazing vendor")
    description = RichTextUploadingField(null=True, blank=True, default="I am an amazing vendor")
    
    address = models.CharField(max_length=100, default="Kathmandu, Nepal")
    contact = models.CharField(max_length=100, default="+977 1234567890")
    shipping_on_time = models.CharField(max_length=100, default="100")
    authentic_rating = models.CharField(max_length=100, default="100")
    days_return = models.CharField(max_length=100, default="100")
    warranty_period = models.CharField(max_length=100, default="100")
    
    user= models.ForeignKey(User, on_delete= models.SET_NULL, null=True)
    date= models.DateTimeField(auto_now_add=True, null=True, blank=True) 
    
    class Meta:
        verbose_name_plural = "Vendors"
        
    def vendor_image(self):
        return mark_safe('<img src = "%s" width= "50" height = "50" />' % (self.image.url)) 
    
    def __str__(self):
        return self.title
    

class Product(models.Model):
    
    user= models.ForeignKey(User, on_delete= models.SET_NULL, null=True) 
    category= models.ForeignKey(Category, on_delete= models.SET_NULL, null=True, related_name="category") 
    subcategory= models.ForeignKey(SubCategory, on_delete= models.SET_NULL, null=True, related_name="subcategory") 
    listcategory= models.ForeignKey(ListCategory, on_delete= models.SET_NULL, null=True, related_name="listcategory") 
    vendor= models.ForeignKey(Vendor, on_delete= models.SET_NULL, null=True, related_name="vendor") 
    pid = ShortUUIDField(unique=True, length=10, max_length=20, prefix="pro", alphabet="abcdefgh12345")
    title = models.CharField(max_length=100, default="Brand New Fit Band")
    image = models.ImageField(upload_to=user_directory_path, default="product.jpg")
    # description = models.TextField(null=True, blank=True, default="This is a product")
    description = RichTextUploadingField(null=True, blank=True, default="This is a product")
    short_description = models.TextField(null=True, blank=True, default="This is a short product des")

    stock_count = models.CharField(max_length=100, default="20", null= True, blank=True)
    life = models.CharField(max_length=100, default="100 days", null=True, blank=True)
    mfd= models.DateTimeField(auto_now_add=False, null=True, blank=True)
    
    
    
    
    price = models.DecimalField(max_digits=999999999999, decimal_places=2, default="1.99")
    old_price = models.DecimalField(max_digits=999999999999, decimal_places=2, default="2.99")
    
    
    
   # tags= models.ForeignKey(Tags, on_delete= models.SET_NULL, null=True) 
    tag =  TaggableManager( blank=True)
    product_status= models.CharField(choices=STATUS, max_length=10 , default="in_review")
    
    status = models.BooleanField(default=True)
    in_stock= models.BooleanField(default=True)
    featured= models.BooleanField(default=False)
    digital= models.BooleanField(default=False)
    
    sku = ShortUUIDField(unique=True, length=5, max_length=10, prefix="sku", alphabet="1234567890")
    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True, blank=True)
    
    
    class Meta:
        verbose_name_plural = "Products"
        
    def product_image(self):
        return mark_safe('<img src = "%s" width= "50" height = "50" />' % (self.image.url)) 
    
    def __str__(self):
        return self.title
    
    def get_percentage(self):
        new_price= ((self.old_price-self.price)/ self.old_price) *100
        return new_price
    
class ProductImages(models.Model):
    
    images= models.ImageField(upload_to="product-images", default="product.jpg")
    product= models.ForeignKey(Product, related_name="p_images", on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)
    
    
    class Meta:
        verbose_name_plural = "Product Images"
        




#####################Cart, Order, OrderItem  ############
#####################Cart, Order, OrderItem  ############
#####################Cart, Order, OrderItem  ############
#####################Cart, Order, OrderItem  ############
#####################Cart, Order, OrderItem  ############

class CartOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=9999999999, decimal_places=2, default="1.99" )
    paid_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    product_status = models.CharField(choices=STATUS_CHOICE, max_length=30, default="processing")
    order_id =  ShortUUIDField(unique=True, length=10, max_length=20, prefix="ord", alphabet="abcdefgh12345")
    
    class Meta:
        verbose_name_plural = "Cart Orders"
        




class CartOrderItems(models.Model):
    
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=200)
    product_status = models.CharField(max_length=200)
    item = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    qty= models.IntegerField(default=0)
    price = models.DecimalField(max_digits=9999999999, decimal_places=2, default="1.99" )
    total= models.DecimalField(max_digits=9999999999, decimal_places=2, default="1.99" )
    
    class Meta:
        verbose_name_plural = "Cart Order Items"
        
    def category_image(self):
        return mark_safe('<img src = "%s" width= "50" height = "50" />' % (self.image.url)) 
    

    def order_image(self):
        return mark_safe('<img src = "/media/%s" width= "50" height = "50" />' % (self.image)) 
    
    
    
##################### Product Review , Wishlist, Address  ############
##################### Product Review , Wishlist, Address  ############
##################### Product Review , Wishlist, Address  ############
##################### Product Review , Wishlist, Address  ############
##################### Product Review , Wishlist, Address  ############


class ProductReview(models.Model):
    
    
    
    user = models.ForeignKey(User, on_delete= models.SET_NULL, null=True) 
    product = models.ForeignKey(Product, on_delete= models.SET_NULL, null=True, related_name="reviews") 
    review = models.TextField()
    rating = models.IntegerField(choices=RATING, default=None)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Product Reviews"
        
    
    def __str__(self):
        return self.product.title
    
    
    def get_rating(self):
        return self.rating


class Wishlist(models.Model):
    
    
    
    user = models.ForeignKey(User, on_delete= models.SET_NULL, null=True) 
    product = models.ForeignKey(Product, on_delete= models.SET_NULL, null=True) 
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Wishlists"
        
    
    def __str__(self):
        return self.product.title
    
    
class Address(models.Model):
    
    user = models.ForeignKey(User, on_delete= models.SET_NULL, null=True) 
    address = models.CharField(max_length=100 , null=True)
    contact_no = models.CharField(max_length=13 , null=True)
    
    email = models.CharField(max_length=100 , null=True)
    status = models.BooleanField(default=False)
    
    
    class Meta:
        verbose_name_plural = "Addresses"
        
        