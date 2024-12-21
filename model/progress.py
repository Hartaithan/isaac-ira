class Progress:
    def __init__(self, title: str):
        self.title = title

    def start(self):
        print(f"\n{self.title}: starting")

    def update(self, description, progress, total, length=20):
        filled = int(length * progress // total)
        bars = '█' * filled + '-' * (length - filled)
        percent = f"{100 * progress / total:.1f}%"
        print(f'\r\033[K[{bars}] {percent} {description}',
              end='\r', flush=True)

    def complete(self, error=None):
        if not error:
            print(f"\r\033[K{self.title}: complete", end='\r')
        else:
            print(f"\r\033[K{self.title}: error, {error}", end='\r')
        print()
