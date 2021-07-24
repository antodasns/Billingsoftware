from django.shortcuts import render 
from django.http import HttpResponse,HttpResponseRedirect
from product.forms import create_product,create_purchases,create_purchase_invoices,create_asset_purchases,create_barcodes,uploading_products
from product.models import products,categorisation,alternate_units,sub_products,alternate_cost_price
from dashboard.models import notification
from itertools import*
import json    
import barcode   
import random  
from barcode.writer import ImageWriter
from PIL import Image
import xlrd 
from django.core.files import File
from django.contrib.auth.models import User 
from django.contrib.auth.decorators import login_required
import re
from settings_billing.models import store_details
# Create your views here.
@login_required(login_url='/login')
def product_details(request):
	
	pro_details=products.objects.all().order_by('-id')
	active_sidebar1=1
	return render(request,'product/product_details.html',{'active_sidebar1':active_sidebar1,'pro_details':pro_details})
	
@login_required(login_url='/login')
def purchase_details(request):

	purch_details=purchase_final.objects.all()
	active_sidebar2=1
	return render(request,'product/purchase_details.html',{'active_sidebar2':active_sidebar2,'purch_details':purch_details})
	
@login_required(login_url='/login')
def create_barcode_id(request,id):
	
	prodx=products.objects.all()
	pro_name=products.objects.values_list('product_name', flat=True).get(pk=id)
	form=create_barcodes()
	active_sidebar2=1
	return render(request,'product/create_barcode.html',{'active_sidebar2':active_sidebar2,'form':form,'prodx':prodx,"prid":id,"pro_name":pro_name})
	
@login_required(login_url='/login')
def create_barcode(request):
	
	prodx=products.objects.all()
	form=create_barcodes()
	active_sidebar2=1
	return render(request,'product/create_barcode.html',{'active_sidebar2':active_sidebar2,'form':form,'prodx':prodx})

@login_required(login_url='/login')
def barcode_generator(request):

	if request.method == 'POST':
		
		prod_id=request.POST.get('selected_product')
		unit=request.POST.get('unit')
		prod_name=products.objects.values_list('product_name', flat=True).get(pk=prod_id)
		prod_cost=float(products.objects.values_list('product_price', flat=True).get(pk=prod_id))+float(products.objects.values_list('product_tax_amount', flat=True).get(pk=prod_id))
		prod_cost=round(prod_cost)
		prod_code=products.objects.values_list('product_code', flat=True).get(pk=prod_id)
		#return HttpResponse(len(prod_code))
		#length=len(list(filter(lambda m:m.isdigit(), str(prod_code))))
		length=len(prod_code)
		image=barcode.get_barcode_class('code128')
		image_bar=image('{0}'.format(prod_code), writer=ImageWriter())
		file=open('/var/www/html/django/store_billing_lite/static/images/barcode/vj1.png',"wb")
		image_bar.write(file)
		

		file = '/var/www/html/django/store_billing_lite/static/images/barcode/vj1.png'
		if length==3:
			im = Image.open(file)
			crop_rectangle = (20, 168, 200, 195)
			cropped_im = im.crop(crop_rectangle)
			cropped_im.save(file)
		elif length==4:
			im = Image.open(file)
			crop_rectangle = (20, 165, 225, 196)
			cropped_im = im.crop(crop_rectangle)
			cropped_im.save(file)
		elif length==5:
			im = Image.open(file)
			crop_rectangle = (20, 162, 260, 198)
			cropped_im = im.crop(crop_rectangle)
			cropped_im.save(file)
		elif length==6:
			im = Image.open(file)
			crop_rectangle = (20, 163, 270, 200)
			cropped_im = im.crop(crop_rectangle)
			cropped_im.save(file)
		else:
			im = Image.open(file)
			crop_rectangle = (20, 165, 290, 200)
			cropped_im = im.crop(crop_rectangle)
			cropped_im.save(file)
		unit=int(unit)

		unit_list=[]
		for x in range(unit):
			unit_list.append(x)	
	active_sidebar4=1
	store_info=store_details.objects.latest('id')
	return render(request,'barcodes/bar.html',{'unit_list':unit_list,'prod_code':prod_code,'prod_name':prod_name,
		'prod_cost':prod_cost,'store_info':store_info})
	
