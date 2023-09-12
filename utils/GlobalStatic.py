from utils.singleton import singleton

@singleton
class GlobalResources:
    @property
    def resource(self):
        return self.__resource

    """全局资源"""
    def __init__(self):
        self.__resource = {}

    def __getitem__(self, item):
        return self.get_resource(item)

    def  __setitem__(self, key, value):
        self.add_resource(key, value)

    def add_resource(self, key, value):
        """添加资源"""
        self.__resource[key] = value

    def get_resource(self, key):
        """获取资源"""
        return self.__resource.get(key, None)

    def remove_resource(self, key):
        """移除资源"""
        if key in self.__resource:
            del self.__resource[key]

    def list_resources(self):
        """列出所有资源"""
        return self.__resource.keys()