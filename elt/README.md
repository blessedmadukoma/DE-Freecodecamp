Automation using dbt

### To run the project:
1. set environmental variables in both the parent folder (.) and `elt` folder.
2. set and activate python environment: 
  - `python3 -m venv env`
  - `source env/bin/activate`
3. Install requirements.txt: `pip install -r requirements.txt`

Note:
- To generate the fernet key: `python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"`