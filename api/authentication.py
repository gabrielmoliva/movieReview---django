from rest_framework.authentication import BasicAuthentication

class CustomBasicAuthentication(BasicAuthentication):
    # prevents the browser from presenting a login popup if the user inserts invalid credentials 
    def authenticate_header(self, request):
        return None