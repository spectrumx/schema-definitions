# Experiment

An experiment in SDS is an abstraction described primarily by a special metadata file. An experiment MAY group datasets and artifacts. The files MAY back-reference the experiment UUID in their user-controlled metadata. If present, back-references are likely to be managed by SDS to retain consistency.

A future experiment implementation MAY follow a schema similar to the following:

```jsonc
{
    // required fields
    "name": "My Experiment, required",
    "uuid": "...", // identifier for this experiment, internal to SDS, only provided (and required) for updates,
    "datasets": [ // may be empty, required
        // Collection of dataset UUIDs in SDS that are part of this experiment, whether they
        //      existed before (used as inputs) or were created during the experiment (as outputs).
        //      Examples of the dataset creation include experiments involving data cleaning
        //      or other transformations, synthetic data generation, and experiments with a
        //      data collection step.
    ],
    "artifacts": [ // may be empty, required
        // Collection of file UUIDs in SDS that are part of this experiment.
        //      These are assorted files that may include logs, transformed data,
        //      configuration files, guides, support material, plots, binaries, reports,
        //      models, source code, notebooks, dataframes, and so on.
        //      i.e. anything that is not part of a dataset, but might be useful for reproducibility.
    ],

    // optional fields
    "abstract": "The abstract of the publication, optional",
    "authors": ["Optional Author <email@example.com>", "Another Author[ <...>]", ...],
    "description": "A short description of the experiment, optional",
    "doi": "The DOI of the dataset, optional",
    "institutions": ["Optional Institution", "Another Institution", ...],
    "keywords": ["Optional Keyword", "Another Keyword", ...],
    "license": "The license that applies to this experiment, optional",
    "release_date": "When the experiment was released, ISO 8601 format, optional",
    "repository": "URI for a repository of this experiment, or related to it, optional",
    "version": "A tag for this experiment version, optional",
    "website": "The website of the experiment, optional",
    "provenance": {
        // provenance fields, open-ended, optional
        //   This experiment's provenance is meant to give a quick glance at e.g.: how the experiment was conducted; what were
        //      the inputs and outputs; how to reproduce it; how the experiment is divided; timelines of each step.
        //      Artifacts provenance should be listed here as well e.g.: how they were generated/acquired and processed;
        //      Dataset provenance should be in their respective dataset entries.
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
