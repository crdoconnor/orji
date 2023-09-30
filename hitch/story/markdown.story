Convert chunks of orgmode text into markdown:
  docs: markdown
  about: |
    Convert chunks of orgmode text into markdown using .body.markdown.
  given:
    files:
      markdown.org: |
        * Note title

        Text with /emphasis/ and *bold* and a [[https://www.google][link]].

        + Bullet one
        + Bullet two

      markdown.jinja2: |
        {{ root.at("Note title").body.markdown }}


  steps:
  - orji:
      cmd: cat markdown.org markdown.jinja2
      output: |
        Text with /emphasis/ and *bold* and a [link](https://www.google).

        * Bullet one
        * Bullet two
