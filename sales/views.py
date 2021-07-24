from django.shortcuts import render
from sales.forms import create_sale
from product.models import products,alternate_units,categorisation,sub_products,alternate_cost_price
from sales.models import create_sales_table,create_sales_final,sale_totals,taxes,create_wholesale_sales_table,create_wholesale_sales_final,sale_wholesale_totals,wholesale_taxes,reports
from dashboard.models import notification
from settings_billing.models import store_details
from itertools import*
import json       
from django.http import HttpResponse,HttpResponseRedirect 
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required 
from returns.models import sales_returned

# Create your views here.
@login_required(login_url='/login')
def dashboard_sales(request):
 
	active_sidebar1=2
	return render(request,'sales/dashboard_sales.html',{'active_sidebar1':active_sidebar1})

@login_required(login_url='/login')
def sales_details(request):
	sale_detail=create_sales_final.objects.all().order_by('-sale_invoice_ref')
	active_sidebar4=1
	activebar=1
	return render(request,'sales/sales_details.html',{'active_sidebar4':active_sidebar4,'activebar':activebar,'sale_detail':sale_detail})

@login_required(login_url='/login')
def sales_details_wholesale(request):
	sale_detail=create_wholesale_sales_final.objects.all().order_by('-sale_invoice_ref')
	active_sidebar4=1
	activebar=2
	return render(request,'sales/sales_details_wholesale.html',{'active_sidebar4':active_sidebar4,'activebar':activebar,'sale_detail':sale_detail})
 

@login_required(login_url='/login')
def stock_movement(request):
	active_sidebar4=2
	return render(request,'sales/stock_movement.html',{'active_sidebar4':active_sidebar4})


@login_required(login_url='/login')
def creating_sales(request):

	prodx=products.objects.all()
	unit_types=alternate_units.objects.all()
	cust_invoice=create_sales_table.objects.values_list('sales_invoice_no', flat=True)
	if cust_invoice==None:
		cust_invoice=0
	cust_invo_sum=max(cust_invoice)+1
	form = create_sale()
	active_sidebar2=2
	return render(request,'sales/create_sales.html',{'active_sidebar2':active_sidebar2,'form':form,'prodx':prodx,
		'unit_types':unit_types})

