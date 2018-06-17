import random
import string


def generate_link(size=6, chars=string.ascii_lowercase + string.ascii_uppercase + string.digits):
    nLink = ''
    for i in range(size):
        nLink += random.choice(chars)
    return nLink


def create_shortcode(instance, size=6):
    new_link = generate_link(size=size)
    print(instance)
    qs_exists = instance.objects.filter(shortcode=new_link).exists()
    if qs_exists:
        return create_shortcode(instance=instance)
    return new_link
