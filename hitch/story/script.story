Run templated script to send email:
  about: |
    Simple org mode file used with simple template.
  given:
    files:
      org/simple.org: |
        * TODO An email I want to send :email:

        ** email

        billg@microsoft.com

        ** body

        Windows sucks.

        * TODO Wash car :morning:

        Car wash.

        * TODO File taxes :evening:

        File taxes for wife too.

        * DONE Watch TV
      org/simple2.org: |
        * Another note

        * Another irrelevant note.
      orun/email.sh: |
        echo {{ note.at("body").body.oneline }}
        cat {{ note.at("email").body.tempfile() }}

        echo
        echo {{ orgfile }}
        echo {{ tmp }}
        echo {{ out }}
  steps:
  - orji:
      env:
        ORJITMP: ./tmp
      cmd: run org orun
      output: |
        Windows sucks.
        billg@microsoft.com
        /gen/working/org/simple.org
        /gen/working/11111.tmp
        /gen/working



Run templated failing script:
  based on: Run templated script to send email
  about: |
    Simple org mode file used with simple template.
  given:
    files:
      orun/email.sh: |
        echo {{ note.at("body").body.oneline }}
        cat {{ note.at("email").body.tempfile() }}
        exit 1
  replacement steps:
  - orji:
      cmd: run org orun
      error: yes
      output: |
        Windows sucks.
        billg@microsoft.com

        ERROR running email.sh in /gen/working/11111.tmp


