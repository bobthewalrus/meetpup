from __future__ import unicode_literals
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
import bcrypt, re

emailregex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.+_-]+\.[a-zA-Z]+$')
nameregex = re.compile(r'^[a-zA-Z]+$')
#==============================================================
#            ******** Event Manager *********
#==============================================================
class EventManager(models.Manager):
    def eventcreator(self, request):
        users_list = User.objects.filter(id=request.session['user']['id'])
        event = self.create(name=request.POST['name'], date=request.POST['date'], time=request.POST['time'], duration=request.POST['duration'], street=request.POST['street'], state=request.POST['state'], city=request.POST['city'], zipcode=request.POST['zipcode'], description=request.POST['description'], user=users_list[0])
        return ()
#==============================================================
#            ******** User Manager *********
#==============================================================
class UserManager(models.Manager):
    def registervalidation(self, request):
        errors = self.validate_inputs(request)

        if len(errors) >0:
            return (False, errors)
        password = request.POST['password'].encode()
        pw_hash = bcrypt.hashpw(password, bcrypt.gensalt())
        print pw_hash

        user = self.create(firstname=request.POST['firstname'], lastname = request.POST['lastname'], email=request.POST['email'], pw_hash=pw_hash, zipcode = request.POST['zipcode'])
        print user.pw_hash
        return (True, user)

    def validate_inputs(self,request):
        email = request.POST['email'].lower()
        firstname = request.POST['firstname'].lower()
        lastname = request.POST['lastname'].lower()
        password = request.POST['password']
        passwordconf = request.POST['passwordconf']
        zipcode = request.POST['zipcode']

        errors=[]
        if len(firstname) <3 or len(lastname) <3:
            errors.append("Names must be longer than 2 characters.")
        if not nameregex.match(firstname):
            errors.append('Names must contain  only letters.')

        if not nameregex.match(lastname):

            errors.append('Last name must contain only letters.')
        if not emailregex.match(email):
            errors.append('Email is invalid.')

        if password != passwordconf:
            errors.append('Passwords do not match!')
        elif len(password) < 8:
            errors.append('Password is too short!')

        users_list = User.objects.filter(email=email)
        if users_list:
            errors.append('Email is invalid.')

        return errors

    def loginvalidation(self,request):
        print '**********validating login******'
        try:
            users_list = User.objects.filter(email=request.POST['email'])
            if users_list:

                user = users_list[0]
            else:
                return (False, ["Email or password doesn't exist"])
            password = request.POST['password'].encode()
            passwordhashed = bcrypt.hashpw(password, bcrypt.gensalt())
            print passwordhashed
            print "user's pw_hash is ",user.pw_hash
            print password
            # if bcrypt.hashpw(password, user.pw_hash.encode()) == user.pw_hash.encode():
            #     print bcrypt.hashpw(password, user.pw_hash.encode())
            #     print user.pw_hash
            return (True, user)
        except ObjectDoesNotExist:
            print "POOOOP"
            pass
        return (False, ["Email and password don't match."])

#==============================================================
#            ******** Classes *********
#==============================================================
# class Place(models.Model):
#     name = models.CharField(max_length=225, default="location_name")
#     latitude = models.DecimalField(max_digits=9, decimal_places=6, default="37.375400")
#     longitude = models.DecimalField(max_digits=9, decimal_places=6, default="-121.910158")

class User(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    pw_hash = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=10)
    biography = models.TextField(null=True)
    image = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class Pet(models.Model):
    name = models.CharField(max_length=225)
    birthday = models.DateField()
    biography = models.TextField(null=True)
    breed = models.CharField(max_length=150)
    user = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Event(models.Model):
    name = models.CharField(max_length=225)
    date = models.DateField()
    time = models.TimeField()
    duration = models.CharField(max_length=255)
    street = models.CharField(max_length= 225)
    state = models.CharField(max_length = 55)
    city = models.CharField(max_length = 125)
    zipcode = models.CharField(max_length = 10)
    description = models.CharField(max_length=355)
    user= models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = EventManager()

class Post(models.Model):
    title = models.CharField(max_length=125, default="Prior to adding title column")
    description = models.CharField(max_length=355)
    user = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)

class Comment(models.Model):
    description = models.CharField(max_length=355)
    user = models.ForeignKey(User)
    post = models.ForeignKey(Post)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Qa(models.Model):
    description = models.CharField(max_length=355)
    user = models.ForeignKey(User)
    event = models.ForeignKey(Event)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# class Review(models.Model):
#     description = models.CharField(max_length=355)
#     rating = models.IntegerField()
#     user = models.ForeignKey(User)
#     created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now = True)
