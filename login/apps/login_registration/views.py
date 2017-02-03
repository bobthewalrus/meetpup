from django.shortcuts import render, HttpResponse, redirect
from models import User, Pet, Event, Post, Comment, Qa
from django.contrib import messages
from django.urls import reverse
import googlemaps
from random import randint

def index(request):
    return render(request, "login_registration/index.html")

def print_messages(request, message_list):
    for message in message_list:
        messages.add_message(request,messages.INFO, message)

def loginvalidate(request):
    if request.method == "POST":
        print 'loginvalidate'
        print request.POST['email']
        result = User.objects.loginvalidation(request)
        print "Login validation complete"
        # print result
        if result[0] == False:
            print_messages(request, result[1])
            return redirect(reverse('success'))
        # print request
        print result[1]
        print "Passing to the login function"
        return login(request, result[1])
    else:
        print "Methods not post for loginvalidate"
        return redirect('/success')

def login(request, user):
    print "Here at Login"
    request.session['user'] = {
    'id': user.id,
    'firstname' : user.firstname,
    'lastname' : user.lastname,
    'email' : user.email,
    'zipcode': user.zipcode,
    # 'biography' : user.biography
    }
    print request.session['user']['zipcode']
    return redirect('success')


def registervalidate(request):
    print "registering!"
    result= User.objects.registervalidation(request)
    if not result[0]:
        print_messages(request, result[1])
        return redirect('success')
    return login(request, result[1])


def copy(request):
    user = User.objects.filter(id=request.session['user']['id'])[0]
    context = {
        'user':user,
        'events':Event.objects.all()
    }
    return render(request, 'login_registration/copy.html', context)


def success(request):
    if request.session.has_key('user'):
        return redirect('/copy')
    # if not 'user' in request.session:
    #     return redirect('/')
    # centeringpoint = request.session['user']['zipcode']
    # geocoder.geocode({'address': centeringpoint}, function(results, status){
    #     if status == google.maps.GeocoderStatus.OK:
    #         lat = results[0].geometry.location.lat()
    #         lng = results[0].geometry.location.lng()
    # print lat
    # print lng
    # })
    # user = User.objects.filter(id=request.session['user']['id'])[0]
    context = {
        'events':Event.objects.all()
    }
    gmaps = googlemaps.Client(key='AIzaSyDfaj5Z9lfipt5fV4D3CNy6a2I-HLDIZg4')
    try:
        geocode_result = gmaps.geocode(request.session['user']['zipcode'])
    except:
        geocode_result = gmaps.geocode(95112)
    location =  geocode_result[0]['geometry']['location']
    request.session['centered']= "{}, {}".format(location['lat'], location['lng'])
    # request.session['zip']='37.386402,-121.925215'
    # print request.session['zip']
    return render(request, 'login_registration/success.html', context)
    # var lat = '';
    # var lng = '';
    # var address = {zipcode} or {city and state};
    # geocoder.geocode( { 'address': address}, function(results, status) {
    #   if (status == google.maps.GeocoderStatus.OK) {
    #      lat = results[0].geometry.location.lat();
    #      lng = results[0].geometry.location.lng();
    #     });
    #   } else {
    #     alert("Geocode was not successful for the following reason: " + status);
    #   }
    # });
    # alert('Latitude: ' + lat + ' Logitude: ' + lng);


def zipupdate(request):
    return redirect('success')


def eventform(request):
    user = User.objects.filter(id=request.session['user']['id'])[0]
    context = {
        'user':user,
        'events':Event.objects.all()
    }
    return render(request,'login_registration/eventform.html', context)


def createevent(request):
    user=request.session['user']['id']
    print user
    result= Event.objects.eventcreator(request)
    return redirect('community')

def logout(request):
    request.session.flush()
    # request.session.pop('user')
    return redirect('/success')

def register(request):
    return render(request, 'login_registration/registration.html')

def community(request):
    user = User.objects.filter(id=request.session['user']['id'])[0]
    posts = Post.objects.all()
    context ={
    'posts':posts,
    'user':user
    }
    return render(request, 'login_registration/community.html', context)

def forumtopic(request):
    return render(request, 'login_registration/forumtopic.html')

def adoption(request):
    return render(request, 'login_registration/adoption.html')


def topic(request, post_id):
    user = User.objects.filter(id=request.session['user']['id'])[0]
    post = Post.objects.filter(id=post_id)[0]
    comments = Comment.objects.filter(post = post)
    context={
        'post':post,
        'comments':comments,
        'user':user
    }
    return render(request, 'login_registration/forumtopic.html', context)

