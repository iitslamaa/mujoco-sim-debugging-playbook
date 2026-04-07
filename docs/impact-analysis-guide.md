# Impact Analysis Guide

The impact analysis flips the dependency map around.

Instead of asking what an artifact depends on, it asks:

- if this dependency changes, what downstream artifacts are affected?

That makes it useful for deciding how wide a refresh needs to be after touching a generator or upstream report.
