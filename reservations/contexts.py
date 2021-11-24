import datetime


def reservations(request):

    context = {
        'reservations_start_date': datetime.date.today().strftime("%Y-%m-%d"),
    }

    return context
