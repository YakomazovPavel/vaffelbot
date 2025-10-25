import requests
from PIL import Image
from io import BytesIO

from storage import storage, DishModel, Dish


def get_color_from_image_url(image_url: str) -> str:
    try:
        # Send a GET request to the image URL
        response = requests.get(image_url)
        response.raise_for_status()  # Raise an exception for bad status codes

        # Open the image using Pillow from the response content
        image = Image.open(BytesIO(response.content))
        r, g, b = image.getpixel((10, 10))
        hex_color = f"#{r:02x}{g:02x}{b:02x}"
        return hex_color

    except requests.exceptions.RequestException as e:
        print(f"Error downloading image: {e}")
        return None
    except IOError as e:
        print(f"Error opening or saving image with Pillow: {e}")
        return None


updated_count = 0
dishes = storage.get_dishes()
for dish in dishes:
    dish: DishModel
    try:
        if dish.photo_url:
            color = get_color_from_image_url(image_url=dish.photo_url)
            print(f"dish ({dish.id}) new color {color}")
            storage.session.query(Dish).filter(Dish.id == dish.id).update(
                {"color": color}
            )
            storage.session.commit()
            updated_count += 1
    except Exception as e:
        print(e)
    # break
print(f"Обновлено блюд {updated_count}")
