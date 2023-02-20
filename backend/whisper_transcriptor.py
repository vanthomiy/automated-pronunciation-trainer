import whisper


class WhisperTranscriptor:
    def __init__(self, model_name="base.en", file_name="output.mp3"):
        self.model_name = model_name
        self.model = whisper.load_model(self.model_name)
        self.file_name = file_name

    def transcript(self):
        """
        Transcribe the wav file by the whisper model
        :return:
        """
        result = self.model.transcribe(self.file_name)
        # os.remove(self.file_name)
        return result["text"]

    def spectogram(self):
        """
        Create array of the wav file to return to the frontend
        :return:
        """
        pass



    @staticmethod
    def get_models():
        return whisper.available_models()
