class ListCommandConfig(object):
    def __init__(self, args):
        self.glob = args['<glob>'] if args['<glob>'] else '*.md'
        self.format = (
            args['--format']
            if args['--format']
            else '\u001b[30m- \u001b[0m\u001b[01m[$status]\u001b[0m \u001b[31m$file:$line\u001b[0m $title \u001b[0m\u001b[34m$tags\u001b[0m \u001b[31m$date\u001b[0m'
        )
        self.all = True if args['--all'] else False
        self.statuses = args['--statuses'].replace('=', '').split(',') if args['--statuses'] else []
        self.tags = args['--tags'].replace('=', '').split(',') if args['--tags'] else []
        self.today = True if args['--today'] else False
        self.upcoming = True if args['--upcoming'] else False
        self.sort_by = args['--sort_by'].replace('=', '').split(',') if args['--sort_by'] else None

    def __str__(self):
        return str(self.__class__) + ': ' + str(self.__dict__)

