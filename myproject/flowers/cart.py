from decimal import Decimal
from django import template

register = template.Library()
@register.simple_tag(takes_context=True)
class Cart:
    def __init__(self, request):
        """
        Инициализация корзины. Если корзина уже существует в сеансе, загружаем её.
        Иначе создаём новую корзину.
        """
        self.session = request.session
        cart = self.session.get('cart')
        if 'cart' not in self.session:
            # Сохранение корзины в сессии
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        """
        Добавление или обновление товара в корзине.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            if update_quantity:
                self.cart[product_id]['quantity'] = quantity
            else:
                self.cart[product_id]['quantity'] += quantity
        else:
            self.cart[product_id] = {
                'quantity': quantity,
                'price': str(product.price)
            }
        self.save()

    def save(self):
        """
        Сохранение корзины в сессии.
        """
        self.session['cart'] = self.cart
        self.session.modified = True

    def remove(self, product):
        """
        Удаление товара из корзины.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def get_total_price(self):
        """
        Возвращает общую стоимость товаров в корзине.
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def __iter__(self):
        """
        Итерация по товарам в корзине.
        """
        product_ids = self.cart.keys()
        for product_id in product_ids:
            yield self.cart[product_id]

    def __len__(self):
        """
        Возвращает количество товаров в корзине.
        """
        return sum(item['quantity'] for item in self.cart.values())