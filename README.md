# Dependency Risk Analyzer

A sophisticated machine learning-powered tool that analyzes Python package dependencies to identify security vulnerabilities and assess their risk levels. The Dependency Risk Analyzer combines CVE databases, GitHub repository metrics, and predictive machine learning models to provide comprehensive security insights.

## 🎯 Features

- **CVE Vulnerability Detection**: Automatically fetches and analyzes Common Vulnerabilities and Exposures (CVE) data for dependencies
- **GitHub Repository Analysis**: Gathers metrics including stars, open issues, and update frequency to assess project health
- **ML-Based Risk Scoring**: Uses a trained machine learning model to predict risk scores based on multiple security factors
- **Real-time Analysis**: Analyzes multiple dependencies simultaneously with instant risk assessment
- **Detailed Reports**: Provides comprehensive vulnerability details including CVSS scores and repository health metrics
- **Web Interface**: User-friendly dashboard for easy dependency analysis
- **RESTful API**: FastAPI backend for programmatic access

## 📊 How It Works

The analyzer evaluates dependencies using five key features:

1. **CVE Count**: Number of known vulnerabilities for the package
2. **Average CVSS Score**: Severity rating of vulnerabilities (0-10 scale)
3. **GitHub Stars**: Project popularity indicator
4. **Open Issues**: Maintenance indicator
5. **Last Updated Days**: Package recency metric

These features are processed through a trained machine learning model that outputs a **risk score (0-1)** and **status** (Low, Medium, High Risk).

## 🏗️ Project Structure

```
dependency-risk-analyzer/
├── backend/
│   ├── main.py                 # FastAPI application entry point
│   ├── cve_fetcher.py          # CVE data retrieval module
│   ├── github_analyzer.py      # GitHub metrics analyzer
│   ├── predictor.py            # ML prediction engine
│   ├── train_model.py          # Model training script
│   ├── generate_dataset.py     # Dataset generation utility
│   ├── suggestions.py          # Risk mitigation suggestions
│   ├── pypi_fetcher.py         # PyPI package information fetcher
│   ├── requirements.txt        # Python dependencies
│   ├── requirements_fixed.txt  # Pinned dependency versions
│   ├── risk_model.pkl          # Trained ML model (serialized)
│   ├── scaler.pkl              # Feature scaler (serialized)
│   └── training_data.csv       # Training dataset
│
├── frontend/
│   ├── index.html              # Main UI page
│   ├── script.js               # Frontend logic and API integration
│   └── style.css               # Styling and UI design
│
├── .gitignore                  # Git ignore rules
└── README.md                   # This file

```

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- pip (Python package manager)
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Backend Setup

   1. **Navigate to the backend directory**:
      ```bash
      cd backend
      ```

   2. **Install dependencies**:
      ```bash
      pip install -r requirements.txt
      ```

   3. **Set environment variables** (optional):
      Create a `.env` file in the backend directory if API keys are needed:
      ```bash
      # Example .env file
      GITHUB_TOKEN=your_github_token_here
      ```

   4. **Run the FastAPI server**:
      ```bash
      python main.py
      ```
      Or use Uvicorn directly:
      ```bash
      uvicorn main:app --reload
      ```

      The API will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to the frontend directory**:
   ```bash
   cd frontend
   ```

2. **Open in a web browser**:
   Simply open `index.html` in your preferred web browser, or serve it using a local server:
   ```bash
   # Using Python 3
   python -m http.server 8001
   
   # Or using Node.js http-server
   npx http-server
   ```

3. **Access the application**:
   Open `http://localhost:8001` (or appropriate port) in your browser

## 📖 Usage

### Via Web Interface

1. Open the frontend application in your browser
2. Enter package names (one per line or comma-separated)
3. Click "Analyze Dependencies"
4. Review the risk scores, vulnerability details, and recommendations

### Via REST API

**Analyze Dependencies**:

```bash
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{"dependencies": ["requests", "django", "flask"]}'
```

**Response Example**:
```json
{
  "dependencies": [
    {
      "package": "requests",
      "risk_score": 0.25,
      "status": "Low Risk",
      "details": {
        "stars": 52000,
        "open_issues": 45,
        "last_updated_days": 3,
        "cve_count": 2,
        "avg_cvss": 5.3
      }
    }
  ]
}
```

**Health Check**:
```bash
curl http://localhost:8000/
```

