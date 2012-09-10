from django.template.loader import get_template
from django.template import Context, RequestContext
from django.contrib import auth
from django.http import HttpResponse, HttpResponseRedirect
from balance.bal.models import Transaction, Frelation, Balancer
from django.contrib.auth.models import User
from decimal import Decimal
import datetime

# Create your views here.

def index(request):
    ''
    if request.user.is_authenticated():
        return HttpResponseRedirect('/add/')
    now = datetime.datetime.now()
    t = get_template('index.html')
    html = t.render(RequestContext(request, {'current_date':now}))
    return HttpResponse(html)

def login(request):
    ''
    
    errors = []

    if request.method != 'POST':
        return HttpResponse('Only POSTs are allowed')
    if not request.POST.get('uname',''):
        errors.append('Please Enter Username.')
    if not request.POST.get('pass',''):
        errors.append('Please Enter password.')
    if not errors:
        #try:
        username = request.POST.get('uname','')
        password = request.POST.get('pass','')
        user = auth.authenticate(username=username,password=password)
        if user is not None and user.is_active:
            auth.login(request,user)
            # return HttpResponse("Logged In..Good work.")
            values = []
            values = Balancer.objects.filter(trans_member_id = user.id)
            print values
            for value in values:
                print value.trans.paidby
            friends = []
            friends = Frelation.objects.filter(a_user_id = user.id)
            # print friends
            mfriends = Frelation.objects.filter(friend_with_id = user.id)
            # print friends
            for friend in friends:
                print friend.friend_with.first_name
            t = get_template('mypage.html')
            html = t.render(RequestContext(request , { 'values':values, 'friends':friends,'mfriends':mfriends, 'myid':request.user.id, 'username':username}))
            return HttpResponse(html)

        else:
            errors.append("Username, password didnt match")
        #except:
        #    errors.append("Username, password didnt match")
            
    now = datetime.datetime.now()
    t = get_template('index.html')
    html = t.render(RequestContext(request, {'current_date':now, 'errors': errors }))
    return HttpResponse(html)

def add(request):
    'title, amount, date, desc'
    errors = []
    # print len(request.POST.getlist('member'))
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/index/')
    if request.method == 'POST':
        print request.POST
        if not request.POST.get('title',''):
            errors.append('Please enter title')
        elif len(request.POST.get('title')) > 10:
            errors.append('Please enter title less than 10 characters')
        try:
            if not request.POST.get('amount',''):
                errors.append('Please Enter amount.')
            elif Decimal(request.POST.get('amount')) >= 100.00:
                errors.append('Please enter amount less than 100')
        except:
            errors.append("Please enter valid amount")
   
        if not request.POST.get('date',''):
            errors.append('Please Enter Date')
        if not request.POST.get('desc',''):
            errors.append('Please enter a short description')
        elif len(request.POST.get('desc')) > 100:
            errors.append('Please enter title less than 100 characters')
        if len(request.POST.getlist('member')) < 2:
            errors.append('Please select atleast 2 members of transaction')
        
        print errors
        if not errors:
            trans_amount = request.POST.get('amount')
            trans_name = request.POST.get('title')
            trans_description = request.POST.get('desc')
            trans_date = request.POST.get('date')
            count = len(request.POST.getlist('member'))
            
            #try:
            print count
            val = Decimal(trans_amount) / count
            if str(request.user.id) in request.POST.getlist('member'):
                myamount = val
            else:
                myamount = 0.0

            t = Transaction(trans_amount=trans_amount,
                            trans_name=trans_name,
                            trans_date=trans_date,
                            trans_description=trans_description,
                            paidby=request.user,
                            amount=myamount)
            t.save()
           
            for member_id in request.POST.getlist('member'):
                member_id = int(member_id)
                b = Balancer(amount=val,
                             trans_id = t.id,
                             trans_member = User.objects.get(id = member_id)
                             )
                b.save()
            status = "Congrats, Successfully added new transaction to Database"
            #except:
            #    status = "Could not add to database"
            values = []
            values = Balancer.objects.filter(trans_member = request.user.id)
            print values
            friends = []
            friends = Frelation.objects.filter(a_user_id = request.user.id)
            mfriends = Frelation.objects.filter(friend_with_id = request.user.id)
            print friends
            print "myid: %d" %request.user.id
            for friend in friends:
                print friend.friend_with.first_name

            t = get_template('mypage.html')
            html = t.render(RequestContext(request,{ 'values':values,'status':status, 'friends':friends,'mfriends':mfriends, 'myid':request.user.id, 'username':request.user.username}))
            return HttpResponse(html)
    
    values = []
    values = Balancer.objects.filter(trans_member_id = request.user.id)
    friends = []
    friends = Frelation.objects.filter(a_user_id = request.user.id)
    mfriends = Frelation.objects.filter(friend_with_id = request.user.id)
    print friends
    for friend in friends:
        print friend.friend_with.first_name

    t = get_template('mypage.html')
    print values
    html = t.render(RequestContext(request,{ 'values':values,'errors':errors,'friends':friends,'mfriends':mfriends, 'myid':request.user.id, 'username':request.user.username}))
    return HttpResponse(html)
    # return HttpResponse("Good Work, Need to add to Database")


def transdetails(request,transid):
    ''
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/index/')

    values = []
    errors = []
    trans = []
    try:
        print transid
        values = Balancer.objects.filter(trans_id = int(transid))
        print values
        print "------"
        trans = Transaction.objects.get(id = int(transid))
        print trans
    except:
        errors.append('Not Found in Database')
    flag = False
    t = get_template('details.html')
    
    if not errors:
        for value in values:
            if value.trans_member.id == request.user.id:
                flag = True
                break
        if flag == False:
            if trans.paidby.id == request.user.id:
                flag = True
    
        if not flag:
            values =[]
            trans = []
    else:
        errors.append('Invalid Transaction')   
    html = t.render(RequestContext(request,{ 'values':values,'trans':trans, 'errors':errors }))
    return HttpResponse(html)
    

def logout(request):
    ''
    auth.logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect("/index/")
