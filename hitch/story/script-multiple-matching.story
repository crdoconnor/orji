Templated with more than one note:
  about: |
    Simple org mode file used with simple template.
  given:
    files:
      tmp/_:
      org/simple.org: |
        * TODO Wash car :email-reminder:

        Car wash.

        * DONE Watch TV
      org/simple2.org: |
        * Another note

        * TODO File taxes :email-reminder:

        File taxes for wife too.

        * Another irrelevant note.
      orun/email-reminder.sh: |
        echo {{ note.body.oneline }}
  variations:
    Fails:
      steps:
      - orji:
          env:
            ORJITMP: ./tmp
          cmd: run org orun
          error: yes
          output: |
            Multiple matching notes use --multiple to run all of them

            /gen/working/org/simple.org: 0: Wash car
            /gen/working/org/simple2.org: 1: File taxes

    Run multiple:
      steps:
      - orji:
          env:
            ORJITMP: ./tmp
          cmd: run --multiple org orun
          error: yes
          output: |
            Car wash.
            File taxes for wife too.
