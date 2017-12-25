import pexpect
from secret import (
    amo5,
    amo7,
    amo8,
    amo9,
    amo10,
    amp1,
    amp2,
    lts1,
    lts2,
    smtp2,
    ns1,
)

# connection constructor

def test:
    child = pexpect.spawn('echo $HOME')
