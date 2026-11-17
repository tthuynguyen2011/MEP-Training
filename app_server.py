"""
Local Server phục vụ MEP Energy Master Suite trên Máy tính cá nhân (Offline 100%)
Không yêu cầu Internet, chỉ sử dụng thư viện chuẩn của Python.
"""

import http.server
import socketserver
import webbrowser
import os
import sys

PORT = 8089
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

def run():
    os.chdir(DIRECTORY)
    url = f"http://localhost:{PORT}/MEP_Energy_Master_App.html"
    print("=" * 75)
    print(f"  MEP ENERGY MASTER SUITE - LOCAL OFFLINE SERVER")
    print("=" * 75)
    print(f"  * Trạng thái : Đang chạy Local trên máy tính cá nhân (Không cần Internet)")
    print(f"  * Địa chỉ Web: {url}")
    print(f"  * Thư mục    : {DIRECTORY}")
    print("=" * 75)
    print("  Nhấn Ctrl+C để dừng server khi không sử dụng.\n")

    # Tự động mở trình duyệt
    try:
        webbrowser.open(url)
    except Exception as e:
        print(f"Vui lòng mở trình duyệt và truy cập: {url}")

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nĐã dừng server an toàn.")
            sys.exit(0)

if __name__ == "__main__":
    run()
