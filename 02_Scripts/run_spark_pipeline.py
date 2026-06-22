"""
run_spark_pipeline.py - Master Orchestrator for Individual Project 2
Runs the full data pipeline: Bronze -> Silver -> Gold
Logs execution times and statuses.
"""

import time
import json
import os
import subprocess
import sys

# Windows Spark fixes
os.environ['SPARK_HOME'] = r'C:\Users\richa\spark'
os.environ['HADOOP_HOME'] = r'C:\Users\richa\hadoop'
if os.environ['SPARK_HOME'] + r'\bin' not in os.environ['PATH']:
    os.environ['PATH'] += os.pathsep + os.environ['SPARK_HOME'] + r'\bin'
if os.environ['HADOOP_HOME'] + r'\bin' not in os.environ['PATH']:
    os.environ['PATH'] += os.pathsep + os.environ['HADOOP_HOME'] + r'\bin'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, '..', '08_Logs')
os.makedirs(LOG_DIR, exist_ok=True)

def run_layer(script_name, layer_name):
    print(f"\n{'='*60}")
    print(f"  RUNNING {layer_name.upper()} LAYER")
    print(f"{'='*60}\n")
    
    script_path = os.path.join(BASE_DIR, script_name)
    start_time = time.time()
    
    try:
        # Run the script with explicit env
        env = os.environ.copy()
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            timeout=300,
            env=env
        )
        
        elapsed = time.time() - start_time
        
        if result.returncode == 0:
            print(result.stdout)
            print(f"\n✅ {layer_name.upper()} completed in {elapsed:.1f}s")
            return {"status": "success", "time": elapsed, "output": result.stdout[-500:]}
        else:
            print(f"STDERR: {result.stderr}")
            print(f"STDOUT: {result.stdout}")
            print(f"\n❌ {layer_name.upper()} FAILED")
            return {"status": "failed", "time": elapsed, "error": result.stderr[-500:]}
            
    except subprocess.TimeoutExpired:
        elapsed = time.time() - start_time
        print(f"\n⏰ {layer_name.upper()} TIMEOUT after {elapsed:.1f}s")
        return {"status": "timeout", "time": elapsed}
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"\n❌ {layer_name.upper()} EXCEPTION: {e}")
        return {"status": "error", "time": elapsed, "error": str(e)}

if __name__ == "__main__":
    print("🚀 Starting Individual Project 2 Data Pipeline...")
    print(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    total_start = time.time()
    results = {}
    
    # Layer 1: Bronze
    results['bronze'] = run_layer('bronze_layer.py', 'Bronze')
    
    # Only continue if previous layer succeeded
    if results['bronze']['status'] == 'success':
        # Layer 2: Silver
        results['silver'] = run_layer('silver_layer.py', 'Silver')
    
    if results.get('silver', {}).get('status') == 'success':
        # Layer 3: Gold
        results['gold'] = run_layer('gold_layer.py', 'Gold')
    
    total_time = time.time() - total_start
    
    # Summary
    print(f"\n{'='*60}")
    print(f"  PIPELINE EXECUTION SUMMARY")
    print(f"{'='*60}")
    
    all_success = True
    for layer, res in results.items():
        status_icon = "✅" if res['status'] == 'success' else "❌"
        print(f"  {status_icon} {layer.upper():10s} | {res['status']:10s} | {res.get('time', 0):.1f}s")
        if res['status'] != 'success':
            all_success = False
    
    print(f"\n  Total Time: {total_time:.1f}s")
    print(f"  Overall: {'✅ ALL SUCCESS' if all_success else '❌ SOME LAYERS FAILED'}")
    
    summary_path = os.path.join(LOG_DIR, f'pipeline_summary_{time.strftime("%Y%m%d_%H%M%S")}.json')
    with open(summary_path, 'w') as f:
        json.dump({
            "timestamp": time.strftime('%Y-%m-%d %H:%M:%S'),
            "total_time": total_time,
            "layers": results,
            "overall_status": "success" if all_success else "failed"
        }, f, indent=2)