############################################################################################################

 
 
 
################################# create product ##########################################################
@login_required(login_url='/login')
def create_products(request):

	prodx=products.objects.all()
	repeat_category=products.objects.order_by().values_list('category_ref', flat=True).distinct()
	repeat_brand=products.objects.order_by().values_list('brand_ref', flat=True).distinct()
	units=categorisation.objects.all()
	
	if request.method == 'POST':
		form=create_product(request.POST)
		pro_name=request.POST['product']
		if pro_name.isdigit():
			if form.is_valid():
				old_stock=products.objects.values_list('product_stock', flat=True).get(pk=pro_name)
				
				update_stock = products.objects.filter(pk=pro_name).update(product_stock=int(request.POST.get('product_stock'))+int(old_stock))
				update_limit_stock = products.objects.filter(pk=pro_name).update(product_low_stock_limit=request.POST.get('product_low_stocklimit'))
				# update_cost = products.objects.filter(pk=pro_name).update(product_cost=form.cleaned_data['product_cost'])
				# update_mrp = products.objects.filter(pk=pro_name).update(product_price=form.cleaned_data['product_price'])
				# update_wholesale = products.objects.filter(pk=pro_name).update(product_wholesale_price=form.cleaned_data['product_wholesale_price'])
				# update_disc = products.objects.filter(pk=pro_name).update(product_discount=form.cleaned_data['product_discount'])
				# product_code=form.cleaned_data['product_code']
				# product_hsn=form.cleaned_data['product_hsn']
				# product_alternate_cost=form.cleaned_data['product_alter_cost']
				# product_alternate_price=form.cleaned_data['product_alter_price']
				
				notify_update = notification.objects.filter(pk=pro_name).first()
				
				if notify_update == None:
					cre_notification=notification(
					id=products.objects.values_list('id', flat=True).get(pk=pro_name),
					product_name=products.objects.values_list('product_name', flat=True).get(pk=pro_name),
					product_stock=request.POST.get('product_stock'),
					product_low_stock_limit=request.POST.get('product_low_stocklimit')
					)
					cre_notification.save()

				notify_update_product_stock=notification.objects.filter(pk=pro_name).update(product_stock=request.POST.get('product_stock'))
				notify_update_product_low_stock_limit=notification.objects.filter(pk=pro_name).update(product_low_stock_limit=request.POST.get('product_low_stocklimit'))
		
				
				
			else:
				return HttpResponse(form.errors)
			return HttpResponseRedirect("/create_products")

		else:
			
			if form.is_valid():
				tax_inc=request.POST.get('taxes_stat')
				
				if tax_inc=="True":
					tax_stat="in"
					tax_amount=float(request.POST.get('product_tax_category'))*float(request.POST.get('product_price'))
					tax_amount=float(tax_amount)/100
					prod_price=float(request.POST.get('product_price'))-tax_amount
					final_pro_price=request.POST.get('product_price')
					taxable_amount=(float(request.POST.get('product_price'))*100)/(100+float(request.POST.get('product_tax_category')))

					# alter_tax_amount=float(request.POST.get('product_tax_category'))*float(request.POST['product_alter_price0'])
					# alter_tax_amount=float(tax_amount)/100
					# alter_prod_price=float(request.POST['product_alter_price0'])-tax_amount

					# alter_final_pro_price=request.POST['product_alter_price']
					# alter_taxable_amount=(float(request.POST['product_alter_price'])*100)/(100+float(request.POST.get('product_tax_category')))
				else:
					tax_stat="ex"
					tax_amount=float(request.POST.get('product_tax_category'))*float(request.POST.get('product_price'))
					tax_amount=float(tax_amount)/100
					prod_price=float(request.POST.get('product_price'))+tax_amount
					final_pro_price=float(request.POST.get('product_price'))+tax_amount
					taxable_amount=float(request.POST.get('product_price'))

					# alter_tax_amount=float(request.POST.get('product_tax_category'))*float(request.POST['product_alter_price0'])
					# alter_tax_amount=float(tax_amount)/100
					# alter_prod_price=float(request.POST['product_alter_price0'])+tax_amount

					# alter_final_pro_price=float(request.POST['product_alter_price'])+tax_amount
					# alter_taxable_amount=float(request.POST['product_alter_price'])

				#wholesale............................

				if tax_inc=="True":
					
					wholesale_tax_amount=float(request.POST.get('product_tax_category'))*float(request.POST.get('product_wholesale_price'))
					wholesale_tax_amount=float(wholesale_tax_amount)/100
					wholesale_prod_price=float(request.POST.get('product_wholesale_price'))-wholesale_tax_amount
					wholesale_final_pro_price=request.POST.get('product_wholesale_price')
					wholesale_taxable_amount=(float(request.POST.get('product_wholesale_price'))*100)/(100+float(request.POST.get('product_tax_category')))
				else:
					
					wholesale_tax_amount=float(request.POST.get('product_tax_category'))*float(request.POST.get('product_wholesale_price'))
					wholesale_tax_amount=float(wholesale_tax_amount)/100
					wholesale_prod_price=float(request.POST.get('product_wholesale_price'))+wholesale_tax_amount
					wholesale_final_pro_price=float(request.POST.get('product_wholesale_price'))+wholesale_tax_amount
					wholesale_taxable_amount=float(request.POST.get('product_wholesale_price'))

				# return HttpResponse(request.POST.get('product_tax_category'))
				tax_amount=float(request.POST.get('product_tax_category'))*float(request.POST.get('product_price'))
				tax_amount=float(tax_amount)/100
				wholesale_tax_amount=float(request.POST.get('product_tax_category'))*float(request.POST.get('product_wholesale_price'))
				wholesale_tax_amount=float(wholesale_tax_amount)/100
				dif_price_cost=float(request.POST.get('product_price'))-float(request.POST.get('product_cost'))
				price_tax_amount=float(request.POST.get('product_tax_category'))*dif_price_cost
				price_tax_am=float(price_tax_amount)/100
				price_taxes=round(price_tax_am,2)
				cre_product=products(
					product_name=request.POST['product'],
					product_code=request.POST.get('product_code_pnr'),
					product_integer_code=request.POST['product_code'],
					product_hsn=request.POST['product_hsn'],
					product_stock=request.POST.get('product_stock'),
					product_low_stock_limit=request.POST.get('product_low_stocklimit'),
					product_cost=request.POST.get('product_cost'),
					product_price=prod_price,
					product_wholesale_price=wholesale_prod_price,
					product_tax_satus=tax_stat,
					product_tax_category=request.POST['product_tax_category'],
					product_discount=request.POST.get('product_discount'),
					product_alternate_cost=0,
					product_alternate_price=0,
					category_ref=request.POST['category'],
					brand_ref=request.POST['brand'],
					unit_type_ref=categorisation.objects.values_list('product_unit_type', flat=True).get(pk=request.POST['unit']),
					alternate_unit_ref=0,
					product_tax_amount=tax_amount,
					wholesale_product_tax_amount=wholesale_tax_amount,
					price_tax=price_taxes,
					final_price=final_pro_price,
					final_wholesale_price=wholesale_final_pro_price,
					taxable_price=taxable_amount,
					wholesale_taxable_price=wholesale_taxable_amount,
					wholesaleprice_without_tax=request.POST.get('product_wholesale_price')
					)
				cre_product.save()
				cre_sub_product=sub_products(
					product_name=request.POST['product'],
					product_code=request.POST.get('product_code_pnr'),
					product_integer_code=request.POST['product_code'],
					product_hsn=request.POST['product_hsn'],
					product_stock=request.POST.get('product_stock'),
					product_low_stock_limit=request.POST.get('product_low_stocklimit'),
					product_cost=request.POST.get('product_cost'),
					product_price=prod_price,
					product_wholesale_price=request.POST.get('product_wholesale_price'),
					product_tax_satus=tax_stat,
					product_tax_category=request.POST['product_tax_category'],
					product_discount=request.POST.get('product_discount'),
					product_alternate_cost=0,
					product_alternate_price=0,
					category_ref=request.POST['category'],
					brand_ref=request.POST['brand'],
					unit_type_ref=categorisation.objects.values_list('product_unit_type', flat=True).get(pk=request.POST['unit']),
					alternate_unit_ref=0,
					product_tax_amount=tax_amount,
					price_tax=price_taxes,
					final_price=final_pro_price,
					final_wholesale_price=wholesale_final_pro_price,
					taxable_price=taxable_amount,
					wholesale_taxable_price=wholesale_taxable_amount,
					wholesaleprice_without_tax=request.POST.get('product_wholesale_price')
					)
				cre_sub_product.save()

				cre_notification=notification(
					product_name=request.POST['product'],
					product_stock=request.POST.get('product_stock'),
					product_low_stock_limit=request.POST.get('product_low_stocklimit')
					)
				cre_notification.save()

				lates_id=products.objects.values_list('id', flat=True).latest('pk')

				cre_alter=alternate_cost_price(
					product_ref_id=lates_id,
					unit_type_id=request.POST['alter_units'],
					product_price=final_pro_price,
					product_cost=request.POST.get('product_cost'),
					taxable_price=taxable_amount,
					price_without_tax=request.POST.get('product_price')
					)
				cre_alter.save()
				# if request.POST['alter_units0'] != "0":
				alter_count=request.POST['counting']

				for cc in range(1,int(alter_count)+1):

					if tax_inc=="True":
						alter_final_pro_price=request.POST['product_alter_price%d'%cc]
						alter_taxable_amount=(float(request.POST['product_alter_price%d'%cc])*100)/(100+float(request.POST.get('product_tax_category')))
					else:
						alter_taxable_amount=float(request.POST['product_alter_price%d'%cc])
						alter_final_pro_price=float(request.POST['product_alter_price%d'%cc])+tax_amount
					if request.POST['alter_units%d'%cc]=="0":
						continue
					cre_alter=alternate_cost_price(
						product_ref_id=lates_id,
						unit_type_id=request.POST['alter_units%d'%cc],
						product_price=alter_final_pro_price,
						product_cost=request.POST['product_alter_cost%d'%cc],
						taxable_price=alter_taxable_amount,
						price_without_tax=request.POST['product_alter_price%d'%cc]
						)
					cre_alter.save()
		
				
				
			else:
				return HttpResponse(form.errors)
			return HttpResponseRedirect("/create_products")
	percent=[]
	for x in range(100):
		percent.append(x)
	form = create_product()
	active_sidebar1=1
	return render(request,'product/create_update_product.html',{'active_sidebar1':active_sidebar1,'form':form,'prodx':prodx,'units':units,'percent':percent,'repeat_category':repeat_category,'repeat_brand':repeat_brand})
	