## 🔧 Backend Modules

### main.py
The core FastAPI application that:
- Defines REST API endpoints
- Orchestrates dependency analysis
- Integrates all analysis modules
- Handles CORS for frontend communication

### cve_fetcher.py
Retrieves CVE information for packages:
- Fetches vulnerability data from CVE databases
- Calculates average CVSS scores
- Returns count of known vulnerabilities

### github_analyzer.py
Analyzes GitHub repository metrics:
- Retrieves star counts
- Counts open issues
- Determines last update timestamp
- Assesses project activity level

### predictor.py
Executes ML-based risk prediction:
- Loads trained model and scaler
- Normalizes input features
- Generates risk scores and risk status
- Returns confidence predictions

### train_model.py
Model training utility:
- Trains the ML model on historical data
- Saves serialized model and scaler
- Optimizes feature importance

### generate_dataset.py
Dataset generation utility:
- Creates training datasets
- Aggregates feature data
- Formats data for model training

## 🤖 Machine Learning Model

- **Type**: Supervised Classification/Regression
- **Framework**: scikit-learn
- **Features**: 5 input features (CVE count, CVSS score, stars, open issues, last updated)
- **Output**: Risk score (0-1) and risk category
- **Training Data**: `training_data.csv`
- **Serialization**: joblib (`.pkl` files)

## 📦 Dependencies

### Core Framework
- **fastapi**: Modern web framework for building APIs
- **uvicorn**: ASGI server for running FastAPI
- **pydantic**: Data validation and serialization

### Data & ML
- **scikit-learn**: Machine learning library
- **pandas**: Data manipulation and analysis
- **joblib**: Model serialization

### Utilities
- **requests**: HTTP client for API calls
- **python-dotenv**: Environment variable management

## 🔐 Security Considerations

- CORS is enabled for all origins (configure for production)
- API calls to external services are made over HTTPS
- Input validation is performed on all dependencies
- Feature scaling prevents model bias

## 📊 Risk Score Interpretation

| Risk Score | Status | Recommendation |
|-----------|--------|-----------------|
| 0.0 - 0.3 | Low Risk | Safe to use; standard maintenance |
| 0.3 - 0.7 | Medium Risk | Monitor updates; consider alternatives |
| 0.7 - 1.0 | High Risk | Review urgently; update or replace |

## 🛠️ Development & Training

### Train a New Model

```bash
cd backend
python generate_dataset.py  # Generate training data
python train_model.py       # Train the model
```

This will update `risk_model.pkl` and `scaler.pkl` with the new trained model.

## 📝 API Documentation

Once the backend is running, access interactive API docs at:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🐛 Troubleshooting

### Backend won't start
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version: `python --version` (requires 3.8+)
- Verify port 8000 is not in use

### Frontend can't connect to API
- Ensure backend is running on `http://localhost:8000`
- Check browser console for CORS errors
- Verify firewall settings

### Model not loading
- Ensure `risk_model.pkl` and `scaler.pkl` exist in backend directory
- Run `train_model.py` to regenerate model files

## 📈 Performance

- Single dependency analysis: ~100-500ms
- Batch analysis (10 packages): ~1-5 seconds
- Memory footprint: ~50-100MB (with loaded model)

## 📄 License

This project is open source and available under the MIT License.

## 👤 Author

**aneeshj-05** - [GitHub Profile](https://github.com/aneeshj-05)

**AM0805** - [GitHub Profile](https://github.com/AM0805)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## 🚦 Roadmap

- [ ] Add support for JavaScript/Node.js packages
- [ ] Implement dependency graph analysis
- [ ] Add vulnerability patch recommendations
- [ ] Create CI/CD integration examples
- [ ] Support for Docker deployment
- [ ] Database integration for result history
- [ ] Advanced filtering and reporting

## ❓ FAQ

**Q: How often is CVE data updated?**
A: CVE data is fetched in real-time from external databases during each analysis.

**Q: Can I use this for private packages?**
A: Currently, the analyzer works best with public packages on PyPI and GitHub.

**Q: Is the model accuracy guaranteed?**
A: The model provides risk assessments based on available data. Always conduct your own security audits.

**Q: Can I integrate this into my CI/CD pipeline?**
A: Yes! Use the REST API to integrate dependency analysis into your build pipeline.

---

**Last Updated**: 2026-03-26
