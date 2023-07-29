from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.db import connection

# Create your views here.
def temp_function():
    return 1+2


def logout(request):
    return redirect('login')

def login(request):
    if request.method == "POST":
        userid = request.POST['name']
        password = request.POST['password']

        cursor = connection.cursor()
        cursor.execute("select * from user_register where user_id= '" + userid + "' and password = '"+password+"'")
        user = cursor.fetchone()
        if user == None:
            cursor.execute("select * from login where admin_id = '" + userid + "' AND password = '" + password + "'")
            admin = cursor.fetchone()
            if admin == None:
                cursor.execute("select * from panchayat where idpanchayat = '" + userid + "' and password = '"+password+"' ")
                panchayat = cursor.fetchone()
                if  panchayat== None:
                    cursor.execute("select * from worker where name = '" +userid +"' and password = '"+password+"'")
                    worker = cursor.fetchone()
                    if worker == None:
                        return redirect('login')
                    else:
                        request.session['workerid'] = userid
                        return redirect('workerhome')
                else:
                    request.session["panchayatId"] = userid
                    return redirect('panchayathome')
            else:
                request.session["adminId"] = userid
                return redirect('adminhome')
        else:
            request.session["userId"] = userid
            return redirect("userhome")
    return render(request, "login.html")

# worker ---------------------------------------------------------------------------------------

def worker_home(request):
    return render(request,'worker/index.html')

def view_work(request):
    worker = request.session["workerid"]
    cursor = connection.cursor()
    cursor.execute("select idpanchayat from worker where name = '"+str(worker)+"' ")
    data = cursor.fetchone()
    panchayat = data[0]
    cursor.execute("select waste_booking.user_id,waste_booking.waste_description,waste_booking.amount,category.name,waste_booking.idwaste_booking,waste_booking.idcategory,waste_booking.book_date,waste_booking.r_status from waste_booking join category where waste_booking.idcategory = category.idcategory and waste_booking.idpanchayat = '"+str(panchayat)+"' and waste_booking.status = 'paid'")
    booking = cursor.fetchall()
    connection.close()
    return render(request, 'worker/view_work.html', {'data': booking})

def apply_leave(request):
    if request.method == 'POST':
        name = request.session['workerid']
        date = request.POST['date']
        details = request.POST['details']
        cursor = connection.cursor()
        cursor.execute("select idworker from worker where name = '"+str(name)+"'")
        worker = cursor.fetchone()
        workerid = worker[0]
        print(str(date),details,name,workerid,"----------------------------------------------------------------------------")
        cursor.execute("insert into worker_leave values(null,'"+str(workerid)+"','"+str(details)+"','"+str(date)+"','pending')")
        cursor.close()
        return HttpResponse("<script>alert('Leave letter submitted');window.location='../workerhome';</script>")
    return render(request,'worker/apply_leave.html')

def view_approved_leave(request):
    cursor = connection.cursor()
    name = request.session['workerid']
    cursor.execute("select idworker from worker where name = '" + str(name) + "'")
    worker = cursor.fetchone()
    workerid = worker[0]
    cursor.execute("select * from leave where workerid = '"+str(workerid)+"' and status = 'approved'")
    leave = cursor.fetchall()
    return render(request,'worker/view_approved_leave.html')


# admin ----------------------------------------------------------------------------------------
def admin_home(request):
    return render(request,'admin/index.html')

def add_district(request):
    if request.method == 'POST':
        name = request.POST['name']

        cursor = connection.cursor()
        cursor.execute("insert into district values(null,'"+str(name)+"')")
        return redirect('adddistrict')
    else:
        return render(request,'admin/add_district.html')

def view_district(request):
    cursor = connection.cursor()
    cursor.execute("select * from district")
    district = cursor.fetchall()
    connection.close()
    return render(request,'admin/view_district.html',{'data':district})

def add_taluk(request,id):
    cursor = connection.cursor()
    if request.method == 'POST':
        taluk = request.POST['name']

        cursor.execute("select * from taluk where taluk_name = '"+str(taluk)+"'")
        Taluk = cursor.fetchone()
        if Taluk == None:
            cursor.execute("insert into taluk values(null,'"+str(id)+"','"+str(taluk)+"')")
            return redirect('addtaluk',id)
        else:
            return HttpResponse("<script>alert('Taluk name already exists');window.location='../addtaluk/<str:id>';</script>")
    else:
        cursor.execute("select * from district where iddistrict = '"+str(id)+"'")
        district = cursor.fetchone()
        return render(request,'admin/add_taluk.html',{'data':district})

