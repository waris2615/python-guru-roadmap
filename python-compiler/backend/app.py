"""Python Compiler Backend - Flask API"""
from flask import Flask, request, jsonify
import subprocess
import tempfile
import os
import time

app = Flask(__name__)

# Security: timeout for code execution
TIMEOUT = 10

@app.route('/compile', methods=['POST'])
def compile():
    data = request.json
    code = data.get('code', '')
    
    if not code.strip():
        return jsonify({'output': '', 'error': 'No code provided'})
    
    # Create temp file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(code)
        temp_file = f.name
    
    try:
        # Run with timeout
        result = subprocess.run(
            ['python3', temp_file],
            capture_output=True,
            text=True,
            timeout=TIMEOUT
        )
        
        output = result.stdout
        error = result.stderr
        
        return jsonify({
            'output': output,
            'error': error,
            'success': result.returncode == 0
        })
    
    except subprocess.TimeoutExpired:
        return jsonify({
            'output': '',
            'error': 'Execution timed out (10s limit)',
            'success': False
        })
    
    except Exception as e:
        return jsonify({
            'output': '',
            'error': str(e),
            'success': False
        })
    
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)