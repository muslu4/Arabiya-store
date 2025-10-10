@echo off
echo Adding BannerSlider changes to git...
cd /d "%~dp0"

git add src/components/BannerSlider.jsx

echo Committing changes...
git commit -m "Fix BannerSlider component - improve link handling and navigation"

echo Pushing changes to repository...
git push

echo BannerSlider changes have been successfully pushed to the repository!
pause
