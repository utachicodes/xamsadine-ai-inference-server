from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import torch
from transformers import WhisperForConditionalGeneration, WhisperTokenizer, WhisperProcessor, pipeline
from werkzeug.utils import secure_filename
import os, uuid
from waitress import serve
import json 

app = Flask(_name_)
CORS(app)  

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = '/tmp'  
app.config['OUTPUT_FOLDER'] = r"C:\Users\abdou\OneDrive\Desktop\Coding"  
app.config["ID_MAPPING_FILE"] = os.path.join(app.config['OUTPUT_FOLDER'], "id_mapping.json")
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'ogg', 'm4a'}


os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

class WhisperTranscriber:
    def _init_(self, model_id: str = "CAYTU/whosper-large-v2"):
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

    def transcribe_audio(self, audio_path: str) -> str:
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
            return result["text"]
        except Exception as e:
            print(f"Error during transcription: {e}")
            return None

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_id_mapping():
    """Get the mapping of IDs to filenames"""
    if os.path.exists(app.config["ID_MAPPING_FILE"]):
        try:
            with open(app.config["ID_MAPPING_FILE"], 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    return {}

def save_id_mapping(mapping):
    """Save the mapping of IDs to filenames"""
    with open(app.config["ID_MAPPING_FILE"], 'w') as f:
        json.dump(mapping, f, indent=2)

# Initialize the transcriber
transcriber = WhisperTranscriber()

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
        
    files = request.files.getlist('file')
    results = []
    last_id = None
    
    for file in files:
        if file and allowed_file(file.filename):
           
            original_filename = secure_filename(file.filename)
            base_filename = os.path.splitext(original_filename)[0]
            
            
            temp_uuid = uuid.uuid4()
            extension = original_filename.split(".")[-1]
            temp_filename = f"{temp_uuid}.{extension}"
            temp_filepath = os.path.join(app.config['UPLOAD_FOLDER'], temp_filename)
            
            
            id_str = str(uuid.uuid4())
            last_id = id_str
            
            
            output_filename = f"{base_filename}_{id_str[:8]}.txt"
            output_filepath = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
        
            
            file.save(temp_filepath)
            
            try:
                
                result = transcriber.transcribe_audio(temp_filepath)
                
                
                with open(output_filepath, 'w', encoding='utf-8') as f:
                    f.write(result)
                
                
                id_mapping = get_id_mapping()
                id_mapping[id_str] = {
                    "filename": output_filename,
                    "original_filename": original_filename
                }
                save_id_mapping(id_mapping)
                
                results.append({
                    'id': id_str,
                    'original_filename': original_filename,
                    'output_filename': output_filename
                })
            finally:
                
                try:
                    os.remove(temp_filepath)
                except:
                    pass
    
    
    if len(results) == 1:
        return jsonify({'id': last_id, 'filename': results[0]['output_filename']})
    else:
        return jsonify({'results': results})

@app.route('/transcription/<id_str>', methods=['GET'])
def retrieve_transcription(id_str):
    """Retrieves a transcription by its ID"""
    try:
        
        id_mapping = get_id_mapping()
        if id_str not in id_mapping:
            return jsonify({'error': 'Transcription ID not found'}), 404
        
        filename = id_mapping[id_str]["filename"]
        filepath = os.path.join(app.config['OUTPUT_FOLDER'], filename)
        
        
        with open(filepath, 'r', encoding='utf-8') as f:
            transcription_text = f.read()
        
        return jsonify({
            'id': id_str,
            'filename': filename,
            'original_filename': id_mapping[id_str]["original_filename"],
            'text': transcription_text
        })
    except Exception as e:
        return jsonify({'error': f'Error retrieving transcription: {str(e)}'}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'gpu_available': torch.cuda.is_available(),
        'gpu_name': torch.cuda.get_device_name(0) if torch.cuda.is_available() else None
    })

if _name_ == '_main_':
    port = int(os.environ.get('AIP_HTTP_PORT', 8080))
    serve(app, host='0.0.0.0', port=port)