def select_district(request):
    cursor = connection.cursor()
    cursor.execute("select * from district")
    district = cursor.fetchall()
    connection.close()
    return render(request,'admin/select_district.html',{'data':district})


def select_taluk(request,id):
    cursor = connection.cursor()
    cursor.execute("select * from taluk where iddistrict = '"+str(id)+"'")
    taluk = cursor.fetchall()
    connection.close()
    return render(request,'admin/select_taluk.html',{'data':taluk})

def add_panchayat(request,id):
    cursor = connection.cursor()
    if request.method == 'POST':

        panchayatid = request.POST['name']
        address = request.POST['address']
        place = request.POST['place']
        phone = request.POST['phone']
        email = request.POST['email']
        district = request.POST['district']
        taluk = request.POST['taluk']
        password = request.POST['password']

        cursor.execute("select * from panchayat where idpanchayat = '"+str(panchayatid)+"'")
        hospital = cursor.fetchone()
        if hospital == None:
            cursor.execute("insert into panchayat values('"+str(panchayatid)+"','"+str(address)+"','"+str(place)+"','"+str(phone)+"','"+str(email)+"','"+str(taluk)+"','"+str(district)+"','"+str(password)+"')")
            return redirect('selectdistrict')
        else:
            return HttpResponse("<script>alert('Hospital already exists');window.location='../selectdistrict';</script>")
    else:
        cursor.execute("select * from taluk where idtaluk = '"+str(id)+"'")
        taluk = cursor.fetchone()
        return render(request,'admin/add_panchayat.html',{'data':taluk})

def view_panchayat(request):
    cursor = connection.cursor()
    cursor.execute("select panchayat.*,district.name,taluk.taluk_name from panchayat join district join taluk where panchayat.iddistrict = district.iddistrict and panchayat.idtaluk = taluk.idtaluk")
    panchayat = cursor.fetchall()
    connection.close()
    return render(request,'admin/view_panchayat.html',{'data':panchayat})

def edit_panchayat(request,id):
    cursor = connection.cursor()
    if request.method == 'POST':
        address = request.POST['address']
        place = request.POST['place']
        phone = request.POST['phone']
        email = request.POST['email']
        password = request.POST['password']
        cursor.execute("update panchayat set address = '"+str(address)+"',place = '"+str(place)+"',phone = '"+str(phone)+"',email = '"+str(email)+"',password = '"+str(password)+"' where idpanchayat = '"+str(id)+"'")
        return redirect('viewpanchayat')
    else:
        cursor.execute("select * from panchayat where idpanchayat = '"+str(id)+"'")
        panchayat = cursor.fetchone()
        return render(request,'admin/edit_panchayat.html',{'data':panchayat})

def delete_panchayat(request,id):
    cursor = connection.cursor()
    cursor.execute("delete from panchayat where idpanchayat = '"+str(id)+"'")
    return redirect('viewpanchayat')

def add_category(request):
    if request.method == 'POST':
        name = request.POST['name']
        price = request.POST['price']

        cursor = connection.cursor()
        cursor.execute("select * from category where name = '"+str(name)+"' ")
        category = cursor.fetchone()

        if category == None:
            cursor.execute("insert into category values(null,'" + str(name) + "','" + str(price) + "')")
            connection.close()
            return redirect('addcategory')
        else:
            return HttpResponse("<script>alert('already exists');window.location='../addcategory';</script>")
    else:
        return render(request, 'admin/add_category.html')

def view_category(request):
    cursor = connection.cursor()
    cursor.execute("select * from category")
    category = cursor.fetchall()
    connection.close()
    return render(request,'admin/view_category.html',{'data':category})


def edit_category(request,id):
    cursor = connection.cursor()
    if request.method == 'POST':
        name = request.POST['category']
        price = request.POST['price']
        cursor.execute("update category set name='"+str(name)+"', price = '"+str(price)+"' where idcategory ='"+str(id)+"'")
        connection.close()
        return redirect('viewcategory')
    else:
        cursor.execute("select * from category where idcategory = '"+str(id)+"'")
        category = cursor.fetchone()
        connection.close()
        return render(request,'admin/edit_category.html',{'data':category})

