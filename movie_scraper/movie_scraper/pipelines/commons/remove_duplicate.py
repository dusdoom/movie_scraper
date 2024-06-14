from scrapy.exceptions import DropItem
from scrapy import Item
from .base_step import BaseStep

class RemoveDuplicate(BaseStep):
    unique_field_key = 'unique_field'
    unique_field_seen = set()
    item_type = Item

    def execute(self, item, spider):
        if(self.unique_field_key not in item):
            raise RuntimeError(f"Item missing unique field identifier: {item}")

        if item[self.unique_field_key] in self.unique_fields_seen:
            raise DropItem(f'Duplicate item found: {item[self.unique_field_key]}')

        self.unique_fields_seen.add(item[self.unique_field_key])
        return item