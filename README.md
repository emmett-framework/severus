# Severus

Severus – */seˈweː.rus/* – is a Python internationalization engine designed with simplicity in mind.

## In a nutshell

*it.json*

```json
{
    "Hello world!": "Ciao mondo!"
}
```

*translate.py*

```python
from severus import Severus, language

T = Severus()

with language("it"):
    print(T("Hello world!"))
```

## Documentation

The documentation is available under the [docs folder](https://github.com/emmett-framework/severus/tree/master/docs).

## License

Severus is released under the BSD License.
