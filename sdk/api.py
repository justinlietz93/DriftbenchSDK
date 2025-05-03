"""
DriftBench SDK API Entry Point

Exposes HTTP endpoints for health checks and LLM response filtering.
Uses Flask and Gunicorn.
"""

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint.

    Returns:
        Response: A JSON response indicating the service is healthy.
    """
    return jsonify({"status": "healthy"}), 200

@app.route("/filter", methods=["POST"])
def filter_response():
    """Filter LLM response endpoint.

    Accepts a JSON payload with 'prompt' and 'response' keys.
    Currently returns a stub response.

    Returns:
        Response: A JSON response indicating the filter status (stub).
    """
    # TODO: Implement the actual filtering logic using the orchestrator
    # data = request.get_json()
    # prompt = data.get("prompt")
    # response_text = data.get("response")
    # result = orchestrator.process_response(prompt, response_text)
    # return jsonify(result)

    return jsonify({
        "status": "ok",
        "message": "TODO: Implement filter logic in orchestrator.py",
        "original_response": request.get_json().get("response", "") if request.is_json else "",
        "filtered_response": None,
        "issues": [],
        "confidence": 1.0
    }), 200

# Note: Gunicorn will be used to run the app in production (see Dockerfile)
if __name__ == "__main__":
    # For local development testing
    app.run(host="0.0.0.0", port=8000, debug=True)

