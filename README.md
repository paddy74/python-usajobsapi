# python-usajobsapi

A Python wrapper for the [USAJOBS REST API](https://developer.usajobs.gov/). The library aims to provide a simple interface for discovering and querying job postings from USAJOBS using Python.

## Features

- Lightweight client for the USAJOBS REST endpoints
- Easily search for job postings with familiar Python types
- No external dependencies required

## Installation

### From PyPI

```bash
pip install python-usajobsapi
```

### From source

```bash
git clone https://github.com/your-username/python-usajobsapi.git
cd python-usajobsapi
pip install .
```

## Usage

Register for a USAJOBS API key and set a valid User-Agent before making requests.

```python
from usajobsapi import USAJobs

client = USAJobs(user_agent="name@example.com", api_key="YOUR_API_KEY")
results = client.search_jobs(keyword="data scientist", location="Remote")
for job in results:
    print(job["Title"])
```

## Contributing

Contributions are welcome! To get started:

1. Fork the repository and create a new branch.
2. Create a virtual environment and install development dependencies.
3. Run the test suite with `pytest` and ensure all tests pass.
4. Submit a pull request describing your changes.

Please open an issue first for major changes to discuss your proposal.

## License

Distributed under the GNU General Public License v3.0. See [LICENSE](LICENSE) for details.

## Project Status

This project is under active development and the API may change. Feedback and ideas are appreciated.

## Contact

Questions or issues? Please open an issue on the repository's issue tracker.
