@echo off
echo Reiniciando o servidor Flask...

:: Encerra o processo Flask
taskkill /f /im python.exe

:: Aguarda um momento (opcional, dependendo se necessário)
timeout /t 1

:: Inicia o servidor Flask novamente
python .\api.py

echo Servidor reiniciado.
