# arXiv Paper Downloader
A Python-based command-line tool for downloading research papers from arXiv based on search queries. This tool was originally developed to facilitate literature review for academic research at Nanyang Technological University.

## Tested on
![Python](https://img.shields.io/badge/Python-3.10%2C%203.11-green)
![Apple](https://img.shields.io/badge/Apple-i7%2C%20M1%2C%20M2%20Pro%2C%20M3%20Pro-green)
![Windows](https://img.shields.io/badge/Windows-10%2C%2011-green)

## Features

- Search and download papers from arXiv using multiple search queries
- Customisable search parameters (results per page, max results, sorting criteria)
- PDF to Markdown conversion capability
- Colored console output with timestamps for better logging
- Configurable delay between requests to respect arXiv's servers
- Automatic retry mechanism for failed downloads
- Type-annotated codebase for better development experience
- Comprehensive documentation with example usage

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/AmirYunus/arxiv_scraper
    cd arxiv_scraper
    ```

2. Create and activate a Conda environment:
    ```bash
    conda create --prefix=venv python=3.11 -y
    conda activate ./venv
    ```

3. Install required dependencies:
    ```bash
    python -m pip install -r requirements.txt
    ```

## Usage

Basic usage example:
```bash
python main.py --query_list "quantum computing" "machine learning"
```

### Command-line Arguments

- `--query_list`: List of search queries (required)
- `--markdown`: Convert PDFs to Markdown format (default: False)
- `--page_size`: Number of results per page (default: 100)
- `--delay_seconds`: Delay between requests in seconds (default: 10)
- `--num_retries`: Number of retry attempts for failed requests (default: 5)
- `--max_results`: Maximum number of results per query (default: 10)
- `--sort_by`: Sort results by ["relevance", "last_updated_date", "submitted_date"] (default: "relevance")

### Advanced Usage Example
```bash
python main.py \
--query_list "quantum computing" "machine learning" \
--markdown True \
--page_size 50 \
--delay_seconds 5 \
--num_retries 3 \
--max_results 20 \
--sort_by last_updated_date
```

## Output Structure

The downloaded papers are organized in the following structure:
```
project_root/
├── pdfs/
│ ├── quantum_computing/
│ │ ├── paper1.pdf
│ │ └── paper2.pdf
│ └── machine_learning/
│ ├── paper3.pdf
│ └── paper4.pdf
└── mds/
│ ├── quantum_computing/
│ │ ├── paper1.md
│ │ └── paper2.md
│ └── machine_learning/
│ │ ├── paper3.md
│ │ └── paper4.md
```

## Contributing

We welcome contributions! Our codebase follows these standards:

### Code Style
- Type annotations for all functions and classes
- Docstrings with example usage for all public methods
- Inline comments for complex logic
- PEP 8 style guidelines

Example of expected code style:
```python
def process_paper(paper: arxiv.Result, similarity_score: float) -> dict[str, Any]:
    """Process an arXiv paper and return its metadata with similarity score.
    
    Args:
    paper (arxiv.Result): The paper result from arXiv API
    similarity_score (float): Cosine similarity score between query and paper
    
    Returns:
    dict[str, Any]: Processed paper metadata including similarity score
    
    Example usage:
    paper = next(arxiv.Search(query="quantum computing").results())
    result = process_paper(paper, 0.85)
    """
    return {
        "title": paper.title,
        "similarity": similarity_score,
        # ... other metadata
        }
```

### How to Contribute

1. **Fork the Repository**
   - Fork the repository to your GitHub account
   - Clone your fork locally

2. **Create a Branch**
   - Create a branch for your feature or bug fix
   - Use descriptive branch names (e.g., `feature/pdf-preview` or `fix/download-retry`)

3. **Make Changes**
   - Write clean, documented code
   - Follow PEP 8 style guidelines for Python code
   - Add comments where necessary

4. **Submit Changes**
   - Push your changes to your fork
   - Create a Pull Request with a clear description of the changes
   - Link any related issues

## Community and Support

- **Issues**: Use GitHub Issues for bug reports and feature requests
- **Discussions**: Join the GitHub Discussions for general questions and community interaction
- **Sponsorship**: Support this project through GitHub Sponsors

## Dependencies

- arxiv==2.1.3
- colorama==0.4.6
- pypdf==5.1.0

## Citation

If you use this tool in your research, please cite it as:

Amir Yunus, "arXiv Paper Downloader," GitHub repository, 2024. [Online]. 
Available: https://github.com/AmirYunus/arxiv_scraper


BibTeX format:
@misc{yunus2024arxiv,
author = {Yunus, Amir},
title = {arXiv Paper Downloader},
year = {2024},
publisher = {GitHub},
journal = {GitHub repository},
howpublished = {\url{https://github.com/AmirYunus/arxiv_scraper}}
}

## Contact

- **Maintainer**: Amir Yunus
- **GitHub**: [@AmirYunus](https://github.com/AmirYunus)

For questions, suggestions, or issues, please use the GitHub Issues section of this repository.

## License

MIT License

Copyright (c) 2024 Amir Yunus

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Acknowledgements

- This project was developed as part of academic research at Nanyang Technological University
- Built using the [arXiv API](https://arxiv.org/help/api/index) for academic paper access
- Thanks to the maintainers of the following libraries:
  - arxiv
  - pypdf
  - colorama