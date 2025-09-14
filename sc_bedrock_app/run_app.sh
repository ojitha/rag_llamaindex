#!/bin/bash
# Script to run the Science Community Chat App - Bedrock Edition

echo "Starting Science Community Chat App (AWS Bedrock)..."
echo "Make sure your AWS credentials are configured:"
echo "  - AWS CLI: aws configure"
echo "  - Environment: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION"
echo ""
echo "The app will be available at: http://localhost:8501"
echo ""

# Run the streamlit app using uv
cd "$(dirname "$0")"
uv run streamlit run app.py