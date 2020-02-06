
export ZSH="/home/souryuu/.oh-my-zsh"

ZSH_THEME="ys"

plugins=(git)

source $ZSH/oh-my-zsh.sh

export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
if command -v pyenv 1>/dev/null 2>&1; then
 eval "$(pyenv init -)"
fi