@login_required(login_url='/login')
def create_sales(request): 
	taxess=0

	prodx=products.objects.all()
	unit_types=alternate_units.objects.all()
	

	


	new_count=[]
	sl_no=[]
	bill_pro_name=[]
	bill_pro_hsn=[]
	bill_pro_qty=[]
	bill_pro_unit=[]
	bill_pro_price=[]
	bill_pro_disc=[]
	bill_pro_tax=[]
	bill_pro_cgst=[]
	bill_pro_sgst=[]
	bill_pro_igst=[]
	cess=[]
	bill_pro_total=[]
	bill_pro_taxable_amount=[]

	if request.method == 'POST':
		cust_invoice=create_sales_table.objects.values_list('sales_invoice_no', flat=True)
		if not cust_invoice:
			cust_invoice=[0]
		cust_invo_sum=max(cust_invoice)+1

		form=create_sale(request.POST)
		if request.POST.get("sale_type") == '1':
			counti=request.POST.getlist('counting')
			sp_disc=request.POST.get('sale_special_discount')
			for ccc in counti:

				new_count.append(int(ccc))
			counts=max(new_count)
			counts_int=int(counts)
			counts_int_sum=counts_int+1

			

			edits=[]
			for x in range(1,counts_int_sum):
				
				y=request.POST.get('selected_product%d'%x)
				if y is not None:
					edits.append(x)
			
			
			for x in edits:

				product_stock_info=products.objects.values_list('product_stock', flat=True).get(product_code=request.POST.get('selected_product%d'%x))
				product_stock_amount=request.POST.get('qty%d'%x)
				pro_stock=float(product_stock_info)-float(product_stock_amount)

				
				update_stock = products.objects.filter(product_code=request.POST.get('selected_product%d'%x)).update(product_stock=pro_stock)
				pro_id=products.objects.values_list('id', flat=True).get(product_code=request.POST.get('selected_product%d'%x))
				notify_update = notification.objects.filter(pk=pro_id).first()
				
				if notify_update == None:
					cre_notification=notification(
					id=products.objects.values_list('id', flat=True).get(pk=pro_id),
					product_name=products.objects.values_list('product_name', flat=True).get(pk=pro_id),
					product_stock=pro_stock,
					product_low_stock_limit=products.objects.values_list('product_low_stock_limit', flat=True).get(pk=pro_id),
					)
					cre_notification.save()
				notify_update_product_stock=notification.objects.filter(pk=pro_id).update(product_stock=pro_stock)
				cre_sales_table=create_sales_table(
				sales_product_ref_id=products.objects.values_list('id', flat=True).get(product_code=request.POST.get('selected_product%d'%x)),
				sales_qty=request.POST.get('qty%d'%x),
				sales_invoice_no=cust_invo_sum
				)
				cre_sales_table.save()
				store_ib=store_details.objects.latest('id')
				if request.POST.get('selected_unit%d'%x)=="0":
					bill_pro_pricess=float(products.objects.values_list('final_price', flat=True).get(product_code=request.POST.get('selected_product%d'%x)))-float(products.objects.values_list('product_discount', flat=True).get(product_code=request.POST.get('selected_product%d'%x)))
				else:
					get_pr_id=products.objects.values_list('id', flat=True).get(product_code=request.POST.get('selected_product%d'%x))
					bill_pro_pricess=float(alternate_cost_price.objects.values_list('product_price', flat=True).get(product_ref_id=get_pr_id,unit_type_id=request.POST.get('selected_unit%d'%x)))-float(products.objects.values_list('product_discount', flat=True).get(product_code=request.POST.get('selected_product%d'%x)))
				if products.objects.values_list('final_price', flat=True).get(product_code=request.POST.get('selected_product%d'%x)) == "ex":
					gst=float(request.POST.get('tax_amount%d'%x))
					bill_pro_taxable_amo=(float(request.POST.get('sub_total%d'%x))-gst)-float(products.objects.values_list('product_discount', flat=True).get(product_code=request.POST.get('selected_product%d'%x)))
					if store_ib.cess_status=="YES":
						cess_value=(bill_pro_taxable_amo/100)
					else:
						cess_value=0
					total_bill=(float(request.POST.get('sub_total%d'%x))*float(request.POST.get('qty%d'%x)))+cess_value
				else:
					if request.POST.get('selected_unit%d'%x)=="0":
						bill_pro_taxable_amo=((float(products.objects.values_list('final_price', flat=True).get(product_code=request.POST.get('selected_product%d'%x)))*100)/(100+float(products.objects.values_list('product_tax_category', flat=True).get(product_code=request.POST.get('selected_product%d'%x)))))*float(request.POST.get('qty%d'%x))
					else:
						get_pr_id=products.objects.values_list('id', flat=True).get(product_code=request.POST.get('selected_product%d'%x))
						bill_pro_taxable_amo=((float(alternate_cost_price.objects.values_list('product_price', flat=True).get(product_ref_id=get_pr_id,unit_type_id=request.POST.get('selected_unit%d'%x)))*100)/(100+float(products.objects.values_list('product_tax_category', flat=True).get(product_code=request.POST.get('selected_product%d'%x)))))*float(request.POST.get('qty%d'%x))
					bill_pro_taxable_amo=bill_pro_taxable_amo-float(products.objects.values_list('product_discount', flat=True).get(product_code=request.POST.get('selected_product%d'%x)))
					gst=(bill_pro_pricess*float(request.POST.get('qty%d'%x)))-bill_pro_taxable_amo
					if store_ib.cess_status=="YES":
						cess_value=(bill_pro_taxable_amo/100)
					else:
						cess_value=0
					total_bill=(bill_pro_pricess*float(request.POST.get('qty%d'%x)))+cess_value
				if store_ib.cess_status=="YES":
					bill_pro_name.append(products.objects.values_list('product_name', flat=True).get(product_code=request.POST.get('selected_product%d'%x)))
					bill_pro_hsn.append(products.objects.values_list('product_hsn', flat=True).get(product_code=request.POST.get('selected_product%d'%x)))
					bill_pro_qty.append(float(request.POST.get('qty%d'%x)))
					bill_pro_unit.append(request.POST.get('selected_post_unit%d'%x).split('(', 1)[1].split(')')[0])
					bill_pro_price.append(bill_pro_pricess)
					bill_pro_disc.append(float(request.POST.get('discount%d'%x)))
					bill_pro_tax.append(products.objects.values_list('product_tax_category', flat=True).get(product_code=request.POST.get('selected_product%d'%x)))
					bill_pro_cgst.append(gst/2)
					bill_pro_sgst.append(gst/2)
					cess.append(bill_pro_taxable_amo/100)



					save_report=reports(
					prod_name=products.objects.values_list('product_name', flat=True).get(product_code=request.POST.get('selected_product%d'%x)),
					qty=request.POST.get('qty%d'%x),
					unit=request.POST.get('selected_post_unit%d'%x).split('(', 1)[1].split(')')[0],
					price=bill_pro_pricess,
					discount=float(request.POST.get('discount%d'%x)),
					taxable_amount=bill_pro_taxable_amo,
					tax_percent=products.objects.values_list('product_tax_category', flat=True).get(product_code=request.POST.get('selected_product%d'%x)),
					cgst=gst/2,
					sgst=gst/2,
					invoice_no=cust_invo_sum
					)
					save_report.save()



					#cess_value=(bill_pro_taxable_amo/100)
					
					#bill_pro_taxable_amount.append(float(products.objects.values_list('product_price', flat=True).get(product_code=request.POST.get('selected_product%d'%x)))-float(products.objects.values_list('product_cost', flat=True).get(product_code=request.POST.get('selected_product%d'%x))))
					bill_pro_total.append(total_bill)
					billing_total=float(request.POST.get('sale_total'))
					bill_pro_taxable_amount.append(bill_pro_taxable_amo)

					import pandas as pd
					df=pd.DataFrame(list(zip(bill_pro_name,bill_pro_hsn,bill_pro_qty,bill_pro_unit,bill_pro_price,bill_pro_tax,bill_pro_disc,bill_pro_taxable_amount,bill_pro_cgst,bill_pro_sgst,cess,bill_pro_total)),columns=['b','c','d','e','f','g','h','i','j','k','l','m'])
					
					aab=df.groupby(['b','e']).agg({'c': 'first','d': 'sum','f': 'sum','g': 'sum','h': 'sum','i': 'first','j': 'sum','k': 'sum','l': 'sum','m': 'sum'}).reset_index().round(3)
					sl=[i for i in range(1,len(aab.index)+1)]
					se = pd.Series(sl)
					aab['n'] = se.values
					cols = ['b','c','d','e','f','g','h','i','j','k','l','m','n']
					lst = []
					
					    
					loop_value=0
					if counts_int<=12:
						loop_value=12-counts_int
					for ddd in range(1,loop_value):
							lst.append(['-', '-', '-','-', '-', '-','-', '-', '-','-', '-', '-','-'])
					df1 = pd.DataFrame(lst, columns=cols)
					aa=aab.append(df1)

					listss=aa.values.tolist()
				else:
					bill_pro_name.append(products.objects.values_list('product_name', flat=True).get(product_code=request.POST.get('selected_product%d'%x)))
					bill_pro_hsn.append(products.objects.values_list('product_hsn', flat=True).get(product_code=request.POST.get('selected_product%d'%x)))
					bill_pro_qty.append(float(request.POST.get('qty%d'%x)))
					bill_pro_unit.append(request.POST.get('selected_post_unit%d'%x).split('(', 1)[1].split(')')[0])
					bill_pro_price.append(bill_pro_pricess)
					bill_pro_disc.append(float(request.POST.get('discount%d'%x)))
					bill_pro_tax.append(products.objects.values_list('product_tax_category', flat=True).get(product_code=request.POST.get('selected_product%d'%x)))
					bill_pro_cgst.append(float(request.POST.get('tax_amount%d'%x))/2)
					bill_pro_sgst.append(float(request.POST.get('tax_amount%d'%x))/2)
					#bill_pro_taxable_amount.append(float(products.objects.values_list('product_price', flat=True).get(product_code=request.POST.get('selected_product%d'%x)))-float(products.objects.values_list('product_cost', flat=True).get(product_code=request.POST.get('selected_product%d'%x))))
					#bill_pro_total.append(float(request.POST.get('sub_total%d'%x)))


					save_report=reports(
					prod_name=products.objects.values_list('product_name', flat=True).get(product_code=request.POST.get('selected_product%d'%x)),
					qty=request.POST.get('qty%d'%x),
					unit=request.POST.get('selected_post_unit%d'%x).split('(', 1)[1].split(')')[0],
					price=bill_pro_pricess,
					discount=float(request.POST.get('discount%d'%x)),
					taxable_amount=bill_pro_taxable_amo,
					tax_percent=products.objects.values_list('product_tax_category', flat=True).get(product_code=request.POST.get('selected_product%d'%x)),
					cgst=float(request.POST.get('tax_amount%d'%x))/2,
					sgst=float(request.POST.get('tax_amount%d'%x))/2,
					invoice_no=cust_invo_sum
					)
					save_report.save()


					bill_pro_total.append(total_bill)
					billing_total=float(request.POST.get('sale_total'))
					bill_pro_taxable_amount.append(float(request.POST.get('sub_total%d'%x))-float(request.POST.get('tax_amount%d'%x)))
					import pandas as pd
					df=pd.DataFrame(list(zip(bill_pro_name,bill_pro_hsn,bill_pro_qty,bill_pro_unit,bill_pro_price,bill_pro_tax,bill_pro_disc,bill_pro_taxable_amount,bill_pro_cgst,bill_pro_sgst,bill_pro_total)),columns=['b','c','d','e','f','g','h','i','j','k','l'])
					
					aab=df.groupby(['b','e']).agg({'c': 'first','d': 'sum','f': 'sum','g': 'sum','h': 'sum','i': 'first','j': 'sum','k': 'sum','l': 'sum'}).reset_index().round(3)
					sl=[i for i in range(1,len(aab.index)+1)]
					se = pd.Series(sl)
					aab['m'] = se.values
					cols = ['b','c','d','e','f','g','h','i','j','k','l','m']
					lst = []
					
					    
					loop_value=0
					if counts_int<=12:
						loop_value=12-counts_int
					for ddd in range(1,loop_value):
							lst.append(['-', '-', '-','-', '-', '-','-', '-', '-','-', '-', '-'])
					df1 = pd.DataFrame(lst, columns=cols)
					aa=aab.append(df1)
					listss=aa.values.tolist()



				import datetime
				now = datetime.datetime.now()


				pro_taxes=products.objects.values_list('product_tax_category', flat=True).get(product_code=request.POST.get('selected_product%d'%x))
				price_taxes=products.objects.values_list('price_tax', flat=True).get(product_code=request.POST.get('selected_product%d'%x))

				tax_date=taxes.objects.filter(sale_date__year=now.year, sale_date__month=now.month,sale_date__day=now.day,tax_percent=pro_taxes)
				pri_tax=float(price_taxes)*float(request.POST.get('qty%d'%x))

				if not tax_date:
					cre_tax_table=taxes(
					tax_percent=pro_taxes,
					sale_date=now,
					total_tax_amount=request.POST.get('tax_amount%d'%x),
					price_tax_amount=round(pri_tax,2)
					) 
					cre_tax_table.save()
				else:


					taxu=taxes.objects.values_list('total_tax_amount', flat=True).get(sale_date__year=now.year, sale_date__month=now.month,sale_date__day=now.day,tax_percent=pro_taxes)
					taxess=float(taxu)+float(request.POST.get('tax_amount%d'%x))
					taxess=round(taxess,2)
					pri_taxu=taxes.objects.values_list('price_tax_amount', flat=True).get(sale_date__year=now.year, sale_date__month=now.month,sale_date__day=now.day,tax_percent=pro_taxes)
					pri_taxess=float(pri_taxu)+round(pri_tax,2)
					update_saletotal = taxes.objects.filter(sale_date__year=now.year, sale_date__month=now.month,sale_date__day=now.day,tax_percent=pro_taxes).update(total_tax_amount=taxess)
					update_pri_tax = taxes.objects.filter(sale_date__year=now.year, sale_date__month=now.month,sale_date__day=now.day,tax_percent=pro_taxes).update(price_tax_amount=pri_taxess)

				
				# sales_final 
			
			if form.is_valid():
				datess=request.POST.get('sale_payment_remainder_date')
				if datess=="":
					datess="1111-11-11"
				
				cre_sales_final_table=create_sales_final(
					sale_type=form.cleaned_data['sale_type'],
					sales_date=form.cleaned_data['sale_date'],
					sales_time=request.POST.get('sale_time'),
					subtotal=billing_total,                               
					sale_invoice_ref=cust_invo_sum,
					sales_special_discount=form.cleaned_data['sale_special_discount'],
					sales_total=billing_total,
					sales_payment_received=form.cleaned_data['sale_payment_received'],
					sales_total_tax_amount=form.cleaned_data['sale_total_tax_amount'],
					sales_total_discount_amount=form.cleaned_data['sale_total_discount_amount'],
					sales_round_off=form.cleaned_data['sale_round_off'],
					sales_transaction_mode=form.cleaned_data['sale_transaction_mode'],
					sales_cash_account=form.cleaned_data['sale_cash_account'],
					sales_payment_remainder_date=datess,
					sales_payment_balance=float(form.cleaned_data['sale_total'])-float(form.cleaned_data['sale_payment_received']),
					sale_return_status=0,
					sales_taxable_amount=round(sum(bill_pro_taxable_amount),3),
					sales_printing=listss
					)
				cre_sales_final_table.save()
				# bill_final_total=form.cleaned_data['sale_total']
				# final_cess=float(bill_final_total)/100
				# bill_final_total=str(round(float(bill_final_total)+final_cess,2))

				bill_final_tax=round(float(form.cleaned_data['sale_total_tax_amount']))
				# bill_final_tax=str(round(sum(bill_final_tax),2))

				bill_final_disc=round(float(form.cleaned_data['sale_total_discount_amount']))
				

				bill_final_date=form.cleaned_data['sale_date']
				
				bill_final_word_total="hhh"

				import datetime
				now = datetime.datetime.now()
				sales=create_sales_final.objects.filter(sales_date__year=now.year, sales_date__month=now.month,sales_date__day=now.day)
				sales_totaling=[]
				for y in sales:
					sales_totaling.append(float(y.subtotal))
				final_totals=sum(sales_totaling)
				
				
				sales_date=sale_totals.objects.filter(sales_date__year=now.year, sales_date__month=now.month,sales_date__day=now.day)
				
				
				if not sales_date:
					cre_sales_timings=sale_totals(
						sales_date=form.cleaned_data['sale_date'],
						sales_totals=final_totals
						)
					cre_sales_timings.save()
				update_saletotal = sale_totals.objects.filter(sales_date__year=now.year, sales_date__month=now.month,sales_date__day=now.day).update(sales_totals=final_totals)
			
			else:
				return HttpResponse(form.errors)


			
			
			store_info=store_details.objects.latest('id')
			zippy=zip(bill_pro_name,bill_pro_hsn,bill_pro_qty,bill_pro_unit,bill_pro_price,bill_pro_tax,bill_pro_disc,bill_pro_taxable_amount,bill_pro_cgst,bill_pro_sgst,bill_pro_total)
			if store_ib.cess_status=="YES":
				return render(request,'sales/sales_bill_retail.html',{'zippy':listss,'bill_final_date':bill_final_date,'bill_final_total':round(sum(bill_pro_total)-int(sp_disc)),'sp_disc':sp_disc,'bill_final_tax':bill_final_tax,'bill_final_disc':bill_final_disc,
				'payment_recieved':form.cleaned_data['sale_payment_received'],'cust_invo_sum':"NO"+str(cust_invo_sum),'bill_final_word_total':bill_final_word_total,'store_info':store_info})
			else:
				return render(request,'sales/sales_bill.html',{'zippy':listss,'bill_final_date':bill_final_date,'bill_final_total':round(sum(bill_pro_total)-int(sp_disc)),'sp_disc':sp_disc,'bill_final_tax':bill_final_tax,'bill_final_disc':bill_final_disc,
				'payment_recieved':form.cleaned_data['sale_payment_received'],'cust_invo_sum':"NO"+str(cust_invo_sum),'bill_final_word_total':bill_final_word_total,'store_info':store_info})

		else:
			cust_invoice=create_wholesale_sales_table.objects.values_list('sales_invoice_no', flat=True)
			if not cust_invoice:
				cust_invoice=[0]
			cust_invo_sum=max(cust_invoice)+1
			counti=request.POST.getlist('counting')
			sp_disc=request.POST.get('sale_special_discount')
			for ccc in counti:

				new_count.append(int(ccc))
			counts=max(new_count)
			counts_int=int(counts)
			counts_int_sum=counts_int+1

			

			edits=[]
			for x in range(1,counts_int_sum):
				
				y=request.POST.get('selected_product%d'%x)
				if y is not None:
					edits.append(x)
			
			
			for x in edits:

				product_stock_info=products.objects.values_list('product_stock', flat=True).get(product_code=request.POST.get('selected_product%d'%x))
				product_stock_amount=request.POST.get('qty%d'%x)
				pro_stock=float(product_stock_info)-float(product_stock_amount)

				
				update_stock = products.objects.filter(product_code=request.POST.get('selected_product%d'%x)).update(product_stock=pro_stock)

				pro_id=products.objects.values_list('id', flat=True).get(product_code=request.POST.get('selected_product%d'%x))
				notify_update = notification.objects.filter(pk=pro_id).first()
				
				if notify_update == None:
					cre_notification=notification(
					id=products.objects.values_list('id', flat=True).get(pk=pro_id),
					product_name=products.objects.values_list('product_name', flat=True).get(pk=pro_id),
					product_stock=pro_stock,
					product_low_stock_limit=products.objects.values_list('product_low_stock_limit', flat=True).get(pk=pro_id),
					)
					cre_notification.save()
				notify_update_product_stock=notification.objects.filter(pk=pro_id).update(product_stock=pro_stock)

				cre_sales_table=create_wholesale_sales_table(
				sales_product_ref_id=products.objects.values_list('id', flat=True).get(product_code=request.POST.get('selected_product%d'%x)),
				sales_qty=request.POST.get('qty%d'%x),
				sales_invoice_no=cust_invo_sum
				)
				cre_sales_table.save()
				if request.POST.get('selected_unit%d'%x)=="0":
					bill_pro_pricess=float(products.objects.values_list('final_wholesale_price', flat=True).get(product_code=request.POST.get('selected_product%d'%x)))-float(products.objects.values_list('product_discount', flat=True).get(product_code=request.POST.get('selected_product%d'%x)))
				else:
					get_pr_id=products.objects.values_list('id', flat=True).get(product_code=request.POST.get('selected_product%d'%x))
					bill_pro_pricess=float(alternate_cost_price.objects.values_list('product_price', flat=True).get(product_ref_id=get_pr_id,unit_type_id=request.POST.get('selected_unit%d'%x)))-float(products.objects.values_list('product_discount', flat=True).get(product_code=request.POST.get('selected_product%d'%x)))
				if products.objects.values_list('final_wholesale_price', flat=True).get(product_code=request.POST.get('selected_product%d'%x)) == "ex":
					
					bill_pro_taxable_amo=float(request.POST.get('sub_total%d'%x))
					
					total_bill=(float(request.POST.get('sub_total%d'%x))*float(request.POST.get('qty%d'%x)))
				else:
					if request.POST.get('selected_unit%d'%x)=="0":
						bill_pro_taxable_amo=((float(products.objects.values_list('final_wholesale_price', flat=True).get(product_code=request.POST.get('selected_product%d'%x)))*100)/(100+float(products.objects.values_list('product_tax_category', flat=True).get(product_code=request.POST.get('selected_product%d'%x)))))*float(request.POST.get('qty%d'%x))
					else:
						get_pr_id=products.objects.values_list('id', flat=True).get(product_code=request.POST.get('selected_product%d'%x))
						bill_pro_taxable_amo=((float(alternate_cost_price.objects.values_list('product_price', flat=True).get(product_ref_id=get_pr_id,unit_type_id=request.POST.get('selected_unit%d'%x)))*100)/(100+float(products.objects.values_list('product_tax_category', flat=True).get(product_code=request.POST.get('selected_product%d'%x)))))*float(request.POST.get('qty%d'%x))
					cess_value=(bill_pro_taxable_amo/100)
					total_bill=(bill_pro_pricess*float(request.POST.get('qty%d'%x)))

				bill_pro_name.append(products.objects.values_list('product_name', flat=True).get(product_code=request.POST.get('selected_product%d'%x)))
				bill_pro_hsn.append(products.objects.values_list('product_hsn', flat=True).get(product_code=request.POST.get('selected_product%d'%x)))
				bill_pro_qty.append(request.POST.get('qty%d'%x))
				bill_pro_unit.append(request.POST.get('selected_post_unit%d'%x).split('(', 1)[1].split(')')[0])
				bill_pro_price.append(bill_pro_pricess)
				bill_pro_disc.append(float(request.POST.get('discount%d'%x)))
				bill_pro_tax.append(products.objects.values_list('product_tax_category', flat=True).get(product_code=request.POST.get('selected_product%d'%x)))
				bill_pro_cgst.append(float(request.POST.get('tax_amount%d'%x))/2)
				bill_pro_sgst.append(float(request.POST.get('tax_amount%d'%x))/2)
				#bill_pro_taxable_amount.append(float(products.objects.values_list('product_price', flat=True).get(product_code=request.POST.get('selected_product%d'%x)))-float(products.objects.values_list('product_cost', flat=True).get(product_code=request.POST.get('selected_product%d'%x))))
				#bill_pro_total.append(float(request.POST.get('sub_total%d'%x)))



				save_report=reports(
				prod_name=products.objects.values_list('product_name', flat=True).get(product_code=request.POST.get('selected_product%d'%x)),
				qty=request.POST.get('qty%d'%x),
				unit=request.POST.get('selected_post_unit%d'%x).split('(', 1)[1].split(')')[0],
				price=bill_pro_pricess,
				discount=float(request.POST.get('discount%d'%x)),
				taxable_amount=bill_pro_taxable_amo,
				tax_percent=products.objects.values_list('product_tax_category', flat=True).get(product_code=request.POST.get('selected_product%d'%x)),
				cgst=float(request.POST.get('tax_amount%d'%x))/2,
				sgst=float(request.POST.get('tax_amount%d'%x))/2,
				invoice_no=cust_invo_sum
				)
				save_report.save()
				

				bill_pro_total.append(total_bill)
				bill_pro_taxable_amount.append(float(request.POST.get('sub_total%d'%x))-float(request.POST.get('tax_amount%d'%x)))
				import pandas as pd
				df=pd.DataFrame(list(zip(bill_pro_name,bill_pro_hsn,bill_pro_qty,bill_pro_unit,bill_pro_price,bill_pro_tax,bill_pro_disc,bill_pro_taxable_amount,bill_pro_cgst,bill_pro_sgst,bill_pro_total)),columns=['b','c','d','e','f','g','h','i','j','k','l'])
				
				aab=df.groupby(['b','e']).agg({'c': 'first','d': 'sum','f': 'sum','g': 'sum','h': 'sum','i': 'first','j': 'sum','k': 'sum','l': 'sum'}).reset_index().round(3)
				sl=[i for i in range(1,len(aab.index)+1)]
				se = pd.Series(sl)
				aab['m'] = se.values
				cols = ['b','c','d','e','f','g','h','i','j','k','l','m']
				lst = []
				  
				    
				loop_value=0
				if counts_int<=12:
					loop_value=12-counts_int
				for ddd in range(1,loop_value):
						lst.append(['-', '-', '-','-', '-', '-','-', '-', '-','-', '-', '-'])
				df1 = pd.DataFrame(lst, columns=cols)
				aa=aab.append(df1)
				listss=aa.values.tolist()

				import datetime
				now = datetime.datetime.now()


				pro_taxes=products.objects.values_list('product_tax_category', flat=True).get(product_code=request.POST.get('selected_product%d'%x))
				price_taxes=products.objects.values_list('price_tax', flat=True).get(product_code=request.POST.get('selected_product%d'%x))

				tax_date=wholesale_taxes.objects.filter(sale_date__year=now.year, sale_date__month=now.month,sale_date__day=now.day,tax_percent=pro_taxes)
				pri_tax=float(price_taxes)*float(request.POST.get('qty%d'%x))

				if not tax_date:
					cre_tax_table=wholesale_taxes(
					tax_percent=pro_taxes,
					sale_date=now,
					total_tax_amount=request.POST.get('tax_amount%d'%x),
					price_tax_amount=round(pri_tax,2)
					) 
					cre_tax_table.save()
				else:
					taxu=wholesale_taxes.objects.values_list('total_tax_amount', flat=True).get(sale_date__year=now.year, sale_date__month=now.month,sale_date__day=now.day,tax_percent=pro_taxes)
					taxess=float(taxu)+float(request.POST.get('tax_amount%d'%x))
					taxess=round(taxess,2)
					pri_taxu=wholesale_taxes.objects.values_list('price_tax_amount', flat=True).get(sale_date__year=now.year, sale_date__month=now.month,sale_date__day=now.day,tax_percent=pro_taxes)
					pri_taxess=float(pri_taxu)+round(pri_tax,2)
					update_saletotal = wholesale_taxes.objects.filter(sale_date__year=now.year, sale_date__month=now.month,sale_date__day=now.day,tax_percent=pro_taxes).update(total_tax_amount=taxess)
					update_pri_tax = wholesale_taxes.objects.filter(sale_date__year=now.year, sale_date__month=now.month,sale_date__day=now.day,tax_percent=pro_taxes).update(price_tax_amount=pri_taxess)

				
				# sales_final 
			
			if form.is_valid():
				datess=request.POST.get('sale_payment_remainder_date')
				if datess=="":
					datess="1111-11-11"
				cre_sales_final_table=create_wholesale_sales_final(
					sale_type=form.cleaned_data['sale_type'],
					sales_date=form.cleaned_data['sale_date'],
					sales_time=request.POST.get('sale_time'),
					subtotal=form.cleaned_data['sale_total'],                               
					sale_invoice_ref=cust_invo_sum,
					sales_special_discount=form.cleaned_data['sale_special_discount'],
					sales_total=form.cleaned_data['sale_total'],
					sales_payment_received=form.cleaned_data['sale_payment_received'],
					sales_total_tax_amount=form.cleaned_data['sale_total_tax_amount'],
					sales_total_discount_amount=form.cleaned_data['sale_total_discount_amount'],
					sales_round_off=form.cleaned_data['sale_round_off'],
					sales_transaction_mode=form.cleaned_data['sale_transaction_mode'],
					sales_cash_account=form.cleaned_data['sale_cash_account'],
					sales_payment_remainder_date=datess,
					sales_payment_balance=float(form.cleaned_data['sale_total'])-float(form.cleaned_data['sale_payment_received']),
					sales_taxable_amount=round(sum(bill_pro_taxable_amount),3),
					sales_printing=listss
					)
				cre_sales_final_table.save()
				# bill_final_total=form.cleaned_data['sale_total']
				# bill_final_total=str(round(float(bill_final_total),2))

				bill_final_tax=round(float(form.cleaned_data['sale_total_tax_amount']))
				# # bill_final_tax=str(round(sum(bill_final_tax),2))

				bill_final_disc=round(float(form.cleaned_data['sale_total_discount_amount']))
				

				bill_final_date=form.cleaned_data['sale_date']
				
				bill_final_word_total="hhh" 

				import datetime
				now = datetime.datetime.now()
				sales=create_wholesale_sales_final.objects.filter(sales_date__year=now.year, sales_date__month=now.month,sales_date__day=now.day)
				sales_totaling=[]
				for y in sales:
					sales_totaling.append(float(y.subtotal))
				final_totals=sum(sales_totaling)
				
				
				sales_date=sale_wholesale_totals.objects.filter(sales_date__year=now.year, sales_date__month=now.month,sales_date__day=now.day)
				
				
				if not sales_date:
					cre_sales_timings=sale_wholesale_totals(
						sales_date=form.cleaned_data['sale_date'],
						sales_totals=final_totals
						)
					cre_sales_timings.save()
				update_saletotal = sale_wholesale_totals.objects.filter(sales_date__year=now.year, sales_date__month=now.month,sales_date__day=now.day).update(sales_totals=final_totals)
			
			else:
				return HttpResponse(form.errors)
			
			store_info=store_details.objects.latest('id')
			zippy=zip(bill_pro_name,bill_pro_hsn,bill_pro_qty,bill_pro_unit,bill_pro_price,bill_pro_tax,bill_pro_disc,bill_pro_taxable_amount,bill_pro_cgst,bill_pro_sgst,bill_pro_total)
			return render(request,'sales/sales_bill.html',{'zippy':listss,'bill_final_date':bill_final_date,'bill_final_total':round(sum(bill_pro_total)-int(sp_disc)),'sp_disc':sp_disc,'bill_final_tax':bill_final_tax,'bill_final_disc':bill_final_disc,
				'payment_recieved':form.cleaned_data['sale_payment_received'],'cust_invo_sum':"WH"+str(cust_invo_sum),'bill_final_word_total':bill_final_word_total,'store_info':store_info})

	form = create_sale()
	
	active_sidebar4=1
	return render(request,'sales/create_sales.html',{'active_sidebar4':active_sidebar4,'form':form,
		'prodx':prodx,'unit_types':unit_types})
	
