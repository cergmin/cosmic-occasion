from time import process_time
from os import path
from pygame import mixer, image, transform


class ResourceController:
    def __init__(self):
        self.resources = dict()
        self.init_time = process_time()
    
    def load(self, key, resource, rewrite=False, 
             resource_type=None, **args):
        if not rewrite and key in self.resources:
            return

        if type(resource) is str:
            ext = path.splitext(resource)[1]
            
            if ext.lower() in ['.jpg', '.jpeg', '.png', '.gif'] or \
               resource_type in ['image', 'picture']:
                self.load_img(key, resource, rewrite, **args)
            elif ext.lower() in ['.mp3', '.wav', '.ogg'] or \
                 resource_type in ['sound', 'music', 'audio']:
                self.load_sound(key, resource, rewrite, **args)
            else:
                self.resources[key] = {
                    'resource': resource,
                    'type': 'string',
                    'last_use': process_time() - self.init_time
                }
        else:
            resource_type = 'unknown'

            if type(resource).__name__ in ['list', 'set', 'dict', 'tuple']:
                resource_type = type(resource).__name__
            elif type(resource).__name__ in ['ElementUI', 'Button', 'Slider']:
                resource_type = 'ElementUI'

            self.resources[key] = {
                'resource': resource,
                'type': 'unknown',
                'last_use': process_time() - self.init_time
            }
    
    def load_sound(self, key, path, rewrite=False, **args):
        if not rewrite and key in self.resources:
            return
        
        sound = mixer.Sound(path)
        sound.stop()

        self.resources[key] = {
            'resource': sound,
            'type': 'sound',
            'last_use': process_time() - self.init_time
        }
    
    def load_img(self, key, path, rewrite=False, alpha=False,
                 max_width=None, max_height=None, **args):
        if not rewrite and key in self.resources:
            return
        
        img = image.load(path)

        if alpha:
            img = img.convert_alpha()
        else:
            img = img.convert()
        
        if max_width is not None and max_width < img.get_size()[0]:
            img = transform.scale(
                img,
                (
                    max(1, max_width),
                    max(
                        1,
                        round(
                            img.get_size()[1] * \
                            (max_width / img.get_size()[0])
                        )
                    )
                )
            )
        
        if max_height is not None and max_height < img.get_size()[1]:
            img = transform.scale(
                img,
                (
                    max(
                        1,
                        round(
                            img.get_size()[0] * \
                            (max_height / img.get_size()[1])
                        )
                    ),
                    max(1, max_height)
                )
            )

        self.resources[key] = {
            'resource': img,
            'type': 'image',
            'alpha': alpha,
            'last_use': process_time() - self.init_time
        }

    def get(self, key, full_info=False):
        if key not in self.resources:
            raise KeyError(
                'There is no resource with key \'' + str(key) + '\''
            )
        
        self.resources[key]['last_use'] = process_time() - self.init_time

        if full_info:
            return self.resources[key]
        else:
            return self.resources[key]['resource']