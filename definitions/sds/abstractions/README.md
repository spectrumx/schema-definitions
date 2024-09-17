# SDS Abstractions

SDS Abstractions are an extensible way to bring new concepts into SDS. Abstractions are defined by special metadata files with information that describes the relationships between files and other abstractions. These metadata files might include extra information and could be a convenient way to avoid redundancy and potential inconsistencies in the user-controlled metadata, which sits at the file-level.

The concept that motivated this sub-component is the "Dataset", which can be seen as a logical grouping of files that does not have a direct counterpart in the data store, yet, it is useful to manage related files. Following the idea of making SDS an experiment-oriented solution, an "Experiment" groups datasets and artifacts (assorted files that might be useful for experiment reproducibility, but are not part of a dataset).

Once they are well-defined, abstractions MAY motivate their own set of API methods for CRUD operations, and MAY be extended to include new metadata fields.