@login_required(login_url='/login')
def create_sales_ajax(request):
	tag_str='' 
	tag_str2=''
	tag_alter=''
	tag_alter_post=''
	if request.method == 'POST' and request.POST['action'] == 'selection':

		if not request.POST.get('selection_bar'):
			get_id=request.POST.get('selection_sele')
			# print("sle",get_id)
		else:
			get_id=request.POST.get('selection_bar')
			# print("bar",get_id)
		get_type=request.POST.get('select_type')
		int_get_type=int(get_type)
		get_pro_ids=products.objects.values_list('id', flat=True).get(product_code=get_id)
		get_barcode=get_id
		get_pro_unit=products.objects.values_list('unit_type_ref', flat=True).get(product_code=get_id)
		get_default_unit=categorisation.objects.values_list('product_default_unit', flat=True).get(product_unit_type=get_pro_unit)	
		get_default_unit_prefix=categorisation.objects.values_list('product_default_unit_prefix', flat=True).get(product_unit_type=get_pro_unit)
		get_alter_unit=products.objects.values_list('alternate_unit_ref', flat=True).get(product_code=get_id)
		get_pr_id=products.objects.values_list('id', flat=True).get(product_code=get_id)
		get_alter_unit_loop=alternate_cost_price.objects.all().filter(product_ref_id=get_pr_id)
		get_stock=products.objects.values_list('product_stock', flat=True).get(product_code=get_id)
		get_tax_category=products.objects.values_list('product_tax_category', flat=True).get(product_code=get_id)
		get_discount=products.objects.values_list('product_discount', flat=True).get(product_code=get_id)
		if int_get_type==1:
			get_price=products.objects.values_list('final_price', flat=True).get(product_code=get_id)
			tax_amount=(float(products.objects.values_list('taxable_price', flat=True).get(product_code=get_id))*float(get_tax_category))/100
		else:
			get_price=products.objects.values_list('final_wholesale_price', flat=True).get(product_code=get_id)
			tax_amount=(float(products.objects.values_list('wholesale_taxable_price', flat=True).get(product_code=get_id))*float(get_tax_category))/100
		
		

		total_tax_amount=1*float(tax_amount)
		total_tax_amount=round(total_tax_amount,3)
		
		sub_total=1*float(get_price)
		excluded_tax=(float(products.objects.values_list('product_tax_category', flat=True).get(product_code=get_id))*sub_total)/100
		
		tax_subtotal=float(sub_total)

		store_ib=store_details.objects.latest('id')

		if int_get_type==1:
			if store_ib.cess_status=="YES":
				cess_total=float(sub_total)-(float(products.objects.values_list('product_tax_amount', flat=True).get(product_code=get_id)))
			else:
				cess_total=0
		else:
			cess_total=0

		
		discount_subbtotal=float(tax_subtotal)-float(get_discount)

		# if get_alter_unit == '0':
		# 	tag_str=tag_str+'<option value="0">{}</option>'.format(get_default_unit,get_default_unit)
		# 	tag_alter=tag_alter+'<option value="0">{}</option>'.format(get_default_unit_prefix,get_default_unit_prefix)
			
		# else:
		# 	tag_str='<option value="0">{}</option>'.format(get_default_unit)
		# 	tag_alter='<option value="0">{}</option>'.format(get_default_unit_prefix)
			
		for x in get_alter_unit_loop:

			get_units=alternate_units.objects.values_list('product_alternate_unit', flat=True).get(product_alternate_code=x.unit_type_id)
			get_units_prefix=alternate_units.objects.values_list('product_alternate_unit_prifix', flat=True).get(product_alternate_code=x.unit_type_id)
			tag_str=tag_str+'<option value="{}">{}</option>'.format(x.unit_type_id,get_units)
			tag_alter=tag_alter+'<option value="{}">{}</option>'.format(x.unit_type_id,get_units_prefix)
				

		totals=0
		fin_tota=0
		fin_taxa=0
		fin_disca=0
		if not request.POST.get('selection_bar'):
			get_pro_id=request.POST.get('selection_sele')
			# print("sle",get_id)
		else:
			get_pro_id=request.POST.get('selection_bar')
			# print("bar",get_id)
		# get_pro_id=request.POST.get('selection')
		get_pro_name=products.objects.values_list('product_name', flat=True).get(product_code=get_pro_id)
		get_qty=1
		subtotiii=request.POST.get('sub_toti')
		subtaxii=request.POST.get('sub_taxi')
		subdiscii=request.POST.get('sub_disci')
		
		get_tax=total_tax_amount
		
		get_subtotal=discount_subbtotal
		get_count=request.POST.get('counti')
		fin_tota=request.POST.get('fintotal')
		fin_taxa=request.POST.get('fintaxe')
		fin_disca=request.POST.get('findiscount')

		totals=float(fin_tota)+float(subtotiii)
		tax_totals=float(fin_taxa)+float(subtaxii)
		tax_totals=round(tax_totals,3)
		disc_totals=float(fin_disca)+float(subdiscii)

		tag_str2=tag_str2+'<tr><td><input type="text" class="form-control" width="300" style="width: 120px;margin-right: -20px;" \
		id="bar_code_id{}" name="bar_code{}"readonly="readonly" value="{}"></td><td>\
		<select class="form-control select" width="300" style="width: 120px;margin-right: -20px;" \
		id="select_id{}"name="selected_product{}" readonly="readonly"><option selected value="{}">{}</option>\
		</select></td><td> <select class="form-control select" width="100" style="width: 65px;margin-right: -20px;" \
		id="unit_id{}" name="selected_unit{}" readonly="readonly">{}</select>\
		<input class="form-control" type="text"  style="display:none" id="unit_post_id{}" name="selected_post_unit{}" value={}>\
		</td><td><input class="form-control" type="text" placeholder="Qty" width="100" style="width: 65px;margin-right: -20px;"\
		 id="qty_id{}" name="qty{}" readonly="readonly" value="{}"></td><td><input class="form-control"\
		  type="text" width="100" style="width: 70px;margin-right: -20px;" id="stock_id{}" name="stock{}" readonly="readonly" value="{}"></td>\
		  <td><input class="form-control" type="text" placeholder="Price" width="100" style="width: 85px;margin-right: -20px;" id="price_id{}" \
		  name="price{}" readonly="readonly" value="{}"></td><td><input class="form-control" type="text"\
		   width="100" style="width: 90px;margin-right: -20px;" id="tax_amount_id{}" name="tax_amount{}" readonly="readonly" value="{}"></td>\
		   <td> <input class="form-control" type="text" width="100" style="width: 90px;margin-right: -20px;" id="discount_id{}" name="discount{}" \
		   readonly="readonly" value="{}"></td><td class="summing"><input class="form-control" type="text" \
		   width="100" style="width: 100px;margin-right: -20px;" id="subtotal_id{}"  name="sub_total{}" readonly="readonly" value="{}">\
		   <input type="hidden" value="{}" id="counts" style="width: 0%;" name="counting"></td><td>\
		   <span width="100" style="font-size:13px;width: 80px;><input type="button" class="btn btn-primary btn-sm mb-5" \
		   id="editing"><i class="mdi mdi-pencil"></i>Edit</span>&nbsp;<span width="100" style="font-size:13px;width: 80px;>\
		   <input type="button" class="btn btn-danger btn-sm mb-5" id="deleting"><i class="mdi mdi-delete"></i>Delete</span>&nbsp;'.format(get_count,get_count,get_barcode,get_count,get_count,get_pro_id,get_pro_name,get_count,get_count,tag_alter,get_count,get_count,get_default_unit,get_count,get_count,get_qty,get_count,get_count,get_stock,get_count,get_count,get_price,get_count,get_count,get_tax,get_count,get_count,get_discount,get_count,get_count,get_subtotal,get_count)
		# tag_head="<tr><th></th><th>PRODUCT</th><th>QTY</th><th>UNIT</th><th>PRICE</th><th>DISCOUNT</th><th>TOTAL</th><th>STATUS</th><th>SUBTOTAL</th></tr></thead><tbody>"




		jsona = json.dumps({'get_barcode': get_barcode ,'get_pro_unit':get_pro_unit,'get_stock':get_stock,'get_price':get_price,'get_discount':get_discount,'tax_amount':tax_amount,'tag_str2':tag_str2,'tag_str':tag_str,'discount_subbtotal':discount_subbtotal,'totals':totals,'tax_totals':tax_totals,'disc_totals':disc_totals,'get_pro_ids':get_pro_ids,'cess_total':cess_total})
		return HttpResponse(jsona, content_type='application/json')


	if request.method == 'POST' and request.POST['action'] == 'quantity':
		totals=0
		fin_tota=0
		fin_taxa=0
		fin_disca=0
		sub_total=0
		qty_no=request.POST.get('quanties')
		unit_val=request.POST.get('unit_val')
		if not unit_val:
			unit_val="0"
		
		# get_id=request.POST.get('selected')
		if not request.POST.get('selection_bar'):
			get_pro_id=request.POST.get('selection_sele')
			# print("sle",get_id)
		else:
			get_pro_id=request.POST.get('selection_bar')
			# print("bar",get_id)
		get_type=request.POST.get('select_type') 
		fin_tota=request.POST.get('fintotal')
		fin_taxa=request.POST.get('fintaxe')
		fin_disca=request.POST.get('findiscount')

		int_get_type=int(get_type)
		get_tax_category=products.objects.values_list('product_tax_category', flat=True).get(product_code=get_pro_id)
		get_discount=products.objects.values_list('product_discount', flat=True).get(product_code=get_pro_id)
		if int_get_type==1:
			if unit_val=="0":
				get_price=products.objects.values_list('final_price', flat=True).get(product_code=get_pro_id)
				tax_amount=(float(products.objects.values_list('taxable_price', flat=True).get(product_code=get_pro_id))*float(get_tax_category))/100
			else:
				get_pr_id=products.objects.values_list('id', flat=True).get(product_code=get_pro_id)
				get_price=alternate_cost_price.objects.values_list('product_price', flat=True).get(product_ref_id=get_pr_id,unit_type_id=unit_val)
				tax_amount=(float(alternate_cost_price.objects.values_list('taxable_price', flat=True).get(product_ref_id=get_pr_id,unit_type_id=unit_val))*float(get_tax_category))/100
		else:
			if unit_val=="0":
				get_price=products.objects.values_list('final_wholesale_price', flat=True).get(product_code=get_pro_id)
				tax_amount=(float(products.objects.values_list('wholesale_taxable_price', flat=True).get(product_code=get_pro_id))*float(get_tax_category))/100
			else:
				get_pr_id=products.objects.values_list('id', flat=True).get(product_code=get_pro_id)
				get_price=alternate_cost_price.objects.values_list('product_price', flat=True).get(product_ref_id=get_pr_id,unit_type_id=unit_val)
				tax_amount=(float(alternate_cost_price.objects.values_list('taxable_price', flat=True).get(product_ref_id=get_pr_id,unit_type_id=unit_val))*float(get_tax_category))/100
		
		

		# total_tax_amount=float(qty_no)*float(tax_amount)
		# total_tax_amount=round(total_tax_amount,3)

		
		
		
		
		total_tax_amount=float(qty_no)*float(tax_amount)
		total_tax_amount=round(total_tax_amount,3)




		total_discount=float(qty_no)*float(get_discount)
		total_discount=round(total_discount,3)


		sub_total=float(qty_no)*float(get_price)
		sub_total=round(sub_total,3)
		excluded_tax=(float(products.objects.values_list('product_tax_category', flat=True).get(product_code=get_pro_id))*sub_total)/100
		total__ex_tax_amount=float(qty_no)*float(excluded_tax)
		total__ex_tax_amount=round(total__ex_tax_amount,3)
		
		tax_subtotal=float(sub_total)

		store_ib=store_details.objects.latest('id')

		if int_get_type==1:
			if store_ib.cess_status=="YES":
				cess_total=float(sub_total)-(float(products.objects.values_list('product_tax_amount', flat=True).get(product_code=get_pro_id))*float(qty_no))
			else:
				cess_total=0
		else:
			cess_total=0

		#cess_total=float(sub_total)-(float(products.objects.values_list('product_tax_amount', flat=True).get(product_code=get_pro_id))*float(qty_no))
		discount_subtotal=float(tax_subtotal)-float(total_discount)

		totals=float(fin_tota)+float(discount_subtotal)
		totals=round(totals,3)
		tax_totals=float(fin_taxa)+float(total_tax_amount)
		tax_totals=round(tax_totals,3)
		disc_totals=float(fin_disca)+float(total_discount)
		disc_totals=round(disc_totals,3)

		jsona = json.dumps({'total_tax_amount':total_tax_amount,'total_discount':total_discount,'tax_subtotal':discount_subtotal,'totals':totals,'tax_totals':tax_totals,'disc_totals':disc_totals,'cess_total':cess_total})

		return HttpResponse(jsona, content_type='application/json')

	prod_ids=[]
	tag_str=""
	
	if request.method == 'POST' and request.POST['action'] == 'unit_selection':
		totals=0
		fin_tota=0
		fin_taxa=0
		fin_disca=0
		sub_total=0
		qty_no=request.POST.get('sele_qty')
		unit_val=request.POST.get('unit_val')
		if not request.POST.get('selection_bar'):
			get_pro_id=request.POST.get('selection_sele')
			
		else:
			get_pro_id=request.POST.get('selection_bar')

		get_type=request.POST.get('select_type') 
		fin_tota=request.POST.get('fintotal')
		fin_taxa=request.POST.get('fintaxe')
		fin_disca=request.POST.get('findiscount')

		int_get_type=int(get_type)
		get_tax_category=products.objects.values_list('product_tax_category', flat=True).get(product_code=get_pro_id)
		get_discount=products.objects.values_list('product_discount', flat=True).get(product_code=get_pro_id)
		if int_get_type==1:
			if unit_val=="0":
				get_price=products.objects.values_list('final_price', flat=True).get(product_code=get_pro_id)
				tax_amount=(float(products.objects.values_list('taxable_price', flat=True).get(product_code=get_pro_id))*float(get_tax_category))/100
			else:
				get_pr_id=products.objects.values_list('id', flat=True).get(product_code=get_pro_id)
				get_price=alternate_cost_price.objects.values_list('product_price', flat=True).get(product_ref_id=get_pr_id,unit_type_id=unit_val)
				tax_amount=(float(alternate_cost_price.objects.values_list('taxable_price', flat=True).get(product_ref_id=get_pr_id,unit_type_id=unit_val))*float(get_tax_category))/100
		else:
			if unit_val=="0":
				get_price=products.objects.values_list('final_wholesale_price', flat=True).get(product_code=get_pro_id)
				tax_amount=(float(products.objects.values_list('wholesale_taxable_price', flat=True).get(product_code=get_pro_id))*float(get_tax_category))/100
			else:
				get_pr_id=products.objects.values_list('id', flat=True).get(product_code=get_pro_id)
				get_price=alternate_cost_price.objects.values_list('product_price', flat=True).get(product_ref_id=get_pr_id,unit_type_id=unit_val)
				tax_amount=(float(alternate_cost_price.objects.values_list('taxable_price', flat=True).get(product_ref_id=get_pr_id,unit_type_id=unit_val))*float(get_tax_category))/100
		total_tax_amount=float(qty_no)*float(tax_amount)
		total_tax_amount=round(total_tax_amount,3)




		total_discount=float(qty_no)*float(get_discount)
		total_discount=round(total_discount,3)


		sub_total=float(qty_no)*float(get_price)
		sub_total=round(sub_total,3)
		excluded_tax=(float(products.objects.values_list('product_tax_category', flat=True).get(product_code=get_pro_id))*sub_total)/100
		total__ex_tax_amount=float(qty_no)*float(excluded_tax)
		total__ex_tax_amount=round(total__ex_tax_amount,3)
		
		tax_subtotal=float(sub_total)

		store_ib=store_details.objects.latest('id')

		if int_get_type==1:
			if store_ib.cess_status=="YES":
				cess_total=float(sub_total)-(float(products.objects.values_list('product_tax_amount', flat=True).get(product_code=get_pro_id))*float(qty_no))
			else:
				cess_total=0
		else:
			cess_total=0

		#cess_total=float(sub_total)-(float(products.objects.values_list('product_tax_amount', flat=True).get(product_code=get_pro_id))*float(qty_no))
		discount_subtotal=float(tax_subtotal)-float(total_discount)

		totals=float(fin_tota)+float(discount_subtotal)
		totals=round(totals,3)
		tax_totals=float(fin_taxa)+float(total_tax_amount)
		tax_totals=round(tax_totals,3)
		disc_totals=float(fin_disca)+float(total_discount)
		disc_totals=round(disc_totals,3)

		jsona = json.dumps({'total_tax_amount':total_tax_amount,'total_discount':total_discount,'tax_subtotal':discount_subtotal,'totals':totals,'tax_totals':tax_totals,'disc_totals':disc_totals,'cess_total':cess_total,'get_price':get_price})

		return HttpResponse(jsona, content_type='application/json')

	if request.method == 'POST' and request.POST['action'] == 'edit_op':
		
		bar=request.POST.get('barcode')
		sel=request.POST.get('selection')
		get_pro_name=products.objects.values_list('product_name', flat=True).get(product_code=sel)
		get_unit=request.POST.get('unit')
		get_qty=request.POST.get('qty')
		get_stock=request.POST.get('stock')
		get_price=request.POST.get('price')
		get_tax=request.POST.get('tax')
		get_discount=request.POST.get('discount')
		get_subtotal=request.POST.get('subtotal')
		
		jsona = json.dumps({'bar':bar,'sel':sel,'get_unit':get_unit,'get_qty':get_qty,'get_stock':get_stock,'get_price':get_price,
			'get_tax':get_tax,'get_discount':get_discount,'get_subtotal':get_subtotal})

		return HttpResponse(jsona, content_type='application/json')

	if request.method == 'POST' and request.POST['action'] == 'del_op':
		
		get_tax=request.POST.get('tax')
		get_discount=request.POST.get('discount')
		get_subtotal=request.POST.get('subtotal')
		
		jsona = json.dumps({'get_tax':get_tax,'get_discount':get_discount,'get_subtotal':get_subtotal})

		return HttpResponse(jsona, content_type='application/json')

	if request.method == 'POST' and request.POST['action'] == 'discount':
		get_id=request.POST.get('selected')
		get_total=request.POST.get('final_total')
		final_total=float(get_total)-float(get_id)
		jsona = json.dumps({'final_total':final_total})

		return HttpResponse(jsona, content_type='application/json')


	if request.method == 'POST' and request.POST['action'] == 'custome':
		get_id=request.POST.get('cust')
		get_cust_debit=customer.objects.values_list('customer_first_time_debit', flat=True).get(pk=get_id)
		get_cust_credit=customer.objects.values_list('customer_first_time_credit', flat=True).get(pk=get_id)
		jsona = json.dumps({'get_cust_debit':get_cust_debit,'get_cust_credit':get_cust_credit})
		return HttpResponse(jsona, content_type='application/json')

