from scrapy.exceptions import DropItem
from scrapy import Item
from itemadapter import is_item, ItemAdapter

class RemoveDuplicate:
    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter["id"] in self.ids_seen:
            raise DropItem(f"Duplicate item found: {item!r}")
        else:
            self.ids_seen.add(adapter["id"])
            return item