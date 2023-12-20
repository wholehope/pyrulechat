import os
import importlib.util
from pydantic import BaseModel, Field, validator
from typing import ClassVar, Dict
from topics.base_topic import BaseTopic

this_file_path = os.path.dirname(os.path.realpath(__file__))

class RuleChat(BaseModel):
    MANAGER_ID: ClassVar[str] = 'manager_keeps_instances_accessible_globally'
    # ... means this field is mandatory
    # we supply a manager id as default, so we alwayes have an instance
    # that can be accessible globally
    sender_id: str = Field(MANAGER_ID, min_length=1, max_length=100)

    # Private class-level cache to store instances
    _instances: ClassVar[Dict[str, 'RuleChat']] = {}
    _topics: ClassVar[Dict[str, 'BaseTopic']] = {}
    _active_topic: str = None

    def __new__(cls, sender_id: str = MANAGER_ID, **data):
        if sender_id in cls._instances:
            return cls._instances[sender_id]
        else:
            instance = super().__new__(cls)
            cls._instances[sender_id] = instance
            return instance

    def __init__(self, **data):
        super().__init__(**data)  # Call the super class (BaseModel) __init__
        self.load_topics()        # Then call load_topics

    @classmethod
    def get_instance(cls, sender_id: str):
        '''
        get instance by sender_id
        this is redundant, since the __new__ is implemented in the same way
        this is just here to show another alternative to get the instance
        this method is bound to the class, not the instance
        '''
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
        '''
        use this method to get chat response
        sender_id is always required
        It always enforce the correct instance you are talking with
        even if you call '456' through the instance of '123',
        you will be always routed to the proper instance of '456'
        '''
        chat_instance = RuleChat.get_instance(sender_id)
        return chat_instance._chat(message)
    
    def _chat(self, message: str):
        if self._active_topic:
            return self._topics[self._active_topic].chat(message)
        else:
            return 'No active topic'

rule_chat_client = RuleChat()

def test_rule_chat_instance():
    # Example usage:
    chat_instance_1 = RuleChat.get_instance(sender_id='123')
    chat_instance_2 = RuleChat(sender_id='123')
    chat_instance_3 = RuleChat(sender_id='456')

    # These will be the same instance
    assert chat_instance_1 is chat_instance_2

    # This will be a different instance
    assert chat_instance_1 is not chat_instance_3

    chat_instance_1.chat('123', 'Hello, world!')
    chat_instance_2.chat('123', 'Hello, world!')
    chat_instance_3.chat('456', 'hello world!')

if __name__ == '__main__':
    test_rule_chat_instance()
    # ret = RuleChat.chat('123', 'Hello, world!')
    ret = rule_chat_client.sender_id
    print(ret)