def delete_category(request,id):
    cursor = connection.cursor()
    cursor.execute("delete from category where idcategory = '"+str(id)+"'")
    connection.close()
    return redirect('viewcategory')

def select_category(request):
    cursor = connection.cursor()
    cursor.execute("select * from category")
    category = cursor.fetchall()
    return render(request,'admin/view_category1.html',{'data':category})

def add_recycle_category(request,id):
    if request.method == 'POST':
        name = request.POST['name']
        cursor = connection.cursor()
        cursor.execute("insert into recycle_category values(null,'"+str(name)+"','"+str(id)+"')")

        return HttpResponse("<script>alert('Recycle category name added');window.location='../selectcategory';</script>")

    else:
        return render(request,'admin/add_recycle_category.html')

def view_recycle_category(request,id):
    cursor = connection.cursor()
    cursor.execute("select recycle_category.name,recycle_category.idrecycle_category from recycle_category where idcategory = '"+str(id)+"'")
    items = cursor.fetchall()
    connection.close()
    return render(request,'admin/view_recycle_category.html',{'data':items})

def delete_recycle_category(request,id):
    cursor = connection.cursor()
    cursor.execute("delete from recycle_category where idrecycle_category = '"+str(id)+"'")
    return HttpResponse("<script>alert('Recycle Category Name Deleted');window.location='../selectcategory';</script>")

def admin_recycled_items(request):
    cursor = connection.cursor()
    cursor.execute("select waste_booking.idpanchayat,category.name,recycle.description from recycle join waste_booking join category where recycle.status = 'success' and recycle.idwaste_booking = waste_booking.idwaste_booking and category.idcategory = waste_booking.idcategory")
    recycle = cursor.fetchall()
    return render(request,'admin/recycled_items.html',{'data':recycle})


# user---------------------------------------------------------------------------------------------------------

def user_home(request):
    return render(request,'user/index.html')

def user_select_district(request):
    cursor = connection.cursor()
    cursor.execute("select * from district")
    district = cursor.fetchall()
    connection.close()
    return render(request,'select_district.html',{'data':district})

def user_select_taluk(request,id):
    cursor = connection.cursor()
    cursor.execute("select * from taluk where iddistrict = '"+str(id)+"'")
    taluk = cursor.fetchall()
    connection.close()
    return render(request,'select_taluk.html',{'data':taluk})

def user_select_panchayat(request,id):
    cursor = connection.cursor()
    cursor.execute("select * from panchayat where idtaluk = '"+str(id)+"'")
    panchayat = cursor.fetchall()
    connection.close()
    return render(request,'select_panchayat.html',{'data':panchayat})



def user_register(request,id):
    if request.method == "POST":
        user_id = request.POST['name']

        name = request.POST['name']
        address = request.POST['address']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']

        cursor = connection.cursor()
        cursor.execute("select * from user_register where user_id= '" + user_id + "' ")
        user = cursor.fetchone()

        if user == None:
            cursor.execute("insert into user_register values('" + user_id + "','" + str(name) + "','" + str(address) + "','" + str(phone) + "','" + str(email) + "','" + str(password) + "','" + str(id) + "')")
            request.session["userId"] = user_id
            return redirect('userhome')
        else:
            return HttpResponse("<script>alert('User Name already exists');window.location='../userregister/'"+id+"'';</script>")
    else:
        return render(request,'user_register.html')

def user_view_category(request):
    cursor = connection.cursor()
    cursor.execute("select * from category")
    category = cursor.fetchall()
    return render(request,'user/view_category.html',{'data':category})


def add_booking(request,id):
    cursor = connection.cursor()
    request.session['categoryId'] = id
    if request.method == 'POST':
        kg = request.POST['kg']

        cursor.execute("select category.price from category where idcategory = '"+str(id)+"'")
        price = cursor.fetchone()
        price = list(price)
        qty = price[0]
        total = int(qty)*int(kg)
        print("-----------------------------------------------------------------------------",total)
        return render(request,'user/waste_booking.html',{'data':total})

