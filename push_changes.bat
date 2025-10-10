@echo off
echo Adding all changes to git...
git add .

echo Committing changes...
git commit -m "Fix frontend-backend connection for Render deployment"

echo Pushing changes to repository...
git push

echo Changes have been pushed successfully!
pause
