import mintapi
import os
from dotenv import load_dotenv

class MintConnection(object):
    def __init__(self):
        load_dotenv()
        self.mint = None

    def startMintConn(self) -> mintapi.Mint:
        username = os.getenv("MINT_USER")
        password = os.getenv("MINT_PASS")
        imap_account = os.getenv("IMAP_ACCOUNT")
        imap_password = os.getenv("EMAIL_PASS")
        
        mint = mintapi.Mint(
            username,
            password,
            mfa_method="email",
            headless = True,
            fail_if_stale=True,
            wait_for_sync=False,
            wait_for_sync_timeout=500,
            imap_account=imap_account,
            imap_password=imap_password,
            imap_server="imap.gmail.com",
            imap_folder="INBOX",
        )
        mint.rest_client
        self.mint = mint
        return mint
    
    def getMintConn(self) -> mintapi.Mint:
        return self.mint

    def closeMintConn(self):
        self.mint.close()