def book_waste(request):
    if request.method == 'POST':
        description = request.POST['description']
        total = request.POST['total']

        userid = request.session['userId']
        cursor = connection.cursor()
        cursor.execute("select user_register.idpanchayat from user_register where user_id = '"+str(userid)+"'")
        idp = cursor.fetchone()
        l = list(idp)
        idpanchayat = l[0]
        categoryID = request.session['categoryId']
        cursor.execute("insert into waste_booking values(null,'"+str(idpanchayat)+"','"+str(userid)+"',curdate(),'"+str(categoryID)+"','"+str(description)+"','pending','"+str(total)+"','recycle')")
        return redirect('bookingsuccess')

def booking_success_page(request):
    return render(request,'user/success_page.html')

def view_panchayat_approved(request):
    userid = request.session['userId']
    cursor = connection.cursor()
    cursor.execute("select waste_booking.user_id,waste_booking.waste_description,waste_booking.amount,category.name,waste_booking.idwaste_booking from waste_booking join category where waste_booking.status = 'approved' and waste_booking.idcategory = category.idcategory and waste_booking.user_id = '"+str(userid)+"'")
    approved = cursor.fetchall()
    return render(request,'user/view_panchayat_approved.html',{'data':approved})

def make_payment(request,id):
    userid = request.session['userId']
    cursor = connection.cursor()
    if request.method == 'POST':
        card_number = request.POST['card_no']
        cvv = request.POST['cvv']
        exp_date = request.POST['date']
        card_holder = request.POST['name']

        cursor.execute("select * from account where card_number = '"+str(card_number)+"' and cvv = '"+str(cvv)+"' and exp_date = '"+str(exp_date)+"' and card_holder = '"+str(card_holder)+"'")
        account = cursor.fetchone()
        if account == None:
            return HttpResponse("<script>alert('account details incorrect');window.location='../panchayatapproved'</script>")
        else:
            cursor.execute("update waste_booking set status = 'paid' where idwaste_booking = '"+str(id)+"' and user_id = '"+str(userid)+"'")
            return render(request,'user/success_page1.html')

    else:
        cursor.execute("select * from account")
        account = cursor.fetchone()
        return render(request,'user/make_payment.html',{'data':account})


def payment_success_page(request):
    return render(request,'user/success_page1.html')


def pending_booking(request):
    userid = request.session['userId']
    cursor = connection.cursor()
    cursor.execute("select waste_booking.user_id,waste_booking.waste_description,waste_booking.amount,category.name,waste_booking.idwaste_booking from waste_booking join category where waste_booking.status = 'pending' and waste_booking.idcategory = category.idcategory and waste_booking.user_id = '"+str(userid)+"'")
    pending = cursor.fetchall()
    return render(request,'user/view_pending_booking.html',{'data':pending})


def delete_pending_booking(request,id):
    cursor = connection.cursor()
    cursor.execute("delete from waste_booking where idwaste_booking = '"+str(id)+"'")
    connection.close()
    return redirect('pendingbooking')

def booked_items(request):
    userid = request.session['userId']
    cursor = connection.cursor()
    cursor.execute("select waste_booking.user_id,waste_booking.waste_description,waste_booking.amount,category.name,waste_booking.idwaste_booking,waste_booking.book_date from waste_booking join category where waste_booking.status = 'paid' and waste_booking.idcategory = category.idcategory and waste_booking.user_id = '"+str(userid)+"'")
    booked = cursor.fetchall()
    return render(request,'user/view_booked_items.html',{'data':booked})

def add_complaint(request):
    cursor = connection.cursor()
    if request.method == 'POST':
        userid = request.session['userId']
        details = request.POST['details']

        cursor.execute("select user_register.idpanchayat from user_register where user_id = '"+str(userid)+"'")
        idpanchayat = cursor.fetchone()
        l = list(idpanchayat)
        id = l[0]

        cursor.execute("insert into complaint values(null,'"+str(userid)+"',curdate(),'"+str(details)+"','pending','"+str(id)+"')")
        return redirect('addcomplaint')
    else:
        return render(request,'user/add_complaint.html')

def view_complaint_reply(request):
    userid = request.session['userId']
    cursor = connection.cursor()
    cursor.execute("select * from complaint where user_id = '"+str(userid)+"' and reply !='pending'")
    reply = cursor.fetchall()
    return render(request,'user/view_complaint_reply.html',{'data':reply})