########################################################################################################################## 


# @login_required(login_url='/login')
# def create_update_products(request):

# 	prodx=products.objects.all()
# 	units=categorisation.objects.all()
	
# 	if request.method == 'POST':
# 		form=create_product(request.POST)

# 		if form.is_valid():
# 			tax_inc=form.cleaned_data['product_tax_included']
# 			tax_amount=float(request.POST['product_tax_category'])*float(form.cleaned_data['product_price'])
# 			tax_amount=float(tax_amount)/100

# 			if tax_inc=="True":
# 				tax_stat="in"
# 				final_pro_price=form.cleaned_data['product_price']
# 			else:
# 				tax_stat="ex"
# 				final_pro_price=float(form.cleaned_data['product_price'])+tax_amount

			
# 			return HttpResponse(categorisation.objects.values_list('product_unit_type', flat=True).get(pk=request.POST['unit']))
# 			cre_product=products(
# 				product_name=form.cleaned_data['product_name'],
# 				product_code=request.POST.get('product_code_pnr'),
# 				product_integer_code=request.POST['product_code'],
# 				product_hsn=form.cleaned_data['product_hsn'],
# 				product_stock=form.cleaned_data['product_stock'],
# 				product_low_stock_limit=form.cleaned_data['product_low_stocklimit'],
# 				product_cost=form.cleaned_data['product_cost'],
# 				product_price=form.cleaned_data['product_price'],
# 				product_wholesale_price=form.cleaned_data['product_wholesale_price'],
# 				product_tax_satus=tax_stat,
# 				product_tax_category=request.POST['product_tax_category'],
# 				product_discount=form.cleaned_data['product_discount'],
# 				product_alternate_cost=form.cleaned_data['product_alter_cost'],
# 				product_alternate_price=form.cleaned_data['product_alter_price'],
# 				category_ref=request.POST['category'],
# 				brand_ref=request.POST['brand'],
# 				unit_type_ref=categorisation.objects.values_list('product_unit_type', flat=True).get(pk=request.POST['unit']),
# 				alternate_unit_ref=request.POST['alter_units'],
# 				product_tax_amount=tax_amount,
# 				final_price=final_pro_price
# 				)
# 			cre_product.save() 

