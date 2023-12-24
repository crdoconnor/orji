---
title: Templated with more than one note
---
# Templated with more than one note


With script mode, you can "orji run" with a directory of templated scripts
and a directory or org files.

It will look through all of them for a TODO note with a tag matching a templated script.

You can use this to trigger templated bash scripts which can execute
pre-defined tasks from notes.

This example runs a bash script to send an email.

With --multiple then multiple matching scripts will be run.





org/simple.org
```org/simple.org
* TODO Wash car :email-reminder:

Car wash.

* DONE Watch TV

```


org/simple2.org
```org/simple2.org
* Another note

* TODO File taxes :email-reminder:

File taxes for wife too.

* Another irrelevant note.

```


orun/email-reminder.sh
```orun/email-reminder.sh
echo {{ note.body.oneline }}

```



