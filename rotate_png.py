from PIL import Image

def rotate_png(image_path, angle):
    # Открытие изображения
    image = Image.open(image_path)

    # Создаем пустое изображение с тем же размером и белым фоном
    output_image = Image.new("RGB", image.size, "white")

    # Повернуть изображение
    rotated_image = image.rotate(angle, resample=Image.BICUBIC)

    # Получаем координаты для центрирования изображения на белом фоне
    x = (output_image.size[0] - rotated_image.size[0]) // 2
    y = (output_image.size[1] - rotated_image.size[1]) // 2

    # Вставляем повернутое изображение на белый фон
    output_image.paste(rotated_image, (x, y), rotated_image)

    # Сохраняем результат
    output_image.save(image_path)