# 			cre_sub_product=sub_products(
# 					product_name=request.POST['product'],
# 					product_code=request.POST.get('product_code_pnr'),
# 					product_integer_code=request.POST['product_code'],
# 					product_hsn=request.POST['product_hsn'],
# 					product_stock=form.cleaned_data['product_stock'],
# 					product_low_stock_limit=form.cleaned_data['product_low_stocklimit'],
# 					product_cost=form.cleaned_data['product_cost'],
# 					product_price=form.cleaned_data['product_price'],
# 					product_wholesale_price=form.cleaned_data['product_wholesale_price'],
# 					product_tax_satus=tax_stat,
# 					product_tax_category=request.POST['product_tax_category'],
# 					product_discount=form.cleaned_data['product_discount'],
# 					product_alternate_cost=request.POST['product_alter_cost'],
# 					product_alternate_price=request.POST['product_alter_price'],
# 					category_ref=request.POST['category'],
# 					brand_ref=request.POST['brand'],
# 					unit_type_ref=categorisation.objects.values_list('product_unit_type', flat=True).get(pk=request.POST['unit']),
# 					alternate_unit_ref=request.POST['alter_units'],
# 					product_tax_amount=tax_amount,
# 					price_tax=price_taxes,
# 					final_price=final_pro_price
# 					)
# 			cre_sub_product.save()

