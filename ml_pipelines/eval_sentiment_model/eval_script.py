"""Evaluation script for sentiment analysis models."""

from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import json
from pathlib import Path
import sys
import os

# Add packages to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../../packages/nlp_utils/src'))

from extractors import SentimentAnalyzer

class SentimentEvaluator:
    """Evaluates sentiment analysis models on test datasets."""
    
    def __init__(self, model_name: str = "distilbert-base-uncased-finetuned-sst-2-english"):
        self.model_name = model_name
        self.analyzer = SentimentAnalyzer(model_name)
        
    def load_test_data(self, data_file: str = None):
        """Load test data for evaluation."""
        # Create synthetic test data for demonstration
        # In production, this would load from labeled test sets
        test_data = [
            ("I love this product! It works perfectly.", "positive"),
            ("This is terrible, completely broken.", "negative"),
            ("It's okay, nothing special.", "neutral"),
            ("Amazing customer service, very helpful!", "positive"),
            ("Worst experience ever, very disappointed.", "negative"),
            ("The app crashes constantly, so frustrating!", "negative"),
            ("Decent features but could be better.", "neutral"),
            ("Excellent quality and fast delivery!", "positive"),
            ("Not working as expected, needs improvement.", "negative"),
            ("Pretty good overall, satisfied with purchase.", "positive"),
        ]
        
        if data_file and Path(data_file).exists():
            # Try to load from file if provided
            try:
                with open(data_file, 'r') as f:
                    lines = f.readlines()
                    # Assume format: text\tlabel
                    file_data = []
                    for line in lines:
                        if '\t' in line:
                            text, label = line.strip().split('\t', 1)
                            file_data.append((text, label))
                    if file_data:
                        test_data = file_data
            except Exception as e:
                print(f"Error loading data file: {e}, using synthetic data")
        
        return test_data
    
    def evaluate_model(self, test_data):
        """Evaluate the sentiment model on test data."""
        predictions = []
        true_labels = []
        detailed_results = []
        
        print(f"🔍 Evaluating {self.model_name} on {len(test_data)} examples...")
        
        for text, true_label in test_data:
            # Get prediction
            result = self.analyzer.analyze_sentiment(text)
            predicted_label = result['sentiment']
            confidence = result['confidence']
            
            predictions.append(predicted_label)
            true_labels.append(true_label)
            
            detailed_results.append({
                'text': text,
                'true_label': true_label,
                'predicted_label': predicted_label,
                'confidence': confidence,
                'correct': predicted_label == true_label
            })
        
        return predictions, true_labels, detailed_results
    
    def compute_metrics(self, predictions, true_labels):
        """Compute evaluation metrics."""
        # Handle label mapping for evaluation
        label_map = {'positive': 1, 'negative': 0, 'neutral': 0.5}
        
        # Convert to numeric for sklearn if needed
        pred_numeric = [label_map.get(p, 0.5) for p in predictions]
        true_numeric = [label_map.get(t, 0.5) for t in true_labels]
        
        accuracy = accuracy_score(true_labels, predictions)
        
        # Get unique labels for classification report
        unique_labels = list(set(true_labels + predictions))
        
        try:
            report = classification_report(
                true_labels, 
                predictions, 
                labels=unique_labels,
                output_dict=True
            )
        except:
            report = {"accuracy": accuracy}
        
        return {
            'accuracy': accuracy,
            'classification_report': report
        }
    
    def print_results(self, metrics, detailed_results):
        """Print evaluation results."""
        print("\n" + "="*50)
        print("📊 SENTIMENT ANALYSIS EVALUATION RESULTS")
        print("="*50)
        
        print(f"Model: {self.model_name}")
        print(f"Accuracy: {metrics['accuracy']:.3f}")
        
        if 'classification_report' in metrics and isinstance(metrics['classification_report'], dict):
            print("\nPer-class metrics:")
            for label, scores in metrics['classification_report'].items():
                if isinstance(scores, dict) and 'precision' in scores:
                    print(f"  {label}: P={scores['precision']:.3f}, R={scores['recall']:.3f}, F1={scores['f1-score']:.3f}")
        
        print(f"\nDetailed Results (first 5):")
        for i, result in enumerate(detailed_results[:5]):
            status = "✅" if result['correct'] else "❌"
            print(f"{status} {result['text'][:50]}...")
            print(f"   True: {result['true_label']}, Pred: {result['predicted_label']} (conf: {result['confidence']:.3f})")
            print()
    
    def save_results(self, metrics, detailed_results, output_file: str):
        """Save evaluation results to file."""
        results = {
            'model_name': self.model_name,
            'metrics': metrics,
            'detailed_results': detailed_results,
            'summary': {
                'total_examples': len(detailed_results),
                'correct_predictions': sum(1 for r in detailed_results if r['correct']),
                'accuracy': metrics['accuracy']
            }
        }
        
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"💾 Results saved to {output_file}")

def main():
    """Main evaluation function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Evaluate sentiment analysis model")
    parser.add_argument("--model", default="distilbert-base-uncased-finetuned-sst-2-english", 
                       help="Hugging Face model name")
    parser.add_argument("--data", help="Test data file (optional)")
    parser.add_argument("--output", help="Output file for results")
    
    args = parser.parse_args()
    
    print("🚀 Starting Galaxy Brain sentiment evaluation pipeline...")
    
    evaluator = SentimentEvaluator(args.model)
    
    # Load test data
    test_data = evaluator.load_test_data(args.data)
    
    # Run evaluation
    predictions, true_labels, detailed_results = evaluator.evaluate_model(test_data)
    
    # Compute metrics
    metrics = evaluator.compute_metrics(predictions, true_labels)
    
    # Print results
    evaluator.print_results(metrics, detailed_results)
    
    # Save results if requested
    if args.output:
        evaluator.save_results(metrics, detailed_results, args.output)
    
    print("✅ Evaluation completed!")

if __name__ == "__main__":
    main()