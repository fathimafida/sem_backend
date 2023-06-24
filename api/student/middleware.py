
import threading

# Thread-local variable to store the request object
thread_local = threading.local()


def get_current_request():
    """
    Returns the current request object.
    """
    return getattr(thread_local, 'request', None)


class RequestMiddleware:
    """
    Middleware to set the request object in a thread-local variable.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Set the request object in the thread-local variable
        thread_local.request = request

        response = self.get_response(request)

        # Clean up the request object from the thread-local variable
        del thread_local.request

        return response
