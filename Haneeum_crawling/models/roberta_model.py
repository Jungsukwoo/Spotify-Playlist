from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F

# 로딩할 사전 학습된 모델 (커스텀 모델로 교체 가능)
MODEL_NAME = "mrm8488/roberta-fake-news"

# 클래스 수: 5단계 분류 [0%, 25%, 50%, 75%, 100%]
CLASS_LABELS = {
    0: (0, "완전 허위"),
    1: (25, "허위 다수"),
    2: (50, "경계 필요"),
    3: (75, "신뢰 가능"),
    4: (100, "완전 사실")
}

# 모델 및 토크나이저 불러오기
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

def predict_fact_score(article: str):
    inputs = tokenizer(article, return_tensors="pt", truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
        probs = F.softmax(outputs.logits, dim=-1)
        pred_class = torch.argmax(probs).item()
    
    score, label = CLASS_LABELS.get(pred_class, (50, "경계 필요"))
    return {
        "model": "RoBERTa",
        "score": score,
        "label": label,
        "probabilities": probs.squeeze().tolist()
    }

# 테스트용 실행
if __name__ == "__main__":
    test_article = "정부는 올해 7월까지 추경 예산의 70%를 집행하겠다고 발표했다."
    result = predict_fact_score(test_article)
    print(result)