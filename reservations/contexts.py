from datetime import date, datetime


def reservations(request):
    availability = request.session.get('availability', {})
    date_format = "%Y-%m-%d"
    duration = None

    if not availability == {}:
        duration = datetime.strptime(
            availability['end'], date_format) - datetime.strptime(availability['start'], date_format)
        duration = duration.days

    context = {
        'reservations_start_date': date.today().strftime("%Y-%m-%d"),
        'reservations_availability': availability,
        'reservations_availability_duration': duration,
    }

    return context
