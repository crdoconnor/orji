Insert vcf file:
  docs: insert-vcf
  about: |
    Insert ical file as a note.
  given:
    files:
      org/contacts.org: |
        * From phone
      direct.jinja2: |
        {{ contacts.to_org() }}
      fromphone.vcf: |
        BEGIN:VCARD
        VERSION:4.0
        FN:John
        N:John;;;;
        TEL:+447777777774
        END:VCARD
        BEGIN:VCARD
        VERSION:4.0
        FN:Peter
        N:Peter;;;;
        TEL:+447777777775
        END:VCARD

  variations:
    Insert contacts in header:
      steps:
      - orji:
          env:
            ORJITMP: ./tmp
          cmd: in direct.jinja2 under org/contacts.org//0 contacts:vcf:fromphone.vcf
          output: |
            Written note(s) successfully

      - file contents:
          filename: org/contacts.org
          contents: |
            * From phone
            ** John
            tel:+447777777774
            ** Peter
            tel:+447777777775
