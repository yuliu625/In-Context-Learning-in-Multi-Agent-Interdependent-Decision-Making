from __future__ import annotations
from loguru import logger

from typing import TYPE_CHECKING
# if TYPE_CHECKING:


HUMAN_MESSAGE_CONTENT_CASES = [
    "What is your model id?",
]


EXPERIMENT_HUMAN_MESSAGE_CONTENT_CASES = [
    """\
Now for the 1 round.
In this round, the price given is:

```json
{"price": 5.24}
```

Now, make your prediction and give reasons.""",
]

