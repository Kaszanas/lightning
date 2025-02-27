import os
from dataclasses import dataclass
from typing import Any, Callable, Type

from typing_extensions import Protocol, runtime_checkable

from lightning_app.components.multi_node.base import MultiNode
from lightning_app.components.multi_node.pytorch_spawn import _PyTorchSpawnRunExecutor
from lightning_app.core.work import LightningWork
from lightning_app.utilities.app_helpers import is_static_method
from lightning_app.utilities.packaging.cloud_compute import CloudCompute
from lightning_app.utilities.tracer import Tracer


@runtime_checkable
class _LiteWorkProtocol(Protocol):
    @staticmethod
    def run() -> None:
        ...


@dataclass
class _LiteRunExecutor(_PyTorchSpawnRunExecutor):
    @staticmethod
    def run(
        local_rank: int,
        work_run: Callable,
        main_address: str,
        main_port: int,
        num_nodes: int,
        node_rank: int,
        nprocs: int,
    ):
        from lightning.lite import LightningLite
        from lightning.lite.strategies import DDPSpawnShardedStrategy, DDPSpawnStrategy

        # Used to configure PyTorch progress group
        os.environ["MASTER_ADDR"] = main_address
        os.environ["MASTER_PORT"] = str(main_port)

        # Used to hijack TorchElastic Cluster Environnement.
        os.environ["GROUP_RANK"] = str(node_rank)
        os.environ["RANK"] = str(local_rank + node_rank * nprocs)
        os.environ["LOCAL_RANK"] = str(local_rank)
        os.environ["WORLD_SIZE"] = str(num_nodes * nprocs)
        os.environ["LOCAL_WORLD_SIZE"] = str(nprocs)
        os.environ["TORCHELASTIC_RUN_ID"] = "1"

        # Used to force Lite to setup the distributed environnement.
        os.environ["LT_CLI_USED"] = "1"

        # Used to pass information to Lite directly.
        def pre_fn(lite, *args, **kwargs):
            kwargs["devices"] = nprocs
            kwargs["num_nodes"] = num_nodes
            kwargs["accelerator"] = "auto"
            strategy = kwargs.get("strategy", None)
            if strategy:
                if isinstance(strategy, str):
                    if strategy == "ddp_spawn":
                        strategy = "ddp"
                    elif strategy == "ddp_sharded_spawn":
                        strategy = "ddp_sharded"
                elif isinstance(strategy, (DDPSpawnStrategy, DDPSpawnShardedStrategy)):
                    raise Exception("DDP Spawned strategies aren't supported yet.")
            return {}, args, kwargs

        tracer = Tracer()
        tracer.add_traced(LightningLite, "__init__", pre_fn=pre_fn)
        tracer._instrument()
        work_run()
        tracer._restore()


class LiteMultiNode(MultiNode):
    def __init__(
        self,
        work_cls: Type["LightningWork"],
        cloud_compute: "CloudCompute",
        num_nodes: int,
        *work_args: Any,
        **work_kwargs: Any,
    ) -> None:
        assert issubclass(work_cls, _LiteWorkProtocol)
        if not is_static_method(work_cls, "run"):
            raise TypeError(
                f"The provided {work_cls} run method needs to be static for now."
                "HINT: Remove `self` and add staticmethod decorator."
            )

        # Note: Private way to modify the work run executor
        # Probably exposed to the users in the future if needed.
        work_cls._run_executor_cls = _LiteRunExecutor

        super().__init__(
            work_cls,
            *work_args,
            num_nodes=num_nodes,
            cloud_compute=cloud_compute,
            **work_kwargs,
        )
