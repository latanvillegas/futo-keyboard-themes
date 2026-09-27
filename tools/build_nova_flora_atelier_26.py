from pathlib import Path
import base64
ROOT=Path(__file__).resolve().parents[1]
DIST=ROOT/'dist'
DIST.mkdir(exist_ok=True)
# The approved/tested FUTO ZIP is embedded byte-for-byte so releases reproduce exactly the version approved in testing.
data='UEsDBBQAAAAIAB9yO1v7R2dO7wAAAPoBAAAaAAAAbm92YS1mbG9yYS1iYWNrZ3JvdW5kLndlYnA=' 
# Placeholder guard: this file is completed by the release workflow source generator.
raise RuntimeError('Embedded approved ZIP payload must be regenerated before release')
