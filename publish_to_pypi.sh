#!/bin/bash
# Script para publicar ForgeFlow no PyPI
# Uso: ./publish_to_pypi.sh [testpypi|pypi]

set -e

TARGET=${1:-testpypi}

echo "🚀 Publicando ForgeFlow no $TARGET..."

# Limpar builds antigos
echo "🧹 Limpando builds antigos..."
rm -rf dist/ build/ *.egg-info

# Build do pacote
echo "📦 Criando pacotes de distribuição..."
python -m build

# Validar pacotes
echo "✅ Validando pacotes..."
python -m twine check dist/*

# Upload
if [ "$TARGET" = "testpypi" ]; then
    echo "📤 Fazendo upload para TestPyPI..."
    python -m twine upload --repository testpypi dist/*
    echo ""
    echo "✅ Publicado no TestPyPI!"
    echo "🔗 Visite: https://test.pypi.org/project/forgeflow/"
    echo ""
    echo "Para testar a instalação:"
    echo "pip install --index-url https://test.pypi.org/simple/ forgeflow"
elif [ "$TARGET" = "pypi" ]; then
    echo "📤 Fazendo upload para PyPI oficial..."
    python -m twine upload dist/*
    echo ""
    echo "✅ Publicado no PyPI!"
    echo "🔗 Visite: https://pypi.org/project/forgeflow/"
    echo ""
    echo "Para instalar:"
    echo "pip install forgeflow"
else
    echo "❌ Opção inválida. Use: testpypi ou pypi"
    exit 1
fi

echo ""
echo "🎉 Publicação concluída com sucesso!"
