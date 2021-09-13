# Welcome to the Advanced TCGAIntegrator.

## Advanced TCGAIntegrator
This is an advanced TCGAIntegrator developed based on the [TCGAIntegrator link](https://github.com/cooperlab/TCGAIntegrator)

The raw TCGA datasets were extracted from [TCGAIntegrator link](https://github.com/cooperlab/TCGAIntegrator). We refined the raw data with three different modes: Survival, Censor and Hybrid. The feature parts of those data would be exactly the same, which would all be a float numpy array returned by TCGAIntegrator. The key difference lies in the design of the label as we intend to analyze the dataset in three different circumstances.

• **Survival Mode**: The label would be a N-length float numpy array containing the death or
last follow up times in days for each sample, which implies that we cannot identify if the
patient is still alive.

• **Censor Mode**: The label would be an N-length float numpy array containing the rightcensoring
status of each sample. A value of ’1’ indicates samples where the patient was
alive at last follow-up and a value of ’0’ indicates uncensored samples where a death event
was observed.

• **Hybrid Mode**: The label would be the combination of Survival and Censor. If the Censor
value of a data input (single row) is 1, we keep the Survival value positive, otherwise, we
swap the numbers for negative.

## TCGAIntegrator Usage
