# v0.2.16
# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
from genlayer import *

class Contract(gl.Contract):
    """
    Mock USDC contract for GenLayer testing.
    Implements a basic ERC20-like interface to handle audit fees and whistleblower bounties.
    """
    balances: TreeMap[Address, u256]
    allowances: TreeMap[str, u256] # Composite key: "{owner_str}-{spender_str}"
    total_supply: u256
    name: str
    symbol: str
    decimals: u256

    def __init__(self):
        # Rule #2: DO NOT reassign TreeMap or DynArray in __init__
        self.total_supply = u256(100000000000000)  # 100M tokens * 10^6 decimals
        self.name = "Mock USD Coin"
        self.symbol = "USDC"
        self.decimals = u256(6)
        
        # Mint initial supply to the deployer
        self.balances[gl.message.sender_address] = self.total_supply

    @gl.public.view
    def balanceOf(self, account: Address) -> u256:
        """
        Returns the balance of the given account.
        """
        if account in self.balances:
            return self.balances[account]
        return u256(0)

    @gl.public.view
    def allowance(self, owner: Address, spender: Address) -> u256:
        """
        Returns the amount of tokens the spender is allowed to withdraw from the owner.
        """
        key = f"{str(owner)}-{str(spender)}"
        if key in self.allowances:
            return self.allowances[key]
        return u256(0)

    @gl.public.write
    def transfer(self, recipient: Address, amount: int) -> bool:
        """
        Transfers tokens from the sender to the recipient.
        Rule #3 & #4: Float is prohibited, using `int`.
        """
        sender = gl.message.sender_address
        sender_balance = self.balanceOf(sender)
        u_amount = u256(amount)

        if sender_balance < u_amount:
            return False

        self.balances[sender] = sender_balance - u_amount
        self.balances[recipient] = self.balanceOf(recipient) + u_amount
        return True

    @gl.public.write
    def approve(self, spender: Address, amount: int) -> bool:
        """
        Approves the spender to transfer tokens from the sender's balance up to the given amount.
        """
        owner = gl.message.sender_address
        key = f"{str(owner)}-{str(spender)}"
        self.allowances[key] = u256(amount)
        return True

    @gl.public.write
    def transferFrom(self, sender: Address, recipient: Address, amount: int) -> bool:
        """
        Transfers tokens from the sender to the recipient using the allowance mechanism.
        """
        spender = gl.message.sender_address
        key = f"{str(sender)}-{str(spender)}"
        current_allowance = self.allowance(sender, spender)
        sender_balance = self.balanceOf(sender)
        u_amount = u256(amount)

        if current_allowance < u_amount or sender_balance < u_amount:
            return False

        # Update allowance
        self.allowances[key] = current_allowance - u_amount
        
        # Update balances
        self.balances[sender] = sender_balance - u_amount
        self.balances[recipient] = self.balanceOf(recipient) + u_amount
        return True

    @gl.public.write
    def mint(self, account: Address, amount: int) -> bool:
        """
        Mints new tokens to the specified account. (For testing purposes)
        """
        u_amount = u256(amount)
        self.balances[account] = self.balanceOf(account) + u_amount
        self.total_supply += u_amount
        return True
