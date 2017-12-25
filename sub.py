from time import localtime, strftime
import subprocess

# setup vars
time = strftime("%Y-%m-%d %H:%M:%S", localtime())
cmd = 'git commit -m "' + time + '"'
pathdot = '~/p/dotfiles'

# array setup for rsync
arrdot = [
    '~/.xonshrc',
    '~/.tmux.conf.local',
    '~/.vimrc',
    '~/.config/xonsh/config.json',
    '~/.config/alacritty/alacritty.yml',
    '~/.bashrc', '~/.config/nvim/init.vim',
    '~/.config/fish/config.fish'
]

# array setup for github
arrgit = [
    'cd ' + pathdot,
    'git add -A',
    cmd,
    'git push'
]

# chain bash commands for dotfiles
bashDot = ['rsync -avz {} {}'.format(x, pathdot) for x in arrdot]
bashDot.extend(arrgit)
bashChain = '; '.join(bashDot)

# subprocess for cmds
process = subprocess.Popen(
    '/bin/bash', stdin=subprocess.PIPE, stdout=subprocess.PIPE)
out, err = process.communicate(bashChain.encode('utf-8'))
print(out.decode('utf-8'))
