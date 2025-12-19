import urllib.request
import ssl

# Ignorar errores de SSL por simplificación en entornos locales/dev
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://cdn.jsdelivr.net/npm/jsbarcode@3.11.5/dist/JsBarcode.all.min.js"
try:
    with urllib.request.urlopen(url, context=ctx) as response, open("static/jsbarcode.all.min.js", 'wb') as out_file:
        data = response.read()
        out_file.write(data)
    print("Downloaded successfully")
except Exception as e:
    print(f"Error: {e}")
