# pyincus

An asynchronous Python SDK for Incus, built to help you manage containers, virtual machines, networks, and storage volumes with a clean, modern API.

`pyincus` is designed for building scalable applications that interact with Incus, leveraging Python's `asyncio` for non-blocking I/O operations.

## Features

* **Asynchronous:** Fully built on `asyncio` for high performance and concurrency.

* **Comprehensive API:** Manage all core Incus resources, including:

  * Containers and Virtual Machines

  * Networks

  * Storage Pools and Volumes

  * Images

  * Profiles

* **Object-Oriented:** A simple and intuitive interface where Incus resources are represented as Python objects.

* **Extensible:** Easily integrate with other asynchronous libraries and frameworks.

## Installation

You can install `pyincus` directly from PyPI using `pip`:
```bash
pip install pyincus
```

## Quick Start

The following example demonstrates how to connect to an Incus server and asynchronously list all containers.
```python
import asyncio
from pyincus import Client

async def main():
    # Initialize the Incus client.
    # The client will automatically attempt to find the Incus socket.
    # You can also pass the URL and credentials explicitly.
    try:
        client = Client()

        # Connect to the Incus server.
        await client.connect()

        # Get a list of all containers.
        containers = await client.containers.all()

        # Print the names of the containers.
        if containers:
            print("Found the following containers:")
            for container in containers:
                print(f"- {container.name}")
        else:
            print("No containers found.")

    except Exception as e:
        print(f"An error occurred: {e}")

if name == "main":
    asyncio.run(main())
```

## Documentation

For a detailed API reference, usage examples, and advanced topics, please refer to the [official documentation](https://projects.edmilsonrodrigues/pyinucs).

## Contributing

We welcome contributions! Please use [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/) for all your commit messages.

If you'd like to contribute, please follow these steps:

1. Fork the repository and clone it locally.

2. Install the `pre-commit` hook:
```bash
pre-commit install
```

3. Run the following commands to set up your environment and ensure basic checks pass:
```bash
make setup
make lint
make static
```

4. Depending on the nature of your changes, run the appropriate tests before pushing:

* For changes in an isolated part of the project, run the unit tests with `make test-unit`.

* For changes that affect a more important part of the project, run the full test suite with `make test`.

* For documentation changes, run `make docs` to see a preview of your changes before committing.

5. **If you are adding a new feature, please create appropriate tests for it inside the `tests/` directory.**

6. If all checks pass, create a new branch for your feature (`git checkout -b feature/your-feature-name`).

7. Commit your changes (`git commit -m 'feat: Add a new feature'`).

8. Push to the branch (`git push origin feature/your-feature-name`).

9. Open a Pull Request.

Please ensure your code follows the project's style guidelines and includes appropriate tests.

## License

This project is licensed under the [MPL2](https://www.mozilla.org/en-US/MPL/2.0/) License - see the `LICENSE` file for details.

*Built with ❤️ by the pyincus community.*