# def sales_bill(request):
# 	return render(request,'sales/sales_bill.html')	




 



@login_required(login_url='/login')
def view_sales(request,id):
	prod_name=[]
	pro_qty=[]
	pro_unit=[]
	cost=[]
	price=[]
	tax_per=[]
	dis_per=[]
	tax_amount=[]
	discount_amount=[]
	subtotal=[]
	returned=[]
	sales=create_sales_final.objects.all().filter(pk=id)
	for x in sales:
		sale_invoice_id=x.sale_invoice_ref
	sale_table=create_sales_table.objects.all().filter(sales_invoice_no=sale_invoice_id)
	for y in sale_table:
		sale_id=(y.sales_product_ref_id)
		pro_qty.append(y.sales_qty)
		prod=products.objects.all().filter(pk=sale_id)
		for z in prod:
			prod_name.append(products.objects.values_list('product_name', flat=True).get(pk=sale_id))
			pro_unit.append(z.unit_type_ref)
			cost.append(z.product_cost)
			price.append(z.product_price)
			tax_amount.append(z.product_tax_amount)
			discount_amount.append(z.product_discount)

	zipped=zip(prod_name,pro_unit,cost,price,tax_amount,discount_amount,pro_qty)

	return render(request,'sales/view_sales.html' ,{'zipped':zipped,'sales':sales})

