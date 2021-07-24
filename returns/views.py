from django.shortcuts import render
from returns.forms import create_sales_returns,create_damaged_products,create_product_returns
from product.models import products,categorisation

from sales.models import create_sales_table,create_sales_final,reports
from returns.models import sales_returned,returned_sales_prod

from django.http import HttpResponse,HttpResponseRedirect
import json  
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required   
# Create your views here.
@login_required(login_url='/login')
def sales_return(request):
	return_id=[]
	return_cust=[]
	return_tim=[]
	returnable_amount=[]
	amount_returned=[]

	sale_return_details=sales_returned.objects.all().order_by('-id')
	for x in sale_return_details:
		return_id.append(x.id)
		return_tim.append(x.sale_return_date)
		returnable_amount.append(x.sale_amount_return)
		amount_returned.append(x.sale_return_cash_account)
		

	zipped=zip(return_id,return_tim,returnable_amount,amount_returned,sale_return_details)
	active_sidebar5=1
	return render(request,'returns/sales_return.html',{'active_sidebar5':active_sidebar5,'zipped':zipped})






@login_required(login_url='/login')
def create_sales_return(request):

	sales_cust_invo=create_sales_table.objects.values_list('sales_invoice_no', flat=True).distinct()
	

	
	sales_invoice=[] 
	sale_cust_name=[]

	sales=create_sales_final.objects.all().order_by('-sale_invoice_ref')
	
	
	if request.method == 'POST':
		
		
		form=create_sales_returns(request.POST)
		
		

	form=create_sales_returns()
	active_sidebar5=1
	return render(request,'returns/create_sales_return.html',{'active_sidebar5':active_sidebar5,'form':form,
		'sales_cust_invo':sales_cust_invo,'sales':sales})




@login_required(login_url='/login')
def create_sales_return2(request):
	aa=[]
	bb=[]
	tag_str=''
	final=0
	prod_code=[]
	prod_qty=[]
	if request.method == 'POST':
		get_id=request.POST.get('selected_cust')

		coun=request.POST.get('counting')
		
		
		
		for cc in range(1,int(coun)+1):
			if request.POST.get('check_%d'%cc) is not None:
				pass
				
				product_na=reports.objects.values_list('prod_name', flat=True).get(pk=request.POST.get('check_%d'%cc))
				product_pri=reports.objects.values_list('price', flat=True).get(pk=request.POST.get('check_%d'%cc))
				
				product_unit=reports.objects.values_list('unit', flat=True).get(pk=request.POST.get('check_%d'%cc))
				product_dis=reports.objects.values_list('discount', flat=True).get(pk=request.POST.get('check_%d'%cc))
				get_tax_category=reports.objects.values_list('tax_percent', flat=True).get(pk=request.POST.get('check_%d'%cc))
				tax_amount=float(get_tax_category)*float(product_pri)
				tax_amount=float(tax_amount)/100
				product_tot=float(product_pri)
				product_tot=round(product_tot,3)
				product_qt=request.POST.get('qty%d'%cc)
				prod_fin=float(product_qt)*float(product_tot)
				prod_fin=round(prod_fin)
				final=float(final)+float(prod_fin)
				prod_code.append(request.POST.get('check_%d'%cc))
				prod_qty.append(request.POST.get('qty%d'%cc))
				tag_str=tag_str+"<tr><td>{}</td><td><input class='form-control' type='number' placeholder='Qty' width='300' style='width: auto' id='qty_id' name='qty{}' value='{}' readonly='readonly'>\
				</td><td>{}</td><td>{}</td><td>{}</td><td>\
				<input class='form-control' type='number' placeholder='fina' width='300' style='width: auto' id='final_final' name='final_fin{}' value='{}' readonly='readonly'>\
				<input type='hidden' value='{}' id='counts' style='width: 0%;' name='counting'><input type='hidden' value='' id='finals' style='width: 0%;'>\
				</td></tr>".format(product_na,coun,product_qt,product_unit,product_tot,product_dis,coun,prod_fin,coun)

	# zipped=zip(prod_code,prod_qty)			
	# return HttpResponse(tag_str)

	active_sidebar1=3
	return render(request,'returns/create_sales_return2.html',{'tag_str':tag_str,'final':final,'get_id':get_id,'coun':coun,
		'prod_code':prod_code,'prod_qty':prod_qty})
