# Galaxy Brain 🌌

**A unified, hermetic NLP development and deployment system**

Galaxy Brain transforms how you build, train, and deploy state-of-the-art NLP systems by combining the industrial strength of spaCy and the vast ecosystem of Hugging Face into a single, cohesive monorepo, orchestrated by a bulletproof build system.

## 🌟 The Galaxy Brain Difference

- **Blazing-Fast Setup**: Onboard with `uv venv && uv pip install -e .` in seconds
- **Bulletproof Builds**: Hermetic, reproducible builds with Bazel + meson-python 
- **Code, Data, and Models as One**: Version-locked Hugging Face models as build dependencies
- **Effortless Deployment**: Single command from source to production-ready containers
- **Hardware Acceleration Ready**: Optimized for accelerators like Cerebras WSE

## 🎯 What it does

Transforms raw customer support emails into structured, validated JSON with enterprise-grade reliability and deployment readiness.

**Input:** Free-form email text  
**Output:** Validated JSON with customer ID, product, sentiment, urgency, entities, summary, and next action

**Deployment:** Production-ready containers, ML pipelines, and API services

## 🚀 Quick Start

### 1. Galaxy Brain Setup (The New Way)

```bash
# Clone and setup
git clone <repo-url> && cd galaxy-brain
uv venv && uv pip install -e .

# Download models and setup Bazel (one-time setup)
uv run python tools/dev_scripts/dev_setup.py

# Verify everything works
bazel test //...
```

### 2. Choose Your Workflow

**🔥 Production API Service**
```bash
# Build and run the FastAPI service
bazel run //apps/api_service:fastapi_server

# Or build a container
bazel build //apps/api_service:api_service_container
```

**⚡ Batch Processing**
```bash
# Process emails in batch
bazel run //apps/batch_processor:batch_processor -- ml_pipelines/sample_emails.txt --summary

# Or use the legacy demo
bazel run //apps/batch_processor:demo
```

**🧪 ML Pipeline Development**
```bash
# Train a custom NER model
bazel run //ml_pipelines:train_ner_model -- --output ./models/custom_ner

# Evaluate sentiment models
bazel run //ml_pipelines:eval_sentiment_model -- --model distilbert-base-uncased
```
## 🏗️ Galaxy Brain Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Galaxy Brain 🌌                          │
├─────────────────┬─────────────────┬─────────────────────────┤
│   APPS/         │   PACKAGES/     │   ML_PIPELINES/         │
│                 │                 │                         │
│ ┌─────────────┐ │ ┌─────────────┐ │ ┌─────────────────────┐ │
│ │ API Service │ │ │ NLP Utils   │ │ │ Training Pipelines  │ │
│ │  FastAPI    │ │ │ spaCy+HF    │ │ │ Model Evaluation    │ │
│ │ Container   │ │ │ PydanticAI  │ │ │ Data Processing     │ │
│ └─────────────┘ │ └─────────────┘ │ └─────────────────────┘ │
│                 │                 │                         │
│ ┌─────────────┐ │ ┌─────────────┐ │        TOOLS/           │
│ │ Batch Proc  │ │ │Custom Models│ │ ┌─────────────────────┐ │
│ │ Large Scale │ │ │ Architectures│ │ │ Dev Scripts         │ │
│ │ Processing  │ │ │ Components  │ │ │ Model Downloads     │ │
│ └─────────────┘ │ └─────────────┘ │ │ Setup & Config      │ │
└─────────────────┴─────────────────┴─┴─────────────────────┴─┘
            ▲                               ▲
            │          Bazel Build Graph    │
            └─────────────────┬─────────────┘
                              ▼
      ┌───────────────────────────────────────────────┐
      │  Hermetic, Reproducible Dependencies:         │
      │  • Version-locked HF models & datasets        │
      │  • Containerized deployment targets           │
      │  • Unified Python + ML + Container ecosystem │ 
      └───────────────────────────────────────────────┘
