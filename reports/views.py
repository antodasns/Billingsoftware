from django.shortcuts import render
from reports.forms import create_sales_report,create_gst_report
from reports.models import create_sales_report_table,create_Gst_report_table

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from settings_billing.models import store_details
from django.http import HttpResponse
from product.models import products,categorisation,alternate_units
from sales.models import create_sales_table,create_sales_final,sale_totals,taxes,reports
import pandas as pd
# Create your views here.

@login_required(login_url='/login')
def create_sales_reports(request):
	
	form=create_sales_report()
	active_sidebar6=1
	return render(request,'reports/create_sales_reports.html',{'active_sidebar6':active_sidebar6,'form':form})

def create_monthly_reports(request):
	
	form=create_sales_report()
	active_sidebar6=1
	return render(request,'reports/create_monthly_report.html',{'active_sidebar6':active_sidebar6,'form':form})

#DAILY SALES
@login_required(login_url='/login')
def view_sales_reports(request):
	final_price=[]
	sale_date=[]
	sale_total=[]
	get_price=[]
	
	get_unit=[]
	spe_disc=[]
	payment_recieved=[]
	taxu=[]
	total_balance=0
	count=0
	df_tax_per=[]
	df_tax_gst=[]
	df_tax_total=[]

	if request.method == 'POST':
			
		form=create_sales_report(request.POST)
		if form.is_valid():
			
				
				
			create_sales_report_month=int(request.POST.get('create_sales_report_month'))
			create_sales_report_year=int(request.POST.get('create_sales_report_year'))
			sales=create_sales_final.objects.filter(sales_date__year=create_sales_report_year, sales_date__month=create_sales_report_month)
			daily_repor=reports.objects.all()
			
			for invo in sales:
				sale_date.append(invo.sales_date)
				sale_total.append(float(invo.sales_total))
				spe_disc.append(float(invo.sales_special_discount))
				payment_recieved.append(float(invo.sales_payment_received))
				total_balance=sum(sale_total)-sum(payment_recieved)
				sales_pro=create_sales_table.objects.filter(sales_invoice_no=invo.sale_invoice_ref)
				sales_prod=create_sales_table.objects.all()
				product_det=products.objects.all()
				
				count=count+1



			tax=taxes.objects.filter(sale_date__year=create_sales_report_year, sale_date__month=create_sales_report_month)
			for x in tax:
				df_tax_per.append(x.tax_percent)
				df_tax_gst.append(round(float(x.total_tax_amount)/2,2))
				df_tax_total.append(x.total_tax_amount)
			df=pd.DataFrame(list(zip(df_tax_per,df_tax_gst,df_tax_total)),columns=['a','b','c'])
			df_1=df.groupby('a', as_index=False).agg({'b':'sum', 'c':'sum'})

			listss=df_1.values.tolist()
			for tt in tax:
				taxu.append(float(tt.total_tax_amount))
				tota_tax=sum(taxu)
				tota_tax_rounded=round(tota_tax,2)
			# else: 
			# 	return HttpResponse(form.errors)
	store_info=store_details.objects.latest('id')
	form=create_sales_report()
	active_sidebar1=7
	return render(request,'reports/repo.html',{'active_sidebar1':active_sidebar1,'form':form,'sales':sales,'daily_repor':daily_repor,'sales_prod':sales_prod,'product_det':product_det,
			'count':count,'sales_totals':sum(sale_total),'spe_disc':sum(spe_disc),'payment_recieved':sum(payment_recieved),'total_balance':total_balance,
			'tota_tax':tota_tax_rounded,'tax':listss,'store_info':store_info})
	