# panchayat---------------------------------------------------------------------------------------------------------------------------------


def panchayat_home(request):
    return render(request,'panchayat/index.html')

def view_booking_request(request):
    idpanchayat = request.session["panchayatId"]
    cursor = connection.cursor()
    cursor.execute("select waste_booking.user_id,waste_booking.waste_description,waste_booking.amount,category.name,waste_booking.idwaste_booking from waste_booking join category where waste_booking.status = 'pending' and waste_booking.idcategory = category.idcategory and waste_booking.idpanchayat = '"+str(idpanchayat)+"'")
    booking = cursor.fetchall()
    connection.close()
    return render(request,'panchayat/view_booking_request.html',{'data':booking})

def delete_booking(request,id):
    cursor = connection.cursor()
    cursor.execute("delete from waste_booking where idwaste_booking = '"+str(id)+"'")
    connection.close()
    return redirect('viewbookingrequest')

def approve_booking(request,id):
    cursor = connection.cursor()
    cursor.execute("update waste_booking set status = 'approved' where idwaste_booking = '"+str(id)+"'")
    connection.close()
    return redirect('viewbookingrequest')

def booked_user(request):
    idpanchayat = request.session["panchayatId"]
    cursor = connection.cursor()
    cursor.execute("select waste_booking.user_id,waste_booking.waste_description,waste_booking.amount,category.name,waste_booking.idwaste_booking,waste_booking.idcategory,waste_booking.book_date,waste_booking.r_status from waste_booking join category where waste_booking.idcategory = category.idcategory and waste_booking.idpanchayat = '"+str(idpanchayat)+"' and waste_booking.status = 'paid'")
    booking = cursor.fetchall()
    connection.close()
    return render(request, 'panchayat/view_booked.html', {'data': booking})

def view_complaint(request):
    panchayatid = request.session['panchayatId']
    cursor = connection.cursor()
    cursor.execute("select * from complaint where reply = 'pending' and idpanchayat = '"+str(panchayatid)+"'")
    complaint = cursor.fetchall()
    connection.close()
    return render(request,'panchayat/view_complaint.html',{'data':complaint})

def send_reply(request,id):
    panchayatid = request.session['panchayatId']
    if request.method == 'POST':
        msg = request.POST['msg']
        cursor = connection.cursor()
        cursor.execute("update complaint set reply = '"+str(msg)+"' where idcomplaint = '"+str(id)+"' and idpanchayat = '"+str(panchayatid)+"'")
        return redirect('viewcomplaint')

def recyle_Category(request,id,idw):
    cursor = connection.cursor()
    if request.method == 'POST':
        idcategory = id
        idrecycle_category = request.POST['idrecycle_category']
        idwastebooking = idw
        description = request.POST['description']
        cursor.execute("insert into recycle values(null,'"+str(idrecycle_category)+"','"+str(idwastebooking)+"','"+str(description)+"','success')")

        return redirect('thankspage')

    else:
        cursor.execute("select * from recycle where idwaste_booking= '"+str(idw)+"'")
        recycle = cursor.fetchone()
        if recycle == None:
            cursor.execute("select * from recycle_category where idcategory= '"+str(id)+"'")
            items = cursor.fetchall()
            print(items,"--------------------------------------------------------------------------")
            return render(request,'panchayat/view_recycle_category.html',{'data':items})
        else:
            return HttpResponse("<script>alert('already recycled');window.location='../../../bookeduser'</script>")

def thanks_page(request):
    return render(request,'panchayat/thanks.html')

def recycled_items(request):
    cursor = connection.cursor()
    cursor.execute("select category.name,recycle_category.name,recycle.description,waste_booking.user_id from recycle join waste_booking join category join recycle_category where waste_booking.idwaste_booking = recycle.idwaste_booking and waste_booking.idcategory = recycle_category.idcategory and category.idcategory = recycle_category.idcategory and recycle.status = 'success' and recycle.idrecycle_category = recycle_category.idrecycle_category")
    # cursor.execute("select recycle_category.name,recycle.description,waste_booking.user_id from recycle join waste_booking join recycle_category where waste_booking.idwaste_booking = recycle.idwaste_booking and recycle.status = 'success' and recycle.idrecycle_category = recycle_category.idrecycle_category")

    recycled = cursor.fetchall()
    print(recycled,"--------------------------------------------------------------------")
    return render(request,'panchayat/view_recycled.html',{'data':recycled})

