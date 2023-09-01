import sys
import random 

from django.core.management.base import BaseCommand, CommandError

from accounts.models import CustomUser
from products.models import Product, Category

class Command(BaseCommand):
    help = 'Add category dump data'

    def handle(self, *args, **options):
        list1 = ["Lavash1", "Lavash 2", "Lavash 3", "Lavash 4"]
        cat = Category.objects.get(id=1)

        a = list((Product(title=f'{i}', price=30000, real_price=15000, count_all=30, count_sold=0, is_deleted=False, category=cat) for i in list1))
        Product.objects.bulk_create(a)
        print('done')