# 			cre_notification=notification(
# 					product_name=request.POST['product'],
# 					product_stock=form.cleaned_data['product_stock'],
# 					product_low_stock_limit=form.cleaned_data['product_low_stocklimit']
# 					)
# 			cre_notification.save()
			 
# 		else:
# 			return HttpResponse(form.errors)
# 		return HttpResponseRedirect("/create_products")
# 	percent=[]
# 	for x in range(100):
# 		percent.append(x)
# 	form = create_product()
# 	active_sidebar1=1
# 	return render(request,'product/create_update_product.html',{'active_sidebar1':active_sidebar1,'form':form,'prodx':prodx,'units':units,'percent':percent})
@login_required(login_url='/login')
def create_product_ajax(request):
	
	tag_str='<option value="0">..........</option>'
	tag_str2=''
	if request.method == 'POST' and request.POST['action'] == 'selection2':
		alter_unit=[]
		get_id=request.POST.get('selection')
		alter_count=request.POST.get('sele_alter')
		excl_unit=request.POST.get('excl_unit')
		get_pro_unit=alternate_units.objects.all()

		for x in get_pro_unit:

			tag_str=tag_str+'<option value="{}">{}</option>'.format(x.product_alternate_code,x.product_alternate_unit)
			tag_str2=tag_str2+'<option value="{}">{}</option>'.format(x.product_alternate_code,x.product_alternate_unit)
		jsona = json.dumps({'alter_unit':tag_str,'alter_unitd':tag_str2})

		return HttpResponse(jsona, content_type='application/json')


	if request.method == 'POST' and request.POST['action'] == 'selection3':
		alter_unit=[]
		get_id=request.POST.get('selection')
		alter_count=request.POST.get('sele_alter')
		alter_count=alter_count+request.POST.get('unit_alter')
		
		if alter_count is not None:
			alter_counting=[alter_count[i:i+2] for i in range(0, len(alter_count), 2)]
			get_pro_unit=alternate_units.objects.all().filter(unit_ref_id=get_id).exclude(product_alternate_code__in=alter_counting).order_by('pk')

			for x in get_pro_unit:

				tag_str=tag_str+'<option value="{}">{}</option>'.format(x.product_alternate_code,x.product_alternate_unit)
				tag_str2=tag_str2+'<option value="{}">{}</option>'.format(x.product_alternate_code,x.product_alternate_unit)
		jsona = json.dumps({'alter_unit':tag_str,'alter_unitd':tag_str2})

		return HttpResponse(jsona, content_type='application/json')


