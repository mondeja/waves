"""Configuration of waves.

In this module is located the data size counter that allows smart allocation
of sizes in memory, storing opened file descriptors of some sounds until
a limit is reached.
"""

# Maximum memory allocated by opened file descriptors
MAX_FDS_MEMORY_BITS = 512 * 8000  # 512 Mb

CURRENT_FDS_MEMORY_BITS = 0
