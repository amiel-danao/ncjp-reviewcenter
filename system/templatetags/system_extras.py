from urllib.parse import parse_qs, urlparse
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

def get_video_id(value):
    """
    Examples:
    - http://youtu.be/SA2iWivDJiE
    - http://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu
    - http://www.youtube.com/embed/SA2iWivDJiE
    - http://www.youtube.com/v/SA2iWivDJiE?version=3&amp;hl=en_US
    """
    query = urlparse(value)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            p = parse_qs(query.query)
            return p['v'][0]
        if query.path[:7] == '/embed/':
            return query.path.split('/')[2]
        if query.path[:3] == '/v/':
            return query.path.split('/')[2]
    # fail?
    return None

@stringfilter
def youthumbnail(value, args):
    '''returns youtube thumb url
    args s, l (small, large)'''
    # qs = value.split('?')
    # video_id = parse_qs(qs[1])['v'][0]
    video_id = get_video_id(value)

    if video_id is None:
        return '#'

    if args == 's':
        return "http://img.youtube.com/vi/%s/2.jpg" % video_id
    elif args == 'l':
        return "http://img.youtube.com/vi/%s/0.jpg" % video_id
    else:
        return None

register.filter('youthumbnail', youthumbnail)