# Lightning & Multi Node Training

Lightning supports makes multi-node training simple by providing a simple interface to orchestrate compute and data.

## Multi Node with raw PyTorch

You can run the multi-node raw PyTorch by running the following commands.

Here is an example where you spawn your processes yourself.

```bash
lightning run app train_pytorch.py
```

or you can use the built-in component for it.

```bash
lightning run app train_pytorch_spawn.py
```

## Multi Node with raw PyTorch + Lite

You can run the multi-node raw PyTorch and Lite by running the following commands.

```bash
lightning run app train_lite.py
```

Using Lite, you retain control over your loops while accessing in a minimal way all Lightning distributed strategies.

## Multi Node with PyTorch Lightning

Lightning supports running PyTorch Lightning from a script or within a Lightning Work.

You can either run a script directly

```bash
lightning run app train_pl_script.py
```

or run your code within as a work.

```bash
lightning run app train_pl.py
```

## Multi Node with any frameworks

```bash
lightning run app train_any.py
```
