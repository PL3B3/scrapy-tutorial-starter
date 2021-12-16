def split_url(url: str):
    url_chunks = url.split('/')
    return '/'.join(url_chunks[:-1]), url_chunks[-1]