@login_required(login_url='/login')
def edit_sales(request,id):
	prod_name=[]
	pro_qty=[]
	pro_unit=[]
	cost=[]
	price=[]
	tax_per=[]
	dis_per=[]
	tax_amount=[]
	discount_amount=[]
	subtotal=[]
	returned=[]
	sales=create_sales_final.objects.all().filter(pk=id)
	for x in sales:
		sale_invoice_id=x.sale_invoice_ref
	sale_table=create_sales_table.objects.all().filter(sales_invoice_no=sale_invoice_id)
	for y in sale_table:
		sale_id=(y.sales_product_ref_id)
		pro_qty.append(y.sales_qty)
		prod=products.objects.all().filter(pk=sale_id)
		for z in prod:
			prod_name.append(products.objects.values_list('product_name', flat=True).get(pk=sale_id))
			pro_unit.append(z.unit_type_ref)
			cost.append(z.product_cost)
			price.append(z.product_price)
			tax_amount.append(z.product_tax_amount)
			discount_amount.append(z.product_discount)

	zipped=zip(prod_name,pro_unit,cost,price,tax_amount,discount_amount,pro_qty)


	return render(request,'sales/edit_sales.html',{'sales':sales})

@login_required(login_url='/login')
def update_sales(request,id):
	if request.method=='POST':
		sales_update=create_sales_final.objects.get(pk=id)
		sales_update.sale_type=request.POST['sale_type']
		sales_update.sales_time=request.POST['Time']
		sales_update.subtotal=request.POST['subtotal']
		sales_update.customer_ref_name=request.POST['customer_na']
		sales_update.sales_credit=request.POST['credit']
		sales_update.sales_debit=request.POST['debit']
		sales_update.sales_special_discount=request.POST['spcl dsct']
		sales_update.sales_total=request.POST['total']
		sales_update.sales_payment_received=request.POST['paymnt rcd']
		sales_update.sales_total_tax_amount=request.POST['total tax amt']
		sales_update.sales_total_discount_amount=request.POST['total dsc amt']
		sales_update.sales_round_off=request.POST['roundoff']
		sales_update.sales_transaction_mode=request.POST['trans mode']
		sales_update.sales_cash_account=request.POST['cshacct']
		sales_update.sales_payment_remainder_date=request.POST['paymntrmddate']
		sales_update.save()
	int_id=int(id)
	return HttpResponseRedirect('/sales/view_sales/%d'%int_id)

