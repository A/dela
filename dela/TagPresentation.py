class TagPresentation:
    def present(self, todos):
        tags = []
        for todo in todos:
            tags += todo.tags

        tags = set(tags)


        for tag in tags:
            print(tag)
