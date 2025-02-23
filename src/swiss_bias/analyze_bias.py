from transformers import pipeline

# Initialize the bias type classifier pipeline
bias_type_classifier = pipeline(
    "text-classification", 
    model="cirimus/modernbert-large-bias-type-classifier"
)

# Example text for bias detection
text = "The article is extremely biased and manipulative."

# Get bias classification results
results = bias_type_classifier(text)
print(results)