def generate_code_ajax(request):
	nubers=[]
	pro_cod=[]
	final=[]
	
	if request.method == 'POST':
		

		cust_invoice=products.objects.values_list('product_integer_code', flat=True)
		if not cust_invoice:
			cust_invoice=[0]
		cust_invo_sum=max(cust_invoice)+1
		store_info=store_details.objects.latest('id')
		ran=str(store_info.store_code)+str(cust_invo_sum)

		jsona = json.dumps({'ran':ran,'int_ran':cust_invo_sum})

	return HttpResponse(jsona, content_type='application/json')

################################# view product ###########################################################################
@login_required(login_url='/login')
def update_product_ajax(request):
	c=0
	tag_str=''
	
	if request.method == 'POST' and request.POST['action'] == 'selected':
		
		get_id=request.POST.get('selection')
		prod_name=products.objects.values_list('product_name', flat=True).get(pk=get_id)
		prod_code=products.objects.values_list('product_code', flat=True).get(pk=get_id)
		prod_hsn=products.objects.values_list('product_hsn', flat=True).get(pk=get_id)
		prod_categor=products.objects.values_list('category_ref', flat=True).get(pk=get_id)
		prod_brand=products.objects.values_list('brand_ref', flat=True).get(pk=get_id)
		prod_unit=categorisation.objects.values_list('id', flat=True).get(product_unit_type=products.objects.values_list('unit_type_ref', flat=True).get(pk=get_id))
		prod_stock=products.objects.values_list('product_stock', flat=True).get(pk=get_id)
		prod_stock_limit=products.objects.values_list('product_low_stock_limit', flat=True).get(pk=get_id)
		# prod_cost=products.objects.values_list('product_cost', flat=True).get(pk=get_id)
		alt_units=alternate_units.objects.all().filter(unit_ref_id=prod_unit).order_by('unit_ref_id')
		prod_alternate_cost_price=alternate_cost_price.objects.all().filter(product_ref_id=get_id).order_by('unit_type_id')
		for prcc in prod_alternate_cost_price:
			

			if prcc==prod_alternate_cost_price[0]:
				prod_cost=prcc.product_cost
				prod_mrp=prcc.price_without_tax
				prod_unit_id=prcc.unit_type_id
			else:
				c=c+1
				prod_alt_cost=prcc.product_cost
				prod_alt_price=prcc.product_price

				unit_ref=alternate_units.objects.values_list('unit_ref_id', flat=True).get(product_alternate_code=prcc.unit_type_id)
				get_pro_unit=alternate_units.objects.all().filter(unit_ref_id=unit_ref)
				tag_alter_str=''
				for x in get_pro_unit:
					if int(prcc.unit_type_id) == int(x.product_alternate_code):
						tag_alter_str=tag_alter_str+'<option value="{}" selected>{}</option>'.format(x.product_alternate_code,x.product_alternate_unit)
					else:	
						tag_alter_str=tag_alter_str+'<option value="{}">{}</option>'.format(x.product_alternate_code,x.product_alternate_unit)

				

				tag_str=tag_str+'<div class="col-md-4 col-12"><div class="form-group"><label>UNIT</label>\
				<select required class="form-control alternate_units" width="300" id="alter_unit_id{}" name="alter_units{}">\
				<option value="0">..........</option>{}</select></div><!-- /.form-group --></div>\
				<!-- /.col --><div class="col-md-4 col-12"><div class="form-group"><label>Cost</label>\
				<input type="number" class="form-control" name="product_alter_cost{}" value="{}">\
				</select></div><!-- /.form-group --></div><!-- /.col --><div class="col-md-4 col-12">\
				<div class="form-group"><label>Price</label><input type="number" class="form-control" name="product_alter_price{}" value="{}">\
				</div><!-- /.form-group --><input type="hidden" value="{}" id="counts" style="width: 0%;" name="counting"></div>'.format(c,c,tag_alter_str,c,prod_alt_cost,c,c,prod_alt_price)


		prod_final_price=products.objects.values_list('final_price', flat=True).get(pk=get_id)
		prod_wholesale=products.objects.values_list('wholesaleprice_without_tax', flat=True).get(pk=get_id)
		prod_tax=products.objects.values_list('product_tax_category', flat=True).get(pk=get_id)
		prod_disc=products.objects.values_list('product_discount', flat=True).get(pk=get_id)
		
		jsona = json.dumps({'pro_id':get_id,'prod_name':prod_name,'prod_code':prod_code,'prod_hsn':prod_hsn,'prod_categor':prod_categor,'prod_brand':prod_brand,
			'prod_unit':prod_unit,'prod_stock':prod_stock,'prod_stock_limit':prod_stock_limit,'prod_cost':prod_cost,'prod_mrp':prod_mrp,'prod_unit_id':prod_unit_id,
			'prod_wholesale':prod_wholesale,'prod_tax':prod_tax,'prod_disc':prod_disc,'tag_str':tag_str})

	return HttpResponse(jsona, content_type='application/json')

