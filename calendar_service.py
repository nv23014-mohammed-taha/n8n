from googleapiclient.discovery import build

def book_appointment(name, date, time):

    event = {
        'summary': f'Dental Appointment - {name}',
        'start': {'dateTime': f'{date}T{time}:00'},
        'end': {'dateTime': f'{date}T{time}:30'}
    }

    service = build('calendar', 'v3', credentials=YOUR_CREDS)
    service.events().insert(calendarId='primary', body=event).execute()

    return "Appointment booked successfully"
