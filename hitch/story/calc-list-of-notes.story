Calculation producing a list of notes:
  docs: calculation-list-of-notes
  about: |
    Run calculations from within a note to generate a list of subnotes.
  given:
    files:
      calc.py: |
        from datetime import datetime

      org/calc.org: |
        * Reminders >
        = [
            CalcNote(state="TODO", title="Replace water filter", scheduled=datetime(2025, month, 2))
            for month in range(2, 13)
          ]
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
        * Reminders >
        = [
            CalcNote(state="TODO", title="Replace water filter", scheduled=datetime(2025, month, 2))
            for month in range(2, 13)
          ]
        ** TODO Replace water filter
        SCHEDULED: <2025-02-02 Sun>
        ** TODO Replace water filter
        SCHEDULED: <2025-03-02 Sun>
        ** TODO Replace water filter
        SCHEDULED: <2025-04-02 Wed>
        ** TODO Replace water filter
        SCHEDULED: <2025-05-02 Fri>
        ** TODO Replace water filter
        SCHEDULED: <2025-06-02 Mon>
        ** TODO Replace water filter
        SCHEDULED: <2025-07-02 Wed>
        ** TODO Replace water filter
        SCHEDULED: <2025-08-02 Sat>
        ** TODO Replace water filter
        SCHEDULED: <2025-09-02 Tue>
        ** TODO Replace water filter
        SCHEDULED: <2025-10-02 Thu>
        ** TODO Replace water filter
        SCHEDULED: <2025-11-02 Sun>
        ** TODO Replace water filter
        SCHEDULED: <2025-12-02 Tue>




