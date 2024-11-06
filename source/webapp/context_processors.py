def strip_language_code(request):
    path = request.path.split('/')[2:]
    return {'language_base_link': "/" + "/".join(path)}