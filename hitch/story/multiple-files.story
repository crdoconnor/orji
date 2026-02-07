Multiple files - grabbing phone numbers from contact notes:
  docs: multiple-files
  about: |
    Output a standard (VCF) contact file containing all of
    the contacts in multiple org files.
  given:
    files:
      friends.org: |
        * TODO Book restaurant

        * John :contact:

        tel:+447777777771

        * Friends

        ** Fred :contact:

        tel:+447777777772

        ** James :contact:

        tel:+447777777773

        * Holiday to Germany
        SCHEDULED: <2024-04-15 Mon>

      work.org: |
        * TODO Finish off report

        * John :contact:

        tel:+447777777774

        * Friends

        ** Fred :contact:

        tel:+447777777775

        ** James :contact:

        tel:+447777777776

      vcf.jinja2: |
        {%- for note in orgfiles.walk() -%}
        {%- if "contact" in note.tags -%}
        BEGIN:VCARD
        VERSION:4.0
        FN:{{ note.name }}
        N:{{ note.name }};;;;
        TEL:{{ note.links.tel }}
        END:VCARD
        {% endif -%}
        {% endfor -%}


  steps:
  - orji:
      cmd: out . vcf.jinja2
      output: |+
        BEGIN:VCARD
        VERSION:4.0
        FN:John
        N:John;;;;
        TEL:+447777777771
        END:VCARD
        BEGIN:VCARD
        VERSION:4.0
        FN:Fred
        N:Fred;;;;
        TEL:+447777777772
        END:VCARD
        BEGIN:VCARD
        VERSION:4.0
        FN:James
        N:James;;;;
        TEL:+447777777773
        END:VCARD
        BEGIN:VCARD
        VERSION:4.0
        FN:John
        N:John;;;;
        TEL:+447777777774
        END:VCARD
        BEGIN:VCARD
        VERSION:4.0
        FN:Fred
        N:Fred;;;;
        TEL:+447777777775
        END:VCARD
        BEGIN:VCARD
        VERSION:4.0
        FN:James
        N:James;;;;
        TEL:+447777777776
        END:VCARD

...
