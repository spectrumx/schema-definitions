# SigMF Metadata Format under SDS

+ [SigMF Metadata Format under SDS](#sigmf-metadata-format-under-sds)
    + [Adding VS Code support](#adding-vs-code-support)

## Adding VS Code support

Add the following user settings to `settings.json`:

```jsonc
"": {
    // ...
    "*.sigmf-meta": "json",
    // ...
}
// ...
"json.schemas": [
    // ...
    {
        "fileMatch": [
            "*.sigmf-meta"
        ],
        "url": "https://raw.githubusercontent.com/sigmf/SigMF/refs/heads/main/sigmf-schema.json"
    },
    // ...
]
```
