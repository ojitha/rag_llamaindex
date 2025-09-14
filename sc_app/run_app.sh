#!/bin/bash
# Script to run the Science Community Chat App

echo "Starting Science Community Chat App..."
echo "Make sure your OPENAI_API_KEY is set:"
echo "export OPENAI_API_KEY='your-api-key-here'"
echo ""
echo "The app will be available at: http://localhost:8501"
echo ""

# Run the streamlit app using uv
cd "$(dirname "$0")"
uv run streamlit run app.py