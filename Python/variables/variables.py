from RPA.Robocorp.Vault import Vault

_secret = Vault().get_secret("sparebin")

sparebin_url = _secret["website_url"]