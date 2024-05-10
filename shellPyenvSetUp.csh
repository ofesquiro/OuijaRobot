export PYENV_ROOT="$HOME/.pyenv"

# Ensure Pyenv is in the system's PATH
export PATH="$PYENV_ROOT/bin:$PATH"

# Load Pyenv automatically
if command -v pyenv 1>/dev/null 2>&1; then
  eval "$(pyenv init --path)"

echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc

echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.profile
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.profile
echo 'eval "$(pyenv init -)"' >> ~/.profile

pyenv install 3.10.4
