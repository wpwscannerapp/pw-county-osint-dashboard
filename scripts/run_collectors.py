#!/usr/bin/env python3
"""
PWC OSINT Data Collectors - Direct Execution
"""

import sys
import os
import subprocess

# Add project root to path
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, root_dir)

print(f"✅ Running from: {root_dir}")

def run_script(script_path):
    full_path = os.path.join(root_dir, script_path)
    print(f"Running: {script_path}")
    result = subprocess.run([sys.executable, full_path], 
                          capture_output=True, 
                          text=True, 
                          cwd=root_dir)
    print(result.stdout)
    if result.stderr:
        print("ERROR:", result.stderr)
    return result.returncode == 0

if __name__ == "__main__":
    print("=" * 70)
    print("🚀 Starting PWC OSINT Data Collectors")
    print("=" * 70)

    success = True
    success &= run_script("collectors/fire_ems_collector.py")
    success &= run_script("collectors/rss_collector.py")
    success &= run_script("collectors/facebook_collector.py")

    print("=" * 70)
    if success:
        print("✅ All collectors completed successfully!")
    else:
        print("❌ Some collectors failed!")
    print("=" * 70)
