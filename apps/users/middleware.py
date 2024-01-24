# middleware.py
from django.http import HttpResponse
from django.urls import resolve, reverse


class InternalRoutingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if response.status_code == 200 and 'Content-Type' in response.headers and 'text/html' in response.headers[
            'Content-Type']:
            content = response.content.decode('utf-8')

            tokens = content.split(' ')

            for i in range(len(tokens)):
                if tokens[i].startswith('href='):
                    link = tokens[i][6:-1]
                    parts = link.split('/')

                    if len(parts) >= 3 and parts[0] == '"/' and parts[2] == '"/':
                        user_site_name = parts[1]
                        routes = parts[3]
                        original_url = reverse('internal_redirect',
                                               kwargs={'user_site_name': user_site_name, 'routes': routes})
                        new_link = f'"{original_url}"'
                        tokens[i] = f'href={new_link}'

            content = ' '.join(tokens)
            response.content = content.encode('utf-8')

        return response