################################# edit product ###########################################################################
@login_required(login_url='/login')
def edit_products(request,id):
	
	prodx=products.objects.all().filter(pk=id)
	form = create_product()
	return render(request,'product/edit_products.html',{'prodx':prodx,'form':form})
	
##########################################################################################################################

################################# update product ###########################################################################
@login_required(login_url='/login')
def update_products(request):
	# return HttpResponse(request.POST['prod_id'])
	
	if request.method == 'POST':
		
		
		tax_inc=request.POST.get('taxes_stat2')
		
		if tax_inc=="True":
			tax_stat="in"
			tax_amount=float(request.POST.get('product_tax_category2'))*float(request.POST.get('product_price2'))
			tax_amount=float(tax_amount)/100
			prod_price=float(request.POST.get('product_price2'))-tax_amount
			final_pro_price=request.POST.get('product_price2')
			taxable_amount=(float(request.POST.get('product_price2'))*100)/(100+float(request.POST.get('product_tax_category2')))

		else:
			tax_stat="ex"
			tax_amount=float(request.POST.get('product_tax_category2'))*float(request.POST.get('product_price2'))
			tax_amount=float(tax_amount)/100
			prod_price=float(request.POST.get('product_price2'))+tax_amount
			final_pro_price=float(request.POST.get('product_price2'))+tax_amount
			taxable_amount=float(request.POST.get('product_price2'))



		pro_update=products.objects.get(pk=request.POST['prod_id2'])
		pro_update.product_name=request.POST['product2']
		# pro_update.product_code=request.POST['product_code']
		pro_update.product_hsn=request.POST['product_hsn2']
		# pro_update.product_stock=request.POST['product_stock']
		# pro_update.product_low_stock_limit=request.POST['product_low_stocklimit']
		pro_update.product_cost=request.POST['product_cost2']
		pro_update.product_price=request.POST['product_price2']
		pro_update.final_price=request.POST['product_price2']
		pro_update.product_wholesale_price=request.POST['product_wholesale_price2']
		pro_update.product_tax_satus=tax_stat
		pro_update.product_tax_category=request.POST['product_tax_category2']
		pro_update.product_discount=request.POST['product_discount2']
		pro_update.product_alternate_cost=request.POST['product_cost2']
		pro_update.product_alternate_price=request.POST['product_price2']
		pro_update.category_ref=request.POST['category2']
		pro_update.brand_ref=request.POST['brand2']
		pro_update.alternate_unit_ref=request.POST['alter_units2']
		pro_update.save()

		

		pro_update2=alternate_cost_price.objects.get(product_ref_id=request.POST['prod_id2'])
		pro_update2.unit_type_id=request.POST['alter_units2']
		pro_update2.product_price=final_pro_price
		pro_update2.product_cost=request.POST.get('product_cost2')
		pro_update2.taxable_price=taxable_amount
		pro_update2.price_without_tax=request.POST.get('product_price2')
		pro_update2.save()
		
	else:
		return HttpResponse(form.errors)
	
	
	return HttpResponseRedirect('/create_products')
	

