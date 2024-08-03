from django.shortcuts import render, get_object_or_404, redirect
from .models import Bill, BillItem, Product
from decimal import Decimal

def product_selection(request):
    if request.method == 'POST':
        # selected_products = request.POST.getlist('products')
        # quantities = []
        # for product_id in selected_products:
        #     quantity = request.POST.get(f'quantities_{product_id}', 1)
        #     quantities.append(quantity)
        include_tax = request.POST.get('include_tax') == 'on'
        return redirect('create_bill', include_tax=include_tax)
    else:
        return render(request, 'product_selection.html')

import logging

logger = logging.getLogger(__name__)

from django.db import transaction
@transaction.atomic
def create_bill(request, include_tax):
    inc=include_tax
    if request.method == 'POST':
        try:
            customer_details = request.POST.get('customer_details')
            gst_number = request.POST.get('gst_number')
            hsn_code = request.POST.get('hsn_code')
            include_tax = include_tax == 'True'
            
            bill = Bill.objects.create(
                customer_details=customer_details,
                gst_number=gst_number,
                hsn_code=hsn_code,
                include_tax=include_tax
            )
            
            total_amount = Decimal('0.00')
            productnames = request.POST.getlist('productname[]')
            descriptions = request.POST.getlist('description[]')
            huid = request.POST.getlist('huid[]')
            prices = request.POST.getlist('price[]')
            quantities = request.POST.getlist('quantity[]')
            gross_weights = request.POST.getlist('gross_weight[]')
            stone_weights = request.POST.getlist('stone_weight[]')
            net_weights = request.POST.getlist('net_weight[]')
            ornament_values = request.POST.getlist('ornament_value[]')
            value_additions = request.POST.getlist('value_addition[]')
            stone_charges = request.POST.getlist('stone_charge[]')
            # propics = request.FILES.getlist('propic[]')
            
            for i in range(len(productnames)):
                try:
                    quantity = int(quantities[i])
                    if quantity <= 0:
                        raise ValueError("Quantity must be positive")
                    
                    product = Product.objects.create(
                        name=productnames[i],
                        price=Decimal(prices[i]),
                        # pro_pic=propics[i] if i < len(propics) else None,
                        description=descriptions[i]
                    )
                    logger.info(f"Created Product: {product.name}")
                    
                    ornament_value = Decimal(ornament_values[i])
                    value_addition = Decimal(value_additions[i])
                    stone_charge = Decimal(stone_charges[i])
                    
                    item_amount = (ornament_value + value_addition + stone_charge) 
                    print(item_amount)
                    total_amount += item_amount
                    
                    BillItem.objects.create(
                        bill=bill,
                        product=product,
                        quantity=quantity,
                        gross_weight=Decimal(gross_weights[i]),
                        stone_weight=Decimal(stone_weights[i]),
                        net_weight=Decimal(net_weights[i]),
                        ornament_value=ornament_value,
                        value_addition=value_addition,
                        stone_charge=stone_charge,
                        huid=huid[i]
                    )
                    logger.info(f"Created BillItem for Product: {product.name}, Quantity: {quantity}")
                except Exception as e:
                    logger.error(f"Error creating Product or BillItem at index {i}: {e}")
                    raise
            
            bill.total_amount = total_amount
            bill.save()
            logger.info(f"Created Bill with ID: {bill.id} and Total Amount: {bill.total_amount}")
            print('tax',include_tax)
            return redirect('print_bill', bill_id=bill.id, include_tax=include_tax)
        except Exception as e:
            logger.error(f"Error creating bill: {e}")
            return render(request, 'create_bill.html', {'include_tax': include_tax, 'error': str(e)})
    else:
        print('kk',inc)
        return render(request, 'create_bill.html', {'include_tax': include_tax == 'yes','inc':inc})
def print_bill(request, bill_id,include_tax):
    bill = get_object_or_404(Bill, id=bill_id)
    bill_items = BillItem.objects.filter(bill=bill)
    include_tax = include_tax == 'True' 

    
    
    total_amount = Decimal('0.00')
    for item in bill_items:
        item.amount = (item.ornament_value + item.value_addition + item.stone_charge)
        total_amount += item.amount

    if include_tax:
        sgst_rate = Decimal('0.015')
        cgst_rate = Decimal('0.015')
        sgst = total_amount * sgst_rate
        cgst = total_amount * cgst_rate
        gross_amount = total_amount + sgst + cgst
    else:
        sgst = cgst = Decimal('0.00')
        gross_amount = total_amount

    return render(request, 'print_bill.html', {
        'bill': bill,

        'bill_items': bill_items,
        'total_amount': total_amount,
        'sgst': sgst,
        'cgst': cgst,
        'gross_amount': gross_amount,
        'include_tax': include_tax
    })
    
def search_bill(request):
    query = request.GET.get('q')
    bills = Bill.objects.filter(id__icontains=query,include_tax=True) if query else Bill.objects.all(include_tax=True)
    return render(request, 'search_bill.html', {'bills': bills, 'query': query})


