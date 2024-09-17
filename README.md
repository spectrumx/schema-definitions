# SpectrumX Schema Definitions

Repository for SpectrumX schema definitions, covering shared data structures and message formats.

## File Structure

Let's aim to keep the following structure for new schema definitions:

```bash
 README.md                     # this file
 definitions                   # all schema definitions
 └─  $COMPONENT                # component that generates messages following this schema
    └─  $SUB_COMPONENT         # (optional) child component
       └─  $MESSAGE_NAME       # a common name describing this message
          ├─  README.md        # (optional) description of the message, required fields, changelogs
          └─  $VERSION         # version tag of this definition (e.g. v0, v0-alpha, v1, v2-rc1, etc.)
             ├─  schema.json   # schema definition
             └─  tests         # (optional) test cases and validation code examples
```

## Resources

+ [How to auto-generate a JSON schema from a Pydantic model](https://docs.pydantic.dev/2.9/why/#json-schema) (expand the example to see the code).
