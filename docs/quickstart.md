Getting started
===============

Ready to get started with Severus? This guide gives a good introduction to the engine.

Initializing your translator
----------------------------

The first thing to do with Severus is creating a translation instance. This is as quick as:

```python
from severus import Severus

T = Severus()
```

As per default configuration, Severus will use english as its default language and the current working directory to look for translation files. Of course you can customize its configuration, here is the complete list of accepted parameters:

| parameter | type | default |
| --- | --- | --- |
| path | str | current working directory |
| default\_language | str | en |
| encoding | str | utf8 |
| watch\_changes | bool | `False` |

Translations
------------

Severus gives you two different ways of handling your translations: using strings directly or mapping keys to identify which string you want to translate. While the first option gives you a quick way to start translating your words, the second one is appropriate when the complexity and the amount of the translation increases in your daily usage.

Let's see the two approaches separately.

### Using strings directly

The quickiest way to use Severus is to start writing your translations using strings directly. This allows you to just write the translation files for the languages you want to translate, and the convenient pattern is to use JSON files. 

Let's say we want to translate some strings from English, our default language, to Italian. Then we can write down an *it.json* file in our translations directory with this contents:

```json
{
    "Hello world!": "Ciao mondo!",
    "Hello {user_name}": "Ciao {user_name}"
}
```

As you can see, languages in Severus are identified by 2 letters codes, and strings may contain parameters in the same shape of the Python's `str.format()` method.

With just this single file we are now able to translate the upper strings depending on the language, as we can write:

```python
from severus import language

with language("it"):
    print(T("Hello {user_name}").format(user_name="Bob"))
```

which will produce *Ciao Bob*.

The `language` context manager is a nice way of handling your translations, but you can also explicitely set a language when calling your Severus instance, like:

```python
T("Hello {user_name}", lang="it")
```

### Mapping your translations

Whenever you want or need a more structured way of handling your translations, you can map such strings using keys. Severus gives you the choice to use JSON or YAML files, depending on which suits you better, but in this case you also have to write the mapping for the strings in your default language. Let's rewrite the upper example with keys, starting with an *en.json* file:

```json
{
    "greetings": {
        "world": "Hello world!",
        "user": "Hello {user_name}"
    }
}
```

and the relevant translation file *it.yaml*:

```yaml
greetings:
  world: Hello World!
  user: "Hello {user_name}"
```

Severus will produce keys joining the different part of your translation tree using dots, so in order to translate the strings in this case we will write:

```python
with language("it"):
    print(T("greetings.user").format(user_name="Bob"))
```

which gives us *Ciao Bob* as in the prior example.

#### Using multiple translation files

Severus also supports separating your translations into multiple files for the same language, so we can rewrite the last example using a folder instead of a single *it.yaml* file:

    it/
        greetings.yaml

and a *greetings.yaml* file like this:

```yaml
world: Hello World!
user: "Hello {user_name}"
time:
  morning: "Good morning"
  night: "Good night"
```

The translation of `greetings.user` will be the same, and as you can see, you can have any number of nested keys for your translations, as it will be for `greetings.time.morning`.

Pluralization
-------------

Severus also support pluralization over your translation strings. This means that when text marked for translation depends on a numeric variable, it might be translated differently based on the numeric value of such variable. As an example, in English we my want to render:

    n item(s)

where if n equals 1, we have:

    an item

while if n is greater than 1, for example 5, we have:

    5 items

In order to achieve this result with Severus, we need to add the relevant forms into our translation file, and we can even support even more cases:

```yaml
cart:
  contains: Your cart contains {items}
  item:
    _: item
    n0: no items
    n1: an item
    n2: "{n} items"
```

and we can translate our strings properly:

```python
with language("en"):
    print(
        T("cart.contains").format(
            items=T("cart.item").format(
                n=len(cart.items)
            )
        )
    )
```

This will print:

    Your cart contains no items (with n=0)
    Your cart contains an item (with n=1)
    Your cart contains 2 items (with n=2)

Mind that we also added a `_` key to our translations, that will handle cases where no numerical parameter was given, so in case we just call:

```python
T("cart.item")
```

we still produce *item* string.
