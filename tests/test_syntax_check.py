#!/usr/bin/env python3
"""Syntax check for enhanced functionality without running actual imports."""

import ast
import os
import sys

def check_python_syntax(filepath):
    """Check if Python file has valid syntax."""
    try:
        with open(filepath, 'r') as f:
            source = f.read()
        
        # Parse the AST to check syntax
        ast.parse(source, filename=filepath)
        return True, None
    except SyntaxError as e:
        return False, str(e)
    except Exception as e:
        return False, str(e)

def main():
    """Check syntax of all Python files in the package."""
    src_dir = os.path.join(os.path.dirname(__file__), '..', 'src', 'document_reader')
    
    files_to_check = [
        os.path.join(src_dir, '__init__.py'),
        os.path.join(src_dir, 'ocr_reader.py'),
        os.path.join(src_dir, 'image_enhancer.py')
    ]
    
    print("Checking Python syntax for enhanced functionality...")
    print("=" * 60)
    
    all_good = True
    for filepath in files_to_check:
        filename = os.path.basename(filepath)
        if os.path.exists(filepath):
            is_valid, error = check_python_syntax(filepath)
            if is_valid:
                print(f"✓ {filename}: Syntax OK")
            else:
                print(f"✗ {filename}: Syntax Error - {error}")
                all_good = False
        else:
            print(f"✗ {filename}: File not found")
            all_good = False
    
    print("=" * 60)
    if all_good:
        print("✓ All files have valid Python syntax!")
        print("✓ Enhanced functionality is syntactically correct")
        
        # Check that key classes and functions exist in the AST
        print("\nChecking for key enhancements...")
        
        # Check ImageEnhancer class
        enhancer_file = os.path.join(src_dir, 'image_enhancer.py')
        with open(enhancer_file, 'r') as f:
            enhancer_ast = ast.parse(f.read())
        
        classes = [node.name for node in ast.walk(enhancer_ast) if isinstance(node, ast.ClassDef)]
        if 'ImageEnhancer' in classes:
            print("✓ ImageEnhancer class found")
        else:
            print("✗ ImageEnhancer class not found")
            all_good = False
            
        # Check OCRReader enhancements
        ocr_file = os.path.join(src_dir, 'ocr_reader.py')
        with open(ocr_file, 'r') as f:
            ocr_ast = ast.parse(f.read())
        
        functions = [node.name for node in ast.walk(ocr_ast) if isinstance(node, ast.FunctionDef)]
        expected_functions = ['process_pdf_with_confidence', 'assess_document_quality', 
                             'get_low_confidence_regions', 'extract_text_with_confidence']
        
        missing_functions = [f for f in expected_functions if f not in functions]
        if not missing_functions:
            print("✓ All new OCRReader methods found")
        else:
            print(f"✗ Missing functions: {missing_functions}")
            all_good = False
            
        return 0 if all_good else 1
    else:
        print("✗ Syntax errors found!")
        return 1

if __name__ == "__main__":
    sys.exit(main())