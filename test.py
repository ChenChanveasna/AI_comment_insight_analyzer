import os
# We suppress logging to keep the CLI clean
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

from transformers import pipeline

def run_poc():
    print("--- AI Comment Insight Analyzer: PoC Mode ---")
    print("Loading model... (This may take a minute on the first run)")
    
    # Initialize the specific social-media tuned model
    try:
        analyzer = pipeline(
            "sentiment-analysis", 
            model="finiteautomata/bertweet-base-sentiment-analysis"
        )
    except Exception as e:
        print(f"Error loading model: {e}")
        return

    print("\nModel Loaded! Type 'quit' to exit.")
    
    while True:
        user_input = input("\nEnter a sentence to analyze: ").strip()
        
        if user_input.lower() == 'quit':
            break
        
        if not user_input:
            continue

        # Perform analysis
        # Note: BERTweet uses POS (Positive), NEU (Neutral), NEG (Negative)
        result = analyzer(user_input)[0]
        
        label = result['label']
        confidence = result['score']

        # Formatting for the user
        color = ""
        if label == "POS":
            display_label = "✅ POSITIVE"
        elif label == "NEG":
            display_label = "❌ NEGATIVE"
        else:
            display_label = "😐 NEUTRAL"

        print(f"Result: {display_label} ({confidence:.2%})")

if __name__ == "__main__":
    run_poc()