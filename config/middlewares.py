import threading


class RequestMiddleware:
    """Middleware to access Request object from within a model or signal"""

    def __init__(self, get_response=None, thread_local=threading.local()):
        self.get_response = get_response
        self.thread_local = thread_local

    def __call__(self, request):
        self.thread_local.current_request = request
        response = self.get_response(request)
        return response
