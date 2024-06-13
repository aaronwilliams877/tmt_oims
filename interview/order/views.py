from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request

from interview.order.models import Order, OrderTag
from interview.order.serializers import OrderSerializer, OrderTagSerializer

# Create your views here.
class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    

class OrderTagListCreateView(generics.ListCreateAPIView):
    queryset = OrderTag.objects.all()
    serializer_class = OrderTagSerializer


class DeactivateOrderView(APIView):
    """Mark an order an inactive."""
    
    def patch(self, request: Request, pk):
        order = get_object_or_404(Order, pk=pk)
        order.deactivate(pk)
        return Response({'message': f'Order {order.id} deactivated successfully'}, status=status.HTTP_200_OK)
