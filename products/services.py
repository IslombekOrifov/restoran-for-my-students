
def upload_product_image_path(instance, image):
    return f"products/{instance.category.title}/{image}"
