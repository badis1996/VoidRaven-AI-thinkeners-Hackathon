from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import sys
import json
import re

def load_model():
    # Load model and tokenizer
    model_name = "tabularisai/robust-sentiment-analysis"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    return tokenizer, model

def analyze_response_relevance(question, answer):
    # Convert to lower case for comparison
    question_lower = question.lower()
    answer_lower = answer.lower()
    
    # Extract key terms from question
    question_words = set(re.findall(r'\w+', question_lower))
    answer_words = set(re.findall(r'\w+', answer_lower))
    
    # Calculate word overlap
    common_words = question_words.intersection(answer_words)
    relevance_score = len(common_words) / len(question_words) if question_words else 0
    
    # Determine relevance level
    if relevance_score > 0.5:
        return "High"
    elif relevance_score > 0.3:
        return "Moderate"
    else:
        return "Low"

def analyze_response_quality(answer):
    # Define indicators for response quality
    metrics = {
        'engagement': {
            'positive': ['because', 'therefore', 'specifically', 'example', 'instance', 'experience'],
            'negative': ['maybe', 'guess', 'not sure', "don't know"]
        },
        'completeness': {
            'positive': ['additionally', 'furthermore', 'moreover', 'also', 'detailed'],
            'negative': ['short', 'brief', 'quick']
        }
    }
    
    results = {}
    answer_lower = answer.lower()
    
    for metric, keywords in metrics.items():
        pos_count = sum(answer_lower.count(word) for word in keywords['positive'])
        neg_count = sum(answer_lower.count(word) for word in keywords['negative'])
        
        total = pos_count + neg_count
        if total == 0:
            results[metric] = "Neutral"
        else:
            score = pos_count / (pos_count + neg_count)
            if score > 0.7:
                results[metric] = "Very Good"
            elif score > 0.5:
                results[metric] = "Good"
            else:
                results[metric] = "Needs Improvement"
    
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
        
        # Reading JSON file
        print(f"Reading file: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            print(f"File content length: {len(content)} characters")
            try:
                qa_pairs = json.loads(content)
                print(f"Number of QA pairs: {len(qa_pairs)}")
            except json.JSONDecodeError as e:
                print(f"JSON Decode Error: {str(e)}")
                print("First 200 characters of file content:")
                print(content[:200])
                return
        
        if not isinstance(qa_pairs, list):
            print(f"Error: Expected a list of QA pairs, but got {type(qa_pairs)}")
            return
            
        if len(qa_pairs) == 0:
            print("Error: No QA pairs found in the file")
            return
        
        print("\nAnalyzing Q&A pairs...")
        print("-" * 50)
        
        for i, qa_pair in enumerate(qa_pairs, 1):
            if not isinstance(qa_pair, dict):
                print(f"Error: QA pair #{i} is not a dictionary")
                continue
                
            if 'AI' not in qa_pair or ('user' not in qa_pair and 'User' not in qa_pair):
                print(f"Error: QA pair #{i} missing 'AI' or 'User/user' key")
                print(f"Keys found: {qa_pair.keys()}")
                continue
                
            question = qa_pair['AI']
            answer = qa_pair.get('user', qa_pair.get('User', ''))
            
            if not question or not answer:
                print(f"Error: Empty question or answer in pair #{i}")
                continue
            
            print(f"\nQ&A Pair #{i}")
            print(f"AI Question: {question[:100]}...")
            print(f"User Answer: {answer[:100]}...")
            
            # Analyze sentiment
            sentiment = predict_sentiment(answer, tokenizer, model)
            
            # Analyze relevance
            relevance = analyze_response_relevance(question, answer)
            
            # Analyze response quality
            quality = analyze_response_quality(answer)
            
            print("\nAnalysis Results:")
            print(f"Response Sentiment: {sentiment}")
            print(f"Question Relevance: {relevance}")
            print(f"Response Engagement: {quality['engagement']}")
            print(f"Response Completeness: {quality['completeness']}")
            print("-" * 50)
        
    except FileNotFoundError:
        print(f"Error: File not found '{file_path}'")
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python sentiment_analyzer.py <file_path>")
        print("Example: python sentiment_analyzer.py qa_pairs.json")
    else:
        file_path = sys.argv[1]
        analyze_file(file_path) 
