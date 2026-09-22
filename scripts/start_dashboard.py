"""Start TNT Media Dashboard"""
import os
import sys
import subprocess
from pathlib import Path


def main():
    print("=" * 60)
    print("  TNT Media Dashboard Launcher")
    print("=" * 60)
    
    # Đường dẫn tới workspace
    workspace = Path(__file__).parent.parent
    
    # Chạy web server
    web_server = os.path.join(workspace, 'src', 'web_server.py')
    
    print(f"\n  Workspace: {workspace}")
    print(f"  Web Server: {web_server}")
    print(f"  URL: http://localhost:8000")
    print("\n  Nhấn Ctrl+C để dừng.\n")
    
    try:
        subprocess.run(
            [sys.executable, web_server],
            cwd=str(workspace),
            check=True
        )
    except KeyboardInterrupt:
        print("\n\nDashboard stopped.")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    main()
