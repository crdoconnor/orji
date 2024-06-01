Insert ical file:
  docs: insert
  about: |
    Insert ical file as a note.
  given:
    files:
      org/calendar.org: |
        * Meetings
        * Birthdays
      direct.jinja2: |
        {{ event.to_org() }}
      calendar.vcf: |
        BEGIN:VCALENDAR
        PRODID:-//xyz Corp//NONSGML PDA Calendar Version 1.0//EN
        VERSION:2.0
        BEGIN:VEVENT
        DTSTAMP:19960704T120000Z
        UID:uid1@example.com
        ORGANIZER:mailto:jsmith@example.com
        DTSTART:19960918T143000Z
        DTEND:19960920T220000Z
        STATUS:CONFIRMED
        CATEGORIES:CONFERENCE
        SUMMARY:Networld+Interop Conference
        DESCRIPTION:Networld+Interop Conference
          and Exhibit\nAtlanta World Congress Center\n
         Atlanta\, Georgia
        END:VEVENT
        END:VCALENDAR

  variations:
    Add within meetings header:
      steps:
      - orji:
          env:
            ORJITMP: ./tmp
          cmd: in direct.jinja2 under org/calendar.org//0 event:ical:calendar.vcf
          output: |
            Written note(s) successfully

      - file contents:
          filename: org/calendar.org
          contents: |
            * Meetings
            ** Networld+Interop Conference
            SCHEDULED: <1996-07-04 Thu 12:00>
            Networld+Interop Conference and Exhibit
            Atlanta World Congress Center
            Atlanta, Georgia
            * Birthdays
