from abc import ABC, abstractmethod
from typing import Type
from scrapy import ItemAdapter
from scrapy.exceptions import NotConfigured

# Step class is an abstract class that defines the interface for all the steps in the pipeline.
class BaseStep(ABC):
    item_type = None

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        if(self.item_type == None):
            raise NotConfigured("Item type not set")

        if(not adapter.is_item(self.item_type)):
            return item

        return self.execute(item, spider)

    @abstractmethod
    def execute(self, item, spider):
        pass
    
    def open_spider(self, spider):
        raise NotImplementedError

    def close_spider(self, spider):
        raise NotImplementedError