def add_worker(request):
    if request.method == 'POST':
        idpanchayat = request.session["panchayatId"]
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        address = request.POST['address']
        password = request.POST['password']

        cursor = connection.cursor()
        cursor.execute("select * from worker where name = '"+str(name)+"' ")
        worker = cursor.fetchone()
        if worker == None:
            cursor.execute("insert into worker values(null,'"+str(idpanchayat)+"','"+str(name)+"','"+str(phone)+"','"+str(email)+"','"+str(address)+"','"+str(password)+"')")
            connection.close()
            return HttpResponse("<script>alert('worker added successfully');window.location='../addworker'</script>")
        else:
            return HttpResponse("<script>alert('This worker already added ');window.location='../addworker'</script>")

    return render(request,'panchayat/add_worker.html')

def view_workers(request):
    cursor = connection.cursor()
    idpanchayat = request.session['panchayatId']
    cursor.execute("select * from worker where idpanchayat = '"+str(idpanchayat)+"'")
    worker = cursor.fetchall()
    connection.close()
    return render(request,'panchayat/view_worker.html',{'data':worker})

def delete_worker(request,id):
    cursor = connection.cursor()
    cursor.execute("delete from worker where idworker = '"+str(id)+"'")
    connection.close()
    return redirect('viewworkers')


def view_workers1(request):
    cursor = connection.cursor()
    idpanchayat = request.session['panchayatId']
    cursor.execute("select * from worker where idpanchayat = '"+str(idpanchayat)+"'")
    worker = cursor.fetchall()
    connection.close()
    return render(request,'panchayat/view_workers1.html',{'data':worker})

def salary_amount(request,id):
    if request.method == 'POST':
        idpanchayat = request.session['panchayatId']
        amount = request.POST['a']
        cursor = connection.cursor()
        cursor.execute("insert into salary values(null,'"+str(id)+"','"+str(idpanchayat)+"','"+str(amount)+"','pending')")
        connection.close()
        return redirect('addworkerpayment')
    else:
        return render(request,'panchayat/salary_amount.html')


def add_worker_payment(request):
    cursor = connection.cursor()
    if request.method == 'POST':
        card_number = request.POST['card_no']
        cvv = request.POST['cvv']
        exp_date = request.POST['date']
        card_holder = request.POST['name']

        cursor.execute("select * from account where card_number = '"+str(card_number)+"' and cvv = '"+str(cvv)+"' and exp_date = '"+str(exp_date)+"' and card_holder = '"+str(card_holder)+"'")
        account = cursor.fetchone()
        if account == None:
            return HttpResponse("<script>alert('account details incorrect');window.location='../viewworkers1'</script>")
        else:
            return render(request,'panchayat/success_page.html')

    else:
        cursor.execute("select * from account")
        account = cursor.fetchone()
        return render(request,'panchayat/worker_payment.html',{'data':account})

def view_worker_name(request):
    cursor = connection.cursor()
    cursor.execute("select name from worker ")

def view_worker_list(request):
    cursor = connection.cursor()
    # cursor.execute("select worker.idworker,worker.name,leave.status from worker join leave where leave.status = 'pending' and worker.idworker = leave.workerid ")
    cursor.execute("select worker.idworker,worker.name from worker join worker_leave where worker_leave.status = 'pending' and worker.idworker = worker_leave.workerid ")
    worker = cursor.fetchall()
    workers = set(worker)
    return render(request,'panchayat/view_workers_list.html',{'data':workers})

def view_worker_leave(request,id):
    cursor = connection.cursor()
    cursor.execute("select * from worker_leave where status = 'pending' and workerid = '"+str(id)+"'")
    pending = cursor.fetchall()
    cursor.close()
    return render(request,'panchayat/view_worker_leave.html',{'data':pending})

def approve_leave(request,id):
    cursor = connection.cursor()
    cursor.execute("update worker_leave set status = 'approved' where idworker_leave = '"+str(id)+"'")