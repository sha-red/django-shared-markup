# -*- coding: utf-8 -*-
# 09/2009 Erik Stein <code@classlibrary.net>


def image_references(image_qs):
    """
    Returns a ReStructured source fragment containing image references 
    for the given Image queryset.
    """
    def make_image_reference(image_obj):
        markup = u".. |%s| image:: %s" % (image_obj.slug, image_obj.imagefile.url)
        cl = image_obj.caption_line()
        if cl:
            markup += u"\n    :alt: %s"
        return markup
    return u"\n".join([make_image_reference(img) for img in image_qs])

