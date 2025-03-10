import os
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    jsonify,
    send_file,
)
import pandas as pd
from dotenv import load_dotenv
from data_processor import DataProcessor
from openai_analyzer import OpenAIAnalyzer
from pdf_generator import PDFGenerator

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-key-for-development")
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB max file size
app.config["ALLOWED_EXTENSIONS"] = {"csv"}
app.config["REPORTS_FOLDER"] = "reports"

# Create uploads and reports directories if they don't exist
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
os.makedirs(app.config["REPORTS_FOLDER"], exist_ok=True)

# Store the current uploaded file path
current_file_path = None


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]
    )


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze_data():
    global current_file_path

    if not current_file_path or not os.path.exists(current_file_path):
        return (
            jsonify(
                {
                    "success": False,
                    "error": "No file has been uploaded or the file was removed.",
                }
            ),
            400,
        )

    try:
        # Process the metric data
        dp = DataProcessor(current_file_path)
        customer_dict, region_dict = dp.process_file()

        # Initialize the AI analyzer
        openai_analyzer = OpenAIAnalyzer()

        # Multi-source data collection - First source: Meeting notes
        success_meeting, meeting_insights = openai_analyzer.extract_meeting_insights()
        if not success_meeting:
            meeting_insights = "Meeting insights data unavailable. Proceeding with available data sources."

        # Multi-source data collection - Second source: Becker's healthcare news
        success_beckers, beckers_insights = openai_analyzer.extract_beckers_insights()
        if not success_beckers:
            beckers_insights = "Becker's healthcare news unavailable. Proceeding with available data sources."

        # AI synthesis of all data sources into comprehensive insights
        success, insights = openai_analyzer.generate_insights(
            (customer_dict, region_dict)
        )

        # Generate executive summary PDF with synthesized information
        success, pdf_content = openai_analyzer.generate_pdf_content(
            (customer_dict, region_dict)
        )

        # Create the downloadable executive summary
        pdf_generator = PDFGenerator(app.config["REPORTS_FOLDER"])
        success, pdf_path = pdf_generator.generate_pdf_from_markdown(
            pdf_content, "executive_summary.pdf"
        )
        pdf_filename = os.path.basename(pdf_path)

        return jsonify(
            {
                "success": True,
                "insights": insights,
                "meeting_insights": meeting_insights,
                "beckers_insights": beckers_insights,
                "pdf_path": pdf_filename,
            }
        )

    except Exception as e:
        import traceback

        error_details = traceback.format_exc()
        print(f"Error during analysis: {str(e)}\n{error_details}")
        return (
            jsonify({"success": False, "error": f"Error during analysis: {str(e)}"}),
            500,
        )


@app.route("/sample_csv")
def sample_csv():
    """Provide a sample CSV file for users to test the application."""
    sample_file_path = os.path.join(
        app.root_path, "static", "samples", "sample_data.csv"
    )

    if not os.path.exists(sample_file_path):
        flash("Sample file not found")
        return redirect(url_for("index"))

    return send_file(
        sample_file_path, as_attachment=True, download_name="sample_data.csv"
    )


@app.route("/use_sample_data", methods=["POST"])
def use_sample_data():
    global current_file_path

    # Get the customer ID from the request (not used, but included for demo purposes)
    data = request.json
    customer_id = data.get("customer_id", "")

    # Always use the sample data file regardless of customer selected
    sample_file_path = os.path.join(
        app.root_path, "static", "samples", "sample_data.csv"
    )

    if not os.path.exists(sample_file_path):
        return jsonify({"success": False, "error": "Sample data file not found"}), 404

    # Save the path for later analysis
    current_file_path = sample_file_path

    try:
        # Read the sample data file
        df = pd.read_csv(sample_file_path)

        # For demo purposes, we'll add a customer name to the filename
        customer_mapping = {
            "customer1": "Sacred Heart Hospital",
        }

        customer_name = customer_mapping.get(customer_id, "Sample Customer")
        filename = f"{customer_name} - Data.csv"

        return jsonify(
            {
                "success": True,
                "filename": filename,
                "rows": len(df),
                "columns": len(df.columns),
                "column_names": df.columns.tolist(),
            }
        )
    except Exception as e:
        return (
            jsonify(
                {"success": False, "error": f"Error processing sample data: {str(e)}"}
            ),
            400,
        )


@app.route("/download/<filename>")
def download_file(filename):
    """Download a generated report file."""
    try:
        file_path = os.path.join(app.config["REPORTS_FOLDER"], filename)
        if not os.path.exists(file_path):
            return jsonify({"error": "File not found"}), 404

        return send_file(file_path, as_attachment=True, download_name=filename)
    except Exception as e:
        return jsonify({"error": f"Error downloading file: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True)