```

## 📁 Galaxy Brain Monorepo Structure

```
/galaxy-brain/
├── MODULE.bazel              # Bazel workspace & external dependencies
├── pyproject.toml            # Python config, dev tools, uv settings
├── .bazelrc                  # Bazel configuration
├── apps/                     # Deployable applications
│   ├── api_service/          # FastAPI production service
│   │   ├── BUILD.bazel       # Container + API targets
│   │   └── src/api_server.py # FastAPI implementation
│   └── batch_processor/      # Large-scale processing
│       ├── BUILD.bazel       # Batch processing targets  
│       └── src/processor.py  # Batch implementation
├── packages/                 # Shared libraries and utilities
│   ├── nlp_utils/           # Core NLP functionality
│   │   ├── BUILD.bazel      # py_library targets
│   │   └── src/             # Models, extractors, agents
│   └── custom_models/       # Custom model architectures
├── ml_pipelines/            # Training and evaluation
│   ├── BUILD.bazel          # Training targets
│   ├── train_ner_model/     # NER training pipeline
│   └── eval_sentiment_model/# Evaluation scripts
├── tools/                   # Development tooling
│   └── dev_scripts/         # Setup, downloads, utils
└── bazel/                   # Custom Bazel rules
    └── hf_repository.bzl    # HuggingFace integration
```

## 🛠️ Galaxy Brain Usage Examples

### 🚀 Production Deployments

**Deploy API Service to Production**
```bash
# Build production container
bazel build //apps/api_service:api_service_container

# Load and run container
docker load < bazel-bin/apps/api_service/api_service_container.tar
docker run -p 8000:8000 galaxy-brain/api-service:latest
```

**Batch Processing at Scale**
```bash
# Process thousands of emails
bazel run //apps/batch_processor:batch_processor -- \
  large_dataset.txt --format json --output results.json
```

### 🧪 Development Workflows

**Interactive API Development**
```bash
# Run FastAPI with hot reload
uv run python apps/api_service/src/api_server.py
# Visit http://localhost:8000/docs for Swagger UI
```

**Model Experimentation**  
```bash
# Train custom NER model
bazel run //ml_pipelines:train_ner_model -- \
  --data custom_training.txt --iterations 200

# Evaluate multiple models
bazel run //ml_pipelines:eval_sentiment_model -- \
  --model cardiffnlp/twitter-roberta-base-sentiment-latest
```

### 📊 Programmatic Usage

```python
# Galaxy Brain library usage
from packages.nlp_utils.src.agent import TriageAgent

agent = TriageAgent()
ticket = await agent.process_email(email_text)
print(ticket.model_dump_json(indent=2))
```

## 📊 Sample Output

```json
{
  "customer_id": "C_SARAH_JOHNSON",
  "product": "Widget-X",
  "sentiment": "negative",
  "urgency": "high",
  "entities": [
    {
      "text": "Widget-X",
      "label": "PRODUCT",
      "start": 8,
      "end": 16,
      "confidence": 1.0
    }
  ],
  "summary": "Critical system outage affecting multiple customers",
  "next_action": "escalate_to_tier_2",
  "confidence_score": 0.89
}
```

## 🔧 Configuration

### Environment Variables

```bash
# Required for full LLM functionality
export OPENAI_API_KEY="your-api-key"

# Optional: Use different models
export PYDANTIC_AI_MODEL="gpt-4o-mini"
```

### Model Configuration

- **spaCy**: `en_core_web_trf` (transformer-based NER)
- **Sentiment**: `distilbert-base-uncased-finetuned-sst-2-english`
- **LLM**: `gpt-4o-mini` (configurable)

## 🎯 Galaxy Brain Advantages Over Traditional Approaches

| Traditional NLP Development | Galaxy Brain 🌌 |
|----------------------------|-----------------|
| ❌ Hours lost on environment setup | ✅ `uv venv && uv pip install -e .` (seconds) |
| ❌ Manual model version management | ✅ Version-locked HF models in MODULE.bazel |
| ❌ "Works on my machine" deployment issues | ✅ Hermetic builds guarantee reproducibility |
| ❌ Complex multi-step container builds | ✅ `bazel build //apps:container` (single command) |
| ❌ Fragile dependency chains | ✅ Dependency graph with automatic rebuilds |
| ❌ Manual CI/CD scripting | ✅ Bazel targets integrate with any CI system |
| ❌ Separate model serving infrastructure | ✅ Unified build → test → deploy pipeline |

