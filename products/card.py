from django.conf import settings
from django.utils import timezone
from .models import *


class Cart():
    def __init__(self, request):
        self.session = request.session
        self.request = request
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        
    def save(self):
        self.session.modified = True

    def add(self, product_item, quantity = 1, updated_quantity=False):
        item_id = str(product_item.id)
        if item_id not in self.cart:
            self.cart[item_id] = {'quantity':0, 'price': product_item.price, 
                                  'adding_time':timezone.now().timestamp()}
        if updated_quantity:
            self.cart[item_id]['quantity'] = quantity
            self.cart[item_id]['adding_time'] = timezone.now().timestamp()
        else: 
            self.cart[item_id]['quantity'] += quantity
        self.save()


    def __iter__(self):
        items_ids = self.cart.keys()
        prod_id_list = []
        for cart_key in items_ids:
            prod_id_list.append(int(cart_key))
        product_items = Product.objects.filter(id__in=prod_id_list)
        cart = self.cart.copy()
        for product in product_items:
            cart[str(product.id)]['product'] = product
            cart[str(product.id)]['product_id'] = product.id
        for item in cart.values():
            item['total_price'] = item['price'] * item['quantity']
            yield item
        
    def remove(self, id):
        del self.cart[id]
        self.save() 
    
    def get_total_price(self):
        total_price = sum(item['price'] * item['quantity'] for item in self.cart.values())
        return total_price
    
    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()
        
    
        

        
        
        