from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from interview.inventory.models import Inventory, InventoryType, InventoryLanguage, InventoryTag
from interview.order.models import Order

class DeactivateOrderViewTests(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.inventory_type = InventoryType.objects.create(name='Type 1')
        self.inventory_language = InventoryLanguage.objects.create(name='English')
        self.inventory_tag1 = InventoryTag.objects.create(name='Tag 1')
        self.inventory_tag2 = InventoryTag.objects.create(name='Tag 2')
        
        self.inventory = Inventory.objects.create(
            name="Inventory Item",
            type=self.inventory_type,
            language=self.inventory_language,
            metadata={'key1': 'value1'}
        )
        self.inventory.tags.add(self.inventory_tag1, self.inventory_tag2)

        self.order = Order.objects.create(
            inventory=self.inventory,
            start_date='2024-06-01',
            embargo_date='2024-07-01'
        )

    def test_deactivate_order(self):
        url = f'/orders/{self.order.id}/deactivate/'
        response = self.client.patch(url)     
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Order.objects.get(id=self.order.id).is_active)

    def test_deactivate_order_not_found(self):
        id = 1000
        url = f'/orders/{id}/deactivate/'
        response = self.client.patch(url)        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
