from .models import User
from datetime import datetime
from rest_framework_simplejwt import authentication
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer

class LastUpdate(object):
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # if not request.path == "/api/token/":
        #     token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
        #
        #     data = {'token': token}
        #     print("A" * 80)
        #     valid_data = VerifyJSONWebTokenSerializer().validate(data)
        #     print("A"*80)
        #     print(valid_data)
        #     user = valid_data['user']
        #     if user:
        #         print("A" * 80)
        #         user.last_updated = datetime.now()
        #         user.save()

        # user = request.user.is_authenticated

        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    def process_view(self, request, view_func, view_args, view_kwargs):

        # request.user = authentication.JWTAuthentication().authenticate(request)[0]  # Manually authenticate the token
        print('A'*80)
        user = request.user
        if user.is_authenticated:
            print("UPDATED"*15)
            user.last_updated = datetime.now()
            user.save()