@login_required(login_url='/login')
def delete_sales(request,id):
	del_sales=create_sales_final.objects.get(pk=id)
	get_sale_invoice=create_sales_final.objects.values_list('sale_invoice_ref', flat=True).get(pk=id)
	sale_del=create_sales_table.objects.all().filter(sales_invoice_no=get_sale_invoice)
	#return HttpResponse(del_sales.sales_total)
	
	tod_sales=sale_totals.objects.values_list('sales_totals', flat=True).get(sales_date=del_sales.sales_date)
	
	update_saletotal = sale_totals.objects.filter(sales_date=del_sales.sales_date).update(sales_totals=round(float(tod_sales)-float(del_sales.sales_total)))
	#return_c=sales_returned.objects.filter(sale_return_date__year=now.year, sale_return_date__month=now.month,sale_return_date__day=now.day)
	

	del_sales.delete()
	sale_del.delete()
	return HttpResponseRedirect('/sales/')

def delete_all_sales(request):
	pro_list=request.POST.get('checked_pro')
	if pro_list=="0":
		return HttpResponse('/sales/')
	else:
		pro_pro_list = pro_list.split (",")
		
		# convert each element as integers
		pro_lists = []
		for i in pro_pro_list:
			pro_lists.append(int(i))

		for x in pro_lists:
			
			del_sales=create_sales_final.objects.get(pk=x)
			get_sale_invoice=create_sales_final.objects.values_list('sale_invoice_ref', flat=True).get(pk=x)
			sale_del=create_sales_table.objects.all().filter(sales_invoice_no=get_sale_invoice)
			tod_sales=sale_totals.objects.values_list('sales_totals', flat=True).get(sales_date=del_sales.sales_date)
	
			update_saletotal = sale_totals.objects.filter(sales_date=del_sales.sales_date).update(sales_totals=round(float(tod_sales)-float(del_sales.sales_total)))
			del_sales.delete()
			sale_del.delete()
		return HttpResponseRedirect('/sales/')


