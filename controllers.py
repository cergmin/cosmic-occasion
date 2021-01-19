from time import process_time
from os import path
from pygame import mixer, image, transform


class ResourceController:
    def __init__(self):
        self.resources = dict()

        # Необходимо, чтобы можно было вычислить в будущем,
        # насколько давно использовался ресурс
        self.init_time = process_time()

    # Загрузка ресурса и присвоение ему специального ключа
    def load(self, key, resource, rewrite=False,
             resource_type=None, **args):
        # Защищает от траты времени на повторную загрузку
        # одного и того же ресурса.
        # Если, вдруг, необходимо заменить ресурс,
        # то нужно поставить флаг rewrite = True

        if not rewrite and key in self.resources:
            return

        # Определение типа ресурса
        if type(resource) is str:
            # Если тип - это строка, то возможно два варианта:
            # 1. Это путь к файлу
            # 2. Это просто строка
            ext = path.splitext(resource)[1]

            if ext.lower() in ['.jpg', '.jpeg', '.png', '.gif'] or \
                    resource_type in ['image', 'picture']:
                self.load_img(key, resource, rewrite, **args)
            elif ext.lower() in ['.mp3', '.wav', '.ogg'] or \
                    resource_type in ['sound', 'music', 'audio']:
                self.load_sound(key, resource, rewrite, **args)
            else:
                # Если нам не удалось определить тип файла по расширению,
                # то мы считаем, что это обычная строка, которую будем хранить
                # в том виде, в котором она была передана.
                self.resources[key] = {
                    'resource': resource,
                    'type': 'string',
                    'last_use': process_time() - self.init_time
                }
        else:
            # Если была передана не строка,
            # то мы сохраняем ресурс таким какой он есть.
            resource_type = 'unknown'

            if type(resource).__name__ in [
                'list', 'set', 'dict', 'tuple', 'int', 'float'
            ]:
                resource_type = type(resource).__name__
            elif type(resource).__name__ in ['ElementUI', 'Button', 'Slider']:
                resource_type = 'ElementUI'

            self.resources[key] = {
                'resource': resource,
                'type': resource_type,
                'last_use': process_time() - self.init_time
            }

    # Специальный метод для загрузки звуков
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

    # Специальный метод для загрузки изображений
    def load_img(self, key, path, rewrite=False, alpha=False,
                 max_width=None, max_height=None, **args):
        # Позволяет указывать необходимость прозрачности и
        # делать некоторое сжатия, указывая максимальную
        # ширину или высоту.

        if not rewrite and self.is_exists(key):
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
                            img.get_size()[1] *
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
                            img.get_size()[0] *
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

    # Получение ресурса по ключу
    def get(self, key, full_info=False):
        if not self.is_exists(key):
            raise KeyError(
                'There is no resource with key \'' + str(key) + '\''
            )

        # Обновление времени последнего использования
        self.resources[key]['last_use'] = process_time() - self.init_time

        # Флаг full_info даёт возможность получить "метаданные"
        if full_info:
            return self.resources[key]
        else:
            return self.resources[key]['resource']

    def is_exists(self, key):
        return key in self.resources
