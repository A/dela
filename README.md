## Dela

![dela](./imgs/dela.png)

### Installation

```
pip install --user dela
```

### Help

```
CLI to list todos in markdown files, like Obsidian Vaults.

Usage:
  dela -h | --help
  dela --version
  dela list [-v] [--all] [--today] [--done] [--someday] [--status=<symbol>] [--tag=<string>...] [--sort_by=<key>] [--format=<string>] [<glob>]

Options:
  -h --help                     Show this screen
  -v --verbose                  Enable logging
  -a --all                      Show all todos including closed ones
  -t --today                    Show only tasks due today or earlier
  -d --done                     Show only done tasks
  --someday                     Show someday tasks marked with [s] status
  -s --status=<symbol>          Filter by status (x, a, c, ~, ...)
  -tag=<string>                 Filter by tag (#work, #home, etc)
  --sort_by=<key>               Sort by given key
  --format=<string>             Format result with given template string.
  --version                     Show version.


Template example:
    dela list --format='- [$status] $file: $title'

    NOTE: Unicode colors are supported


Template and Sorting Keys:
    - message
    - date
    - status
    - tags
    - file

    NOTE: In templates variable should be prefixed with the $ sign.


Supported todo examples:
    - [ ] Todo
    - [x] Done
    - [n] Next
    - [~] Pending
    - [c] Cancelled
    - [ ] 20230703 Todo with a date. If it's the day, `dela list -t` will list this guy
    - [ ] Todo with tags #tagone #tagtwo
    - [ ] 23330101 Future task will be hidden until the day become
```
