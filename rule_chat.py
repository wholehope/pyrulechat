import os
import importlib.util
from pydantic import BaseModel, Field, validator
from typing import ClassVar, Dict
from topics.base_topic import BaseTopic

this_file_path = os.path.dirname(os.path.realpath(__file__))

class RuleChat(BaseModel):
    sender_id: str = Field(..., min_length=1, max_length=100)

    # Private class-level cache to store instances
    _instances: ClassVar[Dict[str, 'RuleChat']] = {}
    _topics: ClassVar[Dict[str, 'BaseTopic']] = {}
    _active_topic: str = None

    def __init__(self, **data):
        super().__init__(**data)  # Call the super class (BaseModel) __init__
        self.load_topics()        # Then call load_topics

    @classmethod
    def get_instance(cls, sender_id: str):
        '''this method is bound to the class, not the instance'''
        # Check if an instance with the same sender_id already exists
        if sender_id in cls._instances:
            return cls._instances[sender_id]

        # Create a new instance and add it to the cache
        instance = cls(sender_id=sender_id)
        cls._instances[sender_id] = instance
        return instance
    
    def dynamic_import(self, module_name, path):
        """Dynamically import a module."""
        module_path = os.path.join(path, module_name + '.py')
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def load_topics(self):
        for filename in os.listdir(f'{this_file_path}/topics/'):
            if filename.endswith('.py') and \
                filename != '__init__.py' and \
                filename != 'base_topic.py':
                topic_name = filename[:-3]  # Remove .py
                topic_module = self.dynamic_import(topic_name, 
                                f'{this_file_path}/topics/')
                if hasattr(topic_module, 'ThisTopic'):
                    topic_instance = topic_module.ThisTopic()
                    self._topics[topic_name] = topic_instance

    @classmethod
    def chat(self, sender_id:str, message: str):
        chat_instance = RuleChat.get_instance(sender_id)
        return chat_instance._chat(message)
    
    def _chat(self, message: str):
        if self._active_topic:
            return self._topics[self._active_topic].chat(message)
        else:
            return 'No active topic'

def test_rule_chat_instance():
    # Example usage:
    chat_instance_1 = RuleChat.get_instance(sender_id='123')
    chat_instance_2 = RuleChat.get_instance(sender_id='123')
    chat_instance_3 = RuleChat.get_instance(sender_id='456')

    # These will be the same instance
    assert chat_instance_1 is chat_instance_2

    # This will be a different instance
    assert chat_instance_1 is not chat_instance_3

    chat_instance_1.chat('Hello, world!')
    chat_instance_2.chat('Hello, world!')
    chat_instance_3.chat('Hello, world!')

if __name__ == '__main__':
    ret = RuleChat.chat('123', 'Hello, world!')
    print(ret)
