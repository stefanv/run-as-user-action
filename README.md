# run-as-user-action

This actions runs one or more commands as a given user, in their shell
environment.

While it is easy to run user commands via `sudo`, it is *not* easy to
spawn an interactive user shell, i.e. one that executes `~/.shellrc`.

This action is mostly useful for testing tools that operate within the
user shell environment.