@login_required(login_url='/login')
def delete_wholesale_sales(request,id):
	del_sales=create_wholesale_sales_final.objects.get(pk=id)
	get_sale_invoice=create_wholesale_sales_final.objects.values_list('sale_invoice_ref', flat=True).get(pk=id)
	sale_del=create_wholesale_sales_table.objects.all().filter(sales_invoice_no=get_sale_invoice)
	#return HttpResponse(del_sales.sales_total)
	
	# tod_sales=sale_totals.objects.values_list('sales_totals', flat=True).get(sales_date=del_sales.sales_date)
	
	# update_saletotal = sale_totals.objects.filter(sales_date=del_sales.sales_date).update(sales_totals=round(float(tod_sales)-float(del_sales.sales_total)))
	#return_c=sales_returned.objects.filter(sale_return_date__year=now.year, sale_return_date__month=now.month,sale_return_date__day=now.day)
	

	del_sales.delete()
	sale_del.delete()
	return HttpResponseRedirect('/sales_wholesale/')

def delete_all_wholesale_sales(request):
	pro_list=request.POST.get('checked_pro')
	if pro_list=="0":
		return HttpResponse('/sales_wholesale/')
	else:
		pro_pro_list = pro_list.split (",")
		
		# convert each element as integers
		pro_lists = []
		for i in pro_pro_list:
			pro_lists.append(int(i))

		for x in pro_lists:
			
			del_sales=create_wholesale_sales_final.objects.get(pk=x)
			get_sale_invoice=create_wholesale_sales_final.objects.values_list('sale_invoice_ref', flat=True).get(pk=x)
			sale_del=create_wholesale_sales_table.objects.all().filter(sales_invoice_no=get_sale_invoice)
			# tod_sales=sale_totals.objects.values_list('sales_totals', flat=True).get(sales_date=del_sales.sales_date)
	
			# update_saletotal = sale_totals.objects.filter(sales_date=del_sales.sales_date).update(sales_totals=round(float(tod_sales)-float(del_sales.sales_total)))
			del_sales.delete()
			sale_del.delete()
		return HttpResponseRedirect('/sales_wholesale/')


