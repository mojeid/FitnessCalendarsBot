""" Module responsible data from custom PerfectGym app HTTP responses. """


def get_class_id_from_perfectgym_classess_list(json_response, class_details):
    """ Parses JSON data and returns Class ID for specific class date/time and trainer."""
    class_id = None
    classes_per_hour = ((json_response['CalendarData'])[0])['ClassesPerHour']

    for entry in classes_per_hour:
        # Classes calendar in Response is organised first by hour then by day.
        if class_details['startTime'] not in entry['Hour']:
            continue
        for crossfit_classes in entry['ClassesPerDay']:
            # skip empty results lists
            if not crossfit_classes:
                continue
            # skip classes that does not match date or trainer requested
            if class_details['date'] not in crossfit_classes[0]['StartTime'] or class_details[
                'trainer'] != crossfit_classes[0]['Trainer']:
                continue

            class_id = crossfit_classes[0]['Id']

    return class_id

