
# The Fields Institute Cybersecurity Fundamentals

A curated collection of projects, exercises, and resources completed as part of the **Fields Institute Cybersecurity Fundamentals** program.  
Covers Linux, Python, Mathematics, and Networking — blending theoretical foundations with hands‑on implementation.

---

## 📑 Table of Contents
- [📂 Repository Structure](#-repository-structure)
- [🐧 Linux Project — Command‑Line Password Manager](#-linux-project--command-line-password-manager-bash--openssl)
- [🐍 Python Project — Android Swipe Pattern Assignment](#-python-project--android-swipe-pattern-assignment)
- [📐 Mathematics Projects — Number Theory, Algebra, Probability & Cryptography](#-mathematics-projects--number-theory-algebra-probability--cryptography-python)
- [🌐 Networking Projects — Socket Programming Assignments](#-networking-projects--socket-programming-assignments)
- [📜 License](#-license)
- [📬 Author](#-author)

---

## 📂 Repository Structure

fields_cyber_fundamentals/
├── linux/                  # Linux fundamentals & projects
├── python/                 # Python programming & applied exercises
├── mathematics/            # Computational mathematics & cryptography
├── computer_networks/      # Networking & socket programming
├── requirements.txt        # Python dependencies
├── .pre-commit-config.yaml # Formatting hooks
├── LICENSE                 # MPL-2.0 License
└── README.md               # Project documentation


---

## 🐧 Linux Project — Command‑Line Password Manager (Bash + OpenSSL)

Built a command‑line password manager in **Bash** using **OpenSSL** for secure storage and retrieval of account passwords protected by a master password.

Implemented:
- `openssl enc` for encryption/decryption of stored credentials  
- `openssl passwd` for secure hashing of the master password  
- `openssl rand` for cryptographically secure random password generation  

Delivered a fully functional script with setup instructions, usage guide, and documentation of the development approach.  
Suitable for personal use on a local Linux machine, with recommendations for further security enhancements.

---

## 🐍 Python Project — Android Swipe Pattern Assignment

Implemented a full set of Python functions to model, validate, and analyze **Android‑style swipe patterns** on a 3×3 grid of nodes (0–8).

Key features:
- **Grid mapping** — `row(i)` and `col(i)` functions to map node indices to grid coordinates.
- **Intermediate node detection** — logic to prevent “jumping over” unvisited nodes.
- **Pattern validation** — `is_admissible()` to check if a node can be appended to an existing pattern.
- **Pattern extension** — `extensions()` to generate all valid one‑step continuations.
- **Pattern generation** — `generate_patterns()` to enumerate all patterns of lengths 0–9.
- **Combinatorial analysis** — counted patterns meeting specific constraints.
- **Visualization tools** — plotted patterns using `matplotlib`.
- **Advanced exploration** — optional complexity metrics and isooptic equivalence classification.

Delivered:
- Well‑documented `.py` implementation
- Written explanation of approach for each exercise
- Support for both functional testing and exploratory analysis

---

## 📐 Mathematics Projects — Number Theory, Algebra, Probability & Cryptography (Python)

Completed a series of Python‑based exercises applying core mathematical concepts to computational problem‑solving in:

- **Elementary Number Theory** — divisibility, modular arithmetic, prime generation, GCD, modular inverses.
- **Abstract Algebra** — group operations, cyclic groups, permutations, and basic ring/field properties.
- **Basic Probability** — discrete probability distributions, combinatorics, expectation, variance, and simulations.
- **Cryptography** — classical ciphers, RSA key generation and encryption/decryption, modular exponentiation, and simple cryptanalysis.

Each topic includes:
- Well‑structured Python scripts demonstrating algorithms and proofs‑by‑computation.
- Clear documentation of the mathematical approach and reasoning.
- Worked examples and test cases to verify correctness.

---

## 🌐 Networking Projects — Socket Programming Assignments

Completed a series of hands‑on networking assignments using **Python socket programming** to build and test core client‑server applications:

- **Web Server** — Implemented an HTTP server capable of handling basic GET requests and serving static content.
- **UDP Pinger** — Built a UDP‑based client to send echo requests and measure round‑trip times, handling packet loss and timeouts.
- **Mail Client** — Developed an SMTP client to send email messages programmatically, including proper message formatting and server interaction.
- **Web Proxy** — Created a proxy server to forward HTTP requests, cache responses, and filter content.

Reinforced:
- Low‑level socket API usage (`socket`, `bind`, `listen`, `accept`, `send`, `recv`)
- TCP vs. UDP communication patterns
- Protocol‑specific message formatting (HTTP, SMTP)
- Error handling, timeouts, and connection management

---

## 📜 License

This repository is licensed under the [MPL‑2.0 License](LICENSE).

---

## Contributing
This project uses pre-commit to ensure code formatting is consistent before committing. The currently-used hooks are:

- black for *.py or *.ipynb files.
- prettier (with --prose-wrap always for markdown)

To set up the hooks on your local machine, install pre-commit, then run pre-commit install to install the formatters that will run before each commit.

## 📬 Author

**Leonard Okyere Afeke**  
GitHub: [git-loa](https://github.com/git-loa)  
LinkedIn: [leonard-afeke](https://linkedin.com/in/leonard-afeke)
