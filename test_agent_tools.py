from app.tools.order_tool import OrderLookupTool
from app.tools.ticket_tool import TicketTool
from app.tools.user_tool import UpdateAddressTool


def main() -> None:
    print("ORDER:", OrderLookupTool().lookup("1234"))
    print(
        "TICKET:",
        TicketTool().create_ticket(
            "delivery_issue",
            "Package damaged",
            "u001",
        ),
    )
    print("UPDATE:", UpdateAddressTool().update("u001", "New Street 45"))


if __name__ == "__main__":
    main()

