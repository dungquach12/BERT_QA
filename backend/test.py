import torch
from simpletransformers.question_answering import QuestionAnsweringModel
from transformers import BertTokenizer

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

saved_model_dir = "backend/BERT"

model = QuestionAnsweringModel("bert", saved_model_dir, use_cuda=False)
tokenizer = BertTokenizer.from_pretrained("bert-base-cased")

@app.route('/answer', methods=['POST'])
def predict_answer():
    data = request.get_json()
    if 'passage' not in data or 'question' not in data:
        return jsonify({'error': 'Missing passage or question'}), 400
    
    context = data['passage']
    question = data['question']

    # Tokenize the input
    inputs = tokenizer(question, context, return_tensors="pt")

    outputs = model.model(**inputs)

    if outputs.start_logits.shape[1] == 0 or outputs.end_logits.shape[1] == 0:
        return jsonify({'error': 'Model output is invalid'}), 500

    # Decode the predicted answer
    answer_start = torch.argmax(outputs.start_logits)
    answer_end = torch.argmax(outputs.end_logits) + 1
    answer = tokenizer.decode(inputs["input_ids"][0][answer_start:answer_end])

    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(debug=True)