# ROI Automation Dashboard

A web application that analyzes CSV data to automatically generate insights, visualizations, and formatted reports. The application processes location-by-month data to identify trends, provide recommendations, and create executive-ready presentations.

## Features

- **Data Upload**: Easily upload CSV files containing location-by-month data
- **Automated Analysis**: Identify positive and negative trends at location, region, and overall levels
- **Data Visualizations**: Generate charts and graphs to visualize key metrics
- **Executive Summary**: Create concise PDF reports with key findings
- **Detailed Presentation**: Generate PowerPoint slides for comprehensive data exploration

## Getting Started

### Prerequisites

- Python 3.8+
- Virtual environment (recommended)

### Installation

1. Clone this repository
2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Create a `.env` file with your configuration:
   ```
   SECRET_KEY=your-secret-key-here
   OPENAI_API_KEY=your-openai-api-key-here
   ```

### Running the Application

```
python app.py
```

The application will be available at http://localhost:5000

## CSV Format Requirements

The application expects CSV files with the following characteristics:

- Data at the location-by-month level
- Columns for location, region, and date information
- Metric columns as defined in the application

## Development

This project uses:

- Flask for the backend API
- Vanilla JavaScript for the frontend
- OpenAI API for data insights generation
- Pandas for data processing
- Matplotlib/Seaborn for visualization generation
- ReportLab and python-pptx for document generation

## License

This project is licensed under the MIT License - see the LICENSE file for details.
