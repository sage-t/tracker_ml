# tracker_python_sdk

This is the Python 3 SDK for using tracker.ml.

## Use

First, initialize tracker using the CLI and update the files you want to track. Then import 
`trackerml` anywhere and everywhere. Use is easy:

```python
import trackerml as tml

# <machine learning code>

# record int, float, or str
tml.record("accuracy", 0.42)
tml.record("model", "Logistic Regression")

# record multiple values under the same key
tml.mrecord("epoch", 1)
tml.mrecord("epoch", 2)
tml.mrecord("epoch", 3)
```

All changes since the previous run and all recorded values will be automatically saved. The CLI
can be used to view/compare trials and undo changes.
