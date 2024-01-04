from pathlib import Path
from orgmunge import ORG_TIME_FORMAT
import icalendar
import jinja2

DEFAULT = jinja2.Template(
    """\
{% for event in events %}* {{ event.summary }}
SCHEDULED: <{{ event.scheduled }}>

{{ event.description }}
{% endfor %}"""
)


class Event:
    def __init__(self, ievent):
        self._ievent = ievent

    @property
    def summary(self):
        return self._ievent.get("SUMMARY")

    @property
    def description(self):
        return self._ievent.get("DESCRIPTION")

    @property
    def scheduled(self):
        return (
            self._ievent.get("DTSTAMP")
            .from_ical(self._ievent.get("DTSTAMP"))
            .strftime(ORG_TIME_FORMAT)
        )


class ICal:
    def __init__(self, icalfile):
        self._icalfile = icalfile
        self._icaltext = Path(icalfile).read_text()
        self._ical = icalendar.Calendar.from_ical(self._icaltext)
        self._events = [
            Event(ievent)
            for ievent in self._ical.walk()
            if ievent.get("SUMMARY") is not None
        ]

    def to_org(self):
        return DEFAULT.render(events=self._events)
