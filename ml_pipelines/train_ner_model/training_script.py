"""Training script for custom NER model fine-tuning."""

import spacy
from spacy.training import Example
from spacy.util import minibatch, compounding
import random
from pathlib import Path
import sys
import os

# Add packages to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../../packages/nlp_utils/src'))

from models import Entity

class NERTrainer:
    """Trainer for custom NER models using spaCy."""
    
    def __init__(self, base_model: str = "en_core_web_trf"):
        self.nlp = spacy.load(base_model)
        
        # Add NER pipe if not present
        if "ner" not in self.nlp.pipe_names:
            ner = self.nlp.add_pipe("ner", last=True)
        else:
            ner = self.nlp.get_pipe("ner")
        
        self.ner = ner
    
    def prepare_training_data(self, data_file: str):
        """
        Prepare training data from annotated text.
        Expected format: Each line contains text and entities in JSON format.
        """
        training_data = []
        
        # For demo purposes, create some synthetic training data
        # In production, this would load from annotated datasets
        synthetic_data = [
            ("I'm having trouble with Widget-X login", {"entities": [(25, 33, "PRODUCT")]}),
            ("The SuperApp is crashing constantly", {"entities": [(4, 12, "PRODUCT")]}),
            ("My account dashboard won't load", {"entities": [(3, 10, "FEATURE"), (11, 20, "FEATURE")]}),
            ("Widget-Pro subscription expired", {"entities": [(0, 10, "PRODUCT")]}),
            ("CloudSync backup failed again", {"entities": [(0, 9, "PRODUCT")]}),
        ]
        
        for text, annotations in synthetic_data:
            doc = self.nlp.make_doc(text)
            example = Example.from_dict(doc, annotations)
            training_data.append(example)
        
        return training_data
    
    def add_labels(self, training_data):
        """Add entity labels to the NER component."""
        for example in training_data:
            for ent in example.reference.ents:
                self.ner.add_label(ent.label_)
    
    def train(self, training_data, n_iter: int = 100, batch_size: int = 4):
        """Train the NER model."""
        # Add labels
        self.add_labels(training_data)
        
        # Disable other pipes during training
        pipe_exceptions = ["ner", "trf_wordpiecer", "trf_tok2vec"]
        unaffected_pipes = [pipe for pipe in self.nlp.pipe_names if pipe not in pipe_exceptions]
        
        with self.nlp.disable_pipes(*unaffected_pipes):
            # Initialize the model
            optimizer = self.nlp.resume_training()
            
            for iteration in range(n_iter):
                random.shuffle(training_data)
                losses = {}
                
                # Create minibatches
                batches = minibatch(training_data, size=compounding(4.0, 32.0, 1.001))
                
                for batch in batches:
                    self.nlp.update(batch, drop=0.35, losses=losses, sgd=optimizer)
                
                if iteration % 10 == 0:
                    print(f"Iteration {iteration}, Losses: {losses}")
    
    def evaluate(self, test_data):
        """Evaluate the trained model."""
        scores = self.nlp.evaluate(test_data)
        return scores
    
    def save_model(self, output_dir: str):
        """Save the trained model."""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        self.nlp.to_disk(output_path)
        print(f"Model saved to {output_path}")

def main():
    """Main training function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Train custom NER model")
    parser.add_argument("--data", help="Training data file")
    parser.add_argument("--output", default="./trained_model", help="Output directory for model")
    parser.add_argument("--iterations", type=int, default=100, help="Number of training iterations")
    parser.add_argument("--base_model", default="en_core_web_trf", help="Base spaCy model")
    
    args = parser.parse_args()
    
    print("🚀 Starting Galaxy Brain NER training pipeline...")
    
    trainer = NERTrainer(args.base_model)
    
    # Prepare training data
    print("📊 Preparing training data...")
    training_data = trainer.prepare_training_data(args.data)
    
    print(f"📈 Training on {len(training_data)} examples...")
    trainer.train(training_data, n_iter=args.iterations)
    
    # Evaluate
    print("🔍 Evaluating model...")
    scores = trainer.evaluate(training_data[:2])  # Quick eval on subset
    print(f"Evaluation scores: {scores}")
    
    # Save model
    trainer.save_model(args.output)
    
    print("✅ Training completed!")

if __name__ == "__main__":
    main()