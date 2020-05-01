#/bin/bash
git update-index --refresh 
git diff-index --quiet HEAD --
if [[ $? -eq 1 ]]; then
    echo "There are untracked changes... Please commit them before doing a new release."
    exit 1
fi
echo "# Before you deploy, have you:"
echo "# 1. Checked that the version number has been bumped, and commited?"
echo "# 2. Checked that the version of software in the README is correct, and commited any changes?"
echo "# If so, run bash deploy.sh | bash"
version=$(cat lissero/__init__.py | grep version | cut -f2 -d "=" | sed -E 's/^[[:space:]]+"(.*)"/v\1/g')
echo "git tag -a $version"
echo "rm -rf build/* dist/*"
echo "python3 setup.py sdist bdist_wheel"
echo "twine upload dist/*"
echo "git push --tags"