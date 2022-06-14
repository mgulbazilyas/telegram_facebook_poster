import os
import pickle
import json


class DataStore:
    def __init__(self, store_name):
        self.name = store_name
        self.filename = store_name + '.pkl'

    def get_objects(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as stream:
                try:
                    return pickle.load(stream)
                except:
                    return []
        return []

    def add_object(self, obj):
        objects = self.get_objects()
        if 'status' not in obj or (obj['status'] == False):
            obj['status'] = False
            objects.append(obj)

        elif obj['status']:
            # TODO: Add
            telegram_id = obj.get('telegram_id')

            for oobj in objects:
                if oobj['telegram_id'] == telegram_id:
                    oobj['status'] = True

        with open(self.filename, 'w') as stream:
            pickle.dump(objects, stream)

    def get_undone(self):
        objects = self.get_objects()
        for obj in objects:
            if not obj['status']:
                return obj


store = DataStore('tfp')
