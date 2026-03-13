Date calculation:
  docs: date-calculation
  about: |
    Run date calculations from within a note and see the results appear within the note.
  variations:
    Using dates:
      given:
        files:
          calc.py: |
            from datetime import timedelta
          org/calc.org: |
            * Date moved to New York
            SCHEDULED: <2025-01-01 Wed>
            * Date moved to Philadelphia
            SCHEDULED: <2025-12-31 Wed>
            * Days lived in New York = ?
            = (date_moved_to_philadelphia.sched - date_moved_to_new_york.sched).days
            * Eight weeks after moving to New York = ?
            sched = date_moved_to_new_york.sched + timedelta(weeks=8)
      steps:
      - orji:
          env:
            ORJITMP: ./tmp
          cmd: calc --module calc.py org/calc.org
          output: |
            Written note(s) successfully

      - file contents:
          filename: org/calc.org
          contents: |
            * Date moved to New York
            SCHEDULED: <2025-01-01 Wed>
            * Date moved to Philadelphia
            SCHEDULED: <2025-12-31 Wed>
            * Days lived in New York = 364
            = (date_moved_to_philadelphia.sched - date_moved_to_new_york.sched).days
            * Eight weeks after moving to New York = ?
            SCHEDULED: <2025-02-26 Wed>
            sched = date_moved_to_new_york.sched + timedelta(weeks=8)
