class TextStream:
    def __init__(self):
        self.data = []
        self.observers = []

    def register_observer(self, observer):
        self.observers.append(observer)

    def notify_observers(self):
        for observer in self.observers:
            observer.update(self)

    def append(self, text):
        self.data.append(text)
        self.notify_observers()

        # print formatted text
        print(f"Streams: {text}")


class StreamObserver:
    def update(self, stream):
        raise NotImplementedError


class VoiceObserver(StreamObserver):
    def __init__(self, voice):
        self.voice = voice

    def update(self, stream):
        text = stream.data[-1]  # Get the latest appended text
        if not self.voice.mute:
            self.voice.speak(text)
