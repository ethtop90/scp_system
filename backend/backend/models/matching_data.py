class Matching_data:
    def __init__(self,username, id, first_data, item_keys, mapping):
        self.username = username
        self.id = id
        self.first_data = first_data
        self.item_keys = item_keys
        self.mapping = mapping
    def to_dict(self):
        return {
            'username': self.username,
            'id': self.id,
            'first_data': self.first_data,
            'item_keys': self.item_keys,
            'mapping': self.mapping
            # Add other attributes as needed
        }