## 📈 Performance Targets

| Metric | Galaxy Brain Target | Traditional | Notes |
|--------|-------------------|-------------|-------|
| Setup Time | **<30 seconds** | 2-4 hours | uv + Bazel optimization |
| Schema Validation | **≥99%** | Variable | Pydantic guarantees |
| Entity Precision | **>85%** | 60-80% | spaCy transformer model |
| Sentiment Accuracy | **>90%** | 70-85% | DistilBERT fine-tuned |
| Build Reproducibility | **100%** | <50% | Hermetic Bazel builds |
| Container Build Time | **<2 minutes** | 10-30 min | Layered caching |
| Deployment Consistency | **100%** | 60-80% | Single source of truth |

## 🛡️ Security Notes

- No PII is logged by default
- API keys are environment variables only
- Consider using local models for sensitive data

## 💡 Common Messages

### "Device set to use mps:0"
This message appears on Apple Silicon Macs (M1/M2/M3) and indicates that PyTorch is using **Metal Performance Shaders** for GPU acceleration. This is **good** - it means your models are running faster! 

To suppress this message, you can:
- Ignore it (recommended - it's just informational)
- Set `PYTORCH_ENABLE_MPS_FALLBACK=1` to force CPU usage
- Use `2>/dev/null` to redirect stderr: `python triage.py --demo 2>/dev/null`

## 🚀 Next Steps & Extensions

### 🎯 Production Enhancements
- **Multi-language Support**: Add language detection + multilingual models
- **Custom Fine-tuning**: Domain-specific model training pipelines  
- **Hardware Acceleration**: Cerebras WSE integration for faster inference
- **Auto-scaling**: Kubernetes deployments with HPA
- **Monitoring**: OpenTelemetry + Prometheus integration

### 🧠 ML/AI Features
- **Advanced Pipelines**: Multi-step reasoning chains
- **Model Ensemble**: Combine multiple model predictions
- **Active Learning**: Improve models from production data
- **A/B Testing**: Model comparison frameworks
- **Local LLM**: Replace OpenAI with Ollama/Llama

### 🔧 Development Experience
- **IDE Integration**: VS Code extensions for Bazel
- **Hot Reloading**: Development mode with file watching
- **Distributed Training**: Multi-GPU training targets
- **Model Registry**: Centralized model versioning
- **Automated Testing**: Property-based testing for ML

## 🎓 Galaxy Brain Learning Outcomes

This project demonstrates:
- **Modern Build Systems**: Bazel for reproducible, scalable builds
- **Hermetic Dependencies**: Eliminating "works on my machine" issues  
- **Container-Native Development**: Production-ready from day one
- **ML Engineering Best Practices**: Versioned models, automated pipelines
- **Unified Tooling**: Single workflow from development to deployment
- **Enterprise Architecture**: Monorepo patterns for large-scale NLP

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.

---

**🌌 Galaxy Brain: Where NLP meets Industrial Engineering**

*Built to demonstrate the future of unified, hermetic NLP development and deployment systems.*

## 📚 Additional Resources

- **[Galaxy Brain Concept Paper](galaxy-brain-concept.md)**: Deep dive into the vision and architecture
- **[Bazel Documentation](https://bazel.build/)**: Learn more about hermetic builds
- **[UV Documentation](https://docs.astral.sh/uv/)**: Fast Python package management
- **[spaCy](https://spacy.io/)**: Industrial-strength NLP
- **[Hugging Face](https://huggingface.co/)**: Transformer models and datasets
- **[PydanticAI](https://ai.pydantic.dev/)**: Schema-first LLM agents

*Transform your NLP workflow today. Stop fighting your tools and start building the future.* 🚀