from .permissions import IsCustomerUser, IsCartOwner, IsOrderShipper
from django.utils import timezone
# from django.http.response import HttpResponse, JsonResponse

# Create your views here.
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Cart, CartItem, Order, OrderItem
from deliveryservice.models import DeliveryServicer
from products.models import Product
from customer.models import Customer

from .serializers import (

    OrderCreateSerializer,
    OrderItemCreateSerializer,
    OrderResponseDisplaySerializer,
    CartItemSerializer,
    CartUpdateSerializer,
    OrderStatusUpdateSerializer,

)
from rest_framework import status


from rest_framework.generics import (
    CreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
    GenericAPIView,

)


from rest_framework.response import Response


class OrderCreateAPTView(CreateAPIView):
    '''
    Creates the Order for Customer
    '''
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer
    permission_classes = (IsAuthenticated, IsCustomerUser)

    def _deductProductStock(self, product, product_count):
        '''
        Deduct Product Stock From Database for order
        '''
        if product.stockCount - product_count >= 0:
            product.stockCount -= product_count
            product.save()
        else:
            # send_notification(Shopowner, message={product:"outofstock"})
            errorMessage = {product.name: "out of stock "}
            return Response(data=errorMessage, status=status.HTTP_400_BAD_REQUEST)

    def _getOfferPrice(self, price, offerexpire, offerpercentage):

        now = timezone.now()
        if now < offerexpire:
            return price - ((price * offerpercentage) // 100)

        return price

    def _calculateTotalBillAmount(self, items):
        '''
        calculates the bill amount for cart
        '''

        __amount = 0

        for item_id in items:

            if not CartItem.objects.filter(id=item_id).exists():
                errorMessage = {"field_error": {"cart item": "Doesn't exist"}}
                return Response(data=errorMessage, status=status.HTTP_400_BAD_REQUEST)

            item = CartItem.objects.get(id=item_id)
            product = item.product
            productprice = product.price
            quantity = item.quantity

            self._deductProductStock(product, quantity)

            originalprice = productprice * quantity
            offer = product.offer

            if offer:
                offerpercentage = offer.percentage
                offerexpiry = offer.expiry
                price = self._getOfferPrice(
                    originalprice, offerexpiry, offerpercentage)
            else:
                price = originalprice

            __amount += price

        return __amount

    def _getOneAvalibaleDeliveryServicer(self):
        '''
        get one delivery servicer for his delivery
        '''
        availableDeliverer = DeliveryServicer.objects.filter(available=True)

        if availableDeliverer.exists():
            deliverer_id = availableDeliverer.first().id
            return deliverer_id
        else:
            errorMessage = {
                "deliveryservicer": "no delivery servicers are active right now"}
            return Response(data=errorMessage, status=status.HTTP_400_BAD_REQUEST)

    def _clearcustomercart(self, order, orderedCartItemsIds):

        # order.orderbycustomer.cart.items.clear()
        customerCartItems = order.orderbycustomer.cart.items

        customerCartItemsAll = customerCartItems.all()

        for cartItem in customerCartItemsAll:
            if cartItem.id in orderedCartItemsIds:
                customerCartItems.remove(cartItem)
                cartItem.delete()

    def _addOrderToCustomerAccount(self, customer, order):

        customer.myorders.add(order)

    def _addOrderToDeliverAccount(self, deliverer, order):

        deliverer.mydeliveries.add(order)

    def _createOrderedItemsFromCartItems(self, items):
        order_items = []

        for item_id in items:

            if not CartItem.objects.filter(id=item_id).exists():
                errorMessage = {"field_error": {"cart item": "Doesn't exist"}}
                return Response(data=errorMessage, status=status.HTTP_400_BAD_REQUEST)

            item = CartItem.objects.get(id=item_id)
            cart_itemdata = {'product': item.product.id,
                             'quantity': item.quantity}

            orderItem_Create_Serializer = OrderItemCreateSerializer(
                data=cart_itemdata)
            orderItem_Create_Serializer.is_valid(raise_exception=True)
            order_item_instance = orderItem_Create_Serializer.save()

            order_items.append(order_item_instance.id)

        return order_items

    def _getOrderCustomer(self, user):
        customer = user.customerprofile.customer
        return customer.id

    def create(self, request, *args, **kwargs):

        requestedData = request.data
        orderitems = requestedData["items"]

        totalPrice = self._calculateTotalBillAmount(orderitems)
        requestedData["amount"] = totalPrice

        requestedData["items"] = self._createOrderedItemsFromCartItems(
            orderitems)

        orderdeliverer = self._getOneAvalibaleDeliveryServicer()
        requestedData["ordershipper"] = orderdeliverer

        orderCustomerID = self._getOrderCustomer(request.user)
        requestedData["orderbycustomer"] = orderCustomerID

        requestedData["status"] = "placed"

        serializer = self.get_serializer(data=requestedData)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()

        # send_notification(orderdeliverer, order)

        self._clearcustomercart(order, orderitems)
        self._addOrderToCustomerAccount(order.orderbycustomer, order)
        self._addOrderToDeliverAccount(order.ordershipper, order)

        orderResponse = OrderResponseDisplaySerializer(order).data

        return Response(orderResponse, status=status.HTTP_201_CREATED)


class UpdateCartAPIView(UpdateAPIView):
    '''
    Update the Cart with new cart items
    '''
    queryset = Cart.objects.all()
    serializer_class = CartUpdateSerializer
    permission_classes = (IsAuthenticated, IsCustomerUser, IsCartOwner)
    lookup_field = "id"

    def update(self, request, *args, **kwargs):

        data = request.data

        customerCart = self.get_object()
        serializer = self.get_serializer_class()

        cart_items = data.get("items")

        if not cart_items:
            errorMessage = {{"field_error": {"items": "required field"}}}
            return Response(data=errorMessage, status=status.HTTP_400_BAD_REQUEST)

        allCartItems = customerCart.items.all()
        # customerCart.items.clear()
        # # clears the cartitems in user cart but not delete it
        if allCartItems.exists():
            for oneCartItem in allCartItems:
                customerCart.items.remove(oneCartItem)
                # deletes the unused cartitems
                oneCartItem.delete()

        for cart_item in cart_items:

            if cart_item.get("quantity") < 1:
                errorMessage = {"value_error": {"quantity": "atleast 1"}}
                return Response(data=errorMessage, status=status.HTTP_400_BAD_REQUEST)

            cart_item_serializer = CartItemSerializer(data=cart_item)
            cart_item_serializer.is_valid(raise_exception=True)

            item = cart_item_serializer.save()
            customerCart.items.add(item)

        cart_serializer = serializer(customerCart)
        return Response(cart_serializer.data, status=status.HTTP_200_OK)


class OrderStatusUpdateAPIView(UpdateAPIView):
    '''
    updates the order status --patch
    either as 'delivery' or as 'reached' or as 'cancelled'
    '''
    queryset = Order.objects.all()
    serializer_class = OrderStatusUpdateSerializer
    permission_classes = (IsAuthenticated, IsOrderShipper)
    lookup_field = "id"

    def update(self, request, *args, **kwargs):
        ''' Status once reached final stage, it must not overwrited '''
        order = self.get_object()
        if order.status in ('reached', 'cancelled'):
            errorMessage = {"status": "can't update further"}
            return Response(data=errorMessage, status=status.HTTP_400_BAD_REQUEST)

        return super(OrderStatusUpdateAPIView, self).update(request, *args, **kwargs)
