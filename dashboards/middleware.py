from django.shortcuts import redirect

class BlockUsersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.blocked_usernames = ['test_vtb', 'spammer', 'hacker']
        # URL, на которые разрешен доступ даже заблокированным пользователям
        self.allowed_urls = ['/info', '/logout', '/']

    def __call__(self, request):
        if (request.user.is_authenticated and 
            request.user.username in self.blocked_usernames and
            request.path not in self.allowed_urls):
            return redirect('/info')
        
        return self.get_response(request)
