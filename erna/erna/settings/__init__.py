import os
from .base import *


if os.environ.get('mode') == 'dev':
    from .dev import *
elif os.environ.get('mode') == 'prod':
    from .prod import *
else:
    from .local import *