#------------------------------------------------
# *** Start a new thread on community page ****
#------------------------------------------------
def post(request):
    if request.method =="POST":
            print request.session['user']['id']
            user_id = request.session['user']['id']
            user = User.objects.filter(id=user_id)[0]
            title = request.POST['title']
            description = request.POST['description']
            if not title or not description:
                messages.add_message(request, messages.INFO, "Please provide title and description")
                return redirect('/community')
            new_post = Post.objects.create(description=description, user=user, title=title)
    return redirect('/community')

#------------------------------------------------
#   ***** Delete a post on community page *****
#------------------------------------------------
def deletepost(request, post_id):
    if request.method == "POST":
        post = Post.objects.filter(id=post_id)
        post.delete()
        Comment.objects.filter(post = post).delete()
    return redirect('/community')

#------------------------------------------------
#      ***** leave a comment for a post *********
#------------------------------------------------
def comment(request, post_id):
    if request.method == "POST":
        user_id = request.session['user']['id']
        user = User.objects.filter(id=user_id)[0]
        description = request.POST['description']
        if not description:
            messages.add_message(request, messages.INFO, "Comment can not be empty")
            return redirect('/topic/{}'.format(post_id))
        post = Post.objects.filter(id=post_id)[0]
        post_id= post.id
        new_comment = Comment.objects.create(user=user, post=post, description=description)
    return redirect('/topic/{}'.format(post_id))

#------------------------------------------------
#      ***** delete comments *********
#------------------------------------------------
def deletecomment(request, post_id, comment_id):
    if request.method == "POST":
        Comment.objects.filter(id=comment_id).delete()
        print post_id
        print comment_id
    return redirect('/topic/{}'.format(post_id))

#------------------------------------------------
#     *****  the rest of the code :D  *******
#------------------------------------------------
def profilepage(request):
    if "pet_breed" in request.session:
        breed = request.session['pet_breed']
        context = {
            'user': User.objects.filter(id=request.session['user']['id'])[0],
            "breed": breed
        }
        return render(request, 'login_registration/profile.html', context)
    context = {
        'user': User.objects.filter(id=request.session['user']['id'])[0],
    }
    return render(request, 'login_registration/profile.html', context)

def editprofile(request):
    context = {
        'user': User.objects.filter(id=request.session['user']['id'])[0]
    }
    return render(request, 'login_registration/edit.html', context)

def updateprofile(request):
    user = User.objects.filter(id=request.session['user']['id'])[0]
    print user.firstname
    user_firstname = request.POST['first_name']
    user_lastname = request.POST['last_name']
    user_email = request.POST['email']
    user_bio = request.POST['bio']

    if not len(user_firstname) < 1:
        user.firstname = user_firstname
        print user.firstname
        request.session['user']['firstname'] = user_firstname
        user.save()

    if not len(user_lastname) < 1:
        user.lastname = user_lastname
        request.session['user']['lastname'] = user_lastname
        user.save()

    if not len(user_email) < 1:
        user.email = user_email
        request.session['user']['email'] = user_email
        user.save()

    if not len(user_bio) < 1:
        user.biography = user_bio
        print user.biography
        request.session['user']['biography'] = user_bio
        user.save()

    print user.firstname
    print user.email
    print request.session['user']

    return redirect('/profilepage')

def addpet(request):
    user = User.objects.filter(id=request.session['user']['id'])[0]
    pet_bd = request.POST['pet_birthday']
    pet_name = request.POST['pet_name']
    pet_breed = request.POST['pet_breed']
    if pet_breed:
        request.session['pet_breed']=pet_breed
    about = request.POST['pet_bio']
    random_image =["http://familypetvacaville.com/clients/9658/images/company_images/.resized/.resized_500x500_Labrador%20(yellow)%20image%20courtesy%20of%20Luigi%20Diamanti%20at%20FreeDigitalPhotos.net.jpg", "http://upshout.net/wp-content/uploads/2015/07/husky-001.jpg","https://c1.staticflickr.com/8/7399/9540655005_753bbb8da3.jpg","https://i1.sndcdn.com/artworks-000145042959-4j4w1d-t500x500.jpg"]
    picker = randint(0,3)
    print random_image[0]
    image = random_image[picker]
    valid = True

    if len(pet_name) <1:
        valid = False

    if len(about) < 1:
        valid = False

    if len(pet_bd) <1:
        valid = False

    if valid:
        Pet.objects.create(name=pet_name, birthday = pet_bd, breed=pet_breed, user=user, image=image, biography=about)
        return redirect('/profilepage')
    else:
        return redirect('/profilepage')

def displayevents(request):
    events = Event.objects.all()
    context = {'events': events}
    return render(request, 'login_registration', context)
