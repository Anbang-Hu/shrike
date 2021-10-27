# Per-file loggers
The compliant logging provided by shrike works nicely with Python-style per-file loggers.

Given an entry script run.py:
```python
{!docs/compliant_logging/run.py!}
```
which calls `a_method()` from script a.py:
```python
{!docs/compliant_logging/a.py!}
```
The output logs are
```
SystemLog:INFO:a:hi from a
SystemLog:INFO:__main__:hi from entry point
```

To ensure that per-file loggers work properly, you must:
1. in the entry script, call `log = logging.getLogger(__name__)` after `enable_compliant_logging()`;
2. for methods you want to import, call `log.logging.getLogger(__name__)` inside method definitions, e.g. (a.py)