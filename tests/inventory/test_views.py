from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.utils import timezone
from datetime import timedelta
from interview.inventory.models import Inventory, InventoryType, InventoryLanguage, InventoryTag
from interview.inventory.serializers import InventorySerializer

class InventoryTests(APITestCase):
    """Inventory test cases."""

    def setUp(self):
        self.inventory_type = InventoryType.objects.create(name='Type 1')
        self.inventory_language = InventoryLanguage.objects.create(name='English')
        self.inventory_tag1 = InventoryTag.objects.create(name='Tag 1')
        self.inventory_tag2 = InventoryTag.objects.create(name='Tag 2')
        
        self.item1 = Inventory.objects.create(
            name="Item 1",
            type=self.inventory_type,
            language=self.inventory_language,
            created_at=timezone.now() - timedelta(days=10),
            metadata={'key1': 'value1'}
        )
        self.item1.tags.add(self.inventory_tag1)

        self.item2 = Inventory.objects.create(
            name="Item 2",
            type=self.inventory_type,
            language=self.inventory_language,
            created_at=timezone.now() - timedelta(days=5),
            metadata={'key2': 'value2'}
        )
        self.item2.tags.add(self.inventory_tag2)

        self.item3 = Inventory.objects.create(
            name="Item 3",
            type=self.inventory_type,
            language=self.inventory_language,
            created_at=timezone.now() - timedelta(days=1),
            metadata={'key3': 'value3'}
        )
        self.item3.tags.add(self.inventory_tag1, self.inventory_tag2)

    def test_list_inventory_items(self):
        url = reverse('inventory-list')
        response = self.client.get(url)
        inventories = Inventory.objects.all()
        serializer = InventorySerializer(inventories, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_list_inventory_items_created_after(self):
        url = reverse('inventory-list')
        response = self.client.get(url, {'created_after': (timezone.now() - timedelta(days=7)).date()})
        inventories = Inventory.objects.filter(created_at__gt=timezone.now() - timedelta(days=7))
        serializer = InventorySerializer(inventories, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_list_inventory_items_invalid_date(self):
        url = reverse('inventory-list')
        response = self.client.get(url, {'created_after': 'invalid-date'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
