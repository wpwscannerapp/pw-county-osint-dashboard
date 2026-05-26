#!/usr/bin/env python3
"""
PWC OSINT Data Collectors - Simple Direct Run
"""

import subprocess
import sys
import os

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(f"Running from: {root}")

def run_collector(filename):
    path = os.path.join(root, "collectors", filename)
    print(f"\n🚀 Running {filename}...")
    try:
        result = subprocess.run([sys.executable, path], 
                              cwd=root, 
                              capture_output=True, 
                              text=True,
                              timeout=300)
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        print(f"✅ {filename} finished with code {result.returncode}")
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Failed to run {filename}: {e}")
        return False

if __name__ == "__main__":
    print("=" * 70)
    print("🚀 Starting All PWC OSINT Collectors")
    print("=" * 70)

    success = True
    success &= run_collector("fire_ems_collector.py")
    success &= run_collector("rss_collector.py")
    success &= run_collector("facebook_collector.py")

    print("=" * 70)
    if success:
        print("🎉 ALL COLLECTORS COMPLETED SUCCESSFULLY!")
    else:
        print("⚠️ Some collectors had errors.")
    print("=" * 70)
