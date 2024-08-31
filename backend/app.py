import torch
from simpletransformers.question_answering import QuestionAnsweringModel
from transformers import BertTokenizer

saved_model_dir = "/content/drive/MyDrive/[HTK] Data cho đồ án cuối kỳ/Model BERT/"
model = QuestionAnsweringModel("bert", saved_model_dir)
tokenizer = BertTokenizer.from_pretrained("bert-base-cased")

def predict_answer(context: str, question: str, model) -> str:

    # Tokenize the input
    inputs = tokenizer(question, context, return_tensors="pt")

    # Generate predictions
    outputs = model.model(**inputs)

    # Decode the predicted answer
    answer_start = torch.argmax(outputs.start_logits)
    answer_end = torch.argmax(outputs.end_logits) + 1
    answer = tokenizer.decode(inputs["input_ids"][0][answer_start:answer_end])

    return answer

def main():
    print('Give context: ');
    context = input();
    print('Give question: ');
    question = input();
    print(predict_answer(context, question, model));

main()