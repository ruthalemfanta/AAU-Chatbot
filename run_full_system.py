#!/usr/bin/env python3
"""
AAU Helpdesk Chatbot - Full System Runner
Starts both backend and frontend for development
"""

import subprocess
import sys
import os
import time
import signal
from pathlib import Path

def run_command_in_background(command, cwd=None, name="Process"):
    """Run a command in the background and return the process"""
    print(f"🚀 Starting {name}...")
    try:
        process = subprocess.Popen(
            command,
            shell=True,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            preexec_fn=os.setsid if os.name != 'nt' else None
        )
        return process
    except Exception as e:
        print(f"❌ Failed to start {name}: {e}")
        return None

def check_dependencies():
    """Check if required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    # Check if virtual environment exists
    venv_path = Path("aau_chatbot_env")
    if not venv_path.exists():
        print("❌ Virtual environment not found. Please run setup.py first.")
        return False
    
    # Check if frontend dependencies are installed
    frontend_path = Path("frontend")
    if not frontend_path.exists():
        print("❌ Frontend directory not found.")
        return False
    
    node_modules = frontend_path / "node_modules"
    if not node_modules.exists():
        print("📦 Installing frontend dependencies...")
        result = subprocess.run(["npm", "install"], cwd="frontend", capture_output=True)
        if result.returncode != 0:
            print("❌ Failed to install frontend dependencies.")
            return False
    
    print("✅ Dependencies check passed!")
    return True

def main():
    """Main function to run the full system"""
    print("🤖 AAU Helpdesk Chatbot - Full System Startup")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    processes = []
    
    try:
        # Start backend (FastAPI)
        backend_command = "source aau_chatbot_env/bin/activate && python app/main.py"
        backend_process = run_command_in_background(backend_command, name="Backend API")
        if backend_process:
            processes.append(("Backend", backend_process))
        
        # Wait a bit for backend to start
        print("⏳ Waiting for backend to start...")
        time.sleep(3)
        
        # Start frontend (React)
        frontend_command = "npm run dev"
        frontend_process = run_command_in_background(frontend_command, cwd="frontend", name="Frontend")
        if frontend_process:
            processes.append(("Frontend", frontend_process))
        
        print("\n" + "=" * 50)
        print("🎉 System started successfully!")
        print("\n📋 Access Points:")
        print("  🌐 Frontend (React):     http://localhost:5173")
        print("  🔧 Backend API:          http://localhost:8000")
        print("  📚 API Documentation:    http://localhost:8000/docs")
        print("  📊 Metrics Dashboard:    http://localhost:5173/metrics")
        print("\n💡 Tips:")
        print("  • Use the chat interface to test the chatbot")
        print("  • Visit /metrics to see evaluation results")
        print("  • Check /docs for API documentation")
        print("  • Press Ctrl+C to stop all services")
        print("\n" + "=" * 50)
        
        # Monitor processes
        while True:
            time.sleep(1)
            for name, process in processes:
                if process.poll() is not None:
                    print(f"⚠️  {name} process stopped unexpectedly")
                    return
    
    except KeyboardInterrupt:
        print("\n🛑 Shutting down services...")
        
        # Terminate all processes
        for name, process in processes:
            try:
                if os.name != 'nt':
                    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
                else:
                    process.terminate()
                print(f"✅ Stopped {name}")
            except Exception as e:
                print(f"⚠️  Error stopping {name}: {e}")
        
        print("👋 Goodbye!")
    
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()