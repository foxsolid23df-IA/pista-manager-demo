$src = Get-Location
$parent = Split-Path -Parent $src
$dest = Join-Path $parent "pista_manager_test"

Write-Host "1. Clonando proyecto a: $dest ..."
if (Test-Path $dest) {
    Remove-Item $dest -Recurse -Force
}
Copy-Item -Path $src -Destination $dest -Recurse -Force

Write-Host "2. Ajustando puertos y nombres en docker-compose.yml ..."
$yml = "$dest\docker-compose.yml"

# Usamos el metodo .Replace de .NET para ser literal y evitar erores de Regex
$content = Get-Content $yml -Raw
$content = $content.Replace("container_name: pista_app", "container_name: pista_app_test")
$content = $content.Replace("container_name: pista_postgres", "container_name: pista_postgres_test")
$content = $content.Replace("8000:8000", "8081:8000")
$content = $content.Replace("postgres_data:", "postgres_data_test:")

Set-Content -Path $yml -Value $content

Write-Host "✅ AMBIENTE DE PRUEBAS CREADO"
Write-Host "Carpeta: $dest"
Write-Host "Puerto Web: 8081"
