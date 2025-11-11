# Virtual environment (Windows PowerShell) — quick setup

Open PowerShell in the project folder and run:

```powershell
# create venv
python -m venv .venv

# activate venv (PowerShell)
.\.venv\Scripts\Activate.ps1

# install packages from requirements (if any)
pip install -r requirements.txt
```

Notes:
- If PowerShell blocks script execution, run: `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned` (may require admin privileges).
- Use `deactivate` to leave the venv.
- Keep a `requirements.txt` file to track dependencies.
