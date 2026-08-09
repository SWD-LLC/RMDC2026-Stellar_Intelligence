# RMDC26 References and Provenance Boundaries

This page distinguishes challenge inputs from external scientific references and software/tooling references.

## Challenge data source

The Stage 1 production fitter reads only the RMDC26 Experienced-tier challenge Parquet on Roman Research Nexus:

```text
/data/data-challenge/rges/RMDC26_Experienced_Data.parquet
```

The challenge dataset is not redistributed in this public repository.

## Official RMDC26 / RGES-PIT resources

- RGES-PIT Data Challenge: https://rges-pit.org/data-challenge/
- Roman Research Nexus / AAS workshop introduction: https://rges-pit.org/data-challenge/aas-workshop/1-nexus/
- Official challenge notebooks: https://github.com/rges-pit/data-challenge-notebooks
- `microlens-submit`: https://github.com/rges-pit/microlens-submit
- `microlens-submit` documentation: https://microlens-submit.readthedocs.io/en/latest/
- manual submission format: https://microlens-submit.readthedocs.io/en/latest/submission_manual.html

The Roman Nexus material identifies `microlens-submit` as the stateful toolkit for managing, validating, and packaging challenge submissions and emphasizes strict adherence to automated submission criteria.

## External scientific reference: OGLE

Optical Gravitational Lensing Experiment (OGLE):

https://www.astrouw.edu.pl/ogle/

OGLE is documented here as an external microlensing survey/reference resource. Unless a specific artifact explicitly states otherwise, OGLE data are **not** challenge-fit inputs and are not silently merged with the RMDC26 simulated light curves.

## Provenance rule

For every RMDC26 artifact, distinguish:

1. **challenge input** — data provided by RMDC26 and directly fitted;
2. **derived challenge result** — parameters, residual metrics, route metadata, validation records, and submission artifacts produced from those inputs;
3. **tooling reference** — software/documentation used to construct or validate the workflow;
4. **external scientific reference** — literature, surveys, catalogs, or examples used for domain context/comparison;
5. **organizer instruction** — challenge-specific clarification that controls a submission convention.

External reference material does not become observational evidence for a challenge event merely because it is useful background.

## Time-coordinate note

The Stage 1 pipeline records `t0_time_system=input_bjd`. A separate read-only audit identified a wording mismatch between the challenge input coordinate and submission documentation. The team requested organizer clarification and locked the RMDC26-specific policy to preserve the Stage 1 numeric BJD values unchanged for submission. No undocumented BJD-to-HJD transform was performed.

## Reproducibility note

The public code and synthetic tests are designed to make the fitting and routing behavior inspectable without republishing protected challenge data. Reproducing the exact competition results requires authorized access to the RMDC26 Experienced dataset on the Roman Research Nexus or an equivalent organizer-provided data source.
