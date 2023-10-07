Run templated script to send email:
  about: |
    Simple org mode file used with simple template.
  given:
    files:
      org/simple.org: |
        * TODO A normal note :selfemail:

        Send this note as an email to my personal email account.

        * TODO Wash car :morning:

        Car wash.

        * TODO File taxes :evening:

        File taxes for wife too.

        * DONE Watch TV
      org/simple2.org: |
        * Another note

        * Another irrelevant note.
      orun/selfemail.sh: |
        cat {{ notebody }}
  steps:
  - orji:
      cmd: run org orun
      output: |2

        Send this note as an email to my personal email account.
