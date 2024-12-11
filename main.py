# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "numpy",
# ]
# ///

import asyncio
import os

# The following lines are required only when running directly from a terminal window. VSCode launches don't need this.
if "PYGAME_HIDE_SUPPORT_PROMPT" not in os.environ:
    import sys
    os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
    sys.path.append("src")
    sys.path.append("Samples/AsteroidShooter/src")

from Samples.AsteroidShooter.src.main import main


if __name__ == "__main__":
    asyncio.run(main(os.path.join("assets")))
