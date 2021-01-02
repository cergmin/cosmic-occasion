from pygame import image, transform
from time import process_time

class ImageController:
    def __init__(self):
        self.images = dict()
        self.init_time = process_time()
    
    def load(self, path, key,
             alpha=False, max_width=None,
             max_height=None, rewrite=False):
        if not rewrite and key in self.images:
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

        self.images[key] = {
            'image': img,
            'alpha': alpha,
            'last_use': process_time() - self.init_time
        }

    def get(self, key, full_info=False):
        if key not in self.images:
            raise KeyError(
                'There is no image with key \'' + str(key) + '\''
            )
        
        self.images[key]['last_use'] = process_time() - self.init_time

        if full_info:
            return self.images[key]
        else:
            return self.images[key]['image']