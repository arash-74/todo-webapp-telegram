from todo.models import User


class CustomBackEnd:
    def authenticate(self, request, username, password=None):
        try:
            user = None
            print(username)
            if username == 'admin':
                user = User.objects.get(username='admin')
                if not user.check_password(password):
                    return None
            else:
                user = User.objects.get(chat_id=username)

            return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            user = None
        return user
