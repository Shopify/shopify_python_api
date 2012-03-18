#!/usr/bin/env python
"""shopify_api.py wrapper script for running it the source directory"""

import sys
import os.path

# Use the development rather than installed version
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(project_root, 'lib'))

execfile(os.path.join(project_root, 'scripts', 'shopify_api.py'))
