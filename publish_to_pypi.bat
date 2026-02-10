@echo off
REM Script para publicar ForgeFlow no PyPI (Windows)
REM Uso: publish_to_pypi.bat [testpypi|pypi]

setlocal enabledelayedexpansion

set TARGET=%1
if "%TARGET%"=="" set TARGET=testpypi

echo 🚀 Publicando ForgeFlow no %TARGET%...

REM Limpar builds antigos
echo 🧹 Limpando builds antigos...
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
for /d %%i in (*.egg-info) do rmdir /s /q "%%i"

REM Build do pacote
echo 📦 Criando pacotes de distribuição...
python -m build
if errorlevel 1 goto error

REM Validar pacotes
echo ✅ Validando pacotes...
python -m twine check dist/*
if errorlevel 1 goto error

REM Upload
if "%TARGET%"=="testpypi" (
    echo 📤 Fazendo upload para TestPyPI...
    python -m twine upload --repository testpypi dist/*
    if errorlevel 1 goto error
    echo.
    echo ✅ Publicado no TestPyPI!
    echo 🔗 Visite: https://test.pypi.org/project/forgeflow/
    echo.
    echo Para testar a instalação:
    echo pip install --index-url https://test.pypi.org/simple/ forgeflow
) else if "%TARGET%"=="pypi" (
    echo 📤 Fazendo upload para PyPI oficial...
    python -m twine upload dist/*
    if errorlevel 1 goto error
    echo.
    echo ✅ Publicado no PyPI!
    echo 🔗 Visite: https://pypi.org/project/forgeflow/
    echo.
    echo Para instalar:
    echo pip install forgeflow
) else (
    echo ❌ Opção inválida. Use: testpypi ou pypi
    exit /b 1
)

echo.
echo 🎉 Publicação concluída com sucesso!
goto end

:error
echo ❌ Erro durante a publicação!
exit /b 1

:end
endlocal
