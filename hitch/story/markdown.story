Markdown:
  about: |
    Convert chunks of orgmode text into markdown using .body.markdown.
  given:
    files:
      markdown.org: |
        * Note title

        Text with /emphasis/ and *bold* and a [[link][https://www.google]].

        + Bullet one
        + Bullet two

      markdown.jinja2: |
        {{ root.at("Note title").body.markdown }}


  steps:
  - orji:
      cmd: markdown.org markdown.jinja2
      output: |2

        Text with /emphasis/ and *bold* and a [link](https://www.google).

        * Bullet one
        * Bullet two
