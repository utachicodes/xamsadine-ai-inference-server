# app.py
from flask import Flask, request, jsonify
import torch
from transformers import WhisperForConditionalGeneration, WhisperTokenizer, WhisperProcessor, pipeline
from werkzeug.utils import secure_filename
import os
from waitress import serve

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = '/tmp'
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'ogg', 'm4a'}

class WhosperTranscriber:
    def __init__(self, model_id: str = "CAYTU/whosper-large-v2"):
        self.model_id = model_id
        self.torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
        self.model = None
        self.tokenizer = None
        self.processor = None
        self.pipe = None
        self.load_model()
        self.configure_pipeline()

    def load_model(self):
        self.model = WhisperForConditionalGeneration.from_pretrained(
            self.model_id,
            device_map="auto",
            use_cache=True,
            attention_dropout=0.1,
            dropout=0.1,
            token=os.environ.get('HF_TOKEN')
        )
        self.model.config.suppress_tokens = []
        self.model.config.no_repeat_ngram_size = 3
        self.model.config.early_stopping = True
        self.model.config.max_length = 448
        self.model.config.num_beams = 5
        self.tokenizer = WhisperTokenizer.from_pretrained(self.model_id, token=os.environ.get('HF_TOKEN'))
        self.processor = WhisperProcessor.from_pretrained(self.model_id, token=os.environ.get('HF_TOKEN'))

    def configure_pipeline(self):
        self.pipe = pipeline(
            "automatic-speech-recognition",
            model=self.model,
            tokenizer=self.tokenizer,
            feature_extractor=self.processor.feature_extractor,
            torch_dtype=self.torch_dtype,
            chunk_length_s=10,
            stride_length_s=1,
            return_timestamps=False,
            batch_size=4
        )

    def transcribe_audio(self, audio_path: str) -> dict:
        try:
            result = self.pipe(
                audio_path,
                generate_kwargs={
                    "temperature": 0.0,
                    "do_sample": False,
                    "num_beams": 5,
                    "length_penalty": 1.0,
                    "repetition_penalty": 1.2
                }
            )
            return result
        except Exception as e:
            print(f"Error during transcription: {e}")
            return None

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

transcriber = WhosperTranscriber()

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
        
    files = request.files.getlist('file')
    results = []
    
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            try:
                result = transcriber.transcribe_audio(filepath)
                results.append({
                    'filename': filename,
                    'transcription': result
                })
            finally:
                if os.path.exists(filepath):
                    os.remove(filepath)
    
    return jsonify({'predictions': results})

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'gpu_available': torch.cuda.is_available(),
        'gpu_name': torch.cuda.get_device_name(0) if torch.cuda.is_available() else None
    })

if __name__ == '__main__':
    port = int(os.environ.get('AIP_HTTP_PORT', 8080))
    serve(app, host='0.0.0.0', port=port)
