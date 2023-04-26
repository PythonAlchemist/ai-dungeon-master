from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
from datasets import load_dataset
import torch
import sounddevice as sd
import io

processor = SpeechT5Processor.from_pretrained("microsoft/speecht5_tts")
model = SpeechT5ForTextToSpeech.from_pretrained("microsoft/speecht5_tts")
vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan")

# load xvector containing speaker's voice characteristics from a dataset
embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")


class Voice:
    """Voice class to generate speech from text."""

    def __init__(self, mute: bool = False):
        """Initialize the voice class by assigning the speaker's voice characteristics and attaching to an incoming text stream"""
        self.speaker_embeddings = torch.tensor(
            embeddings_dataset[5000]["xvector"]
        ).unsqueeze(0)
        self.mute = mute

    def speak(self, text):
        inputs = processor(text=text, return_tensors="pt")
        speech = model.generate_speech(
            inputs["input_ids"], self.speaker_embeddings, vocoder=vocoder
        )
        sd.play(speech.numpy(), samplerate=16000, blocking=True)
