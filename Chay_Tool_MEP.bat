@echo off
chcp 65001 > nul
title MEP Energy Master Suite - Local Offline Tool
cls

echo =========================================================================
echo       KÍCH HOẠT MEP ENERGY MASTER SUITE (HOÀN TOÀN OFFLINE CỤC BỘ)
echo =========================================================================
echo.
echo [1] Đang khởi chạy Ứng dụng Giao diện Đồ họa Standalone...
echo [2] Không cần kết nối Internet - Chạy trực tiếp trên trình duyệt cá nhân.
echo.

set SCRIPT_DIR=%~dp0
set HTML_APP=%SCRIPT_DIR%MEP_Energy_Master_App.html

if exist "%HTML_APP%" (
    echo Đang mở giao diện kỹ thuật: %HTML_APP%
    start "" "%HTML_APP%"
) else (
    echo [LỖI] Không tìm thấy file MEP_Energy_Master_App.html
    pause
    exit /b
)

echo.
echo Đã khởi chạy thành công! Bạn có thể sử dụng toàn bộ 7 Modules ngay bây giờ.
echo File Workbook Excel tính toán chuyên sâu đặt tại:
echo %SCRIPT_DIR%MEP_Energy_Auditor_Master_Toolkit.xlsx
echo.
timeout /t 5 > nul
exit
