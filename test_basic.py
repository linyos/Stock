"""
簡易 API 測試腳本
不需要 requests 套件，僅使用內建的 urllib
"""
import urllib.request
import urllib.parse
import json
import sys

def test_health_check():
    """測試健康檢查端點"""
    try:
        url = "http://localhost:8000/health"
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
            print("✅ 健康檢查成功:", data)
            return True
    except Exception as e:
        print("❌ 健康檢查失敗:", e)
        return False

def test_root_endpoint():
    """測試根端點"""
    try:
        url = "http://localhost:8000/"
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
            print("✅ 根端點回應:", data["message"])
            return True
    except Exception as e:
        print("❌ 根端點失敗:", e)
        return False

if __name__ == "__main__":
    print("=== FastAPI 服務測試 ===")
    print("請確認 FastAPI 服務已啟動 (python run_server.py)")
    print()
    
    if test_health_check() and test_root_endpoint():
        print("✅ 基本端點測試通過！")
        print("🌐 API 文件請訪問: http://localhost:8000/docs")
    else:
        print("❌ 測試失敗，請檢查服務是否正常啟動")
        sys.exit(1)
