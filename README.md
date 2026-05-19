# ITNE352Project: Recipe discovery Client-Server System

**Created by:** Ayman Hameed Abdulla (20184015)
**Supervised by:** Dr. Mohammed Almeer

---

## 1. Project Overview
This project is a multi-threaded Client-Server system designed to browse food recipes using TheMealDB API.

## 2. Architecture
- **Server:** Handles multiple clients using multithreading, manages a local cache for reference data, and logs recipe requests to JSON files.
- **Client:** A menu interface with input validation.
- **API Handler:** A dedicated class (`meal_api.py`) for managing internet requests.

## 3. Additional Concept Implemented
Beyond the core network programming specifications, the system incorporates the following software design paradigms:
* **Object-Oriented Programming (OOP)** to organize our server and API logic into reusable classes, ensuring high maintainability and clean code.
* **Robust Network Data Reassembly:** Implemented a chunk-based buffer accumulation algorithm (`recv_all`) on the client to securely process variable-length application data streams over TCP.
* **Local Caching Layer:** Minimizes unnecessary network overhead by caching static structural data (categories, geographic areas, ingredients) locally during the server's boot sequence.

## 4. How to Run
1. Install dependencies: `pip install requests`
2. Run the server: `python server.py`
3. Run the client: `python client.py`