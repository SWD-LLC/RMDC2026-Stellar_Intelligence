# RMDC26 References and Provenance Boundaries

This page distinguishes challenge inputs from organizer-maintained challenge resources, external scientific references, and software/tooling references.

## Challenge data source

The Stage 1 production fitter reads only the RMDC26 Experienced-tier challenge Parquet on Roman Research Nexus:

```text
/data/data-challenge/rges/RMDC26_Experienced_Data.parquet
```

The challenge dataset is not redistributed in this public repository.

## Official RMDC26 / RGES-PIT resources

Primary challenge pages and repositories:

- RMDC26 challenge page: https://rges-pit.org/data-challenge/
- Roman Research Nexus / AAS workshop introduction: https://rges-pit.org/data-challenge/aas-workshop/1-nexus/
- official challenge notebook and informational repository: https://github.com/rges-pit/data-challenge-notebooks
- official submission-tool repository: https://github.com/rges-pit/microlens-submit
- `microlens-submit` documentation: https://microlens-submit.readthedocs.io/en/latest/

Submission specifications and examples:

- CLI tutorial: https://microlens-submit.readthedocs.io/en/latest/cli_tutorial.html
- Python API: https://microlens-submit.readthedocs.io/en/latest/api.html
- usage examples: https://microlens-submit.readthedocs.io/en/latest/usage_examples.html
- manual submission format: https://microlens-submit.readthedocs.io/en/latest/submission_manual.html

Organizer modeling/workflow notebooks:

- challenge workflow / submission creation: https://github.com/rges-pit/data-challenge-notebooks/blob/main/AAS%20Workshop/Session%20A:%20Nexus/Nexus_Workflow.ipynb
- single-lens fitting and pipelined full-season demonstration: https://github.com/rges-pit/data-challenge-notebooks/blob/main/AAS%20Workshop/Session%20B:%20Single%20Lens%20%26%20Pipelines/Single_Lens_Pipeline.ipynb
- binary-lens fitting approaches: https://github.com/rges-pit/data-challenge-notebooks/blob/main/AAS%20Workshop/Session%20C:%20Binary%20Lens/Fitting_Binary_Lenses.ipynb
- microlensing open-source tools: https://github.com/rges-pit/data-challenge-notebooks/blob/main/Extras/Microlensing_Tools.ipynb

The Roman Nexus documentation identifies `microlens-submit` as the challenge submission toolkit and explicitly warns that strict adherence to submission criteria is required because much of the evaluation is automated.

See `OFFICIAL_CHALLENGE_RESOURCES.md` for the source hierarchy, Nexus reference-directory rules, environment-file policy, and direct mapping of these resources into this repository's workflow.

## External scientific reference: OGLE

Optical Gravitational Lensing Experiment (OGLE):

https://www.astrouw.edu.pl/ogle/

OGLE is documented here as an external microlensing survey/reference resource. Unless a specific artifact explicitly states otherwise, OGLE data are **not** challenge-fit inputs and are not silently merged with the RMDC26 simulated light curves.

## Provenance rule

For every RMDC26 artifact, distinguish:

1. **challenge input** — data provided by RMDC26 and directly fitted;
2. **derived challenge result** — parameters, residual metrics, route metadata, validation records, and submission artifacts produced from those inputs;
3. **organizer-maintained challenge reference** — official instructions, notebooks, environment files, submission specifications, and direct clarifications;
4. **tooling reference** — software/documentation used to construct or validate the workflow;
5. **external scientific reference** — literature, surveys, catalogs, or examples used for domain context/comparison;
6. **organizer instruction** — a challenge-specific clarification that controls a submission convention.

External reference material does not become observational evidence for a challenge event merely because it is useful background.

## Nexus reference content

The organizer-provided Nexus reference notebooks can execute, but are read-only and regularly replaced from their source repository. They are therefore treated as external reference material. Project-owned notebooks, evidence, and code should live in a durable project workspace/repository rather than inside the preloaded reference directory.

## Time-coordinate note

The Stage 1 pipeline records `t0_time_system=input_bjd`. A separate read-only audit identified a wording mismatch between the challenge input coordinate and submission documentation. The team requested organizer clarification and locked the RMDC26-specific policy to preserve the Stage 1 numeric BJD values unchanged for submission. No undocumented BJD-to-HJD transform was performed.

## Reproducibility note

The public code and synthetic tests are designed to make the fitting and routing behavior inspectable without republishing protected challenge data. Reproducing the exact competition results requires authorized access to the RMDC26 Experienced dataset on the Roman Research Nexus or an equivalent organizer-provided data source.
