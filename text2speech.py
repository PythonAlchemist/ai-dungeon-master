from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
from datasets import load_dataset
import torch
import sounddevice as sd

processor = SpeechT5Processor.from_pretrained("microsoft/speecht5_tts")
model = SpeechT5ForTextToSpeech.from_pretrained("microsoft/speecht5_tts")
vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan")

# load xvector containing speaker's voice characteristics from a dataset
embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")

class Voice:

    def __init__(self):

        self.speaker_embeddings = torch.tensor(embeddings_dataset[5000]["xvector"]).unsqueeze(0)

    def speak(self, text):

        # split text into sentences
        sentences = text.split(".")

        # process text
        for sent in sentences:
            
            inputs = processor(text=sent, return_tensors="pt")
            speech = model.generate_speech(inputs["input_ids"], self.speaker_embeddings, vocoder=vocoder)
            sd.play(speech.numpy(), samplerate=16000, blocking=True)


if __name__ == "__main__":

    voice = Voice()
    voice.speak("Hello everyone. My name is Matthew Mercer, voice actor and Dungeon Master for Critical Role and welcome to the first episode of the new series, Critical Role: The Legend of Vox Machina.")