@login_required(login_url='/login')
def save_sales_return(request):
	proo_=''
	if request.method == 'POST':
		get_id=request.POST.get('selected_cust')
		
		retu_amou=request.POST.get('return_returnable_amount')
		retu_retu=request.POST.get('return_amount_retuned')
		ret_time=request.POST.get('return_time')
		ret_transact=request.POST.get('return_transaction_mode')
		ret_cash=request.POST.get('return_cash_account')

		#return status
		update_return_status = create_sales_final.objects.filter(sale_invoice_ref=get_id).update(sale_return_status=1)

		cre_sale_returns=sales_returned(
			
			sales_invoice_ref=get_id,
			sales_returned_invoice=get_id,
			sale_amount_return=retu_amou,
			sale_return_date=ret_time,
			sale_return_transaction_mode=ret_transact,
			sale_return_cash_account=retu_retu,
			
			)
		cre_sale_returns.save()

		proo_cod=request.POST.getlist('pro_cod')
		proo_=''.join(proo_cod)
		import re
		pro_co=re.findall(r'\d+', proo_)
		
		proo_qty=request.POST.getlist('pro_qt')
		qty_=''.join(proo_qty)
		pro_q=re.findall(r'\d+', qty_)
		
		zippy=zip(pro_co,pro_q)

		for x,y in zippy:
			
			
			# product_stock_info=products.objects.values_list('product_stock', flat=True).get(pk=x)
			# pro_stock=float(product_stock_info)+float(y)
			# update_stock = products.objects.filter(pk=x).update(product_stock=pro_stock)
			# retu_pro = create_sales_table.objects.filter(sales_invoice_no=get_id,sales_product_ref_id=x)
			# for qtt in retu_pro:
			# 	new_qty=int(qtt.sales_qty)-int(y)
			
			# 	update_return = create_sales_table.objects.filter(sales_invoice_no=get_id,sales_product_ref_id=x).update(sales_qty=new_qty)
			cre_sale_return_pro=returned_sales_prod(
			sales_product_id=x,
			sales_returned_invoice_id_ref=get_id
			)
			cre_sale_return_pro.save()
		return HttpResponseRedirect("/create_sales_return")

	active_sidebar1=3
	return render(request,'returns/create_sales_return.html')

def create_sales_return_ajax(request):
	prod_ids=[]
	pro_qty=[]
	tag_str=""
	count=0

	if request.method == 'POST' and request.POST['action'] == 'return':

		get_id=request.POST.get('selection')

		get_pro_ref_id=reports.objects.filter(invoice_no=get_id)

		for b in get_pro_ref_id:
			pro_id=b.id
			product_name=b.prod_name
			unit_type_ref=b.unit
			product_discount=b.discount
			product_cost=20
			product_price=b.price
			product_price=b.price
			count=count+1
			disc_tot=float(product_price)-float(product_discount)
			qty_no=b.qty
			fin_total=float(qty_no)*float(disc_tot)


			tag_str=tag_str+"<tr><td><input type='checkbox' id='checkbox_{}' class='filled-in' name='check_{}' value='{}'>\
			<label for='checkbox_{}'></label></td><td>{}</td><td><input class='form-control' type='number' \
			placeholder='Qty' width='300' style='width: auto' id='qty_id' name='qty{}' value='{}' min='0' max='{}'></td><td>{}</td><td>{}</td><td>{}</td>\
			<td>{}</td><td><input type='hidden' value='{}' id='counts' style='width: 0%;' name='counting'></td>\
			</tr>".format(count,count,pro_id,count,product_name,count,qty_no,qty_no,unit_type_ref,product_price,product_discount,fin_total,count)
			# tag_head="<tr><th></th><th>PRODUCT</th><th>QTY</th><th>UNIT</th><th>PRICE</th><th>DISCOUNT</th><th>TOTAL</th><th>STATUS</th><th>SUBTOTAL</th></tr></thead><tbody>"

		jsona = json.dumps({'tag_str':tag_str,'count':count})

		return HttpResponse(jsona, content_type='application/json')


	if request.method == 'POST' and request.POST['action'] == 'custome':
		get_invoi_id=request.POST.get('cust')
		get_id=create_sales_final.objects.values_list('customer_ref_id', flat=True).get(sale_invoice_ref=get_invoi_id)
		get_cust_debit=customer.objects.values_list('customer_first_time_debit', flat=True).get(pk=get_id)
		get_cust_credit=customer.objects.values_list('customer_first_time_credit', flat=True).get(pk=get_id)
		jsona = json.dumps({'get_cust_debit':get_cust_debit,'get_cust_credit':get_cust_credit})
		return HttpResponse(jsona, content_type='application/json')

def create_sales_return_ajax2(request):
	if request.method == 'POST':
		coun=request.POST.get('count')
		for cc in range(1,int(coun)+1):
			if request.POST.get('check_%d'%cc) is not None:
				pass
				
				product_pr=products.objects.values_list('product_price', flat=True).get(pk=request.POST.get('check_%d'%cc))
				pro_tot_pric=int(product_pr)*int(request.POST.get('qty%d'%cc))
				

	jsona = json.dumps({'pro_tot_pric':pro_tot_pric})

	return HttpResponse(jsona, content_type='application/json')



@login_required(login_url='/login')
def delete_sales_return(request,id):
	delete_sales=sales_returned.objects.get(pk=id)
	delete_sales.delete()
	return HttpResponseRedirect('/sales_return/')

def delete_all_return(request):
	pro_list=request.POST.get('checked_pro')
	if pro_list=="0":
		return HttpResponseRedirect('/sales_return/')
	else:
		pro_pro_list = pro_list.split (",")
		
		# convert each element as integers
		pro_lists = []
		for i in pro_pro_list:
			pro_lists.append(int(i))

		for x in pro_lists:
			
			delete_sales=sales_returned.objects.get(pk=x)
			delete_sales.delete()
		return HttpResponseRedirect('/sales_return/')