#MONTHLY SALES
def view_monthly_sales_reports(request):
	
	
	taxu=[]
	totu=[]
	dates=[]
	counting=[]
	days=[]
	taxu=[]
	pri_taxu=[]
	tota_tax=[]
	sale_date=[]
	sale_total=[]
	spe_disc=[]
	payment_recieved=[]
	sale_total1=[]
	sum_tax=0
	df_tax_per=[]
	df_tax_gst=[]
	df_tax_total=[]
	if request.method == 'POST':
			
		form=create_sales_report(request.POST)
		if form.is_valid():
			
				
				
			create_sales_report_month=int(request.POST.get('create_sales_report_month'))
			create_sales_report_year=int(request.POST.get('create_sales_report_year'))
			sales=create_sales_final.objects.filter(sales_date__year=create_sales_report_year, sales_date__month=create_sales_report_month)
			for invo in sales:
				sale_date.append(invo.sales_date)
				sale_total.append(float(invo.sales_total))
				sale_total1.append(float(invo.sales_total))
				spe_disc.append(float(invo.sales_special_discount))
				payment_recieved.append(float(invo.sales_payment_received))
				total_balance=sum(sale_total)-sum(payment_recieved)
				sales_pro=create_sales_table.objects.filter(sales_invoice_no=invo.sale_invoice_ref)
				sales_prod=create_sales_table.objects.all()
				product_det=products.objects.all()

			
				
			taxe=taxes.objects.filter(sale_date__year=create_sales_report_year, sale_date__month=create_sales_report_month)
			for x in taxe:
				df_tax_per.append(x.tax_percent)
				df_tax_gst.append(round(float(x.total_tax_amount)/2,2))
				df_tax_total.append(x.total_tax_amount)
			df=pd.DataFrame(list(zip(df_tax_per,df_tax_gst,df_tax_total)),columns=['a','b','c'])
			df_1=df.groupby('a', as_index=False).agg({'b':'sum', 'c':'sum'})

			listss=df_1.values.tolist()
			
			for tt in taxe:
				taxu.append(float(tt.total_tax_amount))
				tota_tax=sum(taxu)
				tota_tax=round(tota_tax,2)
			for tp in taxe:
				pri_taxu.append(float(tp.price_tax_amount))
				tota_pri_tax=sum(pri_taxu)
				tota_pri_tax=round(tota_pri_tax,2)
			for da in taxe:
				day_date=da.sale_date
				days.append(day_date.day)
			days = list(dict.fromkeys(days))
			
			for tota in days:
				total=0
				total_ta=0

				tax=taxes.objects.filter(sale_date__year=create_sales_report_year, sale_date__month=create_sales_report_month,sale_date__day=tota)
				
				for tta in tax:
					total=float(total)+float(tta.total_tax_amount)
					total_ta=float(total_ta)+float(tta.price_tax_amount)
				dates.append(tta.sale_date)	
				
				taxu.append(total)
				pri_taxu.append(total_ta)
				sale_total=0	
				tot=sale_totals.objects.filter(sales_date__year=create_sales_report_year, sales_date__month=create_sales_report_month,sales_date__day=tota)
				
				for tott in tot:
					sale_total=float(sale_total)+float(tott.sales_totals)
					
					sale_total=round(sale_total,2)
				
				totu.append(sale_total)
				salee=create_sales_final.objects.filter(sales_date__year=create_sales_report_year, sales_date__month=create_sales_report_month,sales_date__day=tota)
				count=0
				for cc in salee:
					count=count+1
				counting.append(count)
		zipped2=zip(dates,counting,taxu,pri_taxu,totu)
		zipped=zip(dates,counting,taxu,pri_taxu,totu)
		# for tui in pri_taxu:

		# 	sum_tax=float(sum_tax)+float(tui)
		for g,h,i,j,k in zipped2:
			sum_tax=float(sum_tax)+float(j)
		

		single_tax=taxes.objects.all()		
			

			# else:
			# 	return HttpResponse(form.errors)
	store_info=store_details.objects.latest('id')
	form=create_sales_report()
	active_sidebar1=7

	return render(request,'reports/monthlyrepo.html',{'active_sidebar1':active_sidebar1,'form':form,'sales':sales,'zipped':zipped,'single_tax':single_tax,'taxe':listss,'tota_tax':tota_tax,'tota_pri_tax':tota_pri_tax,'count':count,\
		'spe_disc':sum(spe_disc),'payment_recieved':sum(payment_recieved),'total_balance':total_balance,'sales_totals':sum(sale_total1),'total_payable_tax':sum_tax,'store_info':store_info})
	

@login_required(login_url='/login')
def create_gst_reports(request):
	if request.method == 'POST':
		
		form=create_gst_report(request.POST)
		if form.is_valid():
			cre_gst_rpt=create_Gst_report_table(
				create_gst_report_month_and_year=form.cleaned_data['create_gst_report_month_and_year'],
				create_gst_report_category=form.cleaned_data['create_gst_report_category'],
				)
			cre_gst_rpt.save()
		else:
			return HttpResponse(form.errors)

	form=create_gst_report()
	active_sidebar2=7
	return render(request,'reports/create_gst_reports.html',{'active_sidebar2':active_sidebar2,'form':form})
