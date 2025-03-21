"""
The Azure ML pipeline for running a basic experiment
that consumes a dataset and does some logging.

to execute:
> python pipelines/experiments/demo_count_rows_and_log.py
--config-dir pipelines/config
--config-name experiments/demo_count_rows_and_log
run.submit=True
"""
# pylint: disable=no-member
# NOTE: because it raises 'dict' has no 'outputs' member in dsl.pipeline construction
import os
import sys

from azure.ml.component import dsl
from shrike.pipeline import AMLPipelineHelper

# NOTE: if you need to import from pipelines.*
ACCELERATOR_ROOT_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)
if ACCELERATOR_ROOT_PATH not in sys.path:
    print(f"Adding to path: {ACCELERATOR_ROOT_PATH}")
    sys.path.append(str(ACCELERATOR_ROOT_PATH))


class CountRowsDemo(AMLPipelineHelper):
    """Runnable/reusable pipeline helper class

    This class inherits from AMLPipelineHelper which provides
    helper functions to create reusable production pipelines.
    """

    def build(self, config):
        """Builds a pipeline function for this pipeline using AzureML SDK (dsl.pipeline).

        This method returns a constructed pipeline function
        (decorated with @dsl.pipeline).

        Args:
            config (DictConfig): configuration object

        Returns:
            dsl.pipeline: the function to create your pipeline
        """

        # helper functions below load the subgraph/component from
        # registered or local version depending on your config.run.use_local
        count_rows_component = self.component_load("CountRowsAndLog")

        # Here you should create an instance of a pipeline function
        # (using your custom config dataclass)
        @dsl.pipeline(
            name="demo-component-count-rows-and-log",
            description="Demo of a component that reads a dataset and counts the rows.",
            default_datastore=config.compute.compliant_datastore,
        )
        def demo_pipeline_function(demo_dataset):
            """Pipeline function for this graph.

            Args:
                demo_dataset: input dataset

            Returns:
                dict[str->PipelineOutputData]: a dictionary of your pipeline outputs
                    for instance to be consumed by other graphs
            """
            # general syntax:
            # component_instance = component_class(input=data, param=value)
            # or
            # subgraph_instance = subgraph_function(input=data, param=value)
            demo_component_step = count_rows_component(input_data=demo_dataset)

            self.apply_recommended_runsettings(
                "CountRowsAndLog", demo_component_step, gpu=False
            )

        # finally return the function itself to be built by helper code
        return demo_pipeline_function

    def pipeline_instance(self, pipeline_function, config):
        """Given a pipeline function, creates a runnable instance based on provided config.

        This is used only when calling this as a runnable pipeline
        using .main() function (see below).
        The goal of this function is to map the config to the
        pipeline_function inputs and params.

        Args:
            pipeline_function (function):
                the pipeline function obtained from self.build()
            config (DictConfig):
                configuration object

        Returns:
            azureml.core.Pipeline: the instance constructed
                                   with its inputs and params.
        """

        # NOTE: self.dataset_load() helps to load the dataset
        # based on its name and version
        pipeline_input_dataset = self.dataset_load(
            name=config.democomponent.input_data,
            version=config.democomponent.input_data_version,
        )

        # we simply call the pipeline function
        demo_pipeline = pipeline_function(demo_dataset=pipeline_input_dataset)

        # and we return that function so that helper can run it.
        return demo_pipeline


# NOTE: main block is necessary only if script is intended to be run from command line
if __name__ == "__main__":
    # calling the helper .main() function
    CountRowsDemo.main()
