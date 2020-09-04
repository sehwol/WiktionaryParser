# Contributing

## Testing MediaWiki markup

If you want to download a Wiktionary page's markup for markup testing, follow
the URL below, replacing `{{PAGE}}` with the word you want.

```
https://en.wiktionary.org/w/api.php?action=parse&page={{PAGE}}&prop=wikitext&formatversion=2&format=json
```

Opening the URL should give you a JSON with the wikitext as a string.


If you need an older version, use the URL below, replacing `{{OLDID}}`.

```
https://en.wiktionary.org/w/api.php?action=parse&oldid={{OLDID}}&prop=wikitext&formatversion=2&format=json
```

More information on the Wiktionary API
[here](https://en.wiktionary.org/w/api.php?action=help&modules=parse).
