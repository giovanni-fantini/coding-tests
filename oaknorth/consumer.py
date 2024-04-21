from datetime import datetime

# { 'total' => { '1000' => 5, '2000' => 6 } }
def consume_invoices(invoices):
    output = {}
    total_invoices = {}
    unpaid_invoices = {}
    overdue_invoices = {}
    monthly_paid_invoices = {str(x): {} for x in range(1, 12)}
    
    for invoice in invoices:
        organisation_id = invoice['organisation_id']

        total_invoices[organisation_id] = total_invoices.get(organisation_id, 0) + 1

        if invoice['status'] == 'UNPAID':
            unpaid_invoices[organisation_id] = unpaid_invoices.get(organisation_id, 0) + 1

            due_date = datetime.strptime(invoice['due_date'], "%Y-%m-%d")
            if due_date.date() < datetime.now().date():
                overdue_invoices[organisation_id] = overdue_invoices.get(organisation_id, 0) + 1
        else:
            paid_date = datetime.strptime(invoice['paid_date'], "%Y-%m-%d")
            month = str(paid_date.month)

            if organisation_id in monthly_paid_invoices[month]:
                monthly_paid_invoices[month][organisation_id] += 1
            else:
                monthly_paid_invoices[month][organisation_id] = 1

    output['total'] = total_invoices
    output['unpaid'] = unpaid_invoices
    output['overdue'] = unpaid_invoices
    output['paid_per_month'] = monthly_paid_invoices

    return output