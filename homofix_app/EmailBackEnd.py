
from django.contrib.auth.backends import ModelBackend

from homofix_app.models import CustomUser

class EmailBackEnd(ModelBackend):
    def authenticate(self,username=None, password=None, **kwargs):
        
        try:

            user=CustomUser.objects.get(username=username)
     
            if user.check_password(password):
                return user
        except:
            pass

        