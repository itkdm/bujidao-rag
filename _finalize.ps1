Set-Location d:\develop\project\bujidao-rag
# 从索引移除 sql 目录（保留本地文件）
git rm --cached -r --quiet ruoyi-vue-pro/sql 2>&1 | Out-Null
git add -A 2>&1 | Select-Object -First 2
Write-Host "=== any sql left in index? ==="
git ls-files | Where-Object { $_ -match 'ruoyi-vue-pro/sql/' } | Select-Object -First 5
Write-Host "=== amend + push ==="
git commit --amend --no-edit 2>&1 | Select-Object -Last 2
git push origin master 2>&1 | Select-Object -Last 12
