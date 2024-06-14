from scrapy.exceptions import DropItem
from scrapy import Item
from .base_step import BaseStep

class ValidateUrl(BaseStep):
    def __init__(self):
        self.item_type = Item

    def execute(self, item, spider):
        if 'url' not in item:
            raise DropItem(f"Item missing url: {item}")

        return item