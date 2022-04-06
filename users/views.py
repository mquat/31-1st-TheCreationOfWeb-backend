import json, bcrypt, jwt

from django.conf  import settings
from django.views import View
from django.http  import JsonResponse
from django.forms import ValidationError
from datetime     import datetime, timedelta

from .models    import User
from .validator import validate_password
from .utils     import login_decorator

class SignUpView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            user         = data['user']
            password     = data['password']
            address      = data['address']
            phone_number = data['phone_number']
            amount       = data['amount']

            validate_password(password)
            
            if User.objects.filter(user=user).exists():
                return JsonResponse({'message':'ID_ALREADY_EXISTS'}, status=400)
            
            if User.objects.filter(phone_number=phone_number).exists():
                return JsonResponse({'message':'PHONE_NUMBER_ALREADY_EXISTS'}, status=400)

            hashed_password = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt()).decode('utf-8')
            
            User.objects.create(
                user         = user,
                password     = hashed_password,
                address      = address,
                phone_number = phone_number,
                amount       = amount
            )

            return JsonResponse({'message':'SUCCESS'}, status=201)
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
        except ValidationError as e:
            return JsonResponse({'message':e.message}, status=400)

class SignInView(View):
    def post(self, request):
        try: 
            data = json.loads(request.body)
            user = User.objects.get(user=data['user'])

            is_checked = bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8'))      
            
            if not is_checked:
                return JsonResponse({'message':'INVALID_PASSWORD'}, status=401)   
            
            access_token = jwt.encode({'user_id':user.id , 'exp':datetime.utcnow() + timedelta(days=3)}, settings.SECRET_KEY, settings.ALGORITHM)
            
            return JsonResponse({'token':access_token}, status=200)
            
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
        except User.DoesNotExist:
            return JsonResponse({'message':'INVALID_USER'}, status=401)

class UserView(View):
    @login_decorator
    def get(self, request):
        user = request.user
        result = {
            'user'         : user.user,
            'address'      : user.address,
            'phone_number' : user.phone_number,
            'amount'       : user.amount
        }

        return JsonResponse({'message':result}, status=200)