@login_required(login_url='/login')
def sales_dashboard_ajax(request):
	
	import datetime
	now = datetime.datetime.now()
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
	for i in range(1,now.day+1):
		purchases=purchase_totals.objects.filter(purchase_time__year=now.year, purchase_time__month=now.month,purchase_time__day=i)
		
		for s in purchases:
			d=s.purchases_total
			globals()["expence_day" + str(i)] = d

	sales_to=sale_totals.objects.filter(sales_date__year=now.year, sales_date__month=now.month)
	sale_sum=0
	for h in sales_to:
		sale_sum=float(sale_sum)+float(h.sales_totals)

	purch_to=purchase_totals.objects.filter(purchase_time__year=now.year, purchase_time__month=now.month)

	purch_su=0
	for dd in purch_to:
		purch_su=float(purch_su)+float(dd.purchases_total)

	tod_sales=sale_totals.objects.values_list('sales_totals', flat=True).get(sales_date__year=now.year, sales_date__month=now.month,sales_date__day=now.day)

	tod_purchases=purchase_totals.objects.values_list('purchases_total', flat=True).get(purchase_time__year=now.year, purchase_time__month=now.month,purchase_time__day=now.day)
	sale_c=create_sales_final.objects.filter(sales_date__year=now.year, sales_date__month=now.month,sales_date__day=now.day)
	sale_counts=0
	discount_amt=0
	pay_recved=0
	tot_disc=0
	for cc in sale_c:
		sale_counts=sale_counts+1

		pay_recved=float(pay_recved)+float(cc.sales_payment_received)
		discount_amt=float(discount_amt)+float(cc.sales_special_discount)
		tot_disc=float(tot_disc)+float(cc.sales_total_discount_amount)
		
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
		pro_pri=products.objects.values_list('product_price', flat=True).get(pk=pri)
		pro_dis=products.objects.values_list('product_discount', flat=True).get(pk=pri)
		pro_cost=products.objects.values_list('product_cost', flat=True).get(pk=pri)
		
		pro_prices=float(pro_pri)-float(pro_dis)-float(pro_cost)
		totals=float(totals)+float(pro_prices*prqt)
	jsona = json.dumps({'sale_sum':sale_sum,'purch_su':purch_su,'tod_sales':tod_sales,'tod_purchases':tod_purchases,'sale_counts':sale_counts,'return_counts':return_counts,'retu_amou':retu_amou,'discount_amt':discount_amt,'pay_recved':pay_recved,'totals':totals,'tot_disc':tot_disc})

	return HttpResponse(jsona, content_type='application/json')


def print_sales(request,id):
	counts_int=0
	list_count=0
	new_count=[]
	sl_no=[]
	bill_pro_name=[]
	bill_pro_hsn=[]
	bill_pro_qty=[]
	bill_pro_unit=[]
	bill_pro_price=[]
	bill_pro_disc=[]
	bill_pro_tax=[]
	bill_pro_cgst=[]
	bill_pro_sgst=[]
	bill_pro_igst=[]
	bill_pro_total=[]
	bill_pro_taxable_amount=[]
	listssa=create_sales_final.objects.values_list('sales_printing', flat=True).get(pk=id)
	sales_invo=create_sales_final.objects.values_list('sale_invoice_ref', flat=True).get(pk=id)
	bill_final_date=create_sales_final.objects.values_list('sales_date', flat=True).get(pk=id)
	bill_final_total=create_sales_final.objects.values_list('subtotal', flat=True).get(pk=id)
	bill_final_tax=create_sales_final.objects.values_list('sales_total_tax_amount', flat=True).get(pk=id)
	bill_final_disc=create_sales_final.objects.values_list('sales_total_discount_amount', flat=True).get(pk=id)
	payment_recieved=create_sales_final.objects.values_list('sales_payment_received', flat=True).get(pk=id)
	cust_invo_sum=create_sales_final.objects.values_list('sale_invoice_ref', flat=True).get(pk=id)
	spc_disc=create_sales_final.objects.values_list('sales_special_discount', flat=True).get(pk=id)
	sales=create_sales_table.objects.all().filter(sales_invoice_no=sales_invo)
	
	import ast
	lists=ast.literal_eval(listssa)
	for x in lists:
		list_count=len(x)


	store_info=store_details.objects.latest('id')
	
	if list_count==13:
		return render(request,'sales/print_retail_sales_bill.html',{'zippy':lists,'bill_final_date':bill_final_date,'bill_final_total':bill_final_total,'bill_final_tax':bill_final_tax,'bill_final_disc':bill_final_disc,
					'payment_recieved':payment_recieved,'cust_invo_sum':"NO"+str(cust_invo_sum),'spc_disc':spc_disc,'store_info':store_info})
	else:
		return render(request,'sales/print_wholesale_sales_bill.html',{'zippy':lists,'bill_final_date':bill_final_date,'bill_final_total':bill_final_total,'bill_final_tax':bill_final_tax,'bill_final_disc':bill_final_disc,
					'payment_recieved':payment_recieved,'cust_invo_sum':"NO"+str(cust_invo_sum),'spc_disc':spc_disc,'store_info':store_info})



def print_sales_wholesale(request,id):
	counts_int=0
	list_count=0
	new_count=[]
	sl_no=[]
	bill_pro_name=[]
	bill_pro_hsn=[]
	bill_pro_qty=[]
	bill_pro_unit=[]
	bill_pro_price=[]
	bill_pro_disc=[]
	bill_pro_tax=[]
	bill_pro_cgst=[]
	bill_pro_sgst=[]
	bill_pro_igst=[]
	bill_pro_total=[]
	bill_pro_taxable_amount=[]
	listssa=create_wholesale_sales_final.objects.values_list('sales_printing', flat=True).get(pk=id)
	sales_invo=create_wholesale_sales_final.objects.values_list('sale_invoice_ref', flat=True).get(pk=id)
	bill_final_date=create_wholesale_sales_final.objects.values_list('sales_date', flat=True).get(pk=id)
	bill_final_total=create_wholesale_sales_final.objects.values_list('subtotal', flat=True).get(pk=id)
	bill_final_tax=create_wholesale_sales_final.objects.values_list('sales_total_tax_amount', flat=True).get(pk=id)
	bill_final_disc=create_wholesale_sales_final.objects.values_list('sales_total_discount_amount', flat=True).get(pk=id)
	payment_recieved=create_wholesale_sales_final.objects.values_list('sales_payment_received', flat=True).get(pk=id)
	cust_invo_sum=create_wholesale_sales_final.objects.values_list('sale_invoice_ref', flat=True).get(pk=id)
	spc_disc=create_sales_final.objects.values_list('sales_special_discount', flat=True).get(pk=id)
	sales=create_wholesale_sales_table.objects.all().filter(sales_invoice_no=sales_invo)
	
	import ast
	lists=ast.literal_eval(listssa)
	
	for x in lists:
		list_count=len(x)


	store_info=store_details.objects.latest('id')
	
	if list_count==13:
		return render(request,'sales/print_retail_sales_bill.html',{'zippy':lists,'bill_final_date':bill_final_date,'bill_final_total':bill_final_total,'bill_final_tax':bill_final_tax,'bill_final_disc':bill_final_disc,
					'payment_recieved':payment_recieved,'cust_invo_sum':"NO"+str(cust_invo_sum),'spc_disc':spc_disc,'store_info':store_info})
	else:
		return render(request,'sales/print_wholesale_sales_bill.html',{'zippy':lists,'bill_final_date':bill_final_date,'bill_final_total':bill_final_total,'bill_final_tax':bill_final_tax,'bill_final_disc':bill_final_disc,
					'payment_recieved':payment_recieved,'cust_invo_sum':"NO"+str(cust_invo_sum),'spc_disc':spc_disc,'store_info':store_info})













