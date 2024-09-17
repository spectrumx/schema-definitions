# Dataset

A dataset in SDS is an abstraction described primarily by a special metadata file. The files MAY back-reference the dataset UUID in their user-controlled metadata. If present, back-references are likely to be managed by SDS to retain consistency.

A future dataset implementation MAY follow a schema similar to the following:

```jsonc
{
    // required fields
    "name": "My Dataset, required",
    "uuid": "...", // identifier for this dataset, internal to SDS, only provided (and required) for updates,
    "files": [ // may be empty, required
        // collection of file UUIDs in SDS that are part of this dataset
    ],

    // optional fields
    "abstract": "The abstract of the publication, optional",
    "authors": ["Optional Author <email@example.com>", "Another Author[ <...>]", ...],
    "description": "A short description of the dataset, optional",
    "doi": "The DOI of the dataset, optional",
    "institutions": ["Optional Institution", "Another Institution", ...],
    "keywords": ["Optional Keyword", "Another Keyword", ...],
    "license": "The license that applies to this dataset, optional",
    "release_date": "When the dataset was released, ISO 8601 format, optional",
    "repository": "URI for a repository of this dataset, or related to it, optional",
    "version": "A tag for this dataset version, optional",
    "website": "The website of the dataset, optional",
    "provenance": {
        // provenance fields, open-ended, optional
        // they are meant to describe the origin of the dataset, how it was collected, processed, and transformed.
        // they might include human-readable descriptions, who to cite, who collected it, and where it has been published before.
    },
    "citation": { // optional
        "bib": {
            // BibTeX citation, optional
        },
        // other citation formats TBD, optional
    },
    "others": {
        // user-defined metadata fields, open-ended, optional
    },
    // no more user-defined fields at the top-level
}
```