@login_required(login_url='/login')
def update_stock(request):
	
	if request.method == 'POST':
		old_stock=products.objects.values_list('product_stock', flat=True).get(pk=request.POST['st_prod_id'])

		pro_stock_update=products.objects.get(pk=request.POST['st_prod_id'])
		pro_stock_update.product_stock=int(old_stock)+int(request.POST['st_new_stock'])
		pro_stock_update.product_low_stock_limit=request.POST['st_new_stock_limit']
		pro_stock_update.save()

	return HttpResponseRedirect('/create_products')
	
##########################################################################################################################
@login_required(login_url='/login')
def del_products(request,id):
	
	del_pro=products.objects.get(pk=id)
	del_pro.delete()
	
	return HttpResponseRedirect('/product_details/')
	
def delete_all_product(request):
	pro_list=request.POST.get('checked_pro')
	if pro_list=="0":
		return HttpResponseRedirect('/product_details/')
	else:
		pro_pro_list = pro_list.split (",")
		
		# convert each element as integers
		pro_lists = []
		for i in pro_pro_list:
			pro_lists.append(int(i))

		for x in pro_lists:
			
			del_pro=products.objects.get(pk=x)
			del_pro.delete()
		return HttpResponseRedirect('/product_details/')
	

###################################################################################################################

@login_required(login_url='/login')
def product_upload(request):
	
	excel_path=''
	if request.method == 'POST':
		form=uploading_products(request.POST,request.FILES)
		if form.is_valid():
			excel_files=form.cleaned_data["excel_file"]
			
			import os
			import tempfile
			fd, path = tempfile.mkstemp()
			with os.fdopen(fd, 'wb') as tmp:
				tmp.write(excel_files.read())
		
		workbook=xlrd.open_workbook(path)
		sheet=workbook.sheet_by_index(0)
			
		for x in range(1,int(sheet.nrows)):
			obj=products(
				product_code = sheet.cell_value(x,0),
				category_ref = sheet.cell_value(x,1),
				sub_category = sheet.cell_value(x,2),
				brand_ref = sheet.cell_value(x,3),
				product_name = sheet.cell_value(x,4),
				product_stock = sheet.cell_value(x,5),
				unit_type_ref = sheet.cell_value(x,6),
				product_cost = sheet.cell_value(x,7),
				product_price = sheet.cell_value(x,8),
				product_tax_amount = sheet.cell_value(x,9),
				
				product_low_stock_limit = sheet.cell_value(x,10),
				product_tax_satus = sheet.cell_value(x,11),
				product_discount = sheet.cell_value(x,12),
				product_hsn=sheet.cell_value(x,13)
				)
			obj.save()
	form=uploading_products()
	active_sidebar3=1
	return render(request,'product/product_upload.html',{'active_sidebar3':active_sidebar3,'form':form})
	









