from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import sys
import re

def load_model():
    # Load model and tokenizer
    model_name = "tabularisai/robust-sentiment-analysis"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    return tokenizer, model

def analyze_interview_metrics(text):
    # Define keywords and patterns for different metrics
    metrics = {
        'motivation': {
            'positive': ['passionate', 'eager', 'driven', 'motivated', 'enthusiastic', 'excited', 'goal', 'achieve', 'improve', 'learn'],
            'negative': ['bored', 'unmotivated', 'tired', 'forced', 'reluctant']
        },
        'communication': {
            'positive': ['explain', 'communicate', 'articulate', 'present', 'discuss', 'share', 'collaborate'],
            'negative': ['unclear', 'confusing', 'hesitant', 'vague']
        },
        'experience': {
            'positive': ['led', 'managed', 'developed', 'created', 'implemented', 'achieved', 'succeeded'],
            'negative': ['failed', 'struggled', 'limited']
        },
        'teamwork': {
            'positive': ['team', 'collaborate', 'support', 'help', 'together', 'partnership'],
            'negative': ['alone', 'individual', 'conflict']
        }
    }
    
    results = {}
    text_lower = text.lower()
    
    for metric, keywords in metrics.items():
        pos_count = sum(text_lower.count(word) for word in keywords['positive'])
        neg_count = sum(text_lower.count(word) for word in keywords['negative'])
        
        total = pos_count + neg_count
        if total == 0:
            results[metric] = "Neutral"
        else:
            score = pos_count / (pos_count + neg_count)
            if score > 0.7:
                results[metric] = "Very Positive"
            elif score > 0.5:
                results[metric] = "Positive"
            elif score > 0.3:
                results[metric] = "Neutral"
            else:
                results[metric] = "Negative"
    
    return results

def predict_sentiment(text, tokenizer, model):
    inputs = tokenizer(text.lower(), return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    
    probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)
    predicted_class = torch.argmax(probabilities, dim=-1).item()
    
    sentiment_map = {0: "Very Negative", 1: "Negative", 2: "Neutral", 3: "Positive", 4: "Very Positive"}
    return sentiment_map[predicted_class]

def analyze_file(file_path):
    try:
        # Loading model
        print("Loading model...")
        tokenizer, model = load_model()
        
        # Reading file
        print(f"Reading file: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        
        # Analyzing sentiment
        print("Analyzing sentiment...")
        overall_sentiment = predict_sentiment(text, tokenizer, model)
        interview_metrics = analyze_interview_metrics(text)
        
        # Output results
        print("\nInterview Analysis Results:")
        print("-" * 50)
        print(f"Overall Sentiment: {overall_sentiment}")
        print("\nDetailed Metrics:")
        print(f"Motivation: {interview_metrics['motivation']}")
        print(f"Communication Skills: {interview_metrics['communication']}")
        print(f"Experience Level: {interview_metrics['experience']}")
        print(f"Teamwork Orientation: {interview_metrics['teamwork']}")
        
    except FileNotFoundError:
        print(f"Error: File not found '{file_path}'")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python sentiment_analyzer.py <file_path>")
        print("Example: python sentiment_analyzer.py text.txt")
    else:
        file_path = sys.argv[1]
        analyze_file(file_path) 
