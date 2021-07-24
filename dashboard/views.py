
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect 
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from dashboard.models import notification
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse

import json  
from sales.models import create_sales_table,create_sales_final,sale_totals
from product.models import products,sub_products

from returns.models import sales_returned
# Create your views here.
# def user_login(request):
# 	if request.method == 'POST':
		
# 		user_name=request.POST.get('username')
# 		pass_word=request.POST.get('password')

# 		user = authenticate(username=user_name, password=pass_word)
# 		if user:
# 			login(request,user)
# 			return HttpResponseRedirect('indexs')
# 		else:
# 			return render(request,'admin_billing/auth_login.html')
# 	return render(request,'admin_billing/auth_login.html')

def user_login(request):
	if request.method == 'POST':
		
		user_name=request.POST.get('username')
		pass_word=request.POST.get('password')


		user = authenticate(username=user_name, password=pass_word)
		if user:
			login(request,user)
			return HttpResponseRedirect('/indexs')
		else:
			return render(request,'dashboard/auth_login.html')
	return render(request,'dashboard/auth_login.html')

def user_logout(request):
	
	logout(request)
	return HttpResponseRedirect('login')


def create_table_ajax(request):
	tag_str=''
	tag_str2=''
	tag_str3=''
	tag_noti_pointer="<i class='mdi mdi-bell'></i>"
	import datetime
	now = datetime.datetime.now()
	month_31=[1,3,5,7,8,10,12]
	month_30=[4,6,9,11]

	if now.month in month_31:
		x=1
	if  now.month in month_30:
		x=2
	if(now.year%4==0 and now.year%100!=0 or now.year%400==0) and now.month==2:
		x=3
	if now.month==2:
		x=4 
	sale_tot=[]
	variablesss=[]
	for i in range(1,32):
		globals()["income_day" + str(i)] = 0
	for i in range(1,now.day+1):
		sales=sale_totals.objects.filter(sales_date__year=now.year, sales_date__month=now.month,sales_date__day=i)
		
		for s in sales:
			d=s.sales_totals
			globals()["income_day" + str(i)] = d			
	

	for i in range(1,32):
		globals()["expence_day" + str(i)] = 0
	# for i in range(1,now.day+1):
	# 	purchases=purchase_totals.objects.filter(purchase_time__year=now.year, purchase_time__month=now.month,purchase_time__day=i)
		
	# 	for s in purchases:
	# 		d=s.purchases_total
	# 		globals()["expence_day" + str(i)] = d

	sales_to=sale_totals.objects.filter(sales_date__year=now.year, sales_date__month=now.month)
	sale_sum=0
	for h in sales_to:
		sale_sum=float(sale_sum)+float(h.sales_totals)

	# purch_to=purchase_totals.objects.filter(purchase_time__year=now.year, purchase_time__month=now.month)

	purch_su=0
	# for dd in purch_to:
	# 	purch_su=float(purch_su)+float(dd.purchases_total)

	tod_sales=sale_totals.objects.values_list('sales_totals', flat=True).get(sales_date__year=now.year, sales_date__month=now.month,sales_date__day=now.day)

	# tod_purchases=purchase_totals.objects.values_list('purchases_total', flat=True).get(purchase_time__year=now.year, purchase_time__month=now.month,purchase_time__day=now.day)
	sale_c=create_sales_final.objects.filter(sales_date__year=now.year, sales_date__month=now.month,sales_date__day=now.day)
	sale_counts=0
	for cc in sale_c:
		sale_counts=sale_counts+1
	return_counts=0
	return_c=sales_returned.objects.filter(sale_return_date__year=now.year, sale_return_date__month=now.month,sale_return_date__day=now.day)
	retu_amou=0
	for cr in return_c:
		return_counts=return_counts+1
		retu_amou=float(retu_amou)+float(cr.sale_amount_return)


	sale_invoi=create_sales_final.objects.filter(sales_date__year=now.year, sales_date__month=now.month,sales_date__day=now.day)
	sal_pr_i=[]
	sal_pr_qt=[]
	for inv in sale_invoi:
		sal_pro_id=create_sales_table.objects.filter(sales_invoice_no=inv.sale_invoice_ref)
		for idd in sal_pro_id:
			sal_pr_i.append(idd.sales_product_ref_id)
			sal_pr_qt.append(idd.sales_qty)


	pro_prices=[]
	totals=0
	for pri,prqt in zip(sal_pr_i,sal_pr_qt):
		pro_pri=sub_products.objects.values_list('product_price', flat=True).get(pk=pri)
		pro_dis=sub_products.objects.values_list('product_discount', flat=True).get(pk=pri)
		pro_cost=sub_products.objects.values_list('product_cost', flat=True).get(pk=pri)
		
		pro_prices=float(pro_pri)-float(pro_dis)-float(pro_cost)
		totals=float(totals)+float(pro_prices*prqt)

	from datetime import date

	prod_inf=notification.objects.all()
	for prost in prod_inf:
		if float(prost.product_stock)<float(prost.product_low_stock_limit):
			

			tag_str=tag_str+'<a href="#"><i class="fa fa-warning text-danger"></i>Only {} item in stock of {} remaining</a>'.format(prost.product_stock,prost.product_name)
			tag_noti_pointer=" <div style='font-size: 12px; padding-left: 18px; margin: -12px; color: red;'><i class='mdi mdi-circle'></i></div><i class='mdi mdi-bell'></i>"
	sal_inf=create_sales_final.objects.all()



	
	# now = datetime.datetime.now()
	# tasks=tasks_table.objects.all()
	# for tsk in tasks:
	# 	if tsk.create_tasks_to_time>=date.today():
	# 		tsk_user=User.objects.values_list('username', flat=True).get(pk=tsk.create_tasks_staffs)
	# 		tag_str2=tag_str2+'<a href="#"><b style="font-size: 15px;">{}</b><br>From: {} To: {}<small class="pull-right"></small></a>'.format(tsk_user,tsk.create_tasks_from_time,tsk.create_tasks_to_time)


	jsona = json.dumps({'income_day1': income_day1,'income_day2': income_day2,'income_day3': income_day3,'income_day4': income_day4,'income_day5': income_day5,
		'income_day6': income_day6,'income_day7': income_day7,'income_day8': income_day8,'income_day9': income_day9,'income_day10': income_day10,
		'income_day11': income_day11,'income_day12': income_day12,'income_day13': income_day13,'income_day14': income_day14,'income_day15': income_day15,'income_day16': income_day16,
		'income_day17': income_day17,'income_day18': income_day18,'income_day19': income_day19,'income_day20': income_day20,'income_day21': income_day21,
		'income_day22': income_day22,'income_day23': income_day23,'income_day24': income_day24,'income_day25': income_day25,'income_day26': income_day26,
		'income_day27': income_day27,'income_day28': income_day28,'income_day29': income_day29,'income_day30': income_day30,'income_day31': income_day31,
		'expence_day1':expence_day1,'expence_day2':expence_day2,'expence_day3':expence_day3,'expence_day4':expence_day4,'expence_day5':expence_day5,
		'expence_day6':expence_day6,'expence_day7':expence_day7,'expence_day8':expence_day8,'expence_day9':expence_day9,'expence_day10':expence_day10,
		'expence_day11':expence_day11,'expence_day12':expence_day12,'expence_day13':expence_day13,'expence_day14':expence_day14,'expence_day15':expence_day15,
		'expence_day16':expence_day16,'expence_day17':expence_day17,'expence_day18':expence_day18,'expence_day19':expence_day19,'expence_day20':expence_day20,
		'expence_day21':expence_day21,'expence_day22':expence_day22,'expence_day23':expence_day23,'expence_day24':expence_day24,'expence_day25':expence_day25,
		'expence_day26':expence_day26,'expence_day27':expence_day27,'expence_day28':expence_day28,'expence_day29':expence_day29,'expence_day30':expence_day30,
		'expence_day31':expence_day31,'x':x,'sale_sum':sale_sum,'purch_su':purch_su,'tod_sales':round(float(tod_sales),2),'sale_counts':sale_counts,
		'return_counts':return_counts,'retu_amou':round(float(retu_amou),2),"incomes":round(float(tod_sales)-float(retu_amou),2),'totals':round(float(totals),2),'tag_str':tag_str,'tag_str2':tag_str2,'tag_str3':tag_str3,'tag_noti_pointer':tag_noti_pointer})
	return HttpResponse(jsona, content_type='application/json')



def create_table_ajaxing(request):
	import datetime
	now = datetime.datetime.now()
	

	sales_to=sale_totals.objects.filter(sales_date__year=now.year, sales_date__month=now.month)
	sale_sum=0
	for h in sales_to:
		sale_sum=float(sale_sum)+float(h.sales_totals)

	purch_to=purchase_totals.objects.filter(purchase_time__year=now.year, purchase_time__month=now.month)

	purch_su=0
	for dd in purch_to:
		purch_su=float(purch_su)+float(dd.purchases_total)
	

	
	jsona = json.dumps({'sale_sum':sale_sum,'purch_su':purch_su})
	return HttpResponse(jsona, content_type='application/json')

@login_required(login_url='/login')
def indexing(request):
	import datetime
	now = datetime.datetime.now()

	active_sidebar0=1
	sales=create_sales_final.objects.all().order_by('-id')[:5]

	
	prod_name=[]
	purcha_id=[]
	purch_id=[]
	stock=[]



	

	sales_date=sale_totals.objects.filter(sales_date__year=now.year, sales_date__month=now.month,sales_date__day=now.day)	
	if not sales_date:
		cre_sales_timings=sale_totals(
			sales_date=now,
			sales_totals=0
			)
		cre_sales_timings.save()

	
	
	return render(request,'dashboard/dash.html',{'active_sidebar0':active_sidebar0,'sales':sales})





@login_required(login_url='/login')
def error_page(request):
	return render(request,'admin_billing/error_400.html')







# # Create your views here.
def layout(request):
	return render(request,'dashboard/layout.html')
# def indexing(request):
	
	
# 	return render(request,'dashboard/dash.html')

def searching_product(request):
	if request.method == 'POST':
		
		search_result=request.POST.get('searches')
	pro_details=products.objects.filter(id__iexact=search_result)
	if not pro_details:
		pro_details=products.objects.filter(product_code__iexact=search_result)
		if not pro_details:
			pro_details=products.objects.filter(product_name__contains=search_result)
	active_sidebar1=1
	return render(request,'product/product_details.html',{'active_sidebar1':active_sidebar1,'pro_details':pro_details})

def clearall_ajax(request):
	notification.objects.all().delete()
	jsona = json.dumps({'cleared':"cleared__"})
	return HttpResponse(jsona, content_type='application/json')
	