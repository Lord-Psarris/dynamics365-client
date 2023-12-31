# Dynamics 365 MS Client

The client helps integrations with ms services apis like the dynamics crm api

## Installation

- Make sure you have Python 3.7+ installed on your system.

- Create and setup a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate
```

- Install the package via the repo using pip:

```shell
pip install --upgrade pip && pip install wheel
pip install git+https://github.com/Lord-Psarris/dynamics365-client.git
```

## Usage

```python
from dynamics365_client import MicrosoftServicesClient

client = MicrosoftServicesClient(environment_url="<dynamics-crm-url>", email="<sso-email>", password="<sso-password>",
                                 client_id="<azure-app-registration-client-id>",
                                 client_secret="<azure-app-registration-client-secret>", tenant_id="<azure-tenant-id>")

# get item from dynamics
print(client.get("leads"))

# get items using id
print(client.get("leads", "0000000-0000-0000-00000000000"))
```

## Contributing

We welcome contributions to improve the application. To contribute, follow these steps:

- Fork the repository and create your branch:
```bash
git checkout -b feature/your-feature-name
```

-Make your changes and commit them:
```bash
git commit -m "Add your message here"
```

-Push to your branch:
```bash
git push origin feature/your-feature-name
```

-Finally, create a pull request on GitHub.

## Issues and Bug Reports

If you encounter any issues or bugs with the application, please open a new issue on this repository.

## License

...
