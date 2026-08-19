Set-Location d:\develop\project\bujidao-rag
$dirs = @('db2','dm','highgo','kingbase','opengauss','oracle','postgresql','sqlserver')
foreach ($d in $dirs) {
    git rm --cached -r --quiet "ruoyi-vue-pro/sql/$d" 2>&1 | Out-Null
}
Write-Host "REMOVED_FROM_INDEX"
git status --short | Select-String 'sql/' | Where-Object { $_ -notmatch 'mysql|tools' } | Select-